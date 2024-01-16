
import  logging
import  traceback,  sys
import  time

from    math        import  trunc
from    rich        import  pretty              #   una volta installato, definisce un output colorato di default
from    rich        import  print
from    datetime    import  datetime



LOG_NAME    =   "utility"


def getStrTimeElapsed( timeSec ):
    if timeSec  <  60:
        return  f"{ round ( timeSec ) }s"

    elif timeSec  <  60*60:
        min     =   trunc ( timeSec/60 )
        sec     =   timeSec  -  min * 60
        return  f"{ min }m { trunc ( sec ) }s"

    else:
        return  f"{ round ( timeSec / 60 ) }m"

    return  "--"



def logException( msg = None ):
    log         =   logging.getLogger   ( LOG_NAME )
    #
    if msg == None:
        log.exception   ( "general error" )
    else:
        log.exception   ( msg )
        print           ( f"{traceback.format_exc()}\\{sys.exc_info()[2]}" )


class timer():
    def __init__( self ):
        self.update ()

    def update( self ):
        self.start  =   datetime.now ().timestamp ()

    def elapsedAtLeast( self,  deltaSec ):
        self.lastDeltaSecs  =   datetime.now ().timestamp ()  -  self.start
        #
        if self.lastDeltaSecs  >  deltaSec:
            return      True
        else:
            return      False

    def getDeltaTime( self ):
        self.lastDeltaSecs  =   datetime.now ().timestamp ()  -  self.start
        return              self.lastDeltaSecs

    def strStart( self ):
        return      datetime.fromtimestamp  ( self.start ).strftime ( "%a %d/%m/%Y %H:%M:%S" )

    def __str__( self ):
        return      f"{ round (  self.getDeltaTime ()  ) }s"




if __name__  ==  "__main__":
    import  argparse

    parser              =   argparse.ArgumentParser ()
    parser.add_argument (   'com',  nargs=1,  help = 'numero com' )
    args                =   vars    ( parser.parse_args () )
    #pretty.install  ()
    #
    test                =   port    ( "COM" + args [ 'com' ][0] )
    if test.conn ():
        #test.sio.write ( "N\x0D" )
        #test.sio.flush()
        recv    =   test.sio.read ()
        print   ( f"{recv=}" )
    else:
        print   ( "impossibile connettere la com" )

