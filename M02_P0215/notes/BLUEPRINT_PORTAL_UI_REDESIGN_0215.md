# Technical Blueprint — Portal UI Redesign cho Module M02_P0215

> **Phạm vi**: Cải thiện UI/UX cho khu vực Portal của module `M02_P0215_EMPLOYEE_DISCIPLINARY_PROCESS`, áp dụng palette McDonald's, không thay đổi logic nghiệp vụ, không thay đổi route/controller/model contract.
> **Loại**: Blueprint/Planning. Không sửa code, không tạo file mới, không apply patch.
> **Ngày**: 2026-05-12

---

## 1. Source Analysis Summary

### 1.1. Manifest & Dependencies

Từ `addons/M02_P0215/__manifest__.py`:

- `name = "M02_P0215_EMPLOYEE_DISCIPLINARY_PROCESS"`, `version = "19.0.1"`, `license = "LGPL-3"`, `application = True`.
- `depends`: `base`, `hr`, `mail`, `portal`, `calendar`, `approvals`, `survey`, `portal_custom`, `M02_P0200`.
- `data` list (theo thứ tự load): security CSV → security XML → data XML (approval/survey/mail) → views XML (master/record/wizards) → `views/x_psm_portal_templates.xml` → tiếp tục các data XML khác → reports.
- **Manifest chưa có khoá `"assets"`** — hiện không có CSS/JS frontend được khai báo riêng cho module 0215.
- `static/` chỉ chứa `static/description/consistency.png` — chưa có `static/src/css|scss|js`.

### 1.2. Portal Routes

Từ `addons/M02_P0215/controllers/portal.py` lớp `DisciplinePortal(CustomerPortal)`:

| Route | Method | Hàm | Mục đích |
|---|---|---|---|
| `/my`, `/my/home` | GET | `home` | Override để đảm bảo super chạy |
| `/my/disciplines`, `/my/disciplines/page/<int:page>` | GET | `portal_psm_my_disciplines` | Danh sách hồ sơ kỷ luật + pager + sortby |
| `/my/discipline/create` | GET, POST | `portal_psm_discipline_create` | Manager tạo Counseling Log mới |
| `/my/discipline/<int:x_psm_record_id>` | GET | `portal_discipline_view` | Trang chi tiết hồ sơ + action panel theo vai trò |
| `/my/discipline/submit_section_ii` | POST | `portal_discipline_submit_section_ii` | Legacy fallback: nhân viên ký Section II |
| `/my/discipline/manager_finalize` | POST | `portal_discipline_manager_finalize` | Legacy fallback: manager ký Section III/IV |
| `/my/discipline/rgm_action` | POST | `portal_discipline_rgm_action` | RGM action: no_repeat / set_repeat / store_level / company_level |
| `/my/discipline/respond` | POST | `portal_discipline_respond` | Bước 9: employee accept/reject |

`_prepare_home_portal_values` thêm `discipline_count` vào portal home.

### 1.3. Portal Templates (XML IDs)

Từ `addons/M02_P0215/views/x_psm_portal_templates.xml`:

| Template ID | Loại | Inherit | Mục đích |
|---|---|---|---|
| `portal_psm_discipline_sidebar_link` | inherit | `portal_custom.portal_my_home_inherit` (priority 50) | Thêm sidebar link tới `/my/disciplines` |
| `portal_psm_my_home_menu_discipline` | inherit | `portal.portal_breadcrumbs` (priority 20) | Breadcrumb cho list/detail |
| `portal_psm_my_home_discipline` | inherit | `portal.portal_my_home` (priority 20) | Docs entry trên portal home |
| `portal_psm_my_disciplines` | primary | — | Trang `/my/disciplines` (bảng + pager) |
| `portal_psm_discipline_create` | primary | — | Form `/my/discipline/create` |
| `portal_psm_discipline_explanation_template` | primary | — | Trang `/my/discipline/<id>` (detail + action) |

### 1.4. Input Field Names mà Controller Phụ Thuộc (KHÔNG ĐƯỢC ĐỔI)

Trong POST `/my/discipline/create`:
- `x_psm_employee_id`, `witness_id`, `violation_category`, `x_psm_violation_type`
- `x_psm_discipline_purpose`, `section_i_description`, `section_ii_feedback`
- `section_iii_identification`, `section_iv_agreement`, `x_psm_date`
- `manager_signature`, `employee_signature`, `witness_signature`
- `explanation_images` (multipart), `csrf_token`

Trong POST `/my/discipline/submit_section_ii`:
- `x_psm_record_id`, `section_ii_feedback`, `employee_signature`, `csrf_token`

Trong POST `/my/discipline/manager_finalize`:
- `x_psm_record_id`, `section_iii_identification`, `section_iv_agreement`, `manager_signature`, `csrf_token`

Trong POST `/my/discipline/rgm_action`:
- `x_psm_record_id`, `action_type` (giá trị: `no_repeat`, `set_repeat`, `store_level`, `company_level`), `csrf_token`

Trong POST `/my/discipline/respond`:
- `x_psm_record_id`, `respond` (giá trị: `accept`, `reject`), `note`, `csrf_token`

### 1.5. User Flow (Xác Nhận Từ Controller + Model + Template)

1. **Manager** mở `/my` → click sidebar/docs entry → vào `/my/disciplines`.
2. Manager bấm "Tạo Counseling Log" (chỉ hiển thị khi `is_manager == True`) → mở `/my/discipline/create`.
3. Manager nhập: nhân viên, người làm chứng (optional), violation category/type, mục đích, 4 sections, ảnh giấy tường trình, ký 2-3 chữ ký → POST tạo `record`.
4. Trạng thái record sau create: `under_review` nếu có đủ chữ ký + Section III, ngược lại `draft`.
5. **Employee** vào `/my/disciplines` → click record của mình → vào `/my/discipline/<id>`.
6. Employee phản hồi Section II + ký (legacy form ở `submit_section_ii`).
7. Manager finalize Section III/IV + ký (legacy form ở `manager_finalize`).
8. RGM (manager của employee) nhận trạng thái `under_review` → bấm các action `rgm_action` → đẩy về `level_determination` / `proposal` / `investigation`.
9. Quy trình tiếp tục qua `hearing` → `proposal` → `issued` → `approval` → `notified` (chủ yếu qua backend/survey/approval).
10. Khi `state == 'notified'`, employee thấy CTA accept/reject (form `/my/discipline/respond`).
11. Accept → `active`; reject với note → workflow tương ứng.

### 1.6. State Machine (12 Trạng Thái)

Từ `x_psm_hr_discipline_record.py` dòng 379-398:

```
draft → under_review → level_determination → investigation → hearing
     → proposal → issued → approval → notified → active → expired
     → cancel
```

| State | Label tiếng Việt |
|---|---|
| `draft` | Khởi tạo |
| `under_review` | Đang xem xét |
| `level_determination` | Xác định cấp xử lý |
| `investigation` | Xác minh nâng cao |
| `hearing` | Họp kỷ luật |
| `proposal` | Đề xuất kỷ luật |
| `issued` | Ban hành quyết định |
| `approval` | Phê duyệt |
| `notified` | Thông báo |
| `active` | Đang hiệu lực |
| `expired` | Hết hiệu lực |
| `cancel` | Đã hủy |

