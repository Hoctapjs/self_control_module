# Phân tích nghiệp vụ: RSG PIF Management — M08_P0801 (Quy trình 0801 — PIF)

> Tài liệu sinh tự động từ mã nguồn (reverse-engineering) — phản ánh **những gì ĐÃ TRIỂN KHAI** tới thời điểm đọc code.
> Mọi câu trả lời đều có dẫn chứng tới `file : model/field/method`. Phần nào không có trong code đều ghi rõ ❌.
>
> - **Module**: `M08_P0801` — *"RSG PIF Management (0801)"* (version 0.2, author MongTuyen, category *Supply Chain/RSG*)
> - **Phụ thuộc (module gốc tái sử dụng)**: `base`, `mail`, `product`, `mrp`, `approvals`, `hr`
> - **Được mở rộng bởi**: `SC_0402_supplier_management`

---

## 0. Tổng quan & sơ đồ trạng thái

Module hiện thực **phần thực thi (execution) của quy trình PIF** — tức là từ **B6 (duyệt yêu cầu) → B7 (RSG tạo PIF) → ... → B14 (báo cáo PIF)** trong sơ đồ gốc.

Cách hoạt động ở mức cao:

1. Người dùng tạo một **Yêu cầu phê duyệt** (`approval.request`) thuộc danh mục *Product Initiation Form (PIF)*. Loại phòng ban yêu cầu (Menu/MKT/S&I/Digital/Supply Chain) được chọn qua trường `x_psm_pif_request_type` — **không tách thành 5 form riêng** như 5 lane B1–B5 trên sơ đồ.
2. Khi yêu cầu được **duyệt** (B6), hệ thống **tự sinh** một bản ghi thực thi `x_psm_pif_object` (B7) và mở ra luồng 7 bước.
3. `x_psm_pif_object` chạy qua một **máy trạng thái 7 bước** với phân công luân phiên RSG ↔ IT, có nhánh **Lab Test Fail → quay lại IT** (đúng tinh thần B11 "Lab test? NO → bước 8").
4. Khi hoàn tất (`valuation` → `completed`), hệ thống **sinh mã WRIN thành phẩm** cho sản phẩm và đánh dấu BOM/Product `completed`.

### Sơ đồ trạng thái thực tế (`x_psm_pif_object.state`)

```
                       action_approve() (approval.request, category.x_psm_0801_is_pif = True)
[approval.request: được duyệt]  ───────────────────────────────►  tạo x_psm_pif_object (state = rsg_create)

 rsg_create ──action_rsg_create() [RSG; bắt buộc 3 ô HTML SSBI/RFM/POS; import Excel]──► it_config
 it_config  ──action_it_config()    [IT]───────────────────────────────────────────────► master_data
 master_data──action_master_setup() [RSG]──────────────────────────────────────────────► lab_test
 lab_test   ──action_finish_lab_test() == PASS [RSG]───────────────────────────────────► pilot
 lab_test   ──action_finish_lab_test() == FAIL [RSG; reset bước 2..5]──────────────────► it_config   (vòng lặp làm lại)
 pilot      ──action_pilot_deploy()  [IT]──────────────────────────────────────────────► valuation
 valuation  ──action_valuation_report() [RSG; sinh WRIN]───────────────────────────────► completed
```

### Bảng 7 bước theo dõi quy trình (`x_psm_pif_process_tracking`, sinh mặc định)

| x_psm_step_code | Tên bước (x_psm_process_name)                    | Phòng ban (x_psm_department_ref) |
|-----------------|--------------------------------------------------|----------------------------------|
| `1_rsg`         | RSG creates PIF                                  | RSG                              |
| `2_it_config`   | IT config                                        | IT                               |
| `3_master`      | RSG setup                                        | RSG                              |
| `4_lab`         | RSG lab test                                     | RSG                              |
| `5_pilot`       | Pilot/Mass                                       | IT                               |
| `6_val`         | PIF Valuation                                    | RSG                              |
| `7_finish`      | Process Completed - Handover to Sourcing         | System                           |

*Dẫn chứng:* `models/pif_object.py : _get_default_tracking_steps()`, `state` (dòng ~158), các `action_*` (dòng 312–461).

---

## 1. Phạm vi & mục tiêu

