# Phase 0 - Triển khai implied_ids module 0200

Ngày thực hiện: 2026-05-14

## Tài liệu đã dùng

- Convention 0213: `addons/M02_P0213/convention/QUY_UOC_DAT_TEN_VA_RULE.md`
- Map 0213: `addons/M02_P0213/structure/module_map.json`
- Tài liệu rà soát: `addons/M02_P0213/RÀ_SOÁT_PHÂN_QUYỀN_MODULE_0213_CHI_TIẾT.md`
- Convention 0200: `addons/M02_P0200/convention/QUY_UOC_DAT_TEN_VA_RULE.md`
- Map 0200: `addons/M02_P0200/structure/module_map.json`
- Source xác nhận cuối cùng: `addons/M02_P0200/security/security.xml`

## Kết quả đối chiếu source

Trước Phase 0, các group sau chưa có chain tới `base.group_user`:

- `GDH_RST_OPS_OC_S`
- `GDH_RST_OPS_OM_M` qua `GDH_RST_OPS_OC_S`
- `GDH_RST_HR_HRBP_S`
- `GDH_RST_HR_HRBP_M` qua `GDH_RST_HR_HRBP_S`
- `GDH_RST_HR_CNB_S`
- `GDH_RST_HR_CNB_M` qua `GDH_RST_HR_CNB_S`

Nhóm `GDH_RST_HR_CNB_S/M` trong tài liệu được ghi là cần xác nhận. Source hiện tại xác nhận nhóm này cũng thiếu chain tới user nội bộ.

## Thay đổi đã triển khai

Trong `addons/M02_P0200/security/security.xml`, thêm `implied_ids` tới `GDH_RST_ALL_BASE_S` cho các group staff:

- `GDH_RST_HR_CNB_S`
- `GDH_RST_HR_HRBP_S`
- `GDH_RST_OPS_OC_S`

Các group manager tương ứng nhận chain gián tiếp:

- `GDH_RST_HR_CNB_M` -> `GDH_RST_HR_CNB_S` -> `GDH_RST_ALL_BASE_S` -> `base.group_user`
- `GDH_RST_HR_HRBP_M` -> `GDH_RST_HR_HRBP_S` -> `GDH_RST_ALL_BASE_S` -> `base.group_user`
- `GDH_RST_OPS_OM_M` -> `GDH_RST_OPS_OC_S` -> `GDH_RST_ALL_BASE_S` -> `base.group_user`

Lý do dùng `GDH_RST_ALL_BASE_S`: đây là group base nội bộ đã có trong module 0200 và đang imply `base.group_user`, phù hợp hơn với cấu trúc phân quyền hiện có so với việc gắn trực tiếp `base.group_user` lặp lại ở từng group manager.

## Tác động dự kiến

- Các group OPS/HRBP/CNB liên quan có thể nhận ACL dành cho `base.group_user`.
- Module 0213 không cần cấp bù ACL nền cho các group này chỉ để mở các tính năng Odoo cơ bản.
- Các module khác đang dùng các group này cũng được hưởng chain user nội bộ, nổi bật gồm các module có tham chiếu `M02_P0200.GDH_RST_OPS_OC_S`, `M02_P0200.GDH_RST_OPS_OM_M`, `M02_P0200.GDH_RST_HR_HRBP_S/M`, `M02_P0200.GDH_RST_HR_CNB_S/M`.

## Baseline test đề xuất sau khi update module

Tạo hoặc dùng 3 user test:

- User OPS: chỉ gắn `M02_P0200.GDH_RST_OPS_OC_S`
- User HRBP: chỉ gắn `M02_P0200.GDH_RST_HR_HRBP_M`
- User HR Admin: gắn `M02_P0200.GDH_RST_HR_ADMIN_M`

Kiểm tra sau khi upgrade module 0200:

- User OPS có `base.group_user` qua implied chain.
- User HRBP có `base.group_user` qua implied chain.
- User CNB nếu test bổ sung có `base.group_user` qua implied chain.
- User OPS/HRBP truy cập được menu/model nền mà module 0213 đang kỳ vọng cho internal user.
- Không tự phát sinh thêm quyền write/unlink ngoài các ACL hiện hữu.

## Lưu ý map

Trước khi triển khai, `addons/M02_P0200/structure/module_map.json` ghi `module_name`/`module_path` lệch với thư mục hiện tại (`M02_P0200_00`). Source thật đã được ưu tiên theo rule làm việc.

Sau thay đổi, đã chạy lại `python structure\build_module_map.py` trong `addons/M02_P0200`; map hiện đã ghi đúng `module_name: M02_P0200` và detail `security__security.xml.json` đã nhận các `implied_ids` mới.