### 1.7. Security/Access Liên Quan Portal

Từ `security/ir.model.access.csv` và `security/security_rules.xml`:

- `access_psm_hr_discipline_record_portal` cho `base.group_portal`: `read=1, write=0, create=0, unlink=0`.
- `rule_psm_hr_discipline_record_portal_own`: portal user chỉ thấy record mà `x_psm_employee_id.user_id == user.id` HOẶC `work_email` khớp `user.login/email`.
- Manager (SM/RGM) có rule riêng với scope `parent_id`/`department_id`/`company_rep_id` để write/create.
- **Hệ quả UX**: Portal employee KHÔNG được tạo, không write trực tiếp qua ORM — mọi update phải qua POST controller, đi qua `sudo()`.

### 1.8. Điểm UI/UX Hiện Tại Còn Yếu

1. **Sidebar link**: dùng inline `style="background: #fff3cd; color: #856404;"` (Bootstrap warning yellow nhạt) — chưa đúng palette McDonald's `#FFC72C`.
2. **List page `/my/disciplines`**:
   - Table dùng `o_portal_my_doc_table` mặc định + `table-responsive` → trên mobile scroll ngang, không thân thiện.
   - Status badge dùng Bootstrap màu (`bg-secondary`, `bg-info`, `bg-warning`, `bg-success`, `bg-dark`, `bg-danger`, `bg-primary`) — palette không đồng bộ McDonald's.
   - Cột "Details" hiển thị `x_psm_violation_type` (Char tự nhập) có thể rỗng → hiện trống.
   - Không có cột "Next action" hoặc highlight việc cần làm.
   - Empty state chỉ là `alert-info` thông thường.
3. **Create form `/my/discipline/create`**:
   - Một form rất dài (8+ section). Tất cả đều `required="1"` ngoại trừ witness.
   - Không có progress indicator/section navigation.
   - Nhiều inline style lẫn Bootstrap classes → khó bảo trì.
   - Modal validation đã dùng palette đúng (`#DA291C` + `#FFC72C` + `#FFFFFF`) — giữ nguyên làm anchor.
4. **Detail page `/my/discipline/<id>`**:
   - Header `bg-warning text-dark` đúng tinh thần nhưng status badge `bg-white text-warning` đọc khó (vàng trên trắng → contrast yếu).
   - State chỉ hiện `record.state.upper()` (key kỹ thuật) thay vì label tiếng Việt.
   - Action panel cho RGM **hiện không có UI** dù controller hỗ trợ route `rgm_action` — đây là **gap UX cần điền**.
   - Không có lifecycle/history view rõ ràng.
5. **Validation modal**: bị duplicate giữa 2 template — nên gom về 1 partial `t-call`.
6. **Lỗi chính tả**: "GỬI PHÀN HỒI" → "GỬI PHẢN HỒI" (button `submit_section_ii`).

### 1.9. Rủi Ro Nếu Chỉnh Sai

- Đổi `name` input → controller `post.get("...")` nhận `None` → record thiếu field.
- Đổi template id → `request.render("M02_P0215.portal_psm_my_disciplines", ...)` fail.
- Bỏ `csrf_token` hidden input → form bị reject 403 CSRF.
- Đổi `enctype="multipart/form-data"` → không upload được file.
- Đổi `id` canvas/hidden input → JS không cập nhật được base64 → chữ ký rỗng.
- Đổi value `respond=accept|reject` hoặc `action_type=no_repeat|...` → branching controller mất tác dụng.

### 1.10. Rủi Ro Ảnh Hưởng Module Khác

- CSS global không scope sẽ leak sang `portal_custom`, `portal`, `survey`, `approvals`.
- XPath inherit dùng selector quá rộng có thể clash priority với module khác.

### 1.11. Lệch Giữa `module_map.json` và Source Thật

- `counts.controllers: 2` (`__init__.py` + `portal.py`) ✓ khớp.
- `counts.views: 5` ✓ khớp.
- `manifest.data` ✓ khớp `__manifest__.py`.
- **Khuyến nghị**: regenerate `module_map.json` sau khi blueprint được áp dụng.

---

## 2. Target Portal UI Architecture

### 2.1. Nguyên Tắc Tổng

- **Chỉnh minimal**: tập trung 90% vào `views/x_psm_portal_templates.xml`. Không sửa controller, model, security.
- **Scope CSS** dưới class wrapper `.o_psm_0215_portal` thêm trên element ngoài cùng mỗi template chính.
- Mọi selector CSS phải bắt đầu bằng `.o_psm_0215_portal`.

### 2.2. Two Implementation Options cho CSS

**Option A (khuyến nghị)** — Asset file scoped:
- Tạo `static/src/scss/portal_psm_0215.scss`.
- Thêm vào `__manifest__.py`:
  ```python
  "assets": {
      "web.assets_frontend": [
          "M02_P0215/static/src/scss/portal_psm_0215.scss",
      ],
  },
  ```
- Ưu: cache tốt, dễ maintain. Rủi ro: thêm key manifest → cần test upgrade.

**Option B (fallback)** — Inline `<style>` trong template phụ:
- Không sửa manifest, không tạo file mới.
- Đặt `<style>` trong template `portal_psm_0215_assets_inline`, các template chính `t-call`.

→ Khuyến nghị Option A.

### 2.3. Template Wrapper

```xml
<t t-call="portal.portal_layout">
    <div class="o_psm_0215_portal">
        <!-- nội dung template -->
    </div>
</t>
```

### 2.4. Áp Dụng Palette

| Màu | Mã hex | Dùng cho |
|---|---|---|
| McDonald's Yellow | `#FFC72C` | Accent, header, CTA chính, focus highlight |
| McDonald's Red | `#DA291C` | Warning/danger, nút từ chối, cảnh báo nghiêm trọng |
| Black | `#000000` | Text chính, heading, high contrast |
| White | `#FFFFFF` | Nền card/form/table |

- Chữ đen trên vàng (contrast 11.5:1 — đạt AAA).
- Chữ trắng trên đỏ (đạt AA cho text lớn).
- Không dùng chữ vàng/trắng trên nền sáng.

### 2.5. Tổ Chức List Page

- Desktop: bảng 5 cột, row hover vàng nhạt 10% opacity.
- Mobile (< 768px): chuyển sang card list — CSS transform table → block.
- Empty state: icon + heading + hint + CTA.

### 2.6. Tổ Chức Create Form

5 logical sections:
1. **Thông tin các bên** (Đại diện + Nhân viên + Người làm chứng)
2. **Ngày & Mục đích**
3. **Vi phạm** (Category + Type)
4. **Nội dung** (Section I → IV + Upload ảnh)
5. **Chữ ký & Submit**

### 2.7. Tổ Chức Detail Page

5 panels:
1. **Thông tin các bên** (read-only)
2. **Thông tin vi phạm** (read-only)
3. **Section I** + ảnh đính kèm
4. **Section II + III + IV** với inline form ký nếu cần
5. **Action panel** contextual theo `state` + `is_manager`/`is_subject`

