munin-mumble
============

Creates Munin graphs from the data that a (local) Murmur server provides via it's [Ice](http://www.zeroc.com/ice.html) interface.

Needs Python Ice bindings and a local database of Slice definitions provided by the packages `python-zeroc-ice` and `ice-slice` on Debian 7 (Wheezy).

Install
-------

Clone this repository or download the mumble file and create a
symlink as *root* in /etc/munin/plugins by using e.g.:

	cd /etc/munin/plugins; ln -s /path/to/mumble mumble

Needed configuration is explained in the script itself.

**Don't forget to restart your munin-node deamon.**
