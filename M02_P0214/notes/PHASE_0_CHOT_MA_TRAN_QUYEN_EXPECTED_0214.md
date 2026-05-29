# Phase 0 - Chốt Ma Trận Quyền Expected 0214

## 1. Mục tiêu

Tài liệu này chốt baseline quyền expected cho module `M02_P0214` trước khi triển khai các phase siết security tiếp theo.

Mục tiêu của Phase 0:

- chốt phạm vi dữ liệu cần khóa
- chốt happy path chuẩn
- chốt nhóm nào được xem
- chốt nhóm nào được xử lý action nhạy cảm
- chốt các giả định không thay đổi trong các phase sau

Nguyên tắc áp dụng:

- không đụng `M02_P0200`
- không thay đổi nền role `portal/internal`
- chỉ siết trong `M02_P0214`

## 2. Tài liệu và nguồn đã dùng

- Convention đã dùng:
  - Không thấy file convention trong `addons/M02_P0214/convention/`
- JSON map đã dùng:
  - [structure/module_map.json](/d:/odoo-19.0+e.20250918/addons/M02_P0214/structure/module_map.json)
- Source chính dùng để xác nhận:
  - [__manifest__.py](/d:/odoo-19.0+e.20250918/addons/M02_P0214/__manifest__.py)
  - [security/ir.model.access.csv](/d:/odoo-19.0+e.20250918/addons/M02_P0214/security/ir.model.access.csv)
  - [security/offboarding_request_rules.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0214/security/offboarding_request_rules.xml)
  - [security/security.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0214/security/security.xml)
  - [models/approval_request_rst_fields.py](/d:/odoo-19.0+e.20250918/addons/M02_P0214/models/approval_request_rst_fields.py)
  - [models/approval_request_rst_survey.py](/d:/odoo-19.0+e.20250918/addons/M02_P0214/models/approval_request_rst_survey.py)
  - [models/approval_request_rst_offboarding.py](/d:/odoo-19.0+e.20250918/addons/M02_P0214/models/approval_request_rst_offboarding.py)
  - [controllers/main.py](/d:/odoo-19.0+e.20250918/addons/M02_P0214/controllers/main.py)
  - [views/resignation_request_views.xml](/d:/odoo-19.0+e.20250918/addons/M02_P0214/views/resignation_request_views.xml)

## 3. Ghi chú về structure map

`module_map.json` hiện đang lệch source:

- map ghi `M02_P0214_00`
- source thật là `M02_P0214`
- `__manifest__.py` depend `M02_P0200`, `M02_P0213`

Vì vậy:

- source thật là chuẩn để chốt expected matrix
- structure map cần regenerate sau khi hoàn tất các phase triển khai

## 4. Phạm vi dữ liệu cần khóa trong 0214

Các vùng dữ liệu phải được coi là nhạy cảm và cần khóa đúng scope `0214`:

- `approval.request` thuộc category nghỉ việc `0214`
- `approval.approver` của request nghỉ việc `0214`
- `survey.survey` của exit interview `0214`
- `survey.question` và `survey.question.answer` của survey đó
- `survey.user_input` và `survey.user_input.line` gắn với survey `0214`
- `mail.activity` thuộc request nghỉ việc `0214` hoặc employee được gắn từ request đó

## 5. Happy path chuẩn của 0214

### 5.1. Happy path phía portal

Portal user phải làm được:

- vào trang nghỉ việc RST của chính mình
- submit đơn nghỉ việc của chính mình
- xem request mới nhất của chính mình
- xem activity liên quan của chính mình
- mở đúng link survey nghỉ việc của chính mình
- hoàn thành activity trên portal nếu activity đó thuộc đúng request và đúng người phụ trách

### 5.2. Happy path phía backend

Backend cần một nhóm xử lý chính có thể:

- mở request nghỉ việc `0214`
- xem tab thông tin nghỉ việc
- xem checklist offboarding
- gửi exit survey
- xem survey result
- gửi email BHXH
- gửi email Adecco
- xử lý hoàn tất quy trình

### 5.3. Happy path về dữ liệu

Dữ liệu ngoài `0214` không được:

- bị nhìn thấy nhờ ACL quá rộng
- bị đọc nhầm qua các search theo email/partner
- bị cập nhật nhờ `sudo()` không có guard

## 6. Nhóm expected trong 0214

### 6.1. Portal

Portal side:

- `base.group_portal`

Vai trò:

- nhân viên nghỉ việc tự submit và theo dõi case của mình

### 6.2. Internal nhóm đọc scope 0214

Theo source hiện tại, nhóm nghiệp vụ `0214` đang xoay quanh các group:

- `M02_P0200_00.GDH_RST_HR_ADMIN_S`
- `M02_P0200_00.GDH_RST_HR_ADMIN_M`
- `M02_P0200_00.GDH_RST_HR_HRBP_S`
- `M02_P0200_00.GDH_RST_HR_HRBP_M`
- `M02_P0200_00.GDH_RST_HR_HEAD_M`
- `M02_P0200_00.GDH_RST_SYSTEM_ST_M`

Lưu ý:

- Phase 0 chỉ chốt expected business matrix
- chưa kết luận ở đây rằng tất cả các nhóm trên đã có nền internal backend giống nhau
- phần đó sẽ được đối chiếu ở Phase 1

