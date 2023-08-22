# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import fields, models


class StockMove(models.Model):
    _name = "stock.move"
    _inherit = ["stock.move"]

    journal_id = fields.Many2one(
        string="Journal",
        related="picking_id.journal_id",
    )
    debit_account_id = fields.Many2one(
        string="Debit Account",
        comodel_name="account.account",
    )
    credit_account_id = fields.Many2one(
        string="Credit Account",
        comodel_name="account.account",
    )
