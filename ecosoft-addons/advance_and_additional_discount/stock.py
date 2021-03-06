from openerp.osv import fields, osv
from openerp.tools.translate import _


class stock_picking(osv.osv):

    _inherit = 'stock.picking'

    def action_invoice_create(self, cr, uid, ids, journal_id=False,
            group=False, type='out_invoice', context=None):
        """ Adding Additional Discount % from SO/PO into INV when created from DO """

        assert type in ('out_invoice', 'in_invoice', 'in_refund', 'out_refund')
        model = type in ('out_invoice', 'out_refund') and 'sale.order' or 'purchase.order'

        order_id_name = (model == 'sale.order' and 'sale_id' or 'purchase_id')
        order_ids_name = (model == 'sale.order' and 'sale_order_ids' or 'purchase_order_ids')
        #First create Advance/Deposit Invoice
        inv_obj = self.pool.get('account.invoice')
        pickings = self.browse(cr, uid, ids)
        for picking in pickings:
            if picking[order_id_name] and picking[order_id_name].advance_type:
                advance_type = 'is_advance' if picking[order_id_name].advance_type == 'advance' else 'is_deposit'
                advance_name = 'Advance' if picking[order_id_name].advance_type == 'advance' else 'Deposit'
                found = inv_obj.search(cr, uid, [(order_ids_name, 'in', [picking[order_id_name].id]), ('state', '!=', 'cancel'), (advance_type, '=', True)])
                if not found:
                    raise osv.except_osv(_('Warning!'),
                            _('Unable to create invoice.! First create %s invoice' % advance_name))

        res = super(stock_picking, self).action_invoice_create(cr, uid, ids, journal_id,
                                                                 group, type, context=context)
        # Loop through each id (DO), getting its SO/PO's Additional Discount, Write it to Invoice
        for picking in pickings:
            if not picking.invoice_state == '2binvoiced':
                continue
            add_disc = 0.0
            invoice_id = res[picking.id]
            if model == 'sale.order':
                orders = inv_obj.browse(cr, uid, invoice_id).sale_order_ids
            else:
                orders = inv_obj.browse(cr, uid, invoice_id).purchase_order_ids
            if orders:
                add_disc = orders[0] and orders[0].add_disc or 0.0
                inv_obj.write(cr, uid, [invoice_id], {'add_disc': add_disc}, context)
                inv_obj.button_compute(cr, uid, [invoice_id])
        return res

