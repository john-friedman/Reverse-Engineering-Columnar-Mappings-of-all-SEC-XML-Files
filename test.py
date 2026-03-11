from datamule import Portfolio
from parser import audit, parse, print_tables
from mappings.all import SEC_DOCUMENTS_MAPPING
import json

portfolio = Portfolio('test')
portfolio.download_submissions(submission_type='QUALIF',filing_date=('2021-01-01','2021-01-31'))

for sub in portfolio:
    for doc in sub:
        doc_type = doc.type
        if doc_type == 'QUALIF':
            tables = parse(doc.content,mapping=SEC_DOCUMENTS_MAPPING[doc_type])
            print_tables(tables)
            #audit(doc.content,mapping=SEC_DOCUMENTS_MAPPING[doc_type])
