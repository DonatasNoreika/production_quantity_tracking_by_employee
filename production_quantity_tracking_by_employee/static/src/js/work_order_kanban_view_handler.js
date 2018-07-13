odoo.define('production_quantity_tracking_by_employee.work_order_kanban_view_handler', function(require) {
"use strict";

var KanbanRecord = require('web_kanban.Record');

KanbanRecord.include({
    on_card_clicked: function() {
        if (this.model === 'mrp.workorder' && this.$el.parents('.o_kanban_small_column_kiosk').length) {
                                            // needed to diffentiate : check in/out kanban view of employees <-> standard employee kanban view
            var action = {
                type: 'ir.actions.client',
                name: 'Confirm',
                tag: 'work_order_confirm_action',
                work_order_id: this.record.id.raw_value,
                wo_qty_production: this.record.qty_production.raw_value,
                wo_qty_diff: this.record.qty_diff.raw_value,
                wo_qty_produced: this.record.qty_produced.raw_value,
                wo_production_id: this.record.production_id.value,
                wo_workcenter_id: this.record.workcenter_id.value,
                wo_product_id: this.record.product_id.value,
            };
            this.do_action(action);
        } else {
            this._super.apply(this, arguments);
        }
    }
});

});
