# Báo Cáo Rà Soát Bảo Mật Module M02_P0214
## Quy Trình Cấp Xin Thôi Việc (RST - Resignation & Turnover Support)

**Phiên bản:** 1.0  
**Ngày rà soát:** 2026-05-15  
**Người rà soát:** Kiến Trúc Sư Bảo Mật Odoo (Senior)  
**Mục đích:** Kiểm toán cơ chế kiểm soát truy cập (Access Control) của module M02_P0214 theo cấu trúc nhóm tổ chức định nghĩa trong module M02_P0200

---

Vì sao phân quyền một module trong Odoo lại ảnh hưởng đến module khác?

Trong Odoo, việc phân quyền “một module” nhưng lại ảnh hưởng sang module khác thường xuất phát từ các điểm sau:

## 1. Dùng chung model

Nếu module A phân quyền trên một model gốc hoặc model dùng chung, ví dụ:

- `res.partner`
- `product.template`
- `stock.picking`
- `account.move`
- `hr.employee`

thì các module khác cũng dùng model đó sẽ bị ảnh hưởng. Đây là nguyên nhân phổ biến nhất.

**Lưu ý để tránh vướng phải:**

- Trước khi thêm ACL hoặc record rule, cần kiểm tra model đó có phải model dùng chung của Odoo hay không.
- Nếu nghiệp vụ chỉ thuộc module riêng, ưu tiên tạo group riêng và rule riêng cho đúng nhóm người dùng của module đó.
- Không nên giới hạn dữ liệu trực tiếp trên model gốc nếu chưa đánh giá các app khác đang dùng model đó.
- Khi cần mở rộng model gốc, nên cân nhắc điều kiện domain thật cụ thể theo field nghiệp vụ của module, thay vì áp rule bao trùm toàn bộ model.

## 2. Record rule quá rộng

`ir.rule` có thể giới hạn dữ liệu theo domain. Nếu rule được áp lên model dùng chung và không giới hạn đúng group hoặc module nghiệp vụ, nó sẽ tác động toàn hệ thống.

Ví dụ: rule trên `res.partner` chỉ cho xem khách hàng của user hiện tại, thì CRM, Sales, Accounting, Inventory đều có thể bị ảnh hưởng.

**Lưu ý để tránh vướng phải:**

- Luôn gắn record rule với group cụ thể, tránh tạo global rule nếu không thật sự cần.
- Domain của rule cần phản ánh đúng phạm vi nghiệp vụ, ví dụ theo `company_id`, `user_id`, `department_id`, trạng thái, hoặc field đánh dấu riêng của module.
- Kiểm tra rule bằng nhiều loại user khác nhau: user thường, manager, admin, user multi-company.
- Với model dùng chung, nên test các màn hình ở module khác có dùng cùng model trước khi kết luận rule đã an toàn.

## 3. ACL trên `ir.model.access.csv` thay đổi quyền model gốc

Nếu module thêm hoặc sửa quyền `read/write/create/unlink` cho một group trên model có sẵn, quyền đó không chỉ áp dụng trong màn hình của module đó, mà áp dụng ở mọi nơi model được dùng.

**Lưu ý để tránh vướng phải:**

- Không cấp quyền `write`, `create`, `unlink` trên model gốc nếu user chỉ cần xem hoặc thao tác qua workflow riêng.
- Tách group theo vai trò nghiệp vụ rõ ràng, ví dụ user, manager, admin của module.
- Kiểm tra xem group được dùng trong ACL có đang được module khác dùng lại hay không.
- Nếu chỉ muốn giới hạn thao tác trên một số bản ghi, dùng record rule hoặc logic nghiệp vụ phù hợp thay vì cấp ACL quá rộng.

## 4. Group kế thừa group khác

Trong Odoo, group có thể dùng `implied_ids`. Nếu group của module A implied một group mạnh hơn hoặc yếu hơn, user có group đó sẽ nhận thêm hoặc mất quyền ở module khác.

Ví dụ: group tùy chỉnh implied `base.group_user`, `sales_team.group_sale_manager`, hoặc group kế toán, thì phạm vi ảnh hưởng sẽ lan rộng.

**Lưu ý để tránh vướng phải:**

- Trước khi thêm `implied_ids`, cần kiểm tra group được kế thừa đang mang theo những quyền gì.
- Không implied group manager của module khác nếu chỉ cần quyền truy cập cơ bản.
- Nên đặt group của module theo tầng quyền rõ ràng: user, manager, admin.
- Sau khi thêm group mới, kiểm tra lại tab quyền truy cập trên user để xem có phát sinh quyền ngoài mong muốn không.

## 5. Menu, action, view chỉ là giao diện, không phải biên giới bảo mật

Ẩn menu của module A không có nghĩa là user không còn quyền với model. Ngược lại, nếu user có quyền model, họ có thể truy cập dữ liệu đó từ module khác, qua smart button, many2one, search, export, API, automation, v.v.

**Lưu ý để tránh vướng phải:**

- Không dùng việc ẩn menu hoặc ẩn button làm cơ chế bảo mật chính.
- Quyền thật sự phải được kiểm soát bằng ACL, record rule, group và kiểm tra quyền trong method khi cần.
- Nếu một action hoặc button gọi logic nhạy cảm, cần kiểm tra quyền ở phía Python, không chỉ kiểm tra ở XML view.
- Sau khi phân quyền, nên thử truy cập dữ liệu qua nhiều đường khác nhau như menu khác, many2one, smart button, export hoặc API.

## 6. Field access hoặc view inheritance trên model dùng chung

Nếu module sửa view, form, tree, search của model gốc bằng XML inheritance, thay đổi đó có thể xuất hiện ở màn hình của module khác nếu cùng dùng view hoặc action liên quan.

**Lưu ý để tránh vướng phải:**

- Khi inherit view của model gốc, cần xác định view đó có đang là view chung của nhiều module hay không.
- Nếu thay đổi chỉ phục vụ module riêng, ưu tiên tạo action/view riêng hoặc dùng group trên field/view element.
- Không sửa trực tiếp layout chung theo hướng làm thay đổi luồng nghiệp vụ của module khác.
- Với field nhạy cảm, nên kiểm soát bằng `groups` ở field hoặc view, đồng thời kiểm tra quyền ở logic backend nếu dữ liệu quan trọng.

## 7. Company rule hoặc multi-company

Các rule theo `company_id`, `company_ids`, hoặc `allowed_company_ids` nếu viết chưa chặt có thể làm user mất quyền xem dữ liệu ở các app khác như Sales, Inventory, Accounting.

**Lưu ý để tránh vướng phải:**

- Khi viết domain theo công ty, cần xử lý cả trường hợp bản ghi không có `company_id` nếu nghiệp vụ cho phép dùng chung.
- Test với user có một công ty và user có nhiều công ty.
- Không tự viết rule multi-company mới nếu Odoo hoặc module gốc đã có rule phù hợp.
- Cẩn thận với domain quá chặt như chỉ cho `company_id = user.company_id`, vì user multi-company thường cần dùng `company_ids` hoặc `allowed_company_ids`.

## 8. Override method trên model dùng chung

Nếu module override `create`, `write`, `unlink`, `search`, `_search`, `read_group`, `fields_view_get`, `name_search`, hoặc constraint của model dùng chung, logic đó chạy cho mọi module gọi model đó.

**Lưu ý để tránh vướng phải:**

- Khi override model dùng chung, cần giới hạn logic bằng điều kiện nghiệp vụ rõ ràng.
- Không raise `AccessError`, `UserError`, hoặc chặn thao tác nếu không chắc request đó đến từ nghiệp vụ của module mình.
- Tránh override các method rộng như `search`, `_search`, `read_group` nếu có thể giải quyết bằng record rule, domain action, hoặc context.
- Nếu bắt buộc dùng context để phân biệt luồng xử lý, cần đặt tên context rõ ràng và chỉ kích hoạt logic khi context đó tồn tại.

## Tóm lại

Trong Odoo, phân quyền không nằm trong phạm vi “module UI”, mà nằm chủ yếu ở:

- model
- group
- ACL
- record rule
- method override

Nếu các thành phần này đặt trên model dùng chung hoặc group dùng chung, ảnh hưởng sang module khác là điều rất dễ xảy ra.

## Cách truy nguyên cụ thể

Khi cần truy nguyên nguyên nhân, nên kiểm tra theo thứ tự:

1. `security/ir.model.access.csv`
2. `security/*.xml` record rules và groups
3. `__manifest__.py` dependencies
4. model được phân quyền
5. các module khác đang dùng cùng model đó

---

## 1. Phạm Vi Rà Soát

### Các Thành Phần Được Kiểm Toán
1. **Danh sách kiểm soát mô hình (ir.model.access.csv)** — 22 quy tắc kiểm soát cấp mô hình
2. **Quy tắc ghi nhận (ir.rule, Record Rules)** — 4 quy tắc lọc dựa trên miền (domain-based)
3. **Nhóm người dùng (res.groups)** — 6 nhóm RST kế thừa từ module M02_P0200
4. **Cấu trúc nhóm ý nghĩa (implied_ids)** — Phân cấp nhóm và quản lý quyền hạn
5. **Bảo mật XML (security.xml)** — Định nghĩa nhóm và quy tắc ghi nhận
6. **Tính năng menu/hành động/chế độ xem (Menu/Action/View Visibility)** — Kiểm soát mức giao diện người dùng
7. **Logic bảo mật Python (Python Security Logic)** — Kiểm tra quyền hạn, hành động ủy quyền (sudo), điều khiển luồng công việc
8. **Controllers Portal** — Xác thực, ủy quyền, và kiểm tra quyền hạn trên các tuyến đường công khai

### Các Mô-đun Phụ Thuộc Được Xem Xét
- **M02_P0200:** Cấu trúc nhóm tổ chức và nhóm cơ sở (GDH_RST_*, GDH_OPS_*)
- **M02_P0213:** Lịch sử và bản ghi nhân sự
- **approval:** Nền tảng quy trình phê duyệt (approval.request, approval.approver, approval.category)
- **survey:** Công cụ khảo sát (survey.user_input, survey.question)
- **hr:** Quản lý nhân sự cơ bản (hr.employee, hr.contract, hr.job)
- **mail:** Hoạt động và truy vết (mail.activity)
- **portal:** Các tuyến đường và controller công khai
- **base:** Nhóm Odoo chuẩn (base.group_user, base.group_portal, base.group_system)

