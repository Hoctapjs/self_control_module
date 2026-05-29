# -*- coding: utf-8 -*-
from markupsafe import Markup

from odoo import models, fields, api, _


class MailActivity(models.Model):
    _inherit = 'mail.activity'

    # OPS specific display state (for offboarding checklist)
    x_psm_0213_ops_display_state = fields.Selection([
        ('pending', 'Pending'),
        ('overdue', 'Overdue'),
        ('done', 'Done'),
    ], string='Trạng thái', compute='_compute_ops_display_state')

    x_psm_0213_is_offboarding_activity = fields.Boolean(
        string='Is 0213 Offboarding Activity',
        compute='_compute_is_offboarding_activity',
        store=True,
        compute_sudo=True,
    )

    @api.depends('res_model', 'res_id')
    def _compute_is_offboarding_activity(self):
        ApprovalRequest = self.env['approval.request'].sudo()
        ops_cat = self.env.ref(
            'M02_P0213.psm_0213_approval_category_resignation',
            raise_if_not_found=False,
        )
        for activity in self:
            is_offboarding = False
            if ops_cat and activity.res_model == 'approval.request' and activity.res_id:
                req = ApprovalRequest.browse(activity.res_id)
                is_offboarding = bool(req.exists() and req.category_id == ops_cat)
            elif ops_cat and activity.res_model == 'hr.employee' and activity.res_id:
                is_offboarding = bool(ApprovalRequest.search_count([
                    ('x_psm_0213_employee_id', '=', activity.res_id),
                    ('category_id', '=', ops_cat.id),
                ]))
            activity.x_psm_0213_is_offboarding_activity = is_offboarding

    @api.depends('active', 'date_deadline', 'state')
    def _compute_ops_display_state(self):
        """active=False => Done, trễ hạn => Overdue, còn lại => Pending"""
        today = fields.Date.today()
        for activity in self:
            if not activity.active:
                activity.x_psm_0213_ops_display_state = 'done'
            elif activity.date_deadline and activity.date_deadline < today:
                activity.x_psm_0213_ops_display_state = 'overdue'
            else:
                activity.x_psm_0213_ops_display_state = 'pending'

    def unlink(self):
        """
        Ngăn xóa activities của OPS Offboarding.
        Thay vào đó archive (active=False) để giữ lại lịch sử checklist.
        """
        ops_cat = self.env.ref('M02_P0213.psm_0213_approval_category_resignation', raise_if_not_found=False)

        if not ops_cat:
            return super().unlink()

        ops_activities = self.filtered(
            lambda a: a.res_model in ['hr.employee', 'approval.request']
            and self._is_ops_offboarding_activity(a, ops_cat)
        )
        others = self - ops_activities

        if others:
            super(MailActivity, others).unlink()

        for activity in ops_activities:
            if activity.active:
                activity.sudo().write({'active': False})
                # Trigger recompute trên approval.request liên quan
                self._trigger_ops_recompute(activity, ops_cat)

        return True

    def _is_ops_offboarding_activity(self, activity, ops_cat):
        """Check if activity belongs to an OPS offboarding request"""
        if activity.res_model == 'approval.request':
            req = self.env['approval.request'].sudo().browse(activity.res_id)
            return req.exists() and req.category_id == ops_cat
        elif activity.res_model == 'hr.employee':
            req = self.env['approval.request'].sudo().search([
                ('x_psm_0213_employee_id', '=', activity.res_id),
                ('category_id', '=', ops_cat.id),
            ], limit=1)
            return bool(req)
        return False

    def _trigger_ops_recompute(self, activity, ops_cat):
        """Trigger recompute on OPS approval.request after activity archive"""
        if activity.res_model == 'approval.request':
            req = self.env['approval.request'].sudo().browse(activity.res_id)
            if req.exists():
                req.modified(['x_psm_0213_employee_activity_ids'])
        elif activity.res_model == 'hr.employee':
            reqs = self.env['approval.request'].sudo().search([
                ('x_psm_0213_employee_id', '=', activity.res_id),
                ('category_id', '=', ops_cat.id),
            ])
            reqs.modified(['x_psm_0213_employee_activity_ids'])

    def _action_done(self, feedback=False, attachment_ids=False):
        """
        Override để trigger recompute checklist sau khi Mark Done.
        """
        ops_cat = self.env.ref('M02_P0213.psm_0213_approval_category_resignation', raise_if_not_found=False)

        res = super()._action_done(feedback=feedback, attachment_ids=attachment_ids)

        if not ops_cat:
            return res

        for activity in self.sudo():
            is_ops_model = activity.res_model in ['hr.employee', 'approval.request']
            if not is_ops_model or not activity.res_id:
                continue

            domain = [
                ('request_status', '=', 'approved'),
                ('category_id', '=', ops_cat.id),
            ]
            if activity.res_model == 'hr.employee':
                domain.append(('x_psm_0213_employee_id', '=', activity.res_id))
            else:
                domain.append(('id', '=', activity.res_id))

            requests = self.env['approval.request'].sudo().search(domain)

            for req in requests:
                pending_activities = self.env['mail.activity'].sudo().search([
                    ('active', '=', True),
                    '|',
                    '&', ('res_model', '=', 'approval.request'), ('res_id', '=', req.id),
                    '&', ('res_model', '=', 'hr.employee'), ('res_id', '=', req.x_psm_0213_employee_id.id if req.x_psm_0213_employee_id else 0),
                ])
                pending_count = len(req._filter_0213_offboarding_activities(pending_activities))

                if pending_count == 0 and req.x_psm_0213_is_plan_launched:
                    subtype = self.env.ref(
                        'M02_P0213.mail_mt_0213_notification',
                        raise_if_not_found=False,
                    )
                    body = Markup(
                        "<div class='o_0213_success'><i class='fa fa-check-circle'></i> %s</div>"
                    ) % _("Thông báo hệ thống: Tất cả các công việc trong checklist đã được hoàn thành.")
                    post_kwargs = {
                        'body': body,
                    }
                    if subtype:
                        post_kwargs['subtype_id'] = subtype.id
                    req.message_post(**post_kwargs)

                req.sudo().modified(['x_psm_0213_employee_activity_ids'])

        return res
