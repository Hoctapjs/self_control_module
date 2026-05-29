# -*- coding: utf-8 -*-
import json


SAFE_INTERNAL_UX_ARCH = """<data>
            <xpath expr="//div[@class='oe_title']" position="after">
                <div class="d-none"/>
            </xpath>
        </data>"""


def migrate(cr, version):
    cr.execute(
        """
        UPDATE ir_ui_view
           SET arch_db = %s::jsonb,
               arch_updated = false
          FROM ir_model_data
         WHERE ir_model_data.model = 'ir.ui.view'
           AND ir_model_data.res_id = ir_ui_view.id
           AND ir_model_data.module = 'M02_P0215'
           AND ir_model_data.name = 'view_psm_hr_discipline_record_form_internal_ux'
        """,
        [json.dumps({"en_US": SAFE_INTERNAL_UX_ARCH})],
    )
