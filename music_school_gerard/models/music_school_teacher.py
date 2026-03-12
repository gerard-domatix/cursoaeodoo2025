from odoo import models, fields

class MusicSchoolTeacher(models.Model):
    _name = 'music.school.teacher'
    _description = 'Teacher'
    _inherits = {'res.partner' : 'partner_id'}

    # name = fields.Char(string='Name', required=True)
    # email = fields.Char(string='Email')
    # phone = fields.Char(string='Phone')
    level = fields.Selection(
        selection=[
            ('all', 'All Levels'),
            ('beginner', 'Beginner'),
            ('intermediate', 'Intermediate'),
            ('advanced', 'Advanced')
        ],
        string='Level',
        default='beginner'
    )
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Partner',
        help='Related contact for this teacher',
        copy=False,
        ondelete='cascade'
    )

    courses_count = fields.Integer(string='Courses Count', compute='_compute_courses_count')

    def _compute_courses_count(self):
        for teacher in self:
            teacher.courses_count = self.env['music.school.course'].search_count([('teacher_id', '=', teacher.id)])
    
    def action_view_courses(self):
        return {
            'name': 'Courses',
            'type': 'ir.actions.act_window',
            'res_model': 'music.school.course',
            'view_mode': 'list,form',
            'domain': [('teacher_id', '=', self.id)],
        }