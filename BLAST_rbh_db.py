#! /usr/bin/env python

""" 
RBH for Ortholog Search 1.0 20/03/2015

CONTACT
Fernan Rodrigo Pérez Gálvez  +52 (442) 272 4272  fernan954<at>gmail<dot>com

GENERAL DESCRIPTION
this script loads databases for a series of anotated genomes
also, makes blast all-to-all depending of a web topology
"""

import glob, sys, csv
from tabulate import tabulate


"""--- FUNCTIONS ---"""

def trim_all(datos):
    """ erases organisms with no genome file or db in working folder """
    nuevo_datos = list(datos)
    salida = list()
    for nuevo_dato in nuevo_datos:
        print nuevo_dato
        if (nuevo_dato[2] == True or nuevo_dato[3]==True):
            salida.append(nuevo_dato)
    return salida

def trim_and_db(entrada):
    """ erases organisms with no genome file, creates missing databases """
    import subprocess
    datos = list(entrada)
    nuevo_datos = list()
    for dato in datos:
        if dato[2] == False:
            # remove organisms with no genome data
            print "\t+ Organism '{}' removed from data.\n".format(dato[0])
        elif dato[3] == False:
            # create db of missing genome files
            comando = 'makeblastdb -in {0}.faa -title db_{1} -dbtype prot -out db_{1}/db_{1} -parse_seqids'.format(dato[0].replace(' ','_'),dato[1])
            subprocess.call(comando.split())
            dato[3] = True
            print "\t+ BLAST+ database from '{0}' successfully created: {1}.\n".format(dato[0], dato[1])
            nuevo_datos.append(dato)
        else:
            nuevo_datos.append(dato)
    return nuevo_datos

"""--- PROGRAM BODY ---"""

# load a file with the organism names to an object
organisms_ruta = raw_input("Enter the name of the file (with extension) containing the organism list: ")
organisms = []
salida = []
with open(organisms_ruta, 'r') as f:
    organisms = [[line.strip()] for line in f]
# create the data object, a list organism - code
for organism in organisms:
    nombre = organism[0].split()
    codigo = nombre[0][0] + nombre[1][0:3]
    organism.append(codigo)

filenames = glob.glob('*.faa')+(glob.glob('*.fna'))+(glob.glob('*.fasta'))
paths = glob.glob('*/')
for organism in organisms:
    # internal search genome files by org name, record results
    if organism[0].replace(' ','_')+'.faa' in filenames or organism[0].replace(' ','_')+'.fasta' in filenames :
        organism.append(True)
    else: organism.append(False)
    # internal search for db with code, record results
    if 'db_'+organism[1]+'/' in paths:
        organism.append(True)
    else: organism.append(False)

# print summary of information
print '\n'
print tabulate(organisms, headers=["Organism","Code", "Genome File", "Database folder"])
print '\n'

bandera = True
for organism in organisms:
    for i in organism:
        if i==False: bandera = False

# check for complete information
if bandera == True:
    #say it's all complete and right
    raw_input('All data is complete\n'+
              '--------------------\n\n'+'A "*.csv" file will be created.\nPress enter to continue...')
    salida = organisms
else:
    #ask for trimming or data base creation
    while 1:
        answer1 = raw_input(
            "Some information is missing.\n" + 
            "----------------------------\n" +
            " + Enter 'trim' to use only available data\n" + 
            " + Enter 'fill' to create missing databases if genome file is present\n" +
            " + Enter 'cancel' to break this process.\n" + 
            "SELECTION: ")
        if answer1 in ('trim','fill'): break
        elif answer1 == 'cancel': sys.exit("You have terminated this program.")
        else: 'Non-valid selection, please retry\n'
    # apply trimming
    if answer1 == 'trim':
        print organisms
        salida = trim_all(organisms)
    else:
        salida = trim_and_db(organisms)
# print final database
print '\nFinal Database\n--------------\n'
print tabulate(salida, headers=["Organism","Code", "Genome File", "Database folder"])
nombre = raw_input('\nPlease give a name for the CSV file: ')
# create csv
with open(nombre+".csv", "wb") as f:
    writer = csv.writer(f)
    writer.writerows(salida)
with open(nombre+"_codes.txt", "wb") as thefile:
    for item in salida:
        thefile.write("%s\n" % item[1])
print 'CSV file created\nEnd of execution'

# ask for continue to BLAST or quit



"""
"""
