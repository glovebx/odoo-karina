# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2013 Mentis d.o.o. (<http://www.mentis.si/openerp>)
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
##############################################################################

{
    "name": "Supplier invoice number reference",
    "version": "1.1",
    "author": "Mentis d.o.o.",
    "category": "Accounting",
    "depends": ['account'],
    "description": """Adds field Supplier Invoice Number to supplier invoice and account move. """,
    "update_xml": [
                 'account_move_view.xml',
                 'account_move_line_view.xml'
                 ],
    "active": False,
    "installable": True,
}
