# -*- coding: utf-8 -*-

###############################################################################
#
#    Periodical Sales Report
#
#    Copyright (C) 2019 Aminia Technology
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

from odoo import api, models
from dateutil.relativedelta import relativedelta
import datetime


class ReportPeriodicalSale(models.AbstractModel):
    _name = 'report.periodical_sales_report.report_periodical_sales'
    
    @api.model
    def render_html(self, docids, data=None):
        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(self.env.context.get('active_id'))
        sales_records = []
        total_sale = 0.0

        if docs.date_from and docs.date_to:
            domain = [('date_order', '>=', docs.date_from),
                      ('date_order', '<=', docs.date_to)]
        else:
            if docs.period == 'today':
                domain = [('date_order', '>=', datetime.datetime.now()
                           .strftime('%Y-%m-%d 00:00:00')),('date_order',
                            '<=', datetime.datetime.now()
                            .strftime('%Y-%m-%d 23:59:59'))]
            elif docs.period == 'last_week':
                domain = [('date_order', '>=', (datetime.date.today()
                -datetime.timedelta(days=7)).strftime('%Y-%m-%d 00:00:00')),
                 ('date_order', '<=', datetime.datetime.now()
                  .strftime('%Y-%m-%d 23:59:59'))
                ]
            elif docs.period == 'last_month':
                domain = [
                    ('date_order', '>=',
                     (datetime.date.today() - relativedelta(months=1)).
                     strftime('%Y-%m-%d 00:00:00')),
                    ('date_order', '<=',
                     datetime.datetime.now().strftime('%Y-%m-%d 23:59:59'))
                ]
        if docs.state != 'all':
            domain.append(('state','=',docs.state))
        orders = self.env['sale.order'].search(domain)
        if orders:
            for order in orders:
                sales_records.append(order)
                total_sale += order.amount_total
        docargs = {
            'doc_ids': self.ids,
            'doc_model': self.model,
            'docs': docs,
            'orders': sales_records,
            'total_sale':total_sale,
            'date_from':docs.date_from,
            'date_to':docs.date_to
        }
        return self.env['report'].render('periodical_sales_report.'
                                         'report_periodical_sales', docargs)
