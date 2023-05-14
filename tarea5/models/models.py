# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re

class paciente(models.Model):
    _name = 'centro_logopedia.paciente'
    _description = 'centro_logopedia.paciente'
    name = fields.Char(string='Nombre',help='Nombre del paciente',required=True)
    birth_date = fields.Date(string='Fecha de nacimiento',help='Fecha de nacimiento del paciente',required=True)
    phone = fields.Char(string='Teléfono',help='Teléfono de contacto del paciente',required=True)
    sesiones_ids = fields.One2many("centro_logopedia.sesion","paciente_id",string="Sesiones")
    @api.constrains('phone')
    def _check_phone(self):
        regex = re.compile('[0-9]{9}\Z',re.I)
        for record in self:
            if record.phone:
                print(f"REGISTRO:{record.phone}")
                if not regex.match(record.phone):
                    raise ValidationError('Error. Indique el número de teléfono con 9 dígitos')

class logopeda(models.Model):
    _name = 'centro_logopedia.logopeda'
    _description = 'centro_logopedia.logopeda'
    name = fields.Char(string='Nombre',help='Nombre del/a logopeda',required=True)
    specialty = fields.Selection(string='Especialidad', selection=[('general','General/Diagnóstico'),('disfagia', 'Disfagia'), ('disfonia', 'Disfonía'), ('autismo','Autismo')],default='general')
    phone = fields.Char(string='Teléfono',help='Teléfono de contacto del logopeda',required=True)
    sesiones_ids = fields.One2many("centro_logopedia.sesion","logopeda_id",string="Sesiones")

class sesion(models.Model):
    _name = 'centro_logopedia.sesion'
    _description = 'centro_logopedia.sesion'
    paciente_id = fields.Many2one(
        string='Paciente',
        help='Id del paciente',
        comodel_name='centro_logopedia.paciente',
        ondelete='set null',
    )
    logopeda_id = fields.Many2one(
        string='Logopeda',
        help='Id del/a logopeda',
        comodel_name='centro_logopedia.logopeda',
        ondelete='set null',
    )
    date = fields.Datetime(string='Fecha y hora',help='Fecha y hora de la sesión',default=lambda self: fields.Datetime.now())
    duration = fields.Integer(string='Duración',help='Duración en minutos de la sesión',default=45)