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
        for student in self.students_ids:
            self.order_ids.unlink()
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