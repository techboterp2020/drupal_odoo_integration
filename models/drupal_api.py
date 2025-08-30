import requests
from odoo import models, _, api
from odoo.exceptions import UserError

class DrupalAPI(models.AbstractModel):
    _name = 'drupal.api'
    _description = 'Drupal API Connector'

    def _get_config(self):
        """Retrieves Drupal API configuration from Odoo's system parameters."""
        params = self.env['ir.config_parameter'].sudo()
        return {
            'url': params.get_param('drupal.url'),
            'username': params.get_param('drupal.username'),
            'password': params.get_param('drupal.password'),
        }

    def _request(self, method, endpoint, json=None):
        """Sends a request to the Drupal JSON:API."""
        config = self._get_config()
        if not all(config.values()):
            raise UserError(_('Drupal API credentials are not set. Please configure them in Settings.'))

        headers = {'Content-Type': 'application/vnd.api+json'}
        auth = (config['username'], config['password'])
        url = f"{config['url'].rstrip('/')}/jsonapi/{endpoint}"

        try:
            response = requests.request(method, url, auth=auth, headers=headers, json=json, timeout=15)
            response.raise_for_status()
            if response.status_code == 204:  # No Content
                return True
            return response.json()
        except requests.exceptions.HTTPError as e:
            raise UserError(_('HTTP Error connecting to Drupal: %s', e.response.text))
        except requests.exceptions.RequestException as e:
            raise UserError(_('Connection Error to Drupal: %s', e))

    @api.model
    def cron_sync(self):
        """Cron job method to sync all marked records."""
        self.env['res.partner'].search([('sync_with_drupal', '=', True)]).action_sync_to_drupal()
        self.env['product.template'].search([('sync_with_drupal', '=', True)]).action_sync_to_drupal()

    def get_products(self):
        """Fetches all products from Drupal."""
        # Note: 'node--article' is a placeholder. Change to your Drupal product content type.
        drupal_content_type = 'node--article'
        endpoint = f'{drupal_content_type}'
        return self._request('GET', endpoint)

    def get_orders(self):
        """Fetches all orders from Drupal."""
        # Note: 'commerce_order--default' is a common Drupal Commerce endpoint. Adjust if needed.
        # Include order items and customer data with the request.
        endpoint = 'commerce_order/default?include=order_items,uid'
        return self._request('GET', endpoint)