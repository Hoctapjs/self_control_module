# -*- coding: utf-8 -*-
"""
Store PSM-specific configuration parameters (key-value pairs).
Independent from Odoo's ir.config_parameter.
"""

import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class PsmParameter(models.Model):
    """Per-database storage of PSM configuration key-value pairs."""
    _name = 'x_psm_parameter'
    _description = 'PSM Parameter'
    _rec_name = 'x_psm_key'
    _order = 'x_psm_key'

    x_psm_key = fields.Char(string='Key', required=True, index=True)
    x_psm_value = fields.Text(string='Value', required=True)
    x_psm_description = fields.Text(string='Description', help='Optional description for this parameter')

    _key_uniq = models.Constraint(
        'unique (x_psm_key)',
        "Key must be unique.",
    )

    @api.model
    def get_param(self, key, default=False):
        """Retrieve the value for a given key.

        :param string key: The key of the parameter value to retrieve.
        :param string default: default value if parameter is missing.
        :return: The value of the parameter, or ``default`` if it does not exist.
        :rtype: string
        """
        param = self.sudo().search([('x_psm_key', '=', key)], limit=1)
        if param:
            return param.x_psm_value
        return default

    @api.model
    def set_param(self, key, value):
        """Sets the value of a parameter.

        :param string key: The key of the parameter value to set.
        :param string value: The value to set.
        :return: the previous value of the parameter or False if it did
                 not exist.
        :rtype: string
        """
        param = self.sudo().search([('x_psm_key', '=', key)], limit=1)
        if param:
            old = param.x_psm_value
            if value is not False and value is not None:
                if str(value) != old:
                    param.write({'x_psm_value': value})
            else:
                param.unlink()
            return old
        else:
            if value is not False and value is not None:
                self.sudo().create({'x_psm_key': key, 'x_psm_value': value})
            return False

    def name_get(self):
        return [(record.id, record.x_psm_key) for record in self]
