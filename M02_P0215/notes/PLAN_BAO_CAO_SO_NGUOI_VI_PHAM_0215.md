# PLAN TRIỂN KHAI: "BÁO CÁO SỐ NGƯỜI VI PHẠM" — MODULE M02_P0215

**Trạng thái:** Chỉ lập plan — KHÔNG sửa code  
**Ngày lập:** 2026-05-16  
**Người lập:** Senior Odoo Functional-Technical Analyst  

---

## 1. PHẠM VI PLAN

- **Module:** M02_P0215_EMPLOYEE_DISCIPLINARY_PROCESS (version 19.0.1.0.3)
- **Chức năng cần lập plan:** Thêm 1 menu báo cáo cho phép chọn khoảng thời gian và thống kê "số người vi phạm" (số nhân viên bị lập hồ sơ kỷ luật) trong kỳ.
- **Convention đã dùng:** `addons/M02_P0215/convention/QUY_UOC_DAT_TEN_VA_RULE.md`
  - Model mới: `x_psm_<tên_model>` → `x_psm.hr.discipline.<...>`
  - Field model mới: `x_psm_<tenfield>`
  - Action mới: `action_psm_<tenaction>`
  - View mới: `view_psm_<tenview>`
  - Rule: ưu tiên dùng cái sẵn có; phân quyền tối thiểu; tách bạch module.
- **JSON map đã dùng:** `addons/M02_P0215/structure/module_map.json`, `module_map_stats.json`
  - Lưu ý: Khi map khác source code → **ƯU TIÊN SOURCE CODE** (đã đối chiếu trực tiếp).
- **Source đã xác nhận (đọc trực tiếp):**
  - `__manifest__.py`
  - `models/x_psm_hr_discipline_record.py`
  - `views/x_psm_hr_discipline_record_views.xml`
  - `views/x_psm_hr_discipline_master_views.xml`
  - `wizards/x_psm_hr_discipline_reject_wizard.py` và `_views.xml` (tham khảo pattern)
  - `security/ir.model.access.csv`, `security_rules.xml`

---

## 2. HIỆN TRẠNG XÁC NHẬN

### Report hiện có
- Chỉ có report **QWeb PDF in theo TỪNG hồ sơ** (`reports/x_psm_discipline_reports.xml`):
  - "Quyết định xử lý kỷ luật"
  - "Quyết định bồi thường"
- **KHÔNG** có báo cáo thống kê tổng hợp nào.

### Menu hiện có
Từ `views/x_psm_hr_discipline_master_views.xml`:
- `menu_psm_hr_discipline_root` → "Discipline" (root, sequence 10)
- `menu_psm_hr_discipline_record_main` → "Records" (seq 1, parent = root)
- `menu_psm_hr_discipline_configuration` → "Configuration" (seq 100, parent = root, groups = hr.group_hr_manager)
  - 3 menu con master data dưới Configuration.
- **Chưa có menu báo cáo nào.**

### Search/filter hiện có
Từ `view_psm_hr_discipline_record_search`:
- **Field tìm:** name, x_psm_employee_id, x_psm_violation_type
- **Filter:** My Records, Chờ RGM Xem xét, Đang Xác minh, Đang Hiệu lực, Store/Company Level
- **Group by:** Employee, State, Violation Category
- **KHÔNG có filter khoảng thời gian (date range)** phục vụ báo cáo.

### Model dữ liệu chính
- **`x_psm.hr.discipline.record`** (`models/x_psm_hr_discipline_record.py`)
  - `_description = "Discipline Record"`
  - `_order = "x_psm_date desc, id desc"`
  - Đây là **model hồ sơ kỷ luật chính** → nguồn dữ liệu duy nhất cho báo cáo.

### Field ngày khả dụng trên record
- **`x_psm_date` (Date)** — "Ngày thực hiện"
  - `required=True`, `default=fields.Date.context_today`
  - **Là field ngày nghiệp vụ chuẩn, luôn có giá trị** → **DÙNG TRƯỜNG NÀY**
- `x_psm_issued_date` (Date) — Ngày ban hành quyết định
  - Chỉ có khi tới bước "issued" → nhiều hồ sơ sẽ rỗng → KHÔNG dùng
- `x_psm_start_date`, `x_psm_end_date` — ngày hiệu lực quyết định (rỗng sớm)
- Các signature date, explanation_date, response_date — chuyên dùng cho bước cụ thể

### Field nhân viên khả dụng
- **`x_psm_employee_id` (Many2one hr.employee)** — "Employee"
  - `required=True`
  - Là nhân viên bị kỷ luật/vi phạm
  - **DÙNG TRƯỜNG NÀY ĐỂ ĐẾM UNIQUE NGƯỜI VI PHẠM** (qua `read_group`)
