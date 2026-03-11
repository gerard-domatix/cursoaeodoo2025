from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    course_id = fields.Many2one(
        comodel_name='music.school.course',
        string='Course',
        help='Course associated with the sale order',
    )
