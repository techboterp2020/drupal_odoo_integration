from odoo import models, fields, api, _
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    drupal_id = fields.Char('Drupal Order ID', readonly=True, copy=False, index=True)

    @api.model
    def action_import_from_drupal(self):
        """Action to import sales orders from Drupal."""
        drupal_api = self.env['drupal.api']
        order_data = drupal_api.get_orders()

        if not order_data or not order_data.get('data'):
            return

        included_data = {item['id']: item for item in order_data.get('included', [])}

        for order in order_data['data']:
            drupal_order_id = order['id']
            if self.search([('drupal_id', '=', drupal_order_id)]):
                continue  # Skip if order already exists

            attributes = order.get('attributes', {})
            relationships = order.get('relationships', {})
            
            # Find the customer
            customer_data = relationships.get('uid', {}).get('data', {})
            if not customer_data:
                continue
                
            drupal_user_id = customer_data['id']
            partner = self.env['res.partner'].search([('drupal_id', '=', drupal_user_id)], limit=1)
            if not partner:
                # Optional: Create customer if not found
                # For now, we skip if the customer doesn't exist in Odoo
                continue

            # Create the Sale Order
            so_vals = {
                'partner_id': partner.id,
                'drupal_id': drupal_order_id,
                'order_line': [],
            }

            # Process order lines
            order_items = relationships.get('order_items', {}).get('data', [])
            for item_ref in order_items:
                item_data = included_data.get(item_ref['id'])
                if not item_data:
                    continue
                
                # This part is complex and depends on your Drupal setup.
                # You need to get the product/SKU from the order item.
                # The following is a placeholder and likely needs adjustment.
                purchased_entity_ref = item_data.get('relationships', {}).get('purchased_entity', {}).get('data')
                if not purchased_entity_ref:
                    continue

                # Assuming the purchased entity is a product variation with a SKU
                product_variation = included_data.get(purchased_entity_ref['id'])
                sku = product_variation.get('attributes', {}).get('sku')
                
                product = self.env['product.product'].search([('default_code', '=', sku)], limit=1)
                if not product:
                    continue

                so_line_vals = {
                    'product_id': product.id,
                    'product_uom_qty': item_data.get('attributes', {}).get('quantity', 1),
                    'price_unit': float(item_data.get('attributes', {}).get('unit_price', {}).get('number', 0)),
                }
                so_vals['order_line'].append((0, 0, so_line_vals))

            if so_vals['order_line']:
                self.create(so_vals)