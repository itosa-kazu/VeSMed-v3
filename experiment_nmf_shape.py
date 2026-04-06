#!/usr/bin/env python3
"""
嗅覚形状互補実験: CPT矩陣の低秩分解 (NMF)

嗅覚系統では、分子形状×受体形状→結合亲和力（物理が免費計算）。
VeSMedでは、疾病機制×変量検出特性→CPT。
もしCPT矩陣が低秩なら、「病理生理形状向量」が存在する証拠。

実験:
1. 8201条D→E辺からCPT矩陣を構築（多状態→代表値に圧縮）
2. NMFで低秩分解 → k個の潜在維度を抽出
3. 再構成誤差を評価（kの関数として）
4. 学出された維度を解釈（どの疾患/変量が各維度で高いか）
5. マスク予測テスト: 既知CPTの一部を隠して、残りから予測できるか
"""

import json
import numpy as np
from sklearn.decomposition import NMF
from sklearn.model_selection import KFold
import sys

def load_data():
    """Load step1/step2/step3 and build D×E matrix."""
    with open('step1_fever_v2.7.json') as f:
        s1 = json.load(f)
    with open('step2_fever_edges_v4.json') as f:
        s2 = json.load(f)
    with open('step3_fever_cpts_v2.json') as f:
        s3 = json.load(f)

    # Get disease and evidence variable lists
    diseases = sorted(set(v['id'] for v in s1['variables'] if v['id'].startswith('D')))
    evidences = sorted(set(v['id'] for v in s1['variables'] if v['id'].startswith(('E','S','L','T','M'))))

    # Build variable info lookup
    var_info = {}
    for v in s1['variables']:
        var_info[v['id']] = v

    # Build edge set with CPT values
    # For multi-state variables, we use the "present" or most informative state probability
    edge_cpts = {}  # (D, E) -> float (representative CPT value)

    full_cpts = s3['full_cpts']

    for eid in evidences:
        if eid not in full_cpts:
            continue
        ecpt = full_cpts[eid]
        parents = ecpt.get('parents', [])
        cpt = ecpt.get('cpt', {})

        if not parents or not cpt:
            continue

        # For variables with disease parents, extract P(positive_state | disease=yes, others=no)
        disease_parents = [p for p in parents if p.startswith('D')]

        if len(disease_parents) == 1:
            # Simple case: one disease parent
            did = disease_parents[0]
            states = var_info.get(eid, {}).get('states', [])

            # Find the "yes" configuration for this disease
            # CPT keys are like "yes" or "no|yes" etc.
            for cpt_key, val in cpt.items():
                parts = cpt_key.split('|')
                # Check if this disease is "yes" and all others are "no"
                if len(parts) == len(parents):
                    parent_states = dict(zip(parents, parts))
                    if parent_states.get(did) == 'yes' and all(
                        v == 'no' for k, v in parent_states.items() if k != did
                    ):
                        # val could be dict (multinomial) or float
                        if isinstance(val, dict):
                            # Use 1 - P(absent) as the "affinity"
                            absent_prob = val.get('absent', val.get('normal', 0))
                            edge_cpts[(did, eid)] = 1.0 - absent_prob
                        else:
                            edge_cpts[(did, eid)] = val
                        break

        elif len(disease_parents) > 1:
            # Multiple disease parents - extract each one individually
            for i, did in enumerate(disease_parents):
                for cpt_key, val in cpt.items():
                    parts = cpt_key.split('|')
                    if len(parts) == len(parents):
                        parent_states = dict(zip(parents, parts))
                        if parent_states.get(did) == 'yes' and all(
                            v == 'no' for k, v in parent_states.items()
                            if k != did and k.startswith('D')
                        ) and all(
                            True for k, v in parent_states.items() if not k.startswith('D')
                        ):
                            if isinstance(val, dict):
                                absent_prob = val.get('absent', val.get('normal', 0))
                                edge_cpts[(did, eid)] = 1.0 - absent_prob
                            else:
                                edge_cpts[(did, eid)] = val
                            break

    # Also extract from noisy_or_params (the main D→E CPTs)
    nop = s3.get('noisy_or_params', {})
    for eid, params in nop.items():
        if not eid.startswith(('E','S','L','T','M')):
            continue
        parent_effects = params.get('parent_effects', {})
        for did, effect in parent_effects.items():
            if not did.startswith('D'):
                continue
            if isinstance(effect, (int, float)):
                edge_cpts[(did, eid)] = effect
            elif isinstance(effect, dict):
                # Multi-state: use max non-absent probability
                vals = [v for k, v in effect.items() if k not in ('absent', 'normal', 'negative')]
                if vals:
                    edge_cpts[(did, eid)] = max(vals)

    print(f"Diseases: {len(diseases)}")
    print(f"Evidence variables: {len(evidences)}")
    print(f"Extracted CPT pairs: {len(edge_cpts)}")

    # Build matrix
    d_idx = {d: i for i, d in enumerate(diseases)}
    e_idx = {e: i for i, e in enumerate(evidences)}

    matrix = np.zeros((len(diseases), len(evidences)))
    mask = np.zeros((len(diseases), len(evidences)), dtype=bool)

    for (did, eid), val in edge_cpts.items():
        if did in d_idx and eid in e_idx:
            matrix[d_idx[did], e_idx[eid]] = val
            mask[d_idx[did], e_idx[eid]] = True

    print(f"Matrix shape: {matrix.shape}")
    print(f"Non-zero entries: {mask.sum()} ({mask.sum()/(matrix.shape[0]*matrix.shape[1])*100:.1f}%)")
    print(f"Matrix value range: [{matrix[mask].min():.4f}, {matrix[mask].max():.4f}]")
    print(f"Matrix mean (non-zero): {matrix[mask].mean():.4f}")

    return matrix, mask, diseases, evidences, var_info, edge_cpts


