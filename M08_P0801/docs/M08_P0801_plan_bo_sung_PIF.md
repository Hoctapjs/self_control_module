# Plan bổ sung Quy trình 0801 (PIF) — M08_P0801

> **Mục tiêu:** Bổ sung phần **nội dung Product Information Form (PIF)** và các quy tắc SLA/sizing/cấu trúc Parent-Child vào module thực thi hiện có, để 0801 phản ánh đúng nghiệp vụ trong bộ tài liệu gốc (flowchart B1–B14, PIF Form, PIF submit routine & Alignment, cấu trúc Menu component).
>
> **Module đích duy nhất:** `addons/M08_P0801` (canonical). **KHÔNG** đụng vào `addons/RSG_0801_pif_management` (đã bị thay thế — xem cảnh báo trong `__manifest__.py`).
>
> **Nguyên tắc cho agent thực thi:** Mỗi phase là một đơn vị công việc độc lập, làm xong → test cài đặt module → commit → mới sang phase sau. KHÔNG gộp nhiều phase trong một phiên. Mọi field custom đặt prefix `x_psm_0801_` (cho field inherit model gốc) hoặc `x_psm_` (cho model mới của module). Mọi model mới đặt prefix `x_psm_pif_`.

---

## 0. Bối cảnh & hiện trạng (đọc trước khi bắt đầu)

**Cái đã có (execution workflow B6→B14):**
- `x_psm_pif_object` — máy trạng thái 7 bước: `rsg_create → it_config → master_data → lab_test → pilot → valuation → completed` (`models/pif_object.py`).
- `x_psm_pif_data_line` (SSBI/RFM/POS/MDS/UDP key-value), `x_psm_pif_object_raw_line` (raw phẳng), `x_psm_pif_process_tracking` (7 bước), `x_psm_pif_lab_history`.
- Kế thừa `approval.request` / `approval.category` để duyệt B6 → tự sinh PIF object.
- Inherit `product.template` (`x_psm_0801_pif_status`, `_wrin_code`, `_gri_code`, `_pif_product_type`, `_pif_bom_id`), `mrp.bom` (`x_psm_0801_pif_status`).
- 2 sequence: `x_psm_pif_object` (PIF/YYYY/0001), `product.wrin.finished` (FG-YYYY-0001).
- Demo: `M08_P0801_demo` (3 PIF, sản phẩm, BOM, users).

**Cái còn thiếu (so với hình ảnh tài liệu):** xem bảng gap trong phần review. Tóm tắt: toàn bộ **header PIF form** (Program, PMIX, Category LV1–7, product form, platforms, 3 tầng giá, effective date), **cấu trúc Parent/Child component**, **PIF sizing + SLA/working-days**, **routing 5 nguồn B1–B5 + B2A**, **B9 chi tiết + B10 kiểm tra hiển thị**, **lab 2 cấp sign-off**, **B13 API SSBI + B14 QWeb report**, **naming rule PMIX + res.groups**.

**Lệnh test cài đặt module sau mỗi phase (Windows, từ thư mục gốc `d:\odoo-19.0+e.20250918`):**
```
python odoo-bin -c <config> -d <db> -u M08_P0801 --stop-after-init
```
(Hoặc script nâng cấp dự án nếu có. Nếu có demo: `-u M08_P0801,M08_P0801_demo`.) Kiểm tra log không có traceback và view load được.

---

## PHASE 1 — Header PIF Form & phân loại sản phẩm

**Mục tiêu:** Mô hình hóa toàn bộ phần header của Product Information Form (hình "PRODUCT INFORMATION FORM").

**Model sửa:** `x_psm_pif_object` (file `models/pif_object.py`).

**Field cần thêm:**
| Field | Kiểu | Ghi chú |
|---|---|---|
| `x_psm_program` | Char | Tên chương trình PIF (vd "2024 December Offers") |
| `x_psm_initiator_dept` | Many2one `hr.department` | Phòng initiate (đã có owner dept, field này là phòng nguồn yêu cầu) |
| `x_psm_new_code_seq` | Integer | "New Code Required" — số thứ tự mã code |
| `x_psm_menu_item_code` | Char | Product ID (Menu Item Code) — **IT Input**, readonly trừ bước `it_config` |
| `x_psm_pmix_code` | Char | Short Name (PMIX Code), **≤ 7 ký tự** (validate ở Phase 5) |
| `x_psm_product_name_en` | Char | Tên menu Tiếng Anh |
| `x_psm_product_name_vi` | Char | Tên menu Tiếng Việt |
| `x_psm_product_form` | Selection | `alacarte` / `combo` / `meal` |
| `x_psm_menu_type` | Char hoặc Selection | Menu Type (vd Regular) |
| `x_psm_cat_lv1`…`x_psm_cat_lv7` | Char (hoặc Selection nếu có danh mục cố định) | Category LV1–LV7 (Day part, loại hình, hình thức bán, local/core/LTO, khung giá, dinh dưỡng, kích cỡ) |
| `x_psm_target_effective_date` | Date | Target Effective Date |