**Hỏi:** Module này hiện thực quy trình gì, ranh giới tới đâu?
**Đáp (đã triển khai):** Hiện thực quy trình **PIF (Product Initiation Form)** của phòng RSG — từ lúc yêu cầu được duyệt, qua cấu hình IT, setup master data, kiểm nghiệm (Lab), pilot/mass, định giá (valuation), tới hoàn tất và sinh mã WRIN thành phẩm. Manifest ghi rõ đây là **module nền (base)** cho luồng PIF, dự kiến mở rộng cho các loại PIF khác (Marketing, S&I, Digital, Supply Chain) và được module `SC_0402_supplier_management` kế thừa.
**Dẫn chứng:** `__manifest__.py` (mô tả, depends, version 0.2).
**Trạng thái:** ✅ Đã triển khai (luồng RSG cốt lõi). ⚠️ Các loại PIF khác mới chỉ tồn tại ở dạng trường phân loại `x_psm_pif_request_type`, chưa có nhánh xử lý riêng.

---

## 2. Vai trò & phòng ban

**Hỏi:** Những phòng ban/vai trò nào tham gia và được ánh xạ qua đâu?
**Đáp (đã triển khai):** Quy trình phân vai cho **RSG** và **IT** (luân phiên theo từng bước). **Không tạo `res.groups` riêng cho module**; thay vào đó quyền thao tác từng bước được kiểm soát theo **tên phòng ban của nhân viên** (`hr.employee.department_id.name`) bằng so khớp chuỗi con (ví dụ chứa `'RSG'`, `'IT'`). Bản đồ trạng thái → phòng ban:

| State        | Phòng được phép bấm "Done" |
|--------------|----------------------------|
| `rsg_create` | RSG |
| `it_config`  | IT |
| `master_data`| RSG |
| `lab_test`   | RSG |
| `pilot`      | IT |
| `valuation`  | RSG |

Có nhánh `'Head'` (quản lý trực tiếp / trưởng phòng) trong `_compute_user_can_process_step` nhưng **hiện không state nào dùng tới** nó. Superuser/`base.group_system` được bỏ qua kiểm tra (bypass).
**Dẫn chứng:** `models/pif_object.py : _check_dept_permission()`, `_compute_user_can_process_step()`, `_compute_is_it_dept()`, `_compute_is_rsg_dept()`.
**Trạng thái:** ⚠️ Đã triển khai nhưng **phân quyền dựa trên tên phòng ban dạng chuỗi** (mong manh, phụ thuộc cách đặt tên `hr.department`); chưa dùng nhóm bảo mật Odoo chuẩn.

---

## 3. Đối tượng nghiệp vụ & dữ liệu

**Hỏi:** Các model chính là gì? Cái nào mới, cái nào kế thừa gốc? Master data lấy từ đâu? Quy tắc đánh mã?
**Đáp (đã triển khai):**

*Model mới (custom):*
- `x_psm_pif_object` — bản ghi thực thi PIF (model trung tâm; kế thừa `mail.thread`, `mail.activity.mixin`).
- `x_psm_pif_data_line` — dòng dữ liệu cấu hình hệ thống (category: SSBI/RFM/POS/MDS/UDP/Access/Other + key/value).
- `x_psm_pif_object_raw_line` & `x_psm_pif_request_raw_line` — dòng nguyên liệu (GRI/WRIN/product/quantity/UoM) lần lượt trên PIF object và trên approval request.
- `x_psm_pif_process_tracking` — 7 bước theo dõi tiến trình.
- `x_psm_pif_lab_history` — lịch sử các lần Lab test (kết quả/note/file/người test/thời điểm).

*Model gốc được kế thừa (`_inherit`):*
- `product.template` → thêm `x_psm_0801_pif_status`, `x_psm_0801_pif_product_type` (finished/raw), `x_psm_0801_pif_bom_id`, `x_psm_0801_wrin_code`, `x_psm_0801_gri_code`.
- `mrp.bom` → thêm `x_psm_0801_pif_status`.
- `approval.category` → thêm `x_psm_0801_is_pif`.
- `approval.request` → thêm `x_psm_0801_pif_object_id`, `x_psm_0801_pif_request_type`, `x_psm_0801_pif_product_id`, `x_psm_0801_pif_bom_id`, `x_psm_0801_pif_vendor_id`, `x_psm_0801_raw_item_ids`, ...

*Master data:* sản phẩm/BOM/nguyên liệu lấy từ `product.product`, `product.template`, `mrp.bom` (gốc); nhà cung cấp từ `product.seller_ids`. Dữ liệu cấu hình SSBI/RFM/POS có thể **import từ file Excel**.

*Đánh mã:* `x_psm_pif_object.name` (PIF ID) lấy qua `ir.sequence.next_by_code('x_psm_pif_object')` → định dạng `PIF/YYYY/0001`; WRIN thành phẩm lấy qua `ir.sequence.next_by_code('product.wrin.finished')` → định dạng `FG-YYYY-0001`, fallback `FG-YYYY-<id 4 số>`.
**Dẫn chứng:** `models/pif_object.py`, `models/pif_project.py`, `models/approval_extensions.py : create()`, `_generate_finished_wrin()`; `data/pif_sequence.xml` (2 sequence đã khai báo).
**Trạng thái:** ✅ Model & quan hệ đầy đủ. ✅ Hai `ir.sequence` (`x_psm_pif_object`, `product.wrin.finished`) đã được khai báo trong `data/pif_sequence.xml`.

