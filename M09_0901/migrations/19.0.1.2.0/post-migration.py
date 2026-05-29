# -*- coding: utf-8 -*-


def migrate(cr, version):
    cr.execute("""
        UPDATE mkt_paf_request
           SET discount_total_estimate = total_promotion_value
         WHERE COALESCE(discount_total_estimate, 0) = 0
           AND COALESCE(gift_quantity, 0) = 0
           AND COALESCE(gift_unit_value, 0) = 0
           AND COALESCE(total_promotion_value, 0) > 0
    """)
    cr.execute("SELECT id FROM x_psm_pif_platform WHERE active IS TRUE")
    platform_ids = [row[0] for row in cr.fetchall()]
    if platform_ids:
        cr.execute("SELECT id FROM mkt_paf_request")
        request_ids = [row[0] for row in cr.fetchall()]
        for request_id in request_ids:
            for platform_id in platform_ids:
                cr.execute("""
                    INSERT INTO mkt_paf_request_pif_platform_rel (request_id, platform_id)
                    VALUES (%s, %s)
                    ON CONFLICT DO NOTHING
                """, (request_id, platform_id))