def run_nmf_sweep(matrix, mask):
    """Run NMF with different k values and measure reconstruction error."""
    print("\n" + "="*60)
    print("NMF Reconstruction Error vs k (rank)")
    print("="*60)

    # For NMF, we need non-negative matrix. Our CPT values are already [0,1].
    # Replace zeros with small epsilon for masked entries to avoid issues
    X = matrix.copy()

    results = []
    for k in [5, 10, 15, 20, 30, 50, 75, 100, 150, 200]:
        if k >= min(X.shape):
            break

        model = NMF(n_components=k, init='nndsvda', max_iter=500, random_state=42)
        W = model.fit_transform(X)  # D_shape: diseases × k
        H = model.components_         # V_shape: k × evidences

        # Reconstruction
        X_hat = W @ H

        # Error only on known entries
        known_errors = (X[mask] - X_hat[mask]) ** 2
        rmse_known = np.sqrt(known_errors.mean())

        # Also compute relative error
        rel_error = np.abs(X[mask] - X_hat[mask]) / np.maximum(X[mask], 0.01)
        mean_rel_error = rel_error.mean()

        # How many known entries are reconstructed within 10%?
        within_10pct = (np.abs(X[mask] - X_hat[mask]) < 0.1).mean()

        results.append((k, rmse_known, mean_rel_error, within_10pct))
        print(f"  k={k:3d}: RMSE={rmse_known:.4f}, MeanRelErr={mean_rel_error:.2f}, Within10%={within_10pct*100:.1f}%")

    return results