---

## 4. Vòng đời & trạng thái

**Hỏi:** Liệt kê đầy đủ trạng thái, điều kiện và method chuyển, ai được chuyển?
**Đáp (đã triển khai):** 7 trạng thái: `rsg_create → it_config → master_data → lab_test → pilot → valuation → completed`. Mỗi bước có một nút `action_*` riêng (xem sơ đồ mục 0). Mỗi action gọi `_check_dept_permission()` (chặn sai phòng), cập nhật `state`, đánh dấu bước tracking `done` qua `_complete_step()`, rồi `activity_schedule()` nhắc việc cho phòng kế tiếp. `state` là `readonly` + có `tracking=True` (ghi vào chatter).
**Dẫn chứng:** `models/pif_object.py`: `action_rsg_create` (312), `action_it_config` (336), `action_master_setup` (353), `action_finish_lab_test` (371), `action_pilot_deploy` (436), `action_valuation_report` (453).
**Trạng thái:** ✅ Đã triển khai đầy đủ.

---

## 5. Phê duyệt

**Hỏi:** Có dùng module approvals gốc không? Mấy cấp? Điều kiện? Xử lý từ chối?
**Đáp (đã triển khai):** **Tái sử dụng nguyên module `approvals` gốc của Odoo** cho khâu phê duyệt yêu cầu tạo PIF (B6). Module chỉ thêm cờ `x_psm_0801_is_pif` lên `approval.category` để đánh dấu danh mục PIF. **Số cấp duyệt & người duyệt do cấu hình danh mục approvals quyết định** (không hard-code trong module này). Điểm mấu chốt: override `action_approve()` — khi duyệt một request thuộc danh mục `x_psm_0801_is_pif` mà chưa có PIF, hệ thống **tự tạo `x_psm_pif_object`** và liên kết hai chiều (`x_psm_0801_pif_object_id`).
**Dẫn chứng:** `models/approval_extensions.py : ApprovalCategory.x_psm_0801_is_pif`, `ApprovalRequest.action_approve()`; `data/pif_data.xml` (danh mục *Product Initiation Form (PIF)*).
**Trạng thái:** ✅ Đã triển khai (tận dụng tối đa module gốc). ⚠️ Luồng **từ chối phê duyệt** dùng cơ chế gốc của approvals; module không có xử lý riêng cho refuse.

---

## 6. Quy tắc & ràng buộc nghiệp vụ

**Hỏi:** Có validation, trường bắt buộc, constraint, compute, onchange tự động nào?
**Đáp (đã triển khai):**
- Bắt buộc nhập đủ **3 ô mô tả HTML (SSBI, RFM, POS)** trước khi RSG hoàn tất bước đầu (`action_rsg_create`).
- Lab test: bắt buộc chọn **kết quả Pass/Fail**; nếu Fail thì **bắt buộc nhập ghi chú** lý do.
- `x_psm_pif_bom_id` trên `x_psm_pif_object` là **bắt buộc** và domain chỉ nhận BOM `x_psm_0801_pif_status = 'completed'`.
- `@api.onchange('x_psm_pif_bom_id')` tự nạp danh sách nguyên liệu từ dòng BOM; tương tự `@api.onchange('x_psm_0801_pif_product_id')` trên approval request nạp BOM/vendor/raw items.
- Compute: `_compute_owner_info` (phòng ban/chức danh người yêu cầu), `_compute_from_product` (BOM + vendor theo sản phẩm).
**Dẫn chứng:** `models/pif_object.py : action_rsg_create()`, `action_finish_lab_test()`, field `x_psm_pif_bom_id`, `_onchange_pif_bom_id()`; `models/approval_extensions.py : _onchange_pif_product_id_populate()`.
**Trạng thái:** ✅ Đã triển khai (chủ yếu validate ở tầng action, chưa dùng `@api.constrains`).

---

## 7. Thông báo & nhắc việc

