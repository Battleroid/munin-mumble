rankings
========

Ever used Raidcall? Want something to sorta kinda fill in the missing icons for idle time? Rankings might just be what you're looking for.

requirements
------------

Install the following via apt or whatever your package manager is:

Debian/Ubuntu:

    python-zeroc-ice ice-slice sqlite3 python-sqlite

Install the requirements in the text file using pip:

    pip install -r requirements.txt

I recommend using virtualenv so you can avoid having a huge clusterfuck of varying version of packages. If you don't, no biggie.

That's it for installing things.

configuration
-------------

1. Creating the database is simple, just run `python rankings.py`. It'll check if the database already exists, if it doesn't it'll create it right there. If it does exist, no worries, nothing will be overwritten.
2. To update the database you'll need to add a cronjob. You can customize the interval to whatever you want, but I typically go for every 5 minutes (ex: `*/5 * * * * /path/to/util.py`). Running `util.py` will do the necessary check and update the database in one go.
3. The provided uWSGI ini should be good enough (at least I hope it is), just setup supervisor or something with it using `uwsgi --ini rankings.conf`. If you don't want to use uwsgi, just add `app.run()` with the appropriate host at the end of the `if '__name__'` spiel in `rankings.py` and run it like any other Python script.
4. You'll need something like Nginx or Apache to proxy to the uWSGI process. I've included a [working] nginx sample, see [nginx_sample](nginx_sample).

todo
----

- [x] add lower tier crowns for 2nd & 3rd
- [x] add total time accumulated (years, months, days, minutes)
- [ ] basic API with marshmallow & flask-restful, or screw that and just use jsonify :-) (?, should I even bother?)

misc
----

The [crown](static/crown.png) is from Raidcall. I hope to replace it with something else later on.
