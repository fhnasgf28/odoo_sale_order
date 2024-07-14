from odoo import models, fields, api, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    is_booking = fields.Boolean(string='Is Booking', default=False)

    @api.model
    def create(self, vals):
        if vals.get('is_booking'):
            sequence_code = 'sale.order.line'
        else:
            sequence_code = 'sale.order'
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code(sequence_code) or _('New')
        res = super(SaleOrder, self).create(vals)
        return res


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    qty_booking = fields.Float(string='Quantity Booking', default=1.0, store=True)
    product_template_id = fields.Many2one('product.template', string='Product Template')

    @api.onchange('product_uom_qty')
    def _onchange_qty_booking(self):
        for line in self:
            line.qty_booking = line.product_uom_qty

    @api.onchange('product_id', 'price_unit', 'product_uom_qty')
    def _onchange_product_id(self):
        for line in self:
            if line.order_id.is_booking:
                line.price_subtotal = line.price_unit * line.product_uom_qty * 1.1
            else:
                line.price_subtotal = line.price_unit * line.product_uom_qty

