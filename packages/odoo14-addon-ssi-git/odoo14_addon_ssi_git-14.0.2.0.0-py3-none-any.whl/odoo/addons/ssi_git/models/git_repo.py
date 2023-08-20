# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class GitRepo(models.Model):
    _name = "git_repo"
    _inherit = ["mixin.master_data"]
    _description = "Git Repository"

    type_id = fields.Many2one(
        string="Type",
        comodel_name="git_repo_type",
        required=True,
    )
