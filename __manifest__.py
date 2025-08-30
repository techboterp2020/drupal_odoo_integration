# -*- coding: utf-8 -*-
{
    'name': 'Drupal Odoo Integration (v18)',
    'version': '18.0.2.0',
    'summary': 'Integrate Odoo with a Drupal Website',
    'description': """
        Connects Odoo 18 with Drupal for seamless data synchronization.
        - Configure Drupal connection credentials.
        - Sync Products and Customers to Drupal.
        - Import Products and Sales Orders from Drupal.
        - Supports manual and automated synchronization.
    """,
    'category': 'Sales/Connector',
    'author': 'Techbot Information Technology LLC',
    'depends': ['base', 'sale_management', 'stock'],
    'data': [
        'security/ir.model.access.csv',
        'wizards/drupal_config_wizard_views.xml',
        'views/res_partner_views.xml',
        'views/product_template_views.xml',
        'views/sale_order_views.xml',
        'data/ir_cron_data.xml',
        'data/ir_actions_server_data.xml',
    ],
    'images': [
        'static/description/screenshot_1.png',
        'static/description/screenshot_2.png',
        'static/description/screenshot_3.png',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}