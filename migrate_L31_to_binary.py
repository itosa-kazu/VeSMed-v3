#!/usr/bin/env python3
"""
Migrate L31 (CT_abdomen) from single 12-state variable to 10 binary variables (L31a-L31j).
Rationale: CT findings are non-exclusive; binary variables allow multi-select.

Updates step1, step2, step3 in one atomic operation.
CPT values are human-set based on literature (PMC/RadioGraphics/StatPearls).
"""
import json, copy

STEP1 = "step1_fever_v2.7.json"
STEP2 = "step2_fever_edges_v4.json"
STEP3 = "step3_fever_cpts_v2.json"

# ══════════════════════════════════════════════
# 10 new binary variables replacing L31
# ══════════════════════════════════════════════
NEW_VARS = [
    {"id": "L31a", "name": "CT_abd_abscess",            "name_ja": "腹部CT: 膿瘍",         "category": "lab", "states": ["absent", "present"]},
    {"id": "L31b", "name": "CT_abd_mass",                "name_ja": "腹部CT: 腫瘤",         "category": "lab", "states": ["absent", "present"]},
    {"id": "L31c", "name": "CT_abd_bowel_wall_thickening","name_ja": "腹部CT: 腸管壁肥厚",   "category": "lab", "states": ["absent", "present"]},
    {"id": "L31d", "name": "CT_abd_free_air",            "name_ja": "腹部CT: 遊離ガス",     "category": "lab", "states": ["absent", "present"]},
    {"id": "L31e", "name": "CT_abd_organ_infarction",    "name_ja": "腹部CT: 臓器梗塞",     "category": "lab", "states": ["absent", "present"]},
    {"id": "L31f", "name": "CT_abd_hepatosplenomegaly",  "name_ja": "腹部CT: 肝脾腫大",     "category": "lab", "states": ["absent", "present"]},
    {"id": "L31g", "name": "CT_abd_lymphadenopathy",     "name_ja": "腹部CT: リンパ節腫大",  "category": "lab", "states": ["absent", "present"]},
    {"id": "L31h", "name": "CT_abd_biliary_dilatation",  "name_ja": "腹部CT: 胆管拡張",     "category": "lab", "states": ["absent", "present"]},
    {"id": "L31i", "name": "CT_abd_pancreatitis",        "name_ja": "腹部CT: 膵炎像",       "category": "lab", "states": ["absent", "present"]},
    {"id": "L31j", "name": "CT_abd_ascites",             "name_ja": "腹部CT: 腹水",         "category": "lab", "states": ["absent", "present"]},
]

