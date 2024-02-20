import  time,  os,  pickle

from    wrap_rich       import  richPrint
from    keyboard        import  KBHit
from    utility         import  timer
from    datetime        import  datetime
from    windows_popup   import  WindowsBalloonTip
from    rich.progress   import  Progress
from    rich.table      import  Table
from    rich.text       import  Text
from    rich.style      import  Style



SCRIPT_VERSION  =   "2"
SCRIPT_DATE     =   "20/2/2024 14:58"
SCRIPT_TITLE    =   "Folder Monitor ver." + SCRIPT_VERSION + " (" + SCRIPT_DATE + ")"
# PROJECT         =   "L439"
# CONFIG_FILE_DEF =   "S1L439_config.ini"


def init_args():
    import  argparse
    global  g

    parser              =   argparse.ArgumentParser ( description = SCRIPT_TITLE )
    #
    parser.add_argument (   '-d',   '--directory',
                            help = "specifica il percorso da monitorare",
                            metavar = "pathname",
                            default     =   os.getcwd   ()
                        )
    parser.add_argument (   '-i',   '--interval',
                            help = "specifica ogni quanto effettuare la verifica",
                            metavar = "seconds",
                            default     =   1
                        )
    parser.add_argument (   '-c',   '--config',
                            help = "specifica un file da cui caricare la configurazione di cosa monitorare",
                            default     =   None
                        )
    parser.add_argument (   '--debug',
                            help = "specifica il livello di debug (0-4)",
                            type=int,  default     =   0
                        )
    args                =   vars    ( parser.parse_args () )
    #
    args [ 'directory' ]    =   os.path.abspath     ( args [ 'directory' ] )
    #
    if g[ 'rp' ].isConsoleMode():       g[ 'rp' ].printDbg      ( f"{args=}" )
    #
    return              args


# def init_config():
#     from    configparser        import  ConfigParser,  ExtendedInterpolation
#     global  g
#
#     if g[ 'config' ]  ==  None:
#         #   costruzione manuale del default del file config
#         config [ 'mask' ]
#
#     else:
#         config          =   ConfigParser    ( interpolation = None )#ExtendedInterpolation () )
#         config.read     ( configFile )
#     #
#     return          config




class currSt():
    FILE_NAME   =   "context.fm"

    def __init__( self,  path,  rp=None ):
        self.prec   =   []
        self.curr   =   []
        self.add    =   []
        self.remove =   []
        self.path   =   path
        self.wpu    =   WindowsBalloonTip   ()      #   windows popup
        #
        if rp == None:      self.rp     =   richPrint   ()
        else:               self.rp     =   rp
        #
        if os.path.isfile ( self.path + '\\' + self.FILE_NAME ):
            file            =   open        ( self.path + '\\' + self.FILE_NAME,  'rb' )
            # dump information to that file
            self.curr       =   pickle.load ( file )
            # close the file
            file.close      ()
            #
            self.numEls     =   len ( self.curr )
            self.rp.print   ( f"Caricati {self.numEls} files da {self.path}\\{self.FILE_NAME}" )

        else:
            self.driveScan  ()


    def driveScan( self ):
        self.curr   =   []
#         self.add    =   []
#         self.remove =   []
        #   scansione disco
        for root, dirs, files  in  os.walk ( self.path ):
            #             rp.print(f"Ci troviamo nella cartella: '{root=}'")
            #             rp.print(f"Le sottocartelle presenti sono: '{dirs=}'")
            #             rp.print(f"I files presenti sono: {files=}")
            #             rp.print()
            for file in files:
                record              =   { 'file': file,  'dir': root }
                self.curr.append    ( record )
        #
        self.numEls =   len ( self.curr )

    def update( self ):
        self.add            =   []
        self.remove         =   []
        old                 =   self.curr
        self.rp.printF      ( "Aggiornamento database...",  self.driveScan () )
        sizeOld             =   len ( old )
        sizeNew             =   len ( self.curr )
