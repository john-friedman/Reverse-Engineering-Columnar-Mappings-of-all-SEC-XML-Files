# Reverse Engineering Columnar Mappings of all SEC XML Files

There are 100+ SEC document types that have XML extensions. XML is harder to work with, and takes up more storage than columnar representation.

This repo consists of:

- xpaths/ : xpaths with attributes of all SEC XML files excluding XBRL
- mappings/ : xml mapped to columnar format.
- src/ : naive parser and utils.

## Misc:

- xpaths generated using [datamule's](https://github.com/john-friedman/datamule-python) SEC Archive. It took about 2 hours using a c8g.xlarge. This was due to bandwidth limitation by Cloudflare at around 200MB/s. It cost about $0.30.

## Are these all 100% correct?

No. If there are not issues, I would be surprised. That said, seems good enough. Also we account for...a lot of malformed XML that most parsers miss.