### Các Mô Hình Được Kiểm Toán
- approval.request (yêu cầu xin thôi việc)
- approval.approver (phê duyệt viên)
- approval.category (danh mục phê duyệt)
- survey.user_input (phản hồi khảo sát)
- survey.question (câu hỏi khảo sát)
- hr.employee (nhân sự)
- hr.contract (hợp đồng)
- mail.activity (hoạt động)
- x_psm_resignation_type (loại thôi việc)
- x_psm_resignation_request (yêu cầu cũ, nếu còn)
- Các mô hình liên quan khác

### Các Tập Tin Chính Được Kiểm Tra
- `addons/M02_P0214/security/ir.model.access.csv`
- `addons/M02_P0214/security/security.xml`
- `addons/M02_P0214/security/offboarding_request_rules.xml`
- `addons/M02_P0214/views/resignation_request_views.xml`
- `addons/M02_P0214/views/offboarding_report_views.xml`
- `addons/M02_P0214/views/config_menu_views.xml`
- `addons/M02_P0214/views/hr_employee_views.xml`
- `addons/M02_P0214/models/approval_request_rst_fields.py`
- `addons/M02_P0214/models/approval_request_rst_approval.py`
- `addons/M02_P0214/models/approval_request_rst_survey.py`
- `addons/M02_P0214/models/approval_request_rst_offboarding.py`
- `addons/M02_P0214/models/approval_request_rst_reminder.py`
- `addons/M02_P0214/models/mail_activity.py`
- `addons/M02_P0214/controllers/main.py`
- `addons/M02_P0200/security/security.xml`

---

## 2. Hiện Trạng Quyền Hạn Hiện Tại

### 2.1. Các Nhóm Người Dùng RST (Từ M02_P0200)

#### Nhóm Cấp Nhân Viên (S - Staff Level)
| ID Nhóm | Tên Tiếng Anh | Tên Tiếng Việt | Implied Ids | Ghi Chú |
|---------|--------------|---------------|------------|--------|
| GDH_RST_HR_ADMIN_S | HR Admin Staff | Nhân viên admin | **KHÔNG có** | ⚠️ Không kế thừa `base.group_user` |
| GDH_RST_HR_CNB_S | HR Payroll Staff | Nhân viên tính lương | GDH_RST_ALL_BASE_S | ✓ Có quyền cơ sở |
| GDH_RST_HR_HRBP_S | HR Business Partner Staff | Nhân viên BP | GDH_RST_ALL_BASE_S | ✓ Có quyền cơ sở |
| GDH_RST_LND_LD_S | L&D Staff | Nhân viên L&D | GDH_RST_ALL_BASE_S | ✓ Có quyền cơ sở |
| GDH_RST_IT_STL_S | IT Support Team Leader | Support team Leader | GDH_RST_ALL_BASE_S | ✓ Có quyền cơ sở |
| GDH_RST_OPS_OC_S | Operations Consultant Staff | Operation consultant | GDH_RST_ALL_BASE_S | ✓ Có quyền cơ sở |

#### Nhóm Cấp Quản Lý (M - Manager Level)
| ID Nhóm | Tên Tiếng Anh | Tên Tiếng Việt | Implied Ids | Ghi Chú |
|---------|--------------|---------------|------------|--------|
| GDH_RST_HR_ADMIN_M | HR Admin Manager | Quản lý admin | GDH_RST_HR_ADMIN_S, GDH_RST_ALL_BASE_S | ✓ Có quyền cơ sở |
| GDH_RST_HR_CNB_M | HR Payroll Manager | Quản lý tính lương | GDH_RST_HR_CNB_S | Kế thừa cấp dưới |
| GDH_RST_HR_HRBP_M | HR Business Partner Manager | Quản lý BP | GDH_RST_HR_HRBP_S, GDH_RST_HR_ADMIN_S | ✓ |
| GDH_RST_HR_HEAD_M | HR Department Head | Trưởng phòng nhân sự | Tất cả nhóm quản lý và OPS | ✓ Quyền cao nhất |
| GDH_RST_LND_MANAGER_M | L&D Manager | Quản lý L&D | GDH_RST_LND_LD_S | Kế thừa cấp dưới |
| GDH_RST_IT_HEAD_M | IT Manager | Quản lý IT | Tất cả nhóm IT | ✓ |
| GDH_RST_OPS_OM_M | Operations Manager | Operation consultant manager | GDH_RST_OPS_OC_S | Kế thừa cấp dưới |
| GDH_OPS_STORE_RGM_M | Store General Manager | Cửa hàng trưởng | Tất cả nhóm cửa hàng | ✓ |
| GDH_RST_SYSTEM_ST_M | System Manager | Quản lý hệ thống | Tất cả nhóm quản lý | ✓ Quyền cao nhất hệ thống |

### 2.2. Danh Sách Kiểm Soát Mô Hình (ir.model.access.csv)

**Tệp:** `addons/M02_P0214/security/ir.model.access.csv`

#### Tóm Tắt Nhanh
- **Tổng số quy tắc:** 22 mục nhập
- **Cấu trúc:** `id, name, model_id:id, group_id:id, perm_read, perm_write, perm_create, perm_unlink`
- **Phạm vi quyền hạn:** Hầu hết được gán cho `base.group_user` hoặc các nhóm RST cụ thể

#### Các Mục Nhập ACL Chi Tiết

| Dòng | ID | Mô Hình | Nhóm | R | W | C | U | Ghi Chú |
|-----|-----|---------|------|---|---|---|---|---------|
| 2 | access_department_block_user | department.block | base.group_user | 1 | 1 | 1 | 1 | Phân bộ phận |
| 3 | access_restaurant_area_user | restaurant.area | base.group_user | 1 | 1 | 1 | 1 | Khu vực nhà hàng |
| 4 | **access_mail_activity_internal_user** | **mail.activity** | **base.group_user** | **1** | **1** | **1** | **1** | ⚠️ CRITICAL: Trùng lặp với mail |
| 5 | **access_approval_request_internal_user** | **approval.request** | **base.group_user** | **1** | **1** | **1** | **1** | ⚠️ CRITICAL: Trùng lặp với approvals |
| 6 | access_restaurant_positioning_area_user | restaurant.positioning.area | base.group_user | 1 | 1 | 1 | 1 | Vị trí khu vực |
| 7 | access_restaurant_station_user | restaurant.station | base.group_user | 1 | 1 | 1 | 1 | Trạm nhà hàng |
| 8 | access_restaurant_shift_user | restaurant.shift | base.group_user | 1 | 1 | 1 | 1 | Ca làm việc |
| 9 | access_shift_log_user | shift.log | base.group_user | 1 | 1 | 1 | 1 | Bản ghi ca |
| 10 | access_shift_log_employee_user | shift.log.employee | base.group_user | 1 | 1 | 1 | 1 | Nhân sự ca |
| 11 | access_shift_log_checklist_user | shift.log.checklist | base.group_user | 1 | 1 | 1 | 1 | Danh sách kiểm tra ca |
| 12 | access_shift_log_checklist_line_user | shift.log.checklist.line | base.group_user | 1 | 1 | 1 | 1 | Dòng danh sách |
| 13 | access_hr_job_position_default_user | hr.job.position.default | base.group_user | 1 | 1 | 1 | 1 | Vị trí công việc mặc định |
| 14 | access_shift_log_generate_wizard_user | shift.log.generate.wizard | base.group_user | 1 | 1 | 1 | 1 | Trợ lý tạo bản ghi ca |
| 15 | access_hr_job_level_user | hr.job.level | base.group_user | 1 | 1 | 1 | 1 | Cấp độ công việc |
| 16 | access_hr_job_grade_user | hr.job.grade | base.group_user | 1 | 1 | 1 | 1 | Hạng công việc |
| 17 | access_hr_contract_kind_user | hr.contract.kind | base.group_user | 1 | 1 | 1 | 1 | Loại hợp đồng |
| 18 | **access_hr_contract_type_internal_user** | **hr.contract.type** | **base.group_user** | **1** | **1** | **1** | **1** | ⚠️ HIGH: Dữ liệu chính, toàn bộ người dùng có thể sửa |
| 19 | **access_resignation_type_internal_user** | **x_psm_resignation_type** | **base.group_user** | **1** | **1** | **1** | **1** | ⚠️ HIGH: Mô hình cũ, toàn bộ quyền |
| 20 | access_survey_user_input_portal_user | survey.user_input | base.group_portal | 1 | 1 | 1 | 0 | Portal xem/sửa khảo sát (không xóa) |
| 21 | access_survey_question_portal_user | survey.question | base.group_portal | 1 | 0 | 0 | 0 | Portal chỉ đọc câu hỏi |
| 22 | access_approval_category_internal_user | approval.category | base.group_user | 1 | 0 | 0 | 0 | Chỉ đọc danh mục phê duyệt |

### 2.3. Quy Tắc Ghi Nhận (Record Rules - ir.rule)

**Tệp:** `addons/M02_P0214/security/offboarding_request_rules.xml`

#### Quy Tắc #1: approval.request - RST Read
```xml
<record id="rule_0214_approval_request_rst_read" model="ir.rule">
    <field name="name">approval.request - RST Read</field>
    <field name="model_id" ref="approval.model_approval_request"/>
    <field name="groups" eval="[
        (4, ref('M02_P0200.GDH_RST_HR_ADMIN_S')),
        (4, ref('M02_P0200.GDH_RST_HR_CNB_S')),
        (4, ref('M02_P0200.GDH_RST_HR_HRBP_S')),
        (4, ref('M02_P0200.GDH_RST_LND_LD_S')),
        (4, ref('M02_P0200.GDH_RST_OPS_OC_S')),
        (4, ref('M02_P0200.GDH_RST_IT_STL_S'))
    ]"/>
    <field name="perm_read">True</field>
    <field name="perm_write">False</field>
    <field name="perm_create">False</field>
    <field name="perm_unlink">False</field>
    <field name="domain_force">[("x_psm_0214_is_rst_request", "=", True)]</field>
</record>
```
**Lưu ý:** ✓ Chính xác — chỉ đọc, tất cả 6 nhóm S-level

