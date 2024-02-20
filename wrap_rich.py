from    rich            import  pretty
from    rich            import  inspect
from    rich.color      import  Color
from    rich.console    import  Console
from    rich.logging    import  RichHandler


import  logging,  traceback,  sys

#   python -m rich.status
#   python -m rich.spinner


class richPrint:
    def __init__( self,  modeConsole=0,  debugLevel=3 ):
        self.console        =   Console ()
        self.debugLevel     =   debugLevel
        self.mode           =   modeConsole #   0:  shell, no log
                                            #   1:  console, no log
                                            #   2:  graph mode, no log
                                            #   3:  graph, log
        pretty.install      ()
        #
        LEVEL           =   logging.DEBUG
        FORMAT          =   "%(message)s"
        #
        match debugLevel:
            case    0:
                log             =   logging.getLogger   ( "main" )
                return

            case    1:  LEVEL   =   logging.CRITICAL
            case    2:  LEVEL   =   logging.ERROR
            case    3:  LEVEL   =   logging.WARNING
            case    4:  LEVEL   =   logging.INFO
            case    5:  LEVEL   =   logging.DEBUG
            case    _:  LEVEL   =   "NOTSET"
        #
        if self.mode == 3:
            logging.basicConfig (   handlers    =   [ RotatingFileHandler ( filename,  maxBytes = maxSize,  backupCount = backups ) ],
                                    level       =   LEVEL,
                                    format      =   '[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s',
                                    datefmt     =   '%Y-%m-%dT%H:%M:%S'
                                )

        elif self.mode == 0  or  self.mode == 1:
            logging.basicConfig (   level       =   LEVEL,
                                    datefmt     =   "[%X]",
                                    format      =   FORMAT,
                                    handlers    =   [ RichHandler ( rich_tracebacks = True ) ]
                                )
#             install             ( show_locals = True )
        #
        self.console.clear  ()              #   cancella lo schermo


    def inspectObj( self, obj,  full=False ):       inspect             ( obj,  methods=full )

    def setDebugLevel( self,  debugLevel ):
        if  self.debugLevel  !=  debugLevel:
            log             =   logging.getLogger   ()
            self.debugLevel =   debugLevel
            match debugLevel:
                case    0:  LEVEL   =   logging.CRITICAL
                case    1:  LEVEL   =   logging.CRITICAL
                case    2:  LEVEL   =   logging.ERROR
                case    3:  LEVEL   =   logging.WARNING
                case    4:  LEVEL   =   logging.INFO
                case    5:  LEVEL   =   logging.DEBUG
                case    _:  LEVEL   =   "NOTSET"
            log.setLevel    ( LEVEL )


    def isConsoleMode( self ):
        if self.mode < 2:   return  True
        else:               return  False


    def print( self, *args, **kwargs ):
        match self.mode:
            case    0:      self.console.print  ( *args, **kwargs )
            case    1:      self.console.log    ( *args, **kwargs )
            case    other:  pass

    def printCrit( self, *args, **kwargs ):
        log.critical    ( *args, **kwargs )
        self.print      ( *args, **kwargs )

    def printDbg( self, *args, **kwargs ):
        log             =   logging.getLogger   ( "main" )
        log.debug       ( *args, **kwargs )
        self.print      ( *args, **kwargs )

    def printInf( self, *args, **kwargs ):
        log             =   logging.getLogger   ( "main" )
        log.info        ( *args, **kwargs )
        self.print      ( *args, **kwargs )



    def printF( self, msg=None,  pf=None,  spinner="dots" ):
        if msg != None  and  pf != None:
            if spinner == None:
                with self.console.status ( msg ):
                    pf  ()
            else:
                with self.console.status ( msg,  spinner=spinner ):
                    pf  ()

    #   print section divider
    def printS( self, msg,  style='rule.line',  align='center' ):
        self.console.rule   ( "[bold white]" + msg,  style=style,  align=align )


    def printE( self, obj=None ):
        self.console.rule   ( "[bold red]Expection with error" )
#         if obj != None:


    def run( self,  function ):
        try:
            return  function    ()

        except Exception as err:
            #inspect     ( main,  methods=True )
            #log                         =   logging.getLogger   ( "main" )
            #log.exception               ( "general error" )
            #self.print                  ( f"{traceback.format_exc()}\{sys.exc_info()[2]}" )
            self.console.rule           ( "[bold red]Errore generale non intercettato" )
            self.console.print_exception( show_locals = True )
            sys.exit                    ( 1 )
