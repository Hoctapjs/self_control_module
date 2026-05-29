import json

from odoo import models, fields, _


class PifObjectSsbiConnector(models.Model):
    _inherit = 'x_psm_pif_object'

    x_psm_ssbi_payload_json = fields.Text(string='Last SSBI Payload', readonly=True)
    x_psm_ssbi_pushed_date = fields.Datetime(string='Last SSBI Push Date', readonly=True)
    x_psm_ssbi_status = fields.Selection([
        ('not_sent', 'Not Sent'),
        ('queued', 'Queued'),
    ], string='SSBI Push Status', default='not_sent', readonly=True)

    def _prepare_ssbi_payload(self):
        self.ensure_one()
        return {
            'pif_id': self.name,
            'state': self.state,
            'request_type': self.x_psm_pif_request_type,
            'program': self.x_psm_program,
            'menu_item_code': self.x_psm_menu_item_code,
            'pmix_code': self.x_psm_pmix_code,
            'product_name_en': self.x_psm_product_name_en,
            'product_name_vi': self.x_psm_product_name_vi,
            'product_form': self.x_psm_product_form,
            'menu_type': self.x_psm_menu_type,
            'target_effective_date': fields.Date.to_string(self.x_psm_target_effective_date) if self.x_psm_target_effective_date else False,
            'effective_date_calc': fields.Date.to_string(self.x_psm_effective_date_calc) if self.x_psm_effective_date_calc else False,
            'pricing': {
                'currency': self.x_psm_currency_id.name if self.x_psm_currency_id else False,
                'instore': self.x_psm_price_instore,
                'delivery': self.x_psm_price_delivery,
                'tsn': self.x_psm_price_tsn,
                'other': self.x_psm_price_other,
            },
            'platforms': [
                {'code': platform.code, 'name': platform.name}
                for platform in self.x_psm_platform_ids
            ],
            'components': [
                {
                    'type': line.x_psm_component_type,
                    'product_code': line.x_psm_product_id.default_code,
                    'product_name': line.x_psm_product_id.display_name,
                    'recipe': line.x_psm_recipe_text,
                    'qty': line.x_psm_qty,
                    'price_vnm': line.x_psm_price_vnm,
                    'price_delivery': line.x_psm_price_delivery,
                    'price_tsn': line.x_psm_price_tsn,
                    'is_default': line.x_psm_is_default,
                    'default_size': line.x_psm_default_size,
                    'allow_upsize': line.x_psm_allow_upsize,
                    'allow_upgrade': line.x_psm_allow_upgrade,
                    'choice_group': line.x_psm_choice_group,
                }
                for line in self.x_psm_component_line_ids
            ],
        }

    def action_push_to_ssbi(self):
        for rec in self:
            payload = rec._prepare_ssbi_payload()
            payload_json = json.dumps(payload, ensure_ascii=False, indent=2, default=str)
            rec.write({
                'x_psm_ssbi_payload_json': payload_json,
                'x_psm_ssbi_pushed_date': fields.Datetime.now(),
                'x_psm_ssbi_status': 'queued',
            })
            rec.message_post(
                body=_("SSBI payload has been prepared and queued for integration."),
                message_type='notification',
            )
        return True

    def action_pilot_deploy(self):
        res = super().action_pilot_deploy()
        self.action_push_to_ssbi()
        return res
