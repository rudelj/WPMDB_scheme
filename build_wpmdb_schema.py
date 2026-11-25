import sys
import json
import os
from datetime import datetime

sys.path.insert(0, r"C:\Users\rudel\.gemini\antigravity\scratch\etsi_directory_services")
from backend import db

out_dir = r"C:\Users\rudel\.gemini\antigravity\scratch\wpmdb-er-diagram"
os.makedirs(out_dir, exist_ok=True)

# 1. Fetch tables from WPMDB
tables_sql = """
SELECT 
    s.name AS schema_name,
    t.name AS table_name,
    t.object_id,
    p.rows AS row_count
FROM WPMDB.sys.tables t
JOIN WPMDB.sys.schemas s ON t.schema_id = s.schema_id
JOIN WPMDB.sys.partitions p ON t.object_id = p.object_id
WHERE p.index_id IN (0, 1)
  AND t.name NOT LIKE '%save%'
  AND t.name NOT LIKE '%Save%'
  AND t.name NOT LIKE '%Bkp%'
  AND t.name NOT LIKE '%Backup%'
  AND t.name NOT LIKE 'tmp%'
  AND t.name NOT LIKE 'TMP%'
  AND t.name NOT LIKE 'X[_]%'
  AND t.name NOT LIKE 'ToDelete%'
  AND t.name NOT LIKE '[_][_]%'
ORDER BY s.name, t.name
"""
tables = db.query_all(tables_sql)

# PKs
pk_sql = """
SELECT 
    t.name AS table_name,
    c.name AS col_name
FROM WPMDB.sys.key_constraints kc
JOIN WPMDB.sys.tables t ON kc.parent_object_id = t.object_id
JOIN WPMDB.sys.index_columns ic ON kc.parent_object_id = ic.object_id AND kc.unique_index_id = ic.index_id
JOIN WPMDB.sys.columns c ON ic.object_id = c.object_id AND ic.column_id = c.column_id
WHERE kc.type = 'PK'
"""
pks = db.query_all(pk_sql)
pk_map = {}
for p in pks:
    pk_map.setdefault(p['table_name'].lower(), set()).add(p['col_name'].lower())

# Columns
col_sql = """
SELECT 
    t.name AS table_name,
    c.name AS col_name,
    ty.name AS type_name,
    c.is_nullable
FROM WPMDB.sys.columns c
JOIN WPMDB.sys.tables t ON c.object_id = t.object_id
JOIN WPMDB.sys.types ty ON c.user_type_id = ty.user_type_id
ORDER BY t.name, c.column_id
"""
columns = db.query_all(col_sql)
cols_by_table = {}
for c in columns:
    cols_by_table.setdefault(c['table_name'], []).append(c)

# FKs
fk_sql = """
SELECT 
    t_p.name AS parent_table,
    c_p.name AS parent_col,
    t_r.name AS ref_table,
    c_r.name AS ref_col
FROM WPMDB.sys.foreign_keys fk
JOIN WPMDB.sys.tables t_p ON fk.parent_object_id = t_p.object_id
JOIN WPMDB.sys.tables t_r ON fk.referenced_object_id = t_r.object_id
JOIN WPMDB.sys.foreign_key_columns fkc ON fk.object_id = fkc.constraint_object_id
JOIN WPMDB.sys.columns c_p ON fkc.parent_object_id = c_p.object_id AND fkc.parent_column_id = c_p.column_id
JOIN WPMDB.sys.columns c_r ON fkc.referenced_object_id = c_r.object_id AND fkc.referenced_column_id = c_r.column_id
"""
fks = db.query_all(fk_sql)

raw_tables_list = []
included_table_names = set()

for t in tables:
    tname = t['table_name']
    included_table_names.add(tname)
    
    t_cols = cols_by_table.get(tname, [])
    table_pks = pk_map.get(tname.lower(), set())
    
    raw_cols = []
    for c in t_cols:
        is_pk = c['col_name'].lower() in table_pks
        raw_cols.append({
            "name": c['col_name'],
            "type": c['type_name'],
            "nullable": bool(c['is_nullable']),
            "pk": is_pk
        })
    
    raw_tables_list.append({
        "name": tname,
        "columns": raw_cols
    })

raw_fks_list = []
for f in fks:
    if f['parent_table'] in included_table_names and f['ref_table'] in included_table_names:
        raw_fks_list.append({
            "table": f['parent_table'],
            "column": f['parent_col'],
            "refTable": f['ref_table'],
            "refColumn": f['ref_col']
        })

schema_json = {
    "dialect": "postgres",
    "database": "WPMDB",
    "schema": "dbo",
    "tables": raw_tables_list,
    "foreignKeys": raw_fks_list,
    "introspectedAt": datetime.now().isoformat()
}

schema_path = os.path.join(out_dir, "schema.json")
with open(schema_path, "w", encoding="utf-8") as f:
    json.dump(schema_json, f, indent=2)

print(f"Generated schema.json for WPMDB with {len(raw_tables_list)} tables and {len(raw_fks_list)} FKs.")