#### Quy Tắc #2: approval.request - RST Manage
```xml
<record id="rule_0214_approval_request_rst_manage" model="ir.rule">
    <field name="name">approval.request - RST Manage</field>
    <field name="model_id" ref="approval.model_approval_request"/>
    <field name="groups" eval="[
        (4, ref('M02_P0200.GDH_RST_HR_ADMIN_M')),
        (4, ref('M02_P0200.GDH_RST_HR_CNB_M')),
        (4, ref('M02_P0200.GDH_RST_HR_HRBP_M')),
        (4, ref('M02_P0200.GDH_RST_HR_HEAD_M'))
    ]"/>
    <field name="perm_read">True</field>
    <field name="perm_write">True</field>
    <field name="perm_create">False</field>
    <field name="perm_unlink">False</field>
    <field name="domain_force">[("x_psm_0214_is_rst_request", "=", True)]</field>
</record>
```
**Lưu ý:** ✓ Chính xác — đọc/ghi nhưng không xóa

#### Quy Tắc #3: approval.request - Direct Manager (⚠️ VẤNĐỀ V-07)
```xml
<record id="rule_0214_approval_request_direct_manager_manage" model="ir.rule">
    <field name="name">approval.request - Direct Manager</field>
    <field name="model_id" ref="approval.model_approval_request"/>
    <field name="groups" eval="[(4, ref('base.group_user'))]"/>
    <field name="perm_read">True</field>
    <field name="perm_write">True</field>
    <field name="perm_create">False</field>
    <field name="perm_unlink">False</field>
    <field name="domain_force">[("manager_id.user_id", "=", user.id), ("x_psm_0214_is_rst_request", "=", True)]</field>
</record>
```
**Lưu ý:** ⚠️ MEDIUM RISK — áp dụng cho `base.group_user`, quá rộng

#### Quy Tắc #4: approval.approver - RST Read
```xml
<record id="rule_0214_approval_approver_rst_read" model="ir.rule">
    <field name="name">approval.approver - RST Read</field>
    <field name="model_id" ref="approval.model_approval_approver"/>
    <field name="groups" eval="[
        (4, ref('M02_P0200.GDH_RST_HR_ADMIN_S')),
        (4, ref('M02_P0200.GDH_RST_HR_CNB_S')),
        (4, ref('M02_P0200.GDH_RST_HR_HRBP_S')),
        (4, ref('M02_P0200.GDH_RST_LND_LD_S')),
        (4, ref('M02_P0200.GDH_RST_OPS_OC_S')),
        (4, ref('M02_P0200.GDH_RST_IT_STL_S'))
    ]"/>
    <field name="perm_read">True</field>
    <field name="perm_write">False</field>
    <field name="perm_create">False</field>
    <field name="perm_unlink">False</field>
    <field name="domain_force">[("request_id.x_psm_0214_is_rst_request", "=", True)]</field>
</record>
```
**Lưu ý:** ✓ Chính xác — chỉ đọc, tất cả 6 nhóm S-level

### 2.4. Quy Tắc Ghi Nhận Khảo Sát (Survey Record Rules)

**Tệp:** `addons/M02_P0214/security/security.xml`

#### Quy Tắc: survey.user_input - Portal Owner
```xml
<record id="rule_0214_survey_user_input_portal_owner" model="ir.rule">
    <field name="name">survey.user_input - Portal Owner</field>
    <field name="model_id" ref="survey.model_survey_user_input"/>
    <field name="groups" eval="[(4, ref('base.group_portal'))]"/>
    <field name="perm_read">True</field>
    <field name="perm_write">True</field>
    <field name="perm_create">False</field>
    <field name="perm_unlink">False</field>
    <field name="domain_force">[("partner_id", "=", user.partner_id.id)]</field>
</record>
```
**Lưu ý:** ✓ Chính xác — portal users chỉ sửa khảo sát của họ

#### Quy Tắc: survey.question - RST Groups
```xml
<record id="rule_0214_survey_question_rst_groups" model="ir.rule">
    <field name="name">survey.question - RST Groups</field>
    <field name="model_id" ref="survey.model_survey_question"/>
    <field name="groups" eval="[
        (4, ref('M02_P0200.GDH_RST_HR_ADMIN_S')),
        ...
    ]"/>
    <field name="perm_read">True</field>
    <field name="perm_write">False</field>
    <field name="perm_create">False</field>
    <field name="perm_unlink">False</field>
    <field name="domain_force">[("survey_id.name", "ilike", "Exit")]</field>
</record>
```
**Lưu ý:** ✓ Chính xác — chỉ đọc, lọc theo khảo sát Exit

### 2.5. Kiểm Soát Menu/Hành Động/Chế Độ Xem (UI-Level Security)

#### Menu và Hành Động

**Tệp:** `addons/M02_P0214/views/resignation_request_views.xml`

**Form approval.request — Các Nút Hành Động:**
```xml
<button name="action_send_social_insurance" type="object" string="Send Social Insurance"
    groups="M02_P0200.GDH_RST_HR_ADMIN_S,GDH_RST_HR_ADMIN_M,GDH_RST_HR_HEAD_M,GDH_RST_SYSTEM_ST_M"/>

<button name="action_done" type="object" string="Mark as Done"
    groups="GDH_RST_HR_ADMIN_M,GDH_RST_HR_HRBP_M,GDH_RST_HR_HEAD_M,GDH_RST_SYSTEM_ST_M"/>

<button name="action_view_my_activities" type="object" string="View Activities"
    groups="GDH_RST_HR_ADMIN_S,GDH_RST_HR_CNB_S,GDH_RST_HR_HRBP_S,GDH_RST_LND_LD_S,GDH_RST_OPS_OC_S,GDH_RST_IT_STL_S"/>
```
**Lưu ý:** ✓ Chính xác — các nút được bảo vệ bởi các nhóm thích hợp

**Tệp:** `addons/M02_P0214/views/offboarding_report_views.xml`

**Hành Động Máy Chủ (Server Action):**
```xml
<record id="action_0214_offboarding_report" model="ir.actions.server">
    <field name="name">Offboarding Report</field>
    <field name="model_id" ref="approval.model_approval_request"/>
    <field name="state">code</field>
    <field name="code">action = records.action_offboarding_report()</field>
    <field name="group_ids" eval="[
        (4, ref('M02_P0200.GDH_RST_HR_HRBP_S')),
        (4, ref('M02_P0200.GDH_RST_HR_HRBP_M')),
        (4, ref('M02_P0200.GDH_RST_HR_HEAD_M')),
        (4, ref('M02_P0200.GDH_RST_SYSTEM_ST_M'))
    ]"/>
</record>
```
**Lưu ý:** ✓ Chính xác — giới hạn cho HRBP và quản lý cao cấp

**Tệp:** `addons/M02_P0214/views/config_menu_views.xml`

**Hành Động Cấu Hình:**
```xml
<record id="action_0214_config_menu" model="ir.actions.server">
    <field name="name">Configuration Menu</field>
    <field name="group_ids" eval="[
        (4, ref('M02_P0200.GDH_RST_HR_ADMIN_M')),
        (4, ref('M02_P0200.GDH_RST_HR_HEAD_M')),
        (4, ref('M02_P0200.GDH_RST_SYSTEM_ST_M'))
    ]"/>
</record>
```
**Lưu ý:** ✓ Chính xác — chỉ quản lý admin, trưởng phòng và quản lý hệ thống

#### Chế Độ Xem (Views)

**Tệp:** `addons/M02_P0214/views/offboarding_report_views.xml`

⚠️ **VẤNĐỀ V-10:** Các chế độ xem báo cáo thiếu thuộc tính `groups`
```xml
<record id="view_0214_offboarding_report_tree" model="ir.ui.view">
    <field name="name">Offboarding Report</field>
    <field name="model">approval.request</field>
    <field name="type">tree</field>
    <!-- THIẾU: <field name="groups">...</field> -->
</record>
```

**Tệp:** `addons/M02_P0214/views/hr_employee_views.xml`

⚠️ **VẤNĐỀ V-11:** Trường nhân viên RST thiếu bảo vệ nhóm
```xml
<field name="x_psm_0214_is_rst_employee" widget="boolean" string="Is RST Employee"/>
<!-- THIẾU: groups="..." -->
```

---

## 3. Đối Chiếu Với Cấu Trúc Tổ Chức (M02_P0200)

### Các Nhóm RST Được Sử Dụng trong 0214

| Nhóm 0200 | Loại | Mục Đích Sử Dụng trong 0214 | Kiểm Soát Quền Hạn |
|-----------|------|----------------------------|-------------------|
| GDH_RST_ALL_BASE_S | Cơ sở | Quyền cơ bản cho tất cả nhân viên RST | ✓ Kế thừa `base.group_user` |
| GDH_RST_HR_ADMIN_S | Nhân viên | Admin HR | ⚠️ Không kế thừa `base.group_user` |
| GDH_RST_HR_CNB_S | Nhân viên | Tính lương | ✓ Kế thừa cấp dưới |
| GDH_RST_HR_HRBP_S | Nhân viên | HR Business Partner | ✓ Kế thừa cấp dưới |
| GDH_RST_LND_LD_S | Nhân viên | L&D (Đào tạo) | ✓ Kế thừa cấp dưới |
| GDH_RST_OPS_OC_S | Nhân viên | Operations Consultant | ✓ Kế thừa cấp dưới |
| GDH_RST_IT_STL_S | Nhân viên | IT Support Leader | ✓ Kế thừa cấp dưới |
| GDH_RST_HR_ADMIN_M | Quản lý | Quản lý Admin HR | ✓ Kế thừa cấp dưới |
| GDH_RST_HR_CNB_M | Quản lý | Quản lý Tính lương | ✓ Kế thừa cấp dưới |
| GDH_RST_HR_HRBP_M | Quản lý | Quản lý HRBP | ✓ Kế thừa cấp dưới |
| GDH_RST_HR_HEAD_M | Cấp cao | Trưởng phòng HR | ✓ Kế thừa tất cả |
| GDH_RST_SYSTEM_ST_M | Cấp cao | Quản lý Hệ Thống | ✓ Kế thừa tất cả |

### Nguyên Tắc Least Privilege (Quyền Hạn Tối Thiểu)

**Hiện Trạng:**
- ✓ Quy tắc ghi nhận hầu hết được phân cấp đúng (S-level read-only, M-level read-write)
- ✓ Nút hành động được bảo vệ bởi các nhóm thích hợp
- ⚠️ ACL quá rộng (base.group_user có quyền CRUDL cho hầu hết mô hình)
- ⚠️ Một số ACL trùng lặp với các mô-đun lõi (mail, approval)
- ⚠️ GDH_RST_HR_ADMIN_S không kế thừa base.group_user