def cross_validate(matrix, mask, k_values=[10, 20, 30, 50]):
    """Mask 20% of known entries and predict them from the remaining 80%."""
    print("\n" + "="*60)
    print("Cross-Validation: Predict masked CPTs from remaining")
    print("="*60)

    known_indices = np.array(np.where(mask)).T  # (N, 2)
    n_known = len(known_indices)

    np.random.seed(42)
    perm = np.random.permutation(n_known)
    n_test = n_known // 5
    test_idx = perm[:n_test]
    train_idx = perm[n_test:]

    print(f"Total known: {n_known}, Train: {len(train_idx)}, Test: {len(test_idx)}")

    for k in k_values:
        if k >= min(matrix.shape):
            continue

        # Build training matrix (mask out test entries)
        X_train = matrix.copy()
        test_mask = np.zeros_like(mask)
        for idx in test_idx:
            r, c = known_indices[idx]
            X_train[r, c] = 0  # hide test values
            test_mask[r, c] = True

        # Fit NMF on training data
        model = NMF(n_components=k, init='nndsvda', max_iter=500, random_state=42)
        W = model.fit_transform(X_train)
        H = model.components_
        X_hat = W @ H

        # Evaluate on test set
        test_true = matrix[test_mask]
        test_pred = X_hat[test_mask]

        rmse = np.sqrt(((test_true - test_pred) ** 2).mean())
        within_10 = (np.abs(test_true - test_pred) < 0.1).mean()
        within_20 = (np.abs(test_true - test_pred) < 0.2).mean()

        # Correlation
        corr = np.corrcoef(test_true, test_pred)[0, 1]

        print(f"  k={k:3d}: RMSE={rmse:.4f}, r={corr:.3f}, Within10%={within_10*100:.1f}%, Within20%={within_20*100:.1f}%")


def interpret_factors(matrix, mask, diseases, evidences, var_info, k=20):
    """Extract and interpret NMF factors."""
    print("\n" + "="*60)
    print(f"Factor Interpretation (k={k})")
    print("="*60)

    model = NMF(n_components=k, init='nndsvda', max_iter=500, random_state=42)
    W = model.fit_transform(matrix)  # diseases × k
    H = model.components_            # k × evidences

    # For each factor, show top diseases and top variables
    for f in range(min(k, 10)):  # Show first 10 factors
        print(f"\n--- Factor {f+1} ---")

        # Top diseases
        top_d = np.argsort(W[:, f])[-5:][::-1]
        d_names = []
        for idx in top_d:
            did = diseases[idx]
            info = var_info.get(did, {})
            name = info.get('name_ja', info.get('name', did))
            d_names.append(f"  {did} {name} ({W[idx, f]:.2f})")

        # Top variables
        top_e = np.argsort(H[f, :])[-5:][::-1]
        e_names = []
        for idx in top_e:
            eid = evidences[idx]
            info = var_info.get(eid, {})
            name = info.get('name_ja', info.get('name', eid))
            e_names.append(f"  {eid} {name} ({H[f, idx]:.2f})")

        print("Top diseases:")
        for n in d_names:
            print(n)
        print("Top variables:")
        for n in e_names:
            print(n)

    return W, H


def main():
    print("="*60)
    print("嗅覚形状互補実験: CPT矩陣NMF分解")
    print("="*60)

    matrix, mask, diseases, evidences, var_info, edge_cpts = load_data()

    # 1. NMF reconstruction error sweep
    run_nmf_sweep(matrix, mask)

    # 2. Cross-validation (predict hidden CPTs)
    cross_validate(matrix, mask, k_values=[10, 20, 30, 50, 75])

    # 3. Factor interpretation
    W, H = interpret_factors(matrix, mask, diseases, evidences, var_info, k=20)

    # 4. Summary statistics
    print("\n" + "="*60)
    print("Summary")
    print("="*60)

    # Effective rank (how many singular values capture 90% of variance)
    U, s, Vt = np.linalg.svd(matrix, full_matrices=False)
    cum_var = np.cumsum(s**2) / np.sum(s**2)
    rank_90 = np.searchsorted(cum_var, 0.90) + 1
    rank_95 = np.searchsorted(cum_var, 0.95) + 1
    rank_99 = np.searchsorted(cum_var, 0.99) + 1

    print(f"Singular value analysis:")
    print(f"  Rank for 90% variance: {rank_90}")
    print(f"  Rank for 95% variance: {rank_95}")
    print(f"  Rank for 99% variance: {rank_99}")
    print(f"  Top 10 singular values: {s[:10].round(2)}")
    print(f"  → Effective dimensionality ≈ {rank_90}-{rank_95}")
    print(f"  → 嗅覚有効維度(~30)と比較: {'同量級' if rank_90 < 100 else '異量級'}")


if __name__ == '__main__':
    main()