- `x_psm_company_rep_id` — đại diện công ty (KHÔNG dùng để đếm)
- `x_psm_witness_id` — người làm chứng (KHÔNG dùng để đếm)

### Field state hiện có
```
state (Selection):
draft, under_review, level_determination, investigation, hearing,
proposal, issued, approval, notified, active, expired, cancel
```

### Security hiện có liên quan
**Groups dùng chung từ module M02_P0200:**
- `M02_P0200.GDH_OPS_STORE_SM_M` (SM — quản lý cửa hàng)
- `M02_P0200.GDH_OPS_STORE_RGM_M` (RGM)
- `M02_P0200.GDH_RST_HR_HRBP_S` (HRBP)
- `M02_P0200.GDH_RST_OPS_OC_S` (OC)
- `hr.group_hr_manager` (HR Manager — Odoo gốc)

**Access hiện tại (`ir.model.access.csv`):**
- Mỗi model có dòng access/nhóm; wizard hiện có đều khai báo access theo nhóm.

**Record rules (`security_rules.xml`):**
- `ir.rule` trên `x_psm.hr.discipline.record` giới hạn phạm vi xem theo SM/RGM/HRBP/OC/portal.
- **KHÔNG có rule trên transient model.**
- ⚠️ **Báo cáo phải tôn trọng các ir.rule này** → Dữ liệu tự giới hạn theo quyền user (không `sudo()`).

---

## 3. THIẾT KẾ ĐỀ XUẤT

### Tên chức năng
**"Báo cáo số người vi phạm"** (menu hiển thị tiếng Việt, đồng bộ với các label tiếng Việt khác trong module).

### Hướng triển khai (chốt)
- Tạo **1 wizard transient** mở từ menu mới.
- Wizard cho **nhập khoảng thời gian**, tính **trực tiếp** bằng `read_group`/`search_count` trên model hồ sơ kỷ luật hiện có.
- **KHÔNG** tạo model gốc mới, **KHÔNG** thêm field vào record, **KHÔNG** PDF, **KHÔNG** `sudo()`.
- Báo cáo tự động bị **giới hạn theo ir.rule của user** (đúng nguyên tắc minimum permission, không phá phân quyền).

### Menu/action
- **Menu mới:** `menu_psm_hr_discipline_violation_report`
  - parent = `menu_psm_hr_discipline_root` (cùng cấp Records / Configuration)
  - sequence = 50 (nằm giữa Records=1 và Configuration=100)
  - ⚠️ KHÔNG đặt dưới "Records" (Records là act_window hồ sơ) và KHÔNG dưới "Configuration" (chỉ hr.group_hr_manager, là master data).
  - groups = `"M02_P0200.GDH_OPS_STORE_SM_M,M02_P0200.GDH_OPS_STORE_RGM_M,M02_P0200.GDH_RST_HR_HRBP_S,M02_P0200.GDH_RST_OPS_OC_S,hr.group_hr_manager"`

- **Action mới:** `action_psm_hr_discipline_violation_report`
  - `ir.actions.act_window`, `res_model` = wizard, `view_mode` = form, `target` = new

- **Drill-down:** nút trong wizard trả về 1 `ir.actions.act_window` dict động trỏ tới `x_psm.hr.discipline.record` (KHÔNG cần tạo thêm record action XML).

### Wizard/transient model
- **_name** = `x_psm.hr.discipline.violation.report.wizard`
- **_description** = "Violation Headcount Report Wizard"
- **File:** `wizards/x_psm_hr_discipline_violation_report_wizard.py`
- **Kế thừa:** `models.TransientModel`

### Input fields
Theo convention `x_psm_<tenfield>`:
- **`x_psm_date_from`** (Date, `required=True`)
  - Default = ngày đầu tháng hiện tại (hoặc ngày đầu tháng context)
- **`x_psm_date_to`** (Date, `required=True`)
  - Default = `fields.Date.context_today()`
- **`x_psm_state_filter`** (Selection, KHÔNG bắt buộc)
  - Tùy chọn lọc 1 trạng thái cụ thể; để trống = tất cả trạng thái (trừ 'cancel' nếu `x_psm_include_cancelled=False`)
- **`x_psm_include_cancelled`** (Boolean, default=False)
  - Mặc định loại hồ sơ state='cancel' khỏi thống kê

