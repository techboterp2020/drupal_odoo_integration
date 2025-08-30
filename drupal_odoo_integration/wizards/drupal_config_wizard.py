from odoo import models, fields, api

class DrupalConfigWizard(models.TransientModel):
    _name = 'drupal.config.wizard'
    _description = 'Drupal Configuration Wizard'

    def _get_default_config(self):
        """Helper to get config parameters."""
        params = self.env['ir.config_parameter'].sudo()
        return {
            'drupal_url': params.get_param('drupal.url'),
            'drupal_username': params.get_param('drupal.username'),
            'drupal_password': params.get_param('drupal.password'),
        }

    drupal_url = fields.Char(
        'Drupal URL', 
        required=True, 
        help="e.g., https://yourdrupalsite.com",
        default=lambda self: self._get_default_config().get('drupal_url')
    )
    drupal_username = fields.Char(
        'Drupal Username', 
        required=True,
        default=lambda self: self._get_default_config().get('drupal_username')
    )
    drupal_password = fields.Char(
        'Drupal Password', 
        required=True, 
        widget='password',
        default=lambda self: self._get_default_config().get('drupal_password')
    )

    def action_save_config(self):
        self.ensure_one()
        params = self.env['ir.config_parameter'].sudo()
        params.set_param('drupal.url', self.drupal_url)
        params.set_param('drupal.username', self.drupal_username)
        params.set_param('drupal.password', self.drupal_password)
        return {'type': 'ir.actions.act_window_close'}