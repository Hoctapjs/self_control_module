# -*- coding: utf-8 -*-
import sys
from datetime import timedelta
from odoo import api, fields

print('=== PHASE 6 VERIFICATION START ===')

# Ensure we have enough approvers for head category
Category = env['approval.category']
HeadCat = env.ref('M09_0901.mkt_0901_approval_category_paf_head')
if not HeadCat:
    print('ERROR: Head approval category not found')
    sys.exit(1)
existing = HeadCat.user_ids
needed = 5 - len(existing)
if needed > 0:
    print(f'Adding {needed} dummy approvers to head category')
    for i in range(needed):
        login = f'paf_approver_{i+1}'
        user = env['res.users'].search([('login', '=', login)], limit=1)
        # Use existing internal users or fallback to admin
        user = env['res.users'].search([('login', '=', login)], limit=1)
        if not user:
            user = env.ref('base.user_admin')
        HeadCat.write({'user_ids': [(4, user.id)]})
        print(f'Added user {login} to head approvers')
else:
    print('Head category already has sufficient approvers')

# Retrieve a template
Template = env['mkt_paf.template'].search([], limit=1)
if not Template:
    print('ERROR: No PAF template found')
    sys.exit(1)

# Ensure product
ProductTmpl = env['product.template'].search([('paf_can_use', '=', True)], limit=1)
if not ProductTmpl:
    ProductTmpl = env['product.template'].create({
        'name': 'PAF Test Product',
        'paf_can_use': True,
        'standard_price': 10.0,
    })
    print('Created test product template')

# Ensure required departments on template
if not Template.required_dept_evaluation:
    depts = env['hr.department'].search([], limit=5)
    Template.required_dept_evaluation = [(6, 0, depts.ids)]
    print('Set required_dept_evaluation on template')

# Create PAF request
paf = env['mkt_paf.request'].create({
    'template_id': Template.id,
    'planned_start_date': fields.Date.today() + timedelta(days=30),
    'planned_end_date': fields.Date.today() + timedelta(days=60),
    'forecast_revenue': 1000.0,
    'product_ids': [(6, 0, [ProductTmpl.id])],
})
print(f'Created PAF {paf.name} state={paf.state}')

# Submit to evaluation
paf.action_submit_to_evaluation()
print('Submitted to evaluation, state:', paf.state)

# Complete evaluations
for line in paf.evaluation_line_ids:
    line.action_start_review()
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
print('All evaluations done, state:', paf.state)

# Ensure head approval request has sufficient approvers before collection
head_req = paf.head_approval_request_id
if head_req:
    existing = head_req.approver_ids
    needed = head_req.approval_minimum - len(existing)
    if needed > 0:
        dummy_users = env['res.users'].search([], limit=needed)
        head_req.approver_ids = [(4, u.id) for u in dummy_users]
        print(f'Added {needed} dummy approvers to head request')
# Collect evaluations (if not auto)
if paf.state == 'dept_evaluation':
    paf.action_collect_evaluations()
print('After collecting, state:', paf.state)

# Approve head requests
head_req = paf.head_approval_request_id
if not head_req:
    print('ERROR: No head approval request')
    sys.exit(1)
head_req.action_approve()
print('Head approved, state:', paf.state)

# Approve C-level
clevel_req = paf.clevel_approval_request_id
if not clevel_req:
    print('ERROR: No C-level approval request')
    sys.exit(1)
clevel_req.action_approve()
print('C-level approved, state:', paf.state)

# Verify M08 PIF approval request was created and is waiting for RSG approval
pif_req = env['approval.request'].search([
    ('x_psm_mkt_paf_request_id', '=', paf.id),
    ('x_psm_0801_pif_request_type', '=', 'marketing'),
], limit=1)
if pif_req:
    print('M08 PIF approval request created:', pif_req.id, 'status:', pif_req.request_status)
else:
    print('ERROR: M08 PIF approval request not created')
    sys.exit(1)

# Open valuation
action = paf.action_open_valuation()
print('Valuation opened')
report = env['mkt_paf.valuation.report'].search([('paf_request_id', '=', paf.id)], limit=1)
if not report:
    print('ERROR: Valuation report not created')
    sys.exit(1)
report.actual_revenue = 1200.0
report.actual_cost = 900.0
report._compute_valuation_stats()
print('Report stats ROI:', report.actual_roi_percent, 'Variance:', report.variance_vs_forecast)
report.action_publish()
print('Report published, PAF final state:', paf.state)

if paf.state == 'done':
    print('SUCCESS: Phase 6 fully functional')
else:
    print('FAILURE: Final PAF state not done')
    sys.exit(1)
