# -*- coding: utf-8 -*-
from odoo import models, fields


class HrDisciplineExplanation(models.Model):
    _name = "x_psm.hr.discipline.explanation"
    _description = "Discipline Explanation Entry"
    _order = "create_date desc"

    x_psm_record_id = fields.Many2one(
        "x_psm.hr.discipline.record",
        string="Discipline Record",
        required=True,
        ondelete="cascade",
    )
    sequence = fields.Integer(string="Lần thứ", default=1)

    # Explanation content
    x_psm_incident_date_time = fields.Datetime(string="Thời gian xảy ra sự việc")
    x_psm_incident_location = fields.Char(string="Địa điểm")
    x_psm_witness_names = fields.Char(string="Người làm chứng")
    x_psm_explanation_content = fields.Text(string="Nội dung tường trình")
    x_psm_explanation_reason = fields.Text(string="Nguyên nhân")
    x_psm_explanation_commitment = fields.Text(string="Cam kết")
    x_psm_employee_signature = fields.Binary(string="Chữ ký")

    # Status
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("submitted", "Submitted"),
            ("rejected", "Rejected"),
            ("accepted", "Accepted"),
        ],
        default="draft",
        string="Trạng thái",
    )

    x_psm_rejection_reason = fields.Text(string="Lý do từ chối")
    x_psm_submitted_date = fields.Datetime(string="Ngày gửi")
    x_psm_reviewed_date = fields.Datetime(string="Ngày review")
    x_psm_reviewed_by = fields.Many2one("res.users", string="Người review")
