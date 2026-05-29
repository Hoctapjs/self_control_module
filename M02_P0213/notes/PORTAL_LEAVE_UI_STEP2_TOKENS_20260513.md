# Portal Leave UI - Step 2 Tokens

Date: 2026-05-13

Blueprint: `notes/BLUEPRINT_PORTAL_LEAVE_REQUEST_0213_V1.md`

## Files Changed

- `__manifest__.py`
- `static/src/scss/portal_resignation_0213.scss`

## Result

- Added `web.assets_frontend` entry for `M02_P0213/static/src/scss/portal_resignation_0213.scss`.
- Added scoped CSS variables under `.o_psm_0213_portal`.
- Added palette tokens using the required McDonald's colors:
  - `--psm-0213-yellow: #FFC72C`
  - `--psm-0213-red: #DA291C`
  - `--psm-0213-black: #000000`
  - `--psm-0213-white: #FFFFFF`
- Added semantic, spacing, radius, typography, line-height, letter-spacing, shadow, and transition tokens.

## Scope Guard

- No route, controller, model, form action, field name, readonly, or CSRF behavior changed.
- No global CSS selectors were added.
- The token scope is `.o_psm_0213_portal`, matching the blueprint and avoiding conflict with 0215.
- The existing template wrapper remains unchanged in this step. Wrapper refactor belongs to step 3.
