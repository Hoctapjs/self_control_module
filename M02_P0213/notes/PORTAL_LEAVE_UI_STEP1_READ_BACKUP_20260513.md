# Portal Leave UI - Step 1 Read And Backup

Date: 2026-05-13

Blueprint: `notes/BLUEPRINT_PORTAL_LEAVE_REQUEST_0213_V1.md`

## Files Read

- `convention/QUY_UOC_DAT_TEN_VA_RULE.md`
- `structure/module_map.json`
- `__manifest__.py`
- `views/resignation_portal_template.xml`

## Backup

- Source: `views/resignation_portal_template.xml`
- Backup: `notes/backups/resignation_portal_template.step1.20260513.bak`
- Backup extension is `.bak` so Odoo does not load it as a view file.

## Current Template State

- Portal template id: `view_psm_0213_resignation_portal_template`
- Current wrapper class: `.psm-ops-resignation-portal`
- CSS is currently inline inside the QWeb template.
- `__manifest__.py` loads `views/resignation_portal_template.xml` through `data`.
- No portal UI asset bundle is declared in the manifest yet.

## Functional Points To Preserve In Later Steps

- Submit form action: `/my/resignation/submit`
- Submit method: `post`
- CSRF input: `request.csrf_token()`
- Activity done action: `/my/resignation/ops/activity/done`
- Required submitted fields:
  - `resignation_date`
  - `resignation_type_id`
  - `resignation_reason`
- Hidden approver field:
  - `approver_user_id`
- Employee information fields are readonly display fields and must not become submitted business inputs unless explicitly required.

## Step 1 Result

Step 1 is complete. No controller, model, route, or form behavior was changed in this step.
