# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class OdooModule(models.Model):
    _name = "odoo_module"
    _inherit = ["mixin.master_data"]
    _description = "Odoo Module"

    version_ids = fields.Many2many(
        string="Versions",
        comodel_name="odoo_version",
        relation="rel_odoo_version_2_module",
        column1="module_id",
        column2="version_id",
    )
