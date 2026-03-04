from odoo import models, fields, api

class MusicSchoolCourse(models.Model):
    _name= 'music.school.course'
    _description = 'Course'

    name = fields.Char(string = "Name", required=True)
    description = fields.Text(string = "Description")
    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('active', 'Active'),
            ('archived', 'Archived')
        ],
        string = 'State',
        required=True,
        group_expand='group_expand_states',
    )
    teacher_id = fields.Many2one(
        comodel_name='music.school.teacher',
        string="Teacher",
        help="Teacher responsible for this course"
    )
    instrument_id = fields.Many2one(
        comodel_name='music.school.instrument',
        string="Instrument",
        help="Instrument taught in this course"
    )
    level = fields.Selection(
        [   
            ('all', 'All Levels'),
            ('beginner', 'Beginner'),
            ('intermediate', 'Intermediate'),
            ('advanced', 'Advanced')
        ],
        string = 'Level',
        required=True,
        default='beginner'
    )
    date_start = fields.Date(string="Start Date")
    date_end = fields.Date(string="End Date")   
    capacity = fields.Integer(string="Capacity")
    duration = fields.Integer(string="Duration(Days)", compute="_compute_duration", store=True)

    color = fields.Integer(
        string="Color",
        help="Color associated with the course for calendar views"    
    )

    students_ids = fields.Many2many(
        comodel_name='music.school.student',
        string="Students",
        help="Students enrolled in this course"
    )
    
    def action_active(self):
        self.state = 'active'

    def action_archived(self):
        self.state = 'archived'
        self.env['music.school.lesson'].search([('course_id', '=', self.id)]).write({'state': 'completed'})

    def action_draft(self):
        self.state = 'draft'

    def group_expand_states(self, states, domain):
        return ['draft', 'active', 'archived']
    
    def action_create_lesson(self):
        lesson = self.env['music.school.lesson'].create({
            'course_id': self.id,
            'teacher_id': self.teacher_id.id,
        })

    def action_assign_students(self):
        for record in self:
            students = self.env['music.school.student'].search([])
            if students:
                record.students_ids = [(6, 0, students.ids)]

    @api.depends('date_start', 'date_end')
    def _compute_duration(self):
        for record in self:
            if record.date_start and record.date_end:
                duration = (record.date_end - record.date_start).days + 1
                record.duration = duration
            else:
                record.duration = 0