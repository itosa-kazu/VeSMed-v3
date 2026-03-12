#!/usr/bin/env python3
"""
audit_edges.py - Systematic audit of Bayesian Network edges for fever differential diagnosis.

Loads step1 (variables), step2 (edges), and step3 (CPTs) to compare
expected vs actual disease-variable connections based on medical knowledge.

For each disease, defines which variables it SHOULD connect to (>5-10% frequency),
then flags missing edges and missing CPTs.
"""

import json
import sys
from pathlib import Path
from collections import defaultdict

# ---------------------------------------------------------------------------
# 1. EXPECTED_EDGES dictionary
#    Maps disease_id -> list of variable_ids that the disease should connect to.
#    Based on medical textbook knowledge, including symptoms seen in >5-10% of cases.
#    Edges FROM risk factors TO diseases are also included (listed under the disease).
#    Disease-to-disease edges (e.g. D08->D09) are included where relevant.
# ---------------------------------------------------------------------------

EXPECTED_EDGES = {
    # ===== D01: ウイルス性上気道炎 (Viral URI / Common cold) =====
    "D01": [
        "T01", "T02",           # fever duration (short), onset (gradual)
        "S01",                  # cough (mild)
        "S02",                  # sore throat
        "S03",                  # nasal symptoms (rhinorrhea - cardinal)
        "S05",                  # headache (mild)
        "S06",                  # myalgia (mild)
        "S07",                  # fatigue (mild)
        "S46",                  # anorexia (common)
        "E01",                  # temperature (low-grade)
        "E08",                  # pharyngeal exam (erythema)
        "L01",                  # WBC (normal or low)
        "L02",                  # CRP (normal or mildly elevated)
        "R11",                  # close contact
        "R19",                  # season (winter)
        "D20",                  # can progress to sinusitis
    ],

    # ===== D02: インフルエンザ (Influenza) =====
    "D02": [
        "T01", "T02",           # fever duration, sudden onset
        "S01",                  # cough (dry, prominent)
        "S02",                  # sore throat
        "S05",                  # headache (prominent)
        "S06",                  # myalgia (prominent, characteristic)
        "S07",                  # fatigue (severe)
        "S09",                  # rigors/chills
        "S46",                  # anorexia
        "E01",                  # temperature (high, >39)
        "E02",                  # heart rate (tachycardia)
        "L01",                  # WBC (normal or low)
        "L02",                  # CRP (mild-moderate)
        "L06",                  # rapid influenza test
        "R05",                  # immunosuppressed (severity)
        "R11",                  # close contact / outbreak
        "R17",                  # influenza vaccine
        "R19",                  # season (winter)
    ],

    # ===== D03: COVID-19 =====
    "D03": [
        "T01", "T02",           # fever duration (5-14d), onset (1-2d)
        "S01",                  # cough (dry)
        "S02",                  # sore throat
        "S04",                  # dyspnea (Day 5-7, key)
        "S05",                  # headache
        "S06",                  # myalgia
        "S07",                  # fatigue (prominent)
        "S09",                  # rigors
        "S14",                  # diarrhea (10-20%)
        "S19",                  # taste/smell disorder (characteristic)
        "S21",                  # chest pain (if pneumonia)
        "S46",                  # anorexia
        "E01",                  # temperature
        "E04",                  # respiratory rate (tachypnea in severe)
        "E05",                  # SpO2 (key for severity)
        "L01",                  # WBC (lymphopenia)
        "L02",                  # CRP
        "L04",                  # chest X-ray (bilateral infiltrate/GGO)
        "L08",                  # COVID antigen test
        "L14",                  # peripheral blood (lymphopenia)
        "L20",                  # D-dimer (elevated in severe)
        "R05",                  # immunosuppressed
        "R11",                  # close contact
        "R18",                  # COVID vaccine
    ],

    # ===== D04: 急性咽頭扁桃炎 (Acute pharyngotonsillitis) =====
    "D04": [
        "T01",                  # fever duration (3-5d)
        "T02",                  # onset speed (acute)
        "S02",                  # sore throat (main symptom)
        "S05",                  # headache
        "S07",                  # fatigue
        "S09",                  # rigors (with high fever)
        "S13",                  # nausea/vomiting (in children/young adults with strep)
        "S46",                  # anorexia
        "E01",                  # temperature (high)
        "E08",                  # pharyngeal exam (exudate, key)
        "E13",                  # lymphadenopathy (cervical, key)
        "L01",                  # WBC (elevated in bacterial)
        "L02",                  # CRP
        "L07",                  # rapid strep test
        "R01",                  # age (young)
        "R11",                  # close contact
    ],

    # ===== D05: 市中肺炎 (Community-acquired pneumonia) =====
    "D05": [
        "T01", "T02",           # fever duration, onset speed
        "S01",                  # cough (productive, key)
        "S04",                  # dyspnea (key)
        "S06",                  # myalgia
        "S07",                  # fatigue
        "S09",                  # rigors (bacterial pneumonia)
        "S21",                  # chest pain (pleuritic)
        "S46",                  # anorexia
        "E01",                  # temperature (high)
        "E04",                  # respiratory rate (tachypnea, key)
        "E05",                  # SpO2 (hypoxia)
        "E07",                  # lung auscultation (crackles, key)
        "L01",                  # WBC (elevated)
        "L02",                  # CRP (high)
        "L03",                  # procalcitonin (elevated in bacterial)
        "L04",                  # chest X-ray (infiltrate, key)
        "L09",                  # blood culture
        "L14",                  # peripheral blood (left shift)
        "L28",                  # ESR
        "R01",                  # age (elderly)
        "R03",                  # smoking
        "R04",                  # diabetes
        "R05",                  # immunosuppressed
        "R07",                  # recent hospitalization
        "R16",                  # heavy alcohol
        "R37",                  # aspiration risk
    ],

    # ===== D06: 急性気管支炎 (Acute bronchitis) =====
    "D06": [
        "T01",                  # fever duration (short, 3-5d)
        "T02",                  # onset speed
        "S01",                  # cough (main symptom, prolonged 1-3 weeks)
        "S02",                  # sore throat (sometimes)
        "S07",                  # fatigue
        "E01",                  # temperature (low-grade)
        "E07",                  # lung auscultation (wheezes/rhonchi)
        "L01",                  # WBC (usually normal)
        "L02",                  # CRP (mildly elevated)
        "R03",                  # smoking
    ],

    # ===== D07: 急性胃腸炎 (Acute gastroenteritis) =====
    "D07": [
        "T01", "T02",           # fever duration (short), onset (sudden)
        "S12",                  # abdominal pain (diffuse/epigastric)
        "S13",                  # nausea/vomiting (key)
        "S14",                  # diarrhea (key)
        "S07",                  # fatigue
        "S06",                  # myalgia (viral GE)
        "S46",                  # anorexia
        "E01",                  # temperature (low to moderate)
        "E09",                  # abdominal exam (tenderness)
        "L01",                  # WBC
        "L02",                  # CRP
        "R19",                  # season (norovirus=winter, bacterial=summer)
    ],

    # ===== D08: 膀胱炎 (Lower UTI / Cystitis) =====
    "D08": [
        "S10",                  # dysuria (key)
        "S11",                  # urinary frequency (key)
        "S12",                  # abdominal pain (suprapubic)
        "S33",                  # hematuria (common)
        "E01",                  # temperature (usually afebrile or low-grade)
        "L05",                  # urinalysis (pyuria/bacteriuria, key)
        "L02",                  # CRP (mild)
        "R02",                  # sex (female)
        "R04",                  # diabetes
        "R13",                  # urinary catheter
        "R15",                  # pregnancy
        "D09",                  # can progress to pyelonephritis
    ],

    # ===== D09: 急性腎盂腎炎 (Acute pyelonephritis) =====
    "D09": [
        "T01",                  # fever duration
        "S09",                  # rigors (bacteremia)
        "S10",                  # dysuria
        "S11",                  # urinary frequency
        "S12",                  # abdominal pain
        "S13",                  # nausea/vomiting
        "S15",                  # flank pain (key)
        "E01",                  # temperature (high)
        "E02",                  # heart rate
        "E11",                  # CVA tenderness (key)
        "L01",                  # WBC (elevated)
        "L02",                  # CRP (high)
        "L03",                  # procalcitonin
        "L05",                  # urinalysis (key)
        "L09",                  # blood culture
        "R02",                  # sex (female)
        "R04",                  # diabetes
        "R07",                  # recent hospitalization
        "R13",                  # urinary catheter
        "R15",                  # pregnancy
        "D08",                  # from lower UTI (ascending)
    ],

    # ===== D10: 急性虫垂炎 (Appendicitis) =====
    "D10": [
        "T01",                  # fever duration
        "S12",                  # abdominal pain (RLQ, key - migration from epigastric)
        "S13",                  # nausea/vomiting (key)
        "S46",                  # anorexia (key - almost always present)
        "E01",                  # temperature (low-grade initially)
        "E09",                  # abdominal exam (tenderness -> peritoneal signs)
        "L01",                  # WBC (elevated, key)
        "L02",                  # CRP (elevated)
        "L12",                  # abdominal ultrasound
        "L31",                  # abdominal CT
        "R01",                  # age (10-30s)
    ],

    # ===== D11: 急性胆嚢炎 (Cholecystitis) =====
    "D11": [
        "T01",                  # fever duration
        "S12",                  # abdominal pain (RUQ, key)
        "S13",                  # nausea/vomiting (key)
        "S46",                  # anorexia
        "E01",                  # temperature
        "E09",                  # abdominal exam (RUQ tenderness)
        "E10",                  # Murphy sign (key)
        "L01",                  # WBC (elevated)
        "L02",                  # CRP (elevated)
        "L11",                  # liver enzymes (mild elevation)
        "L12",                  # abdominal ultrasound (gallbladder wall thickening, key)
        "R01",                  # age (elderly)
        "R12",                  # gallstone history (key)
    ],

    # ===== D12: 蜂窩織炎 (Cellulitis) =====
    "D12": [
        "T01",                  # fever duration
        "S18",                  # skin complaint (localized pain/redness, key)
        "S09",                  # rigors (if bacteremia)
        "E01",                  # temperature
        "E02",                  # heart rate
        "E12",                  # skin exam (localized erythema/warmth/swelling, key)
        "E13",                  # lymphadenopathy (regional)
        "L01",                  # WBC (elevated)
        "L02",                  # CRP (elevated)
        "L09",                  # blood culture (if severe)
        "R04",                  # diabetes
        "R05",                  # immunosuppressed
        "R09",                  # IV drug use
        "R14",                  # skin wound/trauma (key)
    ],

    # ===== D13: 髄膜炎 (Meningitis) =====
    "D13": [
        "T01",                  # fever duration
        "T02",                  # onset speed (sudden in bacterial)
        "S05",                  # headache (severe, key)
        "S09",                  # rigors
        "S13",                  # nausea/vomiting (ICP elevation)
        "S42",                  # seizure
        "E01",                  # temperature (high)
        "E02",                  # heart rate
        "E03",                  # blood pressure (may be low in sepsis)
        "E06",                  # neck stiffness (key)
        "E12",                  # skin exam (petechiae/purpura in meningococcal)
        "E16",                  # consciousness (confused/obtunded, key)
        "L01",                  # WBC (very elevated in bacterial)
        "L02",                  # CRP (very high in bacterial)
        "L03",                  # procalcitonin (very high in bacterial)
        "L09",                  # blood culture
        "L14",                  # peripheral blood
        "L45",                  # CSF analysis (key)
        "R01",                  # age
        "R05",                  # immunosuppressed
    ],

    # ===== D14: 感染性心内膜炎 (Infective endocarditis) =====
    "D14": [
        "T01", "T02", "T03",   # duration (weeks), onset (insidious), pattern (intermittent)
        "S05",                  # headache (embolic)
        "S07",                  # fatigue (chronic)
        "S08",                  # arthralgia
        "S09",                  # rigors (bacteremia)
        "S16",                  # night sweats
        "S17",                  # weight loss
        "S33",                  # hematuria (embolic glomerulonephritis)
        "S46",                  # anorexia
        "E01",                  # temperature
        "E02",                  # heart rate
        "E12",                  # skin exam (Osler nodes, Janeway lesions, splinter hemorrhages)
        "E14",                  # splenomegaly
        "E15",                  # heart murmur (new, key)
        "E16",                  # consciousness (embolic stroke)
        "L01",                  # WBC
        "L02",                  # CRP (elevated)
        "L03",                  # procalcitonin
        "L09",                  # blood culture (key - 3 sets)
        "L14",                  # peripheral blood
        "L28",                  # ESR (elevated)
        "R09",                  # IV drug use (key)
        "R10",                  # prosthetic valve/device (key)
    ],

    # ===== D15: マラリア (Malaria) =====
    "D15": [
        "T01", "T02", "T03",   # duration, onset (acute), pattern (periodic, key)
        "S05",                  # headache
        "S06",                  # myalgia
        "S07",                  # fatigue
        "S09",                  # rigors (severe, characteristic)
        "S13",                  # nausea/vomiting
        "S14",                  # diarrhea (sometimes)
        "S46",                  # anorexia
        "E01",                  # temperature (very high, periodic)
        "E02",                  # heart rate
        "E03",                  # blood pressure (in severe)
        "E14",                  # splenomegaly (key)
        "E16",                  # consciousness (cerebral malaria)
        "E18",                  # jaundice (hemolysis)
        "L01",                  # WBC (normal or low)
        "L02",                  # CRP
        "L10",                  # malaria smear (key)
        "L11",                  # liver enzymes
        "L14",                  # peripheral blood (thrombocytopenia, key)
        "R06",                  # travel to tropical area (essential)
    ],

    # ===== D16: デング熱 (Dengue) =====
    "D16": [
        "T01",                  # fever duration
        "T02",                  # onset speed (sudden)
        "S05",                  # headache (retro-orbital, key)
        "S06",                  # myalgia (severe, breakbone fever)
        "S07",                  # fatigue
        "S08",                  # arthralgia (prominent)
        "S09",                  # rigors
        "S14",                  # diarrhea (sometimes)
        "S18",                  # skin complaint (rash)
        "S26",                  # bloody stool (in severe DHF)
        "S44",                  # bleeding tendency (in severe)
        "E01",                  # temperature (high)
        "E12",                  # skin exam (maculopapular rash)
        "L01",                  # WBC (leukopenia, key)
        "L02",                  # CRP
        "L11",                  # liver enzymes (elevated)
        "L14",                  # peripheral blood (thrombocytopenia, key)
        "R06",                  # travel (essential)
        "R19",                  # season (summer)
    ],

    # ===== D17: 肺結核 (Pulmonary tuberculosis) =====
    "D17": [
        "T01", "T02",           # duration (weeks-months), onset (insidious)
        "S01",                  # cough (chronic, key)
        "S04",                  # dyspnea (advanced)
        "S07",                  # fatigue (chronic)
        "S16",                  # night sweats (key)
        "S17",                  # weight loss (key)
        "S34",                  # hemoptysis
        "S46",                  # anorexia
        "E01",                  # temperature (low-grade, afternoon)
        "E05",                  # SpO2 (advanced)
        "L01",                  # WBC
        "L02",                  # CRP
        "L04",                  # chest X-ray (upper lobe infiltrate, cavity)
        "L14",                  # peripheral blood
        "L28",                  # ESR (elevated)
        "L35",                  # chest CT (cavity, key)
        "R05",                  # immunosuppressed
        "R11",                  # close contact with TB
        "R16",                  # heavy alcohol
        "R25",                  # HIV
    ],

    # ===== D18: 伝染性単核球症 (Infectious mononucleosis) =====
    "D18": [
        "T01",                  # fever duration (1-2 weeks)
        "T02",                  # onset speed (gradual to acute)
        "S02",                  # sore throat (severe, key)
        "S07",                  # fatigue (prolonged, key)
        "S08",                  # arthralgia
        "S46",                  # anorexia
        "E01",                  # temperature
        "E08",                  # pharyngeal exam (exudate)
        "E12",                  # skin exam (maculopapular rash, especially with amoxicillin)
        "E13",                  # lymphadenopathy (generalized, key)
        "E14",                  # splenomegaly (key)
        "E34",                  # hepatomegaly
        "L01",                  # WBC (lymphocytosis)
        "L02",                  # CRP
        "L11",                  # liver enzymes (elevated, key)
        "L13",                  # heterophile antibody (key)
        "L14",                  # peripheral blood (atypical lymphocytes, key)
        "R01",                  # age (young, 10-20s)
    ],

    # ===== D19: 薬剤熱 (Drug fever) =====
    "D19": [
        "T01", "T03",           # duration, pattern (persistent but "relatively well")
        "S07",                  # fatigue (paradoxically mild)
        "S18",                  # skin complaint (drug rash in some)
        "E01",                  # temperature
        "E02",                  # heart rate (relative bradycardia)
        "E12",                  # skin exam (rash)
        "L01",                  # WBC
        "L02",                  # CRP (mildly elevated)
        "L14",                  # peripheral blood (eosinophilia, key)
        "L28",                  # ESR
        "R08",                  # new medication (key, essential)
    ],

    # ===== D20: 急性副鼻腔炎 (Acute sinusitis) =====
    "D20": [
        "T01",                  # fever duration
        "S03",                  # nasal symptoms (purulent rhinorrhea, key)
        "S05",                  # headache (frontal)
        "S20",                  # facial pain/pressure (key)
        "S01",                  # cough (post-nasal drip)
        "E01",                  # temperature (low-grade)
        "L01",                  # WBC
        "L02",                  # CRP (mild)
        "D01",                  # follows viral URI
    ],

    # ===== D21: 帯状疱疹 (Herpes zoster) =====
    "D21": [
        "T01",                  # fever duration
        "S05",                  # headache (if cranial)
        "S07",                  # fatigue
        "S18",                  # skin complaint (unilateral pain -> vesicles, key)
        "E01",                  # temperature
        "E12",                  # skin exam (vesicular dermatomal, key)
        "E13",                  # lymphadenopathy (regional)
        "L01",                  # WBC
        "L02",                  # CRP (mild)
        "R01",                  # age (elderly)
        "R05",                  # immunosuppressed
    ],

    # ===== D22: 急性前立腺炎 (Acute prostatitis) =====
    "D22": [
        "T01",                  # fever duration
        "S09",                  # rigors
        "S10",                  # dysuria (key)
        "S11",                  # urinary frequency (key)
        "S15",                  # flank/perineal pain
        "E01",                  # temperature (high)
        "E02",                  # heart rate
        "L01",                  # WBC (elevated)
        "L02",                  # CRP (elevated)
        "L05",                  # urinalysis
        "L09",                  # blood culture
        "R02",                  # sex (male only)
        "R13",                  # urinary catheter
    ],

    # ===== D23: リケッチア症 (Rickettsial disease) =====
    "D23": [
        "T01",                  # fever duration
        "T02",                  # onset speed (acute)
        "S05",                  # headache
        "S06",                  # myalgia
        "S07",                  # fatigue
        "S08",                  # arthralgia
        "S09",                  # rigors
        "S18",                  # skin complaint (rash)
        "E01",                  # temperature (high)
        "E02",                  # heart rate
        "E12",                  # skin exam (maculopapular rash, key)
        "E16",                  # consciousness (severe)
        "E17",                  # eschar (key - tick bite)
        "E18",                  # jaundice (severe)
        "L01",                  # WBC
        "L02",                  # CRP (high)
        "L11",                  # liver enzymes (elevated)
        "L14",                  # peripheral blood (thrombocytopenia)
        "R06",                  # travel
        "R19",                  # season (autumn)
    ],

    # ===== D24: TSS (Toxic shock syndrome) =====
    "D24": [
        "T01", "T02",           # duration, onset (fulminant)
        "S06",                  # myalgia (severe)
        "S09",                  # rigors
        "S13",                  # nausea/vomiting
        "S14",                  # diarrhea (watery)
        "S18",                  # skin complaint (diffuse erythroderma, key)
        "E01",                  # temperature (very high)
        "E02",                  # heart rate (tachycardia)
        "E03",                  # blood pressure (hypotension, key)
        "E12",                  # skin exam (diffuse erythroderma, key)
        "E16",                  # consciousness (confusion)
        "L01",                  # WBC
        "L02",                  # CRP
        "L03",                  # procalcitonin
        "L09",                  # blood culture
        "L11",                  # liver enzymes (multi-organ)
        "R14",                  # skin wound
        "R20",                  # tampon (S. aureus TSS)
    ],

    # ===== D25: 急性胆管炎 (Acute cholangitis) =====
    "D25": [
        "T01",                  # fever duration
        "S09",                  # rigors (Charcot triad, key)
        "S12",                  # abdominal pain (RUQ, Charcot triad)
        "S13",                  # nausea/vomiting
        "E01",                  # temperature (high, Charcot triad)
        "E02",                  # heart rate
        "E03",                  # blood pressure (Reynolds pentad)
        "E09",                  # abdominal exam (RUQ tenderness)
        "E16",                  # consciousness (Reynolds pentad)
        "E18",                  # jaundice (Charcot triad, key)
        "L01",                  # WBC (very elevated)
        "L02",                  # CRP (very high)
        "L03",                  # procalcitonin
        "L09",                  # blood culture
        "L11",                  # liver enzymes (elevated, key)
        "L12",                  # abdominal ultrasound (bile duct dilation)
        "R12",                  # gallstone history (key)
    ],

    # ===== D26: PID (Pelvic inflammatory disease) =====
    "D26": [
        "T01",                  # fever duration
        "S12",                  # abdominal pain (lower, suprapubic/bilateral, key)
        "S13",                  # nausea/vomiting (if severe)
        "S46",                  # anorexia
        "E01",                  # temperature
        "E09",                  # abdominal exam (lower tenderness)
        "L01",                  # WBC (elevated)
        "L02",                  # CRP (elevated)
        "R01",                  # age (young women)
        "R02",                  # sex (female only)
        "R36",                  # high-risk sexual behavior
    ],

    # ===== D27: 憩室炎 (Diverticulitis) =====
    "D27": [
        "T01",                  # fever duration
        "S12",                  # abdominal pain (LLQ, key)
        "S13",                  # nausea/vomiting
        "S14",                  # diarrhea or constipation (change in bowel habit)
        "E01",                  # temperature
        "E09",                  # abdominal exam (LLQ tenderness, key)
        "L01",                  # WBC (elevated)
        "L02",                  # CRP (elevated)
        "L31",                  # abdominal CT (key for diagnosis)
        "R01",                  # age (elderly)
    ],

    # ===== D28: 腸チフス (Typhoid fever) =====
    "D28": [
        "T01", "T03",           # duration (1-3w), pattern (stepwise continuous)
        "T02",                  # onset speed (gradual)
        "S05",                  # headache
        "S07",                  # fatigue
        "S12",                  # abdominal pain
        "S13",                  # nausea (constipation more common initially)
        "S14",                  # diarrhea (or constipation)
        "S46",                  # anorexia
        "E01",                  # temperature (stepwise, key)
        "E02",                  # heart rate (relative bradycardia, key)
        "E12",                  # skin exam (rose spots)
        "E14",                  # splenomegaly (key)
        "E18",                  # jaundice (sometimes)
        "L01",                  # WBC (leukopenia, key)
        "L02",                  # CRP
        "L09",                  # blood culture (key)
        "L11",                  # liver enzymes (elevated)
        "R06",                  # travel (South/Southeast Asia, key)
    ],

    # ===== D29: 肝膿瘍 (Liver abscess) =====
    "D29": [
        "T01",                  # fever duration
        "S09",                  # rigors
        "S12",                  # abdominal pain (RUQ)
        "S07",                  # fatigue
        "S46",                  # anorexia
        "E01",                  # temperature (high, spiking)
        "E18",                  # jaundice
        "E34",                  # hepatomegaly (key)
        "L01",                  # WBC (very elevated)
        "L02",                  # CRP (very high)
        "L09",                  # blood culture
        "L11",                  # liver enzymes (elevated, especially ALP)
        "L31",                  # abdominal CT (key)
        "R04",                  # diabetes
        "R06",                  # travel (amoebic)
    ],

    # ===== D30: 腸腰筋膿瘍 (Psoas abscess) =====
    "D30": [
        "T01",                  # fever duration
        "S09",                  # rigors
        "S15",                  # flank pain / back pain
        "S22",                  # back pain (key)
        "S28",                  # hip pain (key - pain with hip extension)
        "E01",                  # temperature
        "E27",                  # psoas sign (key)
        "L01",                  # WBC (elevated)
        "L02",                  # CRP (elevated)
        "L09",                  # blood culture
        "L28",                  # ESR
        "L31",                  # abdominal CT (key)
        "R04",                  # diabetes
    ],

    # ===== D31: 化膿性脊椎炎 (Vertebral osteomyelitis) =====
    "D31": [
        "T01",                  # fever duration (weeks)
        "S09",                  # rigors
        "S22",                  # back pain (key - persistent even at rest)
        "E01",                  # temperature
        "L01",                  # WBC
        "L02",                  # CRP (elevated)
        "L09",                  # blood culture (50-70% positive)
        "L28",                  # ESR (very elevated, key)
        "R04",                  # diabetes
        "R09",                  # IV drug use
    ],

    # ===== D32: 化膿性関節炎 (Septic arthritis) =====
    "D32": [
        "T01",                  # fever duration
        "S08",                  # arthralgia
        "S09",                  # rigors
        "S23",                  # joint swelling (monoarticular, key)
        "S28",                  # hip pain (if hip involved)
        "E01",                  # temperature (high)
        "E21",                  # joint redness/warmth (key)
        "L01",                  # WBC (elevated)
        "L02",                  # CRP (very high)
        "L09",                  # blood culture
        "L28",                  # ESR
        "L30",                  # joint fluid analysis (key - WBC>50000)
        "R01",                  # age
        "R04",                  # diabetes
        "R42",                  # prosthetic joint
    ],

    # ===== D33: 扁桃周囲膿瘍 (Peritonsillar abscess) =====
    "D33": [
        "T01",                  # fever duration
        "S02",                  # sore throat (severe, key)
        "S24",                  # trismus (key)
        "S25",                  # dysphagia (key)
        "E01",                  # temperature (high)
        "E08",                  # pharyngeal exam (unilateral swelling, key)
        "E13",                  # lymphadenopathy (cervical)
        "E22",                  # uvula deviation (key)
        "E31",                  # drooling
        "L01",                  # WBC (elevated)
        "L02",                  # CRP (elevated)
    ],

    # ===== D34: 深頸部感染症 (Deep neck infection) =====
    "D34": [
        "T01",                  # fever duration
        "S02",                  # sore throat
        "S04",                  # dyspnea (airway compromise)
        "S24",                  # trismus
        "S25",                  # dysphagia (key)
        "E01",                  # temperature (high)
        "E23",                  # neck swelling (key)
        "E31",                  # drooling
        "L01",                  # WBC (very elevated)
        "L02",                  # CRP (very high)
        "L31",                  # CT (abscess)
    ],

    # ===== D35: 肺膿瘍 (Lung abscess) =====
    "D35": [
        "T01",                  # fever duration (weeks)
        "S01",                  # cough (productive, foul sputum, key)
        "S04",                  # dyspnea
        "S07",                  # fatigue
        "S09",                  # rigors
        "S17",                  # weight loss (key)
        "S34",                  # hemoptysis
        "S46",                  # anorexia
        "E01",                  # temperature (spiking)
        "L01",                  # WBC (very elevated)
        "L02",                  # CRP (very high)
        "L04",                  # chest X-ray (cavity with air-fluid level)
        "L35",                  # chest CT (key)
        "R16",                  # heavy alcohol (aspiration risk)
        "R37",                  # aspiration risk (key)
    ],

    # ===== D36: 膿胸 (Empyema) =====
    "D36": [
        "T01",                  # fever duration
        "S01",                  # cough
        "S04",                  # dyspnea (key)
        "S21",                  # chest pain (pleuritic, key)
        "S09",                  # rigors
        "E01",                  # temperature (high)
        "E05",                  # SpO2
        "E07",                  # lung auscultation (decreased breath sounds)
        "L01",                  # WBC (very elevated)
        "L02",                  # CRP (very high)
        "L04",                  # chest X-ray (pleural effusion, key)
    ],

    # ===== D37: 細菌性腸炎 (Bacterial enteritis) =====
    "D37": [
        "T01",                  # fever duration
        "S09",                  # rigors
        "S12",                  # abdominal pain
        "S13",                  # nausea/vomiting
        "S14",                  # diarrhea (bloody, key)
        "S26",                  # bloody stool (key)
        "E01",                  # temperature (higher than viral GE)
        "E09",                  # abdominal exam (tenderness)
        "L01",                  # WBC (elevated)
        "L02",                  # CRP (elevated)
        "L34",                  # stool culture (key)
    ],

    # ===== D38: C. difficile感染症 =====
    "D38": [
        "T01",                  # fever duration
        "S12",                  # abdominal pain
        "S13",                  # nausea
        "S14",                  # diarrhea (watery, profuse, key)
        "E01",                  # temperature
        "E09",                  # abdominal exam (tenderness)
        "L01",                  # WBC (very elevated, key)
        "L02",                  # CRP
        "L34",                  # CD toxin test (key)
        "R07",                  # recent hospitalization (key)
        "R14",                  # recent antibiotics (mapped to R14 here, actually R08 more appropriate)
    ],

    # ===== D39: 肛門周囲膿瘍 (Perianal abscess) =====
    "D39": [
        "S12",                  # abdominal/perineal pain
        "S18",                  # skin complaint (localized)
        "E01",                  # temperature
        "L01",                  # WBC
        "L02",                  # CRP
        "R04",                  # diabetes
        "R35",                  # IBD history
    ],

    # ===== D40: カテーテル関連血流感染 (CRBSI) =====
    "D40": [
        "T01",                  # fever duration
        "S09",                  # rigors (key - with line flushing)
        "E01",                  # temperature (spiking)
        "E12",                  # skin exam (insertion site erythema)
        "L01",                  # WBC (elevated)
        "L02",                  # CRP (elevated)
        "L09",                  # blood culture (key)
        "R22",                  # central venous catheter (key)
        "R23",                  # neutropenia
    ],

    # ===== D41: 手術部位感染 (SSI) =====
    "D41": [
        "T01",                  # fever duration
        "S18",                  # skin complaint (wound area)
        "E01",                  # temperature
        "E12",                  # skin exam (wound erythema/drainage, key)
        "L01",                  # WBC
        "L02",                  # CRP
        "R04",                  # diabetes
        "R21",                  # recent surgery (key)
    ],

    # ===== D42: 複雑性尿路感染症 (Complicated UTI) =====
    "D42": [
        "T01",                  # fever duration
        "S09",                  # rigors
        "S10",                  # dysuria (key)
        "S11",                  # urinary frequency (key)
        "S15",                  # flank pain
        "E01",                  # temperature
        "L01",                  # WBC
        "L02",                  # CRP
        "L05",                  # urinalysis (key)
        "L09",                  # blood culture
        "R01",                  # age (elderly)
        "R04",                  # diabetes
        "R13",                  # urinary catheter (key)
    ],

    # ===== D43: 精巣上体炎 (Epididymitis) =====
    "D43": [
        "S10",                  # dysuria
        "S38",                  # scrotal swelling/pain (key)
        "E01",                  # temperature
        "L01",                  # WBC
        "L02",                  # CRP
        "L05",                  # urinalysis
        "R02",                  # sex (male)
        "R36",                  # high-risk sexual (STD in young)
    ],

    # ===== D44: 急性HIV (Acute HIV infection) =====
    "D44": [
        "T01",                  # fever duration (2-4 weeks)
        "S02",                  # sore throat
        "S05",                  # headache
        "S06",                  # myalgia
        "S07",                  # fatigue
        "S08",                  # arthralgia
        "S14",                  # diarrhea
        "S18",                  # skin complaint (rash)
        "S29",                  # oral ulcers
        "E01",                  # temperature
        "E12",                  # skin exam (maculopapular rash)
        "E13",                  # lymphadenopathy (generalized, key)
        "L01",                  # WBC (lymphopenia initially, then lymphocytosis)
        "L14",                  # peripheral blood
        "L33",                  # HIV test (key)
        "R36",                  # high-risk sexual behavior (key)
    ],

    # ===== D45: CMV感染症 (CMV infection) =====
    "D45": [
        "T01",                  # fever duration (prolonged)
        "S07",                  # fatigue (key)
        "E01",                  # temperature
        "E13",                  # lymphadenopathy
        "E14",                  # splenomegaly
        "E34",                  # hepatomegaly
        "L01",                  # WBC (lymphocytosis)
        "L11",                  # liver enzymes (elevated)
        "L14",                  # peripheral blood (atypical lymphocytes)
        "R25",                  # HIV/immunosuppressed (key)
    ],

    # ===== D46: 麻疹 (Measles) =====
    "D46": [
        "T01",                  # fever duration
        "S01",                  # cough (key, 3Cs: cough/coryza/conjunctivitis)
        "S03",                  # nasal symptoms (coryza)
        "S18",                  # skin complaint (rash, key)
        "E01",                  # temperature (very high)
        "E12",                  # skin exam (maculopapular, starts on face, spreads down)
        "E25",                  # conjunctival injection (key)
        "E26",                  # Koplik spots (pathognomonic)
        "L01",                  # WBC (lymphopenia)
        "R43",                  # vaccination (MMR, key)
    ],

    # ===== D47: ムンプス (Mumps) =====
    "D47": [
        "T01",                  # fever duration
        "S05",                  # headache
        "S25",                  # dysphagia
        "E01",                  # temperature
        "E24",                  # parotid swelling (key, bilateral)
        "L01",                  # WBC
        "L36",                  # amylase (elevated, key)
        "R43",                  # vaccination (MMR)
    ],

    # ===== D48: 風疹 (Rubella) =====
    "D48": [
        "T01",                  # fever duration (short)
        "S08",                  # arthralgia (in adults)
        "S18",                  # skin complaint (rash)
        "E01",                  # temperature (low-grade)
        "E12",                  # skin exam (maculopapular rash, starts on face)
        "E13",                  # lymphadenopathy (posterior auricular/cervical, key)
        "L01",                  # WBC (lymphopenia)
        "L02",                  # CRP
        "R43",                  # vaccination (MMR)
    ],

    # ===== D49: カンジダ血症 (Candidemia) =====
    "D49": [
        "T01",                  # fever duration
        "S09",                  # rigors
        "E01",                  # temperature (persistent despite antibiotics)
        "E12",                  # skin exam (endophthalmitis, skin lesions)
        "L01",                  # WBC
        "L02",                  # CRP
        "L09",                  # blood culture (key)
        "L27",                  # beta-D-glucan (key)
        "R22",                  # central venous catheter (key)
        "R23",                  # neutropenia (key)
    ],

    # ===== D50: PCP (Pneumocystis pneumonia) =====
    "D50": [
        "T01",                  # fever duration (weeks)
        "S01",                  # cough (dry, key)
        "S04",                  # dyspnea (progressive, key)
        "S07",                  # fatigue
        "S17",                  # weight loss
        "S46",                  # anorexia
        "E01",                  # temperature
        "E04",                  # respiratory rate
        "E05",                  # SpO2 (hypoxia, key)
        "L02",                  # CRP
        "L04",                  # chest X-ray (bilateral interstitial)
        "L16",                  # LDH (elevated, key)
        "L27",                  # beta-D-glucan (elevated, key)
        "L35",                  # chest CT (GGO, key)
        "R25",                  # HIV (key)
        "R29",                  # steroid chronic
    ],

    # ===== D51: アメーバ赤痢 (Amebiasis) =====
    "D51": [
        "T01",                  # fever duration
        "S12",                  # abdominal pain (RLQ)
        "S13",                  # nausea
        "S14",                  # diarrhea (bloody/mucoid, key)
        "S26",                  # bloody stool (key)
        "E01",                  # temperature
        "L01",                  # WBC
        "L02",                  # CRP
        "R06",                  # travel (key)
    ],

    # ===== D52: レプトスピラ症 (Leptospirosis) =====
    "D52": [
        "T01",                  # fever duration
        "T03",                  # fever pattern (biphasic)
        "S05",                  # headache (severe)
        "S06",                  # myalgia (calf pain, key)
        "S09",                  # rigors
        "E01",                  # temperature (high)
        "E18",                  # jaundice (Weil disease)
        "E25",                  # conjunctival injection (key, suffusion)
        "L01",                  # WBC
        "L02",                  # CRP
        "L11",                  # liver enzymes
        "L14",                  # peripheral blood (thrombocytopenia)
        "R31",                  # contaminated water (key)
    ],

    # ===== D53: ブルセラ症 (Brucellosis) =====
    "D53": [
        "T01", "T03",           # duration (weeks-months), pattern (undulant)
        "S01",                  # cough (sometimes)
        "S05",                  # headache
        "S06",                  # myalgia
        "S07",                  # fatigue
        "S08",                  # arthralgia (key)
        "S09",                  # rigors
        "S16",                  # night sweats (key, undulant fever)
        "S17",                  # weight loss
        "S22",                  # back pain (sacroiliac)
        "S46",                  # anorexia
        "E01",                  # temperature
        "E13",                  # lymphadenopathy
        "E14",                  # splenomegaly (key)
        "E34",                  # hepatomegaly
        "L01",                  # WBC (normal or low)
        "L02",                  # CRP
        "L09",                  # blood culture (key, prolonged incubation)
        "L11",                  # liver enzymes
        "L28",                  # ESR
        "R30",                  # animal contact (livestock, key)
    ],

    # ===== D54: 猫ひっかき病 (Cat scratch disease) =====
    "D54": [
        "T01",                  # fever duration (weeks)
        "S07",                  # fatigue
        "S46",                  # anorexia
        "E01",                  # temperature (low-grade)
        "E13",                  # lymphadenopathy (regional, key)
        "L01",                  # WBC
        "L02",                  # CRP (mild)
        "R30",                  # animal contact (cat, key)
    ],

    # ===== D55: Q熱 (Q fever) =====
    "D55": [
        "T01",                  # fever duration
        "S01",                  # cough
        "S05",                  # headache (severe)
        "S06",                  # myalgia
        "S07",                  # fatigue
        "S09",                  # rigors
        "E01",                  # temperature (high)
        "E34",                  # hepatomegaly
        "L02",                  # CRP
        "L04",                  # chest X-ray (atypical pneumonia)
        "L11",                  # liver enzymes (elevated, key)
        "R30",                  # animal contact (livestock/cat, key)
    ],

    # ===== D56: 百日咳 (Pertussis) =====
    "D56": [
        "T01",                  # fever duration (initially)
        "S01",                  # cough (persistent, worsening)
        "S13",                  # nausea/vomiting (post-tussive)
        "S32",                  # paroxysmal cough (key - characteristic)
        "E01",                  # temperature (usually afebrile in paroxysmal phase)
        "L01",                  # WBC (lymphocytosis, key)
        "L02",                  # CRP
    ],

    # ===== D57: 壊死性筋膜炎 (Necrotizing fasciitis) =====
    "D57": [
        "T01",                  # fever duration
        "S06",                  # myalgia (disproportionate pain, key)
        "S09",                  # rigors
        "S18",                  # skin complaint (pain out of proportion)
        "E01",                  # temperature (high)
        "E02",                  # heart rate (tachycardia)
        "E03",                  # blood pressure (hypotension/shock)
        "E12",                  # skin exam (erythema -> necrosis, key)
        "E16",                  # consciousness
        "L01",                  # WBC (very elevated or very low)
        "L02",                  # CRP (very high)
        "L03",                  # procalcitonin
        "L09",                  # blood culture
        "L17",                  # CK (elevated, key)
        "R04",                  # diabetes
        "R14",                  # skin wound
    ],

    # ===== D58: 成人Still病 (Adult-onset Still disease) =====
    "D58": [
        "T01", "T03",           # duration (weeks), pattern (quotidian/double quotidian)
        "S02",                  # sore throat (key - non-exudative)
        "S06",                  # myalgia
        "S07",                  # fatigue
        "S08",                  # arthralgia (polyarthralgia, key)
        "S23",                  # joint swelling
        "S46",                  # anorexia
        "E01",                  # temperature (spiking, key - salmon rash with fever)
        "E12",                  # skin exam (salmon-colored evanescent rash, key)
        "E13",                  # lymphadenopathy
        "E14",                  # splenomegaly
        "E34",                  # hepatomegaly
        "L01",                  # WBC (neutrophilic leukocytosis)
        "L02",                  # CRP (very high)
        "L11",                  # liver enzymes
        "L15",                  # ferritin (very high >1000, key)
        "L28",                  # ESR
    ],

    # ===== D59: SLE (Systemic lupus erythematosus) =====
    "D59": [
        "T01",                  # fever duration
        "S07",                  # fatigue (key)
        "S08",                  # arthralgia (key)
        "S23",                  # joint swelling
        "S18",                  # skin complaint (rash)
        "S29",                  # oral ulcers
        "S30",                  # photosensitivity
        "S33",                  # hematuria (lupus nephritis)
        "S34",                  # hemoptysis (alveolar hemorrhage, rare but important)
        "E01",                  # temperature
        "E12",                  # skin exam (malar rash, discoid)
        "E13",                  # lymphadenopathy
        "E20",                  # butterfly rash (key)
        "L01",                  # WBC (low)
        "L02",                  # CRP
        "L14",                  # peripheral blood
        "L15",                  # ferritin
        "L18",                  # ANA (key)
        "L22",                  # pancytopenia
        "L28",                  # ESR (elevated)
        "R02",                  # sex (female, 9:1)
    ],

    # ===== D60: ANCA関連血管炎 (ANCA vasculitis) =====
    "D60": [
        "T01",                  # fever duration (weeks-months)
        "S01",                  # cough (pulmonary involvement)
        "S07",                  # fatigue
        "S17",                  # weight loss
        "S33",                  # hematuria (glomerulonephritis, key)
        "S34",                  # hemoptysis (alveolar hemorrhage)
        "E01",                  # temperature
        "E12",                  # skin exam (purpura, ulcers)
        "L01",                  # WBC
        "L02",                  # CRP (elevated)
        "L04",                  # chest X-ray (infiltrates, nodules)
        "L19",                  # ANCA (key)
        "L28",                  # ESR (very elevated)
    ],

    # ===== D61: PMR/GCA (Polymyalgia rheumatica / Giant cell arteritis) =====
    "D61": [
        "T01",                  # fever duration
        "S05",                  # headache (temporal, key for GCA)
        "S06",                  # myalgia (proximal, key for PMR)
        "S07",                  # fatigue
        "S17",                  # weight loss
        "S27",                  # morning stiffness (>30min, key for PMR)
        "S46",                  # anorexia
        "E01",                  # temperature
        "L01",                  # WBC
        "L02",                  # CRP (very elevated, key)
        "L28",                  # ESR (very elevated, >50-100, key)
        "R01",                  # age (>50, key)
    ],

    # ===== D62: サルコイドーシス (Sarcoidosis) =====
    "D62": [
        "T01",                  # fever duration
        "S01",                  # cough (dry)
        "S04",                  # dyspnea
        "S07",                  # fatigue (key)
        "S08",                  # arthralgia (Lofgren syndrome)
        "S17",                  # weight loss
        "S31",                  # dry eyes/mouth
        "S46",                  # anorexia
        "E01",                  # temperature
        "E12",                  # skin exam (erythema nodosum)
        "E13",                  # lymphadenopathy (bilateral hilar)
        "E35",                  # eye findings (uveitis, key)
        "L02",                  # CRP
        "L04",                  # chest X-ray (BHL, key)
        "L22",                  # pancytopenia (sometimes)
        "L24",                  # ACE (elevated, key)
        "L28",                  # ESR
        "L35",                  # chest CT (BHL, key)
    ],

    # ===== D63: IBD (Inflammatory bowel disease) =====
    "D63": [
        "T01",                  # fever duration
        "S07",                  # fatigue
        "S08",                  # arthralgia (extraintestinal)
        "S12",                  # abdominal pain
        "S14",                  # diarrhea (key)
        "S17",                  # weight loss (key)
        "S26",                  # bloody stool (key, especially UC)
        "S29",                  # oral ulcers
        "S46",                  # anorexia
        "E01",                  # temperature
        "E09",                  # abdominal exam
        "E35",                  # eye findings (uveitis/episcleritis)
        "L01",                  # WBC
        "L02",                  # CRP
        "L28",                  # ESR
        "R35",                  # IBD history
    ],

    # ===== D64: 反応性関節炎 (Reactive arthritis) =====
    "D64": [
        "T01",                  # fever duration
        "S08",                  # arthralgia (key, asymmetric large joints)
        "S10",                  # dysuria (urethritis)
        "S23",                  # joint swelling (key)
        "E01",                  # temperature
        "E21",                  # joint redness/warmth
        "E25",                  # conjunctival injection (key - triad with urethritis/arthritis)
        "L02",                  # CRP (elevated)
        "L28",                  # ESR
    ],

    # ===== D65: 痛風/偽痛風 (Gout/Pseudogout) =====
    "D65": [
        "S08",                  # arthralgia (acute, severe)
        "S23",                  # joint swelling (monoarticular, key)
        "E01",                  # temperature
        "E21",                  # joint redness/warmth (key)
        "L01",                  # WBC (sometimes elevated)
        "L02",                  # CRP (elevated)
        "L23",                  # uric acid (elevated in gout)
        "L30",                  # joint fluid (crystals, key)
    ],

    # ===== D66: 家族性地中海熱 (FMF) =====
    "D66": [
        "T01", "T03",           # duration (1-3 days episodes), pattern (periodic, key)
        "S08",                  # arthralgia
        "S12",                  # abdominal pain (serositis)
        "S21",                  # chest pain (pleurisy)
        "E01",                  # temperature (high, brief)
        "L01",                  # WBC (elevated during attacks)
        "L02",                  # CRP (elevated during attacks)
        "L28",                  # ESR
    ],

    # ===== D67: 悪性リンパ腫 (Malignant lymphoma) =====
    "D67": [
        "T01", "T03",           # duration (weeks-months), pattern (Pel-Ebstein)
        "S07",                  # fatigue (key)
        "S16",                  # night sweats (key, B symptom)
        "S17",                  # weight loss (key, B symptom)
        "S46",                  # anorexia
        "E01",                  # temperature (key, B symptom)
        "E13",                  # lymphadenopathy (key)
        "E14",                  # splenomegaly
        "E34",                  # hepatomegaly
        "L01",                  # WBC
        "L02",                  # CRP
        "L04",                  # chest X-ray (mediastinal mass)
        "L15",                  # ferritin
        "L16",                  # LDH (elevated, key)
        "L22",                  # pancytopenia
        "L28",                  # ESR
        "L41",                  # IL-6/sIL-2R (elevated, key)
    ],

    # ===== D68: 急性白血病 (Acute leukemia) =====
    "D68": [
        "T01",                  # fever duration
        "S07",                  # fatigue (key)
        "S44",                  # bleeding tendency (key)
        "S46",                  # anorexia
        "E01",                  # temperature
        "E12",                  # skin exam (petechiae, gingival hypertrophy in AML)
        "E13",                  # lymphadenopathy
        "E14",                  # splenomegaly
        "E34",                  # hepatomegaly
        "L01",                  # WBC (very high or very low)
        "L02",                  # CRP
        "L04",                  # chest X-ray
        "L15",                  # ferritin
        "L16",                  # LDH (elevated)
        "L21",                  # peripheral blood blasts (key)
        "L22",                  # pancytopenia (key)
    ],

    # ===== D69: 腎細胞癌 (Renal cell carcinoma) =====
    "D69": [
        "T01",                  # fever duration (paraneoplastic)
        "S15",                  # flank pain
        "S17",                  # weight loss (key)
        "S33",                  # hematuria (key)
        "E01",                  # temperature
        "L01",                  # WBC (sometimes elevated)
        "L02",                  # CRP (elevated)
        "L04",                  # chest X-ray (metastasis)
        "L28",                  # ESR (elevated)
        "L31",                  # abdominal CT (mass, key)
    ],

    # ===== D70: 肝細胞癌 (Hepatocellular carcinoma) =====
    "D70": [
        "T01",                  # fever duration
        "S07",                  # fatigue
        "S12",                  # abdominal pain (RUQ)
        "S17",                  # weight loss (key)
        "S46",                  # anorexia
        "E01",                  # temperature
        "E18",                  # jaundice
        "E28",                  # ascites
        "E34",                  # hepatomegaly (key)
        "L11",                  # liver enzymes (elevated)
        "L25",                  # AFP (elevated, key)
        "R24",                  # liver cirrhosis (key)
    ],

    # ===== D71: 甲状腺クリーゼ (Thyroid storm) =====
    "D71": [
        "T01",                  # fever duration
        "S14",                  # diarrhea
        "S35",                  # palpitation (key)
        "S36",                  # tremor (key)
        "S45",                  # sweating abnormality (excessive, key)
        "E01",                  # temperature (very high, key)
        "E02",                  # heart rate (very fast, key)
        "E03",                  # blood pressure
        "E16",                  # consciousness (agitation -> coma)
        "E19",                  # thyroid enlargement
        "L32",                  # thyroid function (hyperthyroid, key)
        "R34",                  # thyroid disease history (key)
    ],

    # ===== D72: 副腎クリーゼ (Adrenal crisis) =====
    "D72": [
        "T01",                  # fever duration
        "S07",                  # fatigue (severe)
        "S12",                  # abdominal pain
        "S13",                  # nausea/vomiting (key)
        "E01",                  # temperature
        "E02",                  # heart rate
        "E03",                  # blood pressure (hypotension, key)
        "E16",                  # consciousness
        "L44",                  # electrolytes (hyponatremia, hyperkalemia, key)
        "R29",                  # steroid chronic (sudden withdrawal, key)
    ],

    # ===== D73: 褐色細胞腫 (Pheochromocytoma) =====
    "D73": [
        "S05",                  # headache (paroxysmal, key)
        "S35",                  # palpitation (key)
        "S45",                  # sweating abnormality (excessive, key)
        "E01",                  # temperature
        "E02",                  # heart rate (tachycardia)
        "E03",                  # blood pressure (hypertension, paroxysmal, key)
    ],

    # ===== D74: 悪性症候群 (NMS - Neuroleptic malignant syndrome) =====
    "D74": [
        "T01",                  # fever duration
        "S37",                  # muscle rigidity (lead pipe, key)
        "S45",                  # sweating abnormality
        "S36",                  # tremor
        "E01",                  # temperature (very high, key)
        "E02",                  # heart rate (tachycardia)
        "E03",                  # blood pressure (labile)
        "E16",                  # consciousness (altered, key)
        "L17",                  # CK (very elevated, key)
        "R26",                  # antipsychotic use (key)
    ],

    # ===== D75: セロトニン症候群 (Serotonin syndrome) =====
    "D75": [
        "T01",                  # fever duration
        "S14",                  # diarrhea
        "S36",                  # tremor (key)
        "S37",                  # muscle rigidity (less than NMS)
        "S45",                  # sweating abnormality (excessive)
        "E01",                  # temperature (elevated)
        "E02",                  # heart rate (tachycardia)
        "E16",                  # consciousness (agitation)
        "E30",                  # clonus (key, distinguishes from NMS)
        "L17",                  # CK (mildly elevated)
        "R27",                  # serotonergic drug (key)
    ],

    # ===== D76: 輸血関連発熱 (Transfusion reaction) =====
    "D76": [
        "T01",                  # fever duration (brief)
        "S09",                  # rigors (key)
        "E01",                  # temperature
        "E02",                  # heart rate
        "E03",                  # blood pressure (may drop)
        "L02",                  # CRP
        "R33",                  # blood transfusion (key)
    ],

    # ===== D77: DVT/PE (Deep vein thrombosis / Pulmonary embolism) =====
    "D77": [
        "T01",                  # fever duration
        "T03",                  # fever pattern
        "S04",                  # dyspnea (sudden, key for PE)
        "S21",                  # chest pain (pleuritic, key for PE)
        "S39",                  # unilateral leg swelling (key for DVT)
        "E01",                  # temperature (low-grade)
        "E02",                  # heart rate (tachycardia)
        "E04",                  # respiratory rate
        "E05",                  # SpO2 (hypoxia)
        "L04",                  # chest X-ray
        "L20",                  # D-dimer (elevated, key)
    ],

    # ===== D78: 熱中症 (Heat stroke) =====
    "D78": [
        "T01",                  # fever duration
        "S13",                  # nausea/vomiting
        "S42",                  # seizure
        "S45",                  # sweating abnormality (anhidrosis in classic, key)
        "E01",                  # temperature (very high >40, key)
        "E02",                  # heart rate (tachycardia)
        "E03",                  # blood pressure (hypotension)
        "E16",                  # consciousness (confusion -> coma, key)
        "E29",                  # anhidrosis
        "L17",                  # CK (elevated, rhabdomyolysis)
        "R32",                  # heat exposure (key)
    ],

    # ===== D79: 人工弁心内膜炎 (Prosthetic valve endocarditis) =====
    "D79": [
        "T01",                  # fever duration (weeks)
        "S07",                  # fatigue
        "S09",                  # rigors
        "E01",                  # temperature
        "E15",                  # heart murmur (new or changed, key)
        "L01",                  # WBC
        "L02",                  # CRP
        "L09",                  # blood culture (key)
        "L28",                  # ESR
        "R28",                  # prosthetic valve (key)
    ],

    # ===== D80: 無石胆嚢炎 (Acalculous cholecystitis) =====
    "D80": [
        "S12",                  # abdominal pain (RUQ)
        "S13",                  # nausea/vomiting
        "E01",                  # temperature
        "E09",                  # abdominal exam (RUQ tenderness)
        "E10",                  # Murphy sign
        "L01",                  # WBC (elevated)
        "L02",                  # CRP
        "L12",                  # abdominal ultrasound (gallbladder distension/wall thickening)
        "R07",                  # recent hospitalization/critical illness
    ],

    # ===== D81: SBP (Spontaneous bacterial peritonitis) =====
    "D81": [
        "S12",                  # abdominal pain (diffuse)
        "S13",                  # nausea
        "E01",                  # temperature
        "E02",                  # heart rate
        "E03",                  # blood pressure (hypotension)
        "E09",                  # abdominal exam (diffuse tenderness)
        "E16",                  # consciousness (hepatic encephalopathy)
        "E28",                  # ascites (key - prerequisite)
        "L01",                  # WBC
        "L02",                  # CRP
        "L09",                  # blood culture
        "L29",                  # ascitic fluid (PMN>250, key)
        "R24",                  # liver cirrhosis (key)
    ],

    # ===== D82: 院内髄膜炎 (Nosocomial meningitis) =====
    "D82": [
        "S05",                  # headache (key)
        "S42",                  # seizure
        "E01",                  # temperature
        "E06",                  # neck stiffness (key)
        "E16",                  # consciousness (key)
        "L01",                  # WBC
        "L02",                  # CRP
        "L45",                  # CSF analysis (key)
        "R21",                  # recent surgery (neurosurgery, key)
    ],

    # ===== D83: 侵襲性アスペルギルス症 (Invasive aspergillosis) =====
    "D83": [
        "T01",                  # fever duration
        "S01",                  # cough
        "S04",                  # dyspnea
        "S34",                  # hemoptysis (key)
        "E01",                  # temperature (persistent despite antibiotics)
        "E05",                  # SpO2
        "L01",                  # WBC
        "L02",                  # CRP
        "L04",                  # chest X-ray
        "L26",                  # galactomannan (key)
        "L27",                  # beta-D-glucan
        "L35",                  # chest CT (halo sign, key)
        "R23",                  # neutropenia (key)
        "R29",                  # steroid chronic
    ],

    # ===== D84: 単純ヘルペス脳炎 (Herpes encephalitis) =====
    "D84": [
        "T01",                  # fever duration
        "S05",                  # headache (severe, key)
        "S42",                  # seizure (key, temporal lobe)
        "E01",                  # temperature (high)
        "E06",                  # neck stiffness
        "E16",                  # consciousness (confusion -> coma, key)
        "L01",                  # WBC
        "L45",                  # CSF (HSV PCR positive, key)
        "L46",                  # brain MRI (temporal lobe lesion, key)
    ],

    # ===== D85: 歯原性感染症 (Dental infection / Ludwig angina) =====
    "D85": [
        "S02",                  # sore throat / pain
        "S24",                  # trismus
        "S25",                  # dysphagia
        "S40",                  # facial swelling (key)
        "E01",                  # temperature
        "E23",                  # neck swelling (Ludwig angina)
        "L01",                  # WBC (elevated)
        "L02",                  # CRP
    ],

    # ===== D86: 急性膵炎 (Acute pancreatitis) =====
    "D86": [
        "T01",                  # fever duration
        "S12",                  # abdominal pain (epigastric, radiating to back, key)
        "S13",                  # nausea/vomiting (key)
        "S22",                  # back pain
        "E01",                  # temperature
        "E09",                  # abdominal exam (epigastric tenderness)
        "L01",                  # WBC
        "L02",                  # CRP (prognostic)
        "L11",                  # liver enzymes (if gallstone)
        "L36",                  # amylase/lipase (very high, key)
        "R12",                  # gallstone history
        "R16",                  # heavy alcohol (key)
    ],

    # ===== D87: 亜急性甲状腺炎 (Subacute thyroiditis) =====
    "D87": [
        "T01", "T03",           # duration (weeks), pattern
        "S05",                  # headache
        "S07",                  # fatigue
        "S35",                  # palpitation (thyrotoxic phase)
        "E01",                  # temperature
        "E19",                  # thyroid enlargement
        "E32",                  # thyroid tenderness (key)
        "L01",                  # WBC
        "L02",                  # CRP (elevated)
        "L11",                  # liver enzymes (sometimes)
        "L28",                  # ESR (very elevated, key)
        "L32",                  # thyroid function (initially hyperthyroid, key)
    ],

    # ===== D88: アルコール離脱 (Alcohol withdrawal) =====
    "D88": [
        "T01",                  # fever duration
        "S36",                  # tremor (key)
        "S42",                  # seizure (key)
        "S45",                  # sweating (excessive, key)
        "E01",                  # temperature
        "E02",                  # heart rate (tachycardia)
        "E03",                  # blood pressure (hypertension)
        "E16",                  # consciousness (agitation, delirium, key)
        "L02",                  # CRP
        "R39",                  # heavy alcohol recent cessation (key)
    ],

    # ===== D89: 悪性高熱症 (Malignant hyperthermia) =====
    "D89": [
        "T01",                  # fever duration
        "S37",                  # muscle rigidity (key)
        "S45",                  # sweating
        "E01",                  # temperature (rapidly rising, very high, key)
        "E02",                  # heart rate (tachycardia)
        "E03",                  # blood pressure
        "L17",                  # CK (very elevated, key)
        "R38",                  # general anesthesia (key)
    ],

    # ===== D90: ベーチェット病 (Behcet disease) =====
    "D90": [
        "T01", "T03",           # duration (recurrent), pattern (recurrent)
        "S07",                  # fatigue
        "S29",                  # oral ulcers (key, recurrent)
        "S41",                  # genital ulcers (key)
        "E01",                  # temperature
        "E12",                  # skin exam (erythema nodosum, papulopustular)
        "E35",                  # eye findings (uveitis, key)
        "L02",                  # CRP
        "L28",                  # ESR
    ],

    # ===== D91: チクングニア熱 (Chikungunya) =====
    "D91": [
        "T01",                  # fever duration
        "S05",                  # headache
        "S06",                  # myalgia
        "S08",                  # arthralgia (severe, polyarticular, key)
        "S18",                  # skin complaint (rash)
        "S23",                  # joint swelling
        "E01",                  # temperature (high)
        "E12",                  # skin exam (maculopapular rash)
        "L01",                  # WBC (lymphopenia)
        "L02",                  # CRP
        "R06",                  # travel (key)
    ],

    # ===== D92: 腫瘍熱 (Tumor fever) =====
    "D92": [
        "T01",                  # fever duration (weeks-months)
        "T03",                  # fever pattern
        "S01",                  # cough (if pulmonary)
        "S07",                  # fatigue
        "S16",                  # night sweats
        "S17",                  # weight loss (key)
        "S46",                  # anorexia
        "E01",                  # temperature (low-moderate)
        "L01",                  # WBC
        "L02",                  # CRP
        "L04",                  # chest X-ray
        "L28",                  # ESR
        "R40",                  # malignancy known (key)
    ],

    # ===== D93: DRESS症候群 (DRESS syndrome) =====
    "D93": [
        "T01",                  # fever duration
        "S18",                  # skin complaint (widespread rash, key)
        "S40",                  # facial swelling (periorbital edema, key)
        "E01",                  # temperature (high)
        "E12",                  # skin exam (maculopapular -> exfoliative, key)
        "E13",                  # lymphadenopathy (key)
        "L01",                  # WBC (eosinophilia or atypical lymphocytes)
        "L02",                  # CRP
        "L11",                  # liver enzymes (elevated, key)
        "L14",                  # peripheral blood (eosinophilia/atypical lymphocytes, key)
        "R08",                  # new medication (key - aromatic anticonvulsants, allopurinol etc.)
    ],

    # ===== D94: IgG4関連疾患 (IgG4-related disease) =====
    "D94": [
        "T01",                  # fever duration
        "S07",                  # fatigue
        "S12",                  # abdominal pain (pancreatic)
        "S16",                  # night sweats
        "S17",                  # weight loss
        "E01",                  # temperature (low-grade)
        "E18",                  # jaundice (obstructive, autoimmune pancreatitis)
        "E24",                  # parotid/submandibular gland swelling
        "L02",                  # CRP (mild)
        "L28",                  # ESR
        "L37",                  # IgG4 (elevated, key)
    ],

    # ===== D95: 日本脳炎 (Japanese encephalitis) =====
    "D95": [
        "S05",                  # headache (severe, key)
        "S13",                  # nausea/vomiting
        "S42",                  # seizure (key)
        "E01",                  # temperature (high)
        "E06",                  # neck stiffness
        "E16",                  # consciousness (rapid deterioration, key)
        "L01",                  # WBC
        "L02",                  # CRP
        "L45",                  # CSF analysis
        "L46",                  # brain MRI (thalamic lesions, key)
        "R06",                  # travel / endemic area
        "R43",                  # vaccination (JE vaccine)
    ],

    # ===== D96: 菊池病 (Kikuchi disease) =====
    "D96": [
        "T01", "T03",           # duration (weeks), pattern
        "S07",                  # fatigue
        "S17",                  # weight loss
        "S46",                  # anorexia
        "E01",                  # temperature
        "E13",                  # lymphadenopathy (cervical, key - painful)
        "E14",                  # splenomegaly (sometimes)
        "E34",                  # hepatomegaly (sometimes)
        "L01",                  # WBC (leukopenia, key)
        "L02",                  # CRP
        "L28",                  # ESR
        "R02",                  # sex (young women more common)
    ],

    # ===== D97: キャッスルマン病 (Castleman disease) =====
    "D97": [
        "T01",                  # fever duration (months)
        "S07",                  # fatigue
        "S17",                  # weight loss
        "S46",                  # anorexia
        "E01",                  # temperature
        "E13",                  # lymphadenopathy (key)
        "E14",                  # splenomegaly
        "E34",                  # hepatomegaly
        "L01",                  # WBC
        "L02",                  # CRP
        "L22",                  # pancytopenia
        "L28",                  # ESR
        "L41",                  # IL-6/sIL-2R (very elevated, key)
    ],

    # ===== D98: 高安動脈炎 (Takayasu arteritis) =====
    "D98": [
        "T01",                  # fever duration
        "S07",                  # fatigue
        "S05",                  # headache (sometimes)
        "S06",                  # myalgia
        "S17",                  # weight loss
        "E01",                  # temperature
        "E02",                  # heart rate
        "E03",                  # blood pressure (asymmetric, key)
        "E33",                  # pulse deficit (key)
        "L02",                  # CRP (elevated)
        "L28",                  # ESR (very elevated)
        "R02",                  # sex (young women)
    ],

    # ===== D99: 非結核性抗酸菌症 (NTM) =====
    "D99": [
        "T01",                  # fever duration (months)
        "S01",                  # cough (chronic, key)
        "S04",                  # dyspnea
        "S07",                  # fatigue
        "S17",                  # weight loss
        "S34",                  # hemoptysis
        "E01",                  # temperature (low-grade)
        "L02",                  # CRP
        "L04",                  # chest X-ray (bronchiectasis, nodules)
        "L35",                  # chest CT (key - tree-in-bud, bronchiectasis)
        "R02",                  # sex (older thin women)
        "R05",                  # immunosuppressed
    ],

    # ===== D100: A型急性肝炎 (Hepatitis A) =====
    "D100": [
        "T01",                  # fever duration
        "S07",                  # fatigue (key, prodromal)
        "S12",                  # abdominal pain (RUQ)
        "S13",                  # nausea/vomiting (key)
        "S14",                  # diarrhea
        "S46",                  # anorexia (key, early)
        "E01",                  # temperature
        "E18",                  # jaundice (key, after prodrome)
        "E34",                  # hepatomegaly
        "L02",                  # CRP
        "L11",                  # liver enzymes (very high, key - ALT>1000)
        "L39",                  # hepatitis serology (HAV IgM, key)
        "R06",                  # travel (endemic areas)
    ],

    # ===== D101: 梅毒二期 (Secondary syphilis) =====
    "D101": [
        "T01",                  # fever duration
        "S02",                  # sore throat (mucous patches)
        "S07",                  # fatigue
        "S08",                  # arthralgia
        "S18",                  # skin complaint (widespread rash)
        "S29",                  # oral ulcers (mucous patches)
        "S43",                  # palm/sole rash (key, characteristic)
        "E01",                  # temperature (low-grade)
        "E12",                  # skin exam (maculopapular rash, key)
        "E13",                  # lymphadenopathy (generalized)
        "L02",                  # CRP
        "L38",                  # RPR/TPHA (key)
        "R36",                  # high-risk sexual behavior
    ],

    # ===== D102: レジオネラ肺炎 (Legionella pneumonia) =====
    "D102": [
        "T01",                  # fever duration
        "S01",                  # cough (non-productive initially, key)
        "S04",                  # dyspnea
        "S05",                  # headache
        "S07",                  # fatigue
        "S09",                  # rigors
        "S12",                  # abdominal pain (watery diarrhea/pain)
        "S13",                  # nausea
        "S14",                  # diarrhea (watery, key - distinguishes from other pneumonia)
        "E01",                  # temperature (very high, >40)
        "E04",                  # respiratory rate
        "E05",                  # SpO2
        "E07",                  # lung auscultation
        "E16",                  # consciousness (confusion, key)
        "L01",                  # WBC (elevated)
        "L02",                  # CRP (very high)
        "L04",                  # chest X-ray (rapidly progressive infiltrate)
        "L11",                  # liver enzymes (elevated)
        "L40",                  # Legionella urinary antigen (key)
        "L44",                  # electrolytes (hyponatremia, key)
    ],

    # ===== D103: 急性リウマチ熱 (Acute rheumatic fever) =====
    "D103": [
        "T01",                  # fever duration (weeks)
        "S08",                  # arthralgia (migratory polyarthritis, key - Jones major)
        "S21",                  # chest pain (pericarditis)
        "S23",                  # joint swelling (migratory, large joints, key)
        "S18",                  # skin complaint (erythema marginatum, subcutaneous nodules)
        "S42",                  # seizure (Sydenham chorea, rare)
        "E01",                  # temperature
        "E12",                  # skin exam (erythema marginatum, subcutaneous nodules, key)
        "E15",                  # heart murmur (carditis, key - Jones major)
        "E21",                  # joint redness/warmth (key)
        "L01",                  # WBC (elevated)
        "L02",                  # CRP (very elevated)
        "L28",                  # ESR (very elevated, key)
    ],

    # ===== D104: オウム病 (Psittacosis / Chlamydia psittaci pneumonia) =====
    "D104": [
        "T01",                  # fever duration
        "S01",                  # cough (dry initially, key)
        "S04",                  # dyspnea
        "S05",                  # headache (severe, key)
        "S06",                  # myalgia
        "S07",                  # fatigue
        "S09",                  # rigors
        "E01",                  # temperature (high)
        "E14",                  # splenomegaly (sometimes)
        "E34",                  # hepatomegaly (sometimes)
        "L01",                  # WBC (normal or low)
        "L02",                  # CRP (elevated)
        "L04",                  # chest X-ray (infiltrate)
        "L11",                  # liver enzymes (elevated)
        "R30",                  # animal contact (pet birds, key)
    ],
}


