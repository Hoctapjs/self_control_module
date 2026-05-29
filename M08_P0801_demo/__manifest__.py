{
    'name': "M08_P0801 Demo Data",
    'summary': "Dữ liệu mẫu cho module RSG PIF Management (0801)",
    'description': """
        Module dữ liệu mẫu cho M08_P0801.

        Bao gồm:
        - 6 phòng ban chính (RSG, IT, MKT, S&I, MENU, SC)
        - 6 người dùng demo (mỗi phòng ban 1 người + 2 trưởng phòng)
        - 6 nhân viên liên kết với phòng ban
        - 1 nhà cung cấp mẫu (HAVI Vietnam)
        - 9 nguyên liệu thô + 3 thành phẩm
        - 3 BOM (công thức nguyên liệu) đã hoàn thiện
        - 3 PIF mẫu ở các trạng thái khác nhau:
            * PIF-DEMO-001: rsg_create (RSG đang chờ điền thông tin)
            * PIF-DEMO-002: lab_test  (đang thử nghiệm, có 1 lần fail)
            * PIF-DEMO-003: completed (hoàn tất, đã sinh WRIN)
    """,
    'author': "MongTuyen",
    'version': '0.1',
    'category': 'Supply Chain/RSG',
    'depends': ['M08_P0801'],
    'data': [
        'data/01_departments.xml',
        'data/02_job_positions.xml',
        'data/03_users.xml',
        'data/04_employees.xml',
        'data/05_partners.xml',
        'data/06_products.xml',
        'data/07_bom.xml',
        'data/08_pif_objects.xml',
    ],
    'installable': True,
    'application': False,
}