### 2.8. CTA Hierarchy

| Loại | Màu nền | Màu chữ | Dùng cho |
|---|---|---|---|
| Primary | `#FFC72C` | `#000000` | Lưu, Hoàn tất, Tạo mới, Chấp nhận |
| Secondary | `#FFFFFF` | `#000000` + viền | Hủy, Quay lại, Xóa chữ ký |
| Danger | `#DA291C` | `#FFFFFF` | Từ chối kỷ luật |
| Ghost | trong suốt | `#000000` + underline | Link điều hướng phụ |

### 2.9. Status Badge Mapping

| Nhóm | States | Nền | Chữ |
|---|---|---|---|
| Neutral | `draft`, `cancel`, `expired` | xám nhạt | xám đậm |
| In Progress | `under_review`, `level_determination`, `investigation`, `hearing`, `proposal`, `issued`, `approval` | `#FFC72C` | `#000000` |
| Pending Action | `notified` | `#DA291C` | `#FFFFFF` |
| Success | `active` | `#000000` | `#FFFFFF` + viền vàng |

---

## 3. Visual Design System

### 3.1. Palette & CSS Variables

```scss
.o_psm_0215_portal {
    /* Primary palette — McDonald's */
    --psm-0215-yellow:        #FFC72C;
    --psm-0215-red:           #DA291C;
    --psm-0215-black:         #000000;
    --psm-0215-white:         #FFFFFF;

    /* Derived tints / shades */
    --psm-0215-yellow-soft:   #FFF4D0;   /* nền vàng nhạt cho alert/banner */
    --psm-0215-yellow-strong: #E6B428;   /* hover/active vàng */
    --psm-0215-red-soft:      #FCEAE7;   /* nền đỏ nhạt cho error */
    --psm-0215-red-strong:    #B11F14;   /* hover/active đỏ */

    /* Neutral support */
    --psm-0215-gray-50:       #FAFAFA;   /* nền card */
    --psm-0215-gray-100:      #F2F2F2;   /* nền input/section */
    --psm-0215-gray-200:      #E5E5E5;   /* border nhẹ */
    --psm-0215-gray-500:      #6B6B6B;   /* muted text */
    --psm-0215-gray-700:      #3F3F3F;   /* secondary text */

    /* Token semantics */
    --psm-0215-bg:            var(--psm-0215-white);
    --psm-0215-text:          var(--psm-0215-black);
    --psm-0215-text-muted:    var(--psm-0215-gray-500);
    --psm-0215-border:        var(--psm-0215-gray-200);
    --psm-0215-accent:        var(--psm-0215-yellow);
    --psm-0215-danger:        var(--psm-0215-red);
}
```

### 3.2. Component Styles

#### Header / Banner

```scss
.o_psm_0215_portal .psm-banner {
    background: var(--psm-0215-yellow);
    color: var(--psm-0215-black);
    padding: 1rem 1.25rem;
    border-radius: .75rem .75rem 0 0;
    font-weight: 700;
    letter-spacing: .25px;
}
```

#### Card

```scss
.o_psm_0215_portal .psm-card {
    background: var(--psm-0215-white);
    border: 1px solid var(--psm-0215-border);
    border-radius: .75rem;
    box-shadow: 0 1px 2px rgba(0,0,0,.04);
    overflow: hidden;
}
```

#### Table + Mobile Card List

```scss
.o_psm_0215_portal .psm-table {
    width: 100%;
    border-collapse: separate;
    border-spacing: 0;
}
.o_psm_0215_portal .psm-table thead th {
    background: var(--psm-0215-black);
    color: var(--psm-0215-white);
    font-weight: 600;
    text-transform: uppercase;
    font-size: .8rem;
    padding: .65rem .9rem;
}
.o_psm_0215_portal .psm-table tbody tr:hover {
    background: var(--psm-0215-yellow-soft);
}
.o_psm_0215_portal .psm-table tbody td {
    padding: .8rem .9rem;
    border-bottom: 1px solid var(--psm-0215-border);
}

/* Mobile: chuyển table → card list */
@media (max-width: 767.98px) {
    .o_psm_0215_portal .psm-table thead { display: none; }
    .o_psm_0215_portal .psm-table tbody tr {
        display: block;
        margin-bottom: .75rem;
        border: 1px solid var(--psm-0215-border);
        border-radius: .5rem;
        overflow: hidden;
    }
    .o_psm_0215_portal .psm-table tbody td {
        display: flex;
        justify-content: space-between;
        gap: 1rem;
        border-bottom: 1px dashed var(--psm-0215-border);
    }
    .o_psm_0215_portal .psm-table tbody td::before {
        content: attr(data-label);
        font-weight: 600;
        color: var(--psm-0215-gray-500);
    }
}
```

> Cần thêm `data-label="…"` trên từng `<td>` trong QWeb để mobile hiển thị nhãn.

#### Status Badge

```scss
.o_psm_0215_portal .psm-badge {
    display: inline-flex;
    align-items: center;
    gap: .35rem;
    padding: .25rem .65rem;
    border-radius: 999px;
    font-size: .75rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: .25px;
}
.o_psm_0215_portal .psm-badge--neutral  { background: #EFEFEF; color: #3F3F3F; }
.o_psm_0215_portal .psm-badge--progress { background: var(--psm-0215-yellow); color: var(--psm-0215-black); }
.o_psm_0215_portal .psm-badge--pending  { background: var(--psm-0215-red); color: var(--psm-0215-white); }
.o_psm_0215_portal .psm-badge--success  {
    background: var(--psm-0215-black);
    color: var(--psm-0215-white);
    box-shadow: inset 0 0 0 2px var(--psm-0215-yellow);
}
```

QWeb map state → modifier:

```xml
<t t-set="state_group" t-value="
    'neutral'  if rec.state in ('draft','cancel','expired') else
    'pending'  if rec.state == 'notified' else
    'success'  if rec.state == 'active' else
    'progress'"/>
<span t-attf-class="psm-badge psm-badge--#{state_group}">
    <t t-esc="dict(rec._fields['state'].selection).get(rec.state, rec.state)"/>
</span>
```

#### Buttons

```scss
.o_psm_0215_portal .psm-btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: .5rem;
    padding: .65rem 1.25rem;
    border-radius: 999px;
    font-weight: 700;
    border: 1px solid transparent;
    transition: transform .12s ease, background-color .12s ease;
    min-height: 44px; /* tap target */
}
.o_psm_0215_portal .psm-btn:focus-visible {
    outline: 3px solid var(--psm-0215-yellow);
    outline-offset: 2px;
}
.o_psm_0215_portal .psm-btn--primary {
    background: var(--psm-0215-yellow);
    color: var(--psm-0215-black);
}
.o_psm_0215_portal .psm-btn--primary:hover { background: var(--psm-0215-yellow-strong); }
.o_psm_0215_portal .psm-btn--secondary {
    background: var(--psm-0215-white);
    color: var(--psm-0215-black);
    border-color: var(--psm-0215-gray-200);
}
.o_psm_0215_portal .psm-btn--danger {
    background: var(--psm-0215-red);
    color: var(--psm-0215-white);
}
.o_psm_0215_portal .psm-btn--danger:hover { background: var(--psm-0215-red-strong); }
```

