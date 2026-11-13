"""Rebuild Phase 2 tasks 6-9, NHANES Path A tables, and final figures."""

import json
from math import comb, pi, sqrt
from pathlib import Path
from statistics import NormalDist

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from phase2_analysis import DATA, OUT, ROOT, read_xpt, require_unique_seqn


FIGURES = ROOT / "figures" / "phase2"
FIGURES.mkdir(parents=True, exist_ok=True)
DRAW_SIZE = 10
RNG_SEED = 20261113


def analysis_sample() -> pd.DataFrame:
    demo = read_xpt("DEMO_L")
    sleep = read_xpt("SLQ_L")
    supp = read_xpt("DSQTOT_L")
    for frame, name in ((demo, "DEMO_L"), (sleep, "SLQ_L"), (supp, "DSQTOT_L")):
        require_unique_seqn(frame, name)
    merged = demo.merge(sleep, on="SEQN", how="inner", validate="one_to_one")
    merged = merged.merge(supp, on="SEQN", how="inner", validate="one_to_one")
    sample = merged.loc[
        merged["RIDAGEYR"].ge(20)
        & merged["DSD010"].isin([1, 2])
        & merged["SLD012"].notna()
    ].copy()
    if sample["SEQN"].duplicated().any() or sample.empty:
        raise ValueError("Expected a nonempty sample with one row per adult")
    sample["supplement_use"] = sample["DSD010"].eq(1)
    # Code 2 means <3 hours and 14 means 14+ hours. Both classify the binary
    # short-sleep event, but neither is an exact numeric duration.
    sample["short_weekday_sleep"] = sample["SLD012"].lt(7)
    return sample


def numeric_hours(frame: pd.DataFrame, column: str) -> pd.Series:
    source = frame[column]
    if not isinstance(source, pd.Series):
        raise TypeError(f"Expected one Series for {column}")
    values = pd.to_numeric(source, errors="coerce")
    if not isinstance(values, pd.Series):
        raise TypeError(f"Expected numeric Series for {column}")
    return values.where(values.ge(3) & values.le(13.5))


def normal_figure(x: pd.Series, mean: float, sd: float) -> None:
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.5, 4.3), layout="constrained")
    ax1.hist(x, bins=np.arange(2.75, 14.0, 0.5), density=True,
             color="#457b9d", edgecolor="white", linewidth=0.6, label="Observed")
    grid = np.linspace(3, 13.5, 350)
    density = np.exp(-0.5 * ((grid - mean) / sd) ** 2) / (sd * sqrt(2 * pi))
    ax1.plot(grid, density, color="#e76f51", linewidth=2.2, label="Matched normal density")
    ax1.set(xlabel="Usual weekday sleep (hours)", ylabel="Density",
            title="Observed sleep and a normal curve")
    ax1.legend(frameon=False)

    observed = np.sort(x.to_numpy(dtype=float))
    probabilities = (np.arange(1, len(observed) + 1) - 0.5) / len(observed)
    normal = NormalDist(mu=mean, sigma=sd)
    theoretical = np.fromiter((normal.inv_cdf(float(p)) for p in probabilities), dtype=float)
    ax2.scatter(theoretical, observed, s=5, alpha=0.18, color="#457b9d", rasterized=True)
    limits = (min(theoretical.min(), observed.min()), max(theoretical.max(), observed.max()))
    ax2.plot(limits, limits, color="#e76f51", linewidth=1.5)
    ax2.set(xlabel="Normal-model quantile (hours)", ylabel="Observed quantile (hours)",
            title="Normal Q-Q comparison")
    fig.suptitle(f"Adult weekday sleep: exact-hour codes only (n={len(x):,}), unweighted")
    fig.savefig(FIGURES / "fig2_weekday_sleep_normal_check.png", dpi=180)
    plt.close(fig)


def covariance_figure(pairs: pd.DataFrame, covariance: float) -> None:
    fig, ax = plt.subplots(figsize=(7, 6), layout="constrained")
    hb = ax.hexbin(pairs["weekday_hours"], pairs["weekend_hours"],
                   gridsize=28, extent=(3, 13.5, 3, 13.5), mincnt=1,
                   cmap="YlGnBu", bins="log")
    ax.plot([3, 13.5], [3, 13.5], linestyle="--", color="#ad3b37", linewidth=1.2,
            label="Same weekday and weekend hours")
    ax.set(xlim=(3, 13.5), ylim=(3, 13.5),
           xlabel="Usual weekday sleep (hours)", ylabel="Usual weekend sleep (hours)",
           title=f"Weekday vs weekend sleep (n={len(pairs):,})\nEmpirical covariance = {covariance:.2f} hours²")
    ax.legend(frameon=False, loc="upper left")
    fig.colorbar(hb, ax=ax, label="Participants (log color scale)")
    fig.savefig(FIGURES / "fig3_weekday_vs_weekend_sleep.png", dpi=180)
    plt.close(fig)


