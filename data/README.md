Recovery Source: Data
=====================

This is the source data used by [Recovery Source Services](
https://github.com/recoverysource/services) projects. This is everything the
Recovery Source project knows about 12-Step groups.

This data was orginally created for Hugo, however this framework proved to be
unstable and the future format should be based on i18n+framework.

Data Format
-----------

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
