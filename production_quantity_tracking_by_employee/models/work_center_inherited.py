# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _

class workcenter_routing_inherited(models.Model):
    _inherit = 'mrp.routing.workcenter'

    next_wo_after = fields.Integer(string=_("Next Work Order after:"), default=0)