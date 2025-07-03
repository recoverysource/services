Recovery Source: Services
=========================

This repository provides a "standardized" solution to test, deploy, and maintain
various web "services" provided by [Recovery Source](https://handbook.recoverysource.net/).

Basic Workflows
---------------

To Do ...

Repository Structure
--------------------

The structure of this repository:

- ``Makefile``: Convenient helper tasks
- ``data/``: Primary source of data (all known 12-Step groups)
- ``sync/``: Python3 module that collects and re-mangles data
- ``web_index/``: Hugo-based website that hosts https://sober.page
- ``ansible/``: Used for configuration management (deploy, maintain, etc.)
- ``test/``: Data used for automated testing

Web Index
---------

Sober Pages service as a directory services for 12-step focused websites and
aims to provide support for basic maintenance tasks.

See this website running at https://sober.page/.

Source Data
-----------

Everything the Recovery Source project knows about 12-Step groups.

### Data Format

**Location:** ``data/domains/<group>.yaml``

**Format [[YAML](https://handbook.recoverysource.net/essentials/yaml.html)]:**
```
<subdomain>:
  title: website title
  keywords: list, of, regions
  target: <URL>
  type: forward OR cname
  feed: <type>^<URL>[^<options>]
```

**Required:** subdomain, title, target

**Rules:**

- ``data/domains/*.yaml`` MUST be [valid YAML](https://yaml-online-parser.appspot.com/)
- [``title``, ``keywords``] may be mixed-case, all other fields must be lower-case
- ``target`` should be the shortest functional URL (without
[path/query/fragment](https://handbook.recoverysource.net/essentials/websites.html#url))
- ``target`` should include www if upstream redirects to this address
- ``feed`` may be a [YAML list](https://handbook.recoverysource.net/essentials/yaml.html)
of feed locations (type+url)
- ``subdomain`` is limited to one (1) per ``target``
- ``subdomain`` format should follow ``[type][area]-[district]`` (e.g. aa0-5)
- ``subdomain`` may append characters to resolve conflicts (e.g. aa1-4north)
- ``subdomain`` should use the lowest represented district as canonical
- ``subdomain`` can be used as a SP alias to redirect additional-represented districts
- ``feed/type`` must be one of [``aamod``, ``tsml``]

Sync
----

Data synchronization is done using the ``sync`` python module.

**$ cd services && python3 -m sync -h**:
```
usage: python3 -m sync [-h] [actions] <options>

Synchronize sober.page data with various destinations

options:
  -h, --help        show this help message and exit
  -H <path>         Path to source data (hugo format)
  -w <path>         Local workspace used for importing/caching data
  -l <level>        Log level (DEBUG, INFO*, WARNING, ERROR)

actions[*]:
  -m <path>         Generate nginx map file at <path>
  -z <zone>:<path>  Generate bind9 zone (db) at <path>

[*] At least one script action must be specified.
```
