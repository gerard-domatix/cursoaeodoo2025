from odoo import models, fields, api

class MusicSchoolInstrument(models.Model):
    _name = 'music.school.instrument'
    _description = 'Instrument'

    name = fields.Char(string="Name",required=True)
    active = fields.Boolean(string="Active", default=True)
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
    repaired = fields.Boolean(string='Repaired', compute="_compute_repaired", inverse="set_repaired")

    def generate_last_revision_date(self):
        for record in self:
            record.lastRevisionDate = fields.Date.today()
    
    def _compute_repaired(self):
        for record in self:
            if record.lastRevisionDate:
                record.repaired = True
            else:
                record.repaired = False

    def set_repaired(self):
        for record in self:
            if record.repaired:
                record.lastRevisionDate = fields.Date.today()
            else:
                record.lastRevisionDate = False

