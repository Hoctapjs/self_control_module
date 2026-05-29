# Prompt Rà Soát Và Triển Khai UI/UX Module 0502 Cho Codex

## Mục Đích

Tài liệu này là prompt tiếng Việt có dấu để Codex dùng khi thực hiện rà soát, chỉ ra lỗi tiềm ẩn, xác định phần chưa hoàn thành, cải thiện UI/UX và triển khai từng bước cho module Odoo `M02_P0502`.

Phạm vi chính:

- Module: `addons/M02_P0502`
- Nghiệp vụ: quản lý bảo trì / sửa chữa máy móc, kế thừa quy trình chuẩn của Odoo Maintenance, Field Service, Stock, Purchase.
- Mục tiêu: làm cho người dùng sử dụng quy trình tự nhiên hơn, ít mệt mỏi hơn, ít bị rơi vào trạng thái không biết phải làm gì tiếp theo.
- Ràng buộc chính: mọi chỉnh sửa phải không làm lỗi các phần module 0502 đã triển khai và không làm lỗi module khác khi cài đặt hoặc nâng cấp.

---

# Prompt Cho Codex Executor

## Role

Bạn là Codex, đóng vai trò Senior Odoo Architect + Senior Odoo Engineer + UX Reviewer có kinh nghiệm với Odoo 19, `maintenance`, `industry_fsm`, `stock`, `purchase`, `purchase_stock`, `hr`, XML view inheritance, ORM, action method, cron, security/access, workflow UX và kiểm thử install/upgrade module.

Nhiệm vụ của bạn là **đọc source code hiện tại của module `addons/M02_P0502`, rà soát toàn diện, chỉ ra các lỗi tiềm ẩn, các phần chưa hoàn thành, các điểm bất hợp lý trong thao tác của người dùng, sau đó lập plan và triển khai chỉnh sửa từng bước**.

Mục tiêu cuối cùng:

- Quy trình 0502 dễ dùng hơn.
- Form/list/search/action rõ hơn.
- Người dùng biết đang ở bước nào, thiếu gì, cần làm gì tiếp theo.
- Giảm số lần bấm nút vô nghĩa chỉ để ghi dấu vết.
- Giảm trạng thái treo giữa các module `maintenance`, `project.task`, `stock.picking`, `purchase.order`.
- Không phá logic đã có.
- Không phá dữ liệu cũ.
- Không phá install/upgrade module.
- Không ảnh hưởng module khác.

## Nguyên Tắc Bắt Buộc Trước Khi Làm

Trước khi phân tích sâu, sửa code, review hoặc kết luận, bắt buộc đọc:

- `addons/M02_P0502/convention/QUY_UOC_DAT_TEN_VA_RULE.md`
- `addons/M02_P0502/structure/module_map.json`

Nếu cần, đọc thêm:

- `addons/M02_P0502/structure/module_map_stats.json`
- các file trong `addons/M02_P0502/structure/details/` đúng thành phần liên quan
- các file notes có liên quan trong `addons/M02_P0502/notes/`

Không bắt đầu bằng việc đọc mò toàn bộ source nếu `convention` và `structure` đã có. Dùng `module_map.json` để định hướng trước, sau đó mở đúng source cần xác nhận.

Nếu JSON map khác source code hiện tại, ưu tiên source code thật và ghi rõ JSON map cần regenerate.

## Convention Phải Tuân Thủ

Từ file convention của module:

- Không đổi tên model gốc.
- Field mới bổ sung vào model gốc phải dùng prefix:
  - `x_psm_0502_tenfield`
- Model mới nếu thật sự cần tạo thì dùng:
  - `x_psm_<ten_model>`
- Field mới trong model mới dùng:
  - `x_psm_tenfield`
- Action mới dùng:
  - `action_psm_...`
- View mới dùng:
  - `view_psm_...`
- Ưu tiên dùng model, field, action, view, module có sẵn của Odoo.
- Phân quyền tối thiểu.
- Tách bạch rõ ràng giữa các module.
- Không tạo logic chồng chéo hoặc đặt sai module.
- Không tự ý xóa comment có sẵn, đặc biệt comment tiếng Việt không dấu hoặc comment nghiệp vụ.

## Project Context

Module chính:

- `addons/M02_P0502`
- Manifest name: `M02_P0502_QUAN_LY_BAO_TRI`
- Summary: phase foundation cho quy trình bảo trì.

