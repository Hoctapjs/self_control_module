from odoo import http, _
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
import datetime
import base64


class DisciplinePortal(CustomerPortal):
    def _x_psm_employee_model(self):
        return request.env["hr.employee"].sudo()

    def _x_psm_record_model(self):
        return request.env["x_psm.hr.discipline.record"].sudo()

    def _x_psm_empty_records(self):
        return self._x_psm_record_model().browse()

    def _x_psm_to_int(self, value):
        try:
            return int(value or 0)
        except (TypeError, ValueError):
            return 0

    def _x_psm_redirect_record(self, record, success=None, error=None):
        url = f"/my/discipline/{record.id}" if record else "/my/disciplines"
        if success:
            url = f"{url}?success={success}"
        if error:
            separator = "&" if "?" in url else "?"
            url = f"{url}{separator}error={error}"
        return request.redirect(url)

    def _x_psm_has_portal_signature(self, signature):
        return bool(signature) and len(signature) >= 500

    def _get_employee_from_user(self):
        """
        Helper method to find the employee linked to the current user.
        Priority 1: Linked via user_id field in hr.employee
        Priority 2: Matched via work_email == user.login (or user.email)
        """
        user = request.env.user
        Employee = self._x_psm_employee_model()

        # 1. Try direct link
        employee = Employee.search([("user_id", "=", user.id)], limit=1)
        if employee:
            return employee

        # 2. Try email match (Common for Portal Users)
        # Check both login and email just to be safe
        emails_to_check = [user.login, user.email]
        emails_to_check = [e for e in emails_to_check if e]  # Filter None

        if emails_to_check:
            employee = Employee.search([("work_email", "in", emails_to_check)], limit=1)

        return employee

    def _x_psm_get_subordinates(self, employee):
        if not employee:
            return self._x_psm_employee_model().browse()
            
        user = request.env.user
        # High level groups see everyone in the organization
        if user.has_group("M02_P0200.GDH_RST_OPS_OC_S"):
            return self._x_psm_employee_model().search([("department_id.block_code", "=", "OPS")])

        if user.has_group("M02_P0200.GDH_RST_HR_HRBP_S") or \
           user.has_group("M02_P0200.GDH_RST_SYSTEM_ST_M"):
            return self._x_psm_employee_model().search([])
            
        # Store level managers see everyone in the same store (department)
        return self._x_psm_employee_model().search(
            [("department_id", "=", employee.department_id.id), ("id", "!=", employee.id)]
        )

    def _x_psm_get_employee_level(self, employee):
        if not employee:
            return False
        if "job_level_id" in employee._fields and employee.job_level_id:
            return employee.job_level_id

        job = employee.job_id
        if job and "level_id" in job._fields:
            return job.level_id
        return False

    def _x_psm_is_manager_employee(self, employee):
        if not employee:
            return False
        
        user = request.env.user
        # Shift Manager and above groups from M02_P0200
        # Note: RGM, PM, ST usually imply SM, but we check explicitly or via base groups.
        # Management groups from M02_P0200
        # HR is excluded from portal manager status as they manage in the backend.
        manager_groups = [
            "M02_P0200.GDH_OPS_STORE_SM_M",   # Shift Manager
            "M02_P0200.GDH_OPS_STORE_RGM_M",  # RGM
            "M02_P0200.GDH_OPS_STORE_PM_M",   # People Manager
            "M02_P0200.GDH_OPS_STORE_ST_M",   # System Manager
            "M02_P0200.GDH_RST_OPS_OC_S",     # Operation Consultant
            "M02_P0200.GDH_RST_SYSTEM_ST_M",  # System Admin
        ]
        
        if any(user.has_group(group) for group in manager_groups):
            return True

        # Fallback: Check traditional Odoo hierarchy (Has Direct Reports)
        if employee.child_ids:
            return True

        return False

    def _x_psm_can_view_record(self, record, employee):
        if not record or not employee:
            return False
        is_subject = record.x_psm_employee_id == employee
        is_parent = record.x_psm_employee_id.parent_id == employee
        is_rep = record.x_psm_company_rep_id == employee
        return is_subject or is_parent or is_rep or self._x_psm_is_manager_employee(employee)

    def _x_psm_can_finalize_record(self, record, employee):
        if not record or not employee:
            return False
        # Allow finalize if: (1) direct manager OR (2) the company rep who created the log
        is_parent = record.x_psm_employee_id.parent_id == employee
        is_rep = record.x_psm_company_rep_id == employee
        return is_parent or is_rep

    def _x_psm_get_record_from_post(self, post):
        record_id = self._x_psm_to_int(post.get("x_psm_record_id"))
        if not record_id:
            return self._x_psm_empty_records()
        return self._x_psm_record_model().browse(record_id).exists()

    def _x_psm_portal_domain(self, employee, is_manager=False):
        if not employee:
            return [("id", "=", -1)]
        
        user = request.env.user
        # OC group sees only OPS records
        if user.has_group("M02_P0200.GDH_RST_OPS_OC_S"):
            return [("x_psm_employee_id.department_id.block_code", "=", "OPS")]

        # High level groups see everything
        if user.has_group("M02_P0200.GDH_RST_HR_HRBP_S") or \
           user.has_group("M02_P0200.GDH_RST_SYSTEM_ST_M"):
            return []
            
        if is_manager:
            subordinates = self._x_psm_get_subordinates(employee)
            return [
                "|",
                ("x_psm_employee_id", "=", employee.id),
                ("x_psm_employee_id", "in", subordinates.ids),
            ]
        
        # Regular employees only see their own records
        return [("x_psm_employee_id", "=", employee.id)]

    def _prepare_portal_layout_values(self):
        values = super()._prepare_portal_layout_values()
        employee = self._get_employee_from_user()
        if employee:
            is_manager = self._x_psm_is_manager_employee(employee)
            # Task 5: count of records where employee is the subject and needs attention
            pending_domain = [
                ("x_psm_employee_id", "=", employee.id),
                ("x_psm_portal_needs_attention", "=", True),
            ]
            values["discipline_needs_action_count"] = self._x_psm_record_model().search_count(pending_domain)

        else:
            values["discipline_needs_action_count"] = 0
        return values

    @http.route(["/my", "/my/home"], type="http", auth="user", website=True)
    def home(self, **kw):
        return super().home(**kw)

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)

        if "discipline_count" in counters or not counters:
            employee = self._get_employee_from_user()
            if employee:
                is_manager = self._x_psm_is_manager_employee(employee)
                domain = self._x_psm_portal_domain(employee, is_manager)
                values["discipline_count"] = self._x_psm_record_model().search_count(domain)
            else:
                values["discipline_count"] = 0

        return values

    @http.route(
        ["/my/disciplines", "/my/disciplines/page/<int:page>"],
        type="http",
        auth="user",
        website=True,
    )
    def portal_psm_my_disciplines(
        self, page=1, date_begin=None, date_end=None, sortby=None, **kw
    ):
        values = self._prepare_portal_layout_values()
        HrDisciplineRecord = self._x_psm_record_model()

        # Smart Lookup
        employee = self._get_employee_from_user()

        # Check if user is a manager (to see subordinates' records)
        if employee:
            # Domain: Records where employee is the subject OR employee is the manager of the subject
            is_manager = self._x_psm_is_manager_employee(employee)
            domain = self._x_psm_portal_domain(employee, is_manager)
        else:
            is_manager = False
            domain = [("id", "=", -1)]

        searchbar_sortings = {
            "date_desc": {"label": _("Mới nhất"), "order": "x_psm_date desc, id desc"},
            "date_asc": {"label": _("Cũ nhất"), "order": "x_psm_date asc, id asc"},
            "state": {"label": _("Theo trạng thái"), "order": "state, x_psm_date desc, id desc"},
            "employee": {
                "label": _("Theo nhân viên"),
                "order": "x_psm_employee_id, x_psm_date desc, id desc",
            },
            "name": {"label": _("Theo mã hồ sơ"), "order": "name, id desc"},
        }
        if not sortby or sortby not in searchbar_sortings:
            sortby = "date_desc"
        order = searchbar_sortings[sortby]["order"]

        # Count for pager
        discipline_count = HrDisciplineRecord.search_count(domain)

        # Pager logic
        pager = portal_pager(
            url="/my/disciplines",
            url_args={"date_begin": date_begin, "date_end": date_end, "sortby": sortby},
            total=discipline_count,
            page=page,
            step=10,
        )

        disciplines = HrDisciplineRecord.search(
            domain, order=order, limit=10, offset=pager["offset"]
        )

        values.update(
            {
                "date": date_begin,
                "disciplines": disciplines,
                "page_name": "discipline",
                "pager": pager,
                "default_url": "/my/disciplines",
                "searchbar_sortings": searchbar_sortings,
                "sortby": sortby,
                "is_manager": is_manager,
                "total_count": discipline_count,
            }
        )
        return request.render("M02_P0215.portal_psm_my_disciplines", values)



    @http.route(
        ["/my/discipline/create"],
        type="http",
        auth="user",
        website=True,
        methods=["GET", "POST"],
    )
    def portal_psm_discipline_create(self, **post):
        """Manager creates a new Counseling Log from Portal"""
        employee = self._get_employee_from_user()
        subordinates = self._x_psm_get_subordinates(employee)

        if not self._x_psm_is_manager_employee(employee):
            return request.redirect("/my")

        if request.httprequest.method == "POST":
            subject_id = self._x_psm_to_int(post.get("x_psm_employee_id"))
            witness_id = self._x_psm_to_int(post.get("witness_id"))
            violation_category_id = self._x_psm_to_int(post.get("violation_category"))

            if not subject_id or not violation_category_id:
                return request.redirect("/my/discipline/create?error=missing_required")
            if subject_id not in subordinates.ids and subject_id != employee.id:
                return request.redirect("/my")

            # Handle Attachments (Physical Explanation Photos)
            files = request.httprequest.files.getlist("explanation_images")
            
            # Handle Signatures
            manager_sig = post.get("manager_signature")
            employee_sig = post.get("employee_signature")
            
            # Logic: If both signed and section III/IV filled -> under_review, else draft
            has_signatures = manager_sig and employee_sig
            has_identification = post.get("section_iii_identification")
            new_state = "under_review" if has_signatures and has_identification else "draft"

            # Create Record
            HrDisciplineRecord = self._x_psm_record_model()
            vals = {
                "x_psm_employee_id": subject_id,
                "x_psm_witness_id": witness_id or False,
                "x_psm_company_rep_id": employee.id,
                "x_psm_violation_type": post.get("x_psm_violation_type"),
                "x_psm_violation_category_id": violation_category_id,
                "x_psm_discipline_purpose": post.get("x_psm_discipline_purpose"),
                "x_psm_section_i_description": post.get("section_i_description"),
                "x_psm_section_ii_feedback": post.get("section_ii_feedback"),
                "x_psm_section_iii_identification": post.get("section_iii_identification"),
                "x_psm_section_iv_agreement": post.get("section_iv_agreement"),
                "x_psm_date": post.get("x_psm_date") or datetime.date.today(),
                "state": new_state,
            }
            if manager_sig:
                vals.update({
                    "x_psm_manager_signature": manager_sig,
                    "x_psm_manager_signature_date": datetime.date.today()
                })
            if employee_sig:
                vals.update({
                    "x_psm_employee_signature": employee_sig,
                    "x_psm_employee_signature_date": datetime.date.today()
                })
            
            witness_sig = post.get("witness_signature")
            if witness_sig:
                vals.update({
                    "x_psm_witness_signature": witness_sig,
                    "x_psm_witness_signature_date": datetime.date.today()
                })
            
            record = HrDisciplineRecord.create(vals)
            if files:
                attachments = []
                for file in files:
                    if file.filename:
                        attachment = (
                            request.env["ir.attachment"]
                            .sudo()
                            .create(
                                {
                                    "name": file.filename,
                                    "datas": base64.b64encode(file.read()),
                                    "res_model": "x_psm.hr.discipline.record",
                                    "res_id": record.id,
                                    "public": True,
                                }
                            )
                        )
                        attachments.append(attachment.id)
                if attachments:
                    record.write({"x_psm_explanation_image_ids": [(6, 0, attachments)]})

            return request.redirect(f"/my/discipline/{record.id}?success=created")

        # GET: Render creation form
        values = {
            "manager_emp": employee,
            "subordinates": subordinates,
            "violation_categories": request.env[
                "x_psm.hr.discipline.violation.category"
            ].sudo().search([]),
            "page_name": "discipline_create",
        }
        return request.render("M02_P0215.portal_psm_discipline_create", values)

    @http.route(
        ["/my/discipline/<int:x_psm_record_id>"], type="http", auth="user", website=True
    )
    def portal_discipline_view(self, x_psm_record_id, **kw):
        record = self._x_psm_record_model().browse(x_psm_record_id).exists()
        current_employee = self._get_employee_from_user()

        if not self._x_psm_can_view_record(record, current_employee):
            return request.redirect("/my")

        # Security: Employee or Manager
        is_manager = (
            record.x_psm_employee_id.parent_id == current_employee
            or record.x_psm_company_rep_id == current_employee
            or self._x_psm_is_manager_employee(current_employee)
        )
        is_subject = record.x_psm_employee_id == current_employee

        if not (is_manager or is_subject):
            return request.redirect("/my")

        # Task 5: Mark read when employee views their own violation record
        if is_subject and record.x_psm_portal_needs_attention:
            record.sudo().write({"x_psm_portal_needs_attention": False})

        values = {
            "record": record,
            "page_name": "discipline_form",
            "is_manager": is_manager,
            "is_subject": is_subject,
            "error": kw.get("error"),
        }
        return request.render(
            "M02_P0215.portal_psm_discipline_explanation_template", values
        )

    @http.route(
        ["/my/discipline/submit_section_ii"],
        type="http",
        auth="user",
        website=True,
        methods=["POST"],
    )
    def portal_discipline_submit_section_ii(self, **post):
        """Legacy fallback: Employee submits Section II and Signature"""
        record = self._x_psm_get_record_from_post(post)
        current_employee = self._get_employee_from_user()

        if not record or record.x_psm_employee_id != current_employee:
            return request.redirect("/my/disciplines")

        employee_signature = post.get("employee_signature")
        if not self._x_psm_has_portal_signature(employee_signature):
            return self._x_psm_redirect_record(record, error="missing_signature")

        record.write(
            {
                "x_psm_employee_explanation": post.get("section_ii_feedback")
                or record.x_psm_section_ii_feedback,
                "x_psm_explanation_date": datetime.date.today(),
                "x_psm_section_ii_feedback": post.get("section_ii_feedback")
                or record.x_psm_section_ii_feedback,
                "x_psm_employee_signature": employee_signature,
                "x_psm_employee_signature_date": datetime.date.today(),
                # Remove state transition to manager_review
            }
        )
        record.message_post(
            body=(
                "Nhân viên đã gửi phản hồi và ký tên trên Portal "
                "(legacy fallback, không qua survey)."
            )
        )

        return self._x_psm_redirect_record(record, success="True")

    @http.route(
        ["/my/discipline/manager_finalize"],
        type="http",
        auth="user",
        website=True,
        methods=["POST"],
    )
    def portal_discipline_manager_finalize(self, **post):
        """Legacy fallback: Manager submits Section III, IV and Signature"""
        record = self._x_psm_get_record_from_post(post)
        current_employee = self._get_employee_from_user()

        if not self._x_psm_can_finalize_record(record, current_employee):
            return request.redirect("/my/disciplines")

        manager_signature = post.get("manager_signature")
        if not self._x_psm_has_portal_signature(manager_signature):
            return self._x_psm_redirect_record(record, error="missing_signature")

        record.write(
            {
                "x_psm_section_iii_identification": post.get(
                    "section_iii_identification"
                )
                or record.x_psm_section_iii_identification,
                "x_psm_section_iv_agreement": post.get("section_iv_agreement")
                or record.x_psm_section_iv_agreement,
                "x_psm_manager_signature": manager_signature,
                "x_psm_manager_signature_date": datetime.date.today(),
                "state": "under_review",
            }
        )
        record.message_post(
            body=(
                "Quản lý đã hoàn tất nội dung III, IV và ký tên chốt "
                "(legacy fallback portal finalize)."
            )
        )

        return self._x_psm_redirect_record(record, success="True")

    @http.route(
        ["/my/discipline/rgm_action"],
        type="http",
        auth="user",
        website=True,
        methods=["POST"],
    )
    def portal_discipline_rgm_action(self, **post):
        """RGM makes decisions on Portal"""
        record = self._x_psm_get_record_from_post(post)
        action_type = post.get("action_type")
        current_employee = self._get_employee_from_user()

        # Security: only the direct manager (RGM) of the employee can act
        if not record or record.x_psm_employee_id.parent_id != current_employee:
            return request.redirect("/my/disciplines")

        if action_type == "no_repeat":
            record.action_psm_rgm_no_repeat()  # -> level_determination
        elif action_type == "set_repeat":
            record.action_psm_rgm_repeat()     # -> level_determination
        elif action_type == "store_level":
            record.action_psm_rgm_store_level()    # -> proposal
        elif action_type == "company_level":
            record.action_psm_rgm_company_level()  # -> investigation

        return self._x_psm_redirect_record(record, success="True")

    @http.route(
        "/my/discipline/respond",
        type="http",
        auth="user",
        methods=["POST"],
        website=True,
    )
    def portal_discipline_respond(self, **post):
        """Bước 9: Nhân viên Chấp nhận hoặc Từ chối hình thức kỷ luật"""
        record = self._x_psm_get_record_from_post(post)
        current_employee = self._get_employee_from_user()

        # Security: only the employee of this record can respond
        if not record or record.x_psm_employee_id != current_employee or record.state != "notified":
            return request.redirect("/my/disciplines")

        respond = post.get("respond")
        if respond == "accept":
            record.action_psm_employee_accept()  # -> active
        elif respond == "reject":
            note = (post.get("note") or "").strip()
            if not note:
                return self._x_psm_redirect_record(record, error="missing_reject_note")
            record.action_psm_employee_reject(note=note)

        return self._x_psm_redirect_record(record)
