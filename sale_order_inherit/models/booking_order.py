from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class BookingOrder(models.Model):
    _name = 'sale.booking.order'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Booking order'

    name = fields.Char(string='Booking Reference', required=True, copy=False, readonly=True,
                       default=lambda self: _('New'))
    partner_id = fields.Many2one('res.partner', string='Customer', required=True)
    order_date = fields.Datetime(string='Order Date', required=True, default=fields.Datetime.now)
    order_line_ids = fields.One2many('booking.order.line', 'order_id', string='Order Lines')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
    ], string='Status', readonly=True, default='draft')

    @api.model
    def create(self, vals):
        print('method ini diklik')
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'sale.booking.order') or _('New')
        res = super(BookingOrder, self).create(vals)
        return res

    def action_confirm(self):
        self.state = 'confirmed'

    def action_cancel(self):
        self.state = 'cancel'
        for record in self:
            if record.state == 'done':
                raise UserError('Completed bookings cannot be cancelled')

    def action_done(self):
        self.state = 'done'
        return {
            'effect': {
                'fadeout': 'slow',
                'message': 'Done Succesfully',
                'type': 'rainbow_man',
            }
        }

    def set_to_draft(self):
        if self.state == 'done':
            raise ValidationError("You cannot reset to draft from the 'Done' state.")
        self.state = 'draft'


class BookingOrderLine(models.Model):
    _name = 'booking.order.line'
    _description = 'Booking Order Line'

    order_id = fields.Many2one('sale.booking.order', string='Booking Order', required=True, ondelete='cascade')
    product_id = fields.Many2one('product.product', string='Product', required=True)
    product_uom_qty = fields.Float('Quantity', required=True)
    price_unit = fields.Float(string='Unit Price', required=True)
    price_subtotal = fields.Float(string='Subtotal', compute='_compute_price_subtotal', store=True)

    def _compute_price_subtotal(self):
        pass
