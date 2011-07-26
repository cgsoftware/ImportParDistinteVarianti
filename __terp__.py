# -*- encoding: utf-8 -*-
##############################################################################
#    
#    Copyright (C) 2009 Italian Community (http://www). 
#    All Rights Reserved
#    $Id$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': 'IMPORT DA EXCEL LE TABELLE CHE LEGANO LE VARIANTI ED I TEMPLATE ALLE MATERIE PRIME',
    'version': '0.1',
    'category': 'Localisation/Italy',
    'description': """Importazione DETTAGLI MATERIE PRIME LEGATE ALLE DIMENSIONI VARIANTI PER CREARE IN AUTOMATICO LE DISTINTE BASI, formati csv/txt 
      esistono 3 tipo di importazione:
      1) distempl.csv, dettaglio di materie prime valide per tutto il tamplate
      2) disvaret.csv, dettaglio di materie prime determinate puntando ad un template di materia prima o semilavorato ed incrociato con lo stesso valore
      3) disvarn.csv, dettaglio di materie prime legate alla sola dimensione variante dell'articolo
      
      sulla prima riga del file excel vanno indicati i campi
      1) TEMPLATE	quantita	matprima	PESO gr
      2) DIMENSION	VARIANTE	CODICE TEMPLATE	100% O P	MATERIA PRIMA	QUANTITA
      3) DIMENSION	VARIANTE	COD. MATER	 % O PESO	QUANTITA
      """,
    'author': 'C & G Software sas',
    'website': 'http://www.cgsoftware.it',
    "depends" : ['product_variant_multi', 'product'],
    "update_xml" : [],
    "active": False,
    "installable": True
}

