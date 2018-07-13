# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class BaseConfigSettings(models.TransientModel):
    _inherit = 'base.config.settings'

    group_produced_qty_attendance_use_pin = fields.Selection([(0, 'Employees do not need to enter their PIN to check in manually in the "Kiosk Mode".'),
                                                 (1, 'Employees must enter their PIN to check in manually in the "Kiosk Mode".')],
                                                string='Employee PIN', help='Enable or disable employee PIN identification at check in', implied_group="production_quantity_tracking_by_employee.group_produced_qty_attendance_use_pin")