Dependencies hiện có:

- `maintenance`
- `hr`
- `industry_fsm`
- `stock`
- `purchase`
- `purchase_stock`

Module hiện không có controller riêng theo `module_map.json`. UI hiện tại chủ yếu là backend Odoo views kế thừa các model chuẩn.

Các model liên quan:

- `maintenance.request`
- `maintenance.equipment`
- `hr.department`
- `project.task`
- `stock.picking`
- `purchase.order`
- `x_psm_request_source`
- `x_psm_request_type`

Các object trung tâm:

- `maintenance.request`: trục chính của quy trình 0502.
- `project.task`: FSM task dùng cho thực thi.
- `stock.picking`: xuất vật tư nội bộ.
- `purchase.order`: mua ngoài / RFQ / PO.
- `maintenance.equipment`: thiết bị và lịch preventive.

## File Bắt Buộc Đọc Và Xác Nhận

### Định hướng

- `addons/M02_P0502/convention/QUY_UOC_DAT_TEN_VA_RULE.md`
- `addons/M02_P0502/structure/module_map.json`

### Manifest / Init

- `addons/M02_P0502/__manifest__.py`
- `addons/M02_P0502/__init__.py`
- `addons/M02_P0502/models/__init__.py`

### Models

- `addons/M02_P0502/models/maintenance_request.py`
- `addons/M02_P0502/models/maintenance_equipment.py`
- `addons/M02_P0502/models/hr_department.py`
- `addons/M02_P0502/models/project_task.py`
- `addons/M02_P0502/models/stock_picking.py`
- `addons/M02_P0502/models/purchase_order.py`
- `addons/M02_P0502/models/request_source.py`
- `addons/M02_P0502/models/request_type.py`

### Views

- `addons/M02_P0502/views/maintenance_request_views.xml`
- `addons/M02_P0502/views/maintenance_equipment_views.xml`
- `addons/M02_P0502/views/hr_department_views.xml`
- `addons/M02_P0502/views/project_task_views.xml`
- `addons/M02_P0502/views/stock_picking_views.xml`
- `addons/M02_P0502/views/purchase_order_views.xml`

### Data / Security

- `addons/M02_P0502/security/ir.model.access.csv`
- `addons/M02_P0502/data/ir_cron_data.xml`
- `addons/M02_P0502/data/request_source_data.xml`
- `addons/M02_P0502/data/request_type_data.xml`

### Notes Nên Đọc Khi Rà Soát

- `addons/M02_P0502/notes/phase_1_ke_hoach_chi_tiet_theo_tung_buoc.md`
- `addons/M02_P0502/notes/phase_1_da_trien_khai.md`
- `addons/M02_P0502/notes/phase_2_ke_hoach_chi_tiet_theo_tung_buoc.md`
- `addons/M02_P0502/notes/plan_trien_khai_0502_theo_phase.md`
- `addons/M02_P0502/notes/dac_ta_nghiep_vu_0502_bao_tri_sua_chua_may_moc.md`
- `addons/M02_P0502/notes/bang_doi_chieu_cau_hoi_0502_voi_module_chuan_odoo.md`
- `addons/M02_P0502/notes/tong_hop_module_lien_quan_0502.md`

## Những Điểm Cần Rà Soát Kỹ

### 1. Rà soát lỗi tiềm ẩn kỹ thuật

Kiểm tra các nhóm lỗi sau:

- Method được gọi bởi button trong XML có thật sự tồn tại trong model không.
- Field dùng trong view có thật sự tồn tại trong model không.
- `invisible`, `readonly`, `required`, domain, context có hợp lệ với Odoo 19 không.
- XML view inheritance có xpath ổn định không.
- Action/menu trong XML có `id`, `res_model`, `domain`, `context` đúng không.
- Data XML có external id ổn định không.
- Cron gọi method tồn tại và domain an toàn không.
- Access CSV có model id đúng không.
- Không có field required mới làm hỏng tạo record chuẩn của Odoo.
- Không có override làm ảnh hưởng toàn bộ model chuẩn ngoài phạm vi 0502.
- Không có action method dùng `ensure_one()` sai chỗ khi có multi-record.
- Không có `UserError` thiếu thông tin khiến người dùng không biết phải sửa field nào.
- Không có compute field thiếu dependency.
- Không có related field gây lỗi khi record liên quan rỗng.
- Không có create/write/action tạo object liên kết trùng lặp không kiểm soát.
- Không có stock/purchase/FSM action tạo record mới mỗi lần bấm thay vì mở record cũ.
- Không có trạng thái treo: đã bấm bước trước nhưng không thể bấm bước tiếp theo vì điều kiện invisible/validation mâu thuẫn.

