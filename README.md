raidcall-idling
===============

Ever use Raidcall? Do you ever miss those little icons and rewards for the number of hours you've idled away in the server? Well if you use Mumble and can deal with my shoddy work you may be in luck.

Forked from [cmur2/munin-mumble](https://github.com/cmur2/munin-mumble). Excellent plugin for munin and gave me the insight to attempt this.

Process
-------

Uses information retrieved about users from Mumble through Ice. Updated via cronjob with `update.py` at an interval you define. I recommend every 5 minutes. Then using Flask a leaderboard of sorts is created with the top idlers!

Requirements
------------

You must have the following packages installed: `sqlite3`, `python-zeroc-ice`, `python-pip`, `ice34-slice`.

You must use `pip` to install `flask`.
