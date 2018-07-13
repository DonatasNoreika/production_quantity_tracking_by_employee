odoo.define('production_quantity_tracking_by_employee.work_order_confirm', function (require) {
"use strict";

var core = require('web.core');
var Model = require('web.Model');
var Widget = require('web.Widget');

var QWeb = core.qweb;
var _t = core._t;


var WorkOrderConfirm = Widget.extend({
    events: {
        "click .o_hr_attendance_back_button": function () {
        this.do_action(this.back_to_main, {clear_breadcrumbs: true});
        var work_order = new Model('mrp.workorder');
        work_order.call('compute_last_attendance_id', [this.next_action]);
        },
        'click .o_hr_attendance_pin_pad_button_0': function() { this.$('.o_produced_qty_NUMbox').val(this.$('.o_produced_qty_NUMbox').val() + 0); },
        'click .o_hr_attendance_pin_pad_button_1': function() { this.$('.o_produced_qty_NUMbox').val(this.$('.o_produced_qty_NUMbox').val() + 1); },
        'click .o_hr_attendance_pin_pad_button_2': function() { this.$('.o_produced_qty_NUMbox').val(this.$('.o_produced_qty_NUMbox').val() + 2); },
        'click .o_hr_attendance_pin_pad_button_3': function() { this.$('.o_produced_qty_NUMbox').val(this.$('.o_produced_qty_NUMbox').val() + 3); },
        'click .o_hr_attendance_pin_pad_button_4': function() { this.$('.o_produced_qty_NUMbox').val(this.$('.o_produced_qty_NUMbox').val() + 4); },
        'click .o_hr_attendance_pin_pad_button_5': function() { this.$('.o_produced_qty_NUMbox').val(this.$('.o_produced_qty_NUMbox').val() + 5); },
        'click .o_hr_attendance_pin_pad_button_6': function() { this.$('.o_produced_qty_NUMbox').val(this.$('.o_produced_qty_NUMbox').val() + 6); },
        'click .o_hr_attendance_pin_pad_button_7': function() { this.$('.o_produced_qty_NUMbox').val(this.$('.o_produced_qty_NUMbox').val() + 7); },
        'click .o_hr_attendance_pin_pad_button_8': function() { this.$('.o_produced_qty_NUMbox').val(this.$('.o_produced_qty_NUMbox').val() + 8); },
        'click .o_hr_attendance_pin_pad_button_9': function() { this.$('.o_produced_qty_NUMbox').val(this.$('.o_produced_qty_NUMbox').val() + 9); },
        'click .o_hr_attendance_pin_pad_button_C': function() { this.$('.o_produced_qty_NUMbox').val(''); },
        'click .o_hr_attendance_pin_pad_button_ok': function() {
            var self = this;
            this.$('.o_hr_attendance_pin_pad_button_ok').attr("disabled", "disabled");
            var work_order = new Model('mrp.workorder');
            work_order.call('work_order_manual', [this.next_action, this.work_order_id, this.$('.o_produced_qty_NUMbox').val()])
            this.do_action(this.back_to_main, {clear_breadcrumbs: true});
        },
    },

    init: function (parent, action) {
        this._super.apply(this, arguments);
        this.next_action = 'production_quantity_tracking_by_employee.produced_qty_attendance_action_kiosk_mode';
        this.back_to_main  = 'production_quantity_tracking_by_employee.produced_qty_attendance_action_kiosk_mode';
        this.work_order_id = action.work_order_id;
        this.wo_qty_production = action.wo_qty_production;
        this.wo_qty_diff = action.wo_qty_diff;
        this.wo_qty_produced = action.qty_produced;
        this.wo_production_id = action.wo_production_id;
        this.wo_workcenter_id = action.wo_workcenter_id;
        this.wo_product_id = action.wo_product_id;
//        this.wo_so_line_name = action.wo_so_line_name;

        var self = this;
    },

    start: function () {
        var self = this;
        self.session.user_has_group('production_quantity_tracking_by_employee.group_produced_qty_attendance_use_pin').then(function(has_group){
            self.use_pin = has_group;
            self.$el.html(QWeb.render("WorkOrderConfirm", {widget: self}));
            self.start_clock();
        });
        return self._super.apply(this, arguments);
    },

    start_clock: function () {
        this.clock_start = setInterval(function() {this.$(".o_hr_attendance_clock").text(new Date().toLocaleTimeString(navigator.language, {hour: '2-digit', minute:'2-digit'}));}, 500);
        // First clock refresh before interval to avoid delay
        this.$(".o_hr_attendance_clock").text(new Date().toLocaleTimeString(navigator.language, {hour: '2-digit', minute:'2-digit'}));
    },

    destroy: function () {
        clearInterval(this.clock_start);
        this._super.apply(this, arguments);
    },
});

core.action_registry.add('work_order_confirm_action', WorkOrderConfirm);

return WorkOrderConfirm;

});
