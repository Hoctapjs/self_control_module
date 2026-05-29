# Plan - Cho HR cấu hình người duyệt trong quy trình approval 0215

Ngày lập: 2026-05-13
Người lập: Claude (giao cho Codex thực hiện)
Tham chiếu:
- `notes/PHASE_B_DA_TRIEN_KHAI_APPROVAL_0215.md`
- `data/approval_category_data.xml`
- `models/x_psm_hr_discipline_record.py`
- `models/x_psm_approval_request.py`
- `convention/QUY_UOC_DAT_TEN_VA_RULE.md`

---

## 1. Mục tiêu

Thay đoạn chọn approver hard-code theo group `hr.group_hr_manager` (xem
[models/x_psm_hr_discipline_record.py:1315](../models/x_psm_hr_discipline_record.py#L1315) -
`_x_psm_get_approval_approver_users`) bằng cách lấy danh sách approver từ
approval.category chuẩn của Odoo, để HR (`hr.group_hr_manager`) tự bật/tắt
người duyệt qua giao diện Approvals.

Không thêm model cấu hình mới, không thêm group mới.

## 2. Quyết định thiết kế đã chốt

| Quyết định | Lựa chọn | Lý do |
|---|---|---|
| Nơi lưu cấu hình approver | `approval.category.approver_ids` (model gốc Odoo) | Đã có sẵn UI, validate, sequence, required. Không phát sinh model phụ |
| Group được sửa cấu hình | `hr.group_hr_manager` (đã có) | Đúng nhóm HR đang vận hành 0215 |
| Approval Category mục tiêu | `M02_P0215.approval_category_psm_discipline_company_level` | Đã tồn tại, đã được seed bằng `noupdate="1"` |
| Cách HR truy cập | Menu app `Approvals` có sẵn + smart link từ form 0215 | HR đã có quyền `approvals.group_approval_user` (implied trong Phase B) |
| Khi không có approver cấu hình | Báo lỗi `UserError` rõ ràng | Bắt buộc HR phải set ít nhất 1 approver |

## 3. Phạm vi thay đổi

### 3.1. File cần SỬA

1. `models/x_psm_hr_discipline_record.py`
2. `data/approval_category_data.xml`
3. `views/x_psm_hr_discipline_record_views.xml` (chỉ nếu cần thêm shortcut)
4. `notes/HUONG_DAN_THAO_TAC_SU_DUNG_QUY_TRINH_0215.md` (cập nhật hướng dẫn)

### 3.2. File KHÔNG động vào

- `models/x_psm_approval_request.py` (bridge approve/refuse vẫn nguyên)
- `security/ir.model.access.csv` (HR Manager đã đủ quyền qua `approvals.group_approval_user`)
- `security/security_rules.xml`
- Các file portal/survey/wizard

## 4. Chi tiết thay đổi

### 4.1. `models/x_psm_hr_discipline_record.py`

#### 4.1.1. Sửa `_x_psm_get_approval_approver_users` (dòng 1315–1322)

Đổi nguồn approver: thay vì query group `hr.group_hr_manager.all_user_ids`,
đọc từ `approval.category.approver_ids` của category 0215.

Pseudocode mới:

```python
def _x_psm_get_approval_approver_lines(self, category):
    """Trả về list dict đã sẵn để write vào approval.request.approver_ids.

    Đọc từ approval.category.approver_ids (cấu hình HR), giữ nguyên
    sequence và required. Lọc theo công ty đang chạy.
    """
    self.ensure_one()
    company = self.env.company
    lines = category.approver_ids.filtered(
        lambda a: not a.user_id.share
        and (not a.user_id.company_ids or company in a.user_id.company_ids)
    )
    return [
        {
            "user_id": line.user_id.id,
            "required": line.required,
            "sequence": line.sequence,
        }
        for line in lines.sorted("sequence")
    ]
```

Lưu ý:
- Đổi tên method từ `_x_psm_get_approval_approver_users` sang
  `_x_psm_get_approval_approver_lines` (đúng ngữ nghĩa mới: lines, không phải users)
  HOẶC giữ tên cũ nhưng đổi return type. **Khuyến nghị: đổi tên** để rõ ràng;
  grep xác nhận chỉ có 1 caller trong file này.
- Bỏ hoàn toàn `self.env.ref("hr.group_hr_manager", ...)` ở method này.

#### 4.1.2. Sửa `_x_psm_create_or_confirm_approval_request` (dòng 1350–1398)

Thay đoạn lấy users và xây `approver_commands` (dòng 1367–1389) bằng cách
dựng `approver_ids` ngay trong vals create — vì category đã có `approver_ids`
chuẩn, ta dùng `_x_psm_get_approval_approver_lines(category)`.

Pseudocode:

```python
def _x_psm_create_or_confirm_approval_request(self):
    self.ensure_one()
    if self.x_psm_approval_request_id:
        if self.x_psm_approval_request_id.request_status == "approved":
            self._x_psm_on_approval_request_approved(self.x_psm_approval_request_id)
            return
        if self.x_psm_approval_request_id.request_status != "refused":
            self._x_psm_write_state("approval")
            return

    category = self.env.ref(
        "M02_P0215.approval_category_psm_discipline_company_level",
        raise_if_not_found=False,
    )
    if not category:
        raise UserError(_("Không tìm thấy cấu hình approval category cho quy trình 0215."))

    approver_lines = self._x_psm_get_approval_approver_lines(category)
    # Cho phép manager_approval đảm nhiệm thay nếu HR cấu hình "Employee's Manager"
    has_manager_approval = bool(category.manager_approval)
    if not approver_lines and not has_manager_approval:
        raise UserError(_(
            "Approval category 0215 chưa có người duyệt nào. "
            "Vui lòng vào Approvals > Configuration > Approval Categories "
            "để cấu hình approvers cho category '%s'."
        ) % category.name)

    vals = self._x_psm_prepare_approval_request_vals(category)
    vals["approver_ids"] = [(0, 0, line) for line in approver_lines]
    approval_request = self.env["approval.request"].sudo().create(vals)
    approval_request.sudo().action_confirm()
    self._x_psm_write_state(
        "approval",
        {
            "x_psm_approval_request_id": approval_request.id,
            "x_psm_approval_requested_date": fields.Datetime.now(),
            "x_psm_approval_refuse_reason": False,
        },
    )
```

Lưu ý:
- Bỏ đoạn `existing_user_ids = set(...)` và `approval_request.sudo().write({"approver_ids": ...})` cũ, đẩy approvers vào ngay trong create.
- Vẫn dùng `sudo()` để xử lý trường hợp người trình không có quyền create `approval.request` trực tiếp (Phase B đã có lý do này).

#### 4.1.3. Thêm helper `action_psm_open_approval_category_config`

Cho phép HR mở thẳng approval.category từ form 0215 (nút "Cấu hình người duyệt").

```python
def action_psm_open_approval_category_config(self):
    self.ensure_one()
    category = self.env.ref(
        "M02_P0215.approval_category_psm_discipline_company_level",
        raise_if_not_found=False,
    )
    if not category:
        raise UserError(_("Không tìm thấy approval category 0215."))
    return {
        "type": "ir.actions.act_window",
        "name": _("Cấu hình người duyệt 0215"),
        "res_model": "approval.category",
        "res_id": category.id,
        "view_mode": "form",
        "target": "current",
    }
```

#### 4.1.4. Cập nhật error message

Trong `_x_psm_create_or_confirm_approval_request`, error message cũ nói
"Không tìm thấy người duyệt trong nhóm HR Manager" — sửa thành thông điệp
hướng dẫn HR đi đến cấu hình (đã có ở pseudocode mục 4.1.2).

### 4.2. `data/approval_category_data.xml`

Bổ sung seed mặc định cho `approver_ids` nhưng vẫn để `noupdate="1"` đối với
record chính (HR sẽ tự quản lý sau khi cài đặt lần đầu).

Phương án seed:

- Tạo 1 approver line mặc định trỏ tới user đang là HR Manager đầu tiên — thực hiện
  bằng `<function>` Python eval trong XML, hoặc bằng `noupdate=1` để chỉ chạy
  lần đầu cài đặt module.
- Đơn giản hơn: KHÔNG seed approver mặc định; thay vào đó, hiển thị banner
  trong view category nhắc HR cấu hình. Lần install đầu, HR sẽ thấy error
  rõ ràng khi bấm trình duyệt nếu chưa cấu hình.

**Khuyến nghị**: chọn cách 2 (không seed cứng), vì:
- HR mỗi công ty sẽ có CEO/HR Manager khác nhau, không thể đoán user nào;
- Error rõ ràng + nút "Cấu hình người duyệt" từ form 0215 (mục 4.1.3) là đủ UX.

Bỏ đoạn implied group `approvals.group_approval_user` từ
`hr.group_hr_manager` ra khỏi `<data>` không-noupdate sang `<data noupdate="1">`
để upgrade module không reset cấu hình group HR nếu admin đã đụng đến.

### 4.3. `views/x_psm_hr_discipline_record_views.xml`

Thêm 1 trong 2:

- (a) Nút "Cấu hình người duyệt" cạnh smart button approval request, chỉ
  hiện cho HR Manager (`groups="hr.group_hr_manager"`). Gọi
  `action_psm_open_approval_category_config`.
- (b) Hoặc chỉ ghi chú text "Cấu hình tại Approvals > Categories > 0215..."
  trong help text của field `x_psm_approval_request_id`.

**Khuyến nghị**: cả 2. Nút giúp HR tới đúng chỗ ngay; help text giúp người
không phải HR hiểu vì sao họ không thấy nút.

### 4.4. Cập nhật `notes/HUONG_DAN_THAO_TAC_SU_DUNG_QUY_TRINH_0215.md`

Thêm 1 mục mới: "Cấu hình người duyệt cấp công ty" mô tả luồng:

1. HR Manager vào app `Approvals`.
2. Vào `Configuration > Approval Categories`.
3. Mở `0215 - Phê duyệt kỷ luật cấp công ty`.
4. Tab `Approvers`: thêm/sửa/xóa user, set `Required`, `Sequence`.
5. (Optional) chỉnh `Minimum Approval` và `Approvers Sequence` (theo thứ tự).
6. (Optional) chỉnh `Employee's Manager` (Approver / Required Approver / Empty).

## 5. Kiểm thử Codex cần chạy

### 5.1. Static

- `python -m compileall .\addons\M02_P0215`
- Parse XML toàn bộ thư mục `addons/M02_P0215` bằng `xml.etree.ElementTree`

### 5.2. Functional (manual trên DB test, ghi rõ kết quả)

1. Cài/upgrade module M02_P0215 trên DB sạch.
2. Đăng nhập HR Manager, mở approval category `0215 - Phê duyệt kỷ luật cấp công ty`. Xác nhận có thể thêm 2 approver: 1 required, 1 optional.
3. Tạo hồ sơ 0215 ở Company Level, đi tới bước `issued`, bấm `Trình duyệt`.
   - Kỳ vọng: approval.request được tạo có đúng 2 approver như cấu hình, đúng `required` flag, đúng `sequence`.
   - Hồ sơ 0215 chuyển sang `approval`.
4. Approver required approve → request đến `approved` → hồ sơ 0215 chuyển `notified` và email gửi nhân viên.
5. Trường hợp HR xóa hết approver trong category, rồi tạo hồ sơ company-level và bấm `Trình duyệt`:
   - Kỳ vọng: `UserError` với message "Approval category 0215 chưa có người duyệt nào...".
6. Hồ sơ company-level đã có approval.request bị refused, HR điều chỉnh → bấm `Trình duyệt` lần 2:
   - Kỳ vọng: tạo `approval.request` mới với approvers theo cấu hình hiện tại của category (không reuse approver cũ).
7. Test với category bật `manager_approval = "required"` và xóa hết `approver_ids`:
   - Kỳ vọng: vẫn tạo được request (vì manager của request_owner sẽ được Odoo gốc tự bổ sung).

## 6. Tương thích ngược

- Field `x_psm_approval_request_id`, `x_psm_approval_status`, dates, reason: KHÔNG đổi schema.
- Hồ sơ cũ đang ở state `approval` với approval.request cũ: vẫn hoạt động bình thường vì luồng approve/refuse không đổi.
- Hồ sơ legacy chưa qua approval: helper `_x_psm_migrate_legacy_approval_bridge` (dòng 1105) vẫn gọi `_x_psm_create_or_confirm_approval_request` nên sẽ tự lấy approver từ cấu hình HR mới.

## 7. Rủi ro & mitigation

| Rủi ro | Mitigation |
|---|---|
| HR chưa cấu hình approver sau upgrade → người dùng bấm Trình duyệt báo lỗi | Error message dẫn đường rõ + nút "Cấu hình người duyệt" trên form 0215; cập nhật `HUONG_DAN_THAO_TAC_SU_DUNG_QUY_TRINH_0215.md` |
| Approver bị unset `share=False` hoặc đổi company | Filter trong `_x_psm_get_approval_approver_lines` đã loại share user và user không thuộc company |
| Hồ sơ multi-company | Vẫn giữ `self.env.company` làm chuẩn lọc; approval.category `_check_company_auto = True` (Odoo gốc) đảm bảo HR không thấy category sai company |
| Codex đổi sai tên method và làm vỡ caller | Caller duy nhất hiện tại là `_x_psm_create_or_confirm_approval_request`. Sửa song song trong cùng commit. Grep `_x_psm_get_approval_approver_users` toàn repo trước khi xóa |

## 8. Checklist hand-off cho Codex

- [ ] Đọc kỹ Section 4 và áp đúng pseudocode/skeleton.
- [ ] Không thêm model mới.
- [ ] Không thêm group security mới.
- [ ] Không thay đổi schema 5 field approval đã có trên `x_psm.hr.discipline.record`.
- [ ] Chạy compile + parse XML, dán log vào commit message.
- [ ] Viết note triển khai mới: `notes/PHASE_H_DA_TRIEN_KHAI_CAU_HINH_APPROVER_0215.md` theo format đã có ở PHASE_B, kèm danh sách file sửa và kết quả test.
- [ ] Cập nhật `structure/module_map.json` nếu module map dùng auto-build (`structure/build_module_map.py`).

## 9. Ước lượng

- Code thay đổi: ~80 dòng net (xóa ~25, thêm ~55).
- Test manual: 6 kịch bản, ước ~30 phút.
- Tổng: 1 buổi làm việc cho Codex là đủ.

## 10. Khuyến nghị chia bước thực hiện

Nên chia plan này thành từng bước trước khi triển khai. Lý do: phạm vi không quá lớn,
nhưng chạm vào nhiều nhóm khác nhau gồm logic Python, data XML, view UX, tài liệu,
kiểm thử và regenerate structure. Nếu làm một mạch dễ sót hoặc khó debug khi upgrade
module lỗi.

Các tài liệu và source đã dùng để đối chiếu khi đưa ra khuyến nghị:

- Convention: `convention/QUY_UOC_DAT_TEN_VA_RULE.md`
- Structure map: `structure/module_map.json`
- Source xác nhận chính:
  - `models/x_psm_hr_discipline_record.py`
  - `data/approval_category_data.xml`
  - `views/x_psm_hr_discipline_record_views.xml`

Đề xuất thứ tự thực hiện:

1. **Bước 1 - Xác nhận hiện trạng**
   - Grep `_x_psm_get_approval_approver_users`.
   - Xác nhận caller của method.
   - Xác nhận approval category XML hiện tại.
   - Xác nhận vị trí smart button trong form view.

2. **Bước 2 - Sửa core logic Python**
   - Đổi helper lấy approver từ `hr.group_hr_manager` sang `approval.category.approver_ids`.
   - Sửa `_x_psm_create_or_confirm_approval_request`.
   - Cập nhật error message.
   - Thêm action mở cấu hình approval category.

3. **Bước 3 - Sửa data XML**
   - Chốt rõ: không seed approver mặc định.
   - Chỉ xử lý phần implied group `approvals.group_approval_user` nếu thật sự cần chuyển sang `noupdate="1"`.
   - Tách bước này riêng vì data XML khi upgrade dễ có tác động ngoài logic code.

4. **Bước 4 - Sửa view**
   - Thêm nút "Cấu hình người duyệt" cho HR Manager.
   - Có thể thêm help text ở khu vực phê duyệt nếu hợp lý.
   - Kiểm tra naming action theo convention: `action_psm_open_approval_category_config` là phù hợp.

5. **Bước 5 - Cập nhật tài liệu**
   - Cập nhật `notes/HUONG_DAN_THAO_TAC_SU_DUNG_QUY_TRINH_0215.md`.
   - Tạo note triển khai `notes/PHASE_H_DA_TRIEN_KHAI_CAU_HINH_APPROVER_0215.md`.

6. **Bước 6 - Static test**
   - Chạy `python -m compileall .\addons\M02_P0215`.
   - Parse XML toàn module.

7. **Bước 7 - Functional/manual test**
   - Test approver required/optional.
   - Test không có approver.
   - Test refused rồi trình lại.
   - Test `manager_approval`.

8. **Bước 8 - Regenerate structure**
   - Vì module có `structure/build_module_map.py`, nếu source thay đổi thì nên chạy lại map ở cuối.

Lưu ý cần chỉnh nhẹ trong plan trước khi giao triển khai: mục 4.2 đang mở bằng câu
"Bổ sung seed mặc định cho `approver_ids`", nhưng ngay sau đó lại khuyến nghị không
seed cứng. Nên đổi cách diễn đạt thành: "Không seed approver mặc định; chỉ dùng
error rõ ràng + shortcut cấu hình". Như vậy plan sạch và ít gây hiểu nhầm hơn.
