# -*- coding: utf-8 -*-
"""
post_init_hook cho M09_0901_demo.

Sau khi module duoc cai dat (cac data XML da load xong), hook nay chay
1 case end-to-end de tao record PAF-DEMO-E2E di TUYEN HOAN CHINH:

    draft
      |  action_submit_to_evaluation()
      v
    dept_evaluation
      |  cho moi line: action_start_review() -> dien field -> action_submit_done()
      |  line cuoi: auto trigger _notify_all_evaluations_complete() ->
      |             action_collect_evaluations() -> tao head approval
      v
    head_approval
      |  paf.action_request_clevel()  (bypass workflow duyet that)
      v
    clevel_approval
      |  paf.action_mark_approved()  -> tao PIF approval.request
      v
    approved -> pif_running
      |  tao x_psm_pif_object thu cong (mo phong RSG duyet PIF Marketing)
      |  -> pif_object.create() override trong M09 set paf.pif_object_id
      v
    pif_running (co pif_object_id)
      |  paf.action_open_valuation()  -> tao mkt_paf.valuation.report draft
      v
    valuation
      |  report.action_publish()
      v
    done

Hook chi chay khi PAF-DEMO-E2E chua ton tai (idempotent).
"""
import logging
from odoo import fields

_logger = logging.getLogger(__name__)


# Du lieu mau dien vao tung eval line theo department_code.
# Phai dap ung validation trong action_submit_done() cua
# mkt_paf.evaluation.line.
EVAL_PAYLOAD = {
    'si': {
        'forecast_demand': 1800.0,
        'confidence_score': 0.91,
        'comment_html': (
            '<p>Du bao 1.800 phan/ngay/cua hang (8 store). '
            'Do tin cay 91% — su dung mo hinh ARIMA + segment GenZ.</p>'
        ),
    },
    'ops': {
        'pilot_capacity_score': 'high',
        'bottleneck_note': (
            'Khu vuc chien gioi han o 1.200 phan/h trong gio cao diem. '
            'Da co ke hoach trien khai pre-cook 30 phut truoc 11:00.'
        ),
        'comment_html': (
            '<p>Nang luc van hanh tot. Khuyen nghi pilot 8 cua hang '
            'flag-ship truoc khi mass rollout.</p>'
        ),
    },
    'finance': {
        'roi_estimated_percent': 42.5,
        'gross_margin_estimated': 175000000.0,
        'comment_html': (
            '<p>ROI uoc tinh 42.5%, loi nhuan gop 175M VND. '
            'Da bao gom chi phi marketing + giam gia loyalty.</p>'
        ),
    },
    'sc': {
        'supply_risk_level': 'low',
        'lead_time_days': 10,
        'food_safety_check_status': 'verified',
        'comment_html': (
            '<p>Nguyen lieu trong nuoc, lead time 10 ngay. '
            'Khong co rui ro thieu hang.</p>'
        ),
    },
    'legal': {
        'regulatory_sla_days': 30,
        'requires_government_approval': True,
        'scheme_compliant': True,
        'legal_filing_type': 'notification',
        'legal_50_percent_check': True,
        'comment_html': (
            '<p>Scheme khuyen mai tuan thu Nghi dinh 81/2018. '
            'Can xin phep Cuc Quang cao truoc 30 ngay launch.</p>'
        ),
    },
}


def post_init_hook(env):
    """Tao 1 PAF end-to-end di tu draft -> done sau khi cai M09_0901_demo."""
    _logger.info('[M09_0901_demo] Bat dau chay end-to-end PAF demo case...')

    PafRequest = env['mkt_paf.request'].sudo()
    existing = PafRequest.search([('name', '=', 'PAF-DEMO-E2E')], limit=1)
    if existing:
        _logger.info(
            '[M09_0901_demo] PAF-DEMO-E2E da ton tai (id=%s), bo qua hook.',
            existing.id,
        )
        return

    try:
        _configure_approval_categories(env)
        paf = _build_and_run_e2e(env)
    except Exception as exc:
        _logger.exception(
            '[M09_0901_demo] Loi khi chay end-to-end PAF demo: %s', exc,
        )
        return

    _logger.info(
        '[M09_0901_demo] Hoan tat. PAF-DEMO-E2E id=%s, state=%s, '
        'pif_object_id=%s.',
        paf.id, paf.state, paf.pif_object_id.id or False,
    )


