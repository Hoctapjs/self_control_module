# -*- coding: utf-8 -*-


def _get_id(cr, module, name):
    cr.execute("""
        SELECT res_id
          FROM ir_model_data
         WHERE module = %s
           AND name = %s
         LIMIT 1
    """, (module, name))
    row = cr.fetchone()
    return row[0] if row else None


def _set_platforms(cr, request_id, xmlids):
    for module, name in xmlids:
        platform_id = _get_id(cr, module, name)
        if not platform_id:
            continue
        cr.execute("""
            INSERT INTO mkt_paf_request_pif_platform_rel (request_id, platform_id)
            VALUES (%s, %s)
            ON CONFLICT DO NOTHING
        """, (request_id, platform_id))


def migrate(cr, version):
    cr.execute("""
        UPDATE product_template
           SET food_safety_declaration_state = 'done',
               food_safety_declaration_no = '12345/2026/ATTP-HCM',
               food_safety_declaration_date = '2026-05-15'
         WHERE id IN (
               SELECT res_id
                 FROM ir_model_data
                WHERE module = 'M08_P0801_demo'
                  AND name = 'demo_tmpl_bbq_chicken_burger'
         )
    """)
    requests = {
        'PAF-DEMO-E2E': {
            'promotion_type': 'gift_attached',
            'gift_quantity': 5000,
            'gift_unit_value': 15000,
            'discount_percent': 0,
            'discount_total_estimate': 0,
            'max_uses_per_customer': 2,
            'time_window_start': 10.0,
            'time_window_end': 22.0,
            'platforms': [
                ('M08_P0801', 'pif_platform_fc'),
                ('M08_P0801', 'pif_platform_sok'),
                ('M08_P0801', 'pif_platform_digital'),
            ],
        },
        'PAF-DEMO-HEAD': {
            'promotion_type': 'discount_direct',
            'discount_percent': 20,
            'discount_total_estimate': 90000000,
            'platforms': [
                ('M08_P0801', 'pif_platform_fc'),
                ('M08_P0801', 'pif_platform_sok'),
                ('M08_P0801', 'pif_platform_dt'),
                ('M08_P0801', 'pif_platform_digital'),
            ],
        },
        'PAF-DEMO-APPROVED': {
            'promotion_type': 'discount_direct',
            'discount_percent': 20,
            'discount_total_estimate': 64000000,
            'platforms': [
                ('M08_P0801', 'pif_platform_fc'),
                ('M08_P0801', 'pif_platform_sok'),
                ('M08_P0801', 'pif_platform_dt'),
                ('M08_P0801', 'pif_platform_digital'),
            ],
        },
    }
    for name, vals in requests.items():
        cr.execute("SELECT id FROM mkt_paf_request WHERE name = %s LIMIT 1", (name,))
        row = cr.fetchone()
        if not row:
            continue
        request_id = row[0]
        cr.execute("""
            UPDATE mkt_paf_request
               SET promotion_type = %s,
                   promotion_legal_form = CASE WHEN %s = 'lucky_draw' THEN 'registration' ELSE 'notification' END,
                   gift_quantity = %s,
                   gift_unit_value = %s,
                   discount_percent = %s,
                   discount_total_estimate = %s,
                   max_uses_per_customer = %s,
                   time_window_start = %s,
                   time_window_end = %s
             WHERE id = %s
        """, (
            vals.get('promotion_type', 'gift_attached'),
            vals.get('promotion_type', 'gift_attached'),
            vals.get('gift_quantity', 0),
            vals.get('gift_unit_value', 0),
            vals.get('discount_percent', 0),
            vals.get('discount_total_estimate', 0),
            vals.get('max_uses_per_customer', 0),
            vals.get('time_window_start', 0),
            vals.get('time_window_end', 24),
            request_id,
        ))
        _set_platforms(cr, request_id, vals.get('platforms', []))
