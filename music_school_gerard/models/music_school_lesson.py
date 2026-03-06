from odoo import models, fields

class MusicSchoolLesson(models.Model):
    _name = 'music.school.lesson'
    _description = 'Lesson'
    _rec_name = 'course_id'
    
    teacher_id = fields.Many2one(
        comodel_name='music.school.teacher',
        string="Teacher",
        help="Teacher giving this lesson"
    )
    course_id = fields.Many2one(
        comodel_name='music.school.course',
        string="Course",
        help="Course this lesson belongs to"
    )
    classroom_id = fields.Many2one(
        comodel_name='music.school.classroom',
        string="Classroom",
        help="Classroom where this lesson takes place"
    )

    state = fields.Selection(
        [
            ('scheduled', 'Scheduled'),
            ('completed', 'Completed'),
            ('canceled', 'Canceled')
        ],  
        string='State',
        required=True,
        default='scheduled',
        group_expand='group_expand_states'
    )

    color = fields.Integer(
        string="Color",
        help="Color associated with the lesson for calendar views"
    )

    date = fields.Datetime(
        string="Date and Time",
        default=fields.Datetime.now,
        help="Date and time of the lesson"
    )
    
    duration = fields.Float(string="Duration (hours)")
    notes = fields.Text(string="Notes")

    attendance_ids = fields.One2many(
        comodel_name='music.school.lesson.attendance',
        inverse_name='lesson_id',
        string="Attendance Records",
        help="Attendance records for this lesson"
    )

    def group_expand_states(self, states, domain):
        return ['scheduled', 'completed', 'canceled']