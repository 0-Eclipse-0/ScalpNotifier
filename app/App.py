from multiprocessing import Process
import tornado
import configparser
import os
from Scalpnotifier import Scalpnotifier
from tornado.ioloop import IOLoop
import tornado.web
from tornado import concurrent
from Log import Log
from GUI import startGUI
from Notification import Notification

executor = concurrent.futures.ThreadPoolExecutor(8)

def cleanInput(arguments):
    isValid = True
    for boolean in ["beautifiedEmailMode", "freeItemMode", "falsePricePrevention"]:
        if boolean not in arguments.keys():
            arguments[boolean] = False
        else:
            arguments[boolean] = True

    # Convert bytes to str
    for arg in arguments.keys():
        if isinstance(arguments[arg], list):
            arguments[arg] = f'{arguments[arg][0].decode()}'

    # Validate email login
    try:
        login = Notification(arguments['sendingEmail'], arguments['targetEmail'], arguments['sendingEmailPass'])
        login.testLogin()
    except:
        isValid = False

    return arguments, isValid

# Read config to update params
class Config():
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.optionxform = str
        self.config.read(os.path.join(os.path.dirname(__file__), '../config.ini'))

    def modify(self, data):
        # Modify config object
        for item in data:
            self.config.set('DEFAULT', item, str(data[item]))

        # Write to config file
        with open('config.ini', 'w') as f:
            self.config.write(f)

    def read(self):
        return dict(self.config.items('DEFAULT')) # tuple -> dict

class ControlPanelHandler(tornado.web.RequestHandler):
    def initialize(self, process):
        self.config = Config()
        self.process = process

    def get(self):
        # Fill page with predefined config
        self.render('../public/gui_template.html',
                    values=self.config.read(),
                    log=Log.output(),
                    isRunning=self.process['isRunning'])

    def post(self):
        if self.process['isRunning'] == True:
                # Reset values
                if self.process['curProcess'] != None:
                    self.process['curProcess'].terminate()

                self.process['curProcess'] = None
                self.process['scalper'] = None
                self.process['isRunning'] = False

                Log.clear()

        else:
            # Include disables switches in arguments and convert to booleans
            arguments, validity = cleanInput(self.request.arguments)

            if (validity):
                self.config.modify(arguments)
                configArgs = self.config.read()
                self.process["scalper"] = Scalpnotifier(configArgs['locationList'], # Creat new scalper object based on args
                        configArgs['itemList'],
                        configArgs['sendInterval'],
                        configArgs['freeItemMode'],
                        configArgs['beautifiedEmailMode'],
                        configArgs['targetEmail'],
                        configArgs['sendingEmail'],
                        configArgs['sendingEmailPass'])

            # Send scalper to background and go to console page
                self.process['curProcess'] = Process(target=self.process['scalper'].run)
                self.process['curProcess'].start()

            else:
                Log.write("Email login failed. Please kill process...")

            self.process['isRunning'] = True

        self.redirect('/')

def makeApp():
    # Struct-like dict for handling global objects and variables
    process = {
        "scalper": None,
        "curProcess": None,
        "isRunning": False
    }

    return tornado.web.Application([
        (r"/", ControlPanelHandler, {'process': process})
    ])

if __name__ == '__main__':
    try:
        startGUI()
        app = makeApp()
        app.listen(80)
        IOLoop.current().start()
    except KeyboardInterrupt:
        Log.clear()