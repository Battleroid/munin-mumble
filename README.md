raidcall-idling
===============

Replicates functionality for user 'Ranks' from Raidcall for Mumble. Captures and tracks registered user's time spent on server.

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

* Use jQuery & built-in API to update without reloading page through AJAX.
