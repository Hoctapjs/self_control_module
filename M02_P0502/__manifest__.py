# Khai bao ma hoa file Python
# -*- coding: utf-8 -*-

# Khai bao thong tin module Odoo nay
{
    # Ten hien thi cua module
    "name": "M02_P0502_QUAN_LY_BAO_TRI",
    # Phien ban module phu hop Odoo 19
    "version": "19.0.5.0.0",
    # Mo ta ngan ve muc dich module
    "summary": "Phase 1 foundation for process 0502 maintenance flow",
    # Cac module phu thuoc can co truoc khi cai dat
    "depends": ["maintenance", "hr", "industry_fsm", "stock", "purchase", "purchase_stock"],
    # Danh sach cac tep du lieu, quyen va giao dien se duoc nap
    "data": [
        # Cau hinh quyen truy cap model
        "security/0502_security.xml",
        "security/ir.model.access.csv",
        # Cau hinh tac vu dinh ky
        "data/ir_cron_data.xml",
        # Cau hinh sequence cho yeu cau dich vu ngoai 0502
        "data/outside_service_sequence_data.xml",
        # Cau hinh sequence cho bo chung tu 0502
        "data/document_sequence_data.xml",
        # Cau hinh stage chuan cho Kanban 0502
        "data/maintenance_stage_data.xml",
        # Du lieu goc cho nguon yeu cau
        "data/request_source_data.xml",
        # Du lieu goc cho loai yeu cau
        "data/request_type_data.xml",
        # Dinh nghia giao dien cho thiet bi bao tri (buoc 5)
        "views/maintenance_equipment_views.xml",
        # Dinh nghia giao dien cau hinh CMT lead tren maintenance team
        "views/maintenance_team_views.xml",
        # Dinh nghia giao dien cau hinh partner dai dien cho phong ban/cua hang
        "views/hr_department_views.xml",
        # Dinh nghia giao dien cho yeu cau bao tri
        "views/maintenance_request_views.xml",
        # Dinh nghia giao dien cho yeu cau dich vu ngoai
        "views/outside_service_request_views.xml",
        # Dinh nghia giao dien theo doi tien do thuc thi FSM task cho buoc 10
        "views/project_task_views.xml",
        # Dinh nghia giao dien lien ket phieu kho voi request 0502
        "views/stock_picking_views.xml",
        # Dinh nghia giao dien lien ket don mua voi request 0502
        "views/purchase_order_views.xml",
        # Wizard in bo chung tu 0502
        "wizards/document_pack_wizard_views.xml",
        # Dinh nghia report chung tu 0502 tren maintenance request
        "reports/maintenance_request_reports.xml",
        # Dinh nghia report in yeu cau bao gia dich vu ngoai
        "reports/outside_service_report.xml",
    ],
    # Du lieu demo cho Phase 3G, chi nap khi cai module voi demo data
    "demo": [
        "demo/psm_0502_demo_data.xml",
    ],
    # Hook chay sau khi cai module de fold cac stage maintenance goc cho Kanban 0502
    "post_init_hook": "post_init_hook",
    # Ket thuc danh sach du lieu module
    "installable": True,
    # Cho phep cai dat module
    "application": False,
    # Day khong phai la ung dung chinh
    "license": "LGPL-3",
    # Giay phep su dung cua module
}
