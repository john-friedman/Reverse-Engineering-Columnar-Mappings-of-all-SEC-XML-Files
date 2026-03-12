from datamule import Portfolio
from src.parser import parser
from mappings.all import SEC_DOCUMENTS_MAPPING
from src.utils import print_tables
import shutil
import os
import json

if os.path.exists('test'):
    shutil.rmtree('test')
portfolio = Portfolio('test')
doc_type = ["4"]
portfolio.download_submissions(document_type=doc_type,filing_date=('2026-01-01','2026-01-05'))

for sub in portfolio:
    for doc in sub:
        if doc.extension != '.xml':
            continue
        if doc.type in doc_type:
            rows = parser(doc.content,mapping=SEC_DOCUMENTS_MAPPING[doc.type])
            with open('local.json','w') as f:
                f.write(str(rows))
            
            #print(len(rows))
            print_tables(rows)
            #print(doc.content)
            input()
            #audit(doc.content,mapping=SEC_DOCUMENTS_MAPPING[doc_type])