# ══════════════════════════════════════════════
# Edge definitions: (from_disease, to_var, from_name, to_name, reason)
# ══════════════════════════════════════════════
NEW_EDGES = [
    # --- L31a: abscess ---
    ("D30",  "L31a", "psoas_abscess",             "CT_abd_abscess", "腸腰筋膿瘍: CTで膿瘍像(感度90%+)"),
    ("D10",  "L31a", "appendicitis",              "CT_abd_abscess", "穿孔性虫垂炎: CT膿瘍像(~15%に合併)"),
    ("D27",  "L31a", "diverticulitis",            "CT_abd_abscess", "憩室炎合併膿瘍(~20%のHinchey II以上)"),
    ("D39",  "L31a", "perianal_abscess",          "CT_abd_abscess", "肛門周囲膿瘍: CT描出"),
    ("D119", "L31a", "perinephric_abscess",       "CT_abd_abscess", "腎周囲膿瘍: CTゴールドスタンダード"),
    ("D29",  "L31a", "pyogenic_liver_abscess",    "CT_abd_abscess", "化膿性肝膿瘍: CT感度95%+(多発が多い)"),
    ("D362", "L31a", "amebic_liver_abscess",      "CT_abd_abscess", "アメーバ性肝膿瘍: CT右葉単発大膿瘍(感度~95%)"),

    # --- L31b: mass ---
    ("D69",  "L31b", "renal_cell_carcinoma",      "CT_abd_mass", "腎細胞癌: CT腎腫瘤(感度90%+)"),
    ("D70",  "L31b", "hepatocellular_carcinoma",  "CT_abd_mass", "肝細胞癌: CT造影で典型的wash-in/wash-out"),
    ("D230", "L31b", "pancreatic_cancer",         "CT_abd_mass", "膵癌: CT低吸収域腫瘤(感度~90%)"),
    ("D231", "L31b", "cholangiocarcinoma",        "CT_abd_mass", "胆管癌: CT腫瘤性病変(~50%)"),
    ("D238", "L31b", "colorectal_cancer",         "CT_abd_mass", "大腸癌: CT壁肥厚/腫瘤像"),
    ("D247", "L31b", "gastric_cancer",            "CT_abd_mass", "胃癌: CT壁肥厚/腫瘤(進行癌)"),
    ("D287", "L31b", "gallbladder_cancer",        "CT_abd_mass", "胆嚢癌: CT胆嚢腫瘤/壁肥厚"),
    ("D92",  "L31b", "tumor_fever",               "CT_abd_mass", "腫瘍熱: CT原発巣/転移巣腫瘤"),
    ("D67",  "L31b", "non_hodgkin_lymphoma",      "CT_abd_mass", "NHL: 腹腔内腫瘤(~25%)"),

    # --- L31c: bowel wall thickening ---
    ("D10",  "L31c", "appendicitis",              "CT_abd_bowel_wall_thickening", "虫垂炎: CT虫垂腫大+壁肥厚+脂肪浸潤(感度95%)"),
    ("D27",  "L31c", "diverticulitis",            "CT_abd_bowel_wall_thickening", "憩室炎: CT結腸壁肥厚+脂肪浸潤(感度94%)"),
    ("D63",  "L31c", "crohns_disease",            "CT_abd_bowel_wall_thickening", "クローン病: CT腸管壁肥厚(mural stratification)"),
    ("D353", "L31c", "ulcerative_colitis",        "CT_abd_bowel_wall_thickening", "UC: CT結腸壁肥厚(連続性)"),
    ("D177", "L31c", "ischemic_colitis",          "CT_abd_bowel_wall_thickening", "虚血性腸炎: CT壁肥厚+thumbprinting"),
    ("D137", "L31c", "acute_mesenteric_ischemia", "CT_abd_bowel_wall_thickening", "腸間膜虚血: CT腸管壁肥厚(後期所見)"),
    ("D238", "L31c", "colorectal_cancer",         "CT_abd_bowel_wall_thickening", "大腸癌: CT非対称性壁肥厚"),
    ("D247", "L31c", "gastric_cancer",            "CT_abd_bowel_wall_thickening", "胃癌: CT胃壁肥厚"),

    # --- L31d: free air ---
    ("D136", "L31d", "peptic_ulcer_perforation",  "CT_abd_free_air", "消化管穿孔: CT遊離ガス(感度95%+)"),
    ("D27",  "L31d", "diverticulitis",            "CT_abd_free_air", "憩室炎穿孔: CT遊離ガス(~8%に合併)"),
    ("D10",  "L31d", "appendicitis",              "CT_abd_free_air", "穿孔性虫垂炎: CT遊離ガス(~5%)"),

    # --- L31e: organ infarction ---
    ("D187", "L31e", "splenic_infarction",        "CT_abd_organ_infarction", "脾梗塞: CT楔状低吸収域(感度90%+)"),
    ("D137", "L31e", "acute_mesenteric_ischemia", "CT_abd_organ_infarction", "腸間膜虚血: CT臓器虚血像/門脈ガス"),

    # --- L31f: hepatosplenomegaly ---
    ("D18",  "L31f", "infectious_mononucleosis",  "CT_abd_hepatosplenomegaly", "EBV: 脾腫50%+(脾破裂リスク)"),
    ("D15",  "L31f", "malaria",                   "CT_abd_hepatosplenomegaly", "マラリア: 脾腫60-80%"),
    ("D16",  "L31f", "dengue",                    "CT_abd_hepatosplenomegaly", "デング熱: 肝脾腫大~30%"),
    ("D45",  "L31f", "CMV_infection",             "CT_abd_hepatosplenomegaly", "CMV: 脾腫~35%"),
    ("D107", "L31f", "hemophagocytic_lymphohistiocytosis", "CT_abd_hepatosplenomegaly", "HLH: 肝脾腫大(診断基準、75%+)"),
    ("D67",  "L31f", "non_hodgkin_lymphoma",      "CT_abd_hepatosplenomegaly", "NHL: 脾腫~45%"),
    ("D354", "L31f", "hodgkin_lymphoma",          "CT_abd_hepatosplenomegaly", "HL: 脾腫30-40%"),
    ("D68",  "L31f", "acute_myeloid_leukemia",    "CT_abd_hepatosplenomegaly", "AML: 肝脾腫大~40%"),
    ("D375", "L31f", "acute_lymphoblastic_leukemia","CT_abd_hepatosplenomegaly", "ALL: 肝脾腫大~45%"),
    ("D209", "L31f", "myelofibrosis",             "CT_abd_hepatosplenomegaly", "骨髄線維症: 巨脾(hallmark、85%+)"),
    ("D234", "L31f", "CML",                       "CT_abd_hepatosplenomegaly", "CML: 脾腫75%"),
    ("D235", "L31f", "CLL",                       "CT_abd_hepatosplenomegaly", "CLL: 脾腫~50%"),
    ("D224", "L31f", "ATLL",                      "CT_abd_hepatosplenomegaly", "ATLL: 肝脾腫大~45%"),
    ("D28",  "L31f", "typhoid_fever",             "CT_abd_hepatosplenomegaly", "腸チフス: 肝脾腫大~40%"),
    ("D113", "L31f", "disseminated_histoplasmosis","CT_abd_hepatosplenomegaly", "播種性ヒストプラズマ: 肝脾腫大55%"),
    ("D58",  "L31f", "adult_onset_still",         "CT_abd_hepatosplenomegaly", "成人Still病: 肝脾腫大40-50%"),
    ("D251", "L31f", "decompensated_cirrhosis",   "CT_abd_hepatosplenomegaly", "非代償性肝硬変: 門脈圧亢進による脾腫"),
    ("D44",  "L31f", "acute_HIV",                 "CT_abd_hepatosplenomegaly", "HIV: 脾腫~30%"),
    ("D97",  "L31f", "castleman_disease",         "CT_abd_hepatosplenomegaly", "キャッスルマン: 多中心型で肝脾腫大~40%"),
    ("D187", "L31f", "splenic_infarction",        "CT_abd_hepatosplenomegaly", "脾梗塞: 背景の脾腫(塞栓源)~15%"),

    # --- L31g: lymphadenopathy ---
    ("D67",  "L31g", "non_hodgkin_lymphoma",      "CT_abd_lymphadenopathy", "NHL: 腹腔内リンパ節腫大~65%"),
    ("D354", "L31g", "hodgkin_lymphoma",          "CT_abd_lymphadenopathy", "HL: 腹腔内リンパ節腫大~55%"),
    ("D17",  "L31g", "pulmonary_tuberculosis",    "CT_abd_lymphadenopathy", "結核: 腹腔内リンパ節腫大(腹部TB)~30%"),
    ("D62",  "L31g", "sarcoidosis",               "CT_abd_lymphadenopathy", "サルコイドーシス: 腹腔リンパ節腫大~30%"),
    ("D44",  "L31g", "acute_HIV",                 "CT_abd_lymphadenopathy", "HIV: 全身リンパ節腫大~35%"),
    ("D235", "L31g", "CLL",                       "CT_abd_lymphadenopathy", "CLL: リンパ節腫大(hallmark)~50%"),
    ("D224", "L31g", "ATLL",                      "CT_abd_lymphadenopathy", "ATLL: リンパ節腫大~50%"),
    ("D97",  "L31g", "castleman_disease",         "CT_abd_lymphadenopathy", "キャッスルマン: リンパ節腫大(定義的特徴)~55%"),
    ("D94",  "L31g", "IgG4_related",              "CT_abd_lymphadenopathy", "IgG4: リンパ節腫大~30%"),
    ("D113", "L31g", "disseminated_histoplasmosis","CT_abd_lymphadenopathy", "播種性ヒストプラズマ: 腹腔リンパ節腫大~35%"),
    ("D69",  "L31g", "renal_cell_carcinoma",      "CT_abd_lymphadenopathy", "RCC: 後腹膜リンパ節転移~15%"),

    # --- L31h: biliary dilatation ---
    ("D25",  "L31h", "acute_cholangitis",         "CT_abd_biliary_dilatation", "急性胆管炎: 胆管拡張73-100%(PMC3474110)"),
    ("D11",  "L31h", "cholecystitis",             "CT_abd_biliary_dilatation", "急性胆嚢炎: CBD拡張(総胆管結石合併時~15%)"),
    ("D231", "L31h", "cholangiocarcinoma",        "CT_abd_biliary_dilatation", "胆管癌: 胆管拡張(hallmark、75%)"),
    ("D230", "L31h", "pancreatic_cancer",         "CT_abd_biliary_dilatation", "膵頭部癌: CBD拡張(double duct sign)~45%"),
    ("D287", "L31h", "gallbladder_cancer",        "CT_abd_biliary_dilatation", "胆嚢癌: 胆管浸潤による拡張~40%"),
    ("D229", "L31h", "autoimmune_pancreatitis",   "CT_abd_biliary_dilatation", "自己免疫性膵炎: 胆管狭窄/拡張~15%"),
    ("D94",  "L31h", "IgG4_related",              "CT_abd_biliary_dilatation", "IgG4関連硬化性胆管炎~25%"),

    # --- L31i: pancreatitis ---
    ("D86",  "L31i", "acute_pancreatitis",        "CT_abd_pancreatitis", "急性膵炎: CT膵腫大+脂肪浸潤(感度~80%)"),
    ("D229", "L31i", "autoimmune_pancreatitis",   "CT_abd_pancreatitis", "自己免疫性膵炎: CTびまん性膵腫大(sausage pancreas)~70%"),
    ("D94",  "L31i", "IgG4_related",              "CT_abd_pancreatitis", "IgG4関連膵炎: CT膵腫大~30%"),
    ("D230", "L31i", "pancreatic_cancer",         "CT_abd_pancreatitis", "膵癌: 閉塞性膵炎(上流膵管拡張)~20%"),

    # --- L31j: ascites ---
    ("D81",  "L31j", "spontaneous_bacterial_peritonitis", "CT_abd_ascites", "SBP: 腹水(前提条件、95%+)"),
    ("D251", "L31j", "decompensated_cirrhosis",   "CT_abd_ascites", "非代償性肝硬変: 腹水75%+"),
    ("D136", "L31j", "peptic_ulcer_perforation",  "CT_abd_ascites", "消化管穿孔: 遊離腹水(腹膜炎)~30%"),
    ("D120", "L31j", "acute_heart_failure",       "CT_abd_ascites", "急性心不全: 腹水(右心不全)~25%"),
    ("D151", "L31j", "acute_liver_failure",       "CT_abd_ascites", "急性肝不全: 腹水~35%"),
    ("D92",  "L31j", "tumor_fever",               "CT_abd_ascites", "腫瘍熱: 癌性腹膜炎~15%"),
    ("D86",  "L31j", "acute_pancreatitis",        "CT_abd_ascites", "急性膵炎: 膵周囲液貯留/腹水(中等症以上)~25%"),
]

