# -*- coding: utf-8 -*-

from odoo import models, fields, api


class odoo_basico(models.Model):
    _name = 'odoo_basico.informacion'
    _description = 'Módulo ejemplo de odoo básico'

    name = fields.Char(required=True,size=20,string="Titulo")
    descripcion = fields.Text(string="Descripción")
    alto_en_cm = fields.Integer(string="Alto en cm:")
    bajo_en_cm = fields.Integer(string="Ancho en cm:")
    largo_en_cm = fields.Integer(string="Largo en cm:")
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

