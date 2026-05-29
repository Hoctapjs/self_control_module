# Violation Person Count Report Test Matrix 0215

Module `M02_P0215_DEMO_DATA` includes dedicated sample data for testing this menu:

`Employee Discipline / Reports / Violation Person Count`

Related accounts:

- `demo0215_sm`: Shift Manager; should only see employees in Store Operations.
- `demo0215_hrbp`: HRBP; used to test broader company-level access.
- `demo0215_hrmgr`: HR Manager / approver.
- `demo0215_emp_c`: Employee C, assigned to the HR department to test department-based access differences against SM.

## Matrix

| Case | Suggested user | Date from | Date to | Filters | Expected result |
| --- | --- | --- | --- | --- | --- |
| 1 | HRBP / HR Manager | 2026-04-01 | 2026-04-05 | State: All, Exclude cancelled | Violating people = 3, Records = 5 |
| 2 | HRBP / HR Manager | 2026-04-10 | 2026-04-12 | State: All, Exclude cancelled | Violating people = 1, Records = 3 |
| 3A | HRBP / HR Manager | 2026-04-24 | 2026-04-27 | State: All, Exclude cancelled | Violating people = 3, Records = 3 |
| 3B | HRBP / HR Manager | 2026-04-24 | 2026-04-27 | State: All, Include cancelled | Violating people = 3, Records = 4 |
| 4 | HRBP / HR Manager | 2026-04-24 | 2026-04-27 | State: Active, Exclude cancelled | Violating people = 2, Records = 2 |
| 5 | HRBP / HR Manager | 2026-12-01 | 2026-12-31 | State: All, Exclude cancelled | Violating people = 0, Records = 0 |
| 6 | HRBP / HR Manager | 2026-04-30 | 2026-04-01 | Any | The system should raise an error because Date From is later than Date To |
| 7A | `demo0215_sm` | 2026-04-28 | 2026-04-29 | State: All, Exclude cancelled | Violating people = 2, Records = 2 |
| 7B | `demo0215_hrbp` / `demo0215_hrmgr` | 2026-04-28 | 2026-04-29 | State: All, Exclude cancelled | Violating people = 3, Records = 3 |

## Sample Records

- Case 1: `REPORT-0215-CASE1-A1`, `REPORT-0215-CASE1-A2`, `REPORT-0215-CASE1-B1`, `REPORT-0215-CASE1-B2`, `REPORT-0215-CASE1-C1`
- Case 2: `REPORT-0215-CASE2-A1`, `REPORT-0215-CASE2-A2`, `REPORT-0215-CASE2-A3`
- Case 3/4: `REPORT-0215-CASE3-ACTIVE-A`, `REPORT-0215-CASE3-DRAFT-B`, `REPORT-0215-CASE3-ACTIVE-C`, `REPORT-0215-CASE3-CANCEL-A`
- Case 7: `REPORT-0215-CASE7-STORE-A`, `REPORT-0215-CASE7-STORE-B`, `REPORT-0215-CASE7-HR-C`

The wizard detail-list button should return the matching records for the selected date range, and the detail row count should match `Records`.
