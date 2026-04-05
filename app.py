#!/usr/bin/env python3
"""
VeSMed V3 — Web Frontend for BN Inference Engine
"""

import json
import os
from flask import Flask, render_template, request, jsonify
from bn_inference import (build_model, infer, entropy, load_json,
                          next_best_test, next_best_falsification_test,
                          compute_idf_disc)

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


@app.after_request
def add_no_cache(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    return response

BASE = os.path.dirname(os.path.abspath(__file__))
STEP1 = os.path.join(BASE, "step1_fever_v2.7.json")
STEP2 = os.path.join(BASE, "step2_fever_edges_v4.json")
STEP3 = os.path.join(BASE, "step3_fever_cpts_v2.json")

# Load model once at startup
step1 = load_json(STEP1)
step2 = load_json(STEP2)
step3 = load_json(STEP3)
variables, diseases, disease_children, noisy_or, root_priors = build_model(step1, step2, step3)

# IDF discriminative coefficients for V3.1 enhanced mode
idf_disc = compute_idf_disc(step2, noisy_or, n_diseases=len(diseases))
IDF_DISC_POWER = 0.5
CF_COVERAGE_ALPHA = 0.3
PRIOR_POWER = 0.5

# Build lookup dicts
var_lookup = {v["id"]: v for v in step1["variables"]}

# Category display order and labels
CATEGORY_ORDER = [
    ("temporal", "時間的特徴", "temporal"),
    ("symptom", "症状", "symptom"),
    ("sign", "身体所見", "sign"),
    ("lab", "検査所見", "lab"),
    ("risk_factor", "リスク因子", "risk"),
]


def get_variables_by_category():
    """Group non-disease variables by category for the frontend."""
    groups = []
    for cat_id, cat_label, css_class in CATEGORY_ORDER:
        items = []
        for v in step1["variables"]:
            if v.get("category") == cat_id:
                items.append({
                    "id": v["id"],
                    "name": v.get("name", ""),
                    "name_ja": v.get("name_ja", ""),
                    "states": v.get("states", []),
                    "note": v.get("note", ""),
                })
        if items:
            groups.append({
                "id": cat_id,
                "label": cat_label,
                "css_class": css_class,
                "variables": items,
            })
    return groups


@app.route("/")
def index():
    groups = get_variables_by_category()
    disease_list = [
        {"id": v["id"], "name": v.get("name", ""), "name_ja": v.get("name_ja", "")}
        for v in step1["variables"] if v.get("category") == "disease"
    ]
    return render_template("index.html", groups=groups, disease_list=disease_list)


@app.route("/api/infer", methods=["POST"])
def api_infer():
    data = request.get_json()
    evidence = data.get("evidence", {})
    risk = data.get("risk_factors", {})

    ranked = infer(evidence, risk, diseases, disease_children, noisy_or,
                   root_priors, disc=idf_disc, disc_power=IDF_DISC_POWER,
                   cf_alpha=CF_COVERAGE_ALPHA, prior_power=PRIOR_POWER)
    h = entropy(ranked)

    results = []
    top3_ids = set()
    for i, (d_id, prob) in enumerate(ranked[:20]):
        v = var_lookup.get(d_id, {})
        results.append({
            "id": d_id,
            "name": v.get("name", d_id),
            "name_ja": v.get("name_ja", d_id),
            "probability": round(prob * 100, 2),
        })
        if i < 3:
            top3_ids.add(d_id)

    # 見逃し注意: critical/high severity, >0.5%, NOT in Top-3
    dont_miss = []
    for d_id, prob in ranked:
        if d_id in top3_ids:
            continue
        v = var_lookup.get(d_id, {})
        sev = v.get("severity", "")
        if sev in ("critical", "high") and prob > 0.005:
            dont_miss.append({
                "id": d_id,
                "name_ja": v.get("name_ja", d_id),
                "probability": round(prob * 100, 2),
                "severity": sev,
            })

    return jsonify({
        "entropy": round(h, 2),
        "n_evidence": len(evidence),
        "n_risk": len(risk),
        "results": results,
        "dont_miss": dont_miss,
    })


@app.route("/api/next_best_test", methods=["POST"])
def api_next_best_test():
    data = request.get_json()
    evidence = data.get("evidence", {})
    risk = data.get("risk_factors", {})

    recommendations = next_best_test(
        evidence, risk, diseases, disease_children, noisy_or, root_priors,
        disc=idf_disc, disc_power=IDF_DISC_POWER, cf_alpha=CF_COVERAGE_ALPHA,
        prior_power=PRIOR_POWER, top_n=15,
    )

    results = []
    for rec in recommendations:
        vid = rec["var_id"]
        v = var_lookup.get(vid, {})
        # Per-state details for expected findings
        state_details = []
        for sd in rec.get("state_details", []):
            state_details.append({
                "state": sd["state"],
                "prob": round(sd["prob"] * 100, 1),
                "h_after": round(sd["h_after"], 2),
            })
        results.append({
            "id": vid,
            "name": v.get("name", vid),
            "name_ja": v.get("name_ja", vid),
            "category": v.get("category", ""),
            "ig": round(rec["ig"], 3),
            "h_now": round(rec["h_now"], 2),
            "expected_h": round(rec["expected_h"], 2),
            "best_state": rec.get("best_state", ""),
            "best_state_h": round(rec.get("best_state_h", 0), 2),
            "state_details": state_details,
        })

    # Falsification recommendations (反証推奨)
    falsification = next_best_falsification_test(
        evidence, risk, diseases, disease_children, noisy_or, root_priors,
        disc=idf_disc, disc_power=IDF_DISC_POWER, cf_alpha=CF_COVERAGE_ALPHA,
        prior_power=PRIOR_POWER, top_n=5,
    )

    falsification_results = []
    for rec in falsification:
        vid = rec["var_id"]
        v = var_lookup.get(vid, {})
        state_details = []
        for sd in rec.get("state_details", []):
            state_details.append({
                "state": sd["state"],
                "prob": round(sd["prob"] * 100, 1),
                "h_after": round(sd["h_after"], 2),
            })
        falsification_results.append({
            "id": vid,
            "name": v.get("name", vid),
            "name_ja": v.get("name_ja", vid),
            "category": v.get("category", ""),
            "h_increase": round(rec["h_increase"], 3),
            "h_now": round(rec["h_now"], 2),
            "disruptive_state": rec.get("disruptive_state", ""),
            "disruptive_h": round(rec.get("disruptive_h", 0), 2),
            "state_details": state_details,
            "ig": round(rec["ig"], 3),
        })

    return jsonify({
        "recommendations": results,
        "falsification": falsification_results,
    })


@app.route("/api/lecture", methods=["POST"])
def api_lecture():
    """
    講義資料用分析API。疾患IDリストを受け取り、臨床推論教材を生成。

    POST body:
      { "disease_ids": ["D10", "D11", ...] }

    Returns:
      - diseases: 各疾患の基本情報 + 辺数
      - lr_rankings: 各疾患のLR上位所見
      - differential_pairs: 鑑別困難ペア + 鑑別の鍵
      - test_performance: テスト案例の成績
    """
    import math as _math
    data = request.get_json()
    target_ids = set(data.get("disease_ids", []))

    if not target_ids:
        return jsonify({"error": "disease_ids required"}), 400

    # Validate IDs
    valid_ids = set()
    for did in target_ids:
        if did in var_lookup and var_lookup[did].get("category") == "disease":
            valid_ids.add(did)

    # 1. Disease info
    disease_info = []
    for did in sorted(valid_ids, key=lambda x: int(x[1:]) if x[1:].isdigit() else 9999):
        v = var_lookup[did]
        n_edges = len(disease_children.get(did, set()))
        disease_info.append({
            "id": did,
            "name_ja": v.get("name_ja", ""),
            "name_en": v.get("name", ""),
            "severity": v.get("severity", ""),
            "n_edges": n_edges,
        })

    # 2. LR rankings per disease
    lr_rankings = {}
    for did in valid_ids:
        children = disease_children.get(did, set())
        if not children:
            continue
        lr_list = []
        for var_id in children:
            params = noisy_or.get(var_id)
            if not params:
                continue
            pe = params["parent_effects"]
            if did not in pe:
                continue
            for state in params["states"][1:]:
                p_d = pe[did].get(state, 0.001)
                p_leak = params["leak"].get(state, 1.0 / len(params["states"]))
                if p_leak > 0 and p_d > 0:
                    lr = p_d / p_leak
                    vname = var_lookup.get(var_id, {}).get("name_ja", var_id)
                    lr_list.append({
                        "var_id": var_id,
                        "var_name": vname,
                        "state": state,
                        "lr": round(lr, 1),
                        "p_disease": round(p_d, 3),
                        "p_leak": round(p_leak, 4),
                    })
        lr_list.sort(key=lambda x: -x["lr"])
        lr_rankings[did] = lr_list[:8]

    # 3. Differential pairs (within target set)
    differential_pairs = []
    id_list = sorted(valid_ids)
    for i, d1 in enumerate(id_list):
        c1 = disease_children.get(d1, set())
        if len(c1) < 3:
            continue
        for d2 in id_list[i + 1:]:
            c2 = disease_children.get(d2, set())
            if len(c2) < 3:
                continue
            shared = c1 & c2
            if len(shared) < 3:
                continue
            jaccard = len(shared) / len(c1 | c2)
            if jaccard < 0.3:
                continue

            # Find discriminating CPT differences
            key_diffs = []
            for var_id in shared:
                params = noisy_or.get(var_id)
                if not params:
                    continue
                pe = params["parent_effects"]
                if d1 not in pe or d2 not in pe:
                    continue
                for state in params["states"][1:]:
                    p1 = pe[d1].get(state, 0.001)
                    p2 = pe[d2].get(state, 0.001)
                    if p1 > 0.05 or p2 > 0.05:
                        ratio = max(p1 / max(p2, 0.001), p2 / max(p1, 0.001))
                        if ratio > 1.5:
                            vname = var_lookup.get(var_id, {}).get("name_ja", var_id)
                            key_diffs.append({
                                "var_name": vname,
                                "state": state,
                                "p1": round(p1, 3),
                                "p2": round(p2, 3),
                                "ratio": round(ratio, 1),
                                "favors": d1 if p1 > p2 else d2,
                            })
            key_diffs.sort(key=lambda x: -x["ratio"])

            # Unique variables
            only1 = [var_lookup.get(v, {}).get("name_ja", v)
                     for v in (c1 - c2)][:5]
            only2 = [var_lookup.get(v, {}).get("name_ja", v)
                     for v in (c2 - c1)][:5]

            n1 = var_lookup.get(d1, {}).get("name_ja", d1)
            n2 = var_lookup.get(d2, {}).get("name_ja", d2)

            differential_pairs.append({
                "d1": d1,
                "d2": d2,
                "name1": n1,
                "name2": n2,
                "jaccard": round(jaccard, 2),
                "shared_count": len(shared),
                "discriminators": key_diffs[:5],
                "unique_to_d1": only1,
                "unique_to_d2": only2,
            })

    differential_pairs.sort(key=lambda x: -x["jaccard"])

    # 4. Test case performance
    cases_file = os.path.join(BASE, "real_case_test_suite.json")
    test_perf = {"n_cases": 0, "top1": 0, "top3": 0, "misses": []}
    if os.path.exists(cases_file):
        cases = load_json(cases_file)
        for c in cases:
            expected = c.get("expected_id", "")
            if expected not in valid_ids or not c.get("in_scope", True):
                continue
            test_perf["n_cases"] += 1
            evidence = c.get("evidence", {})
            risk = c.get("risk_factors", {})
            ranked = infer(evidence, risk, diseases, disease_children,
                           noisy_or, root_priors, disc=idf_disc,
                           disc_power=IDF_DISC_POWER,
                           cf_alpha=CF_COVERAGE_ALPHA,
                           prior_power=PRIOR_POWER)
            rank = None
            for idx, (d, _) in enumerate(ranked):
                if d == expected:
                    rank = idx + 1
                    break
            if rank == 1:
                test_perf["top1"] += 1
                test_perf["top3"] += 1
            elif rank and rank <= 3:
                test_perf["top3"] += 1
            else:
                ename = var_lookup.get(expected, {}).get("name_ja", expected)
                top3_names = [var_lookup.get(d, {}).get("name_ja", d)
                              for d, _ in ranked[:3]]
                test_perf["misses"].append({
                    "case_id": c.get("id", "?"),
                    "expected": ename,
                    "rank": rank,
                    "top3": top3_names,
                })

    n = test_perf["n_cases"]
    if n:
        test_perf["top1_pct"] = round(test_perf["top1"] / n * 100, 1)
        test_perf["top3_pct"] = round(test_perf["top3"] / n * 100, 1)

    # 5. Missing IDs
    missing = sorted(target_ids - valid_ids)

    return jsonify({
        "diseases": disease_info,
        "missing_ids": missing,
        "lr_rankings": lr_rankings,
        "differential_pairs": differential_pairs[:30],
        "test_performance": test_perf,
    })


@app.route("/api/scenario", methods=["POST"])
def api_scenario():
    """
    臨床シナリオAPI。段階的に所見を追加して鑑別の変化を計算。

    POST body:
      { "steps": [
          {"label": "発熱+RUQ痛", "evidence": {"E01": "38.0_39.0", "S89": "RUQ"}, "risk": {}},
          {"label": "+Murphy(+)", "evidence": {"E01": "38.0_39.0", "S89": "RUQ", "E10": "positive"}, "risk": {}},
        ],
        "focus_ids": ["D11", "D25", ...]  // optional: highlight these diseases
      }
    """
    data = request.get_json()
    steps = data.get("steps", [])
    focus_ids = set(data.get("focus_ids", []))

    results = []
    for step in steps:
        evidence = step.get("evidence", {})
        risk = step.get("risk", {})
        label = step.get("label", "")

        ranked = infer(evidence, risk, diseases, disease_children, noisy_or,
                       root_priors, disc=idf_disc, disc_power=IDF_DISC_POWER,
                       cf_alpha=CF_COVERAGE_ALPHA, prior_power=PRIOR_POWER)
        h = entropy(ranked)

        top = []
        for i, (d_id, prob) in enumerate(ranked[:10]):
            v = var_lookup.get(d_id, {})
            top.append({
                "rank": i + 1,
                "id": d_id,
                "name_ja": v.get("name_ja", d_id),
                "prob_pct": round(prob * 100, 1),
                "in_focus": d_id in focus_ids,
            })

        results.append({
            "label": label,
            "entropy": round(h, 2),
            "n_evidence": len(evidence),
            "top": top,
        })

    return jsonify({"steps": results})


if __name__ == "__main__":
    print("VeSMed V3 Web UI: http://localhost:5000")
    app.run(debug=False, host="0.0.0.0", port=5000)
