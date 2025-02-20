# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
import os
import pytz
import locale

from . import miñasUtilidades


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
    foto = fields.Binary(string='Foto')
    adxunto_nome = fields.Char(string="Nome Adxunto")
    adxunto = fields.Binary(string="Arquivo adxunto")

    #Os campos Many2one crean un campo na BD
    moeda_id = fields.Many2one('res.currency',domain="[('active','=','true')]")
    #con domain, filtramos os valores mostrados. Pode ser mediante unha constante (vai entre comillas) ou unha variable
    moeda_en_texto = fields.Char(related="moeda_id.currency_unit_label",string="Moeda en formato texto")

    creador_da_moeda = fields.Char(related="moeda_id.create_uid.login",string="Usuario creador da moeda",)

    #ahora utilizamos una funcion lambda para, en una relacion Many2One poner un valor por defecto - el euro
    moeda_euro_id = fields.Many2one('res.currency',default=lambda self: self.env['res.currency'].search([('name', '=', "EUR")],limit=1))
    #Este campo utilizaremolo para pasarllo como parámetro a un campo tipo fields.Monetary, para que ese campo traballe sempre con Euros.

    gasto_en_euros = fields.Monetary("Gasto en Euros", 'moeda_euro_id')

    moeda_dolar_id = fields.Many2one('res.currency',default= lambda  self: self.env['res.currency'].search([('name','=',"USD")],limit=1))
    gasto_en_dolares = fields.Monetary("Gasto en Dolares",'moeda_dolar_id')

    data = fields.Date(string="Data", default=lambda self: fields.Date.today())
    data_hora = fields.Datetime(string="Data e Hora", default=lambda self: fields.Datetime.now())

    hora_utc  = fields.Char(compute="_actualiza_hora_utc",string="Hora UTC", size=15, store=True)
    hora_timezone_usuario  = fields.Char(compute="actualiza_hora_timezone_usuario",string="Hora Timezone do Usuario", size=15, store=True)

    mes_castelan = fields.Char(compute="_mes_castelan", string="Mes castellano: ")
    mes_galego = fields.Char(compute="_mes_galego", string="Mes galego: ")
    mes_aleman = fields.Char(compute="_mes_aleman", string="Mes alemán: ")


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


    def _cambia_campo_sexo(self, rexistro):
        rexistro.sexo_traducido = "Hombre"

    def envio_email(self):
        meu_usuario = self.env.user
        #mail_de     Odoo pon o email que configuramos en gmail para facer o envio
        mail_reply_to = meu_usuario.partner_id.email  # o enderezo email que ten asociado o noso usuario
        mail_para = 'evanchapela@gmail.com'  # o enderezo email de destino
        mail_valores = {
            'subject': 'Aquí iría o asunto do email ',
            'author_id': meu_usuario.id,
            'email_from': mail_reply_to,
            'email_to': mail_para,
            'message_type': 'email',
            'body_html': 'Aquí iría o corpo do email cos datos por exemplo de "%s" ' % self.descripcion,
        }
        mail_id = self.env['mail.mail'].create(mail_valores)
        mail_id.sudo().send()
        return True

    def ver_contexto(self): # Este método é chamado dende un botón de informacion.xml
        for rexistro in self:
            #Ao usar warning temos que importar a libreria mediante from odoo.exceptions import Warning
            #Importamos tamén a libreria os mediante import os
            raise ValidationError(
                'Contexto: %s Ruta: %s Contido %s' % (rexistro.env.context, os.getcwd(),os.listdir(os.getcwd())))
            #env.context é un diccionario  https://www.w3schools.com/python/python_dictionaries.asp
        return True

    @api.depends('data_hora')
    def _actualiza_hora_utc(self):
        for rexistro in self: # A hora se almacena na BD en horario UTC (2 horas menos no verán, 1 hora menos no inverno)
            rexistro.hora_utc = rexistro.data_hora.strftime("%H:%M:%S")

    def convirte_data_hora_de_utc_a_timezone_do_usuario(self,data_hora_utc_object):  # recibe a data hora en formato object
        usuario_timezone = pytz.timezone(self.env.user.tz or 'UTC')  # obter a zona horaria do usuario. Ollo!!! nas preferencias do usuario ten que estar ben configurada a zona horaria
        return pytz.UTC.localize(data_hora_utc_object).astimezone(usuario_timezone)  # hora co horario do usuario en formato object
        # para usar  pytz temos que facer  import pytz

    @api.depends('data_hora')
    def actualiza_hora_timezone_usuario(self): # Non pode ser un metodo privado porque da erro ao ser chamado dende o boton na vista xml        # "_actualiza_hora_timezone_usuario en odoo_basico.informacion es privado y no se puede activar con un botón"
        for rexistro in self:
            rexistro.chamado_dende_pedido_e_dende_apidepends(rexistro)  # leva rexistro como parametro por que chamado_dende_pedido_e_dende_apidepends ten 2 parametros

    def chamado_dende_pedido_e_dende_apidepends(self,parametro_cos_datos_a_actualizar):  # Ten 2 parametros xa que polo segundo recibe os rexistros que queremos actualizar dende pedido
        # TypeError: informacion.actualiza_hora_timezone_usuario() takes 1 positional argument but 2 were given
        #     parametro_cos_datos_a_actualizar.hora_timezone_usuario = self.convirte_data_hora_de_utc_a_timezone_do_usuario(parametro_cos_datos_a_actualizar.data_hora).strftime("%H:%M:%S")  # Convertimos a hora de UTC a hora do timezone do usuario
        for rexistro in parametro_cos_datos_a_actualizar:
            rexistro.hora_timezone_usuario = rexistro.convirte_data_hora_de_utc_a_timezone_do_usuario(rexistro.data_hora).strftime("%H:%M:%S")  # Convertimos a hora de UTC a hora do timezone do usuario


    # Podemos  configurar locales a nivel de sistema con dpkg-reconfigure locales poñendo un por defecto.
    # apt-get install locales
    # dpkg-reconfigure locales (podemos configurar varios)
    # locale (ver o locale por defecto)
    # locale -a (ver os dispoñibles)

    @api.depends('data')
    def _mes_castelan(self):
        # O idioma por defecto é o configurado en locale na máquina onde se executa odoo.
        # Podemos cambialo con locale.setlocale, os idiomas teñen que estar instalados na máquina onde se executa odoo.
        # Lista onde podemos ver os distintos valores: https://docs.moodle.org/dev/Table_of_locales#Table
        # Definimos en miñasUtilidades un método para asignar o distinto literal que ten o idioma en función da plataforma Windows ou GNULinux
        locale.setlocale(locale.LC_TIME, miñasUtilidades.cadeaTextoSegunPlataforma('Spanish_Spain.1252','es_ES.utf8'))
        for rexistro in self:
            rexistro.mes_castelan = rexistro.data.strftime("%B") # strftime https://strftime.org/

    @api.depends('data')
    def _mes_galego(self):
        # O idioma por defecto é o configurado en locale na máquina onde se executa odoo.
        # Podemos cambialo con locale.setlocale, os idiomas teñen que estar instalados na máquina onde se executa odoo.
        # Lista onde podemos ver os distintos valores: https://docs.moodle.org/dev/Table_of_locales#Table
        # Definimos en miñasUtilidades un método para asignar o distinto literal que ten o idioma en función da plataforma Windows ou GNULinux
        locale.setlocale(locale.LC_TIME, miñasUtilidades.cadeaTextoSegunPlataforma('Galician_Spain.1252', 'gl_ES.utf8'))
        for rexistro in self:
            rexistro.mes_galego = rexistro.data.strftime("%B")
        locale.setlocale(locale.LC_TIME, miñasUtilidades.cadeaTextoSegunPlataforma('Spanish_Spain.1252', 'es_ES.utf8'))


    @api.depends('data')
    def _mes_aleman(self):
        # O idioma por defecto é o configurado en locale na máquina onde se executa odoo.
        # Podemos cambialo con locale.setlocale, os idiomas teñen que estar instalados na máquina onde se executa odoo.
        # Lista onde podemos ver os distintos valores: https://docs.moodle.org/dev/Table_of_locales#Table
        # Definimos en miñasUtilidades un método para asignar o distinto literal que ten o idioma en función da plataforma Windows ou GNULinux
        locale.setlocale(locale.LC_TIME, miñasUtilidades.cadeaTextoSegunPlataforma('German_Germany.1252', 'de_DE.UTF-8'))
        for rexistro in self:
            rexistro.mes_aleman = rexistro.data.strftime("%B")
        locale.setlocale(locale.LC_TIME, miñasUtilidades.cadeaTextoSegunPlataforma('Spanish_Spain.1252', 'es_ES.utf8'))


#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
