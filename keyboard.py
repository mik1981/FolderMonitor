#!/usr/bin/env python
'''
A Python class implementing KBHIT, the standard keyboard-interrupt poller.
Works transparently on Windows and Posix (Linux, Mac OS X).  Doesn't work
with IDLE.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

'''

import os
import logging


LOG_NAME    =   "keyboard"


# Windows
if os.name == 'nt':
    import msvcrt

# Posix (Linux, OS X)
else:
    import sys
    import termios
    import atexit
    from select import select


class KBHit:

    def __init__(self):
        '''Creates a KBHit object that you can call to do various keyboard things.
        '''

        if os.name == 'nt':
            pass

        else:

            # Save the terminal settings
            self.fd = sys.stdin.fileno()
            self.new_term = termios.tcgetattr(self.fd)
            self.old_term = termios.tcgetattr(self.fd)

            # New terminal setting unbuffered
            self.new_term[3] = (self.new_term[3] & ~termios.ICANON & ~termios.ECHO)
            termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.new_term)

            # Support normal-terminal reset at exit
            atexit.register(self.set_normal_term)


    def set_normal_term(self):
        ''' Resets to normal terminal.  On Windows this is a no-op.
        '''

        if os.name == 'nt':
            pass

        else:
            termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.old_term)


    def empty( self ):
        while self.kbhit ():        self.getch  ()


    def getch(self):
        ''' Returns a keyboard character after kbhit() has been called.
            Should not be called in the same program as getarrow().
        '''

        s = ''

        if os.name == 'nt':
            log     =   logging.getLogger   ( LOG_NAME )
            c1      =   msvcrt.getch        ()
            sc      =   False                               #   sc = special char
            arrow   =   False
            #
            if c1  ==  b'\x00':
                c1      =   msvcrt.getch        ()
                sc      =   True

            elif c1  ==  b'\xE0':
                c1      =   msvcrt.getch        ()
                arrow   =   True

            try:
                c2          =   c1.decode   ( 'utf-8' )
                #log.debug   ( f"getch-{c1=}, {c2=}" )
                if sc:
                    match   c2:
                        case    ';':    return  "F1"
                        case    '<':    return  "F2"
                        case    '=':    return  "F3"
                        case    '>':    return  "F4"
                        case    _:      log.warning     ( f"special char -> getch-{c1=}, {c2=}" )

                elif arrow:
                    match   c2:
                        case    'H':    return  "UP"
                        case    'K':    return  "LEFT"
                        case    'P':    return  "DOWN"
                        case    'M':    return  "RIGHT"
                        case    _:      log.warning     ( f"arrow char -> getch-{c1=}, {c2=}" )

                else:
                    match   c2:
                        case    '\x1B': return  "ESC"
                        case    '\x0D': return  "ENTER"
                        case    '\x08': return  "BS"
                        case    _:      log.warning     ( f"normal char -> getch-{c1=}, {c2=}" )

                if  ( c2 >= 'a'  and  c2 <= 'z' )       or  \
                    ( c2 >= 'A'  and  c2 <= 'Z' )       or  \
                    ( c2 >= '0'  and  c2 <= '9' ):
                    return      c2
                else:
                    return      ""

            except Exception as err:
                log.error   ( f"getch-{c1=}\n{err}" )
                return      None

        else:
            return sys.stdin.read(1)


    def getarrow(self):
        ''' Returns an arrow-key code after kbhit() has been called. Codes are
        0 : up
        1 : right
        2 : down
        3 : left
        Should not be called in the same program as getch().
        '''

        if os.name == 'nt':
            msvcrt.getch() # skip 0xE0
            c = msvcrt.getch()
            log                 =   logging.getLogger   ( LOG_NAME )
            log.debug(f"getarrow {c=}")
            vals = [72, 77, 80, 75]

        else:
            c = sys.stdin.read(3)[2]
            vals = [65, 67, 66, 68]

        return vals.index(ord(c.decode('utf-8')))


    def kbhit(self):
        ''' Returns True if keyboard character was hit, False otherwise.
        '''
        if os.name == 'nt':
            return msvcrt.kbhit()

        else:
            dr,dw,de = select([sys.stdin], [], [], 0)
            return dr != []


    def flush( self ):
        while self.kbhit():
            self.getch  ()


# Test
# if __name__ == "__main__":
#
#     kb = KBHit()
#
#     print('Hit any key, or ESC to exit')
#
#     while True:
#
#         if kb.kbhit():
#             c = kb.getch()
#             if c == "ESC":
#                 break
#             print(c)
#
#     kb.set_normal_term()
