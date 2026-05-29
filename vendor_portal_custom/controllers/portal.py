from odoo import http, _
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from odoo.http import request

class VendorPortal(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        
        if 'receipt_count' in counters:
            Picking = request.env['stock.picking'].sudo()
            domain = [
                ('partner_id', '=', request.env.user.partner_id.id),
                ('picking_type_id.code', '=', 'incoming')
            ]
            receipt_count = Picking.search_count(domain)
            values['receipt_count'] = receipt_count
            
        return values

    @http.route(['/my/receipts', '/my/receipts/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_receipts(self, page=1, sortby=None, **kw):
        values = self._prepare_portal_layout_values()
        Picking = request.env['stock.picking'].sudo()

        domain = [
            ('partner_id', '=', request.env.user.partner_id.id),
            ('picking_type_id.code', '=', 'incoming')
        ]

        searchbar_sortings = {
            'date': {'label': _('Scheduled Date'), 'order': 'scheduled_date desc'},
            'name': {'label': _('Reference'), 'order': 'name'},
            'state': {'label': _('Status'), 'order': 'state'},
        }

        if not sortby:
            sortby = 'date'
        sort_order = searchbar_sortings[sortby]['order']

        receipt_count = Picking.search_count(domain)

        pager = portal_pager(
            url="/my/receipts",
            url_args={'sortby': sortby},
            total=receipt_count,
            page=page,
            step=self._items_per_page
        )

        receipts = Picking.search(domain, order=sort_order, limit=self._items_per_page, offset=pager['offset'])

        values.update({
            'receipts': receipts,
            'page_name': 'receipt',
            'pager': pager,
            'default_url': '/my/receipts',
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
        })
        return request.render("vendor_portal_custom.portal_my_receipts", values)

    @http.route(['/my/receipts/<int:receipt_id>'], type='http', auth="user", website=True)
    def portal_my_receipt_detail(self, receipt_id, **kw):
        receipt_sudo = request.env['stock.picking'].sudo().browse(receipt_id)
        
        # Security check: Make sure this receipt belongs to the user and is an incoming receipt
        if not receipt_sudo.exists() or receipt_sudo.partner_id != request.env.user.partner_id or receipt_sudo.picking_type_id.code != 'incoming':
            return request.redirect('/my')

        values = self._prepare_portal_layout_values()
        values.update({
            'receipt': receipt_sudo,
            'page_name': 'receipt',
        })
        
        return request.render("vendor_portal_custom.portal_receipt_page", values)
