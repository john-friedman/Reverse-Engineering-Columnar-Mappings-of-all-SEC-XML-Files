Mapping Construction
Given a frequency audit dict of {xpath: count} for a document type:

Identify table boundaries — find paths that share a common parent with sibling paths at the same depth. That parent is a repeating element → becomes its own table. Paths with no repeating parent → flat document table.
Name tables — flat doc table takes the document type name (e.g. d), repeating tables get a descriptive suffix (e.g. d_related_person, d_issuer)
Name columns — strip the common path prefix, camelCase the leaf element name. Disambiguate collisions (e.g. two street1 fields from different sections get prefixed: brokerStreet1, agentStreet1)
Output one JSON file per document type, plus alias entries in SEC_DOCUMENTS_MAPPING for /A variants that share the same schema