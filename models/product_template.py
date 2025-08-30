from odoo import models, fields

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    drupal_id = fields.Char('Drupal ID', readonly=True, copy=False, index=True)
    sync_with_drupal = fields.Boolean('Sync with Drupal')

    def action_sync_to_drupal(self):
        drupal_api = self.env['drupal.api']
        # Note: 'node--article' is a placeholder. Change to your Drupal product content type, e.g., 'node--product'.
        drupal_content_type = 'node--article'

        for product in self:
            if not product.sync_with_drupal:
                continue

            payload = {
                "data": {
                    "type": drupal_content_type,
                    "attributes": {
                        "title": product.name,
                        "body": {
                            "value": product.description_sale or '',
                            "format": "basic_html",
                        },
                    }
                }
            }

            if product.drupal_id:
                endpoint = f'{drupal_content_type}/{product.drupal_id}'
                drupal_api._request('PATCH', endpoint, json=payload)
            else:
                endpoint = f'{drupal_content_type}'
                response = drupal_api._request('POST', endpoint, json=payload)
                if response and response.get('data'):
                    product.drupal_id = response['data']['id']

    def action_import_from_drupal(self):
        """Wizard action to import products from Drupal."""
        drupal_api = self.env['drupal.api']
        products_data = drupal_api.get_products()

        if not products_data or not products_data.get('data'):
            return

        for product_data in products_data['data']:
            drupal_id = product_data['id']
            attributes = product_data.get('attributes', {})
            title = attributes.get('title')

            if not title:
                continue

            existing_product = self.search([('drupal_id', '=', drupal_id)], limit=1)

            product_vals = {
                'name': title,
                'description_sale': attributes.get('body', {}).get('value', ''),
                'drupal_id': drupal_id,
                'sync_with_drupal': True,
            }

            if existing_product:
                existing_product.write(product_vals)
            else:
                self.create(product_vals)