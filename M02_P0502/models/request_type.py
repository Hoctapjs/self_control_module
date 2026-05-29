from odoo import fields, models


class X0502RequestType(models.Model):
    # ten ky thuat cua model, dung de tham chieu trong code va domain
    _name = "x_psm_request_type"

    # mo ta hien thi cua model, dung de hien thi tren giao dien nguoi dung
    _description = "0502 Request Type"

    # sap xep theo truong sequence truoc, neu bang nhau thi sap xep tiep theo id
    _order = "sequence, id"

    # ten hien thi tren giao dien nguoi dung, la field name
    name = fields.Char(required=True, translate=True)

    # code ky thuat, dung trong logic, khong hien thi tren giao dien, phai nhap va phai duy nhat
    code = fields.Char(required=True)

    # thu tu hien thi trong danh sach, mac dinh la 10, so nho hon se hien thi truoc
    sequence = fields.Integer(default=10)

    # truong active de kich hoat hay ngung kich hoat loai request, mac dinh la kich hoat
    active = fields.Boolean(default=True)

    # huong dan intake mac dinh theo loai request de user biet can ghi nhan thong tin nao o phase 3 buoc 2
    x_psm_0502_intake_question_template = fields.Text(
        string="0502 Intake Question Template",
        help="Guidance template describing the standard intake questions for this 0502 request type.",
    )

    # ghi chu vi du de user tham khao cach ghi nhan thong tin ban dau gon va dung nghiep vu hon
    x_psm_0502_intake_example_note = fields.Text(
        string="0502 Intake Example Note",
        help="Example intake note for this 0502 request type.",
    )

    # template proposal theo loai su co de CMT co khung de xuat xu ly ro hon o phase 3 buoc 11
    x_psm_0502_proposal_template = fields.Text(
        string="0502 Proposal Template",
        help="Standard proposal template or guidance used when building a 0502 treatment proposal for this request type.",
    )

    # template mo ta cong viec/FSM execution package theo loai request de buoc 9 tao task co huong dan nhat quan hon
    x_psm_0502_fsm_task_template = fields.Text(
        string="0502 FSM Task Template",
        help="Standard task instruction template used when a 0502 FSM task is created from this request type.",
    )

    # checklist mau theo loai request de ky thuat vien co khung thuc thi nhat quan tren FSM task
    x_psm_0502_fsm_checklist_template = fields.Text(
        string="0502 FSM Checklist Template",
        help="Standard execution checklist template used when a 0502 FSM task is created from this request type.",
    )

    # goi y vat tu/chuan bi theo loai request de task co execution package ro hon ngay luc duoc tao
    x_psm_0502_fsm_material_template = fields.Text(
        string="0502 FSM Material Template",
        help="Standard material preparation template used when a 0502 FSM task is created from this request type.",
    )

    # ranh buoc du lieu: code phai duy nhat, khong duoc trung lap voi cac record khac trong cung model
    _sql_constraints = [
        ("x_psm_request_type_code_unique", "unique(code)", "Request type code must be unique."),
    ]
