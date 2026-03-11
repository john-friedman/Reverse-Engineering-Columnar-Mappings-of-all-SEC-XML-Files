from datamule import Portfolio
from parser import audit, parse, print_tables
from mappings.all import SEC_DOCUMENTS_MAPPING
import json

portfolio = Portfolio('test')
doc_type = "13F-HR"
portfolio.download_submissions(document_type=doc_type,filing_date=('2021-01-01','2021-01-31'))

for sub in portfolio:
    for doc in sub:
        if doc_type == doc_type:
            tables = parse(doc.content,mapping=SEC_DOCUMENTS_MAPPING[doc_type])
            print_tables(tables)
            #audit(doc.content,mapping=SEC_DOCUMENTS_MAPPING[doc_type])
