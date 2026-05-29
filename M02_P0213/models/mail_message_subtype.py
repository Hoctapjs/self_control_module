# -*- coding: utf-8 -*-

from odoo import models

class MailMessageSubtype(models.Model):
    _inherit = "mail.message.subtype"
    # No extra fields needed; this model exists to allow creation of a new subtype via XML.