**Platforms & giá 3 tầng** (theo hình: In-store/VNM, Delivery/MDS-3PO, TSN/Airport):
- `x_psm_platform_ids` — Many2many tới một model danh mục kênh **mới** `x_psm_pif_platform` (records: FC, SOK, DT, WT, McCafe, Digital) HOẶC Selection multi đơn giản. **Khuyến nghị:** tạo model `x_psm_pif_platform` (name, code) + data XML 6 record để mở rộng được.
- `x_psm_price_instore` (Monetary/Float), `x_psm_price_delivery`, `x_psm_price_tsn`, `x_psm_price_other` — 3(+1) tầng giá đề xuất.
- Lưu ý currency: thêm `x_psm_currency_id` (Many2one `res.currency`, default company currency) nếu dùng Monetary.

**View (`views/pif_views.xml`):** Thêm page **"Product Information"** trong notebook của `view_pif_object_form`, nhóm:
- Group "Initiator & Program": program, initiator_dept, new_code_seq, target_effective_date.
- Group "Product Identity": menu_item_code (readonly theo state), pmix_code, product_name_en, product_name_vi, product_form, menu_type.
- Group "Category": cat_lv1…lv7.
- Group "Platforms & Pricing": platform_ids, price_instore, price_delivery, price_tsn, price_other.
- Readonly theo state: phần lớn chỉnh ở `rsg_create`; `menu_item_code` chỉnh ở `it_config`.

**Data:** `data/pif_data.xml` thêm 6 record `x_psm_pif_platform` (nếu chọn model). Đăng ký file mới trong `__manifest__.py` nếu tách file.

**Demo:** `M08_P0801_demo/data/08_pif_objects.xml` — bổ sung các field header cho 3 PIF demo.

**Acceptance:**
- Cài `-u M08_P0801` không lỗi; form PIF hiển thị page "Product Information" đầy đủ.
- Tạo PIF mới điền được header; `menu_item_code` chỉ sửa được ở bước IT.

---

## PHASE 2 — Cấu trúc Parent/Child component (Menu BOM lựa chọn)

**Mục tiêu:** Mô hình hóa phần "Menu components / Thông tin thành phần" (hình 5 & 6): Parent cố định + các nhóm Child lựa chọn, giá 3 tầng từng dòng, cờ Default/Upsize/Upgrade.

**Model mới:** `x_psm_pif_component_line` (trong `models/pif_object.py` hoặc file mới `models/pif_component.py` — nếu file mới nhớ import trong `models/__init__.py`).

**Field:**
| Field | Kiểu | Ghi chú |
|---|---|---|
| `x_psm_pif_object_id` | Many2one `x_psm_pif_object` ondelete cascade | |
| `x_psm_component_type` | Selection | `parent` (mặc định cố định, non-selectable), `bic_flavor`, `side_dish`, `side_dish_special`, `drink`, `drink_special`, `other` |
| `x_psm_product_id` | Many2one `product.product` | Item code thành phần |
| `x_psm_recipe_text` | Char/Text | "Item Parent Recipe" / mô tả công thức (định dạng GRI-GRI Name\|SSBI Qty*Unit) |
| `x_psm_qty` | Float | QTY |
| `x_psm_price_vnm` | Float | Giá VNM |
| `x_psm_price_delivery` | Float | Giá Delivery |
| `x_psm_price_tsn` | Float | Giá TSN |
| `x_psm_is_default` | Boolean | Là lựa chọn mặc định (vd Default Drink) |
| `x_psm_default_size` | Char | Default Size |
| `x_psm_allow_upsize` | Boolean | Allow Upsize? |
| `x_psm_allow_upgrade` | Boolean | Allow Upgrade? (drink) |
| `x_psm_choice_group` | Char | "Specify groups/products" cho upgrade |