# ══════════════════════════════════════════════
# CPT definitions for each new variable
# Format: {var_id: {"leak_present": float, "parents": {disease_id: p_present}}}
# ══════════════════════════════════════════════
NEW_CPTS = {
    "L31a": {
        "description": "腹部CT: 膿瘍",
        "leak_present": 0.02,
        "parents": {
            "D30":  0.85,  # psoas abscess
            "D10":  0.15,  # appendicitis (perforated)
            "D27":  0.20,  # diverticulitis (complicated)
            "D39":  0.80,  # perianal abscess
            "D119": 0.85,  # perinephric abscess
            "D29":  0.86,  # pyogenic liver abscess
            "D362": 0.89,  # amebic liver abscess
        }
    },
    "L31b": {
        "description": "腹部CT: 腫瘤",
        "leak_present": 0.03,
        "parents": {
            "D69":  0.85,  # RCC
            "D70":  0.80,  # HCC
            "D230": 0.75,  # pancreatic cancer
            "D231": 0.50,  # cholangiocarcinoma
            "D238": 0.60,  # colorectal cancer
            "D247": 0.55,  # gastric cancer
            "D287": 0.65,  # gallbladder cancer
            "D92":  0.50,  # tumor fever
            "D67":  0.25,  # NHL
        }
    },
    "L31c": {
        "description": "腹部CT: 腸管壁肥厚",
        "leak_present": 0.05,
        "parents": {
            "D10":  0.75,  # appendicitis
            "D27":  0.70,  # diverticulitis
            "D63":  0.80,  # Crohn's
            "D353": 0.70,  # UC
            "D177": 0.65,  # ischemic colitis
            "D137": 0.50,  # mesenteric ischemia
            "D238": 0.40,  # colorectal cancer
            "D247": 0.40,  # gastric cancer
        }
    },
    "L31d": {
        "description": "腹部CT: 遊離ガス",
        "leak_present": 0.01,
        "parents": {
            "D136": 0.85,  # peptic ulcer perforation
            "D27":  0.08,  # diverticulitis perforation
            "D10":  0.05,  # perforated appendicitis
        }
    },
    "L31e": {
        "description": "腹部CT: 臓器梗塞",
        "leak_present": 0.01,
        "parents": {
            "D187": 0.85,  # splenic infarction
            "D137": 0.40,  # mesenteric ischemia
        }
    },
    "L31f": {
        "description": "腹部CT: 肝脾腫大",
        "leak_present": 0.06,
        "parents": {
            "D18":  0.50,  # EBV
            "D15":  0.60,  # malaria
            "D16":  0.30,  # dengue
            "D45":  0.35,  # CMV
            "D107": 0.75,  # HLH
            "D67":  0.45,  # NHL
            "D354": 0.35,  # HL
            "D68":  0.40,  # AML
            "D375": 0.45,  # ALL
            "D209": 0.85,  # myelofibrosis
            "D234": 0.75,  # CML
            "D235": 0.50,  # CLL
            "D224": 0.45,  # ATLL
            "D28":  0.40,  # typhoid
            "D113": 0.55,  # histoplasmosis
            "D58":  0.40,  # adult Still
            "D251": 0.60,  # decompensated cirrhosis
            "D44":  0.30,  # HIV
            "D97":  0.40,  # Castleman
            "D187": 0.15,  # splenic infarction (background)
        }
    },
    "L31g": {
        "description": "腹部CT: リンパ節腫大",
        "leak_present": 0.04,
        "parents": {
            "D67":  0.65,  # NHL
            "D354": 0.55,  # HL
            "D17":  0.30,  # TB
            "D62":  0.30,  # sarcoidosis
            "D44":  0.35,  # HIV
            "D235": 0.50,  # CLL
            "D224": 0.50,  # ATLL
            "D97":  0.55,  # Castleman
            "D94":  0.30,  # IgG4
            "D113": 0.35,  # histoplasmosis
            "D69":  0.15,  # RCC (retroperitoneal)
        }
    },
    "L31h": {
        "description": "腹部CT: 胆管拡張",
        "leak_present": 0.02,
        "parents": {
            "D25":  0.80,  # cholangitis
            "D11":  0.15,  # cholecystitis
            "D231": 0.75,  # cholangiocarcinoma
            "D230": 0.45,  # pancreatic cancer (head)
            "D287": 0.40,  # gallbladder cancer
            "D229": 0.15,  # autoimmune pancreatitis
            "D94":  0.25,  # IgG4-related
        }
    },
    "L31i": {
        "description": "腹部CT: 膵炎像",
        "leak_present": 0.01,
        "parents": {
            "D86":  0.80,  # acute pancreatitis
            "D229": 0.70,  # autoimmune pancreatitis
            "D94":  0.30,  # IgG4-related
            "D230": 0.20,  # pancreatic cancer (obstructive)
        }
    },
    "L31j": {
        "description": "腹部CT: 腹水",
        "leak_present": 0.03,
        "parents": {
            "D81":  0.95,  # SBP
            "D251": 0.75,  # decompensated cirrhosis
            "D136": 0.30,  # perforation (peritonitis)
            "D120": 0.25,  # heart failure
            "D151": 0.35,  # acute liver failure
            "D92":  0.15,  # tumor fever (malignant ascites)
            "D86":  0.25,  # pancreatitis (peripancreatic fluid)
        }
    },
}

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  Saved {path}")

