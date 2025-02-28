# Example execute command:  python main.py pdf /home/archy/ /home/archy/Temp/ True
#                           Interpreter script source_dir destination_dir Verbose=True|False


#  ====================== System wide imports  ======================
import os
import fleep
import time
import subprocess
import sys
import locale
import json
# ===================================================================================================================



#  ====================== Helper imports  ======================
#import scrapbook
# ===================================================================================================================



#  ====================== Apps own imports  ======================
from classes.mounter import Mounter as mounter
from classes.rsync import Rsync as rsync
from classes.progress import Progress as progressbar
from classes.filefinder import FileFinder as filefinder
from classes.helper import Helper as helper
#from modules.colorize import textColors as bcolors
import modules.colorize as bcolors
# ===================================================================================================================


# ====================== Div 3rd party libraries======================
import psutil
from pyudev import *
import udiskie
import pyTree
import copyfile
from pretty_json import format_json
import hashlib
import uuid
# ===================================================================================================================

dir(filefinder)
#exit()

# ===================== Verbose and debugging ===================================
verbose = None
# ===================================================================




#  ====================== Clearing the console ======================
subprocess.call("clear")
# ===================================================================================================================



#  ====================== Time, dates and locales  ======================
timestamp = time.time()
print(f'\nTime (localtime): {helper.getDateTimeFromTimestamp(timestamp, "local")}')
print(f'System locale: {locale.getlocale()}\n\n')
# ======================================================================================================================



# ======================= sys.argv stuff ==============================

arg_list = []

for i, value in enumerate(sys.argv):
    if i == 0:
        script = sys.argv[0]
    if i == 1:
        extension = sys.argv[1]
    if i == 2:
        backup_source = sys.argv[2]
    if i == 3:
        backup_destination = sys.argv[3]
    if i == 4:
        verbose = sys.argv[4]

print(f'Script: ' + bcolors.OKBLUE + script + bcolors.ENDC)
print(f'Extension: ' + bcolors.OKBLUE + extension + bcolors.ENDC)
print(f'Backup source: ' + bcolors.OKBLUE + backup_source + bcolors.ENDC)
print(f'Backup destination: ' + bcolors.OKBLUE + backup_destination + bcolors.ENDC)
print(f'Verbose:' + bcolors.OKBLUE + verbose + bcolors.ENDC)
# =====================================================================


#  ====================== What extension to scan for  ======================
#extension = "jpg"
#extensions = {".jpg",".gif",".png"}
#extensions = {".jpg",".jpeg"}
#extensions = {".ods", ".pdf"}
# =====================================================================================================================



#  ====================== Database files  ======================
db_dir = os.path.realpath('dbs') + '/'
db_file = db_dir + 'media-terra.db'
# ==============================================================



#  ====================== Backup source and destination variables  ======================
if not backup_source:
    backup_source = '/storage/terra/'
    #backup_destination = '/storage/terra/backupmachinedump/'
    #backup_destination = '/run/user/1000/gvfs/sftp:host=192.168.10.113,user=archy/home/archy/Backup/BackupMachine/'
    #backup_destination = '/home/archy/Backup/BackupMachineDump2/'
    #backup_destination = '/home/archy/Backup/BackupMachineDump/'/run/media/archy/Seagate Backup Plus Drive/backupmachinedump
if not backup_destination:
    backup_destination = '/run/media/archy/Seagate Backup Plus Drive/backupmachinedump/'
# ===================================================================================================================



#  ====================== Backup log files and error  ======================
backup_log_time = helper.getDateTimeFromTimestamp(timestamp, "local")
backup_log_dir = os.path.realpath('logs') + '/'

os.mkdir(f'{backup_log_dir}{backup_log_time}') # Making unique directory for log files

backup_log_file = f'{backup_log_dir}{backup_log_time}/log.txt'
backup_rsync_file = f'{backup_log_dir}{backup_log_time}/rsync.txt'
backup_error_file = f'{backup_log_dir}{backup_log_time}/error.json'
backup_exists_file = f'{backup_log_dir}{backup_log_time}/exists.json'
backup_list_file = f'{backup_log_dir}{backup_log_time}/list.json'
backup_verify_file = f'{backup_log_dir}{backup_log_time}/verify.json'
# ===================================================================================================================



