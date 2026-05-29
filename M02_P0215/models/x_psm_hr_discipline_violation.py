from odoo import models, fields


class HrDisciplineViolationType(models.Model):
    _name = "x_psm.hr.discipline.violation.type"
    _description = "Discipline Violation Type"

    name = fields.Char(string="Violation Name", required=True)
    x_psm_category_id = fields.Many2one(
        "x_psm.hr.discipline.violation.category", string="Category", required=True
    )
    x_psm_severity = fields.Selection(
        [
            ("minor", "Store Level (Nhẹ)"),
            ("major", "Company Level (Nặng)"),
        ],
        string="Mức độ hành vi",
        default="minor",
        required=True,
        help="Phân loại mức độ vi phạm để xác định cấp xử lý và quy trình.",
    )

    x_psm_improvement_period = fields.Integer(
        string="Improvement Period (Days)",
        default=30,
        help="Period to check for repeat offenses.",
    )
    x_psm_max_repeats = fields.Integer(
        string="Max Repeats",
        default=3,
        help="Maximum number of allowed repeats within the period before escalation.",
    )
