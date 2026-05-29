from odoo import fields, models


class HrDepartment(models.Model):
    # ke thua hr.department de cau hinh partner dai dien cho cua hang/phong ban
    # partner nay se duoc map sang Customer tren FSM task o buoc 9
    _inherit = "hr.department"

    # field lien ket department voi partner dai dien de tao field service task khong can chon tay Customer
    # field tao moi quan he nhieu mot toi model khach hang
    # co nhieu department co the thuoc mot partner
    # moi partner co the dai dien cho nhieu department
    x_psm_0502_partner_id = fields.Many2one(
        # model se duoc map sang
        "res.partner",
        # label hien thi tren giao dien
        string="0502 FSM Customer",
        # khong cho phep thay doi du lieu tu department ma phai thay doi tu partner
        ondelete="restrict",
        # toolip khi hover vao field
        help="Customer/partner automatically mapped to FSM tasks created from 0502 maintenance requests.",
    )

    # field cau hinh user ben store la nguoi duyet buoc 12 cho request phat sinh tu phong ban/cua hang nay
    x_psm_0502_proposal_approver_id = fields.Many2one(
        "res.users",
        string="0502 Store Proposal Approver",
        tracking=True,
        domain="[('share', '=', False)]",
        help="Preferred store-side user to approve the 0502 treatment proposal for requests raised by this department.",
    )

    # field cau hinh nguoi duyet cap cuoi ben store neu doanh nghiep can 2 cap duyet o buoc 12
    # phase 3 chi bo sung them 1 cap cuoi tuy chon, khong tao approval engine chung
    x_psm_0502_proposal_final_approver_id = fields.Many2one(
        "res.users",
        string="0502 Store Final Approver",
        tracking=True,
        domain="[('share', '=', False)]",
        help="Optional final store-side approver for the 0502 proposal when the business requires a second approval level.",
    )
