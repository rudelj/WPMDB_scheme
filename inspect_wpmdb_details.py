import sys
sys.path.insert(0, r"C:\Users\rudel\.gemini\antigravity\scratch\etsi_directory_services")
from backend import db

# List non-dbo tables
non_dbo = db.query_all("""
SELECT s.name AS schema_name, t.name AS table_name, p.rows
FROM WPMDB.sys.tables t
JOIN WPMDB.sys.schemas s ON t.schema_id = s.schema_id
JOIN WPMDB.sys.partitions p ON t.object_id = p.object_id
WHERE s.name != 'dbo' AND p.index_id IN (0,1)
ORDER BY s.name, t.name
""")
print("=== NON-DBO TABLES IN WPMDB ===")
for r in non_dbo:
    print(f"  {r['schema_name']}.{r['table_name']:<30} ({r['rows']} rows)")

# List FK relationships in WPMDB
fks = db.query_all("""
SELECT 
    sch_p.name AS parent_schema,
    t_p.name AS parent_table,
    c_p.name AS parent_col,
    sch_r.name AS ref_schema,
    t_r.name AS ref_table,
    c_r.name AS ref_col,
    fk.name AS fk_name
FROM WPMDB.sys.foreign_keys fk
JOIN WPMDB.sys.tables t_p ON fk.parent_object_id = t_p.object_id
JOIN WPMDB.sys.schemas sch_p ON t_p.schema_id = sch_p.schema_id
JOIN WPMDB.sys.tables t_r ON fk.referenced_object_id = t_r.object_id
JOIN WPMDB.sys.schemas sch_r ON t_r.schema_id = sch_r.schema_id
JOIN WPMDB.sys.foreign_key_columns fkc ON fk.object_id = fkc.constraint_object_id
JOIN WPMDB.sys.columns c_p ON fkc.parent_object_id = c_p.object_id AND fkc.parent_column_id = c_p.column_id
JOIN WPMDB.sys.columns c_r ON fkc.referenced_object_id = c_r.object_id AND fkc.referenced_column_id = c_r.column_id
ORDER BY sch_p.name, t_p.name
""")
print(f"\n=== FOREIGN KEYS IN WPMDB ({len(fks)}) ===")
for f in fks[:40]:
    print(f"  {f['parent_schema']}.{f['parent_table']}.{f['parent_col']} --> {f['ref_schema']}.{f['ref_table']}.{f['ref_col']}")
