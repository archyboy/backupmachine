import subprocess
import os
import io
import sys
import locale
import system

class Rsync:

    def backup(source, destination, options, more_options, fh_rsyncfile):
        os.chdir(destination)
        
        #locale.setlocale(locale.LC_ALL, 'utf8')
        args = ["rsync", options, more_options, source, destination]

        #with open(os.devnull, "w") as f:
        #    subprocess.call(args, stdout=f) #If want to report to devnull for not get memory full errors if not writing to file
        with open(fh_rsyncfile, "a") as f:
            system.call(f'cd {destination}')
            subprocess.call(args, stdout=f)

        #delimiter = [" "]
        #args = [" -av "] + source + delimiter + destination
        #with Popen("rsync -av --log-file=rsync.log --progress /home/archy/Test /home/archy/Development/Python/test/backup/", stdout=PIPE) as p:
        #with Popen("rsync", args, stdout=PIPE) as p:
        #        try:
        #            return p.wait(timeout=None)
        #        except:
        #            p.kill()
        #            p.wait()
