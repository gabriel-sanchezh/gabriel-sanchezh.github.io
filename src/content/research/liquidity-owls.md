---
title: "Liquidity Owls: A High-Frequency Estimation of Integrated Variance"
description: "Replicating and extending Hansen & Lunde (2005) on 1-second Nasdaq quotes: how to combine the overnight return with intraday realized variance."
date: 2026-07-01
note: "Working paper."
abstract: "I revisit the problem of measuring the integrated variance of a full trading day when high-frequency data exist only for the active trading session. Following Hansen and Lunde (2005), I combine the squared overnight return with a Newey–West-corrected realized variance of the open-to-close period, with weights chosen to minimize the mean-squared error among conditionally unbiased estimators. I apply the estimator to one-second best bid and offer quotations for the 30 components of the Dow Jones Industrial Average and three index ETFs over 2,034 trading days from May 2018 to June 2026. The qualitative structure of the original study survives: intraday measures dominate, yet the overnight return always retains informative weight."
keywords:
  - high-frequency data
  - realized variance
  - integrated variance
  - microstructure noise
  - overnight returns
  - Newey–West correction
conclusions:
  - "The qualitative structure of Hansen & Lunde (2005) survives two decades on: intraday measures dominate, yet the overnight return always retains informative weight."
  - "The overnight period now accounts for roughly 30% of daily variance, up from 20% in 2001–2004."
  - "For the diversified ETFs (DIA, SPY, QQQ), the squared overnight return earns weights several times larger than for any individual equity."
  - "Formal specification tests, exploiting the longer sample, reject a fixed overnight share for most instruments."
materials:
  - label: "Paper (PDF)"
    href: "/files/liquidity-owls.pdf"
packages:
  - Python
  - numpy
  - polars
  - pandas
  - databento
colab: "https://colab.research.google.com/github/gabriel-sanchezh/gabriel-sanchezh.github.io/blob/main/notebooks/liquidity-owls.ipynb"
notebook: "/notebooks/liquidity-owls.ipynb"
app: "/apps/liquidity-owls/index.html"
appHeight: 1250
---

The interactive demo above runs on the paper's precomputed estimates — the
full tick-data computation (over a billion Nasdaq ITCH quote records) runs
offline; the notebook documents the pipeline end to end.
