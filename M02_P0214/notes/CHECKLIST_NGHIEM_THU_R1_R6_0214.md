# Checklist Nghiem Thu R1-R6 - M02_P0214

Tai lieu nay dung de test thu cong sau khi trien khai Phase 0-7 cho module
`M02_P0214_QUY_TRINH_OFFBOARDING_RST`.

## 1. Chuan bi

- Upgrade module `M02_P0214` thanh cong tren database test.
- Dang nhap cac user demo: `employee_rst`, `manager_rst`, `it_rst`, `admin_rst`, `hr_rst`.
- Kiem tra menu cau hinh Offboarding RST co template email, user mac dinh, tham so nhac viec va loai phep AL.
- Kiem tra nhan vien demo `RST Employee` co quan ly truc tiep `RST Manager`.
- Kiem tra demo data co AL allocation, expense ton dong va tam ung ton dong.

## 2. R1 - Email va activity cho IT/Admin/HR

- Nhan vien gui don nghi viec tren Portal.
- Quan ly duyet don sau khi da dinh kem phieu nghi viec da ky.
- He thong tao activity cho IT, Admin, HR theo plan RST.
- IT/Admin/HR nhan email co link `/my/offboarding`.
- Vao `/my/offboarding`, moi user chi thay activity cua minh.
- Cron nhac viec bo phan gui toi da theo cau hinh `reminder_interval_days` va `reminder_max_count`.

## 3. R2 - Nhac quan ly duyet va email nhan vien

- Sau khi nhan vien submit don, quan ly truc tiep nhan email nhac duyet co link backend toi don.
- Cron nhac quan ly duyet gui lai neu don van `pending`.
- Khi quan ly duyet don, nhan vien nhan email thong bao da duyet.
- Email nhan vien hien thi snapshot `x_psm_0214_remaining_al_days`.
- Email gui toi ca email cong ty va email ca nhan neu co.

## 4. R3 - Dashboard Exit Interview

- Hoan thanh it nhat mot survey Exit Interview.
- Menu `Report / Exit Interview Dashboard` hien graph, pivot va list co du lieu.
- Filter theo phong ban, chuc danh, ly do nghi va ngay nghi hoat dong dung.
- Pivot tinh duoc diem hai long trung binh.
- List view co the export Excel bang chuc nang san co.
- User khong co nhom HR Manager/System khong thay menu dashboard.

## 5. R4 - Quyet toan luong va ban ky lai

- Sau khi 3 activity IT/Admin/HR done, HR upload file quyet toan luong PDF.
- He thong gui email quyet toan luong cho nhan vien.
- Nhan vien upload ban quyet toan da ky qua Portal.
- Trang thai `x_psm_0214_settlement_signed` chuyen dung.
- Cron nhac nop ban ky quyet toan gui sau so ngay cau hinh neu chua upload.

## 6. R5 - Kiem tra Ke toan

- Voi demo expense/tam ung ton dong, bam `Chot & chuyen Ke toan` bi chan.
- Don ghi `x_psm_0214_finance_check_state = blocked` va co summary phieu ton dong.
- Sau khi tat toan phieu ton dong, bam lai thi state = `passed`.
- HR Head/System co the override khi state = `blocked`, bat buoc nhap ly do.
- Report kiem tra Ke toan liet ke dung don `blocked` va `overridden`.
- `action_done` bi chan neu finance chua `passed` hoac `overridden`.

## 7. R6 - File phieu nghi viec da ky va khoa du lieu

- Khong the duyet don RST neu chua dinh kem file PDF co chu ky 2 ben.
- Khi duyet thanh cong, he thong luu SHA-256 vao `x_psm_0214_signed_resignation_hash`.
- Sau khi duyet, `x_psm_0214_signed_locked = True`.
- Khong the sua cac field trong danh sach protected khi da khoa.
- File luu attachment va chi user dung vai tro/pham vi duoc xem.

## 8. Regression toi thieu

- Module upgrade sach, khong loi missing field/XML ID.
- Registry load duoc voi `--stop-after-init --no-http`.
- Test tag `m02_p0214_r1_r6` pass.
- `structure/module_map.json` da regenerate sau phase 7.
