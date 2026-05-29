# -*- coding: utf-8 -*-
import sys
from datetime import timedelta
from odoo import api, fields, SUPERUSER_ID

# Since we are running this in the Odoo shell, 'self' is the shell environment object.
# The variable 'self' has self.env bound.

print("=== STARTING PAF & PIF WORKFLOW VERIFICATION (PHASE 6) ===")

# 1. Retrieve template
template = self.env['mkt_paf.template'].search([], limit=1)
if not template:
    print("ERROR: No PAF Template found!")
    sys.exit(1)
print("Using PAF Template: %s (Code: %s)" % (template.name, template.code))

# 2. Make sure we have a product template that can be used in PAF
product_tmpl = self.env['product.template'].search([('paf_can_use', '=', True)], limit=1)
if not product_tmpl:
    # Set standard product to paf_can_use
    product_tmpl = self.env['product.template'].search([], limit=1)
    if product_tmpl:
        product_tmpl.paf_can_use = True
        print("Set product.template '%s' paf_can_use=True" % product_tmpl.name)
    else:
        # Create a new product template
        product_tmpl = self.env['product.template'].create({
            'name': 'Test PAF Product',
            'paf_can_use': True,
            'standard_price': 10.0,
        })
        print("Created new product.template '%s'" % product_tmpl.name)

# Find its product.product variant
product_product = self.env['product.product'].search([('product_tmpl_id', '=', product_tmpl.id)], limit=1)
if not product_product:
    product_product = self.env['product.product'].create({
        'product_tmpl_id': product_tmpl.id,
    })
    print("Created product.product for '%s'" % product_tmpl.name)

# Ensure required_dept_evaluation is set on template
if not template.required_dept_evaluation:
    depts = self.env['hr.department'].search([], limit=5)
    template.required_dept_evaluation = [(6, 0, depts.ids)]
    print("Added departments to template required_dept_evaluation: %s" % str(depts.mapped('name')))

# 3. Create a PAF Request
paf = self.env['mkt_paf.request'].create({
    'template_id': template.id,
    'planned_start_date': fields.Date.today() + timedelta(days=30),
    'planned_end_date': fields.Date.today() + timedelta(days=60),
    'forecast_revenue': 1000.0,
    'product_ids': [(6, 0, [product_tmpl.id])],
})
print("Created PAF Request: %s (State: %s)" % (paf.name, paf.state))

# 4. Progress to evaluation
paf.action_submit_to_evaluation()
print("PAF Request state after submit to evaluation: %s" % paf.state)
print("Evaluation lines created: %d" % len(paf.evaluation_line_ids))

# 5. Complete all evaluations
for line in paf.evaluation_line_ids:
    print("Completing evaluation for department: %s (Code: %s)" % (line.department_id.name, line.department_code))
    line.action_start_review()
    # Fill in required fields depending on department
    if line.department_code == 'si':
        line.forecast_demand = 100.0
        line.confidence_score = 0.8
    elif line.department_code == 'ops':
        line.pilot_capacity_score = 'medium'
    elif line.department_code == 'finance':
        line.roi_estimated_percent = 15.0
        line.gross_margin_estimated = 200.0
    elif line.department_code == 'sc':
        line.supply_risk_level = 'low'
        line.lead_time_days = 5
    elif line.department_code == 'legal':
        line.regulatory_sla_days = 7
        line.requires_government_approval = False
        line.scheme_compliant = True
    line.action_submit_done()

print("Evaluation progress: %f%%" % paf.evaluation_progress)
print("PAF Request state after evaluations: %s" % paf.state)

# If not automatically collected, call action_collect_evaluations
if paf.state == 'dept_evaluation':
    paf.action_collect_evaluations()

print("PAF Request state after collecting evaluations: %s" % paf.state)
print("Head Approval Request: %s (Status: %s)" % (paf.head_approval_request_id.name, paf.head_approval_request_id.request_status))

# 6. Approve Head request
paf.head_approval_request_id.action_approve()
print("PAF Request state after Head approve: %s" % paf.state)
print("C-Level Approval Request: %s (Status: %s)" % (paf.clevel_approval_request_id.name, paf.clevel_approval_request_id.request_status))

# 7. Approve C-Level request
paf.clevel_approval_request_id.action_approve()
print("PAF Request state after C-Level approve: %s" % paf.state)

# 8. Check that M08 PIF approval request was triggered.
pif_request = self.env['approval.request'].search([
    ('x_psm_mkt_paf_request_id', '=', paf.id),
    ('x_psm_0801_pif_request_type', '=', 'marketing'),
], limit=1)
if not pif_request:
    print("ERROR: M08 PIF approval request not created!")
    sys.exit(1)
print("M08 PIF approval request: %s (Status: %s)" % (pif_request.name, pif_request.request_status))
if pif_request.x_psm_0801_pif_object_id:
    print("WARNING: Marketing PIF request was already approved/fast-tracked unexpectedly")

# 9. Verify state transitions to 'pif_running'
if paf.state != 'pif_running':
    print("ERROR: PAF state is %s, expected 'pif_running'" % paf.state)
    sys.exit(1)

# 10. Open Valuation
action = paf.action_open_valuation()
print("Opened valuation report. Action details: %s" % str(action))

# Find created report
report = self.env['mkt_paf.valuation.report'].search([('paf_request_id', '=', paf.id)], limit=1)
if not report:
    print("ERROR: Valuation report was not created!")
    sys.exit(1)
print("Found Valuation Report: %s (Status: %s)" % (report.id, report.status))

# Update report details
report.actual_revenue = 1200.0
report.actual_cost = 900.0
report._compute_valuation_stats()
print("Valuation Report Stats - ROI: %f%%, Variance: %f%%" % (report.actual_roi_percent, report.variance_vs_forecast))

# Publish valuation report
report.action_publish()
print("Valuation Report published (Status: %s)" % report.status)
print("Final PAF state: %s" % paf.state)

if paf.state == 'done':
    print("SUCCESS: Workflow end-to-end verification passed successfully!")
else:
    print("ERROR: Final PAF state is %s, expected 'done'" % paf.state)
    sys.exit(1)
