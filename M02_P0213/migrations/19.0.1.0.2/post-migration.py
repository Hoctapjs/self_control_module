# -*- coding: utf-8 -*-

from odoo import SUPERUSER_ID, api


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    subtype = env.ref('M02_P0213.mail_mt_0213_notification', raise_if_not_found=False)
    if not subtype:
        return

    subtype.write({
        'name': 'Thông báo hệ thống 0213',
        'description': False,
        'default': False,
        'internal': True,
    })