def binomial_blocks(sample: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    values = sample.loc[sample["supplement_use"], "short_weekday_sleep"].to_numpy(dtype=int)
    total_users = len(values)
    p = float(values.mean())
    rng = np.random.default_rng(RNG_SEED)
    shuffled = rng.permutation(values)
    blocks_n = total_users // DRAW_SIZE
    block_counts = shuffled[:blocks_n * DRAW_SIZE].reshape(blocks_n, DRAW_SIZE).sum(axis=1)
    observed = np.bincount(block_counts, minlength=DRAW_SIZE + 1)
    expected_prob = np.array([
        comb(DRAW_SIZE, k) * p**k * (1 - p)**(DRAW_SIZE - k)
        for k in range(DRAW_SIZE + 1)
    ])
    table = pd.DataFrame({
        "short_sleepers_k": np.arange(DRAW_SIZE + 1),
        "observed_blocks": observed,
        "observed_fraction": observed / blocks_n,
        "binomial_probability": expected_prob,
        "binomial_expected_blocks": blocks_n * expected_prob,
    })
    table.to_csv(OUT / "path_a2_equal_size_blocks.csv", index=False)

    # Combine the sparse right tail for a readable comparison.
    plot_observed = np.r_[observed[:5], observed[5:].sum()]
    plot_expected = np.r_[blocks_n * expected_prob[:5], blocks_n * expected_prob[5:].sum()]
    positions = np.arange(6)
    fig, ax = plt.subplots(figsize=(8, 4.6), layout="constrained")
    ax.bar(positions - 0.18, plot_observed, width=0.36, color="#457b9d", label="Observed blocks")
    ax.bar(positions + 0.18, plot_expected, width=0.36, color="#e9a852", label="Binomial model")
    ax.set(xticks=positions, xticklabels=["0", "1", "2", "3", "4", "5+"],
           xlabel="Number sleeping <7 hours in a 10-person block",
           ylabel="Number of blocks",
           title=f"Random partition of supplement users (seed {RNG_SEED}; {blocks_n} blocks)")
    ax.legend(frameon=False)
    fig.savefig(FIGURES / "fig1_binomial_blocks.png", dpi=180)
    plt.close(fig)
    return table, {
        "users_n": total_users, "short_sleep_users_n": int(values.sum()),
        "block_size": DRAW_SIZE, "blocks_n": blocks_n,
        "unused_users_n": total_users - blocks_n * DRAW_SIZE,
        "seed": RNG_SEED, "p_short_sleep": p,
        "observed_block_mean": float(block_counts.mean()),
        "observed_block_variance": float(block_counts.var(ddof=0)),
        "binomial_mean": DRAW_SIZE * p,
        "binomial_variance": DRAW_SIZE * p * (1 - p),
    }


def subgroup_probabilities(sample: pd.DataFrame) -> pd.DataFrame:
    age = pd.cut(sample["RIDAGEYR"], bins=[20, 40, 60, float("inf")],
                 right=False, labels=["20-39", "40-59", "60+"])
    dimensions = [
        ("age_band", age, ["20-39", "40-59", "60+"]),
        ("sex", sample["RIAGENDR"].map(
            lambda code: "Male (code 1)" if code == 1 else "Female (code 2)" if code == 2 else None),
         ["Male (code 1)", "Female (code 2)"]),
    ]
    records = []
    for dimension, labels, ordered_groups in dimensions:
        for subgroup in ordered_groups:
            for use in (True, False):
                part = sample.loc[labels.eq(subgroup) & sample["supplement_use"].eq(use)]
                n = len(part)
                k = int(part["short_weekday_sleep"].sum())
                records.append({"dimension": dimension, "subgroup": str(subgroup),
                                "supplement_use": "Yes" if use else "No",
                                "participants_n": n, "short_sleep_n": k,
                                "short_sleep_probability": k / n if n else float("nan")})
    table = pd.DataFrame(records)
    table.to_csv(OUT / "path_a1_subgroup_conditional_probabilities.csv", index=False)
    return table


def weighted_probabilities(sample: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    raw_weight = sample["WTDRD1"]
    if not isinstance(raw_weight, pd.Series):
        raise TypeError("Expected a single WTDRD1 weight Series")
    weight = pd.to_numeric(raw_weight, errors="coerce")
    if not isinstance(weight, pd.Series):
        raise TypeError("Expected numeric WTDRD1 weights")
    valid = sample.loc[weight.gt(0) & np.isfinite(weight)].copy()
    records = []
    for group, part in (
        ("All adults", valid),
        ("Supplement users", valid.loc[valid["supplement_use"]]),
        ("Non-users", valid.loc[~valid["supplement_use"]]),
    ):
        w = part["WTDRD1"].to_numpy(dtype=float)
        y = part["short_weekday_sleep"].to_numpy(dtype=float)
        records.append({"group": group, "participants_n": len(part),
                        "short_sleep_n": int(y.sum()), "sum_weight": float(w.sum()),
                        "unweighted_probability": float(y.mean()),
                        "WTDRD1_weighted_probability": float(np.average(y, weights=w))})
    table = pd.DataFrame(records)
    table.to_csv(OUT / "path_a4_weighted_probability.csv", index=False)

    positions = np.arange(3)
    fig, ax = plt.subplots(figsize=(8, 4.6), layout="constrained")
    ax.bar(positions - 0.18, 100 * table["unweighted_probability"], width=0.36,
           color="#457b9d", label="Unweighted")
    ax.bar(positions + 0.18, 100 * table["WTDRD1_weighted_probability"], width=0.36,
           color="#e9a852", label="WTDRD1 weighted")
    ax.set(xticks=positions, xticklabels=table["group"], ylim=(0, 40),
           ylabel="Weekday sleep <7 hours (%)",
           title="Short sleep in the same positive-weight adult sample")
    ax.legend(frameon=False)
    fig.savefig(FIGURES / "fig4_raw_vs_weighted_short_sleep.png", dpi=180)
    plt.close(fig)
    return table, {"probability_sample_n": len(sample),
                   "positive_weight_n": len(valid),
                   "excluded_nonpositive_or_missing_weight_n": len(sample) - len(valid)}


def main() -> None:
    sample = analysis_sample()
    weekday = numeric_hours(sample, "SLD012")
    x = weekday.dropna()
    x_values = x.to_numpy(dtype=float)
    mean = float(np.mean(x_values))
    variance = float(np.var(x_values, ddof=0))
    sd = sqrt(variance)
    q1, median, q3 = (float(v) for v in np.quantile(x_values, [0.25, 0.5, 0.75]))
    low_fence, high_fence = q1 - 1.5 * (q3 - q1), q3 + 1.5 * (q3 - q1)
    skewness = float(sqrt(len(x) * (len(x) - 1)) / (len(x) - 2)
                     * np.mean(((x_values - mean) / sd) ** 3))
    normal_metrics = {
        "analysis_n": len(sample), "exact_weekday_hours_n": len(x),
        "grouped_endpoint_excluded_n": int(np.count_nonzero(sample["SLD012"].isin([2, 14]))),
        "mean_hours": mean, "empirical_variance_hours_squared": variance,
        "standard_deviation_hours": sd, "median_hours": median,
        "q1_hours": q1, "q3_hours": q3, "iqr_hours": q3 - q1,
        "min_hours": float(np.min(x_values)), "max_hours": float(np.max(x_values)),
        "sample_skewness": skewness,
        "low_fence_hours": low_fence, "high_fence_hours": high_fence,
        "tukey_low_count": int(np.count_nonzero(x_values < low_fence)),
        "tukey_high_count": int(np.count_nonzero(x_values > high_fence)),
        "within_one_sd_fraction": float(np.mean((x_values >= mean - sd) & (x_values <= mean + sd))),
    }
    pd.DataFrame([normal_metrics]).to_csv(OUT / "weekday_sleep_distribution_summary.csv", index=False)
    normal_figure(x, mean, sd)

    pairs = pd.DataFrame({"weekday_hours": weekday,
                          "weekend_hours": numeric_hours(sample, "SLD013")}).dropna()
    x_pair = pairs["weekday_hours"].to_numpy(dtype=float)
    y_pair = pairs["weekend_hours"].to_numpy(dtype=float)
    covariance = float(np.mean((x_pair - np.mean(x_pair)) * (y_pair - np.mean(y_pair))))
    pair_metrics = {"paired_n": len(pairs), "weekday_mean_hours": float(np.mean(x_pair)),
                    "weekend_mean_hours": float(np.mean(y_pair)),
                    "empirical_covariance_hours_squared": covariance}
    pd.DataFrame([pair_metrics]).to_csv(OUT / "weekday_weekend_covariance.csv", index=False)
    covariance_figure(pairs, covariance)

    n = len(sample)
    a_n = int(np.count_nonzero(sample["supplement_use"]))
    b_n = int(np.count_nonzero(sample["short_weekday_sleep"]))
    both_n = int(np.count_nonzero(sample["supplement_use"] & sample["short_weekday_sleep"]))
    bayes = {"analysis_n": n, "supplement_users_n": a_n, "short_sleep_n": b_n,
             "both_n": both_n, "prior_p_supplement": a_n / n,
             "likelihood_p_short_given_supplement": both_n / a_n,
             "evidence_p_short": b_n / n,
             "posterior_p_supplement_given_short": both_n / b_n,
             "p_supplement_given_not_short": (a_n - both_n) / (n - b_n)}
    pd.DataFrame([bayes]).to_csv(OUT / "bayes_reverse_conditional.csv", index=False)

    blocks, block_metrics = binomial_blocks(sample)
    subgroups = subgroup_probabilities(sample)
    weighted, weight_metrics = weighted_probabilities(sample)
    metrics = {"normal": normal_metrics, "covariance": pair_metrics,
               "bayes": bayes, "path_a2": block_metrics,
               "path_a4": weight_metrics}
    (OUT / "extended_metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    print("Weekday sleep:", normal_metrics)
    print("Weekday/weekend covariance:", pair_metrics)
    print("Bayes:", bayes)
    print("Path A2:", block_metrics)
    print("Path A1 subgroup table:\n", subgroups.to_string(index=False))
    print("Path A4 weighted table:\n", weighted.to_string(index=False))
    print(f"Saved {len(blocks)} block-count rows and figures under {FIGURES}")


if __name__ == "__main__":
    main()