**Hỏi:** Ai nhận thông báo, khi nào, qua kênh gì?
**Đáp (đã triển khai):** Sau mỗi bước, hệ thống tạo **activity "To Do"** (`mail.mail_activity_data_todo`) giao cho **trưởng phòng (manager_id.user_id) của phòng kế tiếp** (IT hoặc RSG), với tiêu đề/nội dung phù hợp (ví dụ "PIF Configuration Required", "Lab Test Required", "Lab Test Failed - Revision Required", "Valuation Report Required"). `x_psm_pif_object` kế thừa `mail.thread`/`mail.activity.mixin` nên có chatter + activity. Khi không tìm thấy file Excel, gửi cảnh báo tức thời qua **`bus.bus`** (notification kiểu danger).
**Dẫn chứng:** `models/pif_object.py`: các lệnh `self.activity_schedule(...)` trong từng action; `action_import_data_from_excel()` (bus.bus); `_inherit = ['mail.thread', 'mail.activity.mixin']`.
**Trạng thái:** ✅ Đã triển khai. ⚠️ Phòng ban được tìm bằng `search` theo tên (`name = 'IT'` / `ilike 'IT %'` / `ilike 'RSG'`); nếu không khớp tên, người nhận fallback về chính người thao tác. ❌ Không dùng email template riêng (chỉ activity in-app).

---

## 8. Chứng từ, tài liệu & báo cáo

**Hỏi:** File đính kèm, import dữ liệu, báo cáo QWeb?
**Đáp (đã triển khai):**
- Thay cho file, RSG nhập **3 mô tả HTML** SSBI/RFM/POS (`x_psm_file_ssbi_html`, `x_psm_file_rfm_html`, `x_psm_file_pos_html`) — hiển thị thành 3 trang notebook.
- **Import Excel**: `action_import_data_from_excel()` đọc file `.xlsx` có chữ "PIF" trong thư mục `/mnt/file` (fallback `file/`), bóc các sheet SSBI/RFM/POS/MDS/UDP thành các dòng `x_psm_pif_data_line` (key/value). Dùng thư viện `openpyxl`.
- **Lab proof**: trường Binary `x_psm_lab_test_proof` + lịch sử file trong `x_psm_pif_lab_history`.
- **Báo cáo**: tái sử dụng **BoM Overview** của `mrp` (smart button gọi `mrp.action_report_mrp_bom`).
**Dẫn chứng:** `models/pif_object.py : action_import_data_from_excel()`, field HTML/Binary; `views/pif_views.xml` (smart button BoM Overview, các page SSBI/RFM/POS/Lab Test).
**Trạng thái:** ⚠️ Đã triển khai nhưng import Excel **phụ thuộc đường dẫn & tên file hardcode**, và `openpyxl` là phụ thuộc ngoài không khai báo trong manifest. ❌ Không có báo cáo QWeb riêng cho "PIF valuation report" (B14) — mới chỉ là chuyển trạng thái + sinh WRIN.

---

## 9. Tích hợp & hệ thống ngoài

**Hỏi:** Có tích hợp API/đồng bộ/đọc file hệ thống ngoài không?
**Đáp (đã triển khai):** Khái niệm các hệ thống ngoài (SSBI, RFM, POS, MDS, UDP) được mô hình hóa **dưới dạng dữ liệu** trong `x_psm_pif_data_line` (phân loại theo `x_psm_category`) và nhập qua Excel — **không có kết nối API thực**. Sơ đồ gốc có B13 *"API SSBI"* và lane *ODOO SYSTEM* nhưng trong code **chưa có client/endpoint API nào**.
**Dẫn chứng:** `models/pif_object.py : PifDataLine.x_psm_category`, `action_import_data_from_excel()` (sheet_map SSBI/RFM/POS/MDS/UDP).
**Trạng thái:** ⚠️ Một phần (chỉ lưu dữ liệu cấu hình). ❌ Không có tích hợp API SSBI thực tế.

---

## 10. Báo cáo, KPI & dashboard

**Hỏi:** Có báo cáo/KPI/dashboard nào?
**Đáp (đã triển khai):** Có **danh sách & theo dõi**: list view `x_psm_pif_object` (badge trạng thái), bảng *Process Tracking* 7 bước trên form, list *System Data*, và mượn *BoM Overview* của `mrp`.
**Dẫn chứng:** `views/pif_views.xml` (`view_pif_object_tree`, page Tracking, `view_pif_data_line_list_v3`).
**Trạng thái:** ⚠️ Có view danh sách/tracking. ❌ Không có dashboard/biểu đồ KPI (graph/pivot) chuyên biệt.

---

## 11. Phân quyền & bảo mật

