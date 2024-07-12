from odoo import models, fields, api, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    is_booking = fields.Boolean(string='Is Booking', default=False)
    qty = fields.Float(string='Quantity', default=1.0)

    @api.model
    def create(self, vals):
        print('method ini di klik')
        if vals.get('is_booking'):
            sequence_code = 'sale.order.booking'
        else:
            sequence_code = 'sale.order'
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code(sequence_code) or _('New')
        res = super(SaleOrder, self).create(vals)
        return res
