
odoo.define('production_quantity_tracking_by_employee.employee_kanban_view_handler', function(require) {
"use strict";

var KanbanRecord = require('web_kanban.Record');

KanbanRecord.include({
    on_card_clicked: function() {
        if (this.model === 'hr.employee' && this.$el.parents('.o_hr_employee_attendance_kanban').length) {
            var action = {
                type: 'ir.actions.client',
                name: 'Confirm',
                tag: 'hr_attendance_kiosk_confirm',
                employee_id: this.record.id.raw_value,
                employee_name: this.record.name.raw_value,
            };
            this.do_action(action);
        } else {
            this._super.apply(this, arguments);
        }
    }
});

});
