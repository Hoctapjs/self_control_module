# -*- coding: utf-8 -*-


def migrate(cr, version):
    cr.execute("""
        UPDATE mkt_paf_request
           SET promotion_type = COALESCE(promotion_type, 'gift_attached'),
               promotion_legal_form = COALESCE(promotion_legal_form, 'notification'),
               total_promotion_value = CASE
                   WHEN COALESCE(total_promotion_value, 0) > 0 THEN total_promotion_value
                   WHEN state = 'draft' THEN 0
                   WHEN COALESCE(forecast_revenue, 0) > 0 THEN forecast_revenue
                   ELSE 1
               END
    """)
    cr.execute("""
        UPDATE mkt_paf_request
           SET allow_extended_duration = TRUE
         WHERE planned_start_date IS NOT NULL
           AND planned_end_date IS NOT NULL
           AND (planned_end_date - planned_start_date) > 90
    """)
