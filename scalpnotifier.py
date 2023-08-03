MARKET_LOCATIONS = [] # List of locations
MARKET_ITEMS = [] # List of items
SLEEP_TIME = 300 # Time to wait before checking again (Seconds)
FREE_ONLY = True # Parse only free items
BEAUTIFUL_EMAIL = True # Send emails in html format
TARGET_EMAIL = ""
SENDER_EMAIL = ""

ITEM_CLASS = "x3ct3a4" # Developer only (Future Proofing)

from Scalper import Scalper
from Notification import Notification
from Database import Database
from time import sleep
import threading

def startProcess(item, location, db, newItems):
    db.createTable(item)
    # Build url based on current location and item
    targetUrl = "https://www.facebook.com/marketplace/" \
                + location + "/search?query=" \
                + "%20".join(item.split()) + "&minPrice=0&maxPrice=0" if FREE_ONLY else ""

    browser = Scalper(targetUrl, ITEM_CLASS)
    browser.getSource()

    # Parse free items from sourced list
    for i in parseItems(browser.getItems()):
        if db.entryExists(item, i[1], i[2], i[0], i[3]):  # Add to database if not found
            newItems.append(i)
            db.insertItem(item, i[1], i[2], i[0], i[3])
            db.database.commit()
    browser.end()

def startProgram(db):
    newItems = []
    threads = []

    # Open threads
    for location in MARKET_LOCATIONS:
        for item in MARKET_ITEMS:
            print(f"\rThread started for {item} at {location}")
            t = threading.Thread(target=startProcess, args=(item, location, db, newItems, ))
            threads.append(t)
            t.start()

    print("Waiting for all new threads to complete (Approx: 40s)", end="")

    # Wait until all threads are completed
    for thread in threads:
        thread.join()

    return newItems

def parseItems(original):
    items = []

    for item in range(len(original)):
        original[item][1].replace('\'', "").replace('\"', "") # Prevent SQL error

        if FREE_ONLY: # Find only free items
            if original[item][0] == "Free":
                items.append(original[item])
        else:
            items.append(original[item])

    return items

if __name__ == '__main__':
    db = Database()
    notification = Notification(SENDER_EMAIL, TARGET_EMAIL)

    try:
        while True:
            items = startProgram(db)

            # Output newly found items
            if items == []:
                print("\rNo new items found!")
            else:
                print("\rAll new items:")


                for i in items:
                    print("\t\t• " + ", ".join(i))

                # Send email
                notification.betterEmail(items) if BEAUTIFUL_EMAIL else notification.email(items)

            # Wait Timer
            i = 0
            while i != SLEEP_TIME:
                print("\rChecking again in %.2f minutes..." % ((SLEEP_TIME - i) / 60), end="")
                sleep(1)
                i += 1

    except KeyboardInterrupt:
        print("Exiting...")
        db.database.close()


