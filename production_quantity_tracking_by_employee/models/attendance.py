# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime

from odoo import models, fields, api, exceptions, _
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT


class HrAttendance(models.Model):
    _name = "produced_qty.attendance"
    _description = "Attendance"
    _order = "check_in desc"

    def _default_employee(self):
        return self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)

    employee_id = fields.Many2one('hr.employee', string="Employee", default=_default_employee, required=True, ondelete='cascade', index=True)
    department_id = fields.Many2one('hr.department', string="Department", related="employee_id.department_id")
    check_in = fields.Datetime(string="Time", default=fields.Datetime.now, required=True)
    check_out = fields.Datetime(string="Check Out")

    @api.multi
    def name_get(self):
        result = []
        for attendance in self:
            result.append((attendance.id, _("%(empl_name)s from %(check_in)s") % {
                'empl_name': attendance.employee_id.name_related,
                'check_in': fields.Datetime.to_string(fields.Datetime.context_timestamp(attendance, fields.Datetime.from_string(attendance.check_in))),
            }))
        return result

    @api.multi
    def copy(self):
        raise exceptions.UserError(_('You cannot duplicate an attendance.'))
