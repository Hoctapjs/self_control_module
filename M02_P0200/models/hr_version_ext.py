from odoo import models, fields, api
from dateutil.relativedelta import relativedelta

class HrVersion(models.Model):
    _inherit = 'hr.version'

    contract_kind_id = fields.Many2one('hr.contract.kind', string='Contract Kind', tracking=True)
    allowance_responsibility = fields.Monetary(string='Gross Responsibility allowance', groups="hr_payroll.group_hr_payroll_user")
    allowance_transportation = fields.Monetary(string='Gross Transportation allowance', groups="hr_payroll.group_hr_payroll_user")
    allowance_other = fields.Monetary(string='Gross Other allowance', groups="hr_payroll.group_hr_payroll_user")
    dependents_count = fields.Integer(string='Total Dependents', groups="hr.group_hr_user", tracking=True,
        help="Total number of dependents for PIT deduction (spouse, parents, children, etc.)")

    # New allowances for MCD (Versioned)
    x_psm_monthly_allowance = fields.Monetary(string='Monthly Allowance', groups="hr_payroll.group_hr_payroll_user", tracking=True)
    x_psm_attendance_allowance = fields.Monetary(string='Attendance Allowance', groups="hr_payroll.group_hr_payroll_user", tracking=True)
    x_psm_housing_allowance = fields.Monetary(string='Housing Allowance', groups="hr_payroll.group_hr_payroll_user", tracking=True)
    x_psm_hardshift_allowance = fields.Monetary(string='Hardshift Allowance', groups="hr_payroll.group_hr_payroll_user", tracking=True)
    x_psm_attraction_allowance = fields.Monetary(string='Attraction Allowance', groups="hr_payroll.group_hr_payroll_user", tracking=True)
