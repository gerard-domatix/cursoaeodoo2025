from odoo import models, fields, api
from datetime import timedelta

class MusicSchoolCourseCreateLesson(models.TransientModel):
    _name = 'music.school.course.create.lesson'
    _description = 'Create Lesson Wizard'

    date_start = fields.Datetime(string='Start Date', required=True)
    date_end = fields.Date(string='End Date', required=True)

    def action_create_lessons(self):
        if not self.date_start or not self.date_end:
            return ValueError('Please provide all required information.')
        
        courses = self.env['music.school.course'].browse(self.env.context.get('active_ids', []))
        for course in courses:
            current_date = self.date_start
            while current_date.date() <= self.date_end:
                self.env['music.school.lesson'].create({
                    'course_id': course.id,
                    'date': current_date,
                    'duration': 1.0,
                })
                current_date += timedelta(days=1)