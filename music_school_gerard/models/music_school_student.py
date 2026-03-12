from odoo import models, fields, api

class MusicSchoolStudent(models.Model):
    _name = 'music.school.student'
    _description = 'Student'
    _inherits = {'res.partner' : 'partner_id'}

    active = fields.Boolean(string="Active", default=True)
    # name = fields.Char(string="Name",required=True)
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string="Partner",
        help="Related contact for this student",
        copy=False,
        ondelete='cascade'
    )
    # email = fields.Char(string="Email")
    # phone = fields.Char(string="Phone", related='partner_id.phone', store=True, readonly=False)
    birthdate = fields.Date(string="Birthdate")
    age = fields.Integer(string="Age", compute="_compute_age", store=True)
    user_id = fields.Many2one(
        comodel_name='res.users',
        string="Responsible",
        help="Responsible user for this student",
        default=lambda self: self.env.user
    )
    notes = fields.Html(
        string="Notes",
        help="Additional notes about the student"
    )
    reference = fields.Char(string="Reference", copy=False)

    attendances_count = fields.Integer(string="Attendances", compute="compute_attendances_count")
    def generate_reference(self):
        for record in self:
            record.reference = f"ESC-{record.id}{record.name}"
            
    @api.depends('birthdate')
    def _compute_age(self):
        for record in self:
            if record.birthdate:
                today = fields.Date.today()
                age = today.year - record.birthdate.year - ((today.month, today.day) < (record.birthdate.month, record.birthdate.day))
                record.age = age
            else:
                record.age = 0
    
    @api.onchange('partner_id')
    def _onchange_email(self):
        if self.partner_id:
            self.email = self.partner_id.email
        else:
            self.email = ''

    def action_view_attendances(self):
        return {
            'name': 'Attendances',
            'type': 'ir.actions.act_window',
            'res_model': 'music.school.lesson.attendance',
            'view_mode': 'list,form',
            'domain': [('student_id', '=', self.id)],
            'context': {'default_student_id': self.id}
        }
    
    def compute_attendances_count(self):
        for record in self:
            attendances = self.env['music.school.lesson.attendance'].search_count([('student_id', '=', record.id)])
            record.attendances_count = attendances