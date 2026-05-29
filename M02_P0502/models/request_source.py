from odoo import fields, models

# model master data cho request source

class X0502RequestSource(models.Model):
    # ten ky thuat cua model
    _name = "x_psm_request_source"

    # mo ta hien thi trong Odoo
    _description = "0502 Request Source"

    # quy tac sap xep mac dinh: theo sequence tang dan, neu sequence giong nhau thi sap xep theo id tang dan
    _order = "sequence, id"

    # ten hien thi cho user, duoc su dung trong giao dien nguoi dung va cac thong bao
    name = fields.Char(required=True, translate=True)

    # code ky thuat, duoc su dung de xac dinh duy nhat tung record trong model, khong duoc trung lap
    code = fields.Char(required=True)

    # thu tu sap xep, duoc su dung de xac dinh thu tu hien thi cua cac record trong giao dien nguoi dung, so nho hon se hien thi truoc
    sequence = fields.Integer(default=10)

    # cho phep active / inactive record, khi record bi inactive se khong hien thi trong giao dien nguoi dung va khong duoc su dung trong cac thao tac lien quan, nhung van duoc luu tru trong co so du lieu
    active = fields.Boolean(default=True)

    # rang buoc database: code phai unique, khong duoc trung lap, neu co loi nay thi se khong the luu record vao database va se hien thi thong bao loi "Request source code must be unique."
    _sql_constraints = [
        ("x_psm_request_source_code_unique", "unique(code)", "Request source code must be unique."),
    ]
