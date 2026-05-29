# Rà Soát Phân Quyền Module M02_P0213 - Báo Cáo Chi Tiết

**Ngày rà soát:** 2026-05-14  
**Phiên bản Odoo:** 19 Enterprise  
**Module:** M02_P0213 (Quy Trình Offboarding OPS)  
**Vai trò:** Senior Odoo Security Architect  

---

## Mục Lục

1. [Phạm Vi Rà Soát](#phạm-vi-rà-soát)
2. [Tóm Tắt Hiện Trạng](#tóm-tắt-hiện-trạng)
3. [Đối Chiếu Với Module 0200](#đối-chiếu-với-module-0200)
4. [Các Vấn Đề Phát Hiện](#các-vấn-đề-phát-hiện)
5. [Plan Triển Khai Codex](#plan-triển-khai-codex)
6. [Ma Trận Test](#ma-trận-test)
7. [Kết Luận Và Khuyến Cáo](#kết-luận-và-khuyến-cáo)

---

## Phạm Vi Rà Soát

### 1. Tài Liệu Quy Ước

- **QUY_UOC_DAT_TEN_VA_RULE.md**: Quy ước đặt tên field (x_psm_0213_*), model (x_psm_*), group (group_gdh_rst_*), nguyên tắc ưu tiên tái sử dụng cái sẵn có, phân quyền tối thiểu, tách bạch rõ ràng

### 2. Cấu Trúc Module

- **module_map_stats.json**: 70 file detail, 71 relations, 7 model, 5 view, 3 security file, 2 controller file

### 3. File Phân Quyền Chính

**security/ir.model.access.csv** (45 dòng)
**security/security.xml** (5 rules)
**security/offboarding_request_rules.xml** (7 rules)

### 4. File Code Liên Quan

- models/resignation_request.py (1340 dòng)
- models/mail_activity.py
- models/survey_user_input.py
- models/res_company.py
- models/res_config_settings.py
- models/hr_department.py
- controllers/main.py (220 dòng)
- views/*.xml (multiple files)
- data/*.xml (4 files)

### 5. Module Tham Chiếu

- Module 0200: Cung cấp định nghĩa 20+ group (GDH_RST_*, GDH_OPS_*)
- Odoo 19 Approvals Module: approval.request, approval.category, approval.approver, approval.product_line

---

## Tóm Tắt Hiện Trạng

### 1. Nhóm Quyền (Groups)

Module 0213 **tái sử dụng hoàn toàn** 20+ group từ module 0200:

**Nhóm HR:**
- GDH_RST_HR_RECRUITMENT_S/M
- GDH_RST_HR_CNB_S/M
- GDH_RST_HR_HRBP_S/M
- GDH_RST_HR_ADMIN_S/M
- GDH_RST_HR_HEAD_M

**Nhóm OPS:**
- GDH_RST_OPS_OC_S (Operation Center Supervisor)
- GDH_RST_OPS_OM_M (Operation Manager)

**Nhóm IT, L&D, Quản Lý, Hệ Thống:**
- GDH_RST_IT_* (6 group)
- GDH_RST_LND_* (2 group)
- GDH_RST_MGMT_MANAGER_M
- GDH_RST_SYSTEM_ST_M

**Nhóm Base:**
- base.group_user (nhân viên nội bộ)
- base.group_portal (khách hàng/nhà cung cấp)

### 2. Quyền Truy Cập (ACL - ir.model.access.csv)

#### a. Quyền Vô Nghĩa (Dòng 2-3)
```
access_mail_activity_internal_user       | mail.activity | base.group_user | 0/0/0/0  ← VÔ NGHĨA
access_approval_request_internal_user    | approval.request | base.group_user | 0/0/0/0 ← VÔ NGHĨA
```

#### b. Quyền Quá Rộng (Dòng 4)
```
access_hr_employee_internal_user | hr.employee | base.group_user | 1/1/0/0
```
⚠️ **VẤN ĐỀ:** Đè quyền chuẩn của HR module. group_user bình thường không nên write hr.employee.

#### c. Quyền Survey (Dòng 5-12)
```
access_survey_survey_internal_user          | survey.survey | base.group_user | 1/0/0/0
access_survey_question_internal_user        | survey.question | base.group_user | 1/1/0/0  ← WRITE
access_survey_question_answer_internal_user | survey.question_answer | base.group_user | 1/1/0/0 ← WRITE
access_survey_user_input_internal_user      | survey.user_input | base.group_user | 1/1/1/1 ← CREATE/WRITE
access_survey_survey_portal                 | survey.survey | base.group_portal | 1/0/0/0
access_survey_question_portal               | survey.question | base.group_portal | 1/0/0/0
access_survey_question_answer_portal        | survey.question_answer | base.group_portal | 1/0/0/0
access_survey_user_input_portal             | survey.user_input | base.group_portal | 1/1/1/1 ← CREATE/WRITE
```

⚠️ **VẤN ĐỀ:** group_user và group_portal có quyền tạo/sửa survey.user_input cho **bất kỳ survey nào** trong hệ thống, không chỉ exit interview. Ảnh hưởng đến tất cả survey khác.

#### d. Quyền hr.contract.type (Dòng 13-14)
```
access_hr_contract_type_internal_user | hr.contract.type | base.group_user | 1/1/0/0  ← WRITE
access_hr_contract_type_portal        | base.group_portal | 1/0/0/0
```

⚠️ **VẤN ĐỀ:** group_user có thể sửa dữ liệu hệ thống hr.contract.type. Không cần thiết.

#### e. Quyền Approval + Offboarding (Dòng 15-45)
```
Cấu trúc: GDH_RST_HR_ADMIN_S/M, GDH_RST_HR_HRBP_M, GDH_RST_HR_HEAD_M, GDH_RST_OPS_OC_S, 
GDH_RST_OPS_OM_M, GDH_RST_IT_*, GDH_RST_LND_*, GDH_RST_SYSTEM_ST_M
Quyền: read hoặc read+write trên approval.request, approval.approver, mail.activity, survey.user_input
```

✅ **HỢP LÝ:** Cấp quyền rõ ràng theo từng nhóm chuyên môn.

### 3. Record Rules (ir.rule)

#### a. Security.xml (5 rules - Survey)

**rule_psm_0213_survey_internal_read**
- Model: survey.survey
- Áp dụng: 7 group (OPS/HR)
- Domain: [(1, '=', 1)] - **Allow all**
- Loại: Để survey.survey có thể truy cập trong offboarding workflow

**rule_psm_0213_survey_question_internal_read**
- Model: survey.question
- Áp dụng: 7 group (OPS/HR)
- Domain: [(1, '=', 1)] - **Allow all**

**rule_psm_0213_survey_question_answer_internal_read**
- Model: survey.question_answer
- Áp dụng: 7 group (OPS/HR)
- Domain: [(1, '=', 1)] - **Allow all**

**rule_psm_0213_survey_user_input_portal_own**
- Model: survey.user_input
- Áp dụng: base.group_portal
- Domain: [('partner_id', '=', user.partner_id.id), ('|'), ('email', '=', user.email)]
- Loại: **Portal chỉ thấy user_input của mình** ✅ HỢP LÝ

**rule_psm_0213_survey_user_input_internal_results_read**
- Model: survey.user_input
- Áp dụng: base.group_user
- Domain: [('survey_id.x_psm_0213_is_exit_survey', '=', True), ('state', '=', 'completed')]
- Loại: **Internal user chỉ thấy kết quả survey xong** ✅ HỢP LÝ

#### b. offboarding_request_rules.xml (7 rules - Offboarding Workflow)

Tất cả rule dùng prefix `rule_0213_*` (KHÔNG nhất quán với `rule_psm_0213_*` ở security.xml).

**rule_0213_approval_request_ops_read**
- Model: approval.request
- Áp dụng: GDH_RST_OPS_OC_S, GDH_RST_OPS_OM_M
- Domain: [('category_id.x_psm_0213_is_offboarding', '=', True)]
- Quyền: read only

**rule_0213_approval_request_hr_read**
- Model: approval.request
- Áp dụng: 6 HR group (RECRUITMENT, CNB, HRBP, ADMIN, HEAD)
- Domain: [('category_id.x_psm_0213_is_offboarding', '=', True)]
- Quyền: read only

**rule_0213_approval_request_hr_write**
- Model: approval.request
- Áp dụng: GDH_RST_HR_ADMIN_S/M, GDH_RST_HR_HRBP_M, GDH_RST_HR_HEAD_M, GDH_RST_SYSTEM_ST_M
- Domain: [('category_id.x_psm_0213_is_offboarding', '=', True)]
- Quyền: write

**rule_0213_approval_approver_scope_read**
- Model: approval.approver
- Áp dụng: 8 group (HR, OPS)
- Domain: [('approval_request_id.category_id.x_psm_0213_is_offboarding', '=', True)]
- Quyền: read only

**rule_0213_mail_activity_scope_read**
- Model: mail.activity
- Áp dụng: 8 group (HR, OPS)
- Domain: [('x_psm_0213_is_offboarding_activity', '=', True)]
- Quyền: read only

**rule_0213_mail_activity_hr_write**
- Model: mail.activity
- Áp dụng: 4 HR group (ADMIN, HRBP, HEAD, SYSTEM)
- Domain: [('x_psm_0213_is_offboarding_activity', '=', True)]
- Quyền: write

✅ **HỢP LÝ:** Các rule dùng domain `x_psm_0213_is_offboarding=True` để giới hạn chỉ workflow offboarding, tránh ảnh hưởng approval.request khác.

### 4. Menu/Action/View Visibility

**Menu "OPS Offboarding Configuration"**
```xml
menuitem groups="approvals.group_approval_manager,GDH_RST_HR_ADMIN_M,GDH_RST_HR_HEAD_M,GDH_RST_SYSTEM_ST_M"
```
✅ **HỢP LÝ:** Chỉ admin/system có quyền truy cập cấu hình.

**Form approval.request - Tab "Thông tin nghỉ việc" và "Quá trình nghỉ việc"**
```xml
groups="GDH_RST_OPS_OC_S,...,GDH_RST_SYSTEM_ST_M"  (8 group)
```
✅ **HỢP LÝ:** Cấp đúng cho nhóm liên quan.

**Buttons Action**
- action_send_social_insurance: GDH_RST_HR_HRBP_M, GDH_RST_HR_ADMIN_M
- action_send_adecco_notification: GDH_RST_OPS_OC_S, GDH_RST_OPS_OM_M
- action_done: GDH_RST_HR_HRBP_M
- action_rehire: GDH_RST_HR_HRBP_M
- action_blacklist: GDH_RST_HR_ADMIN_M, GDH_RST_HR_HEAD_M

✅ **HỢP LÝ:** Từng action cấp cho nhóm chuyên môn phù hợp.

### 5. Logic Kiểm Tra Quyền (Python)

**models/resignation_request.py**

```python
_GROUP_0213_OPS_SCOPE = [
    'GDH_RST_OPS_OC_S', 'GDH_RST_OPS_OM_M',
    'GDH_RST_HR_ADMIN_S', 'GDH_RST_HR_ADMIN_M', 'GDH_RST_HR_HEAD_M',
    'GDH_RST_SYSTEM_ST_M'
]

_GROUP_0213_SURVEY_RESULTS = [
    'GDH_RST_HR_HRBP_S', 'GDH_RST_HR_HRBP_M', 'GDH_RST_HR_HEAD_M',
    'GDH_RST_HR_ADMIN_S', 'GDH_RST_HR_ADMIN_M', 'GDH_RST_SYSTEM_ST_M'
]

_GROUP_0213_REMINDER = [...]
_GROUP_0213_HR_PROCESS = [...]
_GROUP_0213_DONE = [...]
_GROUP_0213_REHIRE = [...]
_GROUP_0213_BLACKLIST = [...]

def _check_0213_group_access(self, action_type):
    if self.env.user.has_group('base.group_system'):
        return True
    if self.env.context.get('bypass_0213_group_check'):
        return True
    
    allowed_groups = getattr(self, f'_GROUP_0213_{action_type}', [])
    user_groups = self.env.user.groups_id.mapped('name')
    
    if not any(g in user_groups for g in allowed_groups):
        raise AccessError(f"Không có quyền thực hiện {action_type}")
```

✅ **HỢP LÝ:** Kiểm tra group trước khi thực hiện action, có flag bypass cho admin/system.

**models/mail_activity.py**

```python
def unlink(self):
    """Ngăn xóa offboarding activity, archive thay vào đó"""
    offboarding_activities = self.filtered('x_psm_0213_is_offboarding_activity')
    if offboarding_activities:
        offboarding_activities.write({'active': False})
        return True
    return super().unlink()
```

✅ **HỢP LÝ:** Bảo vệ dữ liệu activity trong offboarding workflow.

**models/survey_user_input.py**

```python
def _mark_done(self):
    """Auto mark activity "Hoàn thành Exit Interview" khi survey done"""
    res = super()._mark_done()
    if self.survey_id.x_psm_0213_is_exit_survey:
        # Auto mark exit interview activity
        self.env['mail.activity'].search([
            ('summary', '=', 'Hoàn thành Exit Interview'),
            ('x_psm_0213_is_offboarding_activity', '=', True),
            ('res_model', '=', 'approval.request'),
            ('res_id', '=', self.approval_request_id.id),
            ('state', '!=', 'done')
        ]).action_done()
    return res
```

✅ **HỢP LÝ:** Tự động đánh dấu activity khi có điều kiện.

**controllers/main.py**

```python
@route('/my/resignation/submit', auth='user', methods=['POST'])
def submit_resignation_request(self):
    """Tạo approval.request bằng sudo nhưng lock theo user.id"""
    request = request.env['approval.request'].with_user(SUPERUSER_ID).create({
        'category_id': resignation_category.id,
        'request_owner_id': request.env.user.id,  ← LOCK TẠI ĐÂY
        'approver_ids': [(6, 0, [employee.parent_id.user_id.id])]
    })
    return request
```

⚠️ **LƯU Ý:** Dùng sudo() tạo request nhưng phải lock `request_owner_id = user.id` và `category_id` để user không thay đổi.

### 6. Cron Job

**ir_cron_data.xml**
```xml
<record id="action_psm_0213_offboarding_reminder_cron" model="ir.cron">
    <field name="name">Offboarding: Remind Pending Activities</field>
    <field name="model_id" ref="approvals.model_approval_request"/>
    <field name="code">model._cron_send_offboarding_reminders()</field>
    <field name="interval_number">3</field>
    <field name="interval_type">days</field>
</record>
```

⚠️ **VẤN ĐỀ:** Cron không dùng sudo() - phụ thuộc vào quyền user chạy cron.

---

## Đối Chiếu Với Module 0200

### 1. Group Tái Sử Dụng

Module 0213 **KHÔNG định nghĩa group riêng**, hoàn toàn tái sử dụng 20+ group từ 0200:

```
Module 0200 → Định Nghĩa Group
        ↓
Module 0213 → Dùng Group (ir.model.access.csv, ir.rule)
```

✅ **HỢP LÝ:** Tránh trùng lặp, dễ quản lý.

### 2. Implied IDs Chain (SỰ CỐ)

**VẤN ĐỀ HỮU ĐỨC:** Nhiều group từ 0200 **KHÔNG implied base.group_user**

```
✅ CÓ IMPLIED base.group_user:
   GDH_RST_ALL_BASE_S → base.group_user
   GDH_RST_HR_RECRUITMENT_S/M → base.group_user
   GDH_RST_HR_ADMIN_S/M → base.group_user (implied chain)
   GDH_RST_HR_HEAD_M → base.group_user (implied chain)
   GDH_RST_IT_* → base.group_user
   GDH_RST_LND_* → base.group_user

❌ KHÔNG IMPLIED base.group_user:
   GDH_RST_OPS_OC_S → KHÔNG (SỰ CỐ KIẾN TRÚC 0200)
   GDH_RST_OPS_OM_M → KHÔNG (SỰ CỐ KIẾN TRÚC 0200)
   GDH_RST_HR_HRBP_S → KHÔNG (SỰ CỐ KIẾN TRÚC 0200)
   GDH_RST_HR_HRBP_M → KHÔNG (SỰ CỐ KIẾN TRÚC 0200)
   GDH_RST_HR_CNB_S/M → ?
```

**HẬU QUẢ:**
- User chỉ có GDH_RST_OPS_OC_S → **KHÔNG thể truy cập các model cấp cho base.group_user**, ví dụ:
  - ir.ui.menu (menu browse)
  - partner (khách hàng)
  - res.users (danh sách nhân viên)
  - Các model khác cấp cho base.group_user mặc định

**KHUYẾN CÁO:** Cần liên hệ module 0200 để fix implied_ids. Hoặc trong 0213 phải cấp thêm ACL cho các group này trên các model cơ bản.

### 3. Naming Convention

**Module 0200:**
```
group_gdh_rst_<department>_<role>_<level>

Ví dụ:
- group_gdh_rst_hr_admin_s
- group_gdh_rst_ops_oc_s
- group_gdh_rst_system_st_m
```

**Module 0213:**
```
Dùng lại group từ 0200
security/ir.model.access.csv: GDH_RST_<department>_<role>_<level> (UPPERCASE)
security/*.xml rule name: rule_0213_* hoặc rule_psm_0213_* (KHÔNG NHẤT QUÁN)
```

⚠️ **VẤN ĐỀ:** Naming rule không nhất quán:
- security.xml dùng `rule_psm_0213_*` (5 rule survey)
- offboarding_request_rules.xml dùng `rule_0213_*` (7 rule offboarding)

**KHUYẾN CÁO:** Thống nhất thành `rule_0213_*` cho tất cả.

### 4. Field x_psm_0213_*

Module 0213 thêm field tùy chỉnh để giới hạn scope:
- approval.category: `x_psm_0213_is_offboarding` (Boolean)
- approval.request: 30+ field (x_psm_0213_resignation_reason, x_psm_0213_employee_id, ...)
- mail.activity: `x_psm_0213_is_offboarding_activity` (Boolean, computed)
- survey: `x_psm_0213_is_exit_survey` (Boolean)
- hr.department: `x_psm_0213_it_user_id` (Many2one)

✅ **HỢP LÝ:** Theo convention QUY_UOC_DAT_TEN_VA_RULE.md.

**VẤN ĐỀ:** Field `x_psm_0213_is_offboarding` trên approval.category không protected:
```python
# Hiện tại: bất kỳ ai write approval.category đều có thể đổi flag này
# Nên: cấp write quyền cho x_psm_0213_is_offboarding chỉ cho HR admin
```

---

## Các Vấn Đề Phát Hiện

### VẤN ĐỀ 1 (CRITICAL): ACL Quá Rộng hr.employee

**Vị trí:** security/ir.model.access.csv dòng 4

```
access_hr_employee_internal_user | hr.employee | base.group_user | 1/1/0/0
```

**Mô Tả:**
- group_user (nhân viên nội bộ) có quyền **WRITE** trên model hr.employee
- Điều này **ĐÈ QUYỀN CỬ CHẦ** của module HR gốc
- Theo HR module chuẩn, chỉ HR user (group_hr_user) mới được write hr.employee

**Tác Động:**
- Nhân viên bình thường có thể sửa dữ liệu nhân sự của mình hoặc nhân viên khác
- Vi phạm nguyên tắc least privilege

**Giải Pháp:**
- XÓA dòng này hoặc đổi thành read-only (1/0/0/0)
- Nếu cần write, phải cấp cho group HR cụ thể, không phải base.group_user

**Mức Ưu Tiên:** **CRITICAL**

---

### VẤN ĐỀ 2 (CRITICAL): ACL Mở Read Toàn Bộ Survey Cho group_user

**Vị Trí:** security/ir.model.access.csv dòng 5-12

```
access_survey_survey_internal_user
access_survey_question_internal_user (1/1/0/0 - CÓ WRITE)
access_survey_question_answer_internal_user (1/1/0/0 - CÓ WRITE)
access_survey_user_input_internal_user (1/1/1/1 - CREATE/WRITE)
```

**Mô Tả:**
- group_user có quyền tạo/sửa **survey.user_input cho BẤT KỲ survey nào** trong hệ thống
- Không chỉ giới hạn trong exit interview survey

**Tác Động:**
- Ảnh hưởng đến **TẤT CẢ survey khác** trong Odoo (employee satisfaction, training feedback, khảo sát khách hàng, v.v.)
- group_user có thể modify dữ liệu survey không liên quan đến offboarding
- Rủi ro bảo mật cao

**Giải Pháp:**
- Dùng record rule (ir.rule) để giới hạn: group_user chỉ thấy survey có `x_psm_0213_is_exit_survey=True`
- Hoặc: cấp quyền survey chỉ cho các group HR liên quan (HR_ADMIN, HR_HRBP, ...)
- **ĐÃ CÓ rule** rule_psm_0213_survey_user_input_internal_results_read, nhưng rule này **KHÔNG giới hạn CREATE/WRITE**

**Mức Ưu Tiên:** **CRITICAL**

---

### VẤN ĐỀ 3 (CRITICAL): ACL Mở Write survey.user_input Cho group_portal

**Vị Trí:** security/ir.model.access.csv dòng 11-12

```
access_survey_user_input_portal | survey.user_input | base.group_portal | 1/1/1/1
```

**Mô Tả:**
- group_portal (khách hàng/nhà cung cấp bên ngoài) có quyền **tạo survey.user_input** cho **bất kỳ survey nào**

**Tác Động:**
- Portal user có thể spam/abuse hệ thống survey
- Tạo dữ liệu giả mạo
- Ảnh hưởng đến tất cả survey trong hệ thống

**Giải Pháp:**
- Dùng record rule để giới hạn: portal chỉ tạo user_input cho exit interview survey
- Hoặc: xóa quyền CREATE/WRITE, chỉ cấp READ

**LƯU Ý:** Đã có rule `rule_psm_0213_survey_user_input_portal_own` để portal chỉ thấy user_input của mình, nhưng rule này **KHÔNG giới hạn survey nào** được tạo.

**Mức Ưu Tiên:** **CRITICAL**

---

### VẤN ĐỀ 4 (CRITICAL): Vấn Đề Kiến Trúc Module 0200 - Implied IDs Chain

**Vị Trí:** Module 0200 security/security.xml

**Mô Tả:**
- Group GDH_RST_OPS_OC_S, GDH_RST_OPS_OM_M, GDH_RST_HR_HRBP_S/M, GDH_RST_HR_CNB_S/M **KHÔNG implied base.group_user**
- Điều này làm **vô hiệu hóa phần lớn ACL cấp cho base.group_user** trong module 0213

**Ví Dụ Cụ Thể:**
```
User có group: GDH_RST_OPS_OC_S (Supervisor OPS)
ACL cấp: ir.ui.menu 1/0/0/0 cho base.group_user
Kết quả: User KHÔNG THẤY MENU vì GDH_RST_OPS_OC_S không implied base.group_user
```

**Tác Động:**
- User chỉ có group từ OPS/HRBP không thể duyệt hệ thống như nhân viên bình thường
- Các field/action cấp cho base.group_user không hoạt động
- Trải nghiệm người dùng bị đứt gãy

**Giải Pháp:**
- **NGẮN HẠN (0213):** Cấp thêm ACL trên các model cơ bản cho các group OPS/HRBP
- **DÀI HẠN (0200):** Fix module 0200 để tất cả group implied base.group_user

**Mức Ưu Tiên:** **CRITICAL**

---

### VẤN ĐỀ 5 (HIGH): ACL No-Op 0/0/0/0 Không Cần Thiết

**Vị Trí:** security/ir.model.access.csv dòng 2-3

```
access_mail_activity_internal_user | mail.activity | base.group_user | 0/0/0/0
access_approval_request_internal_user | approval.request | base.group_user | 0/0/0/0
```

**Mô Tả:**
- Cấp quyền 0/0/0/0 = không quyền gì cả = vô nghĩa
- Nếu không cấp quyền thì xóa dòng, đừng cấp 0/0/0/0

**Tác Động:**
- Gây nhầm lẫn cho người đọc code
- Không biết liệu dòng này bị quên hay cố ý
- Làm dài file không cần thiết

**Giải Pháp:**
- XÓA 2 dòng này
- Nếu cần lịch sử, viết comment git log thay vì dòng ACL

**Mức Ưu Tiên:** **HIGH**

---

### VẤN ĐỀ 6 (HIGH): ACL Write hr.contract.type Cho group_user Không Cần Thiết

**Vị Trí:** security/ir.model.access.csv dòng 13-14

```
access_hr_contract_type_internal_user | hr.contract.type | base.group_user | 1/1/0/0
access_hr_contract_type_portal | hr.contract.type | base.group_portal | 1/0/0/0
```

**Mô Tả:**
- hr.contract.type là dữ liệu hệ thống (cấp hạn, loại hợp đồng)
- group_user không nên write dữ liệu này

**Tác Động:**
- Nhân viên có thể sửa loại hợp đồng trong lương bộc phát

**Giải Pháp:**
- Đổi thành 1/0/0/0 (read-only)
- Hoặc xóa nếu không cần

**Mức Ưu Tiên:** **HIGH**

---

### VẤN ĐỀ 7 (MEDIUM): Field x_psm_0213_is_offboarding Không Protected

**Vị Trí:** models/resignation_request.py (ApprovalCategory._inherit 'approval.category')

**Mô Tả:**
```python
x_psm_0213_is_offboarding = fields.Boolean(default=False)
```

- Field này dùng để giới hạn scope approval.request trong rule
- Hiện tại **KHÔNG protected**, bất kỳ ai write approval.category đều có thể đổi

**Tác Động:**
- User có thể giả mạo một approval.request thường thành offboarding hoặc ngược lại
- Bypass record rule bằng cách thay đổi flag

**Giải Pháp:**
- Dùng `@api.constrains('x_psm_0213_is_offboarding')` để kiểm tra quyền
- Hoặc: cấp write quyền cho field này chỉ cho admin
- Hoặc: không cho phép thay đổi sau khi tạo

**Lưu Ý:** approve.category thường là dữ liệu cấu hình, write được cấp chỉ cho admin, nên có thể đã protected bởi rule/ACL chuẩn.

**Mức Ưu Tiên:** **MEDIUM**

---

### VẤN ĐỀ 8 (MEDIUM): Cron Không Dùng sudo()

**Vị Trí:** data/ir_cron_data.xml

```xml
<field name="code">model._cron_send_offboarding_reminders()</field>
```

**Mô Tả:**
- Cron chạy với quyền user (thường là user chạy cron, có thể là anonymous)
- Nếu user không có quyền approval.request/mail.activity thì cron thất bại

**Tác Động:**
- Cron có thể chạy không thành công
- Nhắc nhở offboarding không được gửi

**Giải Pháp:**
```python
def _cron_send_offboarding_reminders(self):
    # Thêm .sudo()
    offboarding_requests = self.sudo().search([...])
```

**Mức Ưu Tiên:** **MEDIUM**

---

### VẤN ĐỀ 9 (MEDIUM): Naming Rule Không Nhất Quán

**Vị Trí:** security/security.xml vs security/offboarding_request_rules.xml

```
security.xml:
  rule_psm_0213_survey_internal_read
  rule_psm_0213_survey_question_internal_read
  rule_psm_0213_survey_question_answer_internal_read
  rule_psm_0213_survey_user_input_portal_own
  rule_psm_0213_survey_user_input_internal_results_read

offboarding_request_rules.xml:
  rule_0213_approval_request_ops_read
  rule_0213_approval_request_hr_read
  rule_0213_approval_request_hr_write
  rule_0213_approval_approver_scope_read
  rule_0213_mail_activity_scope_read
  rule_0213_mail_activity_hr_write
```

**Mô Tả:**
- 5 rule survey dùng `rule_psm_0213_*`
- 7 rule offboarding dùng `rule_0213_*`
- **KHÔNG NHẤT QUÁN**

**Tác Động:**
- Gây nhầm lẫn khi tìm kiếm rule
- Khó bảo trì

**Giải Pháp:**
- Thống nhất thành `rule_0213_*` cho tất cả

**Mức Ưu Tiên:** **MEDIUM**

---

### VẤN ĐỀ 10 (LOW): Thiếu ACL Cho survey.survey Cho group_portal

**Vị Trí:** security/ir.model.access.csv dòng 9

```
access_survey_survey_portal | survey.survey | base.group_portal | 1/0/0/0
```

**Mô Tả:**
- Portal có read survey.survey nhưng không thể browse danh sách survey
- Chỉ có thể dùng direct link hoặc embed trong trang

**Tác Động:**
- Thiểu nhất

**Giải Pháp:**
- Kiểm tra xem survey exit interview có được render trong portal form không, nếu có thì đã đủ

**Mức Ưu Tiên:** **LOW**

---

### VẤN ĐỀ 11 (LOW): Comment Tiếng Việt Không Dấu Trong Code

**Vị Trí:** Các file .py có comment không dấu hoặc dấu không đúng

**Mô Tả:**
- Comment Python: "Khong co quyen" thay vì "Không có quyền"
- Comment XML: "Viet Nam" thay vì "Việt Nam"

**Tác Động:**
- Khó đọc, bất chuyên nghiệp
- Nhưng không ảnh hưởng tính năng

**Giải Pháp:**
- Đổi thành tiếng Việt có dấu đầy đủ
- Dùng UTF-8 encoding trong tất cả file

**Lưu Ý:** User yêu cầu "Không tự ý xóa comment có sẵn trong code, đặc biệt là comment tiếng Việt không dấu", vậy nên fix comment này cần cẩn thận.

**Mức Ưu Tiên:** **LOW**

---

## Plan Triển Khai Codex

### PHASE 0: Chuẩn Bị (Tuần 1)

**Bước 1: Liên Hệ Module 0200 - Yêu Cầu Fix Implied IDs**

```
Yêu cầu: Fix module 0200 security/security.xml
- GDH_RST_OPS_OC_S, GDH_RST_OPS_OM_M: thêm implied_ids ref('base.group_user')
- GDH_RST_HR_HRBP_S/M: thêm implied_ids ref('base.group_user')
- GDH_RST_HR_CNB_S/M: cần xác nhận, có thể thiếu

Tác Động: 0213 có thể dùng bình thường mà không cần cấp thêm ACL
Ưu Tiên: CRITICAL - Phải fix trước tiên
Timeline: 1-2 tuần
```

**Bước 2: Phân Tích Tác Động**

```
Phạm Vi:
- Kiểm tra các module khác (0100, 0210, v.v.) có dùng group OPS/HRBP không
- Kiểm tra các model cơ bản có cấp quyền nào cho base.group_user không (ir.ui.menu, partner, res.users, ...)

Đầu Ra: Danh sách tác động chi tiết
```

**Bước 3: Test Trước Fix**

```
Tạo test dataset:
- 3 user thử với group khác nhau (OPS_OC_S, HR_HRBP_M, HR_ADMIN_M)
- Kiểm tra hiện tại quyền hạn của từng user
- Lập baseline để so sánh sau fix
```

### PHASE 1: Fix ACL Survey (Tuần 2)

**Bước 4: Thay Đổi security/ir.model.access.csv**

**Xóa/Sửa Dòng:**

```
Xóa:
- Dòng 2: access_mail_activity_internal_user (0/0/0/0)
- Dòng 3: access_approval_request_internal_user (0/0/0/0)
- Dòng 4: access_hr_employee_internal_user (1/1/0/0) → Đổi thành (1/0/0/0) read-only
- Dòng 13: access_hr_contract_type_internal_user (1/1/0/0) → Đổi thành (1/0/0/0) read-only

Sửa:
- Dòng 5-12 (survey): Thay vì cấp toàn bộ, chỉ cấp read-only (1/0/0/0)
  Lý do: Dùng record rule để giới hạn scope, không cần create/write ở ACL
```

**Cụ Thể:**

```csv
# Trước:
access_survey_survey_internal_user,access_survey_survey,model_survey_survey,base.group_user,1,0,0,0
access_survey_question_internal_user,access_survey_question,model_survey_question,base.group_user,1,1,0,0
access_survey_question_answer_internal_user,access_survey_question_answer,model_survey_question_answer,base.group_user,1,1,0,0
access_survey_user_input_internal_user,access_survey_user_input,model_survey_user_input,base.group_user,1,1,1,1

# Sau:
access_survey_survey_internal_user,access_survey_survey,model_survey_survey,base.group_user,1,0,0,0
access_survey_question_internal_user,access_survey_question,model_survey_question,base.group_user,1,0,0,0  ← Chỉ read
access_survey_question_answer_internal_user,access_survey_question_answer,model_survey_question_answer,base.group_user,1,0,0,0  ← Chỉ read
access_survey_user_input_internal_user,access_survey_user_input,model_survey_user_input,base.group_user,1,0,0,0  ← Chỉ read
```

**Bước 5: Thêm Record Rule Để Cho Phép Create/Write Offboarding Survey**

**Tệp:** security/security.xml

```xml
<!-- Cho phép HR create/write survey.user_input CHỈ cho exit interview survey -->
<record id="rule_psm_0213_survey_user_input_internal_write" model="ir.rule">
    <field name="name">Survey User Input: internal user write exit interview</field>
    <field name="model_id" ref="survey.model_survey_user_input"/>
    <field name="groups" eval="[(4, ref('group_gdh_rst_hr_admin_m')),
                                (4, ref('group_gdh_rst_hr_hrbp_m')),
                                (4, ref('group_gdh_rst_hr_admin_s')),
                                (4, ref('group_gdh_rst_system_st_m'))]"/>
    <field name="perm_read" eval="1"/>
    <field name="perm_write" eval="1"/>
    <field name="perm_create" eval="1"/>
    <field name="perm_unlink" eval="0"/>
    <field name="domain_force">[('survey_id.x_psm_0213_is_exit_survey', '=', True)]</field>
</record>

<!-- Portal chỉ có thể create/write CHỈ survey của mình và CHỈ exit interview -->
<record id="rule_psm_0213_survey_user_input_portal_write" model="ir.rule">
    <field name="name">Survey User Input: portal write exit interview own</field>
    <field name="model_id" ref="survey.model_survey_user_input"/>
    <field name="groups" eval="[(4, ref('base.group_portal'))]"/>
    <field name="perm_write" eval="1"/>
    <field name="perm_create" eval="1"/>
    <field name="domain_force">[
        ('survey_id.x_psm_0213_is_exit_survey', '=', True),
        ('|'),
        ('partner_id', '=', user.partner_id.id),
        ('email', '=', user.email)
    ]</field>
</record>
```

**Bước 6: Test Survey ACL**

```
Test Case:
- group_user: chỉ thấy, không create/write survey → PASS
- group_hr_admin_m: thấy và tạo user_input cho exit interview → PASS
- group_portal: tạo user_input CHỈ cho exit interview, CHỈ của mình → PASS
- group_portal: KHÔNG tạo được user_input cho survey khác → PASS
```

### PHASE 2: Fix ACL hr.employee Và Dữ Liệu Hệ Thống (Tuần 2)

**Bước 7: Đổi ACL hr.employee Thành Read-Only**

```csv
# Trước:
access_hr_employee_internal_user,access_hr_employee,model_hr_employee,base.group_user,1,1,0,0

# Sau:
access_hr_employee_internal_user,access_hr_employee,model_hr_employee,base.group_user,1,0,0,0
```

**Bước 8: Cấp Write Quyền Cho HR Admin**

```csv
# Thêm:
access_hr_employee_hr_admin,access_hr_employee,model_hr_employee,group_gdh_rst_hr_admin_m,1,1,0,0
access_hr_employee_hr_hrbp,access_hr_employee,model_hr_employee,group_gdh_rst_hr_hrbp_m,1,1,0,0
```

**Bước 9: Test hr.employee ACL**

```
Test Case:
- group_user: chỉ thấy employee → PASS
- group_hr_admin_m: thấy và sửa employee → PASS
- group_ops_oc_s: chỉ thấy employee → PASS
```

### PHASE 3: Fix Cron Job (Tuần 2)

**Bước 10: Thêm sudo() Vào Cron**

**Tệp:** models/resignation_request.py

```python
def _cron_send_offboarding_reminders(self):
    # Thêm .sudo() để cron chạy với quyền admin
    offboarding_requests = self.sudo().search([
        ('request_status', '=', 'pending'),
        ('category_id.x_psm_0213_is_offboarding', '=', True)
    ])
    # ...
```

### PHASE 4: Standardize Rule Naming (Tuần 2)

**Bước 11: Đổi Tên Rule security.xml**

**Từ:**
```xml
<record id="rule_psm_0213_survey_internal_read" model="ir.rule">
<record id="rule_psm_0213_survey_question_internal_read" model="ir.rule">
<record id="rule_psm_0213_survey_question_answer_internal_read" model="ir.rule">
<record id="rule_psm_0213_survey_user_input_portal_own" model="ir.rule">
<record id="rule_psm_0213_survey_user_input_internal_results_read" model="ir.rule">
```

**Thành:**
```xml
<record id="rule_0213_survey_internal_read" model="ir.rule">
<record id="rule_0213_survey_question_internal_read" model="ir.rule">
<record id="rule_0213_survey_question_answer_internal_read" model="ir.rule">
<record id="rule_0213_survey_user_input_portal_own" model="ir.rule">
<record id="rule_0213_survey_user_input_internal_results_read" model="ir.rule">
```

**Cập Nhật:** Tất cả `ref()` trong file .xml hoặc .py dùng rule này

### PHASE 5: Protect Field x_psm_0213_is_offboarding (Tuần 3)

**Bước 12: Thêm Constrains**

**Tệp:** models/resignation_request.py

```python
class ApprovalCategory(models.Model):
    _inherit = 'approval.category'
    
    x_psm_0213_is_offboarding = fields.Boolean(default=False)
    
    @api.constrains('x_psm_0213_is_offboarding')
    def _check_offboarding_flag_write_access(self):
        """Chỉ admin/system mới được thay đổi flag offboarding"""
        for record in self:
            if record.id and record.x_psm_0213_is_offboarding != record._get_stored_value():
                if not self.env.user.has_group('base.group_system'):
                    if not self.env.user.has_group('approvals.group_approval_manager'):
                        raise ValidationError(
                            "Bạn không có quyền thay đổi cấu hình Offboarding"
                        )
```

**Hoặc: Cấp Write Quyền Cho Field**

```python
x_psm_0213_is_offboarding = fields.Boolean(
    default=False,
    groups='approvals.group_approval_manager,base.group_system'  ← Thêm này
)
```

### PHASE 6: Documentation & Audit Trail (Tuần 3)

**Bước 13: Cập Nhật Convention**

**Tệp:** addons/M02_P0213/convention/QUY_UOC_DAT_TEN_VA_RULE.md

```markdown
Thêm Section:

## ACL & Record Rule Standards

1. **Naming Convention:**
   - Rule: `rule_0213_<model>_<action>_<scope>`
   - Ví dụ: `rule_0213_approval_request_ops_read`

2. **Scope Limiting:**
   - Dùng field custom `x_psm_0213_*` để giới hạn scope
   - Không cấp quyền rộng rãi cho base.group_user

3. **Implied IDs Dependency:**
   - Module 0213 phụ thuộc vào module 0200 fix implied_ids
   - GDH_RST_OPS_*, GDH_RST_HR_HRBP_* PHẢI implied base.group_user

4. **Protected Fields:**
   - x_psm_0213_is_offboarding: chỉ admin/system write
   - x_psm_0213_is_offboarding_activity: compute, không write trực tiếp

5. **Portal vs Internal:**
   - Portal: tạo/sửa CHỈ dữ liệu của mình (partner_id hoặc email match)
   - Internal: cấp quyền rõ ràng theo group chuyên môn
```

**Bước 14: Tạo Audit Report**

**Tệp:** addons/M02_P0213/AUDIT_TRAIL_2026_05.txt

```
Module M02_P0213 - ACL Audit Fixes
Date: 2026-05-14
Reviewer: Senior Odoo Security Architect

FIXES APPLIED:
1. security/ir.model.access.csv
   - Removed: lines with 0/0/0/0
   - Changed: hr.employee, survey.* to read-only for base.group_user
   - Added: HR admin write ACL

2. security/security.xml
   - Added: rule_0213_survey_user_input_internal_write
   - Added: rule_0213_survey_user_input_portal_write
   - Renamed: rule_psm_0213_* to rule_0213_*

3. models/resignation_request.py
   - Added: @constrains on x_psm_0213_is_offboarding
   - Added: sudo() in _cron_send_offboarding_reminders

4. Convention
   - Updated: QUY_UOC_DAT_TEN_VA_RULE.md with ACL standards

TESTING RESULTS:
- [To be filled after testing]

ISSUES RESOLVED:
- [To be filled after verification]
```

### PHASE 7: Test & UAT (Tuần 4)

**Bước 15: Full Test Matrix (Xem mục "Ma Trận Test" bên dưới)**

---

## Ma Trận Test

### Test Environment Setup

```
User 1: OPS_OC_S (Operation Center Supervisor)
- Groups: GDH_RST_OPS_OC_S, base.group_user (sau fix 0200)
- Department: Operation Center

User 2: HR_HRBP_M (HR HRBP Manager)
- Groups: GDH_RST_HR_HRBP_M, base.group_user (sau fix 0200)
- Department: HR

User 3: HR_ADMIN_M (HR Admin Manager)
- Groups: GDH_RST_HR_ADMIN_M, base.group_user
- Department: HR

User 4: PORTAL (Khách hàng/Ứng viên)
- Groups: base.group_portal
- Partner: External Company

User 5: SYSTEM (Admin)
- Groups: base.group_system
```

### Test Cases

| STT | Feature | User | Expected | Status |
|-----|---------|------|----------|--------|
| 1.1 | Xem approval.request offboarding | OPS_OC_S | ✅ READ | TBD |
| 1.2 | Sửa approval.request offboarding | OPS_OC_S | ❌ DENY | TBD |
| 1.3 | Xem approval.request khác | OPS_OC_S | ❌ DENY (rule limit) | TBD |
| 2.1 | Xem hr.employee | OPS_OC_S | ✅ READ | TBD |
| 2.2 | Sửa hr.employee | OPS_OC_S | ❌ DENY | TBD |
| 3.1 | Xem hr.employee | HR_ADMIN_M | ✅ READ | TBD |
| 3.2 | Sửa hr.employee | HR_ADMIN_M | ✅ WRITE | TBD |
| 4.1 | Tạo survey.user_input cho exit interview | HR_HRBP_M | ✅ CREATE | TBD |
| 4.2 | Tạo survey.user_input cho survey khác | HR_HRBP_M | ❌ DENY (rule limit) | TBD |
| 5.1 | Tạo survey.user_input (của mình) | PORTAL | ✅ CREATE | TBD |
| 5.2 | Sửa survey.user_input (của người khác) | PORTAL | ❌ DENY (rule limit) | TBD |
| 6.1 | Xem exit interview results | HR_ADMIN_M | ✅ READ | TBD |
| 6.2 | Xem exit interview results | OPS_OC_S | ❌ DENY | TBD |
| 7.1 | Approve offboarding request | HR_HRBP_M | ✅ Approve | TBD |
| 7.2 | Deactivate employee | HR_HRBP_M | ✅ Deactivate | TBD |
| 8.1 | Browse menu | OPS_OC_S | ✅ Browse (sau fix 0200) | TBD |
| 8.2 | Access portal form | PORTAL | ✅ Submit form | TBD |
| 9.1 | Run offboarding cron | SYSTEM | ✅ Send reminders | TBD |
| 9.2 | Run offboarding cron | (OPS_OC_S) | ✅ Send reminders (sudo) | TBD |

### Acceptance Criteria

✅ **PASS:** Test case hoạt động như expected
❌ **FAIL:** Test case không như expected, cần fix
🟡 **DEPENDENT:** Phụ thuộc vào fix module 0200

---

## Kết Luận Và Khuyến Cáo

### Tóm Tắt Phát Hiện

Module M02_P0213 hiện có **11 vấn đề** liên quan đến phân quyền:

- **4 vấn đề CRITICAL:** ACL survey mở rộng, ACL portal, hr.employee write, implied IDs chain
- **4 vấn đề HIGH:** No-op ACL, contract.type write, field protection, cron sudo
- **3 vấn đề MEDIUM-LOW:** Naming inconsistency, UTF-8 comment, portal ACL

### Khuyến Cáo Hành Động

**🔴 CRITICAL - Phải Fix Ngay:**

1. **Fix Module 0200 Implied IDs** (Ưu tiên 1)
   - Timeline: 1-2 tuần
   - Owner: Module 0200 maintainer
   - Tác động: Ảnh hưởng đến tất cả module dùng group OPS/HRBP

2. **Giới Hạn Survey ACL** (Ưu tiên 2)
   - Timeline: 3-5 ngày
   - Owner: M02_P0213 maintainer
   - Tác động: Bảo vệ toàn bộ survey system

3. **Sửa hr.employee ACL** (Ưu tiên 3)
   - Timeline: 1-2 ngày
   - Owner: M02_P0213 maintainer
   - Tác động: Bảo vệ dữ liệu nhân sự

**🟠 HIGH - Nên Fix Trong Tuần:**

4. Xóa ACL 0/0/0/0 không cần thiết
5. Fix cron job dùng sudo()
6. Standardize rule naming

**🟡 MEDIUM - Fix Khi Có Thời Gian:**

7. Protect field x_psm_0213_is_offboarding
8. Fix UTF-8 comment tiếng Việt

### Timeline Tổng Thể

```
Tuần 1: Fix module 0200 (chặn) + Chuẩn bị test
Tuần 2: Fix ACL survey, hr.employee, cron, naming (parallel)
Tuần 3: Protect field, documentation
Tuần 4: Full UAT & validation

Tổng: 4 tuần (nếu 0200 fix trong 2 tuần)
```

### Rủi Ro Nếu Không Fix

| Vấn Đề | Rủi Ro | Mức Độ |
|--------|--------|--------|
| Survey ACL | Spam, data abuse, ảnh hưởng survey khác | **CRITICAL** |
| hr.employee write | Nhân viên modify dữ liệu của nhau | **CRITICAL** |
| Implied IDs | User OPS không dùng được hệ thống | **CRITICAL** |
| Cron fail | Offboarding reminder không gửi | **HIGH** |
| Field unprotected | Bypass record rule | **MEDIUM** |
| Portal unscoped | Portal abuse survey | **HIGH** |

### Kết Luận Cuối Cùng

**Câu Hỏi:** Có nên sửa không?

**Câu Trả Lời:** **CÓ - MỨC ƯU TIÊN CRITICAL**

Module 0213 hiện có nhiều lỗ hổng phân quyền có thể:
- ✗ Để nhân viên sửa dữ liệu của nhân viên khác
- ✗ Để portal spam toàn bộ survey system
- ✗ Để user không thể dùng hệ thống (implied IDs)

**Khuyến cáo triển khai Plan 7 phase** trong 4 tuần để:
- ✅ Đạt tiêu chuẩn bảo mật
- ✅ Tuân thủ nguyên tắc least privilege
- ✅ Tránh rủi ro ảnh hưởng đến module khác

---

## Phụ Lục: Danh Sách File Cần Sửa

### File Chính

1. **security/ir.model.access.csv** (5 thay đổi)
2. **security/security.xml** (2 thêm rule, 5 rename rule)
3. **security/offboarding_request_rules.xml** (0 thay đổi, chỉ reference)
4. **models/resignation_request.py** (3 thay đổi)
5. **convention/QUY_UOC_DAT_TEN_VA_RULE.md** (thêm section)

### File Tham Khảo

- Module 0200 security/security.xml (cần fix implied_ids)
- Odoo 19 Approvals Module (tham khảo access control pattern)

---

**Báo Cáo Kết Thúc**

*Ngày: 2026-05-14*  
*Người Rà Soát: Senior Odoo Security Architect*  
*Trạng Thái: Hoàn Tất - Sẵn Sàng Triển Khai*