### 2. Rà soát lỗi tiềm ẩn khi install/upgrade

Kiểm tra:

- `python odoo-bin -d <db_test> -i M02_P0502 --stop-after-init`
- `python odoo-bin -d <db_test> -u M02_P0502 --stop-after-init`
- Không lỗi external id.
- Không lỗi view xpath.
- Không lỗi field not found.
- Không lỗi model not found.
- Không lỗi access rights.
- Không lỗi import Python.
- Không lỗi data load order.
- Không lỗi cron method missing.
- Không lỗi dependency thiếu trong manifest.

Nếu chạy bằng Docker, dùng lệnh tương đương theo môi trường hiện tại. Không reset database nếu chưa được phép.

### 3. Rà soát phần chưa hoàn thành

Đọc các note phase và source để xác định:

- Bước nào mới chỉ ghi dấu vết bằng field/time/user nhưng chưa tạo object vận hành thật.
- Bước nào có button nhưng chưa có artifact đủ dùng.
- Bước nào chỉ có note text, chưa có cấu trúc dữ liệu rõ.
- Bước nào chưa có view/search/filter phù hợp.
- Bước nào chưa có smart button để mở object liên quan.
- Bước nào chưa có action quay lại object gốc.
- Bước nào chưa có queue theo vai trò.
- Bước nào chưa có hướng dẫn dữ liệu thiếu.
- Bước nào chưa có validation đủ cụ thể.
- Bước nào cần wizard để giảm sai sót thay vì bắt người dùng tự điền nhiều field.
- Bước nào có thể tận dụng Odoo chuẩn tốt hơn thay vì custom thêm.

### 4. Rà soát UI hiện tại

Tập trung vào `views/maintenance_request_views.xml` trước.

Các vấn đề cần kiểm tra:

- Header có quá nhiều button không.
- Button có tên kỹ thuật hoặc tiếng Anh/Việt lẫn lộn gây khó hiểu không.
- Nút chính ở từng giai đoạn có nổi bật không.
- Người dùng có biết bước hiện tại là gì không.
- Người dùng có biết bước tiếp theo là gì không.
- Các field có nhóm theo nghiệp vụ tự nhiên không.
- Có quá nhiều field audit/time/user làm rối form không.
- Field readonly/audit nên nằm tab riêng hay group riêng không.
- Có thông tin thiếu nhưng bị ẩn ở chỗ khó thấy không.
- List view có đủ cột để điều phối không.
- Search view có filter/group by theo vai trò, trạng thái, SLA, loại yêu cầu, nguồn, phòng ban, thiết bị không.
- Các view liên kết `project.task`, `stock.picking`, `purchase.order` có hiển thị link về maintenance request đủ rõ không.
- Giao diện có khiến user phải nhớ quá nhiều quy tắc thủ công không.

### 5. Rà soát UX quy trình người dùng

Rà soát theo luồng thực tế, không chỉ theo code:

1. Cửa hàng hoặc hệ thống phát sinh nhu cầu bảo trì.
2. Tạo maintenance request.
3. CMT tiếp nhận.
4. Kiểm tra thực tế ban đầu.
5. Kiểm tra preventive schedule nếu là bảo trì định kỳ.
6. Thông báo hoặc phân công CMT Lead.
7. Lập kế hoạch xử lý.
8. Tạo FSM task.
9. Thực thi sửa chữa/bảo trì.
10. Ghi nhận hoàn thành thực thi.
11. Nghiệm thu hoặc đánh giá sau bảo trì.
12. Nếu cần đề xuất chi phí/timeline thì lập proposal.
13. Submit/approve/reject proposal.
14. Xác định xử lý nội bộ hay thuê ngoài.
15. Nếu cần vật tư thì kiểm tra vật tư.
16. Tạo stock picking nếu xuất kho nội bộ.
17. Check tồn kho.
18. Submit/approve material request.
19. Validate stock picking.
20. Nếu thiếu hàng thì tạo RFQ/PO.
21. Theo dõi đến khi request hoàn tất/đóng.

