# -*- coding: utf-8 -*-

from odoo import models, fields, api


class odoo_basico(models.Model):
    _name = 'odoo_basico.informacion'
    _description = 'Módulo ejemplo de odoo básico'

    name = fields.Char(required=True,size=20,string="Titulo:")
    descripcion = fields.Text(string="Descripción:")
    alto_en_cms = fields.Integer(string="Alto en cm:")
    ancho_en_cms = fields.Integer(string="Ancho en cm:")
    longo_en_cms = fields.Integer(string="Largo en cm:")
    peso = fields.Float(digits=(6,2),default=2.7,string="Peso en Kg:")
    autorizado = fields.Boolean(string="¿Autorizado?",default=True)
    sexo_traducido = fields.Selection([('Hombre','Home'),('Mujer','Muller'),('Otros','Outros')],string="Sexo:")
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100



