# -*- coding: utf-8 -*-
"""SLA constraint for PAF Request model.
Ensures planned start date respects regulatory SLA days.
"""
import logging
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)

class PafRequestSLAConstraint(models.Model):
    _inherit = 'mkt_paf.request'

    @api.constrains('planned_start_date', 'regulatory_sla_days')
    def _check_sla_start_date(self):
        for rec in self:
            if rec.planned_start_date and rec.regulatory_sla_days:
                delta = fields.Date.context_today(rec) - rec.planned_start_date
                # delta days negative if planned_start_date in future, ensure enough days before start
                if (rec.planned_start_date - fields.Date.context_today(rec)).days < rec.regulatory_sla_days:
                    raise ValidationError(_(
                        "Planned start date must be at least %s days after today to satisfy Legal SLA.") % rec.regulatory_sla_days)