### Output/result
Readonly, compute:
- **`x_psm_employee_count`** (Integer, readonly, compute)
  - **SỐ NGƯỜI VI PHẠM** = số nhân viên duy nhất trong kỳ (số nhóm khi `read_group` theo `x_psm_employee_id`)
- **`x_psm_record_count`** (Integer, readonly, compute)
  - **TỔNG SỐ HỒ SƠ** vi phạm trong kỳ (result của `search_count` theo domain)

**Tính toán:** bằng `@api.depends` trên các input → kết quả cập nhật trực tiếp UI.

### Có cần transient line model không
**KHÔNG.**
- `read_group` đã đủ đếm unique + tổng hồ sơ.
- Tạo thêm transient line model vi phạm nguyên tắc "ưu tiên dùng cái sẵn có" → thêm complexity + access.
- Nếu sau này cần **BẢNG nhân viên + số lần vi phạm**, dùng **drill-down list group-by** (Phương án C) thay vì line model.

### Có cần PDF không
**KHÔNG.** Nghiệp vụ chỉ yêu cầu thống kê backend. (Constraint cấm tạo PDF không cần thiết.)

### Có cần filter state không
**CÓ** — ở mức tối thiểu:
- **Mặc định LOẠI state='cancel'** (hồ sơ đã hủy không tính là "người vi phạm")
- Các state còn lại (draft...expired) **MẶC ĐỊNH ĐƯỢC TÍNH** vì đều phản ánh 1 sự việc vi phạm đã được ghi nhận
- `x_psm_state_filter` cho phép người dùng **thu hẹp khi cần** (ví dụ chỉ xem state='active')

---

## 4. SO SÁNH PHƯƠNG ÁN HIỂN THỊ KẾT QUẢ

### PHƯƠNG ÁN A — Wizard form + result fields readonly ✅ CHỌN
- **Mô tả:** Wizard có date_from/date_to + 2 ô số readonly (số người vi phạm, tổng hồ sơ), tính bằng `read_group`/`search_count`.
- **Ưu điểm:**
  - Nhỏ gọn nhất; không model phụ; không field record mới
  - Trả lời trực tiếp đúng câu hỏi "số người vi phạm"
  - Cập nhật trực tiếp khi user chọn ngày
- **Nhược điểm:** Chỉ ra con số tổng, không xem được chi tiết từng nhân viên.
- **File cần tạo/sửa:**
  - TẠO: `wizards/x_psm_hr_discipline_violation_report_wizard.py`
  - SỬA: `wizards/__init__.py`, `security/ir.model.access.csv`, `__manifest__.py`
  - TẠO: `views/x_psm_hr_discipline_violation_report_wizard_views.xml`
- **Đánh giá phù hợp:** ⭐⭐⭐⭐⭐ RẤT phù hợp với yêu cầu cốt lõi.

### PHƯƠNG ÁN B — Wizard + transient line model ❌ LOẠI
- **Mô tả:** Thêm model dòng `x_psm.hr.discipline.violation.report.line`, fill bằng `read_group`, hiển thị one2many trong wizard.
- **Ưu điểm:** Thấy danh sách nhân viên và số lần vi phạm ngay trong wizard.
- **Nhược điểm:**
  - Phát sinh thêm 1 model + thêm dòng access
  - Phải fill/clear dòng thủ công
  - Phức tạp hơn; vi phạm "hạn chế tạo model mới"
- **File cần tạo/sửa:** 2 model .py + view + 2 nhóm access
- **Đánh giá phù hợp:** ❌ Dư thừa so với yêu cầu. KHÔNG khuyến nghị.

### PHƯƠNG ÁN C — Action mở list view hồ sơ đã filter + group by employee ✅ DRILL-DOWN
- **Mô tả:** Mở thẳng `x_psm.hr.discipline.record` với domain khoảng ngày + context `group_by=x_psm_employee_id`; đếm người = đếm số nhóm.
- **Ưu điểm:**
  - Tái dụng 100% list view + access + ir.rule sẵn có
  - 0 model mới
- **Nhược điểm:**
  - Nếu mở thẳng từ menu không có form chọn ngày tương tác
  - Không hiển thị con số "số người vi phạm" thành 1 ô rõ ràng
- **File cần tạo/sửa:** Tối thiểu (1 action dict trong wizard).
- **Đánh giá phù hợp:** ✅ Tốt cho DRILL-DOWN. Dùng làm nút "Xem danh sách hồ sơ" trong wizard Phương án A.

