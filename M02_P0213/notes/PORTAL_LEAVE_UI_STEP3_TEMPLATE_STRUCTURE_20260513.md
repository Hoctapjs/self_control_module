# Portal Leave UI - Step 3 Template Structure

Date: 2026-05-13

Blueprint: `notes/BLUEPRINT_PORTAL_LEAVE_REQUEST_0213_V1.md`

## Files Changed

- `views/resignation_portal_template.xml`

## Result

- Replaced portal UI scope from `.psm-ops-resignation-portal` to `.o_psm_0213_portal`.
- Updated the inline CSS scope to the same `.o_psm_0213_portal` class so existing portal status/task styles remain scoped.
- Added `class="psm-resignation-form"` to the resignation submit form.
- Refactored the form banner into `.psm-form-header` with:
  - `.psm-form-header__title`
  - `.psm-form-header__seal`
  - `.psm-form-header__tagline`
  - `.psm-form-header__subtitle`
- Wrapped the form body into three stable sections:
  - `#psm-section-1` / `.psm-form-section`: employee information
  - `#psm-section-2` / `.psm-form-section`: resignation information
  - `#psm-section-3` / `.psm-form-section`: confirmation and commitments
- Added `.psm-section__head`, `.psm-section__index`, and `.psm-section__title` structure for each section.

## Scope Guard

- Submit action remains `/my/resignation/submit`.
- Submit method remains `post`.
- CSRF token remains `request.csrf_token()`.
- Existing submitted field names remain unchanged:
  - `resignation_date`
  - `resignation_type_id`
  - `resignation_reason`
  - `approver_user_id`
- Existing readonly employee fields remain readonly.
- Activity done action remains `/my/resignation/ops/activity/done`.
- No controller, model, route, permission, or business logic changed.

## Next Step

Step 4 should implement the visual component CSS for the new classes.