def main():
    step1 = load_json(STEP1)
    step2 = load_json(STEP2)
    step3 = load_json(STEP3)

    # ── Step 1: Replace L31 with 10 binary variables ──
    idx = None
    for i, v in enumerate(step1["variables"]):
        if v["id"] == "L31":
            idx = i
            break
    if idx is None:
        print("ERROR: L31 not found in step1")
        return
    old_var = step1["variables"][idx]
    print(f"  Removing L31 ({old_var.get('name')}) from step1, inserting {len(NEW_VARS)} binary variables")
    step1["variables"] = step1["variables"][:idx] + NEW_VARS + step1["variables"][idx+1:]

    # ── Step 2: Remove old L31 edges, add new edges ──
    old_count = len(step2["edges"])
    step2["edges"] = [e for e in step2["edges"] if e.get("to") != "L31"]
    removed = old_count - len(step2["edges"])
    print(f"  Removed {removed} old L31 edges from step2")

    for (from_id, to_id, from_name, to_name, reason) in NEW_EDGES:
        step2["edges"].append({
            "from": from_id,
            "to": to_id,
            "from_name": from_name,
            "to_name": to_name,
            "reason": reason,
        })
    print(f"  Added {len(NEW_EDGES)} new edges to step2")

    # ── Step 3: Remove old L31 CPT, add 10 new CPTs ──
    if "L31" in step3["noisy_or_params"]:
        del step3["noisy_or_params"]["L31"]
        print("  Removed old L31 CPT from step3")

    for var_id, cpt_def in NEW_CPTS.items():
        leak_p = cpt_def["leak_present"]
        entry = {
            "description": cpt_def["description"],
            "states": ["absent", "present"],
            "leak": {
                "absent": round(1.0 - leak_p, 4),
                "present": leak_p,
            },
            "parent_effects": {},
        }
        for disease_id, p_present in cpt_def["parents"].items():
            entry["parent_effects"][disease_id] = {
                "absent": round(1.0 - p_present, 4),
                "present": p_present,
            }
        step3["noisy_or_params"][var_id] = entry

    print(f"  Added {len(NEW_CPTS)} new CPT entries to step3")

    # ── Save all ──
    save_json(STEP1, step1)
    save_json(STEP2, step2)
    save_json(STEP3, step3)

    # ── Summary ──
    total_new_edges = len(NEW_EDGES)
    total_diseases = set()
    for e in NEW_EDGES:
        total_diseases.add(e[0])
    print(f"\n=== Migration Summary ===")
    print(f"  Old: 1 variable (L31, 12 states), {removed} edges")
    print(f"  New: {len(NEW_VARS)} binary variables, {total_new_edges} edges across {len(total_diseases)} diseases")
    print(f"  Variables: step1 now has {len(step1['variables'])} variables")
    print(f"  Edges: step2 now has {len(step2['edges'])} edges")

if __name__ == "__main__":
    main()
