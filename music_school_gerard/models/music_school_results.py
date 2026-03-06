from odoo import models, fields, api

class MusicSchoolResults(models.Model):
    _name = 'music.school.results'
    _description = 'Exam Results'
    _rec_name = 'exam_id'

    exam_id = fields.Many2one(
        comodel_name='music.school.exam',
        string="Exam",
        help="Exam for which this result is recorded",
        group_expand='group_expand_exam_id'
    )

    student_id = fields.Many2one(
        comodel_name='music.school.student',
        string="Student",
        help="Student who took the exam"
    )   

    score = fields.Float(string="Score Obtained")
    passed = fields.Boolean(string="Passed", compute="_compute_passed", store=True)
    teacher_notes = fields.Text(string="Teacher Notes")
    
    color = fields.Integer(
        string="Color",
        help="Color associated with the result for kanban views"
    )

    students_ids = fields.Many2many(
        comodel_name='music.school.student',
        string="Students",
        help="Students associated with this result",
        related='exam_id.course_id.students_ids',
    )

    @api.depends('score', 'exam_id.min_score_to_pass')
    def _compute_passed(self):
        for record in self:
            if record.exam_id and record.score is not None:
                record.passed = record.score >= record.exam_id.min_score_to_pass
            else:
                record.passed = False

    def group_expand_exam_id(self, exam_id, domain):
        return self.env['music.school.exam'].search([])