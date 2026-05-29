# Before And After Thay Doi Quyen 0214

Tai lieu nay tong hop trang thai `truoc` va `sau` khi trien khai phan quyen cho module `M02_P0214_00`.

Module nay la quy trinh `Offboarding RST`, nen huong phan quyen duoc trien khai theo cac group `RST` cua `M02_P0200_00`.

## 1. Tai lieu da dung de dinh huong

- Convention:
  - Thu muc `addons/M02_P0214_00/convention/` co ton tai, nhung hien tai khong doc duoc file quy uoc cu the tu terminal, nen dot nay uu tien xac nhan bang source code hien tai.
- JSON map da dung:
  - `addons/M02_P0214_00/structure/module_map.json`
- Source chinh dung de xac nhan:
  - `addons/M02_P0214_00/__manifest__.py`
  - `addons/M02_P0214_00/security/ir.model.access.csv`
  - `addons/M02_P0214_00/security/security.xml`
  - `addons/M02_P0214_00/security/offboarding_request_rules.xml`
  - `addons/M02_P0214_00/views/resignation_request_views.xml`
  - `addons/M02_P0214_00/views/offboarding_report_views.xml`
  - `addons/M02_P0214_00/models/approval_request_rst_fields.py`
  - `addons/M02_P0214_00/models/approval_request_rst_approval.py`
  - `addons/M02_P0214_00/models/approval_request_rst_survey.py`
  - `addons/M02_P0214_00/models/approval_request_rst_reminder.py`
  - `addons/M02_P0214_00/models/approval_request_rst_offboarding.py`
  - `addons/M02_P0200_00/security/security.xml`

## 2. Before

Truoc khi thay doi, `0214` dang o trang thai sau:

- Module chua `depends` vao `M02_P0200_00`.
- Chua load file security rieng theo group to chuc cua `0200`.
- ACL van chu yeu dua tren:
  - `base.group_user`
  - `base.group_portal`
- Chua co record rule rieng cho:
  - `approval.request`
  - `approval.approver`
  theo pham vi case `0214`
- Chua co lop map group `RST` de chan action nhay cam o backend.
- Chua co `groups="M02_P0200_00...."` tren cac button, tab, menu, report quan trong.

Hieu ngan gon:

- user noi bo co quyen theo kieu kha rong
- chua tach ro ai duoc doc, ai duoc xu ly, ai duoc hoan tat quy trinh
- UI va backend chua khoa theo dung vai tro `RST`

## 3. After

Sau khi thay doi, quyen cua `0214` da duoc trien khai theo 4 lop chinh:

### 3.1. Dependency

Da them `M02_P0200_00` vao `depends` trong:

- `addons/M02_P0214_00/__manifest__.py`

Y nghia:

- `0214` da co the dung truc tiep cac group chuan cua `0200`
- phan quyen da bam vao dung he group `RST` thay vi chi dua vao `base.group_user`

### 3.2. Record rule

Da them va load cac file:

- `addons/M02_P0214_00/security/security.xml`
- `addons/M02_P0214_00/security/offboarding_request_rules.xml`

Da bo sung:

- rule portal cho `survey.user_input`
  - portal chi duoc xem du lieu survey cua chinh minh
- rule cho `approval.request`
  - nhom `RST` lien quan duoc doc case offboarding `0214`
  - nhom manager/head/system duoc quyen quan ly sau hon
- rule cho `approval.approver`
  - nhom `RST` lien quan duoc doc approver line cua case `0214`

Y nghia:

- quyen du lieu khong con mo chung theo toan bo noi bo
- pham vi du lieu da bam vao category cua quy trinh `0214`

### 3.3. Button visibility

Da gan `groups` vao cac thanh phan giao dien trong:

- `addons/M02_P0214_00/views/resignation_request_views.xml`
- `addons/M02_P0214_00/views/offboarding_report_views.xml`

Da siep cac diem chinh:

- button `action_send_social_insurance`
- button `action_done`
- button `action_view_my_activities`
- button `action_view_survey_results`
- tab `Thong tin nghi viec`
- tab `Qua trinh nghi viec`
- menu cau hinh `Loai nghi viec`
- report/menu `Offboarding Report`

Y nghia:

- user khong dung group se khong thay nut hoac menu nhay cam
- UI da phan biet ro hon giua nhom doc, nhom xu ly va nhom quan tri

### 3.4. Backend action guard

Da them helper kiem tra group trong:

- `addons/M02_P0214_00/models/approval_request_rst_fields.py`

Helper chinh:

- `_check_0214_group_access(...)`

Da ap vao cac action:

- `action_done`
- `action_send_social_insurance`
- `action_view_survey_results`
- `action_manual_reminder_extension`
- `action_view_my_activities`
- `action_pending_offboarding_subordinates`

Y nghia:

- khong chi an nut o UI
- neu goi action truc tiep tu RPC hoac cach khac, backend van chan neu user khong dung group

## 4. Mapping quyen da ap dung

Dot nay dang ap dung theo huong:

- nhom doc/phoi hop:
  - `GDH_RST_HR_ADMIN_S`
  - `GDH_RST_HR_ADMIN_M`
  - `GDH_RST_HR_HRBP_S`
  - `GDH_RST_HR_HRBP_M`
  - `GDH_RST_HR_HEAD_M`
  - `GDH_RST_SYSTEM_ST_M`
- nhom xu ly `BHXH`:
  - `GDH_RST_HR_ADMIN_S`
  - `GDH_RST_HR_ADMIN_M`
  - `GDH_RST_HR_HEAD_M`
  - `GDH_RST_SYSTEM_ST_M`
- nhom duoc `Done`:
  - `GDH_RST_HR_ADMIN_M`
  - `GDH_RST_HR_HRBP_M`
  - `GDH_RST_HR_HEAD_M`
  - `GDH_RST_SYSTEM_ST_M`
- nhom duoc vao `Offboarding Report` va xem subordinate report:
  - `GDH_RST_HR_HRBP_S`
  - `GDH_RST_HR_HRBP_M`
  - `GDH_RST_HR_HEAD_M`
  - `GDH_RST_SYSTEM_ST_M`

## 5. Pham vi thay doi trong dot nay

Dot nay moi tap trung vao:

- dependency
- record rule cho `approval.request` va `approval.approver`
- portal rule cho `survey.user_input`
- button visibility
- menu/report visibility
- backend action guard

## 6. Nhung gi chua lam trong dot nay

Chua mo rong tiep cac phan sau:

- chua doi ACL goc trong `security/ir.model.access.csv`
- chua them rule rieng cho `mail.activity`
- chua ra soat toan bo controller portal theo group `0200`
- chua chay upgrade module trong Odoo
- chua chay test runtime bang user that theo tung group

Ly do:

- dot nay uu tien khoa cac diem nhay cam truoc
- tranh siet qua sau vao ACL model chung khi chua test du pham vi anh huong

## 7. Tac dong chinh sau thay doi

Sau dot nay, `0214` da ro hon o mat phan quyen:

- quyen da bam vao he group `RST` cua `0200`
- du lieu da duoc loc theo category cua quy trinh `0214`
- nut va menu nhay cam da khong hien dai tra cho user noi bo chung
- backend da co chan thuc su, khong chi chan o UI

Noi de hieu:

- `record rule` tra loi cau hoi: user co duoc thay record nay khong
- `button visibility` tra loi cau hoi: user co thay nut nay khong
- `backend guard` tra loi cau hoi: du co goi thang action thi he thong co cho chay khong

## 8. Kiem tra da thuc hien

Da kiem tra ky thuat sau khi sua:

- `python -m py_compile` cho cac file Python lien quan da pass
- XML parse cho:
  - `security/security.xml`
  - `security/offboarding_request_rules.xml`
  - `views/resignation_request_views.xml`
  - `views/offboarding_report_views.xml`
  da pass

## 9. De xuat test tiep theo

Nen test lai bang cac user dai dien:

- `GDH_RST_HR_ADMIN_S`
- `GDH_RST_HR_ADMIN_M`
- `GDH_RST_HR_HRBP_S`
- `GDH_RST_HR_HRBP_M`
- `GDH_RST_HR_HEAD_M`
- `GDH_RST_SYSTEM_ST_M`
- `base.group_portal`

Can check toi thieu 5 goc:

1. Functional
   - Action co chay dung nghiep vu khong
2. Data
   - User co thay dung record va dung noi dung khong
3. Workflow
   - Trang thai, activity, survey, report co dung khong
4. Security
   - Dung group moi thay, moi xu ly, moi hoan tat duoc khong
5. Reporting / auditability
   - Report va lich su co doc duoc dung pham vi khong

## 10. Ket luan

`0214` da duoc nang cap tu mo hinh quyen kha rong sang mo hinh ro hon theo `RST group cua 0200`.

Dot nay da dat nen tang de:

- tach quyen doc va quyen xu ly
- khoa cac action nhay cam
- dua `0214` ve cung kieu kien truc quyen voi huong da ap dung cho `0213`, nhung dung trong ngu canh `RST`

