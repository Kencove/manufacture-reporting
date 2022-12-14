# Copyright 2022 ForgeFlow S.L. (http://www.forgeflow.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import logging

from odoo import models
from odoo.tools.translate import _

_logger = logging.getLogger(__name__)


class FlattenedBomXlsx(models.AbstractModel):
    _inherit = "report.mrp_flattened_bom_xlsx.flattened_bom_xlsx"

    def generate_xlsx_report(self, workbook, data, objects):
        res = super().generate_xlsx_report(workbook, data, objects)
        sheet = workbook.worksheets_objs[0]
        sheet.name = _("Direct Materials")

        sheet.set_column(6, 7, 20)
        title_style = workbook.formats[2]
        sheet_title = [
            _("Direct Materials Cost"),
            _("Currency"),
        ]
        sheet.set_row(0, None, None, {"collapsed": 1})
        sheet.write_row(1, 6, sheet_title, title_style)

        i = 2
        for o in objects:
            sheet.write(i, 6, o.direct_materials_cost or 0.0)
            sheet.write(i, 7, o.product_tmpl_id.currency_id.symbol or "")
            i += 1

            # We need to calculate the totals for the BoM qty and UoM:
            starting_factor = o.product_uom_id._compute_quantity(
                o.product_qty, o.product_tmpl_id.uom_id, round=False
            )
            requirements = o._get_flattened_totals(factor=starting_factor)
            for product in requirements:
                sheet.write(i, 6, product.standard_price or 0.0)
                sheet.write(i, 7, product.currency_id.symbol or "")
                i += 1
        return res
