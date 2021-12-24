from odoo import api, fields, models, _
from datetime import datetime


class FishingReception(models.Model):
    _name = "fishing.reception"
    name = fields.Char(string='Reference', required=True, readonly=True,
                       default=lambda self: _('New'))
    date = fields.Datetime(string='Date', default=datetime.today())
    fishmonger_id = fields.Many2one('res.partner', string='Fishmonger', required=True)
    boat_id = fields.Many2one('maintenance.equipment', string='Boat')
    note = fields.Text(string='Note')
    state = fields.Selection(
        [('raw', 'Raw'), ('in_treatment', 'In Treatment'), ('in_tunnel', 'In Tunnel'), ('in_packing', 'In Packing')],
        default='raw',
        string="Status", tracking=True)

    details_line_ids = fields.One2many('details.lines', 'reception_id',
                                       string='Prescription Lines')

    # quality = fields.Selection(
    #     [('good_quality', 'Good Quality'), ('bad_quality', 'Bad Quality')], default='good_quality',
    #     string="Quality", related = 'details_line_ids.quality')

    @api.model
    def create(self, vals):
        if not vals.get('note'):
            vals['note'] = 'New Appointment'
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('fishing.reception') or ('New')
            res = super(FishingReception, self).create(vals)
        return res


class DetailsLine(models.Model):
    _name = 'details.lines'
    _description = 'Details Lines'
    _rec_name = 'category'

    @api.model
    def default_get(self, fields):
        res = super(DetailsLine, self).default_get(fields)
        if self._context.get('active_id'):
            if self._context['active_id']:
                res['reception_id'] = self._context['active_id']
        return res

    reception_id = fields.Many2one('fishing.reception', string='Reception', readonly=True)
    category = fields.Many2one('product.category', string='Category')
    qty = fields.Integer(string='Quantity', default=0)
    quality = fields.Selection(
        [('good_quality', 'Good Quality'), ('bad_quality', 'Bad Quality')], default='good_quality',
        string="Quality")
    state = fields.Selection(
        [('to_treat', 'waiting for treatment'),
         ('in_treatment', 'In Treatment'), ('end_treatment', 'Waiting T or P'),
         ('in_tunnel', 'Tunnel being Processed'), ('end_tunnel', 'In Packing'),
         ('in_packing', 'Packing being Processed'), ('end_packing', 'Finished')],
        default='to_treat',
        string="Status")
    # treatment Date
    start_treatment_date = fields.Datetime(string='Start Treatment Date', readonly= True)
    end_treatment_date = fields.Datetime(string='End Treatment Date', readonly= True)

    # tunnel Date
    start_tunnel_date = fields.Datetime(string='Start Tunnel Date', readonly= True)
    end_tunnel_date = fields.Datetime(string='End Tunnel Date', readonly= True)

    # paching Date
    start_packing_date = fields.Datetime(string='Start Packing Date', readonly= True)
    end_packing_date = fields.Datetime(string='End Packing Date', readonly= True)



    def action_start_treatment(self):
        for rec in self:
            rec.state = 'in_treatment'
            print(rec.start_treatment_date, '...........')
            rec.start_treatment_date = datetime.today()


    def action_end_treatment(self):
        for rec in self:
            rec.state = 'end_treatment'
            rec.end_treatment_date = datetime.today()

    def action_start_tunnel(self):
        for rec in self:
            rec.state = 'in_tunnel'
            print(rec.start_tunnel_date, '...........')
            rec.start_tunnel_date = datetime.today()

    def action_end_tunnel(self):
        for rec in self:
            rec.state = 'end_tunnel'
            rec.end_tunnel_date = datetime.today()

    def action_start_packing(self):
        for rec in self:
            rec.state = 'in_packing'
            rec.start_packing_date = datetime.today()

    def action_end_packing(self):
        for rec in self:
            rec.state = 'end_packing'
            rec.end_packing_date = datetime.today()