**Hỏi:** Quyền CRUD theo nhóm, record rule, kiểm soát unlink/sửa?
**Đáp (đã triển khai):**
- `ir.model.access.csv`: tất cả model custom (`x_psm_pif_object`, `x_psm_pif_data_line`, `x_psm_pif_process_tracking`, `x_psm_pif_request_raw_line`, `x_psm_pif_object_raw_line`, `x_psm_pif_lab_history`) mở **CRUD đầy đủ cho `base.group_user`**. `mrp.bom` & `mrp.bom.line` chỉ cấp **read** cho `base.group_user`.
- **Không có record rule** (`ir.rule`) nào → mọi người dùng nội bộ thấy toàn bộ bản ghi.
- Chặn xóa: `x_psm_pif_object.unlink()` chỉ cho superuser/`base.group_system`; người khác bị `UserError` (hướng dẫn dùng Refuse/Cancel).
- Kiểm soát chỉnh sửa theo bước: các field nhập liệu trên form đặt `readonly` theo `state` (ví dụ HTML chỉ sửa ở `rsg_create`, lab chỉ ở `lab_test`).
**Dẫn chứng:** `security/ir.model.access.csv`; `models/pif_object.py : unlink()`; `views/pif_views.xml` (các `readonly="state != ..."`).
**Trạng thái:** ⚠️ Đã có quyền CRUD cơ bản + chặn xóa; **thiếu nhóm bảo mật riêng và record rule** (kiểm soát thao tác chủ yếu dựa vào logic phòng ban trong Python + readonly ở view).

---

## 12. Khối lượng & hiệu năng

**Hỏi:** Có dấu hiệu xử lý khối lượng/hiệu năng trong code?
**Đáp (đã triển khai):** `x_psm_pif_object.name` đặt `index=True`. Các trường tổng hợp người yêu cầu (`x_psm_request_owner_department_id`/`x_psm_request_owner_job_id`) dùng `store=True` (giảm tính lại). `create` dùng `@api.model_create_multi`. Import Excel mở workbook ở chế độ `read_only=True, data_only=True`.
**Dẫn chứng:** `models/pif_object.py`: field `name` (48), `_compute_owner_info` (store), `create()` (253), `action_import_data_from_excel()`.
**Trạng thái:** ✅ Có một số tối ưu cơ bản; chưa có xử lý batch/khối lượng lớn đặc thù.

---

## 13. Ngoại lệ & xử lý lỗi

**Hỏi:** Luồng fail/làm lại, hủy, reset bước, raise lỗi gì?
**Đáp (đã triển khai):**
- **Lab Test FAIL**: ghi lịch sử, **đưa trạng thái quay lại `it_config`**, reset 4 bước tracking (`2_it_config`, `3_master`, `4_lab`, `5_pilot`) về `pending`, và nhắc IT chỉnh sửa — đúng vòng "làm lại" của sơ đồ (B11 NO → B8).
- Mọi lần test (Pass lẫn Fail) đều **ghi lịch sử** vào `x_psm_pif_lab_history`.
- Chặn sai phòng: `AccessError`; thiếu dữ liệu bắt buộc: `ValidationError`; xóa không phép: `UserError`.
- Không tìm thấy file Excel: cảnh báo qua `bus.bus`, không chặn cứng.
**Dẫn chứng:** `models/pif_object.py : action_finish_lab_test()` (371–434), `_check_dept_permission()`, `unlink()`.
**Trạng thái:** ✅ Đã triển khai luồng làm lại & xử lý lỗi. ❌ Không có hành động "Hủy/Cancel" riêng (chỉ gợi ý trong thông báo lỗi unlink).

---

## 14. Dữ liệu & di trú

**Hỏi:** Có dữ liệu mặc định/demo/import nào?
**Đáp (đã triển khai):** `data/pif_data.xml` (`noupdate="1"`) tạo sẵn **một danh mục approvals** *"Product Initiation Form (PIF)"* với `x_psm_0801_is_pif=True`. `data/pif_sequence.xml` (`noupdate="1"`) khai báo 2 sequence. Dữ liệu nghiệp vụ (SSBI/RFM/POS...) di trú qua **import Excel** lúc chạy. Dữ liệu mẫu đầy đủ (3 PIF, 12 sản phẩm, 3 BOM, 8 users/employees) được cung cấp bởi module `M08_P0801_demo`.
**Dẫn chứng:** `data/pif_data.xml`; `data/pif_sequence.xml`; `action_import_data_from_excel()`; `addons/M08_P0801_demo/`.
**Trạng thái:** ✅ Đã triển khai đầy đủ.

---

## 15. Bảng ánh xạ: Module gốc tái sử dụng vs Custom

