# -*- coding: utf-8 -*-
{
    "name": "M02_P0213_0214_DEMO_DATA",
    "summary": "Sample data for testing offboarding 0213 and 0214, focused on annual leave.",
    "description": """
Sample Data Module for M02_P0213 and M02_P0214
==============================================
Provides focused demo data for annual leave testing:
- OPS 0213 and RST 0214 employees with positive, zero, and advance AL balances.
- Annual leave types and allocations dedicated to each process.
- Draft resignation requests with AL deduction values ready for UI/manual testing.
- Post-init setup validates leave allocations/requests and updates demo AL balances.
""",
    "author": "PSM",
    "category": "Human Resources",
    "version": "19.0.1.0.0",
    "depends": [
        "M02_P0200",
        "M02_P0213",
        "M02_P0214",
    ],
    "data": [
        "data/offboarding_al_demo_data.xml",
    ],
    "post_init_hook": "post_init_hook",
    "installable": True,
    "application": False,
    "license": "LGPL-3",
    "auto_install": False,
}
