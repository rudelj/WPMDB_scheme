import sys
import json
import os
sys.path.insert(0, r"C:\Users\rudel\.gemini\antigravity\scratch\etsi_directory_services")
from backend import db

out_dir = r"C:\Users\rudel\.gemini\antigravity\scratch\wpmdb-er-diagram"
os.makedirs(out_dir, exist_ok=True)

# 1. Tables in WPMDB
tables = db.query_all("""
SELECT 
    s.name AS schema_name,
    t.name AS table_name,
    t.object_id,
    p.rows AS row_count
FROM WPMDB.sys.tables t
JOIN WPMDB.sys.schemas s ON t.schema_id = s.schema_id
JOIN WPMDB.sys.partitions p ON t.object_id = p.object_id
WHERE p.index_id IN (0, 1)
ORDER BY p.rows DESC
""")
print(f"Total tables in WPMDB: {len(tables)}")
for t in tables[:30]:
    print(f"  {t['schema_name']}.{t['table_name']:<35} : {t['row_count']} rows")

# 2. Schemas in WPMDB
schemas = db.query_all("""
SELECT s.name AS schema_name, COUNT(t.object_id) AS table_count
FROM WPMDB.sys.schemas s
LEFT JOIN WPMDB.sys.tables t ON s.schema_id = t.schema_id
GROUP BY s.name
HAVING COUNT(t.object_id) > 0
ORDER BY table_count DESC
""")
print("\nSchemas in WPMDB:")
for s in schemas:
    print(f"  {s['schema_name']} ({s['table_count']} tables)")

# 3. PKs
pks = db.query_all("""
SELECT 
    t.name AS table_name,
    c.name AS col_name
FROM WPMDB.sys.key_constraints kc
JOIN WPMDB.sys.tables t ON kc.parent_object_id = t.object_id
JOIN WPMDB.sys.index_columns ic ON kc.parent_object_id = ic.object_id AND kc.unique_index_id = ic.index_id
JOIN WPMDB.sys.columns c ON ic.object_id = c.object_id AND ic.column_id = c.column_id
WHERE kc.type = 'PK'
""")
print(f"\nTotal PK constraints in WPMDB: {len(pks)}")

# 4. FKs
fks = db.query_all("""
SELECT 
    t_p.name AS parent_table,
    c_p.name AS parent_col,
    t_r.name AS ref_table,
    c_r.name AS ref_col,
    fk.name AS fk_name
FROM WPMDB.sys.foreign_keys fk
JOIN WPMDB.sys.tables t_p ON fk.parent_object_id = t_p.object_id
JOIN WPMDB.sys.tables t_r ON fk.referenced_object_id = t_r.object_id
JOIN WPMDB.sys.foreign_key_columns fkc ON fk.object_id = fkc.constraint_object_id
JOIN WPMDB.sys.columns c_p ON fkc.parent_object_id = c_p.object_id AND fkc.parent_column_id = c_p.column_id
JOIN WPMDB.sys.columns c_r ON fkc.referenced_object_id = c_r.object_id AND fkc.referenced_column_id = c_r.column_id
""")
print(f"Total FK constraints in WPMDB: {len(fks)}")

# 5. Views in WPMDB
views = db.query_all("SELECT name FROM WPMDB.sys.views ORDER BY name")
print(f"Total Views in WPMDB: {len(views)}")
for v in views[:15]:
    print(f"  View: {v['name']}")
