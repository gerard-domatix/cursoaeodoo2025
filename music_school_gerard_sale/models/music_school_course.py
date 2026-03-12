from odoo import models, fields, api

class MusicSchoolCourse(models.Model):
    _inherit = 'music.school.course'

    price = fields.Float(string='Price', default=0.0, help='Price of the course')

    product_id = fields.Many2one(
        comodel_name='product.product',
        string='Product',
        help='Product associated with the course',
    )

    order_ids = fields.One2many(
        comodel_name='sale.order',
        inverse_name='course_id',
        string='Orders',
        help='Sale orders associated with this course',
    )

    order_count = fields.Integer(
        string="Orders Count",
        compute='_compute_order_count',
        help="Number of sales orders associated with the course"
    )

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.price = self.product_id.list_price
        else:
            self.price = 0.0

    def action_create_orders(self):
        self.order_ids.unlink()
        for student in self.students_ids:
            self.env['sale.order'].create({
                'partner_id': student.partner_id.id,
                'course_id': self.id,
                'company_id': self.env.company.id,
                'order_line': [(0, 0, {
                    'product_id': self.product_id.id,
                    'product_uom_qty': 1,
                    'price_unit': self.price,
                })],
            })
    
    def _compute_order_count(self):
        for course in self:
            course.order_count = len(course.order_ids)
    
    def action_view_orders(self):
        return {
            'name': 'Orders',
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order',
            'view_mode': 'list,form',
            'domain': [('course_id', '=', self.id)],
        }

    def action_canceled(self):
        res = super().action_canceled()
        for order in self.order_ids:
            order.action_cancel()
        return res

    def action_draft(self):
        res = super().action_draft()    
        for order in self.order_ids:
            order.action_draft()
        return res

    def action_confirm_and_invoice_sales(self):
            self.order_ids.filtered(lambda o: o.state != 'done').action_confirm()
            self.order_ids.filtered(lambda o: o.invoice_status != 'invoiced')._create_invoices()