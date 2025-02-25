from odoo import models, api, fields


class accion_planificada (models.Model):
    #_inherit = "account.invoice" # Odoo Version 12
    _inherit = "account.move" # Odoo Version 13

    @api.model
    def listado_facturas(self):
        usuario_que_executa_o_metodo_que_e_o_definido_no_xml = self.env.user  # usuario=__system que ten en res_partner name=OdooBot
        self.env.user.tz = self.env['res.partner'].search([('id', '=', 3)])[0].tz  # como ten tz=UTC poñemoslle o tz do usuario=3 que é o administrador
        agora = self.env['odoo_basico.informacion'].convirte_data_hora_de_utc_a_timezone_do_usuario(fields.Datetime.now())
        self.env.user.tz = 'UTC' # deixamolo como estaba con tz=UTC
        #facturas_ids = self.search([('state', '=', 'open')]) Version Odoo 12
        facturas_pagadas_ids = self.search([('payment_state', '=', 'paid')])
        facturas_no_pagadas_ids = self.search([('payment_state','=','not_paid'),('move_type','=','out_invoice')])
        if facturas_pagadas_ids:
            listado = ""
            for rexistro in facturas_pagadas_ids:
                #listado = listado + "<br/>" + str(rexistro.number) + "-> " + str(rexistro.partner_id.display_name) + "-> " + str(rexistro.amount_total) Version Odoo 12
                listado = listado + "<br/>" + str(rexistro.name) + "-> " + str(rexistro.partner_id.display_name) + "-> " + str(rexistro.amount_residual)
            # mail_de     Odoo pon o email que configuramos en gmail para facer o envio
            self.enviar_listado_por_correo(agora, listado, usuario_que_executa_o_metodo_que_e_o_definido_no_xml,"Listaxe de facturas pagadas neste momento %s")

        if facturas_no_pagadas_ids:
            listado = ""
            for rexistro in facturas_no_pagadas_ids:
                #listado = listado + "<br/>" + str(rexistro.number) + "-> " + str(rexistro.partner_id.display_name) + "-> " + str(rexistro.amount_total) Version Odoo 12
                listado = listado + "<br/>" + str(rexistro.name) + "-> " + str(rexistro.partner_id.display_name) + "-> " + str(rexistro.amount_residual)
            # mail_de     Odoo pon o email que configuramos en gmail para facer o envio
            self.enviar_listado_por_correo(agora, listado, usuario_que_executa_o_metodo_que_e_o_definido_no_xml, "Listaxe de facturas non pagadas neste momento %s")

    def enviar_listado_por_correo(self, agora, listado, usuario_que_executa_o_metodo_que_e_o_definido_no_xml,asunto):
        mail_reply_to = usuario_que_executa_o_metodo_que_e_o_definido_no_xml.partner_id.email  # odoobot@example.com
        mail_para = self.env['res.partner'].search([('id', '=', 3)])[0].email  # o enderezo email de destino
        mail_valores = {
            'subject': asunto % agora,
            'author_id': usuario_que_executa_o_metodo_que_e_o_definido_no_xml.id,
            'email_from': mail_reply_to,
            'email_to': mail_para,
            'message_type': 'email',
            'body_html': "Neste momento %s existen as seguintes facturas: %s" % (agora, str(listado)),
        }
        mail_id = self.env['mail.mail'].create(mail_valores)
        mail_id.send()