from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    drupal_id = fields.Char('Drupal ID', readonly=True, copy=False, index=True)
    sync_with_drupal = fields.Boolean('Sync with Drupal')

    def action_sync_to_drupal(self):
        drupal_api = self.env['drupal.api']
        drupal_user_entity = 'user--user'

        for partner in self:
            if not partner.sync_with_drupal or not partner.email:
                continue

            payload = {
                "data": {
                    "type": drupal_user_entity,
                    "attributes": {
                        "name": partner.email, # Drupal users often require name to be the email
                        "mail": partner.email,
                    }
                }
            }
            if partner.drupal_id:
                # Update existing user in Drupal
                endpoint = f'user/user/{partner.drupal_id}'
                drupal_api._request('PATCH', endpoint, json=payload)
            else:
                # Create new user in Drupal
                endpoint = 'user/user'
                response = drupal_api._request('POST', endpoint, json=payload)
                if response and response.get('data'):
                    partner.drupal_id = response['data']['id']