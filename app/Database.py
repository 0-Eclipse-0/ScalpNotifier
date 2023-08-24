import sqlite3
from threading import Lock
import os

DATABASE = os.path.join(os.path.dirname(__file__), '../database.db')

lock = Lock()

class Database:
    def __init__(self):
        self.database = sqlite3.connect(DATABASE, check_same_thread=False)
        self.cursor = self.database.cursor()

    def insertItem(self, item, listing, location, price, link): # Insert item int db after validation
        insertString = "INSERT INTO " + item + " (listing, location, price, link) VALUES (?, ?, ?, ?)"

        lock.acquire(True)
        self.cursor.execute(insertString, (listing, location, price, link))
        lock.release()

    def createTable(self, item): # Create item table if it doesn't exist
        tableString = "CREATE TABLE IF NOT EXISTS " + item + " (listing TEXT, location TEXT, price TEXT, link TEXT);"
        lock.acquire(True)
        self.cursor.execute(tableString)
        lock.release()

    def readDb(self): # Output DB (debugging)
        lock.acquire(True)
        rows = self.cursor.fetchall()
        lock.release()

        for row in rows:
            print(row)

    def entryExists(self, item, listing, location, price, link): # Output if entry already exists
        locateString = "SELECT listing, location, price FROM " + item + " WHERE listing = ? AND location = ? AND price = ? AND link = ?"

        lock.acquire(True)
        self.cursor.execute(locateString, (listing, location, price, link))
        fetchResult = self.cursor.fetchall()
        lock.release()

        return len(fetchResult) == 0  # true if not found
