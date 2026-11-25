import yaml
import os

config_path = r"C:\Users\rudel\.gemini\antigravity\scratch\wpmdb-er-diagram\super-er-diagram.config.yaml"

with open(config_path, "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

# Define domains for WPMDB in English
domains = {
    "work_items": {
        "name": "Standards & Specifications (Work Items)",
        "short": "WKI",
        "color": "#2563eb"
    },
    "schedules": {
        "name": "Milestones & Schedules",
        "short": "SCH",
        "color": "#059669"
    },
    "mandates_legislation": {
        "name": "EC Mandates & Legislation",
        "short": "REG",
        "color": "#d97706"
    },
    "publication_transposition": {
        "name": "Catalogue & NSO Transposition",
        "short": "CAT",
        "color": "#7c3aed"
    },
    "stf_projects": {
        "name": "Special Task Forces (STF)",
        "short": "STF",
        "color": "#0891b2"
    },
    "referentials": {
        "name": "Reference Data & Taxonomies",
        "short": "REF",
        "color": "#4b5563",
        "neutral": True
    },
    "audit_history": {
        "name": "Audit Logs & History",
        "short": "LOG",
        "color": "#64748b",
        "neutral": True
    }
}

config["title"] = "ETSI WPMDB — Work Programme Management Database"
config["domains"] = domains
config["columns"] = [
    ["work_items", "schedules"],
    ["mandates_legislation", "publication_transposition"],
    ["stf_projects", "referentials", "audit_history"]
]
config["hiddenFkColumns"] = []

def classify_wpm_table(name, role_guess):
    n = name.upper()
    
    # 1. Audit & Logs
    if "HISTO" in n or "LOG" in n or "DELETE" in n or "HISTORY" in n or n in ["SCHEDULE_TMP", "TMP_SCHEDULE"]:
        return "audit_history", "log", f"Historical archive and audit log: {name}"

    # 2. STF (Special Task Forces)
    if n.startswith("STF"):
        if n in ["STF_WORK_ITEM"]:
            return "stf_projects", "hub", "Resource allocation and governance for Special Task Forces (STF)"
        elif n in ["STF_SCHEDULE", "STF_TRAVEL"]:
            return "stf_projects", "tx", f"Operational management of STF missions and schedules: {name}"
        elif n in ["STF_REFERENCE_TRAVEL", "STF_SCHEDULE_TYPE"]:
            return "stf_projects", "master", f"STF travel rates and schedule taxonomy: {name}"
        return "stf_projects", "child", f"STF management metadata: {name}"

    # 3. Mandates & Legislation
    if "MANDATE" in n or "LEGISLATION" in n or n.startswith("WKI_DIRECTIVE") or n.startswith("WKI_MANDATE"):
        if n in ["MANDATE"]:
            return "mandates_legislation", "hub", "European Commission standardisation mandates and Standardisation Requests"
        elif n in ["LEGISLATION"]:
            return "mandates_legislation", "hub", "European directives and regulations (RED, EMC, LVD, Cyber Resilience Act...)"
        elif n in ["REQUESTED_DELIVERABLE"]:
            return "mandates_legislation", "tx", "Deliverables officially required by an EU standardisation mandate"
        elif n in ["REQUESTED_DELIVERABLE_WORKITEM", "LEGISLATIONS_MANDATES", "WKI_DIRECTIVE", "WKI_MANDATE"]:
            return "mandates_legislation", "join", f"Legal mandate mapping: {name}"
        elif n in ["PROPERTIES_LEGISLATIONS", "MANDATE_PROPERTY", "REQUESTED_DELIVERABLE_PROPERTY"]:
            return "mandates_legislation", "child", f"Legal properties and regulatory metadata: {name}"
        return "mandates_legislation", "master", f"Regulatory framework lookup: {name}"

    # 4. Publication & Transposition
    if "CATALOG" in n or n in ["TRANSPOSITION", "ARTICLE", "T_EDITION"]:
        if n in ["CATALOG_MAIN"]:
            return "publication_transposition", "hub", "Official catalogue of all published ETSI standards"
        elif n in ["TRANSPOSITION"]:
            return "publication_transposition", "tx", "National transposition of European Standards (EN) by National Standards Bodies (NSOs)"
        elif n in ["CATALOG_TITLE", "CATALOG_INDEX"]:
            return "publication_transposition", "child", f"Publication catalogue details and indexation: {name}"
        elif n == "ARTICLE":
            return "publication_transposition", "tx", "Published normative articles and clauses"
        return "publication_transposition", "child", f"Publication metadata: {name}"

    # 5. Schedules & Milestones
    if n in ["SCHEDULE", "PROTOTYPE", "WP_PROCEDURE"] or n.startswith("EVENT"):
        if n == "SCHEDULE":
            return "schedules", "hub", "Complete milestone timeline tracking standardisation lifecycle (> 520,000 milestones)"
        elif n == "WP_PROCEDURE":
            return "schedules", "master", "Formal approval procedures and voting cycles (AP, PE, MV, OAP)"
        elif n == "PROTOTYPE":
            return "schedules", "child", "Standard milestone prototype templates by deliverable type"
        elif n.startswith("EVENT"):
            return "schedules", "tx", f"Deliverable production lifecycle events: {name}"
        return "schedules", "child", f"Production planning data: {name}"

    # 6. Work Items
    if n.startswith("WKI") or n in ["WORK_ITEM", "SUPERSEDE", "SUPPORTING_MEMBERS", "OTHER_STANDARD"]:
        if n == "WORK_ITEM":
            return "work_items", "hub", "Technical specifications, reports and European standards (TS, TR, EN, ES, GS)"
        elif n in ["SUPERSEDE"]:
            return "work_items", "join", "Standard superseding, revision chain and version succession"
        elif n in ["WKI_CROSS_REF"]:
            return "work_items", "join", "Cross-references and technical dependencies between standards"
        elif n in ["SUPPORTING_MEMBERS"]:
            return "work_items", "child", "ETSI member companies officially supporting Work Item creation"
        elif n in ["WKI_KEYWORD", "WKI_CLUSTER", "WKI_PROJECT", "WKI_FREQUENCY"]:
            return "work_items", "join", f"Thematic indexing and technology categorization: {name}"
        elif n in ["WKI_REMARK", "WKI_MEMO", "WKI_ASPECTS"]:
            return "work_items", "child", f"Technical notes and remarks: {name}"
        return "work_items", "child", f"Work item metadata: {name}"

    # 7. Referentials & Nomenclatures
    if n.startswith("TAB_") or n.startswith("WP_") or n.startswith("APP") or n in ["APPLICATION", "COMMON_FIELD"]:
        if n == "TAB_MILESTONE_CODE":
            desc = "Procedural milestone codes (TB Approval, Membership Vote, Publication)"
        elif n == "TAB_ACTION_TYPE":
            desc = "Standardisation action types"
        elif n == "TAB_STD_TYPE":
            desc = "Standard types (TS, TR, EN, ES, EG, GS)"
        elif n == "TAB_STD_STATUS":
            desc = "Lifecycle status codes for standards"
        elif n == "TAB_CLUSTER":
            desc = "Technology clusters and thematic domains"
        elif n == "WP_KEYWORD":
            desc = "Standardisation thesaurus keywords"
        else:
            desc = f"Reference taxonomy: {name}"
        return "referentials", "master", desc

    return "referentials", role_guess or "master", f"Reference lookup table: {name}"

# Apply classification to all tables
for tname, tinfo in config.get("tables", {}).items():
    current_role = tinfo.get("role", "master")
    dom, role, desc = classify_wpm_table(tname, current_role)
    tinfo["domain"] = dom
    tinfo["role"] = role
    tinfo["description"] = desc
    tinfo["label"] = tname

with open(config_path, "w", encoding="utf-8") as f:
    yaml.dump(config, f, allow_unicode=True, sort_keys=False)

print("Updated WPMDB super-er-diagram.config.yaml with English domains, roles, and descriptions.")
