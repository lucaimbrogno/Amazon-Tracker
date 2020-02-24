# Amazon-Tracker

Amazon product tracker built in Python using the BeautifulSoup library for web scraping and the Simple Mail Transport Protocol (SMTP) library for sending emails.

Enter multiple products into the script in order to start tracking them. The script will check if each of your prodcuts ever drops below your desired price and notify you via gmail to let you know.

To get this script working for your client you must do a few things:
- You must enter your gmail credientials at the top of the tracker file. Including the email you want to send from and to.
- You must enter your User Agent into the header variable. You can find your User Agent at https://www.whatismybrowser.com/detect/what-is-my-user-agent
- You must enable less secure apps on your google account 

This script can be executed in two ways. Currently it's set to run once and end. If you want to use this script as a daemon or run it in the brackground of a project then you can comment the 'ONE TIME EXECECTION" block and uncomment the "BACKGROUND EXECUTION" block. When running as a background process, the script will check your products once per day.
