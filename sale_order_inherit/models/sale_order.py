from odoo import models, fields, api, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    is_booking = fields.Boolean(string='Is Booking', default=False)

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


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    qty_booking = fields.Float(string='Quantity Booking', default=1.0)

    @api.onchange('product_uom_qty')
    def _onchange_qty_booking(self):
        for line in self:
            line.qty_booking = line.product_uom_qty

    @api.onchange('product_id')
    def _onchange_product_id(self):
        print('method ini di klik')
        for line in self:
            if line.order_id.is_booking and line.product_id:
                line.price_unit = line.product_id.lst_price * 1.10
            else:
                line.price_unit = line.product_id.lst_price

