# -*- coding: utf-8 -*-
import base64

from odoo import http
from odoo.http import request


class PortalResignationRST(http.Controller):
    def _split_csv_values(self, raw_value):
        return {
            value.strip().upper()
            for value in (raw_value or "").split(",")
            if value.strip()
        }

    def _get_portal_employee(self):
        return request.env["approval.request"].sudo()._find_rst_employee(
            partner=request.env.user.partner_id,
            user=request.env.user,
        )

    def _is_rst_portal_employee(self, employee):
        if not employee or not employee.department_id or not employee.department_id.block_id:
            return False

        block = employee.department_id.block_id
        codes_param = request.env['x_psm_parameter'].get_param('x_psm_0214_portal_block_codes', 'RST')
        names_param = request.env['x_psm_parameter'].get_param('x_psm_0214_portal_block_names', 'HEAD OFFICE')
        allowed_codes = self._split_csv_values(codes_param)
        allowed_names = self._split_csv_values(names_param)
        block_code = (block.code or "").upper()
        block_name = (block.name or "").upper()
        return (block_code in allowed_codes) or (block_name in allowed_names)

    def _get_resignation_category(self):
        return request.env["approval.request"].sudo()._get_resignation_category()

    def _get_latest_resignation_request(self, category):
        return request.env["approval.request"].sudo().search(
            [
                ("request_owner_id", "=", request.env.user.id),
                ("category_id", "=", category.id),
            ],
            order="create_date desc",
            limit=1,
        )

    def _get_owned_resignation_request_by_id(self, request_id):
        category = self._get_resignation_category()
        if not category:
            return request.env["approval.request"].sudo().browse()

        return request.env["approval.request"].sudo().search(
            [
                ("id", "=", request_id),
                ("request_owner_id", "=", request.env.user.id),
                ("category_id", "=", category.id),
            ],
            limit=1,
        )

    def _get_resignation_types(self):
        return request.env["hr.departure.reason"].sudo().search([])

    def _get_resignation_activities(self, resignation_request):
        if (
            not resignation_request
            or not resignation_request.exists()
            or not resignation_request._is_0214_offboarding_request()
        ):
            return request.env["mail.activity"].sudo().browse()

        return (
            request.env["mail.activity"]
            .sudo()
            .with_context(active_test=False)
            .search(
                resignation_request._build_rst_activity_domain(
                    request=resignation_request
                ),
                order="date_deadline asc",
            )
        )

    def _get_current_user_offboarding_activities(self):
        category = self._get_resignation_category()
        activity_model = request.env["mail.activity"].sudo().with_context(
            active_test=False
        )
        if not category:
            return activity_model.browse()

        activities = activity_model.search(
            [
                ("user_id", "=", request.env.user.id),
                ("res_model", "in", ["approval.request", "hr.employee"]),
            ],
            order="active desc, date_deadline asc, create_date desc",
        )
        return activities.filtered(
            lambda activity: activity_model._is_rst_offboarding_activity(
                activity,
                category,
            )
        )

    def _get_or_create_exit_survey_url(self, resignation_request):
        if (
            not resignation_request
            or resignation_request.request_status not in ["approved", "done"]
            or resignation_request.x_psm_0214_exit_survey_completed
        ):
            return False

        partner = request.env.user.partner_id
        user_input = (
            request.env["approval.request"]
            .sudo()
            ._get_or_create_rst_survey_user_input(
                partner=partner,
                resignation_request=resignation_request,
                create_if_missing=True,
            )
        )
        return user_input.get_start_url() if user_input else False

    @http.route(["/my/resignation"], type="http", auth="user", website=True)
    def portal_resignation_unified(self, **kw):
        employee = self._get_portal_employee()

        if self._is_rst_portal_employee(employee):
            return request.redirect("/my/resignation/rst")

        return request.redirect("/my/resignation/ops")

    @http.route(["/my/resignation/rst"], type="http", auth="user", website=True)
    def portal_resignation_form(self, **kw):
        partner = request.env.user.partner_id
        employee = self._get_portal_employee()
        category = self._get_resignation_category()
        resignation_request = (
            self._get_latest_resignation_request(category)
            if category
            else request.env["approval.request"].sudo().browse()
        )

        activities = []
        survey_url = False
        if resignation_request:
            activities = self._get_resignation_activities(resignation_request)
            survey_url = self._get_or_create_exit_survey_url(resignation_request)

        success = kw.get("success")
        resignation_types = self._get_resignation_types()

        return request.render(
            "M02_P0214.view_psm_resignation_portal_template",
            {
                "partner": partner,
                "employee": employee,
                "success": success,
                "resignation_request": resignation_request,
                "activities": activities,
                "survey_url": survey_url,
                "resignation_types": resignation_types,
            },
        )

    @http.route(
        ["/my/resignation/rst/activity/done"],
        type="http",
        auth="user",
        methods=["POST"],
        website=True,
        csrf=True,
    )
    def portal_activity_done(self, **post):
        activity_id = int(post.get("activity_id", 0))
        if not activity_id:
            return request.redirect("/my/resignation/rst")

        activity = request.env["mail.activity"].sudo().browse(activity_id)
        owned_request = False
        if activity.exists():
            if activity.res_model == "approval.request":
                owned_request = self._get_owned_resignation_request_by_id(activity.res_id)
            elif activity.res_model == "hr.employee":
                latest_request = self._get_latest_resignation_request(
                    self._get_resignation_category()
                )
                if (
                    latest_request
                    and latest_request.x_psm_0214_employee_id
                    and latest_request.x_psm_0214_employee_id.id == activity.res_id
                ):
                    owned_request = latest_request

        if owned_request and activity.user_id == request.env.user:
            activity.sudo().action_feedback(feedback="Completed from Portal")

        return request.redirect("/my/resignation/rst?activity_done=1")

    @http.route(["/my/offboarding"], type="http", auth="user", website=True)
    def portal_offboarding_activities(self, **kw):
        activities = self._get_current_user_offboarding_activities()
        return request.render(
            "M02_P0214.view_psm_offboarding_activities_portal",
            {
                "activities": activities,
                "done": kw.get("done"),
            },
        )

    @http.route(
        ["/my/offboarding/activity/done"],
        type="http",
        auth="user",
        methods=["POST"],
        website=True,
        csrf=True,
    )
    def portal_offboarding_activity_done(self, **post):
        try:
            activity_id = int(post.get("activity_id", 0))
        except (TypeError, ValueError):
            activity_id = 0

        activity_model = request.env["mail.activity"].sudo()
        activity = activity_model.browse(activity_id)
        category = self._get_resignation_category()
        if (
            activity.exists()
            and category
            and activity.user_id == request.env.user
            and activity_model._is_rst_offboarding_activity(activity, category)
        ):
            activity.sudo().action_feedback(
                feedback="Confirmed from Portal — Pending Activities"
            )

        return request.redirect("/my/offboarding?done=1")

    @http.route(
        ["/my/resignation/rst/settlement/download/<int:request_id>"],
        type="http",
        auth="user",
        website=True,
    )
    def portal_settlement_download(self, request_id, **kw):
        resignation_request = self._get_owned_resignation_request_by_id(request_id)
        if (
            not resignation_request
            or not resignation_request.x_psm_0214_settlement_sent
            or not resignation_request.x_psm_0214_salary_settlement_file
        ):
            return request.not_found()

        filename = (
            resignation_request.x_psm_0214_salary_settlement_filename
            or "quyet_toan_luong.pdf"
        )
        headers = [
            ("Content-Type", "application/pdf"),
            ("Content-Disposition", f'attachment; filename="{filename}"'),
        ]
        content = base64.b64decode(resignation_request.x_psm_0214_salary_settlement_file)
        return request.make_response(content, headers=headers)

    @http.route(
        ["/my/resignation/rst/settlement/upload"],
        type="http",
        auth="user",
        methods=["POST"],
        website=True,
        csrf=True,
    )
    def portal_settlement_upload(self, **post):
        try:
            request_id = int(post.get("request_id", 0))
        except (TypeError, ValueError):
            request_id = 0

        resignation_request = self._get_owned_resignation_request_by_id(request_id)
        upload = post.get("signed_settlement_file")
        if resignation_request and upload:
            resignation_request.sudo().write(
                {
                    "x_psm_0214_signed_settlement_file": base64.b64encode(
                        upload.read()
                    ),
                    "x_psm_0214_signed_settlement_filename": upload.filename,
                }
            )

        return request.redirect("/my/resignation/rst?settlement_uploaded=1")

    @http.route(
        ["/my/resignation/rst/submit"],
        type="http",
        auth="user",
        methods=["POST"],
        website=True,
        csrf=True,
    )
    def portal_resignation_submit(self, **post):
        partner = request.env.user.partner_id
        employee = self._get_portal_employee()
        category = self._get_resignation_category()

        vals = {
            "name": f"Offboarding Request - {partner.name}",
            "category_id": category.id if category else False,
            "partner_id": partner.id,
            "x_psm_0214_resignation_reason_id": (
                int(post.get("x_psm_0214_resignation_reason_id"))
                if post.get("x_psm_0214_resignation_reason_id")
                else False
            ),
            "x_psm_0214_resignation_reason": post.get("x_psm_0214_resignation_reason"),
            "x_psm_0214_resignation_date": post.get("x_psm_0214_resignation_date")
            or False,
            "x_psm_0214_employee_id": employee.id if employee else False,
            "x_psm_0214_employee_personal_email": post.get(
                "x_psm_0214_employee_personal_email"
            )
            or False,
            "request_owner_id": request.env.user.id,
        }

        if employee and employee.parent_id and employee.parent_id.user_id:
            vals["approver_ids"] = [
                (
                    0,
                    0,
                    {
                        "user_id": employee.parent_id.user_id.id,
                        "status": "new",
                        "required": True,
                    },
                )
            ]

        approval_request = request.env["approval.request"].sudo().create(vals)
        approval_request.sudo().action_confirm()

        return request.redirect("/my/resignation/rst?success=1")