#### Form Section

```scss
.o_psm_0215_portal .psm-section {
    padding: 1.25rem;
    border-top: 1px solid var(--psm-0215-border);
}
.o_psm_0215_portal .psm-section:first-child { border-top: 0; }
.o_psm_0215_portal .psm-section__head {
    display: flex;
    align-items: center;
    gap: .65rem;
    margin-bottom: .75rem;
}
.o_psm_0215_portal .psm-section__index {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 28px;
    height: 28px;
    border-radius: 50%;
    background: var(--psm-0215-yellow);
    color: var(--psm-0215-black);
    font-weight: 700;
    font-size: .85rem;
}
.o_psm_0215_portal .psm-section__title {
    margin: 0;
    font-size: 1rem;
    font-weight: 700;
    text-transform: uppercase;
}
```

#### Required Field Marker

```scss
.o_psm_0215_portal .psm-label--required::after {
    content: " *";
    color: var(--psm-0215-red);
    font-weight: 700;
}
```

#### Alert

```scss
.o_psm_0215_portal .psm-alert {
    display: flex;
    gap: .75rem;
    align-items: flex-start;
    padding: .85rem 1rem;
    border-radius: .5rem;
    border-left: 4px solid;
    margin-bottom: 1rem;
}
.o_psm_0215_portal .psm-alert--danger  {
    background: var(--psm-0215-red-soft);
    border-color: var(--psm-0215-red);
}
.o_psm_0215_portal .psm-alert--success {
    background: var(--psm-0215-yellow-soft);
    border-color: var(--psm-0215-yellow);
    color: var(--psm-0215-black);
}
.o_psm_0215_portal .psm-alert--info {
    background: var(--psm-0215-gray-100);
    border-color: var(--psm-0215-gray-500);
}
```

#### Empty State

```scss
.o_psm_0215_portal .psm-empty {
    text-align: center;
    padding: 3rem 1rem;
    border: 1px dashed var(--psm-0215-border);
    border-radius: .75rem;
    background: var(--psm-0215-gray-50);
}
.o_psm_0215_portal .psm-empty__icon {
    font-size: 3rem;
    color: var(--psm-0215-yellow);
}
.o_psm_0215_portal .psm-empty__title {
    font-weight: 700;
    margin: .5rem 0;
}
.o_psm_0215_portal .psm-empty__hint {
    color: var(--psm-0215-text-muted);
    margin-bottom: 1rem;
}
```

#### Signature Area

```scss
.o_psm_0215_portal .psm-signature {
    background: var(--psm-0215-white);
    border: 1px dashed var(--psm-0215-gray-200);
    border-radius: .5rem;
    padding: .35rem;
}
.o_psm_0215_portal .psm-signature__pad {
    width: 100%;
    height: clamp(140px, 30vw, 200px);
    touch-action: none;
    cursor: crosshair;
}
.o_psm_0215_portal .psm-signature__hint {
    font-size: .75rem;
    color: var(--psm-0215-text-muted);
    margin-top: .35rem;
}
```

#### File Upload Area

```scss
.o_psm_0215_portal .psm-upload {
    border: 2px dashed var(--psm-0215-yellow);
    border-radius: .65rem;
    padding: 1rem;
    background: var(--psm-0215-yellow-soft);
}
.o_psm_0215_portal .psm-upload__hint {
    color: var(--psm-0215-gray-700);
    margin-top: .5rem;
}
```

### 3.3. Accessibility

| Yêu cầu | Giải pháp |
|---|---|
| Contrast | Chữ đen trên vàng (11.5:1 — AAA); chữ trắng trên đỏ (AA large text) |
| Focus state | `outline: 3px solid #FFC72C; outline-offset: 2px` |
| Label/input | `<label for="id">` match `id` của input |
| Button text | Luôn có text rõ hành động, không chỉ icon |
| Không chỉ dùng màu | Kèm icon + label tiếng Việt cho state |
| Tap target | Tối thiểu 44px (`min-height: 44px`) |
| Alert ARIA | `role="alert"`, `aria-live="polite"` |

---

## 4. Portal UX Redesign Plan

### 4.1. Portal Home / Sidebar

- **Sidebar link** (`portal_psm_discipline_sidebar_link`):
  - Đổi icon wrapper style từ `background:#fff3cd; color:#856404` sang `background:#FFC72C; color:#000000`.
  - Badge `discipline_count > 0`: đổi sang `style="background:#DA291C;"` thay vì `bg-danger` Bootstrap.
  - Giữ text hiện có hoặc đổi thành "Hồ sơ kỷ luật" — xác nhận với user trước.
  - Giữ nguyên xpath `after`, priority `50`, inherit_id.

### 4.2. `/my/disciplines` — List Page

```
[ Searchbar: "Disciplinary Records" | sortby ▼ | (manager) [+ Tạo Counseling Log] ]
[ Empty state hoặc Table/cards ]
[ Pager ]
```

**Desktop columns**: Reference | Employee | Vi phạm (category + type) | Ngày | Trạng thái

**Mỗi `<td>` thêm `data-label="..."`** để mobile cardlist hiển thị nhãn.

**Empty state QWeb**:
```xml
<div class="o_psm_0215_portal psm-empty" role="status" aria-live="polite">
    <i class="fa fa-folder-open psm-empty__icon" aria-hidden="true"/>
    <h5 class="psm-empty__title">Chưa có hồ sơ kỷ luật nào</h5>
    <p class="psm-empty__hint">Hiện tại bạn không có hồ sơ kỷ luật trong tài khoản.</p>
    <a t-if="is_manager" href="/my/discipline/create" class="psm-btn psm-btn--primary">
        <i class="fa fa-plus-circle" aria-hidden="true"/> Tạo Counseling Log
    </a>
</div>
```

**CTA Manager**: dùng class `psm-btn psm-btn--primary` thay `btn btn-warning text-dark fw-bold rounded-pill`.

### 4.3. `/my/discipline/create` — Create Form

**Section layout**:
```
[Banner: "COUNSELLING LOG" — vàng + đen]
[Section 1: Thông tin các bên — số tròn vàng "1"]
[Section 2: Ngày thực hiện + Mục đích]
[Section 3: Vi phạm — Category + Type]
[Section 4: Nội dung — Section I + II + III + IV + Upload ảnh]
[Section 5: Chữ ký — Manager + Employee + Witness]
[Sticky bottom (desktop ≥ 992px): [LƯU & TẠO LOG] + [Hủy bỏ]]
[Modal validation — giữ nguyên, đã đúng palette]
```

**Quy tắc cứng cho create form**:
- KHÔNG đổi `name` bất kỳ input nào.
- KHÔNG đổi `id` canvas/hidden signature.
- KHÔNG đổi `enctype`, `method`, `action`.
- KHÔNG đổi JS inline (signature pad / image preview / employee select / witness select).
- Giữ `<input type="hidden" name="csrf_token" .../>`.

