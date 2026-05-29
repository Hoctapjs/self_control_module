# MKT 0901 - PAF Management

Module số hóa toàn bộ quy trình đề xuất – đánh giá – phê duyệt – triển khai – đo lường một Sản phẩm mới / Chương trình khuyến mãi mới trên Odoo 19 EE.

## Quy trình 12 bước (PAF)

| Bước | Nghiệp vụ | Phòng | Artefact triển khai |
|---|---|---|---|
| **B1** | Odoo cập nhật masterdata (recipe, NVL, giá) | System | Kế thừa `product.template`, `mrp.bom`, `product.supplierinfo`. Thêm field `paf_can_use = Boolean` cho lọc nhanh. |
| **B2** | S&I tracking thay đổi PAF template | S&I | Kế thừa `mail.thread` audit log + view kanban template. |
| **B3** | MKT tạo PAF từ template | MKT | Model mới `mkt_paf.template` + `mkt_paf.request` (action `action_create_from_template`). |
| **B4** | S&I phân tích dữ liệu | S&I | Model `mkt_paf.evaluation.line` (department='si') + computed `forecast_pspd`. |
| **B5** | OPS đánh giá vận hành | OPS | `mkt_paf.evaluation.line` (department='ops') + `pilot_capacity_score`. |
| **B6** | Finance đánh giá ROI | Finance | `mkt_paf.evaluation.line` (department='finance') + `roi_estimated_percent`, `gross_margin`. |
| **B7** | SC đánh giá khả năng cung ứng | SC | `mkt_paf.evaluation.line` (department='sc') + `supply_risk_level`. |
| **B8** | Legal đánh giá scheme + thời gian xin phép | Legal | `mkt_paf.evaluation.line` (department='legal') + `regulatory_sla_days`. |
| **B9** | Head các phòng duyệt | Heads | `approval.request` (category `mkt_0901_paf_head_review`) — sequence multi-approver. |
| **B10** | C-Level duyệt cuối | C-Level | `approval.request` (category `mkt_0901_paf_clevel_review`) — chỉ 1 approver. |
| **B11** | RSG trigger PIF | RSG | `_run_pif_workflow()` → tạo `approval.request` PIF từ module `M08_P0801`. |
| **B12** | S&I xuất báo cáo PAF Valuation | S&I | Model `mkt_paf.valuation.report` + QWeb report `mkt_0901_report_paf_valuation`. |
| **Note 1** | Break PSPD theo store | S&I + OPS | Model `mkt_paf.pspd.line` + cron `mkt_0901_cron_pspd_distribute`. |
| **Note 2** | SLA pháp lý động | Legal | Computed `paf_effective_start_date = paf_planned_start - regulatory_sla_days` + constraint chặn schedule sát ngày. |

> Note: PIF integration migrated từ RSG_0801 (deprecated) sang M08_P0801 theo migration plan ngày 2026-05-26.
