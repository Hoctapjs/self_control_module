# Portal Leave UI - Step 5 Progress Nav

Date: 2026-05-13

Blueprint: `notes/BLUEPRINT_PORTAL_LEAVE_REQUEST_0213_V1.md`

## Files Changed

- `views/resignation_portal_template.xml`
- `static/src/scss/portal_resignation_0213.scss`

## Result

- Added a sticky 3-step progress navigation after the form header:
  - `#psm-section-1`: Thong tin
  - `#psm-section-2`: Nghi viec
  - `#psm-section-3`: Xac nhan
- Added progress component CSS:
  - `.psm-form-progress`
  - `.psm-form-progress__dot`
  - `.psm-form-progress__dot.is-active`
  - `.psm-form-progress__number`
- Added `scroll-margin-top` to `.psm-form-section` so anchor jumps do not hide the section title behind the sticky nav.
- Added mobile behavior: progress nav becomes static and compact on small screens.

## Scope Guard

- No JavaScript was added in this step.
- Active state is static on the first item. Dynamic active state belongs to optional step 6.
- Submit action remains `/my/resignation/submit`.
- CSRF token and submitted field names remain unchanged.
- No controller, model, route, permission, or business logic changed.
