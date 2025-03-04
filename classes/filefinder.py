# Copyright Archy's Software I

import os
import fleep
import locale
import json
from classes.helper import Helper as helper

import subprocess
from time import time

from os import system
import modules.colorize as bcolors

# Class to index and locate files in the filesystem using Popen("Linux command", "OPTION")
class FileFinder:
    #start_path = '/home/archy/Test/'

    def __init__(self, *args, **kwargs):
        return super().__init__(*args, **kwargs)

    def updateDB(args):

        system.call("updatedb --output dbs/media-terra.db --database-root /run/media/archy/terra")
        #with Popen(args, stdout=PIPE) as p:
        #    try:
        #        return p.wait(timeout=None)
        #    except:
        #        p.kill()
        #        p.wait()



    def getFileIndex(db_file):
        #locale.setlocale(locale.LC_ALL, 'utf8')
        all_files = []
        args = ["locate", f'-d{db_file}', "*"]
        #print(args)

        #p = subprocess.call("echo", shell=False)
        #p = subprocess.check_output("locate -d %s .jpg" % format(db_file), shell=True)

        #print(p)
        p = subprocess.Popen(args, stdout=subprocess.PIPE)

        for line in p.stdout:
            filepath = line.decode("utf-8") # Decode from binary mode to string so  b' goes away
            filepath = str(filepath)[:-1] # Slice away /n at end of line
            all_files.append(line)

        return all_files



    def getFilesByExtension(extension, filepath_index):
        verbose = None
        found_files = []
        #extension = extension.lower()

        for filepath in filepath_index:
            # filepath = line.decode("utf-8") # Decode from binary mode to string so  b' goes away
            # filepath = str(filepath)[:-1] # Slice away /n at end of line
            #filepath = filepath.lower()
            filepath = filepath.decode("utf-8")
            filepath = str(filepath)
            filepath = filepath.strip('\n')

            file_name, file_ext = os.path.splitext(filepath)
            #file_ext = file_ext.strip('.')

            #print(file_name)
            #print(file_ext)

            #if str.lower(file_ext) == str.lower(extension):
            #    print('Found uppercase extension on : ' + file_name + file_ext)

            if not os.path.isdir(file_name + file_ext):
            #found_extension = str.lower(filepath.rsplit('.', 1)[-1])  # Splits out the extension
                #print(file_name + filepath)
                if os.path.isfile(file_name + file_ext):
                    #print(file_name + file_ext)
                    if str.lower(file_ext).strip('.') == str.lower(extension):
                        found_files.append(file_name + file_ext)
                else:
                    #with open(f'logs/backup_{helper.getDateTimeFromTimestamp(time(), "local")}.notfound', 'a') as file_backup_exeption:
                    #    try:
                    #        file_backup_exeption.write(f'Not valid filepath: {filepath}')
                    #    except:
                    #        print(f'Error: Could not write to log file')
                    if os.path.islink(file_name + file_ext):
                        file_error = 'link'
                    else:
                        file_error = 'unknown'

                    if not verbose == None:
                        print(f'{bcolors.FAIL + "File error" + bcolors.ENDC}: ({bcolors.WARNING + file_error + bcolors.ENDC}) {file_name + file_ext}')
        return found_files



    def getFilesByType(extensions, filepath_index):
        found_files = set()

        for filepath in filepath_index:
            if (os.path.isfile(filepath) and os.access(filepath, os.R_OK)):
                with open(filepath, 'rb') as file:
                    info = fleep.get(file.read(128))
                    for extension in extensions:
                        #print (extension)
                        if(info.extension_matches(extension)):
                            found_files.add(filepath)

        return found_files


####
