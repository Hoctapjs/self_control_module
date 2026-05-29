# Portal Leave UI - Step 4 Component CSS

Date: 2026-05-13

Blueprint: `notes/BLUEPRINT_PORTAL_LEAVE_REQUEST_0213_V1.md`

## Files Changed

- `views/resignation_portal_template.xml`
- `static/src/scss/portal_resignation_0213.scss`

## Result

- Added component classes to the portal form:
  - `psm-form-control`
  - `psm-commitment-panel`
  - `psm-commitment-panel__title`
  - `psm-commitment-panel__intro`
  - `psm-commitment-item`
  - `psm-commitment-item__num`
  - `psm-commitment-item__text`
  - `psm-btn`
  - `psm-btn--danger`
  - `psm-btn--secondary`
  - `psm-alert`
  - `psm-alert--info`
  - `psm-alert--success`
  - `psm-alert--warning`
  - `psm-alert--danger`
- Implemented component CSS for:
  - Header banner
  - Section cards and section title rows
  - Form labels and form controls
  - Commitment panel and numbered commitment items
  - Primary/secondary buttons
  - Status, warning, and error alerts
  - Small-screen button stacking

## Scope Guard

- Submit action remains `/my/resignation/submit`.
- Submit method remains `post`.
- CSRF token remains `request.csrf_token()`.
- Submitted field names remain unchanged:
  - `resignation_date`
  - `resignation_type_id`
  - `resignation_reason`
  - `approver_user_id`
- Existing readonly employee fields remain readonly.
- Activity done action remains `/my/resignation/ops/activity/done`.
- No controller, model, route, permission, or business logic changed.

## Note

The existing inline CSS block in the template is still present for the current status/task cards. New form-control selectors use higher specificity so the step 4 component styles win over the old inline `.form-control` rules.
