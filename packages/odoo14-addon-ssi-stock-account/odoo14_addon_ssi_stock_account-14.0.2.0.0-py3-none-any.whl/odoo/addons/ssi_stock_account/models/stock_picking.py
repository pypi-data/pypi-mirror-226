# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import fields, models


class StockPicking(models.Model):
    _name = "stock.picking"
    _inherit = ["stock.picking"]

    journal_id = fields.Many2one(
        string="Journal",
        comodel_name="account.journal",
    )
