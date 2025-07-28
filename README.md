Recovery Source: Services
=========================

This repository provides a "standardized" solution to test, deploy, and maintain
various web "services" provided by [Recovery Source](https://handbook.recoverysource.net/).

**Repository Structure:**

- **data**: Source data for all services
- **sync**: Synchronize source and remote data with other resources
- **web_index**: [Directory listing of 12-Step groups](https://sober.page/)
- **nameserver**: Configuration for [DNS](https://handbook.recoverysource.net/essentials/websites.html#domain-name-system) services
- **forwarder**: Configuration for "HTTP Redirector" service
- **test**: Data used for automated testing

Source Data
-----------

[Source Data](https://github.com/recoverysource/services/tree/master/data)
holds our collection of known 12-Step groups with publicly available meeting
information. This directory contains another README file with addition details.

Synchronize Data
----------------

The [sync](https://github.com/recoverysource/services/tree/master/sync) utility
is a python3 package that uses ``Source Data`` to scrape meeting data from known
sources and assemble them all into a single standardized collection .

This script is responsible for keeping this data synchronized with other services,
such as CloudFlare DNS, a Managed VPS, or into a format suitable for the
``Web Index``. Developer notes are available in sync/README.

Help text is available using:
```
$ cd services && python3 -m sync -h
```

Web Index
---------

Sober Pages service as a directory services for 12-step focused websites and
aims to provide support for basic maintenance tasks.

See this website running at https://sober.page/.

Forwarder
---------

Every 12-Step website that we list includes a link back that website. We also
provide a subdomain that redirects all requests to that domain. This has been
used for creating short/friendly URLs on flyers, but the options are endless.

Name Server
-----------

For any 12-Step group that does not have a website and finds the cost to be
a burden, our subdomain can be used as a primary website.

Automatic Testing
-----------------

We utilize automatic testing to prevent as many potential issues as possible.
This is used by automatic release processes as well as developers.
