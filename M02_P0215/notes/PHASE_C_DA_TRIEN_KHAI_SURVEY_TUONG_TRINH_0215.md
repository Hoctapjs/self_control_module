# Phase C - Da trien khai survey cho tuong trinh 0215

Ngay cap nhat: 2026-05-07

## 1. Tai lieu da dung

- Convention: `addons/M02_P0215/convention/QUY_UOC_DAT_TEN_VA_RULE.md`
- JSON map: `addons/M02_P0215/structure/module_map.json`
- JSON stats: `addons/M02_P0215/structure/module_map_stats.json`
- Source xac nhan:
  - `addons/M02_P0215/__manifest__.py`
  - `addons/M02_P0215/models/x_psm_hr_discipline_record.py`
  - `addons/M02_P0215/models/x_psm_survey_user_input.py`
  - `addons/M02_P0215/wizards/x_psm_hr_discipline_reject_wizard.py`
  - `addons/M02_P0215/data/survey_explanation_data.xml`
  - `addons/M02_P0215/data/mail_template.xml`
  - `addons/M02_P0215/data/email_template_rejection.xml`
  - `addons/M02_P0215/views/x_psm_hr_discipline_record_views.xml`

## 2. Pham vi da lam

### 2.1. Them dependency survey

- Manifest da them dependency `survey`.
- Manifest da them data file `data/survey_explanation_data.xml`.

### 2.2. Tao survey template cho tuong trinh

Da them survey mau:

- `M02_P0215.survey_psm_explanation`

Bo cau hoi gom:

- Thoi gian xay ra su viec
- Dia diem
- Nguoi chung kien
- Noi dung tuong trinh
- Nguyen nhan
- Cam ket cai thien
- Xac nhan noi dung

### 2.3. Link survey response vao ho so 0215

Da them field tren `x_psm.hr.discipline.record`:

- `x_psm_explanation_survey_id`
- `x_psm_explanation_survey_user_input_id`
- `x_psm_explanation_survey_state`
- `x_psm_explanation_rejection_reason`

Da them smart button mo response survey tren form record.

### 2.4. Tao bridge voi survey.user_input

Da them file:

- `models/x_psm_survey_user_input.py`

Noi dung:

- them field `x_psm_0215_record_id` tren `survey.user_input`
- override `_mark_done()` de callback ve record 0215 khi nhan vien submit xong survey

### 2.5. Dong bo answer survey ve snapshot cu

Khi survey hoan tat, module se:

- cap nhat `x_psm_employee_explanation`
- cap nhat `x_psm_explanation_date`
- cap nhat `x_psm_section_ii_feedback`
- tao/cap nhat snapshot trong `x_psm.hr.discipline.explanation`

Nghia la report/mail dang doc field cu van tiep tuc dung duoc.

### 2.6. Sua action gui cho nhan vien

`action_psm_send_to_employee()` hien tai:

- tu dong tao `survey.user_input` neu chua co
- gui email kem link survey
- tao activity cho nhan vien kem link survey

### 2.7. Sua luong tu choi tuong trinh

Wizard `x_psm.hr.discipline.reject.wizard` hien tai:

- luu ly do tu choi ve record
- tao response survey moi
- doi record ve `draft`
- gui email yeu cau lam lai theo link survey moi

## 3. Cac diem chua doi

- Portal template custom cu van con trong source, chua bo hoan toan.
- Route portal custom `submit_section_ii` van con de tuong thich.
- Chu ky nhan vien tren survey chua duoc thay the bang co che ky phap ly; phan nay van de lai tren record 0215 neu can nghiep vu noi bo.

## 4. Kiem tra da chay

- `python -m compileall addons/M02_P0215`
- parse toan bo XML trong module
- regenerate `structure/module_map.json`

## 5. Buoc tiep theo de test

Can upgrade module tren database test va test cac luong:

1. Tao ho so draft -> gui yeu cau tuong trinh.
2. Nhan vien mo link survey va submit.
3. Kiem tra Section II va explanation history da duoc sync.
4. Tu choi tuong trinh -> tao link survey moi.
5. Manager chot phieu sau khi survey da done.