| Hạng mục nghiệp vụ            | Dùng module gốc                                   | Phần custom của M08_P0801 |
|------------------------------|---------------------------------------------------|---------------------------|
| Phê duyệt yêu cầu (B6)       | ✅ `approvals` (category, request, action_approve) | Cờ `x_psm_0801_is_pif`, tự sinh `x_psm_pif_object` khi duyệt |
| Sản phẩm / WRIN / GRI        | ✅ `product` (`product.template`/`product.product`) | `x_psm_0801_pif_status`, `x_psm_0801_wrin_code`, `x_psm_0801_gri_code`, `x_psm_0801_pif_product_type` |
| Công thức / nguyên liệu      | ✅ `mrp` (`mrp.bom`, `mrp.bom.line`, BoM Overview) | `x_psm_0801_pif_status` trên BOM, raw line, auto-nạp từ BOM |
| Chatter / nhắc việc          | ✅ `mail` (`mail.thread`, `mail.activity.mixin`)   | Activity theo từng bước, bus notification |
| Nhân sự / phòng ban          | ✅ `hr` (`hr.employee`, `hr.department`, `hr.job`)  | Phân quyền theo tên phòng ban |
| Máy trạng thái PIF (B7–B14)  | —                                                 | ✅ `x_psm_pif_object` + 7 bước tracking + lab history |
| Dữ liệu hệ thống SSBI/RFM/POS| —                                                 | ✅ `x_psm_pif_data_line` + import Excel |

---

## 16. Khoảng trống / TODO phát hiện trong code

1. ✅ ~~**Thiếu khai báo `ir.sequence`**~~ — Đã bổ sung `data/pif_sequence.xml` với 2 sequence (`x_psm_pif_object` → `PIF/YYYY/0001`; `product.wrin.finished` → `FG-YYYY-0001`). PIF ID và WRIN giờ được sinh đúng format.
2. ⚠️ **Phân quyền theo tên phòng ban dạng chuỗi** (`'RSG' in name`, `'IT' in name`): dễ vỡ nếu đổi cách đặt tên `hr.department`. Cân nhắc dùng `res.groups`/`hr.department` tham chiếu cứng qua XML id.
3. ⚠️ **Import Excel hardcode** đường dẫn `/mnt/file` và quy ước tên file chứa "PIF"; `openpyxl` **không khai báo trong manifest/`external_dependencies`**.
4. ❌ **B13 "API SSBI" chưa hiện thực** — chỉ lưu dữ liệu, không có kết nối thực.
5. ❌ **B14 "PIF valuation report" chưa có báo cáo QWeb** — mới dừng ở chuyển trạng thái + sinh WRIN.
6. ⚠️ **Không có record rule**: mọi nội bộ thấy toàn bộ PIF; cân nhắc giới hạn theo phòng ban/người tạo nếu cần.
7. ⚠️ **5 lane yêu cầu B1–B5** (Menu/MKT/S&I/Digital/SC) gộp thành 1 trường `x_psm_pif_request_type`, chưa có xử lý khác biệt theo từng nguồn.
8. ⚠️ Nhánh **`'Head'`** trong `_compute_user_can_process_step` được viết nhưng không state nào dùng (code chết tiềm năng).

---

### Phụ lục — Các file đã đọc để kết luận

- `addons/M08_P0801/__manifest__.py`
- `addons/M08_P0801/models/__init__.py`
- `addons/M08_P0801/models/pif_object.py`
- `addons/M08_P0801/models/pif_project.py`
- `addons/M08_P0801/models/approval_extensions.py`
- `addons/M08_P0801/security/ir.model.access.csv`
- `addons/M08_P0801/data/pif_data.xml`
- `addons/M08_P0801/data/pif_sequence.xml`
- `addons/M08_P0801/views/pif_views.xml`

---

## Phase 1 update - Header PIF Form & product classification

**Trang thai:** Da trien khai theo plan `M08_P0801_plan_bo_sung_PIF.md` Phase 1.

**Noi dung da bo sung trong code:**

- `models/pif_object.py`: them header fields tren `x_psm_pif_object` cho Program, Initiator Department, New Code Required, Product ID/Menu Item Code, PMIX, ten san pham EN/VI, Product Form, Menu Type, Category LV1-LV7, Target Effective Date, Platforms va Pricing.
- `models/pif_object.py`: them model danh muc `x_psm_pif_platform` voi `name`, `code`, `sequence`, `active` va unique constraint theo `code`.
- `data/pif_data.xml`: them 6 platform mac dinh `FC`, `SOK`, `DT`, `WT`, `MCCAFE`, `DIGITAL`.
- `views/pif_views.xml`: them tab `Product Information`; cac field header chinh chi sua o `rsg_create`, rieng `Product ID / Menu Item Code` chi sua o `it_config`.
- `security/ir.model.access.csv`: them access cho `x_psm_pif_platform`.
- `addons/M08_P0801_demo/data/08_pif_objects.xml`: cap nhat 3 PIF demo voi header, category, platform va pricing mau.

**Source dung de xac nhan:** `__manifest__.py`, `models/pif_object.py`, `views/pif_views.xml`, `data/pif_data.xml`, `security/ir.model.access.csv`, `addons/M08_P0801_demo/data/08_pif_objects.xml`.