### 4.4. `/my/discipline/<id>` — Detail Page

**Status badge tiếng Việt** (thay `record.state.upper()`):
```xml
<t t-set="state_group" t-value="
    'neutral'  if record.state in ('draft','cancel','expired') else
    'pending'  if record.state == 'notified' else
    'success'  if record.state == 'active' else
    'progress'"/>
<span t-attf-class="psm-badge psm-badge--#{state_group}">
    <t t-esc="dict(record._fields['state'].selection).get(record.state, record.state)"/>
</span>
```

**Alert mapping** (thêm vào đầu card body):
```xml
<t t-if="request.params.get('success') == 'created'">
    <div class="psm-alert psm-alert--success" role="status" aria-live="polite">
        <i class="fa fa-check-circle" aria-hidden="true"/>
        <span>Hồ sơ đã được tạo thành công.</span>
    </div>
</t>
<t t-if="error == 'missing_signature'">
    <div class="psm-alert psm-alert--danger" role="alert">
        <i class="fa fa-exclamation-triangle" aria-hidden="true"/>
        <span>Vui lòng ký tên trước khi gửi.</span>
    </div>
</t>
<t t-if="error == 'missing_reject_note'">
    <div class="psm-alert psm-alert--danger" role="alert">
        <i class="fa fa-exclamation-triangle" aria-hidden="true"/>
        <span>Vui lòng nhập lý do từ chối trước khi gửi.</span>
    </div>
</t>
```

**Action panel contextual theo role/state**:

| Điều kiện | Block render |
|---|---|
| `is_subject` + không có `employee_signature` + `state in ('draft','under_review')` + có `section_ii_feedback` | Form ký bổ sung employee |
| `is_subject` + `state == 'draft'` (chưa có feedback) | Form nhập feedback + ký |
| `is_manager` + không có `manager_signature` + `state in ('draft','under_review')` + có `section_iii_identification` | Form manager ký bổ sung |
| `is_manager` + `state == 'draft'` + chưa có Section III | Form nhập Section III/IV + ký |
| `record.x_psm_employee_id.parent_id.user_id == request.env.user` + `state == 'under_review'` | Block 4 button RGM action (đề xuất thêm — hỏi user trước) |
| `state == 'notified'` + `is_subject` + `not record.x_psm_is_accepted` | Form accept/reject |
| `record.x_psm_action_id` + `record.x_psm_is_accepted` | Result panel |

**Block RGM action UI đề xuất thêm** (controller đã hỗ trợ route `/my/discipline/rgm_action`):
```xml
<t t-if="record.state == 'under_review' and record.x_psm_employee_id.parent_id.user_id.id == request.env.user.id">
    <div class="psm-section">
        <div class="psm-section__head">
            <span class="psm-section__index">★</span>
            <h6 class="psm-section__title">Quyết định cấp xử lý (RGM)</h6>
        </div>
        <form action="/my/discipline/rgm_action" method="post" class="d-flex flex-wrap gap-2">
            <input type="hidden" name="csrf_token" t-att-value="request.csrf_token()"/>
            <input type="hidden" name="x_psm_record_id" t-att-value="record.id"/>
            <button type="submit" name="action_type" value="no_repeat"     class="psm-btn psm-btn--secondary">Không tái phạm</button>
            <button type="submit" name="action_type" value="set_repeat"    class="psm-btn psm-btn--secondary">Đánh dấu tái phạm</button>
            <button type="submit" name="action_type" value="store_level"   class="psm-btn psm-btn--primary">Xử lý cấp Nhà hàng</button>
            <button type="submit" name="action_type" value="company_level" class="psm-btn psm-btn--danger">Đẩy lên cấp Công ty</button>
        </form>
    </div>
</t>
```

> ⚠️ **Hỏi user trước** khi thêm block RGM action vì có thể nằm ngoài scope "chỉ cải UI".

### 4.5. Employee Response / Signature

- Canvas mobile: `height: clamp(140px, 30vw, 200px)`, `touch-action: none`.
- Nút "Xóa chữ ký" dùng `psm-btn psm-btn--secondary` (không phải danger — xóa chữ ký không phải hành động phá hoại).
- Validation JS hiện tại giữ nguyên.

### 4.6. Manager Finalize / RGM Action / Accept-Reject

- CTA phân cấp: Primary (vàng) → Danger (đỏ) → Secondary (trắng/viền).
- Không đổi POST URL.
- Modal validation: giữ nguyên JS + markup.

---

## 5. QWeb And CSS Implementation Design

### 5.1. Files Cần Sửa

**Bắt buộc**:
- `addons/M02_P0215/views/x_psm_portal_templates.xml` — bọc wrapper, thay class, `data-label`, status badge, alert palette, sửa "PHÀN HỒI" → "PHẢN HỒI".

**Có thể (Option A)**:
- `addons/M02_P0215/__manifest__.py` — thêm key `"assets"`.
- `addons/M02_P0215/static/src/scss/portal_psm_0215.scss` — tạo file SCSS mới (scoped).

**Không sửa**:
- `controllers/portal.py`
- `models/x_psm_hr_discipline_record.py`
- `security/*`

### 5.2. Quy Tắc QWeb/XML

| Quy tắc | Lý do |
|---|---|
| Giữ `t-call="portal.portal_layout"` | Mất breadcrumbs/searchbar/menu |
| Giữ `csrf_token` hidden input | 403 CSRF nếu thiếu |
| Giữ `enctype="multipart/form-data"` | Upload ảnh fail nếu thiếu |
| Giữ `method="post"`, `action="..."` | Controller POST không nhận được |
| Giữ `name` của mọi input/select | Controller `post.get("...")` trả `None` |
| Giữ `id` canvas (`*-pad`) + hidden (`*_sig_data`) | JS không update được base64 |
| Giữ `value` radio/button | Branching controller mất tác dụng |
| Escape XML: `&` → `&amp;`, `<` → `&lt;` | XML invalid → lỗi parse |
| `t-foreach="x" t-as="y"` đầy đủ 2 attr | QWeb error nếu thiếu 1 |
| `or '---'` cho field optional | Tránh crash khi field rỗng |
| `t-if` guard cho record optional | Tránh AttributeError |

### 5.3. JS Inline

- Giữ nguyên 100% JS inline hiện có (signature pad, select sync, image preview, validation modal).
- Thêm JS nhỏ vào script block hiện có nếu cần (confirm before reject).
- Không thêm thư viện external.

### 5.4. CSS Scope Rules

```scss
/* ✅ Đúng */
.o_psm_0215_portal .psm-btn--primary { ... }
.o_psm_0215_portal .psm-table thead th { ... }

/* ❌ Cấm — selector global */
.btn { ... }
.card { ... }
.table { ... }
.badge { ... }
.alert { ... }
.form-control { ... }
.o_portal_my_doc_table { ... }
```

### 5.5. XML IDs Không Được Đổi

```
portal_psm_discipline_sidebar_link
portal_psm_my_home_menu_discipline
portal_psm_my_home_discipline
portal_psm_my_disciplines
portal_psm_discipline_create
portal_psm_discipline_explanation_template
```

