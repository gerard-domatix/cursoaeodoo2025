from odoo import models, fields, api

class MusicSchoolCourseChangeState(models.TransientModel):
    _name = 'music.school.course.change.state'
    _description = 'Change Course State Wizard'

    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('active', 'Active'),
            ('archived', 'Archived')
        ],
        string = 'State',
    )

    def action_apply_change_state(self):
        courses = self.env['music.school.course'].browse(self.env.context.get('active_ids', []))
        if courses:
            courses.write({'state': self.state})