# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class odoo_basico(models.Model):
    _name = 'odoo_basico.informacion'
    _description = 'Módulo ejemplo de odoo básico'

    name = fields.Char(required=True,size=20,string="Titulo:")
    descripcion = fields.Text(string="Descripción:")
    alto_en_cms = fields.Integer(string="Alto en cm:")
    ancho_en_cms = fields.Integer(string="Ancho en cm:")
    longo_en_cms = fields.Integer(string="Largo en cm:")
    peso = fields.Float(digits=(6,2),default=2.7,string="Peso en Kg:")
    volume = fields.Float(digits=(6,7),compute="_volume", store=True, string="Volume m3")
    densidad = fields.Float(digits=(6,2),compute="_densidad",store=True,string="Densidad Kg/m3")
    autorizado = fields.Boolean(string="¿Autorizado?",default=True)
    sexo_traducido = fields.Selection([('Hombre','Home'),('Mujer','Muller'),('Otros','Outros')],string="Sexo:")
    literal = fields.Char(store=False)

    _sql_constraints = [('nomeUnico', 'unique(name)', 'Non se pode repetir o nome')]
    _order = "descripcion desc"

    @api.depends('alto_en_cms', 'longo_en_cms', 'ancho_en_cms')
    def _volume(self):
        for rexistro in self:
            rexistro.volume = float(rexistro.alto_en_cms) * float(rexistro.longo_en_cms) * float(rexistro.ancho_en_cms) / 1000000

    @api.depends('volume', 'peso')
    def _densidad(self):
        for rexistro in self:
            if rexistro.volume != 0:
                rexistro.densidad = float(rexistro.peso) / float(rexistro.volume)
            else:
                rexistro.densidad = 0.00

    @api.onchange('alto_en_cms')
    def _avisoAlto(self):
        for rexistro in self:
            if rexistro.alto_en_cms > 7:
                rexistro.literal = 'O alto ten un valor posiblemente excesivo %s é maior que 7' % rexistro.alto_en_cms
            else:
                rexistro.literal = ""

    @api.constrains('peso')  # Ao usar ValidationError temos que importar a libreria ValidationError
    def _constrain_peso(self):   # from odoo.exceptions import ValidationError
        for rexistro in self:
            if rexistro.peso < 1 or rexistro.peso > 4:
                raise ValidationError('Os peso de %s ten que ser entre 1 e 4 ' % rexistro.name)

#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100



