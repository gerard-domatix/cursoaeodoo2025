from odoo import models, fields

class MusicSchoolLessonAttendance(models.Model):
    _name = 'music.school.lesson.attendance'
    _description = 'Lesson Attendance'
    _rec_name = 'student_id'

    sequence = fields.Integer(string="Sequence", default=10, help="Sequence order for attendance records")
    lesson_id = fields.Many2one(
        comodel_name='music.school.lesson',
        string="Lesson",
        help="Related lesson for this attendance record",
    )
    student_id = fields.Many2one(
        comodel_name='music.school.student',
        string="Student",
        required=True,
    )
    is_present = fields.Boolean(string="Is Present", default=False)
    date = fields.Datetime(string="Date", help="Date and time of the attendance record")
    notes = fields.Text(string="Notes", help="Additional notes about the attendance")