import sys
sys.path.insert(0, r"C:\Users\rudel\.gemini\antigravity\scratch\etsi_directory_services")
from backend import db

fks = db.query_all("""
SELECT 
    sch_p.name AS parent_schema,
    t_p.name AS parent_table,
    c_p.name AS parent_col,
    sch_r.name AS ref_schema,
    t_r.name AS ref_table,
    c_r.name AS ref_col
FROM WPMDB.sys.foreign_keys fk
JOIN WPMDB.sys.tables t_p ON fk.parent_object_id = t_p.object_id
JOIN WPMDB.sys.schemas sch_p ON t_p.schema_id = sch_p.schema_id
JOIN WPMDB.sys.tables t_r ON fk.referenced_object_id = t_r.object_id
JOIN WPMDB.sys.schemas sch_r ON t_r.schema_id = sch_r.schema_id
JOIN WPMDB.sys.foreign_key_columns fkc ON fk.object_id = fkc.constraint_object_id
JOIN WPMDB.sys.columns c_p ON fkc.parent_object_id = c_p.object_id AND fkc.parent_column_id = c_p.column_id
JOIN WPMDB.sys.columns c_r ON fkc.referenced_object_id = c_r.object_id AND fkc.referenced_column_id = c_r.column_id
WHERE sch_p.name IN ('mandate', 'legislation', 'work_item')
""")

print("FKs in mandate, legislation, work_item:")
for f in fks:
    print(f"  {f['parent_schema']}.{f['parent_table']}.{f['parent_col']} --> {f['ref_schema']}.{f['ref_table']}.{f['ref_col']}")
