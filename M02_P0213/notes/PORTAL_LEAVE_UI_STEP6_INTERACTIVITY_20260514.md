# Portal Leave UI - Step 6 Interactivity

Date: 2026-05-14

Blueprint: `notes/BLUEPRINT_PORTAL_LEAVE_REQUEST_0213_V1.md`

## Files Changed

- `__manifest__.py`
- `views/resignation_portal_template.xml`
- `static/src/js/portal_resignation_0213.js`

## Result

- Added `M02_P0213/static/src/js/portal_resignation_0213.js` to `web.assets_frontend`.
- Added progress nav click handling:
  - Prevents default anchor jump.
  - Smooth-scrolls to the target section.
  - Updates `.is-active` on the clicked progress item.
  - Updates `aria-current="step"` for accessibility.
- Added `IntersectionObserver` support:
  - Updates active progress item while scrolling through sections.
  - Gracefully does nothing in browsers without `IntersectionObserver`.
- Script is scoped to `.o_psm_0213_portal` and exits immediately when the page is not the 0213 portal form.

## Scope Guard

- No controller, model, route, permission, or business logic changed.
- Submit action remains `/my/resignation/submit`.
- CSRF token and submitted field names remain unchanged.
- Activity done action remains `/my/resignation/ops/activity/done`.
