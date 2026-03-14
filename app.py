#!/usr/bin/env python3
"""
VeSMed V3 — Web Frontend for BN Inference Engine
"""

import json
import os
from flask import Flask, render_template, request, jsonify
from bn_inference import (build_model, infer, entropy, load_json,
                          next_best_test, compute_idf_disc)

app = Flask(__name__)

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
    return render_template("index.html", groups=groups)


@app.route("/api/infer", methods=["POST"])
def api_infer():
    data = request.get_json()
    evidence = data.get("evidence", {})
    risk = data.get("risk_factors", {})

    ranked = infer(evidence, risk, diseases, disease_children, noisy_or,
                   root_priors, disc=idf_disc, disc_power=IDF_DISC_POWER,
                   cf_alpha=CF_COVERAGE_ALPHA)
    h = entropy(ranked)

    results = []
    for d_id, prob in ranked[:20]:
        v = var_lookup.get(d_id, {})
        results.append({
            "id": d_id,
            "name": v.get("name", d_id),
            "name_ja": v.get("name_ja", d_id),
            "probability": round(prob * 100, 2),
        })

    return jsonify({
        "entropy": round(h, 2),
        "n_evidence": len(evidence),
        "n_risk": len(risk),
        "results": results,
    })


@app.route("/api/next_best_test", methods=["POST"])
def api_next_best_test():
    data = request.get_json()
    evidence = data.get("evidence", {})
    risk = data.get("risk_factors", {})

    recommendations = next_best_test(
        evidence, risk, diseases, disease_children, noisy_or, root_priors,
        disc=idf_disc, disc_power=IDF_DISC_POWER, cf_alpha=CF_COVERAGE_ALPHA,
        top_n=15,
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

    return jsonify({"recommendations": results})


if __name__ == "__main__":
    print("VeSMed V3 Web UI: http://localhost:5000")
    app.run(debug=False, host="0.0.0.0", port=5000)
