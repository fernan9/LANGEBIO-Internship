#! /usr/bin/env python
#coding=utf-8
""" DESCRIPTION

"""

import glob, sys, csv
from tabulate import tabulate
from Bio.Blast.Applications import NcbiblastnCommandline

"""--- FUNCTIONS ---"""

def carga_csv(file_name):
    """ creates a list of lists with a csv file """
    tabla = list()
    archivo = open(file_name+'.csv',"rU")
    csvreader = csv.reader(archivo, dialect=csv.excel_tab, delimiter = ',')
    for row in csvreader:
        tabla.append(row)
    return tabla

def crea_comparacion(tabla_ref, estructura = 'star', comparacion = 'uni'):
    """ creates comparisons lists (code) depending on arguments """
    lista = []
    tabla = list(tabla_ref)
    if estructura == 'star':
        nodo = tabla.pop(0)
        print nodo
        for organismo in tabla:
            lista.append([nodo[1],organismo[1]])
            if comparacion == 'bi':
                lista.append([organismo[1], nodo[1]])
    else:
        comps = estructura.split(',')
        for comp in comps:
            pareja = comp.split('-')
            query = tabla[int(pareja[0])][1]
            db = tabla[int(pareja[1])][1]
            lista.append([query, db])
            if comparacion == 'bi':
                lista.append([db, query])
    return lista

def imprime_comparacion(listas):
    """ prints the comparison as a readable format"""
    print 'COMPARISONS\n-----------\n'
    for lista in listas:
        print lista[0] + ' --> ' + lista[1]
    print '\n'

def imprime_referencia(claves):
    """ prints the comparison as a readable format"""
    print 'REFERENCE\n---------'
    n = 0
    for key, val in claves.items():
        print n, '. ', key, '\t', val
        n=n+1
    print '\n'

def crea_diccionario(tabla):
    """ creates a dictionary of code:organism"""
    diccionario={}
    for row in tabla:
        diccionario[row[1]]=row[0]
    return diccionario
    
"""--- PROGRAM BODY ---"""
print '----------------\nBLAST EVALUATION\n----------------'
blast_eval = 1e-05
comparison_list = []
# charge csv file
nombre_csv = raw_input('Please enter the CSV file name: ')
organismos = carga_csv(nombre_csv)
referencia = crea_diccionario(organismos)
comparison_list = crea_comparacion(organismos)
# present csv data
print '\nCSV data\n--------'
print tabulate(organismos, headers=["Organism","Code", "Genome File", "Database folder"]) + '\n'
# present options: blast parameters, comparison parameters, run
while 1:
    
    imprime_referencia(referencia)
    imprime_comparacion(comparison_list)
    print 'CHOOSE AN OPTION\n----------------\n1) Comparisons\n2) Run\n3) Quit'
    user_in = raw_input('Option: ')
    if user_in == '1':
        imprime_referencia(referencia)
        print ('Please enter the comparisons using the organism index.\n' +
              'Format: "-" between indices; "," between comparisons; no spaces.\n')
        nueva_comparacion = raw_input('Comparisons: ')
        print 'Choose "bi" for bidirectional or "uni" for unidirectional; no quotation marks.'
        tipo_comparacion = raw_input('Direction: ')
        comparison_list = crea_comparacion(organismos, nueva_comparacion, tipo_comparacion)
    elif user_in == '2':
        blast_eval = raw_input('\nPlease write the desired E value for BLAST runs; 1e-5 suggested.\nE_value: ')
        print '\nBLAST+ commands to be runned...\n'
        break
    elif user_in == '3': quit()
    else: print ('Incorrect option, try again.\n')

# create commands for comparisons
comandos = []
for pair in comparison_list:
    nombre = referencia[pair[0]].split()
    comandos.append([(nombre[0]+'_'+nombre[1]+'.fasta'), ('db_'+pair[1]+'/db_'+pair[1]), (pair[0]+'_'+pair[1]+'.xml')])
print tabulate(comandos, headers=["Genome file","Database", "Product file"]) + '\n'
raw_input('Press ENTER to continue')
# run commands, inform data created
for comando in comandos:
    blastn_cline = NcbiblastnCommandline(query=comando[0], db=comando[1], evalue=blast_eval ,outfmt=5, out=comando[2])
    print 'File ' + comando[2] + ' is currently in progess...'
    stdout, stderr = blastn_cline()
print 'WORK COMPLETED\n--------------'

