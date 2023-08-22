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

executor = concurrent.futures.ThreadPoolExecutor(8)

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
        with open('../config.ini', 'w') as f:
            self.config.write(f)


    def read(self):
        return dict(self.config.items('DEFAULT')) # tuple -> dict

class ConsoleHandler(tornado.web.RequestHandler):
    def initialize(self, process):
        self.process = process

    def get(self):
        # Determine if console has content and output it on refresh
        self.render('../public/console_template.html', log=Log.output())

    def post(self):
        # Terminate runnning instance if it exists
        if self.process['isRunning'] == True:
                # Reset values
                self.process['curProcess'].terminate()
                self.process['curProcess'] = None
                self.process['scalper'] = None
                self.process['isRunning'] = False

                Log.clear()

                print("Process terminated")

        self.redirect('/')


class ControlPanelHandler(tornado.web.RequestHandler):
    def initialize(self, process):
        self.config = Config()
        self.process = process

    def get(self):
        # Fill page with predefined config
        self.render('../public/gui_template.html', values=self.config.read())

    def post(self):
        # Include disables switches in arguments and convert to booleans
        for boolean in ["beautifiedEmailMode", "freeItemMode", "falsePricePrevention"]:
            if boolean not in self.request.arguments.keys():
                self.request.arguments[boolean] = False
            else:
                self.request.arguments[boolean] = True

        # Convert bytes to str
        for arg in self.request.arguments.keys():
            if isinstance(self.request.arguments[arg], list):
                self.request.arguments[arg] = f'{self.request.arguments[arg][0].decode()}'

        self.config.modify(self.request.arguments)
        configArgs = self.config.read()
        self.process["scalper"] = Scalpnotifier(configArgs['locationList'], # Creat new scalper object based on args
                      configArgs['itemList'],
                      configArgs['sendInterval'],
                      configArgs['freeItemMode'],
                      configArgs['falsePricePrevention'],
                      configArgs['beautifiedEmailMode'],
                      configArgs['targetEmail'],
                      configArgs['sendingEmail'],
                      configArgs['sendingEmailPass'])

        # Send scalper to background and go to console page
        # executor.submit(self.scalper.run())
        self.process['curProcess'] = Process(target=self.process['scalper'].run)
        self.process['curProcess'].start()
        self.process['isRunning'] = True
        print("Running again")

        self.redirect('/console')


def makeApp():
    # Struct-like dict for handling global objects and variables
    process = {
        "scalper": None,
        "curProcess": None,
        "isRunning": False
    }

    return tornado.web.Application([
        (r"/", ControlPanelHandler, {'process': process}),
        (r"/console", ConsoleHandler, {'process': process})
    ])
if __name__ == '__main__':
    try:
        startGUI()
        app = makeApp()
        app.listen(80)
        IOLoop.current().start()
    except KeyboardInterrupt:
        Log.clear()