**Field thêm trên `x_psm_pif_object`:**
- `x_psm_component_line_ids` — One2many tới `x_psm_pif_component_line`.
- `x_psm_insert_ketchup_chili` — Selection yes/no ("Insert KETCHUP & CHILI SACHET as choice?").

**Onchange:** Khi chọn `x_psm_pif_bom_id`, ngoài việc nạp raw materials (đã có), nạp các dòng BOM thành **component_type = parent** vào `x_psm_component_line_ids` (giữ nguyên `_onchange_pif_bom_id` cũ cho raw, thêm logic cho component). Child do người dùng thêm thủ công.

**View:** Page **"Menu Components"** trên form PIF:
- Section Parent: `x_psm_component_line_ids` filtered `component_type='parent'` + field `x_psm_insert_ketchup_chili`.
- Các section Child (BIC Flavor / Side-Dish / Drink / Other): list editable với QTY + 3 giá + các cờ. Có thể dùng nhiều `<field>` cùng One2many với `domain`/`context` mặc định `component_type`, hoặc 1 list duy nhất có cột `component_type`. **Khuyến nghị** 1 list duy nhất có cột type để đơn giản, kèm group-by type.

**Demo:** thêm vài component line cho PIF demo (1 parent + 1 drink child có Default Coke + upsize).

**Acceptance:** chọn BOM → parent tự nạp; thêm được child drink với default/upsize và 3 giá; cài module không lỗi.

---

## PHASE 3 — PIF Sizing & SLA / Working days

**Mục tiêu:** Mô hình hóa bảng "PIF submit routine & Alignment" + timeline (Build/Test/Backup → Effective).

**Model sửa:** `x_psm_pif_object`.

**Field:**
| Field | Kiểu | Ghi chú |
|---|---|---|
| `x_psm_pif_size` | Selection | `large` / `medium` / `small` / `adhoc` |
| `x_psm_price_tier` | Integer | (Large/Med/Small = 3; Ad-hoc = 1) — có thể compute từ size |
| `x_psm_week_number` | Char | "1st & 3rd" / "2nd & 4th" — compute từ size |
| `x_psm_menu_code_count` | Char | số deals (20 / 10-20 / 4-10 / 1-3) |
| `x_psm_system_code_count` | Integer | Total system code (60/45/21/9) |
| `x_psm_days_build_rfm` | Integer | Build RFM (10/7/2/1) |
| `x_psm_days_test_lab` | Integer | Test LAB (3/2/1/1) |
| `x_psm_days_backup` | Integer | Back up (2/1/1/1) |
| `x_psm_total_working_days` | Integer | compute = build+test+backup (hoặc theo bảng: 15/10/4/3) |
| `x_psm_submit_date` | Date | ngày submit PIF |
| `x_psm_effective_date_calc` | Date | compute: Large/Med/Small = "Next Monday" sau khi đủ working days; Ad-hoc = "After Back-up day" |

**Logic compute:** Tạo dict cấu hình size → (price_tier, week, system_code, build, test, backup, total, effective_rule). Compute các field theo `x_psm_pif_size`. `effective_date_calc`: từ `submit_date` cộng working days (bỏ T7/CN nếu muốn đúng "working day") rồi đẩy tới Monday kế tiếp; Ad-hoc = ngay sau backup.

**View:** Group "PIF Sizing & SLA" trong page Product Information (hoặc page riêng "Planning"): size, các field compute readonly, submit_date, effective_date_calc.

**(Tùy chọn) Deadline tracking:** thêm `x_psm_deadline` per-step nếu muốn cảnh báo trễ — có thể để Phase mở rộng sau, không bắt buộc.

**Acceptance:** chọn size = Large → tự điền 3/1st&3rd/60/10/3/2/15; effective_date_calc ra Thứ Hai kế tiếp hợp lý.

---

## PHASE 4 — Routing 5 nguồn (B1–B5), B2A ảnh, B9 chi tiết, B10 kiểm tra hiển thị

**Mục tiêu:** Phản ánh đúng nhánh flowchart: nguồn yêu cầu khác nhau, B2A (MKT gửi ảnh), B9 setup chi tiết, B10A–D kiểm tra hiển thị.