### KẾT LUẬN
🎯 **Chọn PHƯƠNG ÁN A làm chính, TÍCH HỢP PHƯƠNG ÁN C làm drill-down.**
- Wizard (A) trả lời trực tiếp con số "số người vi phạm" + "tổng hồ sơ"
- Thêm nút "Xem danh sách hồ sơ" trong wizard → trả về `ir.actions.act_window` dict (C)
- Mở list hồ sơ đã filter theo kỳ + group by employee để xem chi tiết
- Loại Phương án B vì tạo model thừa, trái convention "dùng cái sẵn có"

---

## 5. PLAN TRIỂN KHAI CHO CODEX

### PHASE 1 — Xác nhận field/model/security & chốt thiết kế

**Mục tiêu:** Khóa quyết định kỹ thuật trước khi code.

**File cần tạo/sửa:** Không (chỉ rà soát).

**Nội dung cần làm:**
- Xác nhận lại:
  - model nguồn = `x_psm.hr.discipline.record`
  - field ngày = `x_psm_date`
  - field nhân viên = `x_psm_employee_id`
  - state loại trừ mặc định = 'cancel'
- Chốt danh sách nhóm được xem báo cáo (xem bảng quyết định Phase 4)
- **Bảng quyết định danh sách nhóm:**
  ```
  ✅ GDH_OPS_STORE_SM_M (SM — quản lý cửa hàng)
  ✅ GDH_OPS_STORE_RGM_M (RGM)
  ✅ GDH_RST_HR_HRBP_S (HRBP)
  ✅ GDH_RST_OPS_OC_S (OC)
  ✅ hr.group_hr_manager (HR Manager)
  ```
  Lưu ý: SM xem được báo cáo, NHƯNG số liệu của SM vẫn tự giới hạn theo ir.rule phạm vi cửa hàng.

**Quy tắc convention cần tuân thủ:** Đối chiếu source > JSON map.

**Rủi ro:** Hiểu sai "ngày" → chọn nhầm `x_psm_issued_date` → nhiều hồ sơ bị bỏ sót. Phải dùng `x_psm_date`.

**Cách kiểm tra:** Đọc lại model file, xác nhận field tồn tại + required.

**Điều kiện hoàn thành:** Bảng quyết định kỹ thuật được chốt.

---

### PHASE 2 — Tạo wizard model + validation + logic thống kê

**Mục tiêu:** Có model transient tính đúng số liệu.

**File cần tạo/sửa:**
- **TẠO:** `wizards/x_psm_hr_discipline_violation_report_wizard.py`
- **SỬA:** `wizards/__init__.py` (thêm import dòng mới, KHÔNG xóa import cũ)

**Nội dung cần làm:**
```python
class HrDisciplineViolationReportWizard(models.TransientModel):
    _name = "x_psm.hr.discipline.violation.report.wizard"
    _description = "Violation Headcount Report Wizard"
    
    # INPUT FIELDS
    x_psm_date_from = fields.Date(required=True, default=<ngày đầu tháng>)
    x_psm_date_to = fields.Date(required=True, default=fields.Date.context_today)
    x_psm_state_filter = fields.Selection([...], default=False)
    x_psm_include_cancelled = fields.Boolean(default=False)
    
    # OUTPUT FIELDS (readonly, compute)
    x_psm_employee_count = fields.Integer(compute='_compute_x_psm_counts', readonly=True)
    x_psm_record_count = fields.Integer(compute='_compute_x_psm_counts', readonly=True)
    
    # HELPER METHOD — Build domain
    def _x_psm_get_domain(self):
        domain = [
            ('x_psm_date', '>=', self.x_psm_date_from),
            ('x_psm_date', '<=', self.x_psm_date_to),
        ]
        if not self.x_psm_include_cancelled:
            domain.append(('state', '!=', 'cancel'))
        if self.x_psm_state_filter:
            domain.append(('state', '=', self.x_psm_state_filter))
        return domain
    
    # COMPUTE — Tính số liệu
    @api.depends('x_psm_date_from', 'x_psm_date_to', 'x_psm_state_filter', 'x_psm_include_cancelled')
    def _compute_x_psm_counts(self):
        for rec in self:
            domain = rec._x_psm_get_domain()
            # Tổng hồ sơ
            rec.x_psm_record_count = self.env['x_psm.hr.discipline.record'].search_count(domain)
            # Số người vi phạm (duy nhất) — read_group theo employee_id
            groups = self.env['x_psm.hr.discipline.record'].read_group(
                domain, ['id'], ['x_psm_employee_id'], limit=None
            )
            rec.x_psm_employee_count = len([g for g in groups if g['x_psm_employee_id']])
    
    # VALIDATION — Kiểm tra ngày hợp lệ
    @api.constrains('x_psm_date_from', 'x_psm_date_to')
    def _check_dates(self):
        for rec in self:
            if rec.x_psm_date_from > rec.x_psm_date_to:
                raise UserError("Ngày bắt đầu không được lớn hơn ngày kết thúc.")
    
    # ACTION — Drill-down xem danh sách hồ sơ
    def action_psm_view_records(self):
        self.ensure_one()
        domain = self._x_psm_get_domain()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'x_psm.hr.discipline.record',
            'view_mode': 'list,form',
            'domain': domain,
            'context': {'group_by': 'x_psm_employee_id'},
            'name': 'Disciplinary Records - Violation Report',
        }
```