## 7. Ma trận quyền expected theo model

### 7.1. `approval.request`

Expected:

- Portal:
  - chỉ tạo và xem request của chính mình
- Internal read:
  - thấy đúng request nghỉ việc `0214`
- Internal write:
  - chỉ nhóm xử lý mới được sửa case `0214`
- Internal create:
  - không mở rộng tạo tràn cho mọi internal user

### 7.2. `approval.approver`

Expected:

- Internal read:
  - các nhóm đọc được thấy approver line của request `0214`
- Internal write:
  - không mở rộng nếu business không cần
- Create/unlink:
  - mặc định không kỳ vọng mở rộng trong `0214`

### 7.3. `survey.survey`, `survey.question`, `survey.question.answer`

Expected:

- Portal:
  - chỉ đọc đúng survey dùng cho flow portal
- Internal:
  - chỉ đọc cấu trúc survey `0214`
- Write:
  - không mở rộng cho user nội bộ thông thường trong flow vận hành

### 7.4. `survey.user_input`, `survey.user_input.line`

Expected:

- Portal:
  - chỉ đọc/ghi bài khảo sát của chính mình
- Internal:
  - chỉ đọc kết quả survey thuộc request `0214`
- Write/create/unlink:
  - không mở rộng rộng rãi cho internal user
- Tính đúng:
  - mỗi request `0214` nên gắn được với đúng `survey.user_input`

### 7.5. `mail.activity`

Expected:

- Portal:
  - chỉ thấy activity thuộc request của chính mình
  - chỉ hoàn thành activity được giao cho chính mình
- Internal:
  - chỉ thấy activity thuộc flow `0214`
- Write:
  - chỉ nhóm xử lý hoặc automation phù hợp mới được cập nhật

## 8. Ma trận quyền expected theo action

### 8.1. `action_send_exit_survey`

Expected:

- chỉ nhóm HR xử lý hoặc nhóm quản lý case được dùng
- không phải mọi internal user đều được gửi survey

### 8.2. `action_view_survey_results`

Expected:

- nhóm đọc `0214` được xem
- chỉ xem result của đúng request `0214`

### 8.3. `action_send_social_insurance`

Expected:

- chỉ nhóm HR xử lý và nhóm quản trị/quản lý cao hơn được dùng

### 8.4. `action_send_adecco_notification`

Expected:

- chỉ nhóm HR xử lý và nhóm quản trị/quản lý cao hơn được dùng

### 8.5. `action_done`

Expected:

- chỉ nhóm manager hoặc nhóm quản lý quy trình được dùng
- không mở cho nhóm staff đọc thông thường

### 8.6. `action_view_my_activities`

Expected:

- user có quyền với case `0214` mới dùng được trong backend
- portal dùng flow riêng, không trộn với backend action

### 8.7. `action_pending_offboarding_subordinates`

Expected:

- chỉ nhóm theo dõi hoặc quản trị `0214` mới dùng

## 9. Nhóm expected theo mức thao tác

### 9.1. Nhóm chỉ nên đọc

Expected read-only hoặc gần read-only:

- `GDH_RST_HR_ADMIN_S`
- `GDH_RST_HR_HRBP_S`

### 9.2. Nhóm được xử lý nghiệp vụ

Expected xử lý phần lớn action:

- `GDH_RST_HR_ADMIN_M`
- `GDH_RST_HR_HRBP_M`
- `GDH_RST_HR_HEAD_M`

### 9.3. Nhóm hệ thống

Expected full control trong ngữ cảnh `0214`:

- `GDH_RST_SYSTEM_ST_M`

Lưu ý:

- đây là ma trận expected nghiệp vụ
- ở Phase 1 sẽ cần đối chiếu lại với actual source để xem nhóm nào thực tế đang rộng hơn hoặc hẹp hơn

## 10. Các quyết định phải giữ cố định cho các phase sau

### 10.1. Không sửa nền quyền ở 0200

Không triển khai theo hướng:

- sửa chain group trong `M02_P0200`
- nâng nền internal cho các nhóm chưa có sẵn

### 10.2. Không coi UI là lớp bảo vệ chính

Phải siết đồng thời:

- ACL
- record rule
- backend guard
- `sudo()` flow

### 10.3. Survey phải gắn chặt vào request

Không dùng search survey rộng chỉ bằng:

- `partner_id`
- `email`

nếu chưa kiểm tra đúng request `0214`.

### 10.4. Portal chỉ dùng dữ liệu của chính owner

Mọi flow portal phải bám đúng:

- `request_owner_id = current user`
- activity thuộc request đó
- survey thuộc request đó

## 11. Đầu ra cần dùng cho Phase 1

Phase 1 sẽ dùng tài liệu này để đối chiếu:

- expected matrix theo model
- expected matrix theo action
- happy path portal
- happy path backend
- các quyết định cố định không được phá vỡ

## 12. Kết luận

Phase 0 của `0214` chốt rằng:

- `0214` cần được siết tương tự `0213`
- trọng tâm khóa dữ liệu nằm ở `approval.request`, `survey.user_input`, `mail.activity`
- phải giữ nguyên nguyên tắc không đụng `0200`
- những phase sau sẽ chỉ được phép siết bên trong `M02_P0214`

Tài liệu này là baseline expected để dùng cho toàn bộ các phase tiếp theo.
