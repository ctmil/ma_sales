# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models

class SaleOrder(models.Model):
	_inherit = 'sale.order'

	@api.multi
	def _compute_billed_amount(self):
		"""
        	unique_variants = self.filtered(lambda template: len(template.product_variant_ids) == 1)
	        for template in unique_variants:
        	    template.default_code = template.product_variant_ids.default_code
	        for template in (self - unique_variants):
        	    template.default_code = ''
		"""
		for order in self:
			res = 0
			for line in order.order_line:
				if line.invoice_lines:
					for inv_line in line.invoice_lines:
						if inv_line.invoice_id.state not in ['sent','draft','cancel']:
							res = res + inv_line.price_subtotal
			order.billed_amount = res

	billed_amount = fields.Float('Monto facturado',compute=_compute_billed_amount)