**Quy tắc convention:**
- Field prefix `x_psm_`
- Method action prefix `action_psm_`
- KHÔNG tạo field trên model gốc
- KHÔNG `sudo()`
- `search_count()` và `read_group()` theo quyền user (tự giới hạn ir.rule)

**Rủi ro:**
- `read_group()` signature khác giữa version Odoo → kiểm tra kỹ docs version 19.0
- Lệch biên ngày (>= / <=) → cẩn thận bao phủ đúng ngày biên

**Cách kiểm tra:** Mở shell/odoo, gọi `read_group()` thủ công, đối chiếu con số.

**Điều kiện hoàn thành:** Import OK, KHÔNG lỗi cú pháp Python.

---

### PHASE 3 — Tạo wizard view + action + menu

**Mục tiêu:** Người dùng truy cập được báo cáo qua menu.

**File cần tạo/sửa:**
- **TẠO:** `views/x_psm_hr_discipline_violation_report_wizard_views.xml`

**Nội dung cần làm:**
```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <!-- View Form Wizard -->
    <record id="view_psm_hr_discipline_violation_report_wizard_form" model="ir.ui.view">
        <field name="name">hr.discipline.violation.report.wizard.form</field>
        <field name="model">x_psm.hr.discipline.violation.report.wizard</field>
        <field name="arch" type="xml">
            <form string="Báo cáo số người vi phạm">
                <group string="Lựa chọn khoảng thời gian">
                    <field name="x_psm_date_from"/>
                    <field name="x_psm_date_to"/>
                </group>
                <group string="Bộ lọc tùy chọn">
                    <field name="x_psm_state_filter"/>
                    <field name="x_psm_include_cancelled"/>
                </group>
                <group string="Kết quả" colspan="2">
                    <div class="alert alert-info" role="alert">
                        <strong><field name="x_psm_employee_count" class="fw-bold" style="font-size: 20px;"/></strong> 
                        nhân viên vi phạm | 
                        <strong><field name="x_psm_record_count" class="fw-bold"/></strong> hồ sơ
                    </div>
                </group>
                <footer>
                    <button name="action_psm_view_records" string="Xem danh sách hồ sơ" type="object" class="btn-primary"/>
                    <button string="Đóng" special="cancel" class="btn-secondary"/>
                </footer>
            </form>
        </field>
    </record>

    <!-- Action -->
    <record id="action_psm_hr_discipline_violation_report" model="ir.actions.act_window">
        <field name="name">Báo cáo số người vi phạm</field>
        <field name="res_model">x_psm.hr.discipline.violation.report.wizard</field>
        <field name="view_mode">form</field>
        <field name="target">new</field>
    </record>

    <!-- Menu -->
    <menuitem id="menu_psm_hr_discipline_violation_report" 
              name="Báo cáo số người vi phạm" 
              parent="menu_psm_hr_discipline_root" 
              action="action_psm_hr_discipline_violation_report" 
              sequence="50"
              groups="M02_P0200.GDH_OPS_STORE_SM_M,M02_P0200.GDH_OPS_STORE_RGM_M,M02_P0200.GDH_RST_HR_HRBP_S,M02_P0200.GDH_RST_OPS_OC_S,hr.group_hr_manager"/>
</odoo>
```

**Quy tắc convention:**
- View id: `view_psm_*`
- Action id: `action_psm_*`
- KHÔNG sửa menu/action/view hiện có
- Menu groups phải khớp danh sách nhóm ở Phase 4

**Rủi ro:**
- Trùng id → lỗi load
- Menu hiện ra cho nhóm không có access → lỗi khi click
- groups trên menu PHẢI khớp nhóm trong `access.csv`

**Cách kiểm tra:** Cập nhật module, menu "Báo cáo số người vi phạm" xuất hiện cạnh "Records".

**Điều kiện hoàn thành:** Mở menu → form wizard hiển thị KHÔNG lỗi.

---

### PHASE 4 — Security/access + manifest load order

**Mục tiêu:** Phân quyền tối thiểu, load đúng thứ tự.

