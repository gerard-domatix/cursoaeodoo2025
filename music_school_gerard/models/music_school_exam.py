from odoo import models, fields, api

class MusicSchoolExam(models.Model):
    _name = 'music.school.exam'
    _description = 'Exam'

    name = fields.Char(string="Name", required=True)
    course_id = fields.Many2one(
        comodel_name='music.school.course',
        string="Course",
        help="Course associated with this exam"
    )
    date = fields.Datetime(string="Exam Date")
    instrument_id = fields.Many2one(
        comodel_name='music.school.instrument',
        string="Instrument",
        help="Instrument for which the exam is conducted"
    )
    min_score_to_pass = fields.Float(string="Minimum Score to Pass", default=0)
    max_score = fields.Float(string="Maximum Score", default=10)
    state = fields.Selection(
        [
            ('scheduled', 'Scheduled'),
            ('completed', 'Completed'), 
            ('canceled', 'Canceled')
        ],
        string='State',
        required=True,
        default='scheduled',
        group_expand='group_expand_states',
    ) 
    teacher_id = fields.Many2one(
        comodel_name='music.school.teacher',
        string="Examiner",
        help="Teacher responsible for conducting the exam"
    )
    
    results_ids = fields.One2many(
        comodel_name='music.school.results',
        inverse_name='exam_id',
        string="Exam Results",
        help="Results of students who took this exam"
    )   

    color = fields.Integer(
        string="Color",
        help="Color associated with the exam for calendar views"
    )   

    def group_expand_states(self, states, domain):
        return ['scheduled', 'completed', 'canceled']
    
    def action_generate_results(self):
        for exam in self:
            for student in exam.course_id.students_ids:
                self.env['music.school.results'].create({
                    'exam_id': exam.id,
                    'student_id': student.id,
                    'score': 0,
                })

    def finish_exams(self):
        exams =self.env['music.school.exam'].search([('state', 'in', ['scheduled','canceled'])])
        for exam in exams:
            if exam.date and exam.date < fields.Datetime.now():
                exam.state = 'completed'