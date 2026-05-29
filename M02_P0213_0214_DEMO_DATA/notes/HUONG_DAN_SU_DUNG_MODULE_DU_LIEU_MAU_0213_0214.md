# Huong Dan Su Dung Module Du Lieu Mau 0213/0214

Module `M02_P0213_0214_DEMO_DATA` tao du lieu mau de test nhanh quy trinh nghi viec 0213 va 0214, tap trung vao phep nam (AL).

## Tai khoan demo

- `al_demo_manager` / `123`: quan ly demo, co quyen Approval Manager va HR Head RST.
- `0213_al_positive` / `123`: nhan vien 0213 con 12 ngay AL.
- `0213_al_zero` / `123`: nhan vien 0213 con 0 ngay AL.
- `0213_al_advance` / `123`: nhan vien 0213 am 7 ngay AL.
- `0214_al_positive` / `123`: nhan vien 0214 con 10 ngay AL.
- `0214_al_zero` / `123`: nhan vien 0214 con 0 ngay AL.
- `0214_al_advance` / `123`: nhan vien 0214 am 8 ngay AL.

## Ban ghi test chinh

- `0213 Demo Resignation - AL Positive`
- `0213 Demo Resignation - AL Zero`
- `0213 Demo Resignation - Advance AL`
- `0214 Demo Resignation - AL Positive`
- `0214 Demo Resignation - AL Zero`
- `0214 Demo Resignation - Advance AL`

Sau khi cai module, post-init hook validate allocation/leave demo va ghi snapshot `x_psm_0200_remaining_al_days` tren employee de UI AL advance cua 0213/0214 hien dung ngay.
