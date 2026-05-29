# Khai bao ma hoa file Python
# -*- coding: utf-8 -*-

from odoo import fields, models
from odoo.exceptions import UserError


class X0502DocumentPackWizard(models.TransientModel):
    _name = "x_psm_0502_document_pack_wizard"
    _description = "0502 Document Pack Wizard"

    # field lien ket wizard voi maintenance request dang can in bo chung tu
    x_psm_request_id = fields.Many2one(
        "maintenance.request",
        string="Maintenance Request",
        required=True,
        readonly=True,
        help="0502 maintenance request used to generate the selected document pack.",
    )

    x_psm_include_request_document = fields.Boolean(
        string="Request Document",
        default=True,
        help="Include the full 0502 request document in the pack.",
    )
    x_psm_include_inspection_report = fields.Boolean(
        string="Inspection Report",
        default=True,
        help="Include the initial inspection report in the pack.",
    )
    x_psm_include_treatment_proposal = fields.Boolean(
        string="Treatment Proposal",
        default=True,
        help="Include the treatment proposal document in the pack.",
    )
    x_psm_include_material_issue_request = fields.Boolean(
        string="Material Issue Request",
        default=True,
        help="Include the material issue request in the pack.",
    )
    x_psm_include_acceptance_record = fields.Boolean(
        string="Acceptance Record",
        default=True,
        help="Include the acceptance record in the pack.",
    )

    def action_psm_print_document_pack(self):
        self.ensure_one()

        if not any([
            self.x_psm_include_request_document,
            self.x_psm_include_inspection_report,
            self.x_psm_include_treatment_proposal,
            self.x_psm_include_material_issue_request,
            self.x_psm_include_acceptance_record,
        ]):
            raise UserError("Please select at least one 0502 document to print.")

        self.x_psm_request_id._psm_assign_missing_document_numbers()
        return self.env.ref("M02_P0502.action_report_psm_0502_document_pack").report_action(self)
