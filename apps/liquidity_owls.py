import marimo

app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt

    return mo, np, plt


@app.cell
def _():
    # Precomputed estimates from the paper (Table: optimal daily volatility).
    # Columns: mu0, mu1, mu2, eta1^2, eta2^2, rho = eta12/(eta1*eta2), phi, w1*, w2*
    DATA = {
        "SPY": (0.74, 0.36, 0.63, 0.48, 0.82, 0.32, 0.71, 0.60, 0.84),
        "QQQ": (1.27, 0.59, 1.11, 1.16, 1.76, 0.34, 0.79, 0.45, 0.90),
        "DIA": (0.67, 0.32, 0.58, 0.44, 0.68, 0.31, 0.76, 0.51, 0.88),
        "AAPL": (2.04, 0.96, 1.94, 4.01, 4.15, 0.39, 0.93, 0.14, 0.98),
        "AMGN": (1.33, 0.37, 1.80, 0.68, 3.56, 0.33, 0.92, 0.27, 0.68),
        "AMZN": (2.65, 1.22, 2.52, 8.15, 6.12, 0.36, 0.97, 0.06, 1.02),
        "AXP": (2.21, 1.11, 2.16, 5.19, 6.06, 0.32, 0.86, 0.27, 0.88),
        "BA": (3.68, 1.53, 3.77, 11.42, 19.88, 0.41, 0.92, 0.19, 0.90),
        "CAT": (2.47, 1.16, 2.48, 5.28, 3.96, 0.30, 0.95, 0.10, 0.95),
        "CRM": (3.08, 1.39, 3.11, 7.69, 8.54, 0.31, 0.92, 0.18, 0.91),
        "CSCO": (1.37, 0.58, 1.46, 2.05, 2.53, 0.42, 0.99, 0.03, 0.93),
        "CVX": (2.02, 0.98, 2.00, 3.47, 5.26, 0.43, 0.88, 0.25, 0.89),
        "DIS": (1.88, 0.84, 1.96, 4.07, 4.42, 0.42, 0.98, 0.04, 0.95),
        "GOOGL": (2.23, 1.03, 2.13, 5.51, 3.58, 0.34, 0.98, 0.04, 1.03),
        "GS": (2.20, 0.98, 2.27, 3.45, 4.14, 0.37, 0.94, 0.13, 0.91),
        "HD": (1.55, 0.68, 1.70, 1.91, 2.60, 0.35, 0.94, 0.14, 0.86),
        "HON": (1.34, 0.57, 1.46, 1.46, 2.42, 0.34, 0.91, 0.20, 0.84),
        "IBM": (1.55, 0.69, 1.65, 3.63, 3.89, 0.38, 0.97, 0.06, 0.91),
        "JNJ": (0.85, 0.32, 1.05, 0.44, 1.11, 0.26, 0.88, 0.31, 0.72),
        "JPM": (1.75, 0.83, 1.68, 2.89, 3.01, 0.37, 0.92, 0.16, 0.96),
        "KO": (0.76, 0.28, 0.91, 0.42, 0.78, 0.36, 0.97, 0.08, 0.81),
        "MCD": (0.91, 0.37, 1.09, 0.66, 1.29, 0.34, 0.93, 0.18, 0.78),
        "MMM": (1.62, 0.66, 1.89, 1.60, 3.30, 0.33, 0.91, 0.23, 0.78),
        "MRK": (1.27, 0.48, 1.66, 1.00, 2.13, 0.31, 0.95, 0.13, 0.73),
        "MSFT": (1.74, 0.77, 1.70, 2.37, 3.12, 0.30, 0.88, 0.27, 0.90),
        "NKE": (2.24, 1.13, 2.08, 7.21, 4.17, 0.38, 0.98, 0.03, 1.06),
        "NVDA": (5.55, 2.43, 5.50, 19.08, 26.10, 0.33, 0.90, 0.24, 0.90),
        "PG": (0.84, 0.31, 1.11, 0.39, 1.48, 0.22, 0.83, 0.45, 0.63),
        "SHW": (1.95, 0.92, 2.09, 2.72, 4.04, 0.25, 0.85, 0.32, 0.79),
        "TRV": (1.65, 0.84, 1.76, 2.25, 3.19, 0.25, 0.82, 0.35, 0.77),
        "UNH": (1.87, 0.77, 2.14, 3.51, 5.35, 0.41, 0.98, 0.04, 0.86),
        "V": (1.44, 0.65, 1.53, 1.95, 2.88, 0.32, 0.89, 0.24, 0.84),
        "WMT": (0.98, 0.35, 1.20, 0.72, 1.68, 0.37, 0.96, 0.11, 0.78),
    }
    ETFS = ("SPY", "QQQ", "DIA")
    return DATA, ETFS


@app.cell
def _(mo):
    mo.md(
        r"""
        ## How much weight should the overnight return get?

        The whole-day variance estimator is $RV_t(\varphi) = \omega_1(\varphi)\, r_{1,t}^2 + \omega_2(\varphi)\, RV_{2,t}$
        — a weighted combination of the squared **overnight return** and the
        noise-corrected **intraday realized variance**. Among conditionally
        unbiased combinations, one importance factor $\varphi$ minimizes the
        mean-squared error.

        These are the estimates from the paper — 1-second Nasdaq quotes,
        2,034 trading days (2018–2026). **Pick an instrument, drag $\varphi$,
        and see why ignoring the overnight return is a mistake.**
        """
    )
    return


