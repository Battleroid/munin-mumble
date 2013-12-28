raidcall-idling
===============

Ever use Raidcall? Do you ever miss those little icons and rewards for the number of hours you've idled away in the server? Well if you use Mumble and can deal with my shoddy work you may be in luck.

Features a small API as well (needs work though). You can access all users by navigating to `http://yourhost:port/users`. This will return a JSON response with all users and their current points (eventually some more info).

To retrieve an individual's information simply navigate to `http://yourhost:port/user/username`. This will return a JSON response with that individual's stats.

Forked from [cmur2/munin-mumble](https://github.com/cmur2/munin-mumble). Excellent plugin for munin that gave me the insight to attempt this.

Uses [sorttable](http://www.kryogenix.org/code/browser/sorttable/) which makes it easy as hell to sort by fields in an HTML table. No dependencies either.

Requirements
------------

You will need `python-pip` installed to install Flask. To install Flask run `pip install flask`.

You will need following packages installed: `python-zeroc-ice`, `ice-slice`, and `sqlite3` installed.

Installation
------------

1. First create the database by running `sqlite3 idle.db < schema.sql`.
2. Create a cronjob to run every five minutes (or however often you wish). Sample: `*/5 * * * * /path/to/update.py /path/to/your/database.db`.
3. Execute `app.py`.

Be aware if you choose to use a different database name you will need to change the name inside `app.py` and your cronjob. 

If you decide to use an update interval other than every five minutes you will need to change the values in the template `leaderboard.html` to reflect the proper amount of time accumulated.

Todo
----

* Consolidate **all** configurable settings to one file for easy importing.
* Split up views/controls/files etc so I don't have one giant cluster of functions.
* Make script check for existence of database, create it if it does not exist.
* Improve the API.
