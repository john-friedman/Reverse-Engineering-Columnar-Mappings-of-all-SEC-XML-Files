
# Reverse Engineering Columnar Mappings of all SEC XML Files

There are 100+ SEC document types that have XML extensions. XML is harder to work with, and takes up more storage than columnar representation.

This repo consists of:

- xpaths/ : xpaths with attributes of all SEC XML files excluding XBRL
- mappings/ : xml mapped to columnar format.

Mappings is currently in .py format, will be converted to .json in the future.

## Misc:

- xpaths generated using [datamule's](https://github.com/john-friedman/datamule-python) SEC Archive. It took about 2 hours using a c8g.xlarge. This was due to bandwidth limitation by Cloudflare at around 200MB/s.

## TODO
download the new xpaths that have values
parser works, but needs attribute handling
pretty print for tables