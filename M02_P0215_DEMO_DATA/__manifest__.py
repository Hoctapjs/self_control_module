# -*- coding: utf-8 -*-
{
    "name": "M02_P0215_DEMO_DATA",
    "summary": """
        Sample data for testing the employee discipline process 0215.
    """,
    "description": """
        Sample Data Module for M02_P0215
        ================================
        Provides demo data including:
        - Sample employees for the main roles in process 0215.
        - Sample discipline records in representative states.
        - Data for quick testing of Store Level, Company Level, and repeat-offense paths.
        - Matrix data for testing the violation-person-count report by date range.
    """,
    "author": "PSM",
    "category": "Human Resources",
    "version": "19.0.2",
    "depends": [
        "M02_P0215",
    ],
    "data": [
        "data/x_psm_hr_discipline_demo_data.xml",
    ],
    "installable": True,
    "application": False,
    "license": "LGPL-3",
    "auto_install": False,
}