---

## Phase 2 update - Parent/Child component

**Trang thai:** Da trien khai theo plan `M08_P0801_plan_bo_sung_PIF.md` Phase 2.

**Noi dung da bo sung trong code:**

- `models/pif_object.py`: them field `x_psm_component_line_ids` va `x_psm_insert_ketchup_chili` tren `x_psm_pif_object`.
- `models/pif_object.py`: them model `x_psm_pif_component_line` de luu parent/child component, QTY, 3 tang gia, default size, default/upsize/upgrade va choice group.
- `models/pif_object.py`: mo rong `_onchange_pif_bom_id()` de khi chon BOM se nap dong BOM thanh component `parent`, song song voi raw material line da co.
- `views/pif_views.xml`: them tab `Menu Components` tren form PIF, gom co KETCHUP/CHILI va danh sach component editable theo state.
- `security/ir.model.access.csv`: them access cho `x_psm_pif_component_line`.
- `addons/M08_P0801_demo/data/08_pif_objects.xml`: bo sung component demo cho 3 PIF, gom parent line va child drink/side-dish co default/upsize/upgrade minh hoa.

**Source dung de xac nhan:** `models/pif_object.py`, `views/pif_views.xml`, `security/ir.model.access.csv`, `addons/M08_P0801_demo/data/08_pif_objects.xml`.

---

## Phase 3 update - PIF Sizing & SLA / Working days

**Trang thai:** Da trien khai theo plan `M08_P0801_plan_bo_sung_PIF.md` Phase 3.

**Noi dung da bo sung trong code:**

- `models/pif_object.py`: them `x_psm_pif_size`, `x_psm_submit_date` va cac field compute SLA: `x_psm_price_tier`, `x_psm_week_number`, `x_psm_menu_code_count`, `x_psm_system_code_count`, `x_psm_days_build_rfm`, `x_psm_days_test_lab`, `x_psm_days_backup`, `x_psm_total_working_days`, `x_psm_effective_date_calc`.
- `models/pif_object.py`: them bang cau hinh size `large/medium/small/adhoc` theo price tier, week number, menu/system code count va so ngay Build/Test/Backup.
- `models/pif_object.py`: them helper cong working days bo qua Thu Bay/Chu Nhat; Large/Medium/Small day effective duoc day toi Monday gan nhat sau khi du working days, Ad-hoc dung ngay sau backup working days.
- `views/pif_views.xml`: them group `PIF Sizing & SLA` trong tab `Product Information`, size/submit date sua o `rsg_create`, cac field SLA readonly compute.
- `addons/M08_P0801_demo/data/08_pif_objects.xml`: bo sung size va submit date mau cho 3 PIF demo.

**Source dung de xac nhan:** `models/pif_object.py`, `views/pif_views.xml`, `addons/M08_P0801_demo/data/08_pif_objects.xml`.

---

## Phase 6 update - SSBI stub, valuation report, security & technical cleanup

**Trang thai:** Da trien khai theo plan `M08_P0801_plan_bo_sung_PIF.md` Phase 6.

**Noi dung da bo sung trong code:**

- `report/pif_report_action.xml` va `report/pif_valuation_report.xml`: them report PDF `PIF Valuation Report`, in header PIF, pricing, platforms, components, tracking va lab history.
- `views/pif_views.xml`: them nut `Print Valuation Report` tren form PIF khi o state `valuation/completed`.
- `models/ssbi_connector.py`: them stub `action_push_to_ssbi()` de dong goi payload JSON tu PIF, component, pricing, platform va luu vao `x_psm_ssbi_payload_json`; gan status `queued` va ghi chatter.
- `models/ssbi_connector.py`: override `action_pilot_deploy()` de tu goi `action_push_to_ssbi()` khi chuyen `pilot -> valuation`.
- `views/pif_views.xml`: them nut `Push SSBI` va tab `SSBI Integration` de xem payload/status.
- `security/pif_groups.xml`: them cac group `group_pif_rsg`, `group_pif_it`, `group_pif_manager`.
- `models/pif_object.py`: cap nhat `_check_dept_permission()`, `_compute_user_can_process_step()`, `_compute_is_it_dept()`, `_compute_is_rsg_dept()` de uu tien `res.groups`, van giu fallback ten phong ban cho du lieu/demo cu.
- `models/pif_object.py`: bo nhanh `Head` chet trong `_compute_user_can_process_step()`.
- `__manifest__.py`: khai bao `external_dependencies` cho `openpyxl` va dang ky cac file security/report moi.
- `models/pif_object.py` + `data/pif_data.xml`: chuyen duong dan import Excel sang config parameter `m08_p0801.pif_import_dir`, default `/mnt/file`, co fallback `file/`.