def _configure_approval_categories(env):
    """Cau hinh approver cho 2 category PAF de action_confirm khong fail.

    M09_0901 khai bao mkt_0901_approval_category_paf_head voi
    approval_minimum=5 nhung khong cau hinh approver_ids -> khi
    action_collect_evaluations() goi action_confirm() se UserError
    "You have to add at least 5 approvers...".

    O demo, ta ha minimum xuong 1 va dat 1 approver cho moi category.
    Production thuc te se cau hinh thu cong qua UI.
    """
    mkt_head = env.ref('M08_P0801_demo.demo_user_mkt_head', raise_if_not_found=False)
    if not mkt_head:
        _logger.warning('[M09_0901_demo] Khong tim thay demo_user_mkt_head, '
                        'bo qua _configure_approval_categories.')
        return

    rsg_head = env.ref('M08_P0801_demo.demo_user_rsg_head',
                       raise_if_not_found=False) or mkt_head

    head_cat = env.ref('M09_0901.mkt_0901_approval_category_paf_head',
                       raise_if_not_found=False)
    clevel_cat = env.ref('M09_0901.mkt_0901_approval_category_paf_clevel',
                         raise_if_not_found=False)
    # M08 PIF category: cung can approver de _run_pif_workflow() ->
    # action_confirm() khong fail "at least 1 approver".
    pif_cat = env.ref('M08_P0801.approval_category_data_pif',
                      raise_if_not_found=False)

    configs = [
        (head_cat, mkt_head),
        (clevel_cat, mkt_head),
        (pif_cat, rsg_head),
    ]
    for cat, approver in configs:
        if not cat:
            continue
        cat_su = cat.sudo()
        # Chi gan approver neu chua co
        if not cat_su.approver_ids:
            cat_su.write({
                'approval_minimum': 1,
                'approver_ids': [(0, 0, {
                    'user_id': approver.id,
                    'required': True,
                    'sequence': 10,
                })],
            })
            _logger.info(
                '[M09_0901_demo]   Configured category "%s": '
                'approval_minimum=1, approver=%s',
                cat_su.name, approver.login,
            )


def _build_and_run_e2e(env):
    """Tao PAF va chay tron luong B3 -> B12."""
    template = env.ref('M09_0901_demo.demo_paf_template_lto')
    creator = env.ref('M08_P0801_demo.demo_user_mkt')
    product = env.ref('M08_P0801_demo.demo_tmpl_bbq_chicken_burger')
    bom = env.ref('M08_P0801_demo.demo_bom_bbq_chicken')
    product.write({
        'food_safety_declaration_state': 'done',
        'food_safety_declaration_no': '12345/2026/ATTP-HCM',
        'food_safety_declaration_date': fields.Date.to_date('2026-05-15'),
    })
    channels = [
        env.ref('M08_P0801.pif_platform_fc').id,
        env.ref('M08_P0801.pif_platform_sok').id,
        env.ref('M08_P0801.pif_platform_digital').id,
    ]

    PafRequest = env['mkt_paf.request'].sudo()

    # --- B3: MKT tao PAF tu template ---
    # Dung sudo() de tranh AccessError khi user demo chua duoc gan group
    # PAF Creator (MKT). creator_id van duoc set qua vals -> computed
    # creator_department_id va creator_job_id van chinh xac.
    paf = PafRequest.create({
        'name': 'PAF-DEMO-E2E',
        'template_id': template.id,
        'creator_id': creator.id,
        'description_html': (
            '<h3>BBQ Chicken Burger LTO Mua He 2026 (End-to-End Demo)</h3>'
            '<p>PAF demo di xuyen suot luong tich hop 0901 (Marketing PAF) '
            'va 0801 (PIF). Chay tu post_init_hook cua M09_0901_demo.</p>'
        ),
        'product_ids': [(6, 0, [product.id])],
        'bom_ids': [(6, 0, [bom.id])],
        'planned_start_date': fields.Date.to_date('2026-08-15'),
        'planned_end_date': fields.Date.to_date('2026-10-31'),
        'forecast_revenue': 420000000.0,
        'promotion_type': 'gift_attached',
        'gift_quantity': 5000,
        'gift_unit_value': 15000.0,
        'eligible_channel_ids': [(6, 0, channels)],
        'max_uses_per_customer': 2,
        'time_window_start': 10.0,
        'time_window_end': 22.0,
        'food_safety_responsible_dept_id': env.ref('M08_P0801_demo.dept_sc').id,
    })
    _logger.info('[M09_0901_demo] B3 done: PAF created id=%s, name=%s',
                 paf.id, paf.name)

    # --- B4-B8: Submit + dien eval lines ---
    paf = paf.sudo()
    paf.action_submit_to_evaluation()
    _logger.info('[M09_0901_demo] B4 done: state=%s, %s eval lines',
                 paf.state, len(paf.evaluation_line_ids))

    _fill_evaluation_lines(env, paf)

    # Sau khi line cuoi action_submit_done, _notify_all_evaluations_complete
    # da tu trigger action_collect_evaluations -> state=head_approval
    if paf.state != 'head_approval':
        _logger.warning(
            '[M09_0901_demo] Sau eval, state=%s (mong doi head_approval). '
            'Goi action_collect_evaluations() thu cong.', paf.state,
        )
        paf.action_collect_evaluations()
    _logger.info('[M09_0901_demo] B9 done: state=%s, head_approval_request=%s',
                 paf.state, paf.head_approval_request_id.id or False)

    # --- B9 -> B10: Bypass head approval workflow, sang clevel ---
    # Trong production, Heads se duyet approval.request -> trigger
    # action_request_clevel. O day ta goi truc tiep de demo flow.
    paf.action_request_clevel()
    _logger.info('[M09_0901_demo] B10 done: state=%s, clevel_approval_request=%s',
                 paf.state, paf.clevel_approval_request_id.id or False)

    # --- B10 -> B11: Bypass clevel approval, mark approved, trigger PIF ---
    paf.action_mark_approved()
    _logger.info('[M09_0901_demo] B11 done: state=%s (sau _run_pif_workflow)',
                 paf.state)

    # --- B11 chi tiet: Tao x_psm_pif_object thu cong cho PIF approval.request ---
    # M08 chi fast-track digital/supply_chain, marketing PIF can RSG duyet that.
    # O day ta gia lap: tao x_psm_pif_object truc tiep, override M09
    # se tu set paf.pif_object_id.
    _create_pif_object_for_paf(env, paf)
    _logger.info('[M09_0901_demo] B11 chi tiet: pif_object_id=%s',
                 paf.pif_object_id.id or False)

    # --- B12: Mo Valuation report draft ---
    paf.action_open_valuation()
    _logger.info('[M09_0901_demo] B12 buoc 1 done: state=%s', paf.state)

    report = env['mkt_paf.valuation.report'].sudo().search(
        [('paf_request_id', '=', paf.id)], limit=1,
    )
    report.write({
        'actual_revenue': 480000000.0,
        'actual_cost': 305000000.0,
        'summary_html': (
            '<h3>Bao cao Valuation - PAF-DEMO-E2E</h3>'
            '<ul>'
            '<li>Doanh thu thuc te: 480M VND (vuot du bao 14%)</li>'
            '<li>Chi phi thuc te: 305M VND</li>'
            '<li>ROI thuc te: ~57%</li>'
            '<li>Khuyen nghi: tai phat hanh trong Q2 2027 voi 16 cua hang.</li>'
            '</ul>'
        ),
    })
    report.action_publish()
    _logger.info('[M09_0901_demo] B12 buoc 2 done: report published, '
                 'paf state=%s', paf.state)

    return paf


