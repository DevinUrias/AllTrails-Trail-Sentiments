#!/usr/bin/env python3
import os
import re
import json
import argparse
from pathlib import Path
from typing import List

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default="Data/Cleaned_Trail_Reviews.csv")
    ap.add_argument("--config_dir", default="config")
    ap.add_argument("--out_dir", default="Results")
    return ap.parse_args()

def read_lines(path: Path) -> List[str]:
    if not path.exists():
        return []
    with open(path, "r", encoding="utf-8") as f:
        lines = [ln.strip() for ln in f if ln.strip()]
    return lines

def split_terms_phrases(lines: List[str]):
    phrases = [ln for ln in lines if " " in ln]
    terms = [ln for ln in lines if " " not in ln]
    return terms, phrases

def normalize_phrases(text: str, phrases: List[str], glue="_") -> str:
    if not isinstance(text, str):
        return ""
    t = text.lower()
    replacements = {
        "worth it": "worthit",
        "must do": "mustdo",
        "must see": "must_see",
        "highly recommend": "highly_recommend",
        "never again": "never_again"
    }
    for k, v in replacements.items():
        t = t.replace(k, v)
    for ph in phrases:
        if ph in t:
            t = t.replace(ph, ph.replace(" ", glue))
    return t

def try_load_vader():
    try:
        from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
        return SentimentIntensityAnalyzer()
    except Exception:
        return None

def simple_sentiment(text: str, pos_terms: set, neg_terms: set) -> float:
    if not text:
        return np.nan
    toks = re.findall(r"[a-zA-Z_']+", text.lower())
    if not toks:
        return np.nan
    pos = sum(1 for t in toks if t in pos_terms)
    neg = sum(1 for t in toks if t in neg_terms)
    if pos == 0 and neg == 0:
        return 0.0
    return (pos - neg) / (pos + neg)

def blended_score(text: str, vader, pos_terms: set, neg_terms: set) -> float:
    if not isinstance(text, str) or not text.strip():
        return np.nan
    fb = simple_sentiment(text, pos_terms, neg_terms)
    if vader is not None:
        try:
            vd = float(vader.polarity_scores(text)['compound'])
            return 0.6 * fb + 0.4 * vd
        except Exception:
            pass
    return fb

def extract_category_text(full_text: str, regex_list) -> str:
    if not isinstance(full_text, str) or not full_text.strip():
        return ""
    sents = re.split(r'(?<=[\.!?])\s+', full_text.lower())
    keep = []
    for s in sents:
        if any(p.search(s) for p in regex_list):
            keep.append(s)
    return " ".join(keep)

def apply_simple_negation_flip(text: str, score: float) -> float:
    if isinstance(text, str) and "not crowded" in text:
        return -score if score != 0 else 0.4
    return score

def plot_monthly(df_monthly: pd.DataFrame, y_col: str, title: str, out_path: Path):
    plt.figure(figsize=(10, 5))
    plt.plot(df_monthly['Month'], df_monthly[y_col], marker='o')
    plt.title(title)
    plt.xlabel("Month")
    plt.ylabel("Mean" if y_col.endswith("_mean") else "Value")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    plt.close()

def main():
    args = parse_args()
    data_path = Path(args.data)
    cfg_dir = Path(args.config_dir)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(data_path)
    df = df.dropna(subset=["Date", "Content", "Rating"]).copy()
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df = df.dropna(subset=["Date"]).copy()

    with open(cfg_dir/"categories.json", "r", encoding="utf-8") as f:
        categories = json.load(f)

    pos_lines = read_lines(cfg_dir/"pos_words.txt")
    neg_lines = read_lines(cfg_dir/"neg_words.txt")
    pos_terms, pos_phrases = split_terms_phrases(pos_lines)
    neg_terms, neg_phrases = split_terms_phrases(neg_lines)

    df["Content_lc"] = df["Content"].astype(str).str.lower()
    df["Content_norm"] = df["Content_lc"].apply(lambda t: normalize_phrases(t, pos_phrases + neg_phrases))

    cat_regex = {cat: [re.compile(pat) for pat in pats] for cat, pats in categories.items()}

    vader = try_load_vader()
    POS_SET = set([t.strip() for t in pos_terms if t.strip()])
    NEG_SET = set([t.strip() for t in neg_terms if t.strip()])

    for cat in categories.keys():
        sn_col = f"{cat}_snippet"
        se_col = f"{cat}_sent"
        df[sn_col] = df["Content_norm"].apply(lambda t: extract_category_text(t, cat_regex[cat]))
        df[se_col] = df[sn_col].apply(lambda s: blended_score(s, vader, POS_SET, NEG_SET))
        if cat.lower() == "crowding":
            df[se_col] = df.apply(lambda r: apply_simple_negation_flip(r[sn_col], r[se_col]), axis=1)

    df["Overall_Review_sent"] = df["Content_norm"].apply(lambda t: blended_score(t, vader, POS_SET, NEG_SET))

    review_cols = ["Date", "Rating", "Content"] + \
                  [f"{cat}_snippet" for cat in categories.keys()] + \
                  [f"{cat}_sent" for cat in categories.keys()] + \
                  ["Overall_Review_sent"]
    review_out = out_dir/"review_sentiment_scores.csv"
    df[review_cols].to_csv(review_out, index=False)

    df["Month"] = df["Date"].dt.to_period("M").dt.to_timestamp()
    agg_cols = [f"{cat}_sent" for cat in categories.keys()] + ["Overall_Review_sent"]
    monthly = (
        df.groupby("Month")[agg_cols + ["Rating"]]
          .agg(["mean", "count"])
          .sort_index()
    )
    monthly.columns = ["_".join([part for part in col if part]) for col in monthly.columns.to_flat_index()]
    monthly = monthly.reset_index()
    monthly_out = out_dir/"monthly_sentiment_summary.csv"
    monthly.to_csv(monthly_out, index=False)

    for cat in categories.keys():
        col = f"{cat}_sent_mean"
        if col in monthly.columns:
            plot_monthly(monthly, col, f"{cat} — Monthly Mean Sentiment", out_dir/f"{cat.lower()}_monthly_sentiment.png")

    if "Overall_Review_sent_mean" in monthly.columns:
        plot_monthly(monthly, "Overall_Review_sent_mean", "Overall Review Sentiment — Monthly Mean", out_dir/"overall_review_monthly_sentiment.png")

    if "Rating_mean" in monthly.columns:
        plot_monthly(monthly, "Rating_mean", "Monthly Mean Star Rating", out_dir/"rating_monthly_mean.png")

    print(f"[OK] Wrote: {review_out}")
    print(f"[OK] Wrote: {monthly_out}")
    print(f"[OK] Plots saved to: {out_dir.resolve()}")

    
    plt.figure(figsize=(10,6))
    plt.scatter(df['Date'], df['Rating'], c=(df['Rating'] < 5), cmap='coolwarm', alpha=0.3)
    plt.xlabel("Date")
    plt.ylabel("Rating")
    plt.title("Trail Ratings Over Time")
    plt.ylim(0.5, 5.5)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(args.out_dir, "ratings_over_time.png"))
    plt.close()

if __name__ == "__main__":
    main()