Với mỗi bước, chỉ ra:

- Ai là người thao tác.
- Người đó đang ở màn hình nào.
- Người đó cần thấy thông tin gì.
- Người đó cần bấm nút nào.
- Điều kiện nào làm nút xuất hiện.
- Nếu thiếu dữ liệu thì thông báo hiện ra có đủ cụ thể không.
- Sau khi bấm xong, hệ thống đưa người dùng đi đâu.
- Có tạo object liên quan không.
- Có cách mở lại object liên quan không.
- Có điểm nào gây khó chịu, mệt mỏi, phải đoán, phải nhớ, phải nhập lại không.

## Mục Tiêu UI/UX Cần Đề Xuất Và Triển Khai

### 1. Làm rõ trạng thái quy trình

Đề xuất và triển khai nếu an toàn:

- Field/status computed thể hiện bước hiện tại bằng ngôn ngữ nghiệp vụ.
- Nhóm field “Tình trạng hiện tại”.
- Nhóm field “Việc cần làm tiếp theo”.
- Warning/readonly reason khi chưa đủ điều kiện bấm bước tiếp theo.
- Search filter cho queue theo bước.

Không tạo workflow engine mới nếu chưa cần. Ưu tiên compute field và view grouping.

### 2. Giảm header button overload

Nếu header đang có quá nhiều button:

- Giữ button cần nhất cho bước hiện tại.
- Các button mở object liên quan có thể chuyển sang smart button hoặc tab/link phù hợp.
- Các action ít dùng có thể đặt ở action menu nếu Odoo hỗ trợ hợp lý.
- Không xóa action cũ nếu còn cần cho backward compatibility.
- Không đổi method name nếu button cũ đang dùng.

### 3. Tổ chức lại form theo nghiệp vụ

Đề xuất bố cục:

- Tab/section “Thông tin yêu cầu”.
- Tab/section “Tiếp nhận và SLA”.
- Tab/section “Kiểm tra ban đầu”.
- Tab/section “Kế hoạch và FSM”.
- Tab/section “Đề xuất và phê duyệt”.
- Tab/section “Vật tư / Kho / Mua hàng”.
- Tab/section “Thực thi”.
- Tab/section “Nghiệm thu”.
- Tab/section “Dấu vết hệ thống”.

Audit field như user/time/status kỹ thuật nên đặt nơi ít gây nhiễu hơn, trừ những field thật sự cần cho quyết định hiện tại.

### 4. Cải thiện list/search view

Đề xuất và triển khai nếu an toàn:

- Cột chính: tên request, thiết bị, phòng ban/cửa hàng, loại yêu cầu, nguồn, người phụ trách, trạng thái quy trình, SLA, ngày tạo, task/kho/PO liên quan.
- Filter:
  - Chưa tiếp nhận
  - Quá SLA tiếp nhận
  - Chờ kiểm tra
  - Chờ lập kế hoạch
  - Chờ FSM
  - Đang thực thi
  - Chờ nghiệm thu
  - Chờ duyệt đề xuất
  - Chờ vật tư
  - Chờ mua ngoài
- Group by:
  - Phòng ban
  - Loại yêu cầu
  - Nguồn yêu cầu
  - Người phụ trách
  - Trạng thái quy trình
  - SLA

### 5. Cải thiện liên kết object chéo

Kiểm tra và cải thiện:

- Từ `maintenance.request` mở được FSM task, stock picking, PO liên quan.
- Từ `project.task` nhìn thấy request gốc và mở lại được.
- Từ `stock.picking` nhìn thấy request/task gốc.
- Từ `purchase.order` nhìn thấy request/task gốc.
- Không tạo duplicate object khi object liên quan đã tồn tại.

### 6. Cải thiện thông báo lỗi

Khi action bị chặn, `UserError` phải nói rõ:

- Thiếu field nào.
- Cần điền ở tab/section nào.
- Ai có quyền thực hiện.
- Bước trước nào chưa hoàn tất.
- Object liên quan nào cần tạo hoặc mở.

Tránh thông báo chung chung như “Missing required data”.

## Ràng Buộc Kỹ Thuật Khi Sửa

