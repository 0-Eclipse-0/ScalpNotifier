# Configuration class
from Scalper import Scalper
from Notification import Notification
from Database import Database
from Log import Log
from time import sleep
import threading
import hashlib

class Scalpnotifier:
    def __init__(self,
                 locations,
                 items,
                 sleepTime,
                 freeOnlyMode,
                 beautifiedEmailMode,
                 targetEmail,
                 senderEmail,
                 senderEmailPass):
        self.targetEmail = targetEmail
        self.senderEmail = senderEmail
        self.senderEmailPass = senderEmailPass
        self.locations = locations.split(', ')
        self.items = items.split(', ')
        self.freeOnlyMode = True if (freeOnlyMode) == "True" else False
        self.beautifiedEmailMode = True if (beautifiedEmailMode) == "True" else False
        self.sleepTime = int(sleepTime)
        self.itemClass = "x3ct3a4"

    def startProcess(self, item, location, db, newItems):
        # Hash to avoid sql errors
        itemHash = "hash_" + str(hashlib.sha512(item.encode()).hexdigest())

        db.createTable(itemHash)

        # Build url based on current location and item
        targetUrl = "https://www.facebook.com/marketplace/" \
                    + location + "/search?query=" \
                    + "%20".join(item.split()) + ("&minPrice=0&maxPrice=0" if self.freeOnlyMode else '')

        browser = Scalper(targetUrl, self.itemClass)
        browser.getSource()

        # Parse free items from sourced list
        for i in self.parseItems(browser.getItems()):
            if db.entryExists(itemHash, i[1], i[2], i[0], i[3]):  # Add to database if not found
                newItems.append(i)
                db.insertItem(itemHash, i[1], i[2], i[0], i[3])
                db.database.commit()
        browser.end()

    def startProgram(self, db):
        newItems = []
        threads = []

        # Open threads
        for location in self.locations:
            for item in self.items:
                Log.write(f"Thread started for {item} at {location}")
                t = threading.Thread(target=self.startProcess, args=(item, location, db, newItems,))
                threads.append(t)
                t.start()

        Log.write("Waiting for all new threads to complete (Approx: 40s)")

        # Wait until all threads are completed
        for thread in threads:
            thread.join()

        return newItems

    def parseItems(self, original):
        items = []

        for item in range(len(original)):
            original[item][1].replace('\'', "").replace('\"', "")  # Prevent SQL error

            if self.freeOnlyMode:  # Find only free items
                if original[item][0] == "Free":
                    items.append(original[item])
            else:
                items.append(original[item])

        return items

    def run(self):
        db = Database()
        notification = Notification(self.senderEmail, self.targetEmail, self.senderEmailPass)

        try:
            while True:
                items = self.startProgram(db)

                # Output newly found items
                if items == []:
                    Log.write("No new items found!")
                else:
                    Log.write("All new items:")

                    for i in items:
                        Log.write("\t\t• " + ", ".join(i[:(len(i)) - 2]))

                    # Send email
                    notification.betterEmail(items) if self.beautifiedEmailMode else notification.email(items)

                # Wait Timer
                i = 0
                while i != self.sleepTime:
                    Log.write(str("\rChecking again in %.2f minutes..." % ((self.sleepTime - i) / 60)))
                    sleep(self.sleepTime / 10)
                    i += self.sleepTime / 10


        except KeyboardInterrupt:
            db.database.close()