**File cần tạo/sửa:**
- **SỬA:** `security/ir.model.access.csv` (THÊM dòng, KHÔNG sửa dòng cũ)
- **SỬA:** `__manifest__.py` (THÊM file view mới vào 'data')

**Nội dung cần làm:**

**Trong `ir.model.access.csv` — THÊM 5 dòng sau (không xóa dòng cũ):**
```csv
access_psm_hr_discipline_violation_report_wizard_sm,hr.discipline.violation.report.wizard.sm,model_x_psm_hr_discipline_violation_report_wizard,M02_P0200.GDH_OPS_STORE_SM_M,1,1,1,0
access_psm_hr_discipline_violation_report_wizard_rgm,hr.discipline.violation.report.wizard.rgm,model_x_psm_hr_discipline_violation_report_wizard,M02_P0200.GDH_OPS_STORE_RGM_M,1,1,1,0
access_psm_hr_discipline_violation_report_wizard_hrbp,hr.discipline.violation.report.wizard.hrbp,model_x_psm_hr_discipline_violation_report_wizard,M02_P0200.GDH_RST_HR_HRBP_S,1,1,1,0
access_psm_hr_discipline_violation_report_wizard_oc,hr.discipline.violation.report.wizard.oc,model_x_psm_hr_discipline_violation_report_wizard,M02_P0200.GDH_RST_OPS_OC_S,1,1,1,0
access_psm_hr_discipline_violation_report_wizard_admin,hr.discipline.violation.report.wizard.admin,model_x_psm_hr_discipline_violation_report_wizard,hr.group_hr_manager,1,1,1,1
```

**Giải thích cột CSV:**
- Col 1: id (tên ID duy nhất)
- Col 2: name (tên hiển thị)
- Col 3: model_id:id (id XML của model)
- Col 4: group_id:id (id của group Odoo)
- Col 5-8: perm_read, perm_write, perm_create, perm_unlink

**Transient model cần:** perm_read=1, perm_write=1, perm_create=1, perm_unlink=0 (form cần create+write để dùng form; không xóa transient)

**Trong `__manifest__.py` — THÊM vào list 'data':**
```python
"views/x_psm_hr_discipline_violation_report_wizard_views.xml",
```
**Vị trí:** Đặt SAU `"views/x_psm_hr_discipline_manual_confirm_wizard_views.xml"` và TRƯỚC `"views/x_psm_portal_templates.xml"` (đồng nhất với cụm wizard hiện có).

**Quy tắc convention:**
- Minimum permission (chỉ đủ dùng form)
- groups menu = groups access
- KHÔNG cần security_rules.xml mới (transient không cần ir.rule)

**Rủi ro:**
- Quên access → user gặp `AccessError`
- Cấp tràn quyền → vi phạm convention
- Sai vị trí trong manifest → view nạp trước khi model sẵn sàng → lỗi XML

**Cách kiểm tra:**
- Terminal shell: `self.env['ir.model.access'].check('x_psm.hr.discipline.violation.report.wizard', 'read')` cho mỗi nhóm
- Đăng nhập từng nhóm thử mở menu

**Điều kiện hoàn thành:** Đúng nhóm (5 nhóm trên) thấy menu & chạy được, nhóm khác không.

---

### PHASE 5 — Test UI / phân quyền / dữ liệu rỗng & ngày sai

**Mục tiêu:** Đảm bảo đúng nghiệp vụ và an toàn.

**File cần tạo/sửa:** Không.

**Nội dung cần làm:** Chạy đủ TEST MATRIX mục 6.

**Quy tắc convention:** KHÔNG sửa code để "ép" test pass.

**Rủi ro:** `read_group()` lệch số khi nhiều company; biên ngày sai.

**Cách kiểm tra:** So số wizard với list group-by-employee thủ công (xem CASE 7 trong TEST MATRIX).

**Điều kiện hoàn thành:** Toàn bộ case trong TEST MATRIX đạt kết quả mong đợi.

---

### PHASE 6 — Regenerate structure map (nếu cần)

**Mục tiêu:** Đồng bộ JSON map với source mới.

**File cần tạo/sửa:**
- `structure/module_map.json`
- `structure/module_map_stats.json`
- `structure/details/*` (tự sinh)

**Nội dung cần làm:** Chạy `structure/build_module_map.py` để cập nhật map.

```bash
cd addons/M02_P0215/structure
python build_module_map.py
```

**Quy tắc convention:** Map phản ánh source, không sửa tay.

**Rủi ro:** Map cũ gây sai lệch ở lần phân tích sau.

