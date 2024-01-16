import  time,  os,  pickle
from    wrap_rich       import  *
from    keyboard        import  *
from    utility         import  timer
from    rich.progress   import  Progress


SCRIPT_VERSION  =   "1"
SCRIPT_DATE     =   "15/1/2024 15:07"
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
                            default     =   '.'
                        )
    parser.add_argument (   '-i',   '--interval',
                            help = "specifica ogni quanto effettuare la verifica",
                            metavar = "seconds",
                            default     =   1
                        )
    args                =   vars    ( parser.parse_args () )
    #
    if g[ 'rp' ].isConsoleMode():       g[ 'rp' ].printDbg      ( f"{args=}" )
    #
    return              args




class currSt():
    FILE_NAME   =   "context.fm"

    def __init__( self,  path,  rp=None ):
        self.prec   =   []
        self.curr   =   []
        self.add    =   []
        self.remove =   []
        self.path   =   path
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

        else:
            if len( self.add ) > 0:
                cnt         =   0
                self.rp.printS  ( "[bold white]Aggiunto",  style="blue" )
                for rec  in  self.add:
                    self.rp.print   ( f"{cnt+1}- [white on blue]{self.add [ cnt ] [ 'file' ]}[/white on blue]\t{self.add [ cnt ] [ 'dir' ]}" )
                    cnt             +=  1
            #
            if len( self.remove ) > 0:
                cnt         =   0
                self.rp.printS  ( "[bold white]Rimosso",  style="yellow" )
                for rec  in  self.remove:
                    self.rp.print   ( f"{cnt+1}- [white on yellow]{self.remove [ cnt ] [ 'file' ]}[/white on yellow]\t{self.remove [ cnt ] [ 'dir' ]}" )
                    cnt             +=  1

    def close( self ):
        # open a file, where you ant to store the data
        file        =   open ( self.path + '\\' + self.FILE_NAME,  'wb' )
        # dump information to that file
        pickle.dump ( self.curr,  file )
        # close the file
        file.close  ()


def fm_init():
    global  g

    g[ 'cs' ]       =   currSt  ( g[ 'args' ] [ 'directory' ] )



def main_loop():
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
                    task        =   progress.add_task   ( f"[white]Attesa prossima verifica ('u' forza aggiornamento db)...",  total=secs )
                    while secs  >  0:
                        if g[ 'kb' ].kbhit ():
                            if g[ 'kb' ].getch ()  !=  'u':
                                uscita  =   True
                            secs    =   0
                        else:
                            progress.update ( task,  advance=1.0 )
                            time.sleep  ( 1 )
                            secs        -=  1

            elif g[ 'kb' ].kbhit ():
                uscita  =   True
                secs    =   0

            else:
                time.sleep  ( 1 )
                secs        -=  1


if __name__  ==  "__main__":
    g               =   {}
    g[ 'kb' ]       =   KBHit       ()
    g[ 'rp' ]       =   richPrint   ()
    g[ 'rp' ].printS( f"{SCRIPT_TITLE}" )
    g[ 'args' ]     =   init_args   ()
    g[ 'rp' ].run   ( main_loop )
    g[ 'cs' ].close ()
    g[ 'rp' ].print ( "Programma terminato" )
