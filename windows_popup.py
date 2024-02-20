#from    win11toast  import  toast
from    win11toast  import  notify
# import  time
# import  logging


LOG_NAME    =   "winPopup"


class WindowsBalloonTip:
    def __init__( self,  title=None,  msg=None ):
        if title != None  and  msg != None:
            notify      ( title,  msg )


    def show( self,  title,  msg ):
        notify      ( title,  msg )


def balloon_tip( title,  msg ):
    w   =   WindowsBalloonTip   ( title,  msg )


if __name__ == '__main__':
    balloon_tip ( "test",  "OK" )