**Cách kiểm tra:** Map có entry wizard/view/action mới.

**Điều kiện hoàn thành:** Map khớp source (có entry `x_psm_hr_discipline_violation_report_wizard`, `action_psm_hr_discipline_violation_report`, `view_psm_hr_discipline_violation_report_wizard_form`).

---

## 6. TEST MATRIX

### CASE 1 — Kỳ có dữ liệu, nhiều người

| Thành phần | Giá trị |
|-----------|--------|
| **User/group** | HRBP (GDH_RST_HR_HRBP_S) |
| **Input** | date_from=2026-04-01, date_to=2026-04-30 |
| **Dữ liệu mẫu** | 5 hồ sơ của 3 nhân viên trong tháng 4 (state ≠ cancel) |
| **Kết quả mong đợi** | employee_count=3, record_count=5 |
| **Rủi ro quan sát** | Đếm trùng nhân viên; lệch biên ngày |

### CASE 2 — Một nhân viên vi phạm nhiều lần

| Thành phần | Giá trị |
|-----------|--------|
| **User/group** | HR Manager (hr.group_hr_manager) |
| **Input** | date_from=2026-04-01, date_to=2026-04-30 |
| **Dữ liệu mẫu** | 3 hồ sơ cùng 1 nhân viên |
| **Kết quả mong đợi** | employee_count=1, record_count=3 |
| **Rủi ro** | Nhầm đếm hồ sơ thành đếm người |

### CASE 3 — Loại trừ hồ sơ 'cancel'

| Thành phần | Giá trị |
|-----------|--------|
| **User/group** | HR Manager |
| **Input** | Kỳ có 4 hồ sơ, trong đó 1 hồ sơ state='cancel' |
| **Tùy chọn** | `x_psm_include_cancelled=False` → record_count=3; `=True` → record_count=4 |
| **Rủi ro** | domain state không áp dụng đúng |

### CASE 4 — Lọc theo 1 state cụ thể

| Thành phần | Giá trị |
|-----------|--------|
| **User/group** | HR Manager |
| **Input** | x_psm_state_filter='active' |
| **Kết quả** | Chỉ đếm hồ sơ state='active' trong kỳ |
| **Rủi ro** | state_filter và include_cancelled xung đột logic |

### CASE 5 — Không có dữ liệu

| Thành phần | Giá trị |
|-----------|--------|
| **User/group** | HRBP |
| **Input** | Kỳ tương lai (ví dụ 2026-12-01 đến 2026-12-31) không có hồ sơ |
| **Kết quả** | employee_count=0, record_count=0 (KHÔNG lỗi) |
| **Rủi ro** | read_group trả rỗng → exception |

### CASE 6 — Ngày sai (from > to)

| Thành phần | Giá trị |
|-----------|--------|
| **Input** | date_from=2026-04-30, date_to=2026-04-01 |
| **Kết quả** | UserError chặn, KHÔNG tính |
| **Rủi ro** | constrains không kích hoạt khi compute chạy trước |

### CASE 7 — Phạm vi phân quyền (ir.rule) ⭐ QUAN TRỌNG

| Thành phần | Giá trị |
|-----------|--------|
| **User/group** | SM cửa hàng A vs HRBP công ty |
| **Input** | Cùng kỳ |
| **Kết quả** | SM chỉ đếm hồ sơ trong phạm vi rule SM (phòng ban/cấp dưới); HRBP đếm theo công ty. Số liệu KHÁC nhau là ĐÚNG. |
| **Rủi ro** | Lỡ dùng `sudo()` → rò rỉ số liệu ngoài phạm vi → BUG BẢO MẬT |

### CASE 8 — Nhóm không được cấp quyền

| Thành phần | Giá trị |
|-----------|--------|
| **User/group** | user portal hoặc nhóm ngoài danh sách 5 nhóm |
| **Kết quả** | KHÔNG thấy menu / KHÔNG mở được wizard |
| **Rủi ro** | menu groups không khớp access |

### CASE 9 — Drill-down "Xem danh sách hồ sơ"

| Thành phần | Giá trị |
|-----------|--------|
| **Action** | Bấm nút "Xem danh sách hồ sơ" trong wizard |
| **Kết quả** | Mở list hồ sơ đã filter kỳ, group by employee; số nhóm = employee_count |
| **Rủi ro** | domain drill-down lệch domain compute |

---

## 7. PHÂN TÍCH TÁC ĐỘNG

### Ảnh hưởng đến phân quyền gốc Odoo
✅ **KHÔNG.** Chỉ thêm access cho 1 transient model mới và dùng lại group sẵn có (M02_P0200.* và hr.group_hr_manager). Không sửa group/rule gốc.

