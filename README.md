# ScalpNotifier
>Facebook scalping program built in Python using Selenium and BeautifulSoup for obtaining and parsing through
>facebook marketplace data, Sqlite3 for a simple database to avoid users recieving notifications about repeating items,
>and Tornado Web Handler for hosting a GUI created in Bootstrap5 and HTML.

### Usage
1. Run `pip install -r requirements.txt` from the root of the ScalpNotifier directory
2. Execute `python run.py` to start the GUI.
3. Fill in information (locations and items must be in comma separated list format). Email must be gmail, and the password must be an [App-Password](https://support.google.com/mail/answer/185833?hl=en) however modifications
can be made to app.Notification to use a different smtp server.
4. Hit "run" and a scalping process will be started. It will continue to run at your selected interval until "Kill Process" is selected. All configuration information will be saved to `config.ini` in order to auto-fill for later uses.

### Tips
- The database can be reset by deleting `database.db`
- "False Price Prevention" hasn't been implemented yet
- Avoid too short of intervals as Google has a daily limit of emails for Apps

### Warning
- Do not run this program on public networks
- Do not host this program on a public web server

### Images
Setup            |  Running
:-------------------------:|:-------------------------:
![](https://github.com/0-Eclipse-0/ScalpNotifier/blob/main/images/setup.png)  |  ![](https://github.com/0-Eclipse-0/ScalpNotifier/blob/main/images/running.png)

![](https://github.com/0-Eclipse-0/ScalpNotifier/blob/main/images/email.png)
