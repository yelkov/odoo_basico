# -*- coding: utf-8 -*-
from dataclasses import field

from odoo import models, fields, api
from odoo.api import ondelete
from odoo.exceptions import ValidationError


class pedido(models.Model):
    _name = 'odoo_basico.pedido'
    _description = 'Módulo pedido de odoo básico'

    nome = fields.Char(required=True,size=20,string="Nome pedido:")
    data = fields.Date(required=True,string="Data do pedido:")
    lineapedido_ids = fields.One2many("odoo_basico.lineapedido",'pedido_id', string='Líneas de pedido:')
    cliente = fields.Many2one('res.partner', ondelete="cascade", required=True)
    name = fields.Char(required=True,size=20,string="Identificador de Pedido")
    persoa_id = fields.Many2one('res.partner', ondelete="set null", domain="[('visible','=','True')]", index= True, string="Persoa: ")

    def actualizadorSexo(self):
        informacion_ids = self.env['odoo_basico.informacion'].search([('autorizado', '=', False)])
        for rexistro in informacion_ids:
            self.env['odoo_basico.informacion']._cambia_campo_sexo(rexistro)

    def creaRexistroInformacion(self):
        creado_id = self.env['odoo_basico.informacion'].create({'name': 'Creado dende pedido'})
        creado_id.descripcion =  "Creado dende o modelo pedido"
        creado_id.autorizado = False

    def actualizaRexistroInformacion(self):
        informacion_id = self.env['odoo_basico.informacion'].search([('name', '=','Creado dende pedido')])
        if informacion_id:
            informacion_id.name = "Actualizado ..."
            informacion_id.descripcion = "Actualizado dende o modelo pedido"
            informacion_id.sexo_traducido = "Mujer"

    def actualizadorHoraTimezone(self):
        # informacion_ids = self.env['odoo_basico.informacion'].search([])
        # for rexistro in informacion_ids:
        #     self.env['odoo_basico.informacion'].chamado_dende_pedido_e_dende_apidepends(rexistro)
        informacion_ids = self.env['odoo_basico.informacion'].search([])
        self.env['odoo_basico.informacion'].chamado_dende_pedido_e_dende_apidepends(informacion_ids)