---

## 4. Các Vấn Đề Bảo Mật Được Xác Định

### 4.1. VẤNĐỀ CRITICAL (Mức Độ 1: Tối Nguy Hiểm)

#### **V-01: ACL Trùng Lặp - mail.activity**
**Tệp:** `addons/M02_P0214/security/ir.model.access.csv:4`

**Mô Tả:**
```
access_mail_activity_internal_user,mail.activity.user,model_mail_activity,base.group_user,1,1,1,1
```

**Vấn Đề:** Mô-đun `mail` đã định nghĩa quyền truy cập cho `mail.activity`. Mục nhập này trùng lặp, gây ra xung đột tiềm ẩn khi cập nhật các mô-đun phụ thuộc.

**Tác Động:**
- **Odoo Core:** Có thể vô tình ghi đè quyền truy cập của mô-đun lõi
- **Cross-Module:** Ảnh hưởng đến helpdesk, crm, survey và các mô-đun khác sử dụng mail.activity
- **Operational:** Người dùng có thể không mong muốn có quyền xóa hoạt động (perm_unlink=1)

**Giải Pháp Được Đề Xuất:**
- Xóa dòng 4 khỏi ir.model.access.csv

---

#### **V-02: ACL Trùng Lặp - approval.request**
**Tệp:** `addons/M02_P0214/security/ir.model.access.csv:5`

**Mô Tả:**
```
access_approval_request_internal_user,approval.request.user,model_approval_request,base.group_user,1,1,1,1
```

**Vấn Đề:** Mô-đun `approval` đã định nghĩa quyền truy cập cho `approval.request`. Mục nhập này trùng lặp với lớp quyền thứ cấp (ACL + IR.RULE).

**Tác Động:**
- **Odoo Core:** Xung đột với nền tảng phê duyệt, ảnh hưởng đến các quy trình khác
- **Cross-Module:** Bất kỳ mô-đun nào sử dụng approval sẽ bị ảnh hưởng
- **Operational:** Kết hợp với ACL base.group_user (1,1,1,1) cho phép xóa yêu cầu thôi việc

**Giải Pháp Được Đề Xuất:**
- Xóa dòng 5 khỏi ir.model.access.csv
- Dựa vào IR.RULE cho kiểm soát chi tiết

---

#### **V-03: ACL Không Giới Hạn - hr.contract.type**
**Tệp:** `addons/M02_P0214/security/ir.model.access.csv:18`

**Mô Tả:**
```
access_hr_contract_type_internal_user,hr.contract.type,model_hr_contract_type,base.group_user,1,1,1,1
```

**Vấn Đề:** `hr.contract.type` là dữ liệu chính toàn hệ thống. Cho phép toàn bộ `base.group_user` (hàng trăm người dùng) sửa/xóa loại hợp đồng là vi phạm nguyên tắc least privilege.

**Tác Động:**
- **Operational:** Người dùng bình thường có thể xóa loại hợp đồng được sử dụng bởi hàng trăm hợp đồng hiện hoạt
- **Data Integrity:** Có thể gây lỗi tham chiếu (referential integrity) khi xóa các loại hợp đồng
- **Audit:** Không có cách để theo dõi ai đã sửa loại hợp đồng

**Giải Pháp Được Đề Xuất:**
- Thay đổi thành C=0, U=0 (chỉ đọc)
- Hoặc giới hạn quyền ghi cho `GDH_RST_HR_HEAD_M`, `GDH_RST_SYSTEM_ST_M`

---

#### **V-04: ACL Không Giới Hạn - x_psm_resignation_type**
**Tệp:** `addons/M02_P0214/security/ir.model.access.csv:19`

**Mô Tả:**
```
access_resignation_type_internal_user,x_psm_resignation_type,model_x_psm_resignation_type,base.group_user,1,1,1,1
```

**Vấn Đề:** `x_psm_resignation_type` là dữ liệu tham chiếu cấu hình hệ thống. Mô hình này có vẻ cũ hoặc không được sử dụng trong luồng hiện tại, nhưng nếu được sử dụng, cho phép toàn bộ `base.group_user` sửa/xóa là rủi ro.

**Tác Động:**
- **Operational:** Người dùng bình thường có thể tạo, sửa, xóa loại thôi việc
- **Consistency:** Có thể gây lỗi nếu loại bị xóa nhưng vẫn được tham chiếu trong dữ liệu cũ
- **Audit:** Khó theo dõi những thay đổi cấu hình

**Giải Pháp Được Đề Xuất:**
- Xóa hoàn toàn nếu không được sử dụng
- Hoặc giới hạn ghi cho quản lý cao cấp

---

#### **V-05: Lỗi Logic Python - _check_0214_group_access (api.model)**
**Tệp:** `addons/M02_P0214/models/approval_request_rst_fields.py:132-145`

**Mô Tả:**
```python
def _check_0214_group_access(self, required_group_string):
    """Check if user has access to perform action"""
    
    if not self:
        # BUG: Trả về True nếu self trống, không kiểm tra user groups
        return True
    
    for record in self:
        if not record.request_owner_id.user_id.has_group(required_group_string):
            return False
    return True
```

**Vấn Đề:** Khi gọi từ hành động `@api.model` (không có bộ ghi tự nhiên), `self` rỗng. Hàm trả về `True` ngay lập tức mà không kiểm tra xem người dùng hiện tại có quyền hay không.

**Bối Cảnh (Context):**
- `action_pending_offboarding_subordinates()` sử dụng `@api.model` → `self` rỗng
- Gọi `_check_0214_group_access(self._GROUP_0214_SUBORDINATE_REPORT)`
- Trả về `True` → hành động được phép cho bất kỳ người dùng nào

**Tác Động:**
- **Security:** Bypass hoàn toàn kiểm tra quyền hạn cho hành động cấp mô hình
- **Least Privilege:** Người dùng không phải quản lý cấp cao vẫn có thể gọi hành động báo cáo cấp bộ phận
- **Operational:** Dữ liệu nhân sự nhạy cảm (danh sách cấp bộ phận) được tiếp cập không được phép

**Ví Dụ Khai Thác:**
```python
# Bất kỳ người dùng nào cũng có thể gọi:
self.env['approval.request'].action_pending_offboarding_subordinates()
# _check_0214_group_access(self._GROUP_0214_SUBORDINATE_REPORT) trả về True
# → Nhận danh sách cấp bộ phận mà không có quyền
```

**Giải Pháp Được Đề Xuất:**
```python
def _check_0214_group_access(self, required_group_string):
    """Check if user has access to perform action"""
    
    if not self:
        # FIX: Kiểm tra user hiện tại thay vì trả về True
        return self.env.user.has_group(required_group_string)
    
    for record in self:
        if not record.request_owner_id.user_id.has_group(required_group_string):
            return False
    return True
```

---

#### **V-06: Lỗi Logic Python - action_done (Deactivation Risk)**
**Tệp:** `addons/M02_P0214/models/approval_request_rst_approval.py:79-108`

**Mô Tả:**
```python
def action_done(self):
    """Mark offboarding request as completed"""
    for request in self:
        user_to_deactivate = request.x_psm_0214_user_to_deactivate_id
        
        # DANGER: Chỉ kiểm tra base.group_system, không kiểm tra quản lý cao cấp
        if user_to_deactivate and not user_to_deactivate.has_group('base.group_system'):
            user_to_deactivate.active = False
            user_to_deactivate.partner_id.active = False
    
    # Tiếp tục logic hoàn thành...
```

**Vấn Đề:** Khi đánh dấu yêu cầu thôi việc là "hoàn thành", hệ thống tự động vô hiệu hóa người dùng. Kiểm tra `base.group_system` quá hẹp. Những người dùng là quản lý cao cấp (GDH_RST_HR_HEAD_M, GDH_RST_SYSTEM_ST_M) không nằm trong base.group_system → có thể bị vô hiệu hóa.

**Tác Động:**
- **Operational:** Vô tình vô hiệu hóa quản lý cao cấp nếu họ nằm trong danh sách nhân viên thôi việc
- **Data Integrity:** Vô hiệu hóa partner của họ → mất quyền truy cập hệ thống
- **Audit:** Không có cách khôi phục tự động

**Giải Pháp Được Đề Xuất:**
```python
def action_done(self):
    """Mark offboarding request as completed"""
    for request in self:
        user_to_deactivate = request.x_psm_0214_user_to_deactivate_id
        
        # FIX: Kiểm tra cả base.group_system và quản lý cao cấp
        if user_to_deactivate and not (
            user_to_deactivate.has_group('base.group_system') or
            user_to_deactivate.has_group('M02_P0200.GDH_RST_HR_HEAD_M') or
            user_to_deactivate.has_group('M02_P0200.GDH_RST_SYSTEM_ST_M')
        ):
            user_to_deactivate.active = False
            user_to_deactivate.partner_id.active = False
    
    # Tiếp tục logic hoàn thành...
```

---

### 4.2. VẤNĐỀ HIGH (Mức Độ 2: Nguy Hiểm Cao)

#### **V-07: Record Rule Quá Rộng - Direct Manager**
**Tệp:** `addons/M02_P0214/security/offboarding_request_rules.xml`

**Mô Tả:**
```xml
<record id="rule_0214_approval_request_direct_manager_manage" model="ir.rule">
    <field name="name">approval.request - Direct Manager</field>
    <field name="groups" eval="[(4, ref('base.group_user'))]"/>
    <field name="domain_force">[("manager_id.user_id", "=", user.id), ("x_psm_0214_is_rst_request", "=", True)]</field>
</record>
```

**Vấn Đề:** Quy tắc này áp dụng cho tất cả `base.group_user` (hàng trăm người dùng). Mặc dù miền lọc bằng `manager_id.user_id = user.id`, nhưng:
1. Quy tắc phía trên `rule_0214_approval_request_rst_manage` cũng cấp quyền đọc/ghi cho M-level managers
2. Người dùng ngoài RST có thể sử dụng `manager_id` để truy cập

**Tác Động:**
- **Cross-Module:** Ảnh hưởng đến người dùng từ các mô-đun khác (OPS, cửa hàng)
- **Least Privilege:** Quá rộng, nên dành cho nhóm cụ thể

**Giải Pháp Được Đề Xuất:**
- Thay đổi `groups` thành chỉ những nhóm quản lý thực tế (M-level RST + OPS)