**4.1 Routing nguồn yêu cầu — ĐÃ CHỐT: Fast-track cho Digital/SC, vẫn tạo PIF:**
- Giữ `x_psm_pif_request_type` (menu/marketing/si/digital/supply_chain) — đã có cả trên `approval.request` và `pif_object`.
- **Menu / MKT / S&I** → qua cổng duyệt B6 như hiện tại → tạo PIF (B7) ở state `rsg_create`.
- **Digital / SC** → **fast-track**: bỏ cổng duyệt thủ công B6 (auto-approve), **vẫn tạo `x_psm_pif_object` với RSG là owner**, nhưng vào thẳng state `it_config` (B8). Mặc định gán `x_psm_pif_size = 'adhoc'` (liên kết Phase 3).
- **Triết lý:** "tiến hành bước 8" = không có cổng phê duyệt thủ công, KHÔNG phải "không có PIF". Giữ **một pipeline duy nhất** `approval.request → x_psm_pif_object` để mọi PIF đều có owner + audit trail.
- **Cách hiện thực (gợi ý):** trong `action_approve()` (hoặc một method tạo request mới), khi `request_type ∈ {digital, supply_chain}`: tự gọi approve ngay (auto-approve) rồi tạo PIF object với `state='it_config'` thay vì `rsg_create`; đồng thời `_complete_step('1_')` để đánh dấu bước RSG-create là done (do hệ thống/fast-track). Với Menu/MKT/S&I giữ nguyên luồng cũ (PIF tạo ở `rsg_create`).
- Lưu ý: vẫn phải đảm bảo các field bắt buộc của bước `rsg_create` (3 ô HTML SSBI/RFM/POS) được xử lý hợp lý cho nhánh fast-track — hoặc nới validate cho nguồn Digital/SC, hoặc cho nhập sau ở bước phù hợp. Quyết định khi code, ưu tiên không chặn cứng luồng nhanh.

**4.2 B2A — ảnh marketing:** Thêm trên `x_psm_pif_object` (hoặc approval.request) các trường đính kèm ảnh: `x_psm_img_pos`, `x_psm_img_sok`, `x_psm_img_dmb`, `x_psm_img_mop` (Binary + filename) hoặc dùng `message_attachment` / `ir.attachment` One2many. Hiển thị khi `request_type='marketing'`.

**4.3 B9 — setup chi tiết (RSG setup / bước master_data):** Thêm checklist sub-task khi ở bước `master_data`:
- Model mới hoặc field Boolean: `x_psm_setup_code_price_store`, `x_psm_setup_udp` (Program/Product/Outage), `x_psm_setup_recipe_ssbi`, `x_psm_setup_rawitem`.
- Trong `action_master_setup()` validate đã tick đủ checklist trước khi chuyển state.

**4.4 B10A–D — kiểm tra hiển thị (display check / sign-off):** Sau setup, các phòng (Menu/MKT/S&I/Digital) xác nhận hiển thị đúng.
- Model mới `x_psm_pif_display_check` (pif_id, department, checked_by, check_date, status pass/fail, note) HOẶC field đơn giản nếu chỉ cần 1 xác nhận.
- View: list các display-check trên page mới "Display Check".

**Acceptance:** request_type=marketing hiển thị ô ảnh B2A; bước master_data yêu cầu tick đủ 4 setup item; có bảng display check.

---

## PHASE 5 — Lab test 2 cấp sign-off + Naming rule PMIX + Constraints

**Mục tiêu:** Lab test theo hình 4 (Initiator test & sign-off → RSG sign-off) và enforce quy tắc đặt tên/dữ liệu bắt buộc.

**5.1 Lab 2 cấp:**
- Thêm field: `x_psm_lab_initiator_signoff` (Boolean) + `x_psm_lab_initiator_user`/`_date`, `x_psm_lab_rsg_signoff` + `_user`/`_date`.
- Sửa `action_finish_lab_test()`: yêu cầu Initiator sign-off trước, rồi RSG sign-off mới cho PASS. Vẫn ghi `x_psm_pif_lab_history`.

**5.2 Naming rule PMIX (`@api.constrains`):**
- `x_psm_pmix_code`: ≤ 7 ký tự; cú pháp theo loại sản phẩm (BIC: `TênCombo_SốLượng_vị`; Combo Digital: `Di` + số). Raise `ValidationError` nếu sai.
- (Tùy chọn) validate `x_psm_menu_item_code` unique.

**5.3 Constraints khác:** chuyển các validate đang nằm rải rác ở action sang `@api.constrains` nơi hợp lý (vd 3 ô HTML, lab note khi fail). Giữ behavior cũ, chỉ chuẩn hóa.