@app.cell
def _(DATA, mo):
    ticker = mo.ui.dropdown(
        options=list(DATA.keys()), value="SPY", label="Instrument"
    )
    phi_slider = mo.ui.slider(
        0.0, 1.0, value=0.5, step=0.01, label="Importance factor φ (your choice)"
    )
    mo.hstack([ticker, phi_slider], justify="start", gap=2)
    return phi_slider, ticker


@app.cell
def _(DATA, ETFS, mo, np, phi_slider, plt, ticker):
    mu0, mu1, mu2, eta1sq, eta2sq, rho, phi_star, w1_star, w2_star = DATA[
        ticker.value
    ]
    eta1, eta2 = np.sqrt(eta1sq), np.sqrt(eta2sq)

    def combo_sd(phi):
        w1 = (1 - phi) * mu0 / mu1
        w2 = phi * mu0 / mu2
        var = (
            w1**2 * eta1sq
            + w2**2 * eta2sq
            + 2 * w1 * w2 * rho * eta1 * eta2
        )
        return np.sqrt(var)

    grid = np.linspace(0.0, 1.0, 201)
    sds = np.array([combo_sd(p) for p in grid])
    phi_u = phi_slider.value

    fig, (ax1, ax2) = plt.subplots(
        1, 2, figsize=(9.5, 4.2), gridspec_kw={"width_ratios": [3, 2]}
    )

    ax1.plot(grid, sds, color="#2563eb", lw=2)
    ax1.scatter(
        [phi_star], [combo_sd(phi_star)], color="#16a34a", zorder=5,
        label=f"Optimal φ* = {phi_star:.2f}",
    )
    ax1.scatter(
        [phi_u], [combo_sd(phi_u)], color="#dc2626", zorder=5,
        label=f"Your φ = {phi_u:.2f}",
    )
    ax1.set_xlabel("Importance factor φ")
    ax1.set_ylabel("Std. dev. of the estimator (%²)")
    ax1.set_title(f"{ticker.value}: precision of RV(φ)")
    ax1.legend(frameon=False, fontsize=9)
    ax1.spines[["top", "right"]].set_visible(False)

    labels = ["Overnight ω₁", "Intraday ω₂"]
    w1_u = (1 - phi_u) * mu0 / mu1
    w2_u = phi_u * mu0 / mu2
    x = np.arange(2)
    ax2.bar(x - 0.18, [w1_star, w2_star], width=0.36, color="#16a34a",
            label="Optimal")
    ax2.bar(x + 0.18, [w1_u, w2_u], width=0.36, color="#dc2626", alpha=0.8,
            label="Yours")
    ax2.set_xticks(x, labels)
    ax2.set_title("Component weights")
    ax2.legend(frameon=False, fontsize=9)
    ax2.spines[["top", "right"]].set_visible(False)

    fig.tight_layout()

    kind = "index ETF" if ticker.value in ETFS else "DJIA equity"
    overnight_share = mu1 / (mu1 + mu2)
    loss = 100 * (combo_sd(phi_u) / combo_sd(phi_star) - 1)

    mo.vstack(
        [
            fig,
            mo.md(
                f"""
                **{ticker.value}** ({kind}): the overnight period carries
                ≈ **{overnight_share:.0%}** of measured daily variance
                (μ₁ = {mu1:.2f}, μ₂ = {mu2:.2f}). The optimal combination sets
                φ\* = {phi_star:.2f}, i.e. weights **ω₁\* = {w1_star:.2f}** on
                the squared overnight return and **ω₂\* = {w2_star:.2f}** on
                the intraday measure. Your current φ = {phi_u:.2f} gives an
                estimator whose standard deviation is **{loss:.1f}% above the
                optimum**.
                """
            ),
        ]
    )
    return


@app.cell
def _(DATA, ETFS, mo, np, plt):
    tickers_sorted = sorted(DATA.keys(), key=lambda t: DATA[t][7], reverse=True)
    w1s = [DATA[t][7] for t in tickers_sorted]
    colors = ["#2563eb" if t in ETFS else "#cbd5e1" for t in tickers_sorted]

    fig2, ax3 = plt.subplots(figsize=(9.5, 4.2))
    ax3.bar(np.arange(len(tickers_sorted)), w1s, color=colors)
    ax3.set_xticks(np.arange(len(tickers_sorted)), tickers_sorted,
                   rotation=90, fontsize=8)
    ax3.set_ylabel("Optimal overnight weight ω₁*")
    ax3.set_title(
        "Diversified ETFs (blue) earn overnight weights several times "
        "larger than single stocks"
    )
    ax3.spines[["top", "right"]].set_visible(False)
    fig2.tight_layout()

    mo.vstack(
        [
            fig2,
            mo.md(
                "A single stock's overnight return is dominated by "
                "idiosyncratic news, so it is noisy and gets shrunk toward "
                "zero. An ETF diversifies that noise away — its overnight "
                "return is informative enough to earn a weight of 0.45–0.60."
            ),
        ]
    )
    return


if __name__ == "__main__":
    app.run()