#         self.add        =   self.curr  -  old
#         self.remove     =   old  -  self.curr
        for rec in self.curr:
            idx     =   0
            uscita  =   False
            while idx  <  sizeOld  and  not uscita:
                if  rec [ 'file' ]   ==  old [ idx ] [ 'file' ]  and    rec [ 'dir' ]    ==  old [ idx ] [ 'dir' ]:
                    #   file gia' presente
                    uscita      =   True
                #
                idx     +=  1
            #
            if not uscita:
                self.add.append ( rec )
        #
        for rec in old:
            idx     =   0
            uscita  =   False
            while idx  <  sizeNew  and  not uscita:
                if  rec [ 'file' ]   ==  self.curr [ idx ] [ 'file' ]  and   rec [ 'dir' ]    ==  self.curr [ idx ] [ 'dir' ]:
                    #   file gia' presente
                    uscita      =   True
                #
                idx     +=  1
            #
            if not uscita:
                self.remove.append  ( rec )


    def printCurr( self ):
        self.rp.print   ( self.curr )
        self.rp.print   ( f"Trovati {len(self.curr)} files" )

    def printDiff( self ):
        if 0:
            if len( self.add ) > 0  or  len( self.remove ) > 0:     self.rp.printS  ( "Nuovo cambio" )
            if len( self.add ) > 0:                                 self.rp.print   ( f"{self.add=}" )
            if len( self.remove ) > 0:                              self.rp.print   ( f"{self.remove=}" )

        elif 0:
            if len( self.add ) > 0:
                cnt         =   0
                self.rp.printS  ( "[bold white]Aggiunto",  style="blue" )
                for rec  in  self.add:
                    #self.rp.print   ( f"{cnt+1}- [white on blue]{self.add [ cnt ] [ 'file' ]}[/white on blue]\t{self.add [ cnt ] [ 'dir' ]}" )
                    self.rp.console.print   (   f"{cnt+1}- [white on blue]{self.add [ cnt ] [ 'file' ]}[/white on blue]\t{self.add [ cnt ] [ 'dir' ]}",
                                                style=f"link {self.add [ cnt ] [ 'dir' ]}"
                                            )
                    cnt             +=  1
            #
            if len( self.remove ) > 0:
                cnt         =   0
                self.rp.printS  ( "[bold white]Rimosso",  style="yellow" )
                for rec  in  self.remove:
                    #self.rp.print   ( f"{cnt+1}- [white on yellow]{self.remove [ cnt ] [ 'file' ]}[/white on yellow]\t{self.remove [ cnt ] [ 'dir' ]}" )
                    self.rp.console.print   (   f"{cnt+1}- [white on yellow]{self.remove [ cnt ] [ 'file' ]}[/white on yellow]\t{self.remove [ cnt ] [ 'dir' ]}",
                                                style=f"link {self.remove [ cnt ] [ 'dir' ]}"
                                            )
                    cnt             +=  1

        else:
            #strDate         =   datetime.fromtimestamp  ( datetime.now ().timestamp () ).strftime   ( "%a %d/%m/%Y %H:%M:%S" )
            strDate         =   datetime.fromtimestamp  ( datetime.now ().timestamp () ).strftime   ( "%H:%M" )
            stylesRowTable  =   [ "none", "white on gray23" ]
            styleTitleTable =   f" [grey50]({strDate})"
            if len( self.add ) > 0:
                cnt             =   0
                lastDir         =   ""
                table           =   Table   ( title="[bold white]Aggiunto"+styleTitleTable, show_header=False, row_styles=stylesRowTable )
                table.add_column( min_width=4 )
                table.add_column( min_width=40 )
                table.add_column( min_width=60 )
                for rec  in  self.add:
                    styleDir    =   None
                    if cnt  >  0:
                        if lastDir  !=  self.add [ cnt ] [ 'dir' ]:
                            lastDir     =   self.add [ cnt ] [ 'dir' ]
                            styleDir    =   "blue1"
                    else:
                        lastDir     =   self.add [ cnt ] [ 'dir' ]

                    if self.add [ cnt ] [ 'file' ].lower().endswith ( ('.png', '.jpg', '.jpeg', '.heif', '.avif', '.tiff', '.bmp', '.ico', '.jpeg' ) ):
                        textFile        =   Text    (   f"{self.add [ cnt ] [ 'file' ]}",
                                                        style=Style ( color="black", bgcolor="green", link=f"{self.add [ cnt ] [ 'dir' ]}\\{self.add [ cnt ] [ 'file' ]}" )
                                                    )
                    elif self.add [ cnt ] [ 'file' ].lower().endswith ( ('.mp3', '.mp4', '.m4p', '.webm', '.flv', '.gif', '.gifv', '.wmv', '.avi', '.mov', '.qt' ) ):
                        textFile        =   Text    (   f"{self.add [ cnt ] [ 'file' ]}",
                                                        style=Style ( color="black", bgcolor="green3", link=f"{self.add [ cnt ] [ 'dir' ]}\\{self.add [ cnt ] [ 'file' ]}" )
                                                    )
                    else:
                        textFile        =   Text    (   f"{self.add [ cnt ] [ 'file' ]}",
                                                        style=Style ( color="blue1", link=None )
                                                    )
                    if styleDir == None:
                        textDir         =   Text    (   f"{self.add [ cnt ] [ 'dir' ]}",
                                                        style=Style ( color=None, link=f"{self.add [ cnt ] [ 'dir' ]}" )
                                                    )
                    else:
                        textDir         =   Text    (   f"{self.add [ cnt ] [ 'dir' ]}",
                                                        style=Style ( color=f"{styleDir}", link=f"{self.add [ cnt ] [ 'dir' ]}" )
                                                    )
                    cnt             +=  1
                    table.add_row   ( f"{cnt}",  textFile,  textDir )
                #
                if cnt  ==  1:      self.wpu.show           ( f"FolderMonitor: {cnt} nuovo file",  f"{self.path}" )
                else:               self.wpu.show           ( f"FolderMonitor: {cnt} nuovi file",  f"{self.path}" )
                self.rp.console.print   ( table )
            #
            if len( self.remove ) > 0:
                cnt             =   0
                table           =   Table   ( title="[bold white]Rimosso"+styleTitleTable, show_header=False, row_styles=stylesRowTable )
                table.add_column( min_width=4 )
                table.add_column( min_width=40 )
                table.add_column( min_width=60 )
                for rec  in  self.remove:
                    styleDir    =   None
                    if cnt  >  0:
                        if lastDir  !=  self.remove [ cnt ] [ 'dir' ]:
                            lastDir     =   self.remove [ cnt ] [ 'dir' ]
                            styleDir    =   "yellow2"
                    else:
                        lastDir     =   self.remove [ cnt ] [ 'dir' ]

                    textFile        =   Text    (   f"{self.remove [ cnt ] [ 'file' ]}",
                                                    style=Style ( color="yellow2", link=None )
                                                )
                    if styleDir == None:
                        textDir         =   Text    (   f"{self.remove [ cnt ] [ 'dir' ]}",
                                                        style=Style ( color=None, link=f"{self.remove [ cnt ] [ 'dir' ]}" )
                                                    )
                    else:
                        textDir         =   Text    (   f"{self.remove [ cnt ] [ 'dir' ]}",
                                                        style=Style ( color=f"{styleDir}", link=f"{self.remove [ cnt ] [ 'dir' ]}" )
                                                    )
                    table.add_row   ( f"{cnt+1}",  textFile,  textDir )
                    cnt             +=  1
                #
                self.rp.console.print   ( table )


    def close( self ):
        # open a file, where you ant to store the data
        file        =   open ( self.path + '\\' + self.FILE_NAME,  'wb' )
        # dump information to that file
        pickle.dump ( self.curr,  file )
        # close the file
        file.close  ()


