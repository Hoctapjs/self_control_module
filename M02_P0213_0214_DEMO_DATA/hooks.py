# -*- coding: utf-8 -*-
import logging

_logger = logging.getLogger(__name__)

MODULE = "M02_P0213_0214_DEMO_DATA"

AL_BALANCES = {
    "emp_psm_0213_al_positive": 12.0,
    "emp_psm_0213_al_zero": 0.0,
    "emp_psm_0213_al_advance": -7.0,
    "emp_psm_0214_al_positive": 10.0,
    "emp_psm_0214_al_zero": 0.0,
    "emp_psm_0214_al_advance": -8.0,
}


def _ref(env, xmlid):
    return env.ref("%s.%s" % (MODULE, xmlid), raise_if_not_found=False)


def _validate_records(records):
    for record in records:
        try:
            if getattr(record, "state", False) != "validate":
                record._action_validate()
        except Exception as exc:
            _logger.warning(
                "Demo AL setup skipped validation for %s(%s): %s",
                record._name,
                record.id,
                exc,
            )


def post_init_hook(env):
    vals = {}
    leave_type_0213 = _ref(env, "leave_type_psm_0213_demo_al")
    leave_type_0214 = _ref(env, "leave_type_psm_0214_demo_al")
    if leave_type_0213:
        vals["x_psm_0213_al_leave_type_ids"] = [(4, leave_type_0213.id)]
    if leave_type_0214:
        vals["x_psm_0214_al_leave_type_ids"] = [(4, leave_type_0214.id)]
    if vals:
        env.company.sudo().write(vals)

    allocations = env["hr.leave.allocation"].browse()
    leaves = env["hr.leave"].browse()
    for xmlid in (
        "allocation_psm_0213_al_positive",
        "allocation_psm_0213_al_zero",
        "allocation_psm_0213_al_advance",
        "allocation_psm_0214_al_positive",
        "allocation_psm_0214_al_zero",
        "allocation_psm_0214_al_advance",
    ):
        record = _ref(env, xmlid)
        if record:
            allocations |= record

    for xmlid in (
        "leave_psm_0213_al_zero",
        "leave_psm_0213_al_advance",
        "leave_psm_0214_al_zero",
        "leave_psm_0214_al_advance",
    ):
        record = _ref(env, xmlid)
        if record:
            leaves |= record

    _validate_records(allocations.sudo())
    _validate_records(leaves.sudo())

    for xmlid, balance in AL_BALANCES.items():
        employee = _ref(env, xmlid)
        if employee:
            employee.sudo().write({"x_psm_0200_remaining_al_days": balance})
