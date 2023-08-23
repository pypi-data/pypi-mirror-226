# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class OdooModule(models.Model):
    _name = "odoo_module"
    _inherit = [
        "odoo_module",
    ]

    git_repo_id = fields.Many2one(
        string="Git Repository",
        comodel_name="git_repo",
    )
