def print_tables(rows):
    from itertools import groupby
    
    for table_name, group in groupby(rows, key=lambda r: r["_table"]):
        table_rows = list(group)
        cols = [k for k in table_rows[0].keys() if k != "_table"]
        
        print(f"\n### {table_name}\n")
        print("| " + " | ".join(cols) + " |")
        print("| " + " | ".join(["---"] * len(cols)) + " |")
        
        for row in table_rows:
            print("| " + " | ".join(str(row.get(c, "")) for c in cols) + " |")