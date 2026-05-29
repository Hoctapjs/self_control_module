from odoo import SUPERUSER_ID, api


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    requests = env["maintenance.request"].search([
        "|",
        ("x_psm_0502_request_source_id", "!=", False),
        ("x_psm_0502_request_type_id", "!=", False),
    ])
    requests._psm_sync_0502_stage_from_progress()
