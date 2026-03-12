from odoo import models, fields, api

class MusicSchoolCourse(models.Model):
    _name= 'music.school.course'
    _description = 'Course'
    _inherit = ['mail.thread', 'mail.activity.mixin']


    name = fields.Char(string = "Name", copy=False, default="New Course")
    description = fields.Text(string = "Description", company_dependent=True)
    active = fields.Boolean(string="Active", default=True)
    company_id = fields.Many2one(
        comodel_name='res.company',
        string="Company",   
        default=lambda self: self.env.company
    )
    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('active', 'Active'),
            ('archived', 'Archived'),
            ('canceled', 'Canceled')
        ],
        string = 'State',
        required=True,
        group_expand='group_expand_states',
        default='draft'
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
    date_start = fields.Date(
        string="Start Date",
        help="Start date of the course",
        default=fields.Date.today()
        )
    date_end = fields.Date(string="End Date", help="End date of the course")   
    capacity = fields.Integer(string="Capacity", tracking=True, help="Maximum number of students allowed in this course")
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
    
    exam_count = fields.Integer(string="Exam Count", compute="_compute_exam_count")
    lesson_count = fields.Integer(string="Lesson Count", compute="_compute_lesson_count")

    company_id = fields.Many2one(
        comodel_name='res.company',
        string="Company",
        default=lambda self: self.env.company
    )
    
    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'Course name must be unique.'),
    ]

    def _compute_lesson_count(self):
        for record in self:
            record.lesson_count = self.env['music.school.lesson'].search_count([('course_id', '=', record.id)])

    def _compute_exam_count(self):
        for record in self:
            record.exam_count = self.env['music.school.exam'].search_count([('course_id', '=', record.id)]) 
            
    def action_active(self):
        self.state = 'active'

    def action_archived(self):
        self.state = 'archived'
        self.env['music.school.lesson'].search([('course_id', '=', self.id)]).write({'state': 'completed'})

    def action_canceled(self):
        self.state = 'canceled'

    def action_draft(self):
        self.state = 'draft'
        self.message_post(body="Course has been set to draft.")

    def group_expand_states(self, states, domain):
        return ['draft', 'active', 'archived', 'canceled']
    
    def action_create_lesson(self):
        lesson = self.env['music.school.lesson'].create({
            'course_id': self.id,
            'teacher_id': self.teacher_id.id,
        })
        lesson.message_post_with_source('mail.message_origin_link', render_values={'self':lesson, 'origin': self})

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

    @api.constrains('capacity')
    def _check_capacity(self):
        for record in self:
            if record.capacity < 0:
                raise ValueError("Capacity cannot be negative.")
        
    @api.constrains('date_start', 'date_end')
    def _check_dates(self):
        for record in self:
            if record.date_start and record.date_end and record.date_end < record.date_start:
                raise ValueError("End date cannot be before start date.")

    def action_view_exams(self):
        return {
            'name': 'Exams',
            'type': 'ir.actions.act_window',
            'res_model': 'music.school.exam',
            'view_mode': 'list,form',
            'domain': [('course_id', '=', self.id)],
            'context': {'default_course_id': self.id}
        }
    
    def action_view_lessons(self):
        return {
            'name': 'Lessons',
            'type': 'ir.actions.act_window',
            'res_model': 'music.school.lesson',
            'view_mode': 'list,form',
            'domain': [('course_id', '=', self.id)],
            'context': {'default_course_id': self.id}
        }
    
    @api.onchange('teacher_id')
    def _onchange_teacher_id(self):
        if self.teacher_id:
            self.level = self.teacher_id.level
        
    def finish_course(self):
        courses = self.env['music.school.course'].search([('state', 'in', ['active','draft'])])
        for course in courses:
            if course.date_end and course.date_end < fields.Date.today():
                course.state = 'archived'

    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('music.school.course')
        return super().create(vals)