#  ====================== Rsync options default "-avR" -R for relative filepath (with directories)  ======================
rsync_options = "-Pz"
#rsync_options = "-urptgoh"
#rsync_more_options = "--no-perms"
rsync_more_options = ""
# ===================================================================================================================



#  ====================== Creating and or updating the filedatabase (updatedb)  ======================
# updatedb -l 0 -o db_file -U source_directory

updatedb_args = ['updatedb','-o dbs/media-storage.db','-U/run/media/archy/Storage_HDD']

start = time.time()
print('Updating files.db')
print(bcolors.WARNING, end='')
filefinder.updateDB(updatedb_args)
print(bcolors.ENDC, end='')
print(bcolors.OKGREEN + f'Updated file database in {time.time()-start} seconds' + bcolors.ENDC)

# ===================================================================================================================



# =================== Getting index of all file path's found in scan with (mlocate) =================================
start = time.time()
print('\n')
print(bcolors.OKBLUE + 'Building file index')
filepath_index = filefinder.getFileIndex(db_file)
print(f'Using database file: {db_file}')
print(bcolors.OKGREEN + f'Added {len(filepath_index)} records from "{backup_source} and sub-folders" in {time.time()-start} seconds' + bcolors.ENDC)
# ===================================================================================================================



#  ====================== Doing a quick search in file index from mlocate for given .ext(ension(s))  ======================
if extension == None:
    print(f'What extension will you search for? (Ex. "jpg", "pdf", "doc" etc.)')
    extension = input(f'.:')
print(f'You are searching for files with extensions: {extension}')

start = time.time()
print('Quick search for files with', extension, 'extension(s) in indexed filelist......')

found_files_quick = filefinder.getFilesByExtension(extension, filepath_index)

print("Found", len(found_files_quick), "files with", extension, "extension(s) in",
      time.time()-start, "seconds in", backup_source, "and sub-folders")

print("")
# ========================================================================================================================



#  ====================== Deep scanning in binary mode of all files in file index for given .ext(ension(s)) (3rdparty module Fleep)  ======================
found_files_deep = ""

print("Would you like me to perform a deep scan on the system for given file-types / extension??")
answer = input("(y/N):")
if (answer == "y" or answer == "Y"):
    start = time.time()

    print()

    print("Deep scanning for files with", extensions,
          "extension(s) in binary mode.....This can take a long time!")
    found_files_deep = filefinder.getFilesByType(extension, filepath_index)
    print("Found", len(found_files_deep), "files in",
          time.time()-start, "seconds in", backup_source)
else:
    print("Ok got it. No deep scanning...")

print("")
# ========================================================================================================================================



#  ====================== Checks if deep scan found more files than quickscan and ask what files you want to show.  ======================
if(len(found_files_quick) or len(found_files_deep)):
    print(f'Would you like to list all files found?', end='')
    if(found_files_deep):
        print(f' Or (x) if just want to list the extra files from deep scan')
        answer = input("(Y/n/x):")
    else:
        answer = input("(Y/n):")
    if (answer == "y" or answer == "Y" or answer == ""):
        for index, filepath in enumerate(found_files_quick):
            print(f'{index} : {filepath}')
    if (found_files_deep and answer == "x" or answer == "X" and found_files_deep):
        differences = set()
        for filepath in found_files_deep:
            if (filepath not in found_files_quick):
                differences.add(filepath)
                print(filepath)
    else:
        if (len(found_files_deep) > len(found_files_quick)):
            print("")
            print("Deep scan found", len(found_files_deep) - len(found_files_quick),
                  "more files than quick search. Would you like to list the extra files?")
            answer = input("(Y/n):")

            print("")

            if (answer == "y" or answer == ""):
                differences = set()
                for filepath in found_files_deep:
                    if (filepath not in found_files_quick):
                        differences.add(filepath)
                        print(filepath)
            else:
                print("Ok.. So you are not interested in the differences..hmmm")
        else:
            print("Finaly! Where done with deep scanning!")
else:
    print("Sorry..I didnt find any files for you this time :( Tips: Try with another extension")

print("")
# ======================================================================================================



