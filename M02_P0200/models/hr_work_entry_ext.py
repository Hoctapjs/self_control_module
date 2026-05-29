# -*- coding: utf-8 -*-
from odoo import models, api

class HrWorkEntry(models.Model):
    _inherit = 'hr.work.entry'

    @api.model_create_multi
    def create(self, vals_list):
        work_entries = super().create(vals_list)
        
        trial_type = self.env.ref('M02_P0200.work_entry_type_trial', raise_if_not_found=False)
        official_type = self.env.ref('hr_work_entry.work_entry_type_attendance', raise_if_not_found=False)
        if not trial_type:
            trial_type = self.env['hr.work.entry.type'].sudo().search([('code', 'in', ['PB', 'MCD_THUVIEC', 'THUVIEC'])], limit=1)

        target_type_ids = [trial_type.id, official_type.id] if trial_type and official_type else []
        
        for entry in work_entries.filtered(lambda e: e.version_id):
            if entry.work_entry_type_id.id in target_type_ids or not entry.work_entry_type_id:
                kind_type = entry.version_id.contract_kind_id.kind_type
                if kind_type == 'probation' and trial_type:
                    entry.work_entry_type_id = trial_type.id
                elif kind_type and kind_type != 'probation' and official_type:
                    entry.work_entry_type_id = official_type.id
        return work_entries
