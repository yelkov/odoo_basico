# -*- coding: utf-8 -*-

from odoo import models, fields, api


class odoo_basico(models.Model):
    _name = 'odoo_basico.suceso'
    _description = 'Módulo 2 de odoo básico'

    name = fields.Char(required=True, size=20, string="Suceso")
    descripcion = fields.Text(string="A Descripción do Suceso")  # string é a etiqueta do campo
    nivel = fields.Selection([('Baixo', 'Baixo'), ('Medio', 'Medio'), ('Alto', 'Alto')], string='Nivel')
    data_hora = fields.Datetime(string="Data e Hora", default=lambda self: fields.Datetime.now())
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100