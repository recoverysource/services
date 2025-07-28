Data Synchronization
====================

This ``sync`` directory is a python3 package that is used to synchronize data
across various sources and destinations. This is essentially the "data processing"
portion of [Recovery Source Services](https://github.com/recoverysource/services)
workflows.

Processing
----------

**Input:**

[Source Data](https://github.com/recoverysource/services/tree/master/data)
is the root of the Recovery Source (Web) Index. This data was originally
formatted for Hugo and imported via ``sync.hugo``.

This ``Source Data`` includes links to feeds where meeting information can be
collected. Fetching this remote data is handled using ``sync.collect``.

**Cache:**

Collected data is stored using ``sync.db``; this aims to provide an efficient
mechanism to verify freshness, generate output data, and share assembled data.

**Output:**

- ``sync.nginx``: Creates a map file for Nginx
- ``sync.named``: Creates a zone file for Bind9
- ``sync.cloudflare``: Synchronize ``Source Data`` with CloudFlare DNS

Usage
-----

Current help text:
```
services$ python3 -m sync --help

usage: python3 -m sync [-h] [actions] <options>

Synchronize sober.page data to/from various sources

options:
  -h, --help  show this help message and exit
  -H <path>   Path to hugo file containing DNS data
  -w <path>   Local workspace used for importing/caching data
  -l <level>  Log level (DEBUG, INFO, WARNING*, ERROR)

actions[*]:
  -c          Collect meeting data from remote feeds
  -n <path>   Create an nginx map file and store at <path>
  -z <path>   Create a bind9 zone file and store at <path>

[*] At least one script action must be specified.
```

Create a bind9 zone file:
```
python3 -m sync -z /etc/named/db.managed
```

Create an nginx map file:
```
python3 -m sync -n /etc/nginx/canonical_redirects.map
```

Collect meeting data from remote feeds:
```
python3 -m sync -c
```
