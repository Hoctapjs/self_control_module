from odoo import models, fields


class HrDisciplineViolationCategory(models.Model):
    _name = "x_psm.hr.discipline.violation.category"
    _description = "Discipline Violation Category"

    name = fields.Char(string="Category Name", required=True)
    x_psm_code = fields.Char(string="Code")
