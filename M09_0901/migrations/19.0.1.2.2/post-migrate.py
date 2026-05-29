# -*- coding: utf-8 -*-


def migrate(cr, version):
    cr.execute("""
        UPDATE mkt_paf_request
           SET discount_total_estimate = CASE
                   WHEN COALESCE(total_promotion_value, 0) > 0 THEN total_promotion_value
                   WHEN COALESCE(forecast_revenue, 0) > 0 THEN forecast_revenue * 0.2
                   ELSE 1
               END
         WHERE state != 'draft'
           AND COALESCE(total_promotion_value, 0) <= 0
           AND COALESCE(gift_quantity, 0) = 0
           AND COALESCE(gift_unit_value, 0) = 0
           AND COALESCE(discount_total_estimate, 0) = 0
    """)