- Không sửa core Odoo.
- Không sửa module khác nếu chưa chứng minh bắt buộc.
- Không đổi tên model gốc.
- Không đổi tên field cũ nếu không có migration rõ.
- Không xóa XML ID cũ.
- Không xóa dữ liệu cũ.
- Không xóa comment hiện có.
- Không chạy formatter làm đổi hàng loạt file.
- Không tạo dependency mới nếu không cần.
- Không tạo model mới nếu compute/related/action/wizard trên object hiện có đã đủ.
- Không làm field required mới trên model chuẩn khiến các flow Odoo khác bị lỗi.
- Không override method chuẩn quá rộng.
- Nếu override create/write/action chuẩn, phải guard bằng điều kiện 0502 rõ ràng.
- Không cấp quyền rộng hơn cần thiết.
- Không làm record của module khác bị ẩn hoặc bị khóa bởi security của 0502.
- Không dùng `sudo()` để bỏ qua quyền nếu có thể dùng access/domain đúng.

## Output Bắt Buộc Sau Khi Rà Soát

Trước khi sửa code lớn, tạo hoặc cập nhật phần báo cáo trong câu trả lời với các mục:

## 1. Source Analysis Summary

Nêu:

- Đã đọc convention nào.
- Đã đọc JSON map nào.
- Đã đọc source chính nào.
- Module hiện kế thừa model nào.
- View chính nào đang điều khiển UI.
- Action chính nào đang điều khiển workflow.
- Data/security/cron hiện có gì.
- JSON map có khác source không.

## 2. Potential Bugs And Risks

Liệt kê lỗi tiềm ẩn theo mức độ:

- Critical: lỗi có thể làm install/upgrade fail hoặc crash view.
- High: lỗi có thể làm user không hoàn tất quy trình.
- Medium: lỗi gây thao tác sai, duplicate, dữ liệu thiếu.
- Low: lỗi UI/UX, naming, consistency, readability.

Mỗi lỗi cần có:

- File.
- Vị trí hoặc đoạn liên quan.
- Mô tả.
- Tác động.
- Cách sửa đề xuất.
- Test cần chạy.

## 3. Unfinished Or Weak Areas

Chỉ ra:

- Bước nào chưa hoàn thành.
- Bước nào mới có dấu vết tối thiểu.
- Bước nào cần object liên kết tốt hơn.
- Bước nào cần view/filter/action tốt hơn.
- Bước nào cần validation tốt hơn.
- Bước nào cần UX hướng dẫn tốt hơn.

## 4. UX Friction Points

Chỉ ra các điểm người dùng thấy khó chịu/mệt:

- Quá nhiều nút.
- Không biết phải bấm gì tiếp.
- Không biết thiếu dữ liệu gì.
- Phải nhập lại dữ liệu.
- Phải tự mở nhiều màn hình rời rạc.
- Không thấy tiến độ.
- Không thấy owner/SLA rõ.
- Không thấy object liên quan.
- Nút hiện sai thời điểm.
- Tên nút khó hiểu.

## 5. Target Architecture

Đề xuất kiến trúc chỉnh sửa:

- Model/field/compute/action.
- XML form/list/search.
- Data/cron.
- Security.
- Cross-module linking.
- UI/UX grouping.
- Backward compatibility.

Giữ kiến trúc hiện tại, không rewrite lớn.

## 6. Implementation Plan

Lập plan theo từng bước nhỏ, ưu tiên an toàn:

1. Sửa lỗi install/view/action chắc chắn nếu có.
2. Sửa lỗi method/field/action mismatch nếu có.
3. Bổ sung computed helper field nếu cần để hiển thị bước hiện tại/việc cần làm.
4. Cải thiện form view `maintenance.request`.
5. Cải thiện list/search view `maintenance.request`.
6. Cải thiện liên kết sang FSM task.
7. Cải thiện liên kết sang stock picking.
8. Cải thiện liên kết sang purchase order.
9. Cải thiện UserError/validation message.
10. Kiểm tra security/access không mở rộng quá mức.
11. Chạy install/upgrade/check log.

Với mỗi bước:

- File sửa.
- Mục tiêu.
- Nội dung sửa.
- Rủi ro.
- Cách kiểm tra.

## 7. Regression Check Plan

Phải kiểm tra:

