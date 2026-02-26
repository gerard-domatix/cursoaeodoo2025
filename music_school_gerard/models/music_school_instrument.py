from odoo import models, fields

class MusicSchoolInstrument(models.Model):
    _name = 'music.school.instrument'
    _description = 'Instrument'

    name = fields.Char(string="Name",required=True)
    type = fields.Selection(
        [
            ('string', 'String'),
            ('wind', 'Wind'),
            ('percussion', 'Percussion')
        ],
        string = 'Instrument Type',
        required=True,
        default='string'
    )
    description = fields.Text(string='description')
    lastRevisionDate = fields.Date(string='Last Revision Date')

    def generate_last_revision_date(self):
        for record in self:
            record.lastRevisionDate = fields.Date.today()