### Ảnh hưởng đến module khác
✅ **KHÔNG.** Chỉ đọc `x_psm.hr.discipline.record` của chính module 0215. Dùng group của M02_P0200 ở mức tham chiếu (đã là dependency sẵn có trong manifest) — không sửa M02_P0200.

### Ảnh hưởng đến report PDF hiện có
✅ **KHÔNG.** Không động vào `reports/x_psm_discipline_reports.xml`.

### Ảnh hưởng đến menu/action hiện có
✅ **KHÔNG.** Chỉ THÊM menu/action mới; không sửa Records, Configuration hay search view hiện có.

### Rủi ro bảo mật
✅ **Thấp.**
- **KHÔNG** dùng `sudo()` → báo cáo tự giới hạn theo ir.rule của user.
- ⚠️ **Lưu ý ngược lại:** Nếu Codex lỡ dùng `sudo()` để "đếm cho đủ" sẽ làm **lộ số liệu ngoài phạm vi user** → **CẤM sudo trong wizard này**.

### Rủi ro hiệu năng
✅ **Thấp.**
- Dùng `search_count()` + 1 lệnh `read_group()` (có index trên `x_psm_date` và FK `x_psm_employee_id`)
- Dữ liệu kỷ luật khối lượng nhỏ
- Không vòng lặp Python phức tạp

---

## 8. KẾT LUẬN

### Có nên triển khai không
**✅ CÓ.** Khả thi, nhỏ gọn, ít side effect, đáp ứng đúng yêu cầu.

### Mức ưu tiên
**Trung bình** — Tính năng bổ sung, không chặn workflow hiện tại.

### Phương án khuyến nghị
**Phương án A** (wizard transient + result fields readonly) tích hợp **drill-down Phương án C** (act_window list group-by-employee).
- ❌ KHÔNG model line
- ❌ KHÔNG PDF
- ❌ KHÔNG field mới trên record gốc
- ❌ KHÔNG `sudo()`

### Bước đầu tiên Codex nên thực hiện
**Thực hiện PHASE 1:**
1. Chốt bảng quyết định kỹ thuật (model nguồn, field ngày, field nhân viên, mặc định loại state)
2. Xác nhận danh sách nhóm được cấp quyền: ✅ **5 nhóm** (SM, RGM, HRBP, OC, HR Manager) — đã chốt ở trên

---

## DANH SÁCH NHÓM ĐƯỢC CẤP QUYỀN — LẬP IR.MODEL.ACCESS & GROUPS MENU

```
✅ M02_P0200.GDH_OPS_STORE_SM_M (Quản lý cửa hàng — Store Manager)
✅ M02_P0200.GDH_OPS_STORE_RGM_M (Quản lý vùng — Regional Manager)
✅ M02_P0200.GDH_RST_HR_HRBP_S (Chuyên viên HR — HRBP)
✅ M02_P0200.GDH_RST_OPS_OC_S (Chuyên viên vận hành — Operations Coordinator)
✅ hr.group_hr_manager (Quản lý HR — Odoo gốc)
```

**Lưu ý bảo mật:** SM xem được báo cáo, nhưng số liệu của SM vẫn tự giới hạn theo ir.rule `rule_psm_hr_discipline_record_store_manager` (chỉ phạm vi phòng ban/cấp dưới của SM). KHÔNG dùng `sudo()` → hành vi đúng, không phải lỗi.

---

## THAM CHIẾU NHANH — TÊN ĐỐI TƯỢNG PHẢI TẠO

| Loại | ID XML | Tên Python | File |
|------|--------|------------|------|
| Model Transient | - | `x_psm.hr.discipline.violation.report.wizard` | `wizards/x_psm_hr_discipline_violation_report_wizard.py` |
| View Form | `view_psm_hr_discipline_violation_report_wizard_form` | - | `views/x_psm_hr_discipline_violation_report_wizard_views.xml` |
| Action | `action_psm_hr_discipline_violation_report` | - | `views/x_psm_hr_discipline_violation_report_wizard_views.xml` |
| Menu | `menu_psm_hr_discipline_violation_report` | - | `views/x_psm_hr_discipline_violation_report_wizard_views.xml` |
| Access (5 dòng) | `access_psm_hr_discipline_violation_report_wizard_*` | - | `security/ir.model.access.csv` |

---

**END OF PLAN**  
**Phiên bản:** 1.0  
**Ngày cập nhật cuối:** 2026-05-16  
**Trạng thái:** ✅ Sẵn sàng cho Codex triển khai Phase 1
