from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    quantity_booking = fields.Float(string='Quantity Booking', compute='_compute_quantity_booking')
    quantity_after_booking = fields.Float(string='Quantity After Booking', compute='_compute_qty_after_booking')

    @api.depends('product_variant_ids')
    def _compute_quantity_booking(self):
        print('method ini di triger')
        for template in self:
            total_qty_booking = 0
            for product in template.product_variant_ids:
                orders = self.env['sale.order.line'].search([('product_id', '=', product.id)])
                total_qty_booking += sum(order.qty_booking for order in orders)
            template.quantity_booking = total_qty_booking

    @api.depends('quantity_booking', 'qty_available')
    def _compute_qty_after_booking(self):
        print('method on hand ini di klik')
        for template in self:
            template.quantity_after_booking = template.qty_available - template.quantity_booking