def _fill_evaluation_lines(env, paf):
    """Dien tat ca eval line cua PAF, kich hoat workflow chuan."""
    # Sap xep theo sequence de line cuoi cung trigger auto-collect.
    lines = paf.evaluation_line_ids.sorted('sequence')

    user_by_code = {
        'si': env.ref('M08_P0801_demo.demo_user_si'),
        'ops': env.ref('M09_0901_demo.demo_user_ops'),
        'finance': env.ref('M09_0901_demo.demo_user_finance'),
        'sc': env.ref('M08_P0801_demo.demo_user_sc'),
        'legal': env.ref('M09_0901_demo.demo_user_legal'),
    }

    for line in lines:
        code = line.department_code
        evaluator = user_by_code.get(code)
        line_su = line.sudo()
        # start_review yeu cau status='pending'
        line_su.action_start_review()
        # gan evaluator + cac field dac thu
        payload = dict(EVAL_PAYLOAD.get(code, {}))
        if evaluator:
            payload['evaluator_id'] = evaluator.id
        line_su.write(payload)
        # submit_done validate fields theo department_code + co the
        # auto trigger action_collect_evaluations o line cuoi
        line_su.action_submit_done()
        _logger.info(
            '[M09_0901_demo]   eval line dept_code=%s status=%s',
            code, line_su.status,
        )


def _create_pif_object_for_paf(env, paf):
    """Tao x_psm_pif_object cho PIF approval.request gan voi PAF.

    Gia lap viec RSG duyet manual cho PIF Marketing.
    Override trong M09_0901/models/pif_object.py se tu cap nhat
    paf.pif_object_id khi PIF object duoc tao.
    """
    ApprovalRequest = env['approval.request'].sudo()
    pif_req = ApprovalRequest.search([
        ('x_psm_mkt_paf_request_id', '=', paf.id),
        ('category_id.x_psm_0801_is_pif', '=', True),
    ], limit=1)

    if not pif_req:
        _logger.warning('[M09_0901_demo] Khong tim thay PIF approval.request '
                        'cho PAF id=%s, bo qua tao PIF object.', paf.id)
        return

    if pif_req.x_psm_0801_pif_object_id:
        _logger.info('[M09_0901_demo] PIF object da ton tai cho '
                     'approval.request id=%s.', pif_req.id)
        return

    pif_vals = {
        'x_psm_approval_request_id': pif_req.id,
        'x_psm_pif_request_type': pif_req.x_psm_0801_pif_request_type or 'marketing',
        'x_psm_request_owner_id': pif_req.request_owner_id.id,
        # De PIF o state lab_test cho hop ly voi luong Marketing
        # (chua hoan tat, dang trong qua trinh thu nghiem).
        'state': 'lab_test',
    }
    if pif_req.x_psm_0801_pif_product_id:
        pif_vals['x_psm_pif_product_id'] = pif_req.x_psm_0801_pif_product_id.id
    if pif_req.x_psm_0801_pif_bom_id:
        pif_vals['x_psm_pif_bom_id'] = pif_req.x_psm_0801_pif_bom_id.id

    pif = env['x_psm_pif_object'].sudo().create(pif_vals)
    pif_req.x_psm_0801_pif_object_id = pif.id
    _logger.info('[M09_0901_demo]   Tao x_psm_pif_object id=%s state=%s',
                 pif.id, pif.state)