# ---------------------------------------------------------------------------
# 2. Load data files
# ---------------------------------------------------------------------------

def load_json(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    base = Path(__file__).parent

    # Load step1 variables
    step1 = load_json(base / "step1_fever_v2.7.json")
    variables = {v["id"]: v for v in step1["variables"]}
    all_var_ids = set(variables.keys())
    disease_ids = sorted(
        [vid for vid in all_var_ids if vid.startswith("D")],
        key=lambda x: int(x[1:])
    )

    # Load step2 edges
    step2 = load_json(base / "step2_fever_edges_v4.json")
    edges = step2["edges"]

    # Build edge sets per disease
    # disease_edges[D] = set of variable IDs connected to D
    disease_edges: dict[str, set[str]] = defaultdict(set)
    for e in edges:
        f, t = e["from"], e["to"]
        if f.startswith("D"):
            disease_edges[f].add(t)
        if t.startswith("D"):
            disease_edges[t].add(f)

    # Load step3 CPTs
    step3 = load_json(base / "step3_fever_cpts_v2.json")
    full_cpt_keys = set(step3.get("full_cpts", {}).keys())
    noisy_or_keys = set(step3.get("noisy_or_params", {}).keys())
    all_cpt_keys = full_cpt_keys | noisy_or_keys

    # Also map which edges have CPT coverage:
    # A CPT exists for variable X if X is in all_cpt_keys.
    # An edge D->X has CPT coverage if X has a CPT entry that references D as parent.
    # For simplicity, we check if the child variable has any CPT defined.
    # A more thorough check would parse the parent lists, but this is a good first pass.

    # Build noisy-or parent sets for deeper check
    noisy_or_parents: dict[str, set[str]] = {}
    for child, params in step3.get("noisy_or_params", {}).items():
        if isinstance(params, dict) and "parents" in params:
            noisy_or_parents[child] = set(params["parents"].keys())

    full_cpt_parents: dict[str, set[str]] = {}
    for child, params in step3.get("full_cpts", {}).items():
        if isinstance(params, dict) and "parents" in params:
            parents = params["parents"]
            if isinstance(parents, list):
                full_cpt_parents[child] = set(parents)
            elif isinstance(parents, dict):
                full_cpt_parents[child] = set(parents.keys())

    # ---------------------------------------------------------------------------
    # 3. Audit
    # ---------------------------------------------------------------------------

    print("=" * 80)
    print("BAYESIAN NETWORK EDGE AUDIT REPORT")
    print("=" * 80)
    print(f"Step1 variables: {len(all_var_ids)}")
    print(f"Step2 edges: {len(edges)}")
    print(f"Step3 CPTs (full+noisy-or): {len(all_cpt_keys)}")
    print(f"Diseases defined in EXPECTED_EDGES: {len(EXPECTED_EDGES)}")
    print(f"Diseases in step1: {len(disease_ids)}")
    print()

    total_missing_edges = 0
    total_missing_cpts = 0
    total_extra_edges = 0
    diseases_with_issues = 0
    diseases_without_expected = []

    # Track summary stats
    missing_edges_by_disease = {}
    missing_cpts_by_disease = {}

    for did in disease_ids:
        var = variables[did]
        name_ja = var.get("name_ja", var.get("name", ""))
        name_en = var.get("name", "")

        has_edges = sorted(disease_edges.get(did, set()))
        expected = sorted(set(EXPECTED_EDGES.get(did, [])))

        if did not in EXPECTED_EDGES:
            diseases_without_expected.append(f"{did} ({name_ja})")
            continue

        # Validate expected edges reference real variables
        invalid_expected = [v for v in expected if v not in all_var_ids]
        if invalid_expected:
            print(f"WARNING: {did} expected edges reference non-existent variables: {invalid_expected}")

        # Filter to valid only
        expected_valid = [v for v in expected if v in all_var_ids]

        has_set = set(has_edges)
        expected_set = set(expected_valid)

        missing = sorted(expected_set - has_set)
        extra = sorted(has_set - expected_set)

        # Check CPT coverage for existing edges
        missing_cpt_edges = []
        for target in has_edges:
            # For D->X edges: check if X has CPT
            if not target.startswith("D") and target not in all_cpt_keys:
                missing_cpt_edges.append(target)
            # For R->D edges: check if D has CPT with R as parent
            # (more complex, skip for now)

        has_issue = bool(missing) or bool(missing_cpt_edges)
        if has_issue:
            diseases_with_issues += 1

        total_missing_edges += len(missing)
        total_missing_cpts += len(missing_cpt_edges)
        total_extra_edges += len(extra)

        missing_edges_by_disease[did] = missing
        missing_cpts_by_disease[did] = missing_cpt_edges

        # Always print, but highlight issues
        marker = " *** ISSUES ***" if has_issue else ""
        print(f"Disease {did} ({name_ja}){marker}")
        print(f"  Has ({len(has_edges)}): {', '.join(has_edges)}")
        print(f"  Expected ({len(expected_valid)}): {', '.join(expected_valid)}")

        if missing:
            missing_labels = []
            for m in missing:
                v = variables.get(m, {})
                label = f"{m}({v.get('name_ja', v.get('name', '?'))})"
                missing_labels.append(label)
            print(f"  MISSING EDGES ({len(missing)}): {', '.join(missing_labels)}")
        else:
            print(f"  Missing edges: None")

        if extra:
            extra_labels = []
            for e in extra:
                v = variables.get(e, {})
                label = f"{e}({v.get('name_ja', v.get('name', '?'))})"
                extra_labels.append(label)
            print(f"  Extra edges (in step2 but not in expected, may be valid): {', '.join(extra_labels)}")

        if missing_cpt_edges:
            cpt_labels = []
            for c in missing_cpt_edges:
                v = variables.get(c, {})
                label = f"{c}({v.get('name_ja', v.get('name', '?'))})"
                cpt_labels.append(label)
            print(f"  MISSING CPTs ({len(missing_cpt_edges)}): {', '.join(cpt_labels)}")

        print()

    # ---------------------------------------------------------------------------
    # 4. Summary
    # ---------------------------------------------------------------------------

    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total diseases audited: {len(EXPECTED_EDGES)}")
    print(f"Diseases with issues: {diseases_with_issues}")
    print(f"Total missing edges: {total_missing_edges}")
    print(f"Total missing CPTs: {total_missing_cpts}")
    print(f"Total extra edges (in step2 but not in expected): {total_extra_edges}")
    print()

    if diseases_without_expected:
        print(f"Diseases WITHOUT expected edges defined ({len(diseases_without_expected)}):")
        for d in diseases_without_expected:
            print(f"  {d}")
        print()

    # Top diseases by missing edges
    print("TOP DISEASES BY MISSING EDGES:")
    sorted_missing = sorted(
        missing_edges_by_disease.items(),
        key=lambda x: len(x[1]),
        reverse=True
    )
    for did, missing in sorted_missing[:20]:
        if not missing:
            break
        name_ja = variables[did].get("name_ja", "")
        print(f"  {did} ({name_ja}): {len(missing)} missing -> {', '.join(missing)}")

    print()

    # Most commonly missing variables
    print("MOST COMMONLY MISSING VARIABLES:")
    var_missing_count: dict[str, int] = defaultdict(int)
    for missing_list in missing_edges_by_disease.values():
        for v in missing_list:
            var_missing_count[v] += 1
    sorted_vars = sorted(var_missing_count.items(), key=lambda x: x[1], reverse=True)
    for vid, count in sorted_vars[:20]:
        v = variables.get(vid, {})
        print(f"  {vid} ({v.get('name_ja', '')}): missing from {count} diseases")

    print()

    # Generate actionable fix list
    print("=" * 80)
    print("ACTIONABLE: EDGES TO ADD TO step2_fever_edges_v4.json")
    print("=" * 80)
    fix_count = 0
    for did in disease_ids:
        missing = missing_edges_by_disease.get(did, [])
        if not missing:
            continue
        name_en = variables[did].get("name", "")
        for m in missing:
            mv = variables.get(m, {})
            m_name = mv.get("name", "")
            # Determine edge direction
            if m.startswith("R"):
                # Risk factor -> Disease
                direction = f"{m} -> {did}"
                print(f'  {{"from": "{m}", "to": "{did}", '
                      f'"from_name": "{m_name}", "to_name": "{name_en}", '
                      f'"reason": "TODO"}}')
            elif m.startswith("D"):
                # Disease -> Disease
                direction = f"{did} -> {m}"
                print(f'  {{"from": "{did}", "to": "{m}", '
                      f'"from_name": "{name_en}", "to_name": "{m_name}", '
                      f'"reason": "TODO"}}')
            else:
                # Disease -> Symptom/Sign/Lab/Temporal
                direction = f"{did} -> {m}"
                print(f'  {{"from": "{did}", "to": "{m}", '
                      f'"from_name": "{name_en}", "to_name": "{m_name}", '
                      f'"reason": "TODO"}}')
            fix_count += 1

    print()
    print(f"Total edges to add: {fix_count}")


if __name__ == "__main__":
    main()
