# -*- coding: utf-8 -*-
{
    'name': "M09_0901 Demo Data (xuyen suot 0801 + 0901)",
    'summary': "Du lieu mau di xuyen suot M08_P0801 (PIF) va M09_0901 (PAF)",
    'description': """
        Module du lieu mau lien thong cho luong 0801 + 0901.

        Tan dung lai data tu M08_P0801_demo (department, user, employee, product, BOM, PIF),
        chi bo sung phan ma 0901 yeu cau:

        - 3 phong ban moi: OPS, Finance, Legal
        - 6 user + 6 employee gan vao 3 phong ban
        - Bat paf_can_use=True cho 3 thanh pham + 3 BOM trong M08_P0801_demo
        - 1 loyalty program mau (LTO Mua He 2026)
        - 2 PAF template (LTO 5 phong ban, Core 3 phong ban)
        - 10 PAF Request mau, moi cai o 1 state khac nhau:
            * PAF-DEMO-DRAFT       : draft (MKT vua tao, chua submit)
            * PAF-DEMO-EVAL        : dept_evaluation (5 line dang pending/in_review)
            * PAF-DEMO-HEAD        : head_approval (cho Heads duyet)
            * PAF-DEMO-CLEVEL      : clevel_approval (cho C-Level duyet)
            * PAF-DEMO-APPROVED    : approved (vua duyet, chua trigger PIF)
            * PAF-DEMO-PIF         : pif_running (PIF dang chay)
            * PAF-DEMO-VAL         : valuation (dang lam Valuation)
            * PAF-DEMO-DONE        : done (hoan tat, da publish report)
            * PAF-DEMO-REJ         : rejected (Head tu choi)
            * PAF-DEMO-CANCEL      : cancelled (MKT huy)

        Sau khi cai dat, post_init_hook se chay 1 case end-to-end:
        PAF-DEMO-E2E di tu draft -> dept_evaluation -> head_approval ->
        clevel_approval -> approved -> pif_running (tu sinh x_psm_pif_object) ->
        valuation -> done. Day la case dung de demo luong tich hop 0801 <-> 0901.

        QUAN TRONG: cai sau khi M08_P0801_demo va M09_0901 da o state installed.
    """,
    'author': "MongTuyen",
    'license': 'OEEL-1',
    'version': '19.0.0.3.0',
    'category': 'Marketing/PAF',
    'depends': ['M08_P0801_demo', 'M09_0901'],
    'data': [
        'data/01_extra_departments.xml',
        'data/02_extra_users_employees.xml',
        'data/03_paf_master_data_patch.xml',
        'data/04_paf_templates.xml',
        'data/05_paf_static_states.xml',
        'data/06_grant_paf_groups.xml',
        'data/07_paf_banners.xml',
    ],
    'installable': True,
    'application': False,
    'post_init_hook': 'post_init_hook',
}
