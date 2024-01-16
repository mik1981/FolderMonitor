Folder monitoring from the command line to track all added and removed files in the specified folder and its subfolders

usage: FolderMonitor.py [-h] [-d pathname] [-i seconds]

Folder Monitor ver.1 (15/1/2024 15:07)

options:
  -h, --help            show this help message and exit
  -d pathname, --directory pathname
                        specifica il percorso da monitorare
  -i seconds, --interval seconds
                        specifica ogni quanto effettuare la verifica


For example, to monitor the c:\test folder for any changes every 2 minutes type from cli:

FolderMonitor.exe -d c:\test -i 120

By default the application identifies the current folder with a 1 second pause between checks.
The program automatically saves a configuration file, at the position indicated with the -d parameter, the context.fm file containing the list of files present when the program is closed.
To exit the program, press any key.
If the database update is in progress it is necessary to wait for the end before the program exit is actually executed