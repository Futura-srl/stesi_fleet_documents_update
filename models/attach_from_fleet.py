from odoo import models, fields, api, _
from odoo.exceptions import UserError
import magic, base64
import logging

_logger = logging.getLogger(__name__)



class AttachFromFleetInherit(models.TransientModel):
    _inherit = 'attach.from.fleet'

    name = fields.Char(string="Name")
    file = fields.Binary(string="File")


    def get_file_extension_from_base64(self, base64_string):
        try:
            # Decodifica la stringa Base64 in dati binari
            decoded_data = base64.b64decode(base64_string)
    
            # Utilizza la libreria python-magic per identificare il tipo di file
            mime = magic.Magic()
            file_type = mime.from_buffer(decoded_data)
    
            _logger.info("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
            _logger.info(file_type)
            _logger.info("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
    
            # Mappa i tipi di file riconosciuti alle rispettive estensioni
            file_extension_map = {
                'jpeg': '.jpg',
                'png': '.png',
                'pdf': '.pdf',
                'excel': '.xlsx',
            }
    
            # Cerca una corrispondenza parziale nel tipo di file
            for key, value in file_extension_map.items():
                if key.lower() in file_type.lower():
                    _logger.info(value)
                    return value
    
            # Nessuna corrispondenza trovata, restituisci il valore di default
            _logger.info(".bin")
            return ".bin"
    
        except Exception as e:
            # Gestisci eventuali errori durante la decodifica
            return f"Errore durante la decodifica Base64: {str(e)}"

    
    # description
    def create_documents(self):
        id_log = self.id
        extension = self.get_file_extension_from_base64(self.file)
        if self.log_service_id.id != False:
            extension = self.get_file_extension_from_base64(self.file)
            id_log = self.log_service_id.id
        if self.contract_id.id != False:
            extension = self.get_file_extension_from_base64(self.file)
            id_log = self.contract_id.id
        default_facet = self.env['documents.facet'].search([('default_facet_for_fleet', '=', True)])

        document_name = self.fleet_id.name
        if self.tag_id:
            document_name += "_" + self.tag_id.name + "_" + str(id_log) + extension
        self.env['documents.document'].create({
            'datas': self.file,
            'name': document_name,
            'tag_ids': self.tag_id,
            'fleet_id': self.fleet_id.id,
            'service_id': self.log_service_id.id if self.log_service_id else False,
            'contract_id': self.contract_id.id if self.contract_id else False,
            'folder_id': default_facet.folder_id.id,
        })
