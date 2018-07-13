# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError
from odoo.tools import float_compare, float_round
from odoo.addons import decimal_precision as dp

from odoo import models, fields, api, exceptions, _, SUPERUSER_ID

class work_order_inherited(models.Model):
    _inherit = 'mrp.workorder'

    produced_qty_ids = fields.One2many(string=_("Produced Quantities"), comodel_name='bg.produced_quantity', inverse_name='work_order_id')

    qty_produced = fields.Float(
        'Quantity', default=0.0,
        readonly=True,
        compute='sum_produced_qty',
        store=True,
        digits=dp.get_precision('Product Unit of Measure'),
        help="The number of products already handled by this work order")

    qty_diff = fields.Float(compute='_calculate_qty_diff')
    qty_produced_stored = fields.Float(compute='_get_qty_produced', store=True)
    work_center_match = fields.Boolean(compute='get_active_work_center', store=True)
    attendance_id = fields.Many2one('produced_qty.attendance')

    def _calculate_qty_diff(self):
        for work_order in self:
            work_order.qty_diff = work_order.qty_production - work_order.qty_produced

    @api.model
    def get_active_work_center(self):
        last_attendance = self.compute_last_attendance_id()
        hr_wcs = self.env['hr.employee'].browse(last_attendance).work_center_id
        workorder_obj = self.env['mrp.workorder'].search([])
        for work_order in workorder_obj:
            work_order.work_center_match = False
            for work_center in hr_wcs:
                if work_center == work_order.workcenter_id:
                    work_order.work_center_match = True

    @api.depends('produced_qty_ids')
    @api.onchange('produced_qty_ids')
    def _get_qty_produced(self):
        for workorder in self:
            workorder.qty_produced_stored = workorder.qty_produced
            if workorder.qty_produced >= workorder.qty_production:
                workorder.record_production()

    def action_set_qty(self):
        for workorder in self:
            self.ensure_one()
            ctx = dict()
            ctx.update({
                'work_order_id': workorder.id,

            })
            return {
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'bg.produced_quantity',
                'target': 'new',
            }

    @api.onchange('produced_qty_ids')
    @api.depends('produced_qty_ids')
    def sum_produced_qty(self):
        for work_order in self:
            total = 0
            active_batch_size = 0
            for one_qty in work_order.produced_qty_ids:
                if one_qty.qty_confirmed:
                    total += one_qty.produced_qty
            work_order.qty_produced = total
            if work_order.state == 'ready':
                self.button_start()

            bom_obj = self.env['mrp.bom'].search([])
            for active_bom in bom_obj:
                if active_bom.product_tmpl_id.name == work_order.product_id.name:
                    for operation in active_bom.routing_id.operation_ids:
                        if operation.name == work_order.name:
                            active_batch_size = operation.next_wo_after

            if active_batch_size > 0 and work_order.qty_produced >= active_batch_size:
                work_order.record_production()
                work_order.next_work_order_id.button_start()

    def button_finish(self):
        self.ensure_one()
        self.end_all()

        self.write({'state': 'done', 'date_finished': fields.Datetime.now()})

        for work_order in self:
            this_mo_wo_obj = self.env['mrp.workorder'].search([('production_id', '=', work_order.production_id.id)])
            next_wo_trigger = False
            for this_wos in this_mo_wo_obj:
                if not this_wos.date_finished and not next_wo_trigger:
                    this_wos.button_start()
                    next_wo_trigger = True
            # self.env['mrp.production'].search([('id', '=', work_order.production_id.id)]).confirm_produced_qty()
        return self.write({'state': 'done', 'date_finished': fields.Datetime.now()})

    def compute_last_attendance_id(self):
        # Returns employee ID from latest active attendance (with biggest ID)
        attendance_obj = self.env['produced_qty.attendance'].search([])
        last_attendance = 0
        for one_attendance in attendance_obj:
            if one_attendance.id > last_attendance:
                last_attendance = one_attendance.id
        return self.env['produced_qty.attendance'].browse([last_attendance]).employee_id.id

    def create_produced_qty(self, work_order_id, qty):
        vals = {
            'work_order_id': work_order_id,
            'employee_id': self.compute_last_attendance_id(),
            'produced_qty': qty,
        }
        return self.env['bg.produced_quantity'].create(vals)

    @api.multi
    def work_order_manual(self, work_order_id, qty, entered_pin=None):
        for work_order in self:
            self.ensure_one()
            modified_attendance = self.sudo().create_produced_qty(work_order_id, qty)
