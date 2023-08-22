# Console output class for webpage
import os

LOGFILE = os.path.join(os.path.dirname(__file__), '../temp.log')

class Log:
    def write(data):
        with open(LOGFILE, 'a') as log:
            log.write(data + '\n')

    def output():
        if os.path.exists(LOGFILE):
            with open(LOGFILE, 'r') as log:
                return ''.join(log.readlines())
        else: # Error case
            return ''

    def clear():
        if os.path.exists(LOGFILE):
            os.remove(LOGFILE)