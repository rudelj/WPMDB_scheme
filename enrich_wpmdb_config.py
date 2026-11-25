import yaml
import os

config_path = r"C:\Users\rudel\.gemini\antigravity\scratch\wpmdb-er-diagram\super-er-diagram.config.yaml"

with open(config_path, "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

# Define domains for WPMDB
domains = {
    "work_items": {
        "name": "Normes & Spécifications (Work Items)",
        "short": "WKI",
        "color": "#2563eb"
    },
    "schedules": {
        "name": "Jalons & Procédures (Schedules)",
        "short": "SCH",
        "color": "#059669"
    },
    "mandates_legislation": {
        "name": "Mandats CE & Réglementation",
        "short": "REG",
        "color": "#d97706"
    },
    "publication_transposition": {
        "name": "Catalogue & Transposition (NSO)",
        "short": "CAT",
        "color": "#7c3aed"
    },
    "stf_projects": {
        "name": "Équipes Spéciales d'Experts (STF)",
        "short": "STF",
        "color": "#0891b2"
    },
    "referentials": {
        "name": "Référentiels & Nomenclatures",
        "short": "REF",
        "color": "#4b5563",
        "neutral": True
    },
    "audit_history": {
        "name": "Historique & Traçabilité",
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
        return "audit_history", "log", f"Historique et archivage: {name}"

    # 2. STF (Special Task Forces)
    if n.startswith("STF"):
        if n in ["STF_WORK_ITEM"]:
            return "stf_projects", "hub", "Affectation et gouvernance des équipes spéciales d'experts (STF)"
        elif n in ["STF_SCHEDULE", "STF_TRAVEL"]:
            return "stf_projects", "tx", f"Gestion opérationnelle des missions et plannings STF: {name}"
        elif n in ["STF_REFERENCE_TRAVEL", "STF_SCHEDULE_TYPE"]:
            return "stf_projects", "master", f"Barème et nomenclature STF: {name}"
        return "stf_projects", "child", f"Détail de gestion STF: {name}"

    # 3. Mandates & Legislation
    if "MANDATE" in n or "LEGISLATION" in n or n.startswith("WKI_DIRECTIVE") or n.startswith("WKI_MANDATE"):
        if n in ["MANDATE"]:
            return "mandates_legislation", "hub", "Mandats et demandes de normalisation (Standardisation Requests) de la CE"
        elif n in ["LEGISLATION"]:
            return "mandates_legislation", "hub", "Directives et règlements européens (RED, EMC, LVD, CRA...)"
        elif n in ["REQUESTED_DELIVERABLE"]:
            return "mandates_legislation", "tx", "Livrables officiellement requis par un mandat européen"
        elif n in ["REQUESTED_DELIVERABLE_WORKITEM", "LEGISLATIONS_MANDATES", "WKI_DIRECTIVE", "WKI_MANDATE"]:
            return "mandates_legislation", "join", f"Liaison juridique et mandat: {name}"
        elif n in ["PROPERTIES_LEGISLATIONS", "MANDATE_PROPERTY", "REQUESTED_DELIVERABLE_PROPERTY"]:
            return "mandates_legislation", "child", f"Propriétés et métadonnées juridiques: {name}"
        return "mandates_legislation", "master", f"Nomenclature du cadre réglementaire: {name}"

    # 4. Publication & Transposition
    if "CATALOG" in n or n in ["TRANSPOSITION", "ARTICLE", "T_EDITION"]:
        if n in ["CATALOG_MAIN"]:
            return "publication_transposition", "hub", "Catalogue officiel des normes publiées par l'ETSI"
        elif n in ["TRANSPOSITION"]:
            return "publication_transposition", "tx", "Transposition des normes européennes (EN) par les organismes nationaux (NSOs)"
        elif n in ["CATALOG_TITLE", "CATALOG_INDEX"]:
            return "publication_transposition", "child", f"Détails et indexation catalogue: {name}"
        elif n == "ARTICLE":
            return "publication_transposition", "tx", "Articles et chapitres normatifs publiés"
        return "publication_transposition", "child", f"Données de publication: {name}"

    # 5. Schedules & Milestones
    if n in ["SCHEDULE", "PROTOTYPE", "WP_PROCEDURE"] or n.startswith("EVENT"):
        if n == "SCHEDULE":
            return "schedules", "hub", "Échéancier complet des jalons de production des normes (> 520 000 jalons)"
        elif n == "WP_PROCEDURE":
            return "schedules", "master", "Procédures d'approbation et de vote (AP, PE, MV, OAP)"
        elif n == "PROTOTYPE":
            return "schedules", "child", "Gabarits d'échéancier par catégorie de norme"
        elif n.startswith("EVENT"):
            return "schedules", "tx", f"Événements du cycle de production: {name}"
        return "schedules", "child", f"Données de planning: {name}"

    # 6. Work Items
    if n.startswith("WKI") or n in ["WORK_ITEM", "SUPERSEDE", "SUPPORTING_MEMBERS", "OTHER_STANDARD"]:
        if n == "WORK_ITEM":
            return "work_items", "hub", "Spécifications techniques, rapports et normes (TS, TR, EN, ES, GS)"
        elif n in ["SUPERSEDE"]:
            return "work_items", "join", "Remplacement, révision et succession des normes"
        elif n in ["WKI_CROSS_REF"]:
            return "work_items", "join", "Références croisées et dépendances entre normes"
        elif n in ["SUPPORTING_MEMBERS"]:
            return "work_items", "child", "Membres ETSI soutenant officiellement la création du Work Item"
        elif n in ["WKI_KEYWORD", "WKI_CLUSTER", "WKI_PROJECT", "WKI_FREQUENCY"]:
            return "work_items", "join", f"Indexation et catégorisation thématique: {name}"
        elif n in ["WKI_REMARK", "WKI_MEMO", "WKI_ASPECTS"]:
            return "work_items", "child", f"Observations et contenu technique: {name}"
        return "work_items", "child", f"Détail du Work Item: {name}"

    # 7. Referentials & Nomenclatures
    if n.startswith("TAB_") or n.startswith("WP_") or n.startswith("APP") or n in ["APPLICATION", "COMMON_FIELD"]:
        if n == "TAB_MILESTONE_CODE":
            desc = "Codes des jalons procéduraux (TB Approval, Vote, Publication)"
        elif n == "TAB_ACTION_TYPE":
            desc = "Types d'actions de normalisation"
        elif n == "TAB_STD_TYPE":
            desc = "Types de normes (TS, TR, EN, ES, EG, GS)"
        elif n == "TAB_STD_STATUS":
            desc = "Statuts du cycle de vie des normes"
        elif n == "TAB_CLUSTER":
            desc = "Thématiques et clusters technologiques"
        elif n == "WP_KEYWORD":
            desc = "Thésaurus des mots-clés normatifs"
        else:
            desc = f"Nomenclature de référence: {name}"
        return "referentials", "master", desc

    return "referentials", role_guess or "master", f"Table de référence WPMDB: {name}"

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

print("Updated super-er-diagram.config.yaml for WPMDB with 7 domains, roles, and French descriptions.")
