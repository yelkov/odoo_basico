# -*- coding: utf-8 -*-
from dataclasses import field

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class lineapedido(models.Model):
    _name = 'odoo_basico.lineapedido'
    _description = 'Módulo línea de pedido de odoo básico'

    producto = fields.Char(required=True,size=20,string="Producto:")
    descripcion = fields.Char(required=True,string='Descripción do producto:')
    pedido_id = fields.Many2one('odoo_basico.pedido',
                                ondelete= "cascade",required=True, string='Id do pedido:')
    informacion_ids = fields.Many2many("odoo_basico.informacion",
                                       string="Rexistro de Información",
                                       relation="odoo_basico_lineapedido_informacion",
                                       column1="lineapedido_id",column2="informacion_id")