- Install module mới.
- Upgrade module có dữ liệu.
- Mở form maintenance request.
- Tạo request mới.
- Bấm các action chính theo thứ tự.
- Tạo/mở FSM task.
- Tạo/mở stock picking.
- Tạo/mở purchase order.
- Kiểm tra list/search/filter.
- Kiểm tra cron preventive nếu có.
- Kiểm tra không ảnh hưởng tạo maintenance request chuẩn.
- Kiểm tra không ảnh hưởng project task chuẩn.
- Kiểm tra không ảnh hưởng stock picking chuẩn.
- Kiểm tra không ảnh hưởng purchase order chuẩn.

## 8. Files Used For Confirmation

Liệt kê file đã đọc và vai trò của từng file.

## Thứ Tự Triển Khai Đề Xuất Cho Codex

### Bước 0 - Kiểm tra trạng thái repo

Chạy:

```powershell
git status --short
```

Không revert thay đổi không phải của mình.

### Bước 1 - Đọc convention và map

Đọc:

- `addons/M02_P0502/convention/QUY_UOC_DAT_TEN_VA_RULE.md`
- `addons/M02_P0502/structure/module_map.json`

Ghi lại:

- manifest dependencies
- models/views/security/data
- relations chính
- điểm nào map có vẻ cũ hơn source nếu thấy

### Bước 2 - Rà soát source trung tâm

Đọc:

- `models/maintenance_request.py`
- `views/maintenance_request_views.xml`

Mục tiêu:

- Lập danh sách action button.
- Đối chiếu action button với method Python.
- Lập danh sách field view.
- Đối chiếu field view với model.
- Tìm condition invisible/readonly có thể gây kẹt flow.

### Bước 3 - Rà soát object liên kết

Đọc:

- `models/project_task.py`
- `views/project_task_views.xml`
- `models/stock_picking.py`
- `views/stock_picking_views.xml`
- `models/purchase_order.py`
- `views/purchase_order_views.xml`

Mục tiêu:

- Kiểm tra link về request gốc.
- Kiểm tra action mở object liên quan.
- Kiểm tra duplicate creation.
- Kiểm tra list/search có đủ cột/filter.

### Bước 4 - Rà soát preventive/equipment/cron

Đọc:

- `models/maintenance_equipment.py`
- `views/maintenance_equipment_views.xml`
- `data/ir_cron_data.xml`

Mục tiêu:

- Kiểm tra cron method.
- Kiểm tra sinh request định kỳ có chống trùng không.
- Kiểm tra UI thiết bị có rõ lịch preventive không.

### Bước 5 - Rà soát master data và access

Đọc:

- `models/request_source.py`
- `models/request_type.py`
- `data/request_source_data.xml`
- `data/request_type_data.xml`
- `security/ir.model.access.csv`

Mục tiêu:

- Kiểm tra access đủ nhưng không quá rộng.
- Kiểm tra master data dùng được trong form/search.
- Kiểm tra có cần template/hướng dẫn dễ hiểu hơn không.

### Bước 6 - Lập danh sách lỗi và plan

Trước khi sửa, ghi rõ:

- lỗi chắc chắn
- lỗi tiềm ẩn
- điểm UI/UX gây mệt
- phần chưa hoàn thành
- plan sửa theo từng bước

Nếu có lỗi install/view nghiêm trọng, sửa trước.

### Bước 7 - Thực hiện chỉnh sửa từng bước

Ưu tiên thứ tự:

1. Lỗi kỹ thuật chắc chắn.
2. Lỗi khiến flow bị kẹt.
3. Cải thiện thông báo lỗi.
4. Cải thiện form header/button.
5. Cải thiện form grouping.
6. Cải thiện list/search/filter.
7. Cải thiện object links.
8. Cải thiện usability nhỏ.

Không trộn quá nhiều thay đổi không liên quan trong một bước.

### Bước 8 - Chạy kiểm tra

Tùy môi trường, chạy các lệnh phù hợp.

Nếu chạy trực tiếp:

```powershell
python odoo-bin -d <db_test> -i M02_P0502 --stop-after-init
python odoo-bin -d <db_test> -u M02_P0502 --stop-after-init
```

Nếu chạy bằng Docker, dùng container hiện có của dự án. Không reset database nếu chưa được phép.

Nếu không chạy được do môi trường/sandbox, báo rõ đã không chạy được và lý do.

### Bước 9 - Kết luận

Final answer cần nêu:

- Đã sửa file nào.
- Đã cải thiện gì.
- Lỗi tiềm ẩn nào đã xử lý.
- Còn rủi ro gì.
- Đã chạy check nào.
- Check nào chưa chạy được.

