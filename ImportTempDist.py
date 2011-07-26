# -*- encoding: utf-8 -*-

import decimal_precision as dp
import time
import base64
from tempfile import TemporaryFile
import math
from osv import fields, osv
import tools
import ir
import pooler
import tools
from tools.translate import _
import csv
import sys
import os
import re

def _ListaTipiFile(self, cr, uid, context={}):
    return [("T", "Sul Template"), ('V', 'Sulla Variante '), ('TV', 'Su Template e Variante')]



class product_template(osv.osv):

    _inherit = 'product.template'
    
    
    def _import_dist_mat_prime(self, cr, uid, lines, tipo, context):
       # import pdb;pdb.set_trace()
        import_data = {'tipo_file':  tipo}
        inseriti = 0
        aggiornati = 0
        PrimaRiga = True
        errori = ''
        for riga in  lines:
            #riga = riga.replace('"', '')
            #riga = riga.split(";")
            if PrimaRiga:
                testata = riga
                PrimaRiga = False
            else:
                if import_data['tipo_file'] == 'T':
                    #import pdb;pdb.set_trace()
                    #print riga
                    # il file deve aggiungere o aggiornare materie prime sul template
                    
                    TemplateIds = self.pool.get('product.template').search(cr, uid, [('codice_template', '=', riga[0])  ])
                    if TemplateIds:
                     for Template in TemplateIds:
                        #import pdb;pdb.set_trace()
                        ProductObjMatPrima = self.pool.get('product.product')
                        idProduct = ProductObjMatPrima.search(cr, uid, [('default_code', '=', riga[2].strip())])
                        if not idProduct:
                            errori = errori + 'Materia Prima ' + riga[2] + ' NON TROVATA ! \n'
                        else:
                         bomTemplObj = self.pool.get('bom.template')
                         idmatprima = bomTemplObj.search(cr, uid, [('template_id', '=', Template), ('product_id', '=', idProduct[0])])
                         if idmatprima:
                            # record trovato varia la riga
                            valore = {
                                      'product_qty':riga[1].replace(',', '.'),
                                      }
                            #import pdb;pdb.set_trace()
                            ok = bomTemplObj.write(cr, uid, idmatprima, valore)
                            aggiornati = aggiornati + 1                            
                         else:
                            # nuova riga di materie prima del template
                            valore = {
                                      'template_id':Template,
                                      'product_id':idProduct[0],
                                      'product_qty':riga[1].replace(',', '.'),
                                      }
                            #import pdb;pdb.set_trace()
                            idmatprima = bomTemplObj.create(cr, uid, valore)
                            
                            inseriti = inseriti + 1
                        valore = {
                                      'production_peso':riga[3].replace(',', '.'),
                                      }  
                        ok = self.pool.get('product.template').write(cr, uid, [Template], valore)       
                              
                if import_data['tipo_file'] == 'V':
                        #cicla su tutte le colonne che ci sono nel csv
                        #import pdb;pdb.set_trace()
                        nome = riga[0] + "-" + riga[1]    
                        BomVariantObj = self.pool.get('bom.variant')
                        ProductObj = self.pool.get('product.product') 
                        param = [('default_code', '=', riga[2].strip())]  
                        Product_id = ProductObj.search(cr, uid, param)    
                        BomVariantLineObj = self.pool.get('bom.variant.line')
                        param = [('name', '=', nome)]
                        idbomvariant = BomVariantObj.search(cr, uid, param)
                        if riga[3] == 'Q':
                            tipo = 'peso'
                        else:
                            tipo = 'perc'
                        if not Product_id:
                            errori = errori + 'Materia Prima ' + riga[2] + ' NON TROVATA ! \n'
                        else:
                         if not idbomvariant:
                            # devo inserire tutto nuovo prima in testata e poi nelle righe le materie prime
                            valore = {
                                       'name':nome,
                                      }
                            idbomvariant = BomVariantObj.create(cr, uid, valore)
                            
                            valore = {
                                       'bom_variant_id':idbomvariant,
                                       'product_material_id':Product_id[0],
                                       'material_qty':riga[4].replace(',', '.'),
                                       'tipo_calcolo':tipo
                                      }
                            idvarline = BomVariantLineObj.create(cr, uid, valore)
                            inseriti = inseriti + 1
                         else:                            
                            # trovato il record in testata per questo tipo non può cambiare nulla ma nel corpo può aggiungere righe o modificare le esistenti
                            param = [('bom_variant_id', '=', idbomvariant[0]), ('product_material_id', '=', Product_id[0])]
                            idvarline = BomVariantLineObj.search(cr, uid, param)
                            if idvarline:
                                # trovato il recod modifica
                                valore = {
                                       'bom_variant_id':idbomvariant[0],
                                       'product_material_id':Product_id[0],
                                       'material_qty':riga[4].replace(',', '.'),
                                       'tipo_calcolo':tipo
                                      }
                                ok = BomVariantLineObj.write(cr, uid, idvarline, valore)
                                aggiornati = aggiornati + 1
                            else:
                                # aggiunge una nuova riga
                                valore = {
                                       'bom_variant_id':idbomvariant[0],
                                       'product_material_id':Product_id[0],
                                       'material_qty':riga[4].replace(',', '.'),
                                       'tipo_calcolo':tipo
                                      }
                                idvarline = BomVariantLineObj.create(cr, uid, valore)
                                inseriti = inseriti + 1                                
                                        
                                        
                if import_data['tipo_file'] == 'TV' :
                        #cicla su tutte le colonne che ci sono nel csv
                        #import pdb;pdb.set_trace()
                        nome = riga[0] + "-" + riga[1]    
                        BomVariantObj = self.pool.get('bom.variant')
                        Template = self.pool.get('product.template').search(cr, uid, [('codice_template', '=', riga[2])])[0]
                        ProductObj = self.pool.get('product.product') 
                        param = [('default_code', '=', riga[4].strip())]  
                        Product_id = ProductObj.search(cr, uid, param)    
                        BomVariantLineObj = self.pool.get('bom.variant.line')
                        param = [('name', '=', nome), ('template_material_id', '=', Template)]
                        idbomvariant = BomVariantObj.search(cr, uid, param)
                        if riga[3] == 'Q':
                            tipo = 'peso'
                        else:
                            tipo = 'perc'
                        if not Product_id:
                            errori = errori + 'Materia Prima ' + riga[4] + ' NON TROVATA ! \n'
                        else:                            
                         if not idbomvariant:
                            # devo inserire tutto nuovo prima in testata e poi nelle righe le materie prime
                            valore = {
                                       'name':nome,
                                       'template_material_id':Template,
                                      }
                            idbomvariant = BomVariantObj.create(cr, uid, valore)
                            
                            valore = {
                                       'bom_variant_id':idbomvariant,
                                       'product_material_id':Product_id[0],
                                       'material_qty':riga[5].replace(',', '.'),
                                       'tipo_calcolo':tipo
                                      }
                            idvarline = BomVariantLineObj.create(cr, uid, valore)
                            inseriti = inseriti + 1
                         else:                            
                            # trovato il record in testata per questo tipo non può cambiare a meno che non utilizziamo la qta nulla ma nel corpo può aggiungere righe o modificare le esistenti
                            param = [('bom_variant_id', '=', idbomvariant[0]), ('product_material_id', '=', Product_id[0])]
                            idvarline = BomVariantLineObj.search(cr, uid, param)
                            if idvarline:
                                # trovato il recod modifica
                                valore = {
                                       'bom_variant_id':idbomvariant[0],
                                       'product_material_id':Product_id[0],
                                       'material_qty':riga[5].replace(',', '.'),
                                       'tipo_calcolo':tipo
                                      }
                                ok = BomVariantLineObj.write(cr, uid, idvarline, valore)
                                aggiornati = aggiornati + 1
                            else:
                                # aggiunge una nuova riga
                                valore = {
                                       'bom_variant_id':idbomvariant[0],
                                       'product_material_id':Product_id[0],
                                       'material_qty':riga[5].replace(',', '.'),
                                       'tipo_calcolo':tipo
                                      }
                                idvarline = BomVariantLineObj.create(cr, uid, valore)
                                inseriti = inseriti + 1                                
                                        
                    
        return [inseriti, aggiornati, errori]

 

    
    
    def run_auto_import_matprime(self, cr, uid, automatic=False, use_new_cursor=False, context=None):
      pool = pooler.get_pool(cr.dbname)  
      #import pdb;pdb.set_trace()
      testo_log = """Inizio procedura di Aggiornamento/Inserimento Materie Prime su Template e Varianti """ + time.ctime() + '\n'
      percorso = '/home/openerp/filecsv'
      partner_obj = pool.get('product.template')
      if use_new_cursor:
        cr = pooler.get_db(use_new_cursor).cursor()
      elenco_csv = os.listdir(percorso)
      for filecsv in elenco_csv:
        codfor = filecsv.split(".")
        testo_log = testo_log + " analizzo file " + codfor[0] + ".csv \n"
        lines = csv.reader(open(percorso + '/' + filecsv, 'rb'), delimiter=";")
        if codfor[0].lower() == "distempl":
            #lancia il metodo per tutti i modelli
            #import pdb;pdb.set_trace() 
            res = self._import_dist_mat_prime(cr, uid, lines, 'T', context)
        if codfor[0].lower() == "disvarn":
            #lancia il metodo per le categorie indicate
            #import pdb;pdb.set_trace() 
            res = self._import_dist_mat_prime(cr, uid, lines, 'V', context)
        if codfor[0].lower() == "disvaret":
            #lancia il metodo per i modelli indicati
            #import pdb;pdb.set_trace() 
            res = self._import_dist_mat_prime(cr, uid, lines, 'TV', context)
        if res:  
          testo_log = testo_log + " Inseriti " + str(res[0]) + " Aggiornati " + str(res[1]) + " MATERIE PRIME \n"
          #import pdb;pdb.set_trace()
          testo_log = testo_log + str(res[2]) 
        else:
          testo_log = testo_log + " File non riconosciuto  " + codfor[0] + " non trovato  \n"
        os.remove(percorso + '/' + filecsv)
      testo_log = testo_log + " Operazione Teminata  alle " + time.ctime() + "\n"
      #invia e-mail
      type_ = 'plain'
      tools.email_send('OpenErp@mainettiomaf.it',
                       ['Giuseppe.Sciacco@mainetti.com', 'g.dalo@cgsoftware.it'],
                       'Import Automatico Varianti Articoli',
                       testo_log,
                       subtype=type_,
                       )
    

        
      return
product_template()