def main_loop():
    def fm_init():
        global  g
        g[ 'cs' ]       =   currSt  ( g[ 'args' ] [ 'directory' ] )


    def wait1s():
        time.sleep  ( 1 )


    def mngKeyboard():
        global  g

        if g[ 'kb' ].kbhit ():
            c   =   g[ 'kb' ].getch ().upper ()
            #
            match c:
                case "ESC":     return      "uscita"
                case "U":       return      "update"
                case "C":       g[ 'rp' ].console.clear()
                case "H":
                    print       ( "u:           force update" )
                    print       ( "c:           clear console" )
                    print       ( "q or ESC:    quit program" )
        #
        return  "None"


    global  g
    #
    tm                  =   timer   ()
    g[ 'rp' ].printF    ( "Analisi attuale contenuto...",  fm_init,  "bouncingBall" )
    if tm.getDeltaTime ()  >  5:        g[ 'rp' ].print     ( f"Tempo analisi: {tm}" )
    #
    uscita      =   False
    while   not uscita:
        g[ 'rp' ].printF    ( "Aggiornamento database...",  g[ 'cs' ].update,  "shark" )
        g[ 'cs' ].printDiff ()
        #
        secs        =   int ( g[ 'args' ] [ 'interval' ] )
        #
        if secs  >  0:
            if secs  >=  5:
                with Progress( transient=True ) as progress:
                    task        =   progress.add_task   ( "[white]Attesa prossima verifica ('h' per l'help)...",  total=secs )
                    while secs  >  0:
                        scelta      =   mngKeyboard ()
                        match scelta:
                            case "uscita":
                                uscita  =   True
                                secs    =   0
                            case "update":
                                secs    =   0
                            case _:
                                progress.update ( task,  advance=1.0 )
                                secs        -=  1
                                time.sleep  ( 1 )
                        #print(f"{secs=}, {scelta=}")

            else:
                g[ 'rp' ].printF    ( "[white]'h' per l'help...",  wait1s,  spinner=None )
                #time.sleep  ( 1 )
                secs        -=  1
                scelta      =   mngKeyboard ()
                match scelta:
                    case "uscita":      uscita  =   True
                    case "update":      secs    =   0


if __name__  ==  "__main__":
    g                   =   {}
    g[ 'kb' ]           =   KBHit       ()
    g[ 'rp' ]           =   richPrint   ()
    g[ 'rp' ].printS    ( f"{SCRIPT_TITLE}" )
    g[ 'args' ]         =   init_args   ()
#     g[ 'config' ]   =   init_config ()
    g[ 'rp' ].setDebugLevel     ( g[ 'args' ] [ 'debug' ] )
    g[ 'rp' ].run       ( main_loop )
    g[ 'cs' ].close     ()
    g[ 'rp' ].printInf  ( "Programma terminato" )
