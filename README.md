# ETSI WPMDB — Data Model & Interactive ER Diagram

Modèle de données complet et visualiseur relationnel interactif à deux couches pour la base de données **WPMDB** (*Work Programme Management Database*) d'ETSI, généré à l'aide de **`super-er-diagram`**.

🌐 **Visualiseur en ligne** : [https://tnm.etsi.org/WPMDB_scheme/](https://tnm.etsi.org/WPMDB_scheme/)

---

## 📊 Métriques du Schéma

* **Tables analysées** : 113 tables
* **Relations de clés étrangères (FK)** : 64
* **Domaines métier modélisés** : 7
* **Moteur de base de données source** : Microsoft SQL Server (172.27.2.40)
* **Système de visualisation** : Canvas SVG interactif + Panneau d'inspection détaillée

---

## 🏛️ Les 7 Domaines Métier

1. **`work_items` — Normes & Spécifications (Bleu `#2563eb`)** : Livrables techniques (TS, TR, EN, ES, GS), historique de succession (`Supersede`), références croisées inter-normes, mots-clés et membres de soutien.
   * *Tables clés* : `WORK_ITEM`, `Supersede`, `WKI_CROSS_REF`, `SUPPORTING_MEMBERS`, `WKI_KEYWORD`, `WKI_CLUSTER`, `WKI_PROJECT`, `WKI_REMARK`, `WKI_MEMO`.
2. **`schedules` — Jalons & Cycle de Production (Vert `#059669`)** : Calendrier des étapes de normalisation (> 520 000 jalons), gabarits procéduraux (`PROTOTYPE`) et procédures de vote (`WP_PROCEDURE`).
   * *Tables clés* : `SCHEDULE`, `WP_PROCEDURE`, `PROTOTYPE`, `work_item.Event`.
3. **`mandates_legislation` — Mandats CE & Réglementation (Ambre `#d97706`)** : Mandats de standardisation de la Commission Européenne (Standardisation Requests) et Directives / Règlements européens (RED, EMC, LVD, CRA...).
   * *Tables clés* : `mandate.Mandate`, `mandate.Requested_Deliverable`, `mandate.Requested_Deliverable_WorkItem`, `legislation.Legislation`, `legislation.Legislations_Mandates`, `WKI_DIRECTIVE`.
4. **`publication_transposition` — Catalogue & Transposition NSO (Violet `#7c3aed`)** : Publications officielles du catalogue ETSI et transposition nationale par les organismes nationaux (AFNOR, DIN, BSI, etc.).
   * *Tables clés* : `Catalog_Main`, `Catalog_TITLE`, `CATALOG_INDEX`, `TRANSPOSITION`, `ARTICLE`.
5. **`stf_projects` — Équipes Spéciales d'Experts (Cyan `#0891b2`)** : Projets financés Special Task Forces (STF), plannings des experts et frais de déplacement.
   * *Tables clés* : `STF_WORK_ITEM`, `STF_SCHEDULE`, `STF_TRAVEL`, `STF_REFERENCE_TRAVEL`.
6. **`referentials` — Référentiels & Nomenclatures (Gris `#4b5563`)** : Typologies de standards, codes de jalons, actions et thésaurus.
   * *Tables clés* : `TAB_STD_TYPE`, `TAB_STD_STATUS`, `TAB_MILESTONE_CODE`, `TAB_ACTION_TYPE`, `TAB_CLUSTER`, `WP_KEYWORD`.
7. **`audit_history` — Historique & Archivage (Ardoise `#64748b`)** : Tables historiques et logs d'archivage.

---

## 🚀 Utilisation Locale

### Lancement direct
* Sous Windows : Double-cliquez sur `Lancer_Modele_WPMDB.bat`
* Ou ouvrez directement `viewer/index.html` dans votre navigateur.

### Via serveur local HTTP
```bash
cd viewer
python -m http.server 8086
```
Accédez ensuite à [http://localhost:8086](http://localhost:8086).