**Acceptance:** nhập PMIX 8 ký tự → báo lỗi; lab cần cả 2 sign-off mới pass.

---

## PHASE 6 — B13 API SSBI + B14 QWeb Valuation Report + Bảo mật & dọn nợ kỹ thuật

**Mục tiêu:** Hoàn thiện đuôi quy trình và nâng chất lượng nền tảng.

**6.1 B14 — PIF Valuation Report (QWeb):**
- Tạo `report/pif_valuation_report.xml` (QWeb template) + `report/pif_report_action.xml` (ir.actions.report) in ra: header PIF, components, giá 3 tầng, WRIN sinh ra, tracking, lab history.
- Thêm nút "Print Valuation Report" trên form. Đăng ký file trong manifest.

**6.2 B13 — API SSBI (stub/connector):**
- Tối thiểu: method `action_push_to_ssbi()` đóng gói dữ liệu PIF thành JSON + log/queue (không cần endpoint thật). Đặt điểm tích hợp rõ ràng (`models/ssbi_connector.py`) để sau nối API thật. Gọi ở bước pilot→valuation.

**6.3 Bảo mật (dọn nợ từ doc mục 16):**
- Tạo `security/pif_groups.xml`: `group_pif_rsg`, `group_pif_it` (và `group_pif_manager`). Thay thế dần logic so chuỗi tên phòng (`'RSG' in name`) bằng `user.has_group(...)` trong `_check_dept_permission`, `_compute_user_can_process_step`, `_compute_is_it_dept/_rsg_dept`.
- Cân nhắc `ir.rule` giới hạn theo phòng/người tạo nếu cần.

**6.4 Dọn nợ kỹ thuật khác:**
- Khai báo `external_dependencies` (`openpyxl`) trong `__manifest__.py`.
- Bỏ hardcode `/mnt/file` trong `action_import_data_from_excel()` → dùng `ir.config_parameter` hoặc field cấu hình đường dẫn / cho upload attachment trực tiếp.
- Xóa nhánh `'Head'` chết trong `_compute_user_can_process_step` (hoặc nối vào logic duyệt thực sự).

**Acceptance:** in được Valuation Report PDF; phân quyền chạy bằng res.groups; cài module sạch, không cảnh báo thiếu dependency.

---

## Thứ tự ưu tiên & phụ thuộc

```
Phase 1 (header)  ─┬─► Phase 3 (sizing, dùng effective_date/price)
                   ├─► Phase 5 (naming rule cần pmix_code từ P1)
Phase 2 (parent/child) ─► Phase 6.1 (report cần components)
Phase 4 (routing/B9/B10)  (độc lập, sau P1)
Phase 6 (report/api/security)  (cuối, sau khi data model ổn định)
```

- **Bắt buộc làm trước:** Phase 1 (nền data header) → các phase còn lại tham chiếu.
- Phase 2, 3, 4 có thể làm song song nhánh sau Phase 1.
- Phase 5 sau Phase 1. Phase 6 làm cuối.

## Checklist chung mỗi phase (Definition of Done)
- [ ] Field/model thêm đúng prefix, có `string` tiếng Việt/Anh rõ ràng.
- [ ] `ir.model.access.csv` cập nhật cho model mới.
- [ ] View cập nhật, readonly theo `state` hợp lý.
- [ ] Demo data (`M08_P0801_demo`) cập nhật minh họa.
- [ ] `__manifest__.py` đăng ký file mới (nếu có).
- [ ] Cài `-u M08_P0801` (và `,M08_P0801_demo`) không traceback, view render được.
- [ ] Cập nhật `docs/M08_P0801_phan_tich_nghiep_vu.md` phần tương ứng (đánh dấu ✅ mục đã làm).
- [ ] Commit riêng theo phase.

## Ghi chú quan trọng
- **Không** cài đồng thời `RSG_0801_pif_management` và `M08_P0801` (trùng model). Mọi thay đổi chỉ vào `M08_P0801`.
- **Routing B4/B5 đã chốt** (xem Phase 4.1): Digital/SC fast-track bỏ cổng duyệt nhưng vẫn tạo PIF, vào thẳng `it_config`, mặc định size Ad-hoc. Không cần hỏi lại.
- Giữ tối đa việc tái sử dụng module gốc (`approvals`, `product`, `mrp`, `mail`, `hr`) thay vì dựng lại.
