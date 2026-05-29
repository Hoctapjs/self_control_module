# -*- coding: utf-8 -*-
from odoo import models, api, _

class CalendarEvent(models.Model):
    _inherit = 'calendar.event'

    @api.model_create_multi
    def create(self, vals_list):
        events = super().create(vals_list)
        # Strict scope: only check events linked to M02_P0215 discipline records
        for event in events:
            if event.res_model == 'x_psm.hr.discipline.record' and event.res_id:
                discipline_record = self.env['x_psm.hr.discipline.record'].browse(event.res_id)
                if discipline_record.exists() and discipline_record.state == 'investigation':
                    discipline_record._x_psm_write_state('hearing')
        return events

    def write(self, vals):
        result = super().write(vals)
        # Strict scope: only check if the link to the discipline record is being established or updated
        if 'res_model' in vals or 'res_id' in vals:
            for event in self:
                if event.res_model == 'x_psm.hr.discipline.record' and event.res_id:
                    discipline_record = self.env['x_psm.hr.discipline.record'].browse(event.res_id)
                    if discipline_record.exists() and discipline_record.state == 'investigation':
                        discipline_record._x_psm_write_state('hearing')
        return result