## Các Gợi Ý Cải Thiện Cụ Thể Nên Ưu Tiên Xem Xét

### Gợi ý 1 - Tạo “Current Step” và “Next Action”

Nếu chưa có field đủ rõ, cân nhắc thêm compute field trên `maintenance.request`:

- `x_psm_0502_current_step_label`
- `x_psm_0502_next_action_label`
- `x_psm_0502_blocking_reason`

Chỉ thêm nếu thật sự giúp UI/UX và không phá dữ liệu cũ.

### Gợi ý 2 - Gom field audit vào nhóm riêng

Các field như:

- received by/at
- inspected by/at
- planned by/at
- proposed by/at
- approved/rejected by/at
- material checked by/at
- stock issued by/at

nên cân nhắc đưa vào nhóm/tab “Dấu vết xử lý” nếu đang làm rối form chính.

### Gợi ý 3 - Tạo queue theo vai trò

Nếu người dùng phải tự lọc thủ công, bổ sung filter/action menu:

- Request chờ tiếp nhận.
- Request chờ kiểm tra.
- Request chờ lập kế hoạch.
- Request chờ task FSM.
- Request chờ nghiệm thu.
- Request chờ duyệt proposal.
- Request chờ vật tư.
- Request chờ mua ngoài.

### Gợi ý 4 - Nút action cần có điều kiện và tên dễ hiểu

Tên nút nên phản ánh hành động nghiệp vụ:

- “Tiếp nhận yêu cầu”
- “Ghi nhận kiểm tra”
- “Phân công CMT Lead”
- “Xác nhận đã lập kế hoạch”
- “Tạo công việc FSM”
- “Ghi nhận bắt đầu thực thi”
- “Ghi nhận hoàn tất thực thi”
- “Ghi nhận nghiệm thu”
- “Gửi đề xuất duyệt”
- “Duyệt đề xuất”
- “Từ chối đề xuất”
- “Kiểm tra vật tư”
- “Tạo phiếu xuất kho”
- “Kiểm tra tồn kho”
- “Duyệt xuất vật tư”
- “Tạo RFQ/PO”

Không đổi method name; chỉ đổi `string` nếu an toàn.

### Gợi ý 5 - Validation message phải chỉ thẳng chỗ thiếu

Ví dụ tốt:

> Chưa thể đánh dấu đã lập kế hoạch. Vui lòng điền “Scheduled Date” và “Responsible” trong nhóm Kế hoạch xử lý.

Ví dụ không tốt:

> Missing required fields.

## Các Điều Không Được Làm

- Không xóa comment hiện có.
- Không xóa field/action/view/data cũ.
- Không đổi XML ID cũ nếu không bắt buộc.
- Không đổi model name.
- Không đổi field name cũ.
- Không thêm required field trên model chuẩn nếu không kiểm tra flow chuẩn.
- Không viết CSS/JS vì module hiện chủ yếu là backend view, trừ khi có yêu cầu rõ và manifest/asset phù hợp.
- Không thêm controller/portal nếu chưa có yêu cầu nghiệp vụ rõ.
- Không tạo workflow engine mới.
- Không tạo model mới chỉ để hiển thị UI.
- Không sửa module `maintenance`, `industry_fsm`, `stock`, `purchase`, `purchase_stock`, `hr`.
- Không chạy lệnh destructive như `git reset --hard`.

## Files Used For This Prompt

- `addons/M02_P0502/convention/QUY_UOC_DAT_TEN_VA_RULE.md`: quy ước naming, field prefix, action/view id, minimum permission, tách bạch module.
- `addons/M02_P0502/structure/module_map.json`: manifest, dependencies, models, views, security, data, relations của module 0502.
- `addons/M02_P0502/models/maintenance_request.py`: source trung tâm của flow 0502, chứa nhiều field/action/compute cho quy trình bảo trì.
- `addons/M02_P0502/views/maintenance_request_views.xml`: view chính đang quyết định phần lớn UI/UX, header buttons và grouping field của `maintenance.request`.
- `addons/M02_P0502/notes/phase_2_ke_hoach_chi_tiet_theo_tung_buoc.md`: định hướng phase 2 về làm mượt quy trình, giảm thao tác tay, nối mượt các module chuẩn Odoo.

