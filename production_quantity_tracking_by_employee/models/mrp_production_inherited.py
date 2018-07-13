# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _

class mrp_production_inherit(models.Model):
    _inherit = 'mrp.production'

    def confirm_produced_qty(self):
        for production_order in self:
            for wo_produced in production_order.move_finished_ids:
                wo_produced.quantity_done = wo_produced.product_uom_qty
            for wo_consumed in production_order.move_raw_ids:
                wo_consumed.quantity_done = wo_consumed.product_uom_qty