---

#### **V-08: Bảo Vệ Portal ACL - survey.user_input**
**Tệp:** `addons/M02_P0214/security/ir.model.access.csv:20`

**Mô Tả:**
```
access_survey_user_input_portal_user,survey.user_input,model_survey_user_input,base.group_portal,1,1,1,0
```

**Vấn Đề:** Portal users có quyền sửa (W=1) `survey.user_input` mà không cấu hình `Record Rule` để giới hạn quyền. Mặc dù ACL IR.RULE có quy tắc `rule_0214_survey_user_input_portal_owner` (owner check), nhưng:
1. Nếu xóa IR.RULE, portal users có quyền truy cập tất cả khảo sát
2. Điều này cho phép chỉnh sửa phản hồi khảo sát của các nhân viên khác

**Tác Động:**
- **Operational:** Portal users có thể sửa khảo sát của nhân viên khác (nếu IR.RULE bị xóa)
- **Data Integrity:** Dữ liệu khảo sát Exit Interview không đáng tin cậy

**Giải Pháp Được Đề Xuất:**
- Đảm bảo IR.RULE `rule_0214_survey_user_input_portal_owner` luôn hoạt động
- Thêm bình luận trong ir.model.access.csv để giải thích dependency

---

#### **V-09: Override Global - mail.activity.unlink()**
**Tệp:** `addons/M02_P0214/models/mail_activity.py:70-89`

**Mô Tả:**
```python
class MailActivity(models.Model):
    _inherit = "mail.activity"
    
    def unlink(self):
        """Override: Archive instead of delete for RST-related activities"""
        rst_activities = self.filtered(
            lambda a: (
                (a.res_model == 'approval.request' and a.res_id.x_psm_0214_is_rst_request) or
                (a.res_model == 'hr.employee' and a.res_id.x_psm_0214_is_rst_employee)
            )
        )
        rst_activities.active = False
        
        (self - rst_activities).unlink()
```

**Vấn Đề:** Thay đổi toàn cục hành vi `unlink()` cho tất cả mô-đun khác sử dụng `mail.activity`. Điều này ảnh hưởng đến:
1. Helpdesk (help desk activity management)
2. CRM (lead/opportunity activities)
3. HR (non-RST activities)

**Tác Động:**
- **Cross-Module:** Người dùng không thể xóa hoạt động từ các mô-đun khác
- **Operational:** Audit trail bị ảnh hưởng (archive thay vì xóa)
- **Unexpected Behavior:** Người dùng mong đợi xóa nhưng chỉ bị lưu trữ

**Giải Pháp Được Đề Xuất:**
- Thay đổi hành vi chỉ cho `approval.request` RST-specific
- Tạo method `archive_instead_of_unlink()` và gọi từ các hành động 0214 cụ thể

---

#### **V-10: Thiếu Group Attribute Trên Views**
**Tệp:** `addons/M02_P0214/views/offboarding_report_views.xml`

**Mô Tả:**
```xml
<record id="view_0214_offboarding_report_tree" model="ir.ui.view">
    <field name="name">Offboarding Report Tree</field>
    <field name="model">approval.request</field>
    <field name="type">tree</field>
    <!-- THIẾU: <field name="groups">GDH_RST_HR_HRBP_M,GDH_RST_HR_HEAD_M</field> -->
</record>
```

**Vấn Đề:** Các chế độ xem không có thuộc tính `groups`, cho phép bất kỳ người dùng nào có quyền đọc `approval.request` xem báo cáo này.

**Tác Động:**
- **UI/UX:** Người dùng bình thường sẽ thấy menu báo cáo nhưng nhấn vào sẽ không có dữ liệu (do IR.RULE)
- **Consistency:** Hành động có `group_ids`, nhưng chế độ xem không

**Giải Pháp Được Đề Xuất:**
- Thêm `<field name="groups">...</field>` vào tất cả chế độ xem báo cáo

---

#### **V-11: Trường Nhân Viên RST Thiếu Bảo Vệ**
**Tệp:** `addons/M02_P0214/views/hr_employee_views.xml`

**Mô Tả:**
```xml
<field name="x_psm_0214_is_rst_employee" widget="boolean" string="Is RST Employee"/>
```

**Vấn Đề:** Trường này không có thuộc tính `groups`, cho phép bất kỳ người dùng nào có quyền sửa `hr.employee` sửa cờ RST.

**Tác Động:**
- **Data Integrity:** Người dùng có thể thay đổi trạng thái RST của nhân viên
- **Audit:** Khó theo dõi thay đổi
- **Operational:** Có thể gây lỗi trong luồng công việc RST

**Giải Pháp Được Đề Xuất:**
- Thêm `groups="M02_P0200.GDH_RST_HR_HEAD_M,M02_P0200.GDH_RST_SYSTEM_ST_M"`

---

#### **V-12: Logic Kiểm Tra Quyền Sở Hữu - Portal Activity**
**Tệp:** `addons/M02_P0214/controllers/main.py`

**Mô Tả:**
```python
@http.route('/my/resignation/rst/activity/done', auth='user', methods=['POST'])
def post_activity_done(self, activity_id, **kwargs):
    activity = request.env['mail.activity'].browse(activity_id)
    
    # ISSUE: Kiểm tra có thể bỏ sót edge cases
    if activity.user_id != request.env.user:
        raise AccessDenied("Not your activity")
    
    activity.action_done()
```

**Vấn Đề:** Kiểm tra sở hữu cơ bản nhưng có thể có các edge cases:
1. Hoạt động được chỉ định cho quản lý, không phải người dùng
2. Hoạt động nhóm (group-assigned activities)

**Tác Động:**
- **Portal Security:** Portal users có thể không thể hoàn thành hoạt động được chỉ định cho quản lý
- **Workflow:** Luồng công việc có thể bị trì trệ

**Giải Pháp Được Đề Xuất:**
- Kiểm tra rõ: `activity.user_id == user OR activity.group_id có người dùng`

---

### 4.3. VẤNĐỀ MEDIUM (Mức Độ 3: Rủi Ro Trung Bình)

#### **V-13: GDH_RST_HR_ADMIN_S Không Kế Thừa Base Group**
**Tệp:** `addons/M02_P0200/security/security.xml:31-34` (tham chiếu từ 0214)

**Mô Tả:**
```xml
<record id="GDH_RST_HR_ADMIN_S" model="res.groups">
    <field name="name">Nhân viên admin</field>
    <!-- MISSING: <field name="implied_ids" eval="[(4, ref('GDH_RST_ALL_BASE_S'))]"/> -->
</record>
```

**Vấn Đề:** Nhóm này không kế thừa `GDH_RST_ALL_BASE_S` hoặc `base.group_user`, cho nên nhân viên admin HR không có quyền truy cập các chức năng cơ bản của Odoo.

**Tác Động:**
- **Operational:** HR admin không thể truy cập các công cụ cơ bản
- **Workflow:** Có thể cần xử lý thủ công hoặc cấp quyền bổ sung

**Giải Pháp Được Đề Xuất:**
- Thêm `<field name="implied_ids" eval="[(4, ref('GDH_RST_ALL_BASE_S'))]"/>` vào định nghĩa nhóm trong M02_P0200

---

#### **V-14: Xung Đột Nhóm - GDH_RST_SYSTEM_ST_M vs Quản Lý Khác**
**Tệp:** `addons/M02_P0200/security/security.xml:205-215`

**Mô Tả:**
```xml
<record id="GDH_RST_SYSTEM_ST_M" model="res.groups">
    <field name="implied_ids" eval="[
        (4, ref('GDH_RST_ALL_BASE_S')), 
        (4, ref('GDH_RST_HR_HEAD_M')),
        ...
    ]"/>
</record>
```

**Vấn Đề:** `GDH_RST_SYSTEM_ST_M` kế thừa `GDH_RST_HR_HEAD_M`, `GDH_RST_LND_MANAGER_M`, `GDH_RST_IT_HEAD_M`. Điều này tạo ra xung đột tiềm ẩn nếu một người dùng có nhiều vai trò quản lý từ các bộ phận khác nhau.

**Tác Động:**
- **Least Privilege:** System manager tự động có quyền của tất cả các bộ phận
- **Audit:** Khó theo dõi quyền thực tế (implied vs direct)

**Giải Pháp Được Đề Xuất:**
- Tài liệu hóa rõ ràng (comment trong XML)
- Xem xét phân tách thành các nhóm riêng biệt

---

#### **V-15: Portal User Có Quyền Tạo Khảo Sát (Không Áp Dụng)**
**Tệp:** `addons/M02_P0214/security/ir.model.access.csv:20-21`

**Mô Tả:**
```
access_survey_user_input_portal_user,survey.user_input,model_survey_user_input,base.group_portal,1,1,1,0
access_survey_question_portal_user,survey.question,model_survey_question,base.group_portal,1,0,0,0
```

**Vấn Đề:** Portal users có quyền tạo (C=1) `survey.user_input` nhưng không thể tạo câu hỏi. Điều này có thể cho phép tạo khảo sát bất thường.

**Tác Động:**
- **Data Integrity:** Portal users có thể tạo phản hồi khảo sát ngoài dự kiến

**Giải Pháp Được Đề Xuất:**
- Thay đổi C=0 (không cho phép tạo)
- Hoặc sử dụng workflow để kiểm soát việc tạo phản hồi

---

#### **V-16: Sudo() Không Giới Hạn Trong Survey**
**Tệp:** `addons/M02_P0214/models/survey_user_input.py:7-8`

**Mô Tả:**
```python
def _get_linked_0214_request(self, user_input):
    return self.env["approval.request"].sudo().search(...)
```

**Vấn Đề:** Sử dụng `sudo()` để tìm kiếm yêu cầu phê duyệt liên kết. Nếu không cấu hình đúng, có thể tiếp cập dữ liệu của người dùng khác.

**Tác Động:**
- **Information Disclosure:** Có thể tiếp cập thông tin của nhân viên khác

**Giải Pháp Được Đề Xuất:**
- Thêm bình luận giải thích tại sao cần `sudo()`
- Xem xét giới hạn miền tìm kiếm

---

### 4.4. VẤNĐỀ LOW (Mức Độ 4: Rủi Ro Thấp)

#### **V-17: Documentation Gap**
**Tệp:** Toàn bộ module

**Mô Tả:** Không có tài liệu rõ ràng về các quyền hạn được yêu cầu cho từng hành động.

**Giải Pháp Được Đề Xuất:**
- Thêm docstring trong Python methods
- Tạo tài liệu SECURITY.md trong module

---

## 5. Kế Hoạch Triển Khai Khắc Phục (6 Giai Đoạn)

### Giai Đoạn 1: Chuẩn Hóa ACL (ACL Normalization)

**Mục Tiêu:** Loại bỏ các mục nhập ACL trùng lặp và không được phép.

**Các Bước Triển Khai:**

1. **Xóa Mục Nhập Trùng Lặp mail.activity**
   - **Tệp:** `addons/M02_P0214/security/ir.model.access.csv`
   - **Thay Đổi:** Xóa dòng 4
   - **Tiên Điều Kiện:** Xác nhận rằng `mail` module đã cấp quyền
   - **Kiểm Tra:** Xác thực rằng người dùng HR vẫn có thể tạo hoạt động trên yêu cầu
   - **Khôi Phục:** Thêm lại dòng 4 nếu kiểm tra thất bại

2. **Xóa Mục Nhập Trùng Lặp approval.request**
   - **Tệp:** `addons/M02_P0214/security/ir.model.access.csv`
   - **Thay Đổi:** Xóa dòng 5
   - **Tiên Điều Kiện:** Xác nhận rằng `approval` module đã cấp quyền
   - **Kiểm Tra:** Xác thực rằng IR.RULE vẫn kiểm soát quyền hạn
   - **Khôi Phục:** Thêm lại dòng 5 nếu kiểm tra thất bại

3. **Giới Hạn Quyền hr.contract.type**
   - **Tệp:** `addons/M02_P0214/security/ir.model.access.csv`
   - **Thay Đổi Dòng 18:**
     ```
     FROM: access_hr_contract_type_internal_user,hr.contract.type,model_hr_contract_type,base.group_user,1,1,1,1
     TO: access_hr_contract_type_internal_user,hr.contract.type,model_hr_contract_type,base.group_user,1,0,0,0
     ```
   - **Tiên Điều Kiện:** Tạo ACL riêng cho quản lý cao cấp (nếu cần ghi)
   - **Kiểm Tra:** Xác thực rằng người dùng bình thường chỉ có thể đọc
   - **Khôi Phục:** Khôi phục quyền ghi nếu cần

4. **Loại Bỏ hoặc Giới Hạn x_psm_resignation_type**
   - **Tệp:** `addons/M02_P0214/security/ir.model.access.csv`
   - **Tùy Chọn A - Xóa Dòng 19:** Nếu mô hình không được sử dụng
   - **Tùy Chọn B - Giới Hạn:** Nếu cần thiết
     ```
     FROM: access_resignation_type_internal_user,x_psm_resignation_type,model_x_psm_resignation_type,base.group_user,1,1,1,1
     TO: access_resignation_type_internal_user,x_psm_resignation_type,model_x_psm_resignation_type,base.group_user,1,0,0,0
     ```
   - **Tiên Điều Kiện:** Kiểm tra xem mô hình có đang được sử dụng không
   - **Kiểm Tra:** Xác thực tác động đến luồng công việc
   - **Khôi Phục:** Khôi phục quyền đầy đủ nếu cần

---

### Giai Đoạn 2: Áp Dụng Quy Tắc Ghi Nhận Chính Xác (Record Rules Refinement)

**Mục Tiêu:** Thay đổi quy tắc quá rộng và thêm kiểm soát cụ thể.

**Các Bước Triển Khai:**

1. **Thay Đổi Rule Direct Manager**
   - **Tệp:** `addons/M02_P0214/security/offboarding_request_rules.xml`
   - **Thay Đổi:** Giới hạn `groups` chỉ cho những nhóm quản lý RST
     ```xml
     FROM: <field name="groups" eval="[(4, ref('base.group_user'))]"/>
     TO: <field name="groups" eval="[
         (4, ref('M02_P0200.GDH_RST_HR_ADMIN_M')),
         (4, ref('M02_P0200.GDH_RST_HR_CNB_M')),
         (4, ref('M02_P0200.GDH_RST_HR_HRBP_M')),
         (4, ref('M02_P0200.GDH_RST_HR_HEAD_M')),
         (4, ref('M02_P0200.GDH_OPS_STORE_RGM_M'))
     ]"/>
     ```
   - **Tiên Điều Kiện:** Xác nhận danh sách nhóm quản lý
   - **Kiểm Tra:** Xác thực rằng quản lý không RST không thể truy cập
   - **Khôi Phục:** Khôi phục groups gốc

2. **Thêm Bình Luận Về Dependency IR.RULE**
   - **Tệp:** `addons/M02_P0214/security/ir.model.access.csv`
   - **Thay Đổi:** Thêm bình luận dòng 20-21
     ```
     # NOTE: survey.user_input portal access requires ir.rule 'rule_0214_survey_user_input_portal_owner' to be active
     ```

---

### Giai Đoạn 3: Khắc Phục Logic Python (Python Logic Fixes)

**Mục Tiêu:** Sửa lỗi bảo mật trong các phương thức Python.

**Các Bước Triển Khai:**

1. **Khắc Phục _check_0214_group_access (V-05)**
   - **Tệp:** `addons/M02_P0214/models/approval_request_rst_fields.py`
   - **Thay Đổi Dòng 132-145:**
     ```python
     def _check_0214_group_access(self, required_group_string):
         """Check if user has access to perform action"""
         
         if not self:
             # FIX: Kiểm tra user hiện tại thay vì trả về True
             return self.env.user.has_group(required_group_string)
         
         for record in self:
             if not record.request_owner_id.user_id.has_group(required_group_string):
                 return False
         return True
     ```
   - **Tiên Điều Kiện:** Backup code gốc
   - **Kiểm Tra:** Unit test với hành động @api.model
   - **Khôi Phục:** Restore code gốc nếu test thất bại

2. **Khắc Phục action_done (V-06)**
   - **Tệp:** `addons/M02_P0214/models/approval_request_rst_approval.py`
   - **Thay Đổi Dòng 79-108:**
     ```python
     def action_done(self):
         """Mark offboarding request as completed"""
         for request in self:
             user_to_deactivate = request.x_psm_0214_user_to_deactivate_id
             
             # FIX: Kiểm tra cả base.group_system và quản lý cao cấp
             if user_to_deactivate and not (
                 user_to_deactivate.has_group('base.group_system') or
                 user_to_deactivate.has_group('M02_P0200.GDH_RST_HR_HEAD_M') or
                 user_to_deactivate.has_group('M02_P0200.GDH_RST_SYSTEM_ST_M')
             ):
                 user_to_deactivate.active = False
                 user_to_deactivate.partner_id.active = False
     ```
   - **Tiên Điều Kiện:** Backup code gốc
   - **Kiểm Tra:** Xác thực rằng quản lý cao cấp không bị vô hiệu hóa
   - **Khôi Phục:** Restore code gốc nếu test thất bại

3. **Khắc Phục mail.activity.unlink() (V-09)**
   - **Tệp:** `addons/M02_P0214/models/mail_activity.py`
   - **Thay Đổi Dòng 70-89:**
     ```python
     def archive_rst_activities(self):
         """Archive instead of delete RST-related activities"""
         rst_activities = self.filtered(
             lambda a: (
                 (a.res_model == 'approval.request' and a.res_id.x_psm_0214_is_rst_request) or
                 (a.res_model == 'hr.employee' and a.res_id.x_psm_0214_is_rst_employee)
             )
         )
         rst_activities.write({'active': False})
     
     # NOTE: Không override unlink(), gọi archive_rst_activities() từ 0214 actions thay vì
     ```
   - **Tiên Điều Kiện:** Backup code gốc
   - **Kiểm Tra:** Xác thực rằng các mô-đun khác không bị ảnh hưởng
   - **Khôi Phục:** Restore code gốc nếu test thất bại

---

### Giai Đoạn 4: Tăng Cường Bảo Vệ Chế Độ Xem (View Hardening)

**Mục Tiêu:** Thêm `groups` attribute vào các chế độ xem và trường.

**Các Bước Triển Khai:**

1. **Thêm Groups Vào Chế Độ Xem Báo Cáo**
   - **Tệp:** `addons/M02_P0214/views/offboarding_report_views.xml`
   - **Thay Đổi Tất Cả Chế Độ Xem:**
     ```xml
     THÊM: <field name="groups">M02_P0200.GDH_RST_HR_HRBP_S,M02_P0200.GDH_RST_HR_HRBP_M,M02_P0200.GDH_RST_HR_HEAD_M,M02_P0200.GDH_RST_SYSTEM_ST_M</field>
     ```
   - **Tiên Điều Kiện:** Xác nhận chế độ xem nào cần bảo vệ
   - **Kiểm Tra:** UI test với các nhóm khác nhau
   - **Khôi Phục:** Xóa `groups` nếu cần

2. **Bảo Vệ Trường is_rst_employee**
   - **Tệp:** `addons/M02_P0214/views/hr_employee_views.xml`
   - **Thay Đổi:**
     ```xml
     THÊM: groups="M02_P0200.GDH_RST_HR_HEAD_M,M02_P0200.GDH_RST_SYSTEM_ST_M"
     ```
   - **Tiên Điều Kiện:** Backup view gốc
   - **Kiểm Tra:** UI test xác thực rằng trường bị ẩn cho nhân viên bình thường
   - **Khôi Phục:** Xóa `groups` nếu cần

---

### Giai Đoạn 5: Kiểm Tra Toàn Diện (Comprehensive Testing)

**Mục Tiêu:** Xác thực rằng các thay đổi không phá vỡ luồng công việc.

**Các Bước Triển Khai:**

1. **Kiểm Tra Đơn Vị (Unit Tests)**
   - Tạo test cases cho từng fix
   - Xác thực kiểm tra quyền hạn

2. **Kiểm Tra Tích Hợp (Integration Tests)**
   - Kiểm tra luồng công việc hoàn chỉnh
   - Xác thực rằng các mô-đun khác không bị ảnh hưởng

3. **Kiểm Tra Quận Sát (UAT - User Acceptance Testing)**
   - Kiểm tra bởi các nhóm người dùng khác nhau
   - Thu thập phản hồi

---

### Giai Đoạn 6: Tái Tạo Bản Đồ Mô-đun (Module Map Regeneration)

**Mục Tiêu:** Cập nhật tài liệu để phản ánh các thay đổi.

**Các Bước Triển Khai:**

1. **Cập Nhật module_map.json**
   - Cập nhật số lượng ACL rules
   - Cập nhật danh sách affected models
   - Cập nhật notes và security status

2. **Tạo SECURITY.md**
   - Tài liệu hóa các quyền hạn cần thiết cho từng hành động
   - Tài liệu hóa các group dependencies

3. **Cập Nhật KE_HOACH_TRIEN_KHAI**
   - Ghi lại các thay đổi
   - Cập nhật trạng thái triển khai

---

## 6. Ma Trận Kiểm Tra (Test Matrix)

### Các Nhân Vật Kiểm Tra (Test Personas)

| # | Nhân Vật | Nhóm(s) | Mô Tả | Lợi Ích Kiểm Tra |
|---|---------|---------|-------|-----------------|
| 1 | HR Admin Staff | GDH_RST_HR_ADMIN_S | Nhân viên quản trị HR cấp dưới | Kiểm tra ACL S-level |
| 2 | HR Admin Manager | GDH_RST_HR_ADMIN_M | Quản lý quản trị HR | Kiểm tra ACL M-level |
| 3 | HR Payroll Staff | GDH_RST_HR_CNB_S | Nhân viên tính lương | Kiểm tra workflow tính lương |
| 4 | HR HRBP | GDH_RST_HR_HRBP_M | Quản lý HRBP | Kiểm tra báo cáo offboarding |
| 5 | HR Head | GDH_RST_HR_HEAD_M | Trưởng phòng HR | Kiểm tra quyền cao nhất |
| 6 | System Manager | GDH_RST_SYSTEM_ST_M | Quản lý hệ thống | Kiểm tra quyền cao nhất |
| 7 | Store Manager | GDH_OPS_STORE_RGM_M | Cửa hàng trưởng | Kiểm tra direct manager rule |
| 8 | Portal User | base.group_portal | Nhân viên xin thôi việc | Kiểm tra portal access |
| 9 | Regular User | base.group_user | Người dùng bình thường | Kiểm tra negative cases |

### Chi Tiết Kiểm Tra (Test Cases)

#### Yêu Cầu Xin Thôi Việc (approval.request)

| Kịch Bản | Nhân Vật | Hành Động | Kỳ Vọng | Ghi Chú |
|---------|---------|----------|--------|---------|
| **ACL - Đọc Dữ Liệu** | | | | |
| 1 | HR Admin Staff | Xem danh sách yêu cầu RST | ✓ Thành công (IR.RULE S-level) | Kiểm tra rule_rst_read |
| 2 | Regular User | Xem danh sách yêu cầu RST | ✗ Thất bại (IR.RULE từ chối) | Kiểm tra least privilege |
| **ACL - Ghi Dữ Liệu** | | | | |
| 3 | HR Admin Staff | Sửa yêu cầu RST | ✗ Thất bại (W=False trong IR.RULE) | Kiểm tra read-only |
| 4 | HR Admin Manager | Sửa yêu cầu RST | ✓ Thành công (IR.RULE M-level) | Kiểm tra manage rule |
| 5 | Regular User (Manager) | Sửa yêu cầu con (direct mgmt) | ✓ Thành công (Direct Manager Rule) | Kiểm tra manager access |
| **Hành Động - Gửi Khảo Sát** | | | | |
| 6 | HR Admin Staff | Nhấn "Send Exit Survey" | ✓ Thành công (Check _GROUP_0214_HR_PROCESS) | Kiểm tra hành động kiểm tra |
| 7 | HR Payroll Staff | Nhấn "Send Exit Survey" | ✗ Thất bại (Không thuộc _GROUP_0214_HR_PROCESS) | Kiểm tra từ chối |
| **Hành Động - Hoàn Thành (action_done)** | | | | |
| 8 | HR Admin Manager | Nhấn "Mark as Done" | ✓ Thành công + Vô hiệu hóa user | Kiểm tra deactivation |
| 9 | HR Head | Nhấn "Mark as Done" trên yêu cầu của HR Head | ✓ Thành công (Kiểm tra GDH_RST_HR_HEAD_M) | Kiểm tra protection fix V-06 |
| 10 | System Manager | Nhấn "Mark as Done" | ✓ Thành công (Quyền cao nhất) | Kiểm tra quyền cao nhất |
| **Hành Động - Báo Cáo Cấp Bộ Phận** | | | | |
| 11 | HR Admin Manager | Gọi action_pending_offboarding_subordinates | ✓ Thành công (Kiểm tra _check_0214_group_access fix V-05) | Kiểm tra fix api.model |
| 12 | Regular User | Gọi action_pending_offboarding_subordinates | ✗ Thất bại (Không thuộc nhóm) | Kiểm tra from chối |

#### Khảo Sát (survey.user_input / survey.question)

| Kịch Bản | Nhân Vật | Hành Động | Kỳ Vọng | Ghi Chú |
|---------|---------|----------|--------|---------|
| **Portal ACL** | | | | |
| 13 | Portal User | Xem khảo sát của mình | ✓ Thành công (Portal rule + ACL) | Kiểm tra portal owner filter |
| 14 | Portal User A | Xem khảo sát của Portal User B | ✗ Thất bại (Partner filter) | Kiểm tra sự riêng tư |
| 15 | Portal User | Sửa phản hồi khảo sát của mình | ✓ Thành công (W=1 + owner check) | Kiểm tra edit access |
| 16 | Portal User | Xóa khảo sát của mình | ✗ Thất bại (U=0 trong ACL) | Kiểm tra delete restriction |
| **Internal User ACL** | | | | |
| 17 | HR Admin Staff | Xem câu hỏi khảo sát | ✓ Thành công (Survey rule + ACL) | Kiểm tra survey read |
| 18 | Regular User | Xem câu hỏi khảo sát | ✗ Thất bại (IR.RULE từ chối) | Kiểm tra từ chối |

#### Hoạt Động (mail.activity)

| Kịch Bản | Nhân Vật | Hành Động | Kỳ Vọng | Ghi Chú |
|---------|---------|----------|--------|---------|
| **Activity Unlink** | | | | |
| 19 | HR Admin Manager | Xóa hoạt động trên yêu cầu RST | ✗ Hoặc Archive (nếu fix V-09) | Kiểm tra unlink override |
| 20 | HR Admin Manager | Xóa hoạt động trên đơn HV khác | ✓ Xóa bình thường (ngoài RST) | Kiểm tra cross-module impact |

#### Nhân Viên (hr.employee)

| Kịch Bản | Nhân Vật | Hành Động | Kỳ Vọng | Ghi Chú |
|---------|---------|----------|--------|---------|
| **Trường is_rst_employee** | | | | |
| 21 | HR Admin Staff | Xem trường is_rst_employee | ✗ Bị ẩn (Nếu fix V-11) | Kiểm tra field group attribute |
| 22 | HR Head | Xem trường is_rst_employee | ✓ Thành công (Group được phép) | Kiểm tra visibility |
| 23 | HR Admin Staff | Sửa trường is_rst_employee | ✗ Thất bại (Không có quyền) | Kiểm tra write protection |
| 24 | HR Head | Sửa trường is_rst_employee | ✓ Thành công | Kiểm tra M-level write |

#### Loại Hợp Đồng (hr.contract.type)

| Kịch Bản | Nhân Vật | Hành Động | Kỳ Vọng (Sau Fix V-03) | Ghi Chú |
|---------|---------|----------|--------|---------|
| 25 | Regular User | Xem loại hợp đồng | ✓ Thành công (Read=1) | Kiểm tra read access |
| 26 | Regular User | Tạo loại hợp đồng mới | ✗ Thất bại (Create=0 sau fix) | Kiểm tra create protection |
| 27 | Regular User | Sửa loại hợp đồng | ✗ Thất bại (Write=0 sau fix) | Kiểm tra write protection |
| 28 | Regular User | Xóa loại hợp đồng | ✗ Thất bại (Unlink=0 sau fix) | Kiểm tra delete protection |
| 29 | HR Head | Sửa loại hợp đồng | ✓ Hoặc thất bại (tuỳ vào chiến lược) | Kiểm tra quản lý access |

#### Loại Thôi Việc (x_psm_resignation_type)

| Kịch Bản | Nhân Vật | Hành Động | Kỳ Vọng (Sau Fix V-04) | Ghi Chú |
|---------|---------|----------|--------|---------|
| 30 | Regular User | Xem loại thôi việc | ✓ Thành công (Read=1) | Kiểm tra read access |
| 31 | Regular User | Tạo loại thôi việc | ✗ Thất bại (Create=0 sau fix) | Kiểm tra create protection |

#### Portal Routes (Controllers)

| Kịch Bản | Nhân Vật | Hành Động | Kỳ Vọng | Ghi Chú |
|---------|---------|----------|--------|---------|
| **GET /my/resignation/rst** | | | | |
| 32 | Portal User (đã xác thực) | Truy cập form xin thôi việc | ✓ Thành công | Kiểm tra auth="user" |
| 33 | Khách (không đăng nhập) | Truy cập form xin thôi việc | ✗ Chuyển hướng đăng nhập | Kiểm tra auth requirement |
| **POST /my/resignation/rst/submit** | | | | |
| 34 | Portal User | Gửi form xin thôi việc | ✓ Thành công + tạo yêu cầu | Kiểm tra create via portal |
| 35 | Portal User | Gửi lần thứ hai | ✗ Thất bại (Kiểm tra logic) | Kiểm tra duplicate prevention |
| **POST /my/resignation/rst/activity/done** | | | | |
| 36 | Portal User | Hoàn thành hoạt động của mình | ✓ Thành công (Kiểm tra sở hữu) | Kiểm tra ownership check V-12 |
| 37 | Portal User A | Hoàn thành hoạt động của Portal User B | ✗ Thất bại (Không sở hữu) | Kiểm tra từ chối |

---

## 7. Chiến Lược Triển Khai & Rollback

### Thứ Tự Triển Khai Được Khuyến Nghị

1. **Giai Đoạn 1 - ACL Normalization (Tuần 1)**
   - Giai đoạn này ít rủi ro nhất (loại bỏ trùng lặp, giới hạn dữ liệu chính)
   - Có thể triển khai tương đối nhanh

2. **Giai Đoạn 3 - Python Logic Fixes (Tuần 2)**
   - Khắc phục các lỗi bảo mật quan trọng (V-05, V-06, V-09)
   - Đòi hỏi kiểm tra kỹ lưỡng

3. **Giai Đoạn 2 - Record Rules Refinement (Tuần 2-3)**
   - Thay đổi IR.RULE có thể ảnh hưởng đến hiệu suất câu truy vấn
   - Cần kiểm tra tính năng manager reporting

4. **Giai Đoạn 4 - View Hardening (Tuần 3)**
   - Thay đổi UI, ít rủi ro dữ liệu
   - Có thể triển khai nhanh

5. **Giai Đoạn 5 - Testing (Tuần 4-5)**
   - Chạy toàn bộ ma trận kiểm tra
   - Xác thực rằng không có regression

6. **Giai Đoạn 6 - Documentation (Tuần 5)**
   - Cập nhật tài liệu
   - Hoàn thiện

### Kế Hoạch Rollback (Khôi Phục)

**Cho Mỗi Giai Đoạn:**

1. **Trước Triển Khai:**
   - Tạo backup cơ sở dữ liệu
   - Ghi lại trạng thái hiện tại (git commit)

2. **Nếu Kiểm Tra Thất Bại:**
   - Git revert (nếu thay đổi code)
   - Hoặc cập nhật XML/CSV để khôi phục giá trị gốc

3. **Nếu Kiểm Tra Đơn Vị Thất Bại:**
   - Chỉnh sửa logic và chạy lại
   - Không cần rollback nếu chưa triển khai

4. **Nếu Kiểm Tra Tích Hợp Thất Bại:**
   - Khôi phục code
   - Điều tra vấn đề
   - Tạo hotfix riêng biệt

5. **Nếu UAT Phát Hiện Vấn Đề:**
   - Rollback tất cả giai đoạn (nếu cần)
   - Cộng tác với người dùng để xác định nguyên nhân

---

## 8. Kết Luận và Khuyến Nghị

### Tóm Tắt Kết Quả Rà Soát

1. **Số Lượng Vấn Đề Được Xác Định:** 17
   - Critical: 5 vấn đề (V-01 đến V-06)
   - High: 6 vấn đề (V-07 đến V-12)
   - Medium: 4 vấn đề (V-13 đến V-16)
   - Low: 1 vấn đề (V-17)

2. **Mức Độ Nghiêm Trọng Tổng Thể:** CAO
   - 3 lỗi trong logic kiểm tra quyền hạn (V-05, V-06)
   - 2 ACL trùng lặp với các mô-đun lõi (V-01, V-02)
   - 3 ACL quá rộng cho dữ liệu chính (V-03, V-04)
   - 1 override toàn cục ảnh hưởng đến các mô-đun khác (V-09)

3. **Tác Động Tiềm Ẩn:**
   - **Odoo Core:** Xung đột với mail, approval modules
   - **Cross-Module:** Ảnh hưởng đến helpdesk, crm, hr, survey
   - **Operational:** Có thể vô tình vô hiệu hóa quản lý cao cấp, phơi bày dữ liệu nhân sự
   - **Audit:** Khó theo dõi thay đổi cấu hình, không có tài liệu rõ ràng

### Khuyến Nghị Hành Động (Action Items)

#### Ngay Lập Tức (Before Production)

1. ✅ **Khắc Phục V-05 (Python Logic - api.model)**
   - Ưu tiên CRITICAL
   - Có thể bị khai thác để truy cập dữ liệu báo cáo không được phép
   - Ước tính công sức: 2-4 giờ

2. ✅ **Khắc Phục V-06 (action_done Deactivation)**
   - Ưu tiên CRITICAL
   - Có thể vô tình vô hiệu hóa quản lý cao cấp
   - Ước tính công sức: 1-2 giờ

3. ✅ **Xóa ACL Trùng Lặp V-01, V-02**
   - Ưu tiên CRITICAL
   - Xung đột với các mô-đun lõi
   - Ước tính công sức: 30 phút

#### Trong Vòng 1-2 Tuần (Before Release)

4. ✅ **Khắc Phục V-03, V-04 (ACL Master Data)**
   - Ưu tiên HIGH
   - Giới hạn quyền ghi dữ liệu chính
   - Ước tính công sức: 1 giờ

5. ✅ **Khắc Phục V-09 (mail.activity.unlink Override)**
   - Ưu tiên HIGH
   - Ảnh hưởng đến các mô-đun khác
   - Ước tính công sức: 2-3 giờ

6. ✅ **Thay Đổi V-07, V-08 (Record Rules)**
   - Ưu tiên HIGH
   - Giới hạn quyền truy cập quá rộng
   - Ước tính công sức: 2 giờ

#### Trong Vòng 1 Tháng (Before Full Rollout)

7. ✅ **Khắc Phục V-10, V-11, V-12 (View Hardening & Logic)**
   - Ưu tiên MEDIUM
   - Cải thiện UI/UX security
   - Ước tính công sức: 3-4 giờ

8. ✅ **Khắc Phục V-13, V-14, V-15, V-16 (Structural Issues)**
   - Ưu tiên MEDIUM
   - Cải thiện hiểu biết cấu trúc nhóm
   - Ước tính công sức: 2-3 giờ

9. ✅ **Tạo Tài Liệu SECURITY.md**
   - Ưu tiên MEDIUM
   - Giúp triển khai và bảo trì trong tương lai
   - Ước tính công sức: 4-6 giờ

#### Dài Hạn (Optimization & Process)

10. ✅ **Tự Động Hóa Kiểm Tra Bảo Mật**
    - Tạo unit tests cho tất cả hành động kiểm tra quyền hạn
    - Thêm linting rules cho ACL chuẩn hóa
    - Ước tính công sức: 8-10 giờ

### Độc Lập Với Module M02_P0200

**Vấn Đề Cấu Trúc (V-13, V-14):**
- GDH_RST_HR_ADMIN_S không kế thừa base.group_user
- GDH_RST_SYSTEM_ST_M kế thừa quá nhiều nhóm

**Khuyến Nghị:**
- Lên kế hoạch audit M02_P0200 cấu trúc nhóm
- Xem xét phân tách các nhóm thành các danh mục rõ ràng
- Tài liệu hóa implied_ids hierarchy

### Tổng Kết

Module M02_P0214 có **16 vấn đề bảo mật đáng kể** từ critical đến medium level. Việc khắc phục các vấn đề critical ngay lập tức là bắt buộc để tránh tiếp xúc bảo mật. Sau đó, các vấn đề high/medium có thể được khắc phục theo giai đoạn kế hoạch 6 giai đoạn được đề xuất.

**Tổng Ước Tính Công Sức:** 25-35 giờ (khoảng 1 tuần với 1 kỹ sư

**Kiểm Tra Dự Kiến:** 15-20 giờ (tuần thứ 2-3)

**Tài Liệu Hóa:** 4-6 giờ (tuần thứ 4)

---

## Phụ Lục A: Tham Chiếu Nhanh Vấn Đề

| ID | Tên Tiếng Anh | Tên Tiếng Việt | Tệp | Dòng | Mức Độ | Trạng Thái |
|----|--------------|-----------------|-----|------|--------|----------|
| V-01 | Duplicate ACL - mail.activity | ACL Trùng Lặp - mail.activity | ir.model.access.csv | 4 | CRITICAL | Đơn Vị: Delete |
| V-02 | Duplicate ACL - approval.request | ACL Trùng Lặp - approval.request | ir.model.access.csv | 5 | CRITICAL | Đơn Vị: Delete |
| V-03 | Unrestricted ACL - hr.contract.type | ACL Không Giới Hạn - hr.contract.type | ir.model.access.csv | 18 | CRITICAL | Đơn Vị: Restrict |
| V-04 | Unrestricted ACL - x_psm_resignation_type | ACL Không Giới Hạn - x_psm_resignation_type | ir.model.access.csv | 19 | CRITICAL | Đơn Vị: Delete/Restrict |
| V-05 | Python Logic - api.model Bypass | Lỗi Logic Python - api.model Bypass | approval_request_rst_fields.py | 132-145 | CRITICAL | Đơn Vị: Check user.has_group |
| V-06 | Python Logic - Deactivation Risk | Lỗi Logic Python - Rủi Ro Vô Hiệu Hóa | approval_request_rst_approval.py | 79-108 | CRITICAL | Đơn Vị: Check M-level groups |
| V-07 | Record Rule Too Broad | Record Rule Quá Rộng | offboarding_request_rules.xml | N/A | HIGH | Đơn Vị: Limit groups |
| V-08 | Portal ACL Dependency | Dependency ACL Portal | ir.model.access.csv | 20 | HIGH | Đơn Vị: Document |
| V-09 | Global Override - mail.activity.unlink | Override Toàn Cục - mail.activity.unlink | mail_activity.py | 70-89 | HIGH | Đơn Vị: Refactor |
| V-10 | Missing Groups on Views | Thiếu Groups Trên Chế Độ Xem | offboarding_report_views.xml | N/A | HIGH | Đơn Vị: Add groups |
| V-11 | Unprotected Field - is_rst_employee | Trường Không Bảo Vệ - is_rst_employee | hr_employee_views.xml | N/A | HIGH | Đơn Vị: Add groups |
| V-12 | Portal Ownership Check Logic | Logic Kiểm Tra Sở Hữu Portal | main.py | N/A | HIGH | Đơn Vị: Review logic |
| V-13 | Group Structure - Missing Inheritance | Cấu Trúc Nhóm - Thiếu Kế Thừa | security.xml (M02_P0200) | 31-34 | MEDIUM | Đơn Vị: Add implied_ids |
| V-14 | Group Structure - Circular Inheritance | Cấu Trúc Nhóm - Kế Thừa Vòng | security.xml (M02_P0200) | 205-215 | MEDIUM | Đơn Vị: Document/Refactor |
| V-15 | Portal Create Restriction | Hạn Chế Tạo Portal | ir.model.access.csv | 20 | MEDIUM | Đơn Vị: Change C=0 |
| V-16 | Sudo Usage Without Limits | Sudo Không Giới Hạn | survey_user_input.py | 7-8 | MEDIUM | Đơn Vị: Document |
| V-17 | Documentation Gap | Khoảng Trống Tài Liệu | Toàn Bộ Module | N/A | LOW | Đơn Vị: Create SECURITY.md |

---

**Báo Cáo kết thúc tại 2026-05-15**