**Source dung de xac nhan:** `__manifest__.py`, `models/__init__.py`, `models/pif_object.py`, `models/ssbi_connector.py`, `security/pif_groups.xml`, `report/pif_report_action.xml`, `report/pif_valuation_report.xml`, `views/pif_views.xml`, `data/pif_data.xml`.

---

## Hotfix - PIF category flag, SLA week mapping, optional BOM

**Trang thai:** Da sua cac loi sau Phase 6.

- `data/pif_data.xml`: sua field danh muc approval tu `is_pif` sang dung field that `x_psm_0801_is_pif`, tranh loi load data `Invalid field 'is_pif' on model 'approval.category'`.
- `models/pif_object.py`: sua `week_number` theo bang PIF submit routine: Large/Medium/Small = `1st & 3rd`, Ad-hoc = `2nd & 4th`.
- `models/pif_object.py`: go bo `required=True` tren `x_psm_pif_bom_id` de nhánh Digital/SC fast-track co the tao PIF khi request chua co product/BOM; khi co BOM, onchange/raw/component van hoat dong nhu cu.

---

## Phase 4 update - Routing, B2A images, B9 setup, B10 display check

**Trang thai:** Da trien khai theo plan `M08_P0801_plan_bo_sung_PIF.md` Phase 4.

**Noi dung da bo sung trong code:**

- `models/approval_extensions.py`: bo sung fast-track cho request type `digital` va `supply_chain` khi confirm/approve PIF request; van tao `x_psm_pif_object`, gan state `it_config`, gan size `adhoc`, va danh dau step `1_rsg` la done.
- `models/approval_extensions.py`: truyen `x_psm_pif_bom_id` tu approval request sang PIF object khi tao PIF, de dong bo voi field BOM bat buoc tren PIF object.
- `models/pif_object.py`: them cac field anh marketing B2A `x_psm_img_pos`, `x_psm_img_sok`, `x_psm_img_dmb`, `x_psm_img_mop` va filename tuong ung.
- `models/pif_object.py`: them checklist B9 `x_psm_setup_code_price_store`, `x_psm_setup_udp`, `x_psm_setup_recipe_ssbi`, `x_psm_setup_rawitem`; `action_master_setup()` bat buoc tick du 4 muc truoc khi qua `lab_test`.
- `models/pif_object.py`: them model `x_psm_pif_display_check` va One2many `x_psm_display_check_ids` de luu department, checked by, check date, pass/fail va note cho B10.
- `views/pif_views.xml`: them page `Marketing Images`, `Master Setup`, `Display Check` tren form PIF.
- `security/ir.model.access.csv`: them access cho `x_psm_pif_display_check`.
- `addons/M08_P0801_demo/data/08_pif_objects.xml`: bo sung filename anh marketing, checklist setup va display check mau cho PIF demo da qua B9/B10.

**Source dung de xac nhan:** `models/approval_extensions.py`, `models/pif_object.py`, `views/pif_views.xml`, `security/ir.model.access.csv`, `addons/M08_P0801_demo/data/08_pif_objects.xml`.

---

## Phase 5 update - Lab sign-off & PMIX constraints

**Trang thai:** Da trien khai theo plan `M08_P0801_plan_bo_sung_PIF.md` Phase 5.

**Noi dung da bo sung trong code:**

- `models/pif_object.py`: them 2 cap sign-off Lab Test: `x_psm_lab_initiator_signoff` + user/date va `x_psm_lab_rsg_signoff` + user/date.
- `models/pif_object.py`: them action `action_lab_initiator_signoff()` va `action_lab_rsg_signoff()`; RSG sign-off van kiem tra quyen phong RSG theo logic hien co.
- `models/pif_object.py`: sua `action_finish_lab_test()` de PASS bat buoc co ca Initiator sign-off va RSG sign-off; FAIL bat buoc co note truoc khi ghi history/quay lai IT.
- `models/pif_object.py`: them constraint PMIX `x_psm_pmix_code` khong qua 7 ky tu; voi Digital Combo thi bat buoc format `Di` + so.
- `models/pif_object.py`: them constraint optional cho `x_psm_menu_item_code` unique khi co gia tri.
- `views/pif_views.xml`: them nhom `Lab Sign-off` trong tab `Lab Test`, gom 2 nut sign-off va thong tin user/date.
- `addons/M08_P0801_demo/data/08_pif_objects.xml`: bo sung du lieu sign-off mau cho PIF completed.

**Source dung de xac nhan:** `models/pif_object.py`, `views/pif_views.xml`, `addons/M08_P0801_demo/data/08_pif_objects.xml`.