#  ====================== Backing up your storage media using your configuration  ======================
print('Would you like to backup all files found in', backup_source, '?')
answer = input("(Y/n):")
if (answer == "y" or answer == "Y" or answer == ""):
    print(f'Starting backup of files ({backup_source} --> : "{backup_destination})"')
    start = time.time()

    # absolute_file_list = set(list(found_files_quick) + list(found_files_deep)) # Joins quickscan and deepscan result
    found_files_quick = set(found_files_quick)
    # print(found_files_quick)
    absolute_file_list = found_files_quick.union(
        found_files_deep)  # Joins quickscan and deepscan result
    # print(absolute_file_list)

    #print (backup_log_text)
    #print (backup_log_file)

    #  ====================== Creating logfiles and error files object for writing  ======================

    fh_logfile = open(backup_log_file, "a")
    fh_existsfile = open(backup_exists_file, "a")
    fh_rsyncfile = open(backup_rsync_file, "a")
    fh_errorfile = open(backup_error_file, "a")
    fh_verifyfile = open(backup_verify_file, "a")
    # ====================================================================================================

    backup_log_text_start = f' *** Started backup at ( {helper.getDateTimeFromTimestamp(time.time(), "local")} ) *** \n\n'
    fh_logfile.write(backup_log_text_start)
    total_synced = []
    total_exists = []

    errors = []
    exists = []

    print(backup_destination + extension)

    if not (os.path.exists(backup_destination + extension)):
        if os.mkdir(backup_destination + extension):
            print('Failed create extension directory')
        else:
            print(extension + ' directory created')


    for index, filepath in enumerate(absolute_file_list):

        if os.path.isfile(filepath): # If source is a file
            # print(filepath)
            fh_logfile.write(f'{filepath}\n')

            # Starting backup progress
            #rsync.backup(filepath, backup_destination, rsync_options, rsync_more_options, backup_rsync_file)
            if not os.path.exists(backup_destination + extension + "/" + os.path.basename(filepath)): # Check if file not exists in destination directory from before
                #print("Verfify: " + backup_destination + os.path.basename(filepath))
                copyfile.copyFile(filepath, backup_destination + extension + '/')
                total_synced.append(filepath)
                print(f'{index} : {filepath}')

            else:
                total_exists.append(filepath)
                exists.append(['file_exist', filepath])
                #print('File already exist in directory')

            progressbar.printBar(index + 1, len(absolute_file_list), prefix=bcolors.OKBLUE + 'Progress:' + bcolors.WARNING, suffix=bcolors.OKBLUE + 'Complete' + bcolors.ENDC, length=50)
            # time.sleep(0.05) # NOT to use in production
        else:
            fh_errorfile.write(f'File read error: "{filepath}" on index [{index}] Maybe it is a invalid filepath or an directory\n')

    if len(exists):
        fh_existsfile.write(json.dumps(exists))
        fh_existsfile.close()

        #fh_existsfile.write('[')
        #for line in exists:
        #    fh_existsfile.write(str(line) +',\n')
        #fh_existsfile.write(']')

    print("")
    print(f'Backup complete! You syncronized {len(total_synced)} files out of {len(absolute_file_list)}')
    if (len(total_exists)):
        print(f'{len(total_exists)} exist at destination from before')

    backup_log_text_finish = f'\n*** Finished backup at ( {helper.getDateTimeFromTimestamp(time.time(), "local")} ) *** \n'
    fh_logfile.write(backup_log_text_finish)
    fh_logfile.close()
    fh_errorfile.close()
    end = time.time()-start
    print("Backup took", end, "seconds (", end/60, "minutes)")

else:
    print("Got it!! No backups done")
# =============================================================================================================

print('Would you like to load the JSON exists log file?')
if input('Y/n.: ') == 'y' or 'Y' or '':
    with open(backup_exists_file, "r") as fh_read_exist:
        try:
            exists_data = json.load(fh_read_exist)
            fh_read_exist.close()
            print (format_json(exists_data))
        except json.decoder.JSONDecodeError:
            print('Could not load JSON data')

    # format_json(content, style=OUTPUT_STYLE)


else:
    print("We're all done!!")


    #print(exists_data)