Template phụ mới (nếu cần): đặt id với prefix `portal_psm_`, ví dụ `portal_psm_0215_assets_inline`.

---

## 6. Backward Compatibility And Install Safety

### 6.1. Checklist Đầy Đủ

| # | Kiểm tra | Cách kiểm |
|---|---|---|
| 1 | XML hợp lệ | `xmllint --noout views/x_psm_portal_templates.xml` |
| 2 | XPath inherit hợp lệ | install/upgrade không lỗi `xpath did not match` |
| 3 | Template id không đổi | grep template id cũ còn reference |
| 4 | External ID không đổi | grep `M02_P0215.portal_psm_*` |
| 5 | Manifest data order | data list giữ thứ tự; assets là key riêng |
| 6 | Asset path tồn tại | nếu thêm asset, file scss/css phải tồn tại |
| 7 | Không thêm dependency mới | `depends` list không đổi |
| 8 | Không đổi route/controller | `controllers/portal.py` không sửa |
| 9 | Không đổi input field name | xem mục 1.4 |
| 10 | Không đổi model field name | model không sửa |
| 11 | Không đổi security/access | security/* không sửa |
| 12 | Portal không crash khi field rỗng | `or '---'`, `t-if` guard |
| 13 | Mobile không tràn ngang | `overflow-x: hidden` wrapper, cardlist < 768px |
| 14 | CSS scope strict | mọi selector bắt đầu `.o_psm_0215_portal` |

### 6.2. Fallback Cho Field Optional

```xml
<!-- Đúng pattern — dùng or '---' -->
<t t-esc="record.x_psm_violation_category_id.name or '---'"/>
<t t-esc="record.x_psm_emp_department_id.name or '---'"/>
<t t-esc="record.x_psm_emp_job_id.name or '---'"/>
<t t-esc="record.x_psm_violation_type or '---'"/>
<t t-esc="record.x_psm_section_i_description or '---'"/>

<!-- State label an toàn -->
<t t-esc="dict(record._fields['state'].selection).get(record.state, record.state)"/>

<!-- Guard cho Many2one optional -->
<t t-if="record.x_psm_action_id">
    <t t-esc="record.x_psm_action_id.name"/>
</t>
```

---

## 7. Cross-Module Regression Risk Analysis

### 7.1. Module `portal`

- **Rủi ro**: override `.o_portal_my_doc_table`, `.o_portal_pager` toàn cục → vỡ `/my/invoices`, `/my/orders`.
- **Guard**: dùng class `psm-table` riêng, không override `.o_portal_my_doc_table`. Pager giữ `t-call="portal.pager"`.
- **Check**: mở `/my/invoices` sau upgrade → UI không đổi.

### 7.2. Module `portal_custom`

- **Rủi ro**: inherit `portal_custom.portal_my_home_inherit` clash priority.
- **Guard**: giữ `priority="50"`, không đổi xpath expr.
- **Check**: portal home hiển thị sidebar đầy đủ link, không trùng/mất.

### 7.3. Module `hr`

- **Rủi ro**: `employee.name`, `department_id.name` rỗng nếu portal user không link employee.
- **Guard**: dùng `or '---'` cho tất cả field display liên quan employee.
- **Check**: portal user không có employee link → `/my/disciplines` không crash.

### 7.4. Module `mail`

- **Rủi ro**: thêm chatter portal không đúng cách có thể lỗi permission.
- **Guard**: KHÔNG thêm chatter trong blueprint này.

### 7.5. Module `approvals`

- **Rủi ro**: không có tác động portal UI trực tiếp.
- **Guard**: không tạo button gọi `approval.action_*` trên portal.

### 7.6. Module `survey`

- **Rủi ro**: link survey dùng access_token.
- **Guard**: nếu hiển thị link, dùng `record.x_psm_explanation_survey_user_input_id.access_token` — read-only.

### 7.7. Module `M02_P0200`

- **Rủi ro**: phụ thuộc group `GDH_OPS_STORE_SM_M`/`RGM_M`/`HRBP_S`/`OC_S`.
- **Guard**: không sửa security xml/csv; không tham chiếu group mới.

### 7.8. Các Module Portal Khác

- **Rủi ro**: CSS leak nếu không scope đúng.
- **Guard**: bắt buộc mọi selector bắt đầu `.o_psm_0215_portal`.
- **Audit**: `grep -E "^[^.{]" portal_psm_0215.scss` không có selector global.
- **Check**: mở bất kỳ trang portal module khác → UI không đổi.

---

## 8. Business Logic And UX Rules

### 8.1. Quy Tắc Bất Biến (Không Được Phá)

| Quy tắc | Lý do |
|---|---|
| UI không thay đổi nghiệp vụ | Task chỉ là cải thiện giao diện |
| Manager mới thấy CTA tạo Counseling Log | `_x_psm_is_manager_employee` guard |
| Employee chỉ thao tác hồ sơ của mình | Record rule portal own |
| Không đổi `_x_psm_can_view_record` | Security gate controller |
| Không đổi `_x_psm_can_finalize_record` | Security gate controller |
| Không đổi POST route | Controller contract |
| Không đổi trạng thái record bằng UI | Chỉ controller/model được phép |
| Không xóa legacy fallback `submit_section_ii`, `manager_finalize` | Backward compatibility |
| Không làm mất `csrf_token` | 403 CSRF |
| Không làm mất upload attachment | `enctype`, `name` |
| Không làm mất signature | `id` canvas + hidden |
| Không làm mất pager + sortby | UX list page |
| Dữ liệu cũ vẫn render được | `or '---'`, `t-if` guard |

### 8.2. UI Affordance Theo Role/State

| Role | State | Hiển thị |
|---|---|---|
| Employee (is_subject) | draft (chưa có feedback) | Form nhập Section II + ký |
| Employee (is_subject) | under_review (chưa ký) | Form ký bổ sung |
| Employee (is_subject) | notified | Form accept/reject |
| Employee (is_subject) | active/expired/cancel | Read-only |
| Manager (is_parent hoặc is_rep) | draft | Form nhập Section III/IV + ký |
| Manager (is_parent hoặc is_rep) | under_review (chưa ký manager) | Form manager ký bổ sung |
| RGM (parent_id) | under_review | 4 button RGM action (nếu thêm) |
| Khác | * | Read-only |

### 8.3. Copy/Text

- Giữ tiếng Việt có dấu, không phá encoding UTF-8.
- **Sửa lỗi đánh máy**: "GỬI PHÀN HỒI" → "GỬI PHẢN HỒI".
- Giữ comment tiếng Việt không dấu trong model — chủ ý lưu legacy, không sửa.

---

## 9. Implementation Roadmap For AI Coder

### Bước 1 — Đọc convention + structure

| Mục | Chi tiết |
|---|---|
| File đọc | `convention/QUY_UOC_DAT_TEN_VA_RULE.md`, `structure/module_map.json` |
| Mục tiêu | Nắm naming convention `x_psm_0215_*`, rule ưu tiên sẵn có, phân quyền tối thiểu |
| Rủi ro | Không có |
| Test | Không cần |

### Bước 2 — Verify portal routes và template variables

| Mục | Chi tiết |
|---|---|
| File đọc | `controllers/portal.py`, `views/x_psm_portal_templates.xml` |
| Mục tiêu | Đối chiếu input names + render values với blueprint mục 1.4 |
| Rủi ro | Không có |
| Test | Không cần |

### Bước 3 — Audit hiện trạng UX

| Mục | Chi tiết |
|---|---|
| File đọc | Như bước 2 |
| Mục tiêu | Liệt kê "trước → sau" cho từng template |
| Rủi ro | Không có |
| Test | Không cần |

### Bước 4 — Define scoped design wrapper & CSS

| Mục | Chi tiết |
|---|---|
| File sửa | `__manifest__.py` (nếu Option A), tạo `static/src/scss/portal_psm_0215.scss` (nếu Option A) |
| Mục tiêu | Viết CSS theo mục 3.2, mọi selector scope dưới `.o_psm_0215_portal` |
| Rủi ro | Scope sai → leak ra portal khác. Audit selector trước khi commit |
| Test | `python odoo-bin -d <db> -u M02_P0215 --stop-after-init` không lỗi |

### Bước 5 — Redesign portal home/sidebar entry

| Mục | Chi tiết |
|---|---|
| File sửa | `views/x_psm_portal_templates.xml` — template `portal_psm_discipline_sidebar_link` |
| Mục tiêu | Icon vàng `#FFC72C` + chữ đen, badge đỏ `#DA291C` |
| Rủi ro | Phá `portal_custom.portal_my_home_inherit` layout nếu đổi xpath |
| Test | `/my` → sidebar link đúng màu, badge hiển thị khi `discipline_count > 0` |

### Bước 6 — Redesign `/my/disciplines` list page

| Mục | Chi tiết |
|---|---|
| File sửa | `views/x_psm_portal_templates.xml` — template `portal_psm_my_disciplines` |
| Mục tiêu | Bọc wrapper `.o_psm_0215_portal`, thay table classes, `data-label`, status badge, empty state, CTA |
| Rủi ro | Mất pager nếu xóa `t-call="portal.pager"`. Sortby phải truyền đủ. `t-if="is_manager"` giữ nguyên |
| Test | (a) No data → empty state; (b) Có data → table + badge; (c) Mobile → cardlist |

### Bước 7 — Redesign `/my/discipline/create` form

| Mục | Chi tiết |
|---|---|
| File sửa | `views/x_psm_portal_templates.xml` — template `portal_psm_discipline_create` |
| Mục tiêu | 5 section block, button classes, giữ toàn bộ input name/id, modal validation giữ nguyên |
| Rủi ro | Đổi `name` input → controller break. JS inline phụ thuộc DOM id — không đổi id |
| Test | Tạo log mẫu → POST thành công → redirect `/my/discipline/<id>?success=created`. Chữ ký mobile (touch) |

### Bước 8 — Redesign `/my/discipline/<id>` detail/action

| Mục | Chi tiết |
|---|---|
| File sửa | `views/x_psm_portal_templates.xml` — template `portal_psm_discipline_explanation_template` |
| Mục tiêu | Wrapper, banner + status badge tiếng Việt, alert palette, 5 panel, action panel contextual |
| Rủi ro | Đổi `t-if` condition → mất form ký. Đổi form `action`/`name` → POST break |
| Test | Render record ở `draft`, `under_review`, `notified`, `active` → UI đúng state. Submit form ký không lỗi |

### Bước 9 — Mobile/responsive check

| Mục | Chi tiết |
|---|---|
| Viewport | 360px, 768px, 1024px |
| Kiểm | Không overflow, button tap target ≥ 44px, signature canvas đủ rộng, modal centered |
| Tool | DevTools responsive mode + real device nếu có |

### Bước 10 — Install/upgrade/regression check

```bash
# Kiểm tra upgrade
python odoo-bin -d <db_test> -u M02_P0215 --stop-after-init

# Kiểm tra fresh install
python odoo-bin -d <db_test> -i M02_P0215 --stop-after-init

# Kiểm tra với test
python odoo-bin -d <db_test> -u M02_P0215 --test-enable --stop-after-init
```

Docker:
```bash
docker ps
docker exec <odoo_container> odoo -d <db_test> -u M02_P0215 --stop-after-init
docker logs <odoo_container> --tail 200
docker restart <odoo_container>
```

**Regression check**: mở 1 trang portal module khác → UI không đổi.

### Bước 11 — Regenerate structure map

- Chạy generator nếu repo có script, sau khi source ổn định.
- Cập nhật `structure/module_map.json` + `module_map_stats.json` nếu có thêm file mới.

---

## 10. Prompt Cho Executor (AI Coder)

> Copy-paste nguyên văn cho AI Coder thực hiện:

---

**Bạn là AI Coder. Nhiệm vụ: chỉnh sửa UI Portal cho module `addons/M02_P0215` (Employee Disciplinary Process) trong Odoo 19. KHÔNG được sửa logic, route, controller contract, model field, security, hay XML ID hiện có.**

### Bước 1 — Đọc convention và structure trước khi sửa

- `addons/M02_P0215/convention/QUY_UOC_DAT_TEN_VA_RULE.md`
- `addons/M02_P0215/structure/module_map.json`
- Nếu cần thêm: `addons/M02_P0215/structure/module_map_stats.json`

### Bước 2 — Đọc các file Portal liên quan

- `addons/M02_P0215/__manifest__.py`
- `addons/M02_P0215/controllers/portal.py`
- `addons/M02_P0215/views/x_psm_portal_templates.xml`
- `addons/M02_P0215/models/x_psm_hr_discipline_record.py`
- `addons/M02_P0215/security/security_rules.xml`
- `addons/M02_P0215/security/ir.model.access.csv`

### Bước 3 — Palette bắt buộc (McDonald's)

| Màu | Hex | Dùng cho |
|---|---|---|
| Yellow | `#FFC72C` | Accent, header, CTA chính, focus |
| Red | `#DA291C` | Danger, warning, từ chối |
| Black | `#000000` | Text chính, heading |
| White | `#FFFFFF` | Nền card/form |

- **Chữ đen trên vàng** (contrast 11.5:1 — AAA).
- **Chữ trắng trên đỏ** (đạt AA).
- KHÔNG dùng chữ vàng/trắng trên nền sáng.

### Bước 4 — Scope CSS bắt buộc

- Bọc mỗi template chính: `<div class="o_psm_0215_portal">…</div>` ngay trong `<t t-call="portal.portal_layout">`.
- **Mọi selector CSS phải bắt đầu bằng `.o_psm_0215_portal`**.
- CẤM override: `.card`, `.btn`, `.table`, `.badge`, `.alert`, `.form-control`, `.form-select`, `.modal`, `.o_portal*`.
- Option A (asset): thêm `"assets": {"web.assets_frontend": ["M02_P0215/static/src/scss/portal_psm_0215.scss"]}` vào manifest + tạo file SCSS.
- Option B (fallback): `<style>` block trong template phụ `portal_psm_0215_assets_inline`, `t-call` từ 3 template chính.

### Bước 5 — Routes và templates cần kiểm tra

**Routes hiện có** (KHÔNG đổi):
- `/my`, `/my/home`
- `/my/disciplines`, `/my/disciplines/page/<int:page>`
- `/my/discipline/create`
- `/my/discipline/<int:x_psm_record_id>`
- `/my/discipline/submit_section_ii`
- `/my/discipline/manager_finalize`
- `/my/discipline/rgm_action`
- `/my/discipline/respond`

**Template XML IDs** (KHÔNG đổi):
- `portal_psm_discipline_sidebar_link`
- `portal_psm_my_home_menu_discipline`
- `portal_psm_my_home_discipline`
- `portal_psm_my_disciplines`
- `portal_psm_discipline_create`
- `portal_psm_discipline_explanation_template`

### Bước 6 — Quy tắc QWeb/XML (bắt buộc)

1. Giữ `<t t-call="portal.portal_layout">` ở mỗi page template.
2. Giữ `<input type="hidden" name="csrf_token" t-att-value="request.csrf_token()"/>` trong mọi form POST.
3. Giữ `enctype="multipart/form-data"` ở form create.
4. Giữ `method="post"`, `action="/my/..."` trên mọi form.
5. TUYỆT ĐỐI không đổi `name` của input/select/textarea (xem danh sách mục 1.4).
6. Giữ `id` canvas (`employee-pad`, `manager-pad`, `witness-pad`) và hidden input (`employee_sig_data`, `manager_sig_data`, `witness_sig_data`).
7. Giữ `value` của radio purpose (`discipline`, `pip`, `counseling_1`, `counseling_2`).
8. Giữ `value` của button respond (`accept`, `reject`) và rgm action (`no_repeat`, `set_repeat`, `store_level`, `company_level`).
9. Escape XML: `&` → `&amp;`, `<` → `&lt;`, `>` → `&gt;`.
10. `t-foreach="x" t-as="y"` luôn đầy đủ 2 attr.
11. Dùng `or '---'` cho field optional.
12. `t-if` guard cho record có thể rỗng.

### Bước 7 — Không làm lỗi module khác

- CSS chỉ scope dưới `.o_psm_0215_portal`.
- Inherit template giữ priority + xpath cũ.
- Không thêm dependency mới trong `depends`.
- Không sửa file của module khác.

### Bước 8 — Thứ tự sửa

1. Sidebar inherit (`portal_psm_discipline_sidebar_link`).
2. List page (`portal_psm_my_disciplines`) — wrapper, table, empty state, status badge.
3. Create form (`portal_psm_discipline_create`) — 5 section, giữ input name/id/JS.
4. Detail page (`portal_psm_discipline_explanation_template`) — banner, status badge tiếng Việt, alert palette, action panel.
5. (Tùy chọn) Thêm block RGM action UI — hỏi user trước.
6. Manifest assets + SCSS file (nếu Option A).

### Bước 9 — Sửa lỗi chính tả

- "GỬI PHÀN HỒI &amp; KÝ TÊN" → "GỬI PHẢN HỒI &amp; KÝ TÊN" (button `submit_section_ii` trong `portal_psm_discipline_explanation_template`).

### Bước 10 — Kiểm tra

```bash
# Upgrade
python odoo-bin -d <db_test> -u M02_P0215 --stop-after-init

# Fresh install
python odoo-bin -d <db_test> -i M02_P0215 --stop-after-init

# Với test
python odoo-bin -d <db_test> -u M02_P0215 --test-enable --stop-after-init
```

Docker:
```bash
docker ps
docker exec <odoo_container> odoo -d <db_test> -u M02_P0215 --stop-after-init
docker logs <odoo_container> --tail 200
docker restart <odoo_container>
```

Browser check (desktop 1024px + mobile 360px):
- `/my` → sidebar link vàng McDonald's.
- `/my/disciplines` → table + badge tiếng Việt + empty state + CTA manager.
- `/my/discipline/create` → 5 section + signature mobile + modal validation.
- `/my/discipline/<id>` → banner vàng + status badge tiếng Việt + action panel contextual.
- Mở 1 portal page module khác → UI không đổi (regression).

### Bước 11 — Không được làm

- KHÔNG xóa comment có sẵn (đặc biệt comment tiếng Việt không dấu trong model).
- KHÔNG đổi XML ID/external ID đang dùng.
- KHÔNG đổi route, input field name, model field name, security.
- KHÔNG dùng `t-raw` cho user input.
- KHÔNG chạy destructive command (`drop database`, `reset --hard`, v.v.).
- KHÔNG reset database khi chưa được phép.
- KHÔNG thêm thư viện JavaScript external.
- KHÔNG override CSS global gây leak sang module khác.

### Bước 12 — Sau khi sửa

- Nếu repo có script generator: regenerate `structure/module_map.json`.
- Báo cáo: file đã sửa, file mới (nếu có), risk còn lại.

---

## Files Used For Confirmation

| File | Vai trò trong phân tích |
|---|---|
| `addons/M02_P0215/convention/QUY_UOC_DAT_TEN_VA_RULE.md` | Naming convention (`x_psm_0215_*`, `view_psm_*`, group `M02_P0200.*`), rule ưu tiên dùng sẵn, phân quyền tối thiểu, tách bạch module |
| `addons/M02_P0215/structure/module_map.json` (80 dòng đầu) | Manifest snapshot, counts (`controllers: 2`, `views: 5`, `static: 1`), dependency, data list. Map khớp source thật |
| `addons/M02_P0215/__manifest__.py` | Xác nhận `depends` (9 module), `data` list (14 file), `license = "LGPL-3"`, chưa có key `"assets"` |
| `addons/M02_P0215/controllers/portal.py` | Xác nhận 8 routes portal, contract input field name (POST bodies), security guard `_x_psm_can_view_record` + `_x_psm_can_finalize_record`, role detection `_x_psm_is_manager_employee` |
| `addons/M02_P0215/views/x_psm_portal_templates.xml` | Xác nhận 6 template (982 dòng), markup hiện tại, JS inline (signature pad / preview / validation modal), inline style mix Bootstrap, lỗi chính tả "PHÀN HỒI", gap RGM action UI |
| `addons/M02_P0215/models/x_psm_hr_discipline_record.py` (dòng 1-510) | Xác nhận state machine 12 trạng thái (dòng 379-398), field names, `x_psm_is_accepted`, `x_psm_start_date`/`x_psm_end_date`, help text tiếng Việt không dấu (chủ ý lưu legacy) |
| `addons/M02_P0215/security/security_rules.xml` | Xác nhận record rule portal own (`base.group_portal` read-only), manager rules (SM/RGM/HRBP/OC) scope |
| `addons/M02_P0215/security/ir.model.access.csv` | Xác nhận access portal record (`read=1`, `write/create/unlink=0`) — mọi update phải qua POST controller với `sudo()` |
| `addons/M02_P0215/static/` (Glob check) | Xác nhận chỉ có `static/description/consistency.png`, chưa có `static/src/*` |
