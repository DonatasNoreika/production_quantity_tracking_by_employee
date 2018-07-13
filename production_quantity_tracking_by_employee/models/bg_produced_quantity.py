# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError


class BGProducedQuantity(models.Model):
    _name = 'bg.produced_quantity'

    employee_id = fields.Many2one(string=_("Employee"), comodel_name='hr.employee', required=True)
    rel_department_id = fields.Many2one(string=_("Department"), related='employee_id.department_id', store=True)
    employee_wc_id = fields.Char(string= "Employee Work Center", compute='_get_work_centers')
    produced_qty = fields.Float(string=_("Produced Quantity"))
    qty_confirmed = fields.Boolean(string=_("Confirmed"), default=True)
    qty_left = fields.Float(string=_("Left to made"), compute='_calculate_work_order_qty_sum')

    work_order_id = fields.Many2one(string=_("Work Order"), comodel_name='mrp.workorder', required=True)
    work_order_rel = fields.Char(string=_("Work Center"), related='work_order_id.name', store=True)
    production_id = fields.Many2one(string=_("Manufacturing Order"), comodel_name='mrp.production', related='work_order_id.production_id', store=True)

    def _get_work_centers(self):
        for produced_qty in self:
            wc_counter = 0
            employee_work_centers = ''
            for work_center_id in produced_qty.employee_id.work_center_id:
                wc_counter += 1
                employee_work_centers += work_center_id.name
                if wc_counter != len(produced_qty.employee_id.work_center_id):
                    employee_work_centers += ', '
            produced_qty.employee_wc_id = employee_work_centers

    # This function confirms produced quantities and adds to work order
    @api.depends('qty_produced')
    def confirm_qty(self):
        for produced_qty in self:
            produced_qty.work_order_id.qty_produced += produced_qty.produced_qty
            produced_qty.qty_confirmed = True
        dam = self.env['mrp.workorder'].sum_produced_qty()

    def unconfirm_qty(self):
        for produced_qty in self:
            produced_qty.work_order_id.qty_produced -= produced_qty.produced_qty
            produced_qty.qty_confirmed = False
        dam = self.env['mrp.workorder'].sum_produced_qty()


    @api.depends('employee_id')
    def _calculate_work_order_qty_sum(self):
        for produced_qty in self:
            produced_qty.qty_left = produced_qty.work_order_id.qty_diff
