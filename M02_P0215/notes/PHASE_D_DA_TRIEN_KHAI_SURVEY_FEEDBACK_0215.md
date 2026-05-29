# Phase D - Da trien khai survey cho feedback cai thien ngay 0215

Ngay cap nhat: 2026-05-07

## 1. Tai lieu da dung

- Convention: `addons/M02_P0215/convention/QUY_UOC_DAT_TEN_VA_RULE.md`
- JSON map: `addons/M02_P0215/structure/module_map.json`
- JSON stats: `addons/M02_P0215/structure/module_map_stats.json`
- Source xac nhan:
  - `addons/M02_P0215/models/x_psm_hr_discipline_record.py`
  - `addons/M02_P0215/models/x_psm_survey_user_input.py`
  - `addons/M02_P0215/data/survey_feedback_data.xml`
  - `addons/M02_P0215/views/x_psm_hr_discipline_record_views.xml`
  - `addons/M02_P0215/__manifest__.py`

## 2. Pham vi da lam

### 2.1. Tao survey template feedback

Da them file:

- `data/survey_feedback_data.xml`

Survey feedback gom cac cau hoi:

- Van de can cai thien
- Nguyen nhan
- Huong dan da trao doi
- Cam ket cua nhan vien
- Thoi gian theo doi
- Ket qua sau theo doi

### 2.2. Them field link survey feedback vao ho so

Da them tren `x_psm.hr.discipline.record`:

- `x_psm_feedback_survey_id`
- `x_psm_feedback_survey_user_input_id`
- `x_psm_feedback_survey_state`
- `x_psm_feedback_completed_date`

### 2.3. Bridge callback survey feedback

Da mo rong bridge `survey.user_input`:

- them `x_psm_0215_flow_type`
- khi submit xong se dispatch:
  - `explanation` -> callback tuong trinh
  - `feedback` -> callback feedback

### 2.4. Sua action no_repeat

`action_psm_rgm_no_repeat()` hien tai:

- gan action `feedback`
- chuyen record sang `proposal`
- tao `survey.user_input` cho feedback
- tra ve action mo survey feedback ngay tren frontend survey

### 2.5. Dong bo feedback ve ho so

Khi survey feedback hoan tat:

- sync noi dung ve:
  - `x_psm_section_iii_identification`
  - `x_psm_section_iv_agreement`
- ghi `x_psm_feedback_completed_date`
- neu record dang o `proposal` thi chuyen sang `active`
- set `x_psm_start_date = today`

Huong nay dung lai improvement period cua action `feedback` de theo doi 30 ngay.

### 2.6. Hien thi tren form

Da them:

- smart button response feedback
- group "Feedback Survey"
- nut mo survey feedback neu response chua done
- nut xem response feedback

Da doi label nut RGM:

- `Khong tai pham -> Feedback`

## 3. Cac diem chua lam trong phase nay

- Chua cap nhat portal RGM de mo link feedback survey ngay tren portal.
- Chua cap nhat report PDF de in rieng noi dung feedback.
- Chua tach state rieng cho nhanh feedback; tam thoi van dung `proposal -> active`.

## 4. Kiem tra da chay

- `python -m compileall addons/M02_P0215`
- parse toan bo XML trong module
- regenerate `structure/module_map.json`

## 5. Luong sau thay doi

`under_review`
-> RGM chon `Khong tai pham -> Feedback`
-> `proposal` + tao survey feedback
-> manager/RGM hoan tat survey
-> `active`
-> cron/thu cong het hieu luc theo improvement period
