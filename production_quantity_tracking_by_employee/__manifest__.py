# -*- coding: utf-8 -*-

{
    'name': 'Full Production Quantity Tracking by Employee',
    'version': '1.0',
    'author': "Vidas Lisauskas, Romualdas Laurinavičius, Pardavimai lengvai LT, Donatas Noreika",
    'images': ['static/kiosk_2.gif'],
    'support': 'vidas@pardavimai.com',
    'website': "",
    'summary': 'The module provides visibility to production efficiency by employee',
    'description': """

The module provides visibility to production efficiency by employee.
Workorder Quantity by Employee Management application extends Odoo’s labor reporting functionality by providing the capability to capture manufacturing produced quantity data by Work Order by Employee. The app allows to link Employees to one or more Work Centers and set up a Kiosk mode screen on the Shop Floor for Data capture. PIN security can be enabled for Employees logging in. Once the Employees are logged in, the system displays only the Work Orders scheduled on the Work Centers linked to the Employee. Produced quantity is reported by choosing the Work Order Kanban card from the board and entering produced quantity on a touch-friendly number keypad. Captured Data can be reviewed through the Manufacturing Order or a dedicated report available in List View and a Pivot Table or Exported to Excel or CSV for further analysis.

Functions:
    1. A new menu section “Produced Quantities Manager” is added to the Manufacturing module listing all the new menu options. 
    2. Kiosk mode screen is created allowing Employees from Shop Floor to log into the system and enter produced quantities on a Work Order.  Kiosk mode displays only the Work Orders scheduled on the Work Centers linked to the Employee. Produced quantity is entered on a touch-friendly number keypad, enabling to use tablets for data entry.
    3. Produced Quantities tab is added to Work Order screen allowing to review data captured for this Work Order.
    4. A new dedicated report – Produced Quantities is added to review produced quantities by Employee available in List View and a Pivot Table.
    5. A new full screen Work Orders Dashboard View is added to display production plan on the Shop Floor. The view displays scheduled Work Orders in Kanban view. Kanban cards display the following:
     
    * Work Center
    * Product
    * Quantity made
    * Quantity left to do
    * Manufacturing Order
    * Status

Icon made by "Vectors Market" (https://www.flaticon.com/authors/vectors-market) from "Flaticon" (https://www.flaticon.com/) is licensed by "Creative Commons BY 3.0" (http://creativecommons.org/licenses/by/3.0/)
    """,

    'price': 78.00,
    'currency': 'EUR',
    'license': 'OPL-1',

    'depends': ['base','mrp','hr'],
    'category': 'Manufacturing',
    'demo': [
    ],
    'data': [
        'security/workorder_qty_security.xml',
        'security/ir.model.access.csv',
        'views/web_asset_template.xml',
        'views/employee_view.xml',
        'views/attendance_view.xml',
        'views/res_config_view.xml',
        'report/hr_employee_badge.xml',
        'views/work_center_inherited_view.xml',
        'views/work_order_inherited_view.xml',
        'views/bg_produced_qty_view.xml',
        'views/mrp_production_inherited_view.xml',
    ],
    'test': [

    ],
    'installable': True,
    'application': True,
    'qweb': [
        "static/src/xml/attendance.xml",
    ],
    'auto_install': False,
}
