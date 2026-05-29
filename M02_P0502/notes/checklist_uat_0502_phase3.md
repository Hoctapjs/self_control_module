# Checklist UAT 0502 Phase 3

## 1. Chuan bi

- Cai dat/cap nhat module `M02_P0502` voi demo data neu can test nhanh.
- Kiem tra user test da co group phu hop: Store User, Store Approver, Store Final Approver, CMT User, CMT Lead, Manager.
- Kiem tra `0502 Demo CMT Team` co lead, approver, vendor, picking type, source/destination location.
- Kiem tra co thiet bi demo, department demo, request demo va outside service demo.

## 2. Luong noi bo khong vat tu

- Tao request store repair moi voi department, request type, request source va intake detail day du.
- Bam `Receive Request`.
- Nhap thong tin inspection va bam `Mark Inspected`.
- Nhap schedule/responsible va bam `Mark Planned`.
- Tao FSM task va mo task de kiem tra context 0502.
- Nhap proposal, submit approval va xac nhan auto/manual approval.
- Chon service route internal, danh dau service assessed.
- Chon khong phat sinh vat tu, mark material checked.
- Mark execution started/completed sau khi FSM task da dong.
- Nhap acceptance accepted va xac nhan request ve stage `0502 Done`.

## 3. Luong outside service

- Tao request repair can vendor service.
- Di qua inspection, planning, proposal, approval.
- Chon service route `Outside Service` va mark service assessed.
- Kiem tra outside service request duoc tao.
- Chay flow: draft -> sent to vendor -> quoted -> approved -> in progress/completed -> accepted.
- Quay lai request goc, nhap acceptance va xac nhan request dong duoc.

## 4. Luong vat tu va mua ngoai

- Tao request co `Has Material Request`.
- Them material lines voi expected source.
- Tao stock picking va check stock availability.
- Neu khong du ton, tao RFQ/PO va re-check sau khi PO confirmed/done.
- Submit material approval, approve/auto approve, validate picking.
- Xac nhan stock issue status cap nhat dung.

## 5. Rework loop

- Hoan tat execution.
- Nhap acceptance result `Rework Required` hoac `Follow-up Needed`.
- Bam `Mark Acceptance Reviewed`.
- Kiem tra button `Reopen for Rework` hien.
- Bam reopen, xac nhan rework round count tang va execution/acceptance reset.
- Thuc hien execution lai, acceptance accepted va request ve `0502 Done`.

## 6. Reports va document pack

- Mo request co du du lieu.
- In request document, inspection report, proposal, material issue request, acceptance record.
- Mo wizard document pack, tick nhieu report va xac nhan action tra ve report.
- Kiem tra moi chung tu co sequence rieng khi moc tuong ung da hoan tat.

## 7. Security

- Store user chi thay request cua department gan voi employee cua user.
- CMT user thay request cua team minh la member.
- CMT lead thay request cua team minh phu trach.
- Store approver/final approver moi thay va thuc hien duyet proposal dung cap.
- Manager thay toan bo va co quyen unlink history khi can.

## 8. Ket qua chap nhan

- Khong co traceback khi mo menu, form, list, search, report.
- Demo data load khong loi.
- Smoke test `tests/test_0502_flow.py` pass trong moi truong Odoo co day du dependency.
- Cac request demo bao phu intake, proposed, outside service, material/history va done.
