from odoo import models, fields, api, _


class SaleOrderOption(models.Model):
    _inherit = 'sale.order.option'

    qty_booking = fields.Float(string='Quantity Booking', compute="_compute_quantity_booking", default=1.0)
    qty_available = fields.Float(string='Quantity After Booking', compute="_compute_quantity_available_after_booking")

    def _compute_quantity_booking(self):
        pass

    @api.depends('quantity', 'qty_booking')
    def _compute_quantity_available_after_booking(self):
        for option in self:
            option.qty_available = option.quantity - option.qty_booking
