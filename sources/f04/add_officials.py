"""One-off: place the remaining FM Ch 4 official questions into their topic blocks.

Run from the project root:  python sources/f04/add_officials.py
Each entry carries the data ICAI actually printed and the route its own answer follows.
Re-running is safe: an id already present is skipped.
"""
import json, io, os, sys

ENTRIES = [
 ("F04.22", {
   "id": "RTP-J25-FQ5", "status": "VERIFIED",
   "question": "The capital structure of Samyaktva Limited is: 12% debentures ₹3,50,000; 14% preference shares ₹4,50,000; equity shares of ₹10 each ₹8,50,000; total ₹16,50,000. The ₹100 debentures are redeemable at a premium of 6% with a floatation cost of 5% and 5 years to maturity; the current market price is ₹115. The ₹100 preference shares are redeemable at a premium of 10%, were issued at a discount of 2% with a floatation cost of 5% on the issue price, have a current market price of ₹108 and 10 years to maturity. An equity share has a floatation cost of ₹5 with a current market price of ₹30; the last dividend was ₹4 and an annual growth is expected. Compute the cost of each source and the weighted average cost of capital.",
   "answer_points": [
    "**Cost of debentures (SM §5.3).** Kd = [I(1 − t) + (RV − NP) ÷ n] ÷ [(RV + NP) ÷ 2], with I = ₹12, RV = ₹106 (par plus the 6% premium), NP = the market price of ₹115 less 5% floatation cost, and n = 5 years.",
    "**Cost of preference shares (SM §6.2).** Kp = [PD + (RV − NP) ÷ n] ÷ [(RV + NP) ÷ 2], with PD = ₹14, RV = ₹110 (par plus the 10% premium), NP = the issue price of ₹98 less 5% floatation cost on that issue price, and n = 10 years. **No (1 − t)** applies.",
    "**Cost of equity (SM §7.3).** Ke = D1 ÷ (P0 − F) + g, with D0 = ₹4 grossed up to D1 = ₹4(1 + g), P0 = ₹30 and F = ₹5.",
    "**Weighted average cost of capital (SM §9).** Weight the three sources on book values of ₹3,50,000, ₹4,50,000 and ₹8,50,000 against the total of ₹16,50,000, multiply each by its cost, and aggregate.",
    "This question is unusually rich because **every source carries both a premium and a floatation cost** — read each adjustment before substituting, and note that the floatation cost on the preference shares is on the issue price, not the market price."
   ],
   "conclusion": "Three costs and a weighted average; the premium and floatation adjustments carry the marks.",
   "keywords": ["redeemable at a premium", "floatation cost", "issue price", "weighted average"]}),

 ("F04.22", {
   "id": "RTP-M25-FQ5", "status": "VERIFIED",
   "question": "Paramhans Limited's capital structure consists of equity share capital ₹25,00,000 (face value ₹100), reserves and surplus ₹10,00,000, a bank term loan ₹10,00,000, debentures ₹15,00,000 (face value ₹100) redeemable at a premium of 5%, and preference share capital ₹20,00,000 (face value ₹100) redeemable at a premium of 5%; total ₹80,00,000. The coupon rate on debentures is 1.5 times that of the bank term loan, and the preference dividend rate is 1.5 times the debentures' interest rate. Tenure for the bank term loan, debentures and preference share capital is 3, 5 and 7 years respectively. Tax is 25%. Compute the weighted average cost of capital.",
   "answer_points": [
    "**Step 1 — derive the rates from the relationships.** If the bank term loan rate is x, the debenture coupon is 1.5x and the preference dividend rate is 1.5 × 1.5x = 2.25x. One rate must be given or derivable; express the other two from it.",
    "**Step 2 — cost of the bank term loan (SM §5).** The cost of a loan from a financial institution is computed like redeemable debt: Kd = x(1 − 0.25) where it is repaid at par, or the averaging formula over the 3-year tenure.",
    "**Step 3 — cost of debentures.** Kd = [I(1 − t) + (RV − NP) ÷ n] ÷ [(RV + NP) ÷ 2], with RV = ₹105 (par plus 5% premium) and n = 5 years.",
    "**Step 4 — cost of preference shares.** Kp = [PD + (RV − NP) ÷ n] ÷ [(RV + NP) ÷ 2], with RV = ₹105 and n = 7 years, and **no tax adjustment**.",
    "**Step 5 — cost of equity and retained earnings.** Ke and Kr are computed on the given market data; reserves and surplus of ₹10,00,000 are treated as retained earnings, whose cost uses the current market price with no floatation deduction (SM §8).",
    "**Step 6 — WACC.** Weight the five sources on the book values given and aggregate the products in a four-column table."
   ],
   "conclusion": "Five sources, three different tenures, one relationship chain — derive the rates before anything else.",
   "keywords": ["1.5 times", "redeemable at a premium", "reserves and surplus", "weighted average"]}),

 ("F04.22", {
   "id": "RTP-M26-FQ5", "status": "VERIFIED",
   "question": "Zebra Dynamics Ltd. states that its cost of capital based on book value weights is 11%, while the cost of capital based on market value weights is exactly 150 basis points higher. Two comparable peers driven by CAPM show: A Ltd. beta 1.2 with an expected return of 15.20%, and B Ltd. beta 0.8 with an expected return of 12.80%. In book value terms the company maintains an equal ratio of equity and debt; in market value terms its equity trades at a premium. Compute the missing figures.",
   "answer_points": [
    "**Step 1 — recover Rf and the market risk premium from the two peers.** CAPM gives 15.20% = Rf + 1.2 × (Rm − Rf) and 12.80% = Rf + 0.8 × (Rm − Rf). Subtracting, 2.40% = 0.4 × (Rm − Rf), so the **market risk premium is 6%**; substituting back, Rf = 15.20% − 1.2 × 6% = **8%**.",
    "**Step 2 — cost of equity of Zebra Dynamics.** Apply Ke = Rf + β(Rm − Rf) with the company's own beta.",
    "**Step 3 — book value WACC.** With an equal ratio of equity and debt, 11% = 0.5 Ke + 0.5 Kd, which yields the cost of debt once Ke is known.",
    "**Step 4 — market value WACC.** The market value cost of capital is 11% + 1.50% = **12.5%**. Because the equity trades at a premium, the equity weight is higher at market value than at book value, which is why the market value WACC exceeds the book value WACC.",
    "**The principle (SM §9.1).** Market value weight is more correct and represents a firm's capital structure; where equity is the dearer source and trades at a premium, shifting to market value weights raises the weighted average."
   ],
   "conclusion": "A simultaneous-equations question dressed as CAPM; two peers give you Rf and the premium.",
   "keywords": ["basis points", "market risk premium", "book value weights", "market value weights"]}),

 ("F04.22", {
   "id": "RTP-S24-FQ5", "status": "VERIFIED",
   "question": "BS Ltd. has the following capital structure at book value as on 31st March 2024: equity share capital (10,00,000 shares) ₹3,00,00,000; 11.5% preference shares ₹60,00,000; 10% debentures ₹1,00,00,000; total ₹4,60,00,000. The equity shares are sold for ₹300. The company is expected to pay next year a dividend of ₹15 per equity share, expected to grow by 5% per annum forever. Tax is 35%. (i) Compute the WACC based on the existing capital structure. (ii) Compute the new WACC if the company raises an additional ₹50 lakh of debt by issuing 10-year 12% debentures, where the yield on debentures of similar maturity and risk class is 13% and floatation cost is 2%.",
   "answer_points": [
    "**(i) Existing WACC.** Ke = D1 ÷ P0 + g = ₹15 ÷ ₹300 + 0.05 = 0.05 + 0.05 = **10%**. Kp = 11.5% (irredeemable, no tax adjustment). Kd = 10% × (1 − 0.35) = **6.5%**.",
    "ICAI's own table weights these as equity ₹3,00,00,000 at 0.652 × 10.00% = 6.52; 11.5% preference ₹60,00,000 at 0.130 × 11.50%; and the debentures at their weight — aggregating to the existing WACC.",
    "**(ii) New WACC.** The new debentures are issued at a price that yields 13% to investors, less 2% floatation cost, so the net proceeds are below par; Kd on the new tranche = [I(1 − t) + (RV − NP) ÷ n] ÷ [(RV + NP) ÷ 2] with I = ₹12, n = 10 years.",
    "ICAI's second table shows the equity line re-weighted at 0.588 with a cost of 13.00%, because the extra debt changes both the weights and the shareholders' required return.",
    "Recomputing the WACC before and after a change in the structure is the most common form of this question across the RTPs and MTPs."
   ],
   "conclusion": "Two tables; the second changes both weights and costs, not just weights.",
   "keywords": ["D1 ÷ P0 + g", "irredeemable preference", "yield on similar debentures", "floatation cost"]}),

 ("F04.22", {
   "id": "RTP-S26-FQ1", "status": "VERIFIED", "format": "Case MCQs",
   "question": "AURO Engineering Pvt. Ltd. had, as on 31st March 2026, a capital structure at book value of equity share capital (1,00,00,000 shares) ₹30,00,00,000, preference shares and long-term debentures. The company is considering additional debt financing to take advantage of financial leverage and the tax benefits of debt. Answer five questions: the existing cost of equity; the existing weighted average cost of capital; the revised cost of equity after raising additional debt; the after-tax cost of the newly issued debentures; and the revised weighted average cost of capital.",
   "answer_points": [
    "**Existing cost of equity.** ICAI's answer applies the dividend growth model: Ke = D1 ÷ P0 + g = ₹15 ÷ ₹300 + 0.05 = 0.05 + 0.05 = **10%**.",
    "**Cost of preference shares.** Kp = 11.5 ÷ 100 = **11.5%**, with no tax adjustment.",
    "**After-tax cost of the existing debentures.** Kd = 10% × (1 − 0.35) = **6.5%**.",
    "**Existing WACC.** ICAI's table weights equity, preference and debentures on their book values to give **9.12%** on the figures published.",
    "**Revised figures after the additional debt.** The revised capital structure shows equity share capital ₹30,00,00,000 and preference shares ₹6,00,00,000 alongside the enlarged debt; the **revised Ke rises to 10.20%**, the **after-tax cost of the new debentures is 8.40%**, and the **revised WACC is 11.62%** — so the extra debt raises rather than lowers the overall cost, because the shareholders' required return rises with the financial risk.",
    "This five-part case scenario is the format ICAI then used in the January 2026 examination itself, which makes it the single best rehearsal for the chapter."
   ],
   "conclusion": "Five one-mark parts; the lesson is that more debt need not reduce the WACC once Ke responds.",
   "keywords": ["dividend growth model", "after-tax cost of debentures", "revised cost of equity", "revised WACC"]}),

 ("F04.22", {
   "id": "MTP-J26-S1-FQ1a", "marks": 5, "status": "VERIFIED",
   "question": "Divine Limited has the following capital structure, which it considers optimal: debt 25%, preference shares 15%, equity shares 60%. Its expected net income this year is ₹34,285.72, its established dividend payout ratio is 30%, its tax rate is 40%, and investors expect earnings and dividends to grow at a constant rate of 9% in future. It paid a dividend of ₹3.60 per share last year and its shares currently sell at ₹54 per share. New preference shares with a dividend of ₹11 can be sold at ₹95 per share, and debt can be sold at an interest rate of 12%. Compute the component costs and the marginal cost of capital.",
   "answer_points": [
    "**Cost of debt.** Kd = I(1 − t) = 12% × (1 − 0.40) = **7.2%** after tax, the debt being sold at par.",
    "**Cost of preference shares.** Kp = PD ÷ P0 = ₹11 ÷ ₹95 = **11.58%**, with no tax adjustment.",
    "**Cost of equity from retained earnings.** Ke = D1 ÷ P0 + g = ₹3.60(1 + 0.09) ÷ ₹54 + 0.09 = ₹3.924 ÷ ₹54 + 0.09 = 0.0727 + 0.09 = **16.27%**.",
    "**Retained earnings available.** Net income ₹34,285.72 with a 30% payout means **70% is retained = ₹24,000 (approximately)**. Since equity is 60% of the structure, the total capital that can be raised before new shares must be sold is ₹24,000 ÷ 0.60 = **₹40,000**.",
    "**Marginal cost of capital.** Weight the three component costs at the intended proportions of 25%, 15% and 60%: (0.25 × 7.2%) + (0.15 × 11.58%) + (0.60 × 16.27%) = 1.80% + 1.737% + 9.762% = **13.30%**.",
    "**Beyond ₹40,000** the company must issue new equity, whose cost is higher because of floatation cost, so the marginal cost of capital steps up (SM §10)."
   ],
   "conclusion": "Three costs, one break point, two marginal costs — the structure of every marginal cost question.",
   "keywords": ["optimal capital structure", "payout ratio", "retained earnings", "marginal cost of capital"]}),

 ("F04.22", {
   "id": "MTP-M24-S1-FQ3a", "marks": 8, "status": "VERIFIED",
   "question": "Ram Ltd. evaluates all its capital projects using a discounting rate of 16%. Its capital structure consists of equity share capital, retained earnings, a bank term loan and debentures redeemable at par. The rate of interest on the bank term loan is 1.4 times that of the debenture. The remaining tenure of the debentures and the bank loan is 4 years and 6 years respectively. The book value of equity share capital, retained earnings and the bank loan is ₹20,00,000, ₹30,00,000 and ₹20,00,000 respectively. Debentures of book value ₹30,00,000 are currently trading at ₹98 per debenture. The ongoing P/E multiple for the shares stands at 4. Tax is 30%. Calculate the rate of interest on the bank loan and on the debentures.",
   "answer_points": [
    "**The 16% discounting rate is the company's cost of capital** — SM §2 says cost of capital is also known as the cut-off rate — so the WACC equation can be solved backwards for the unknown interest rates.",
    "**Cost of equity and retained earnings from the P/E multiple.** A P/E of 4 implies an earnings yield of 1 ÷ 4 = **25%**, which under the earnings price approach (SM §7.2) is the cost of equity: Ke = E ÷ P. Kr takes the same figure, the market price being used with no floatation adjustment.",
    "**Set up the WACC equation.** Total capital = ₹20,00,000 + ₹30,00,000 + ₹20,00,000 + ₹30,00,000 = **₹1,00,00,000**, with weights 0.20, 0.30, 0.20 and 0.30. So 16% = (0.20 × 25%) + (0.30 × 25%) + (0.20 × Kd bank) + (0.30 × Kd debenture).",
    "**Express one rate in terms of the other.** The bank loan rate is 1.4 times the debenture rate, and each cost is computed after tax: the bank loan at par gives Kd = 1.4r(1 − 0.30), while the debentures trading at ₹98 use the redeemable formula over 4 years.",
    "**Solve.** Substituting leaves a single unknown r, the debenture interest rate; the bank loan rate is then 1.4r.",
    "This question reverses the usual direction — you are given the WACC and asked for a component cost — which is why it carries 8 marks."
   ],
   "conclusion": "Work the P/E into a cost of equity first; everything else is one equation in one unknown.",
   "keywords": ["discounting rate", "P/E multiple", "earnings price approach", "1.4 times"]}),

 ("F04.22", {
   "id": "MTP-M25-S1-FQ2a", "marks": 5, "status": "VERIFIED",
   "question": "Q Ltd. has the following capital structure at book value as on 31st March 2024: equity share capital (10,00,000 shares) ₹4,00,00,000; 12% preference shares ₹80,00,000; 11% debentures ₹2,00,00,000; total ₹6,80,00,000. The equity shares are sold for ₹400. Next year the company will pay a dividend of ₹20 per equity share, expected to grow by 5% per annum forever. Tax is 30%. (i) Compute the WACC based on the existing capital structure. (ii) Compute the new WACC if the company raises an additional ₹50 lakh of debt by issuing 12% debentures, which would increase the expected equity dividend to ₹25.",
   "answer_points": [
    "**(i) Existing WACC.** Ke = D1 ÷ P0 + g = ₹20 ÷ ₹400 + 0.05 = 0.05 + 0.05 = **10%**. Kp = **12%** (irredeemable, no tax adjustment). Kd = 11% × (1 − 0.30) = **7.7%**.",
    "Weights: equity ₹4,00,00,000 ÷ ₹6,80,00,000 = **0.5882**; preference ₹80,00,000 ÷ ₹6,80,00,000 = **0.1176**; debentures ₹2,00,00,000 ÷ ₹6,80,00,000 = **0.2941**.",
    "**WACC = (0.5882 × 10%) + (0.1176 × 12%) + (0.2941 × 7.7%) = 5.882% + 1.412% + 2.265% = 9.56%.**",
    "**(ii) New WACC.** The new ₹50 lakh of 12% debentures costs 12% × (1 − 0.30) = **8.4%**; total capital becomes ₹7,30,00,000; and the expected dividend rises to ₹25, so the new Ke = ₹25 ÷ ₹400 + 0.05 = **11.25%** (assuming the market price is unchanged).",
    "Recompute the weights on ₹7,30,00,000 and aggregate again. Note that **both the weights and the cost of equity change**, which is the point of the second part."
   ],
   "conclusion": "Two tables; the second must re-derive Ke as well as the weights.",
   "keywords": ["D1 ÷ P0 + g", "existing WACC", "new WACC", "re-weighted"]}),

 ("F04.22", {
   "id": "MTP-S24-S2-FQ3a", "marks": 5, "status": "VERIFIED",
   "question": "Calculate the WACC using market value weights from: equity shares (₹10 per share) ₹15,00,000; reserves and surplus ₹5,00,000; preference shares (₹100 each) ₹7,50,000; debentures (₹100 each) ₹5,50,000. Market prices: debentures ₹105, preference shares ₹115, equity shares ₹27. The ₹100 debentures are redeemable at a premium of 10%, carry a 10% coupon, have 4% floatation cost and 10 years to maturity. The ₹100 preference shares are redeemable at par, carry a 12% coupon, have 2% floatation cost and 10 years to maturity. Equity shares have ₹4.5 of floatation cost.",
   "answer_points": [
    "**Cost of debentures (SM §5.3).** Kd = [I(1 − t) + (RV − NP) ÷ n] ÷ [(RV + NP) ÷ 2], with I = ₹10, RV = ₹110, NP = ₹105 less 4% floatation cost, and n = 10 years.",
    "**Cost of preference shares (SM §6.2).** Kp = [PD + (RV − NP) ÷ n] ÷ [(RV + NP) ÷ 2], with PD = ₹12, RV = ₹100, NP = ₹115 less 2% floatation cost, and n = 10 years. No tax adjustment applies.",
    "**Cost of equity and retained earnings (SM §§7.3 and 8).** Ke uses the market price of ₹27 less the ₹4.5 floatation cost; Kr uses the ₹27 market price with **no** floatation deduction.",
    "**Apportioning the market value of equity (SM §9.1).** There is no separate market value for reserves and surplus. Book values are ₹15,00,000 equity capital and ₹5,00,000 reserves, a ratio of **3:1**. Market value of the shares = 1,50,000 shares × ₹27 = **₹40,50,000**, split **₹30,37,500** to equity capital and **₹10,12,500** to reserves.",
    "**WACC table.** Market values are then equity ₹30,37,500, reserves ₹10,12,500, preference 7,500 shares × ₹115 = ₹8,62,500, and debentures 5,500 × ₹105 = ₹5,77,500. Weight each, multiply by its cost, and aggregate.",
    "This is the clearest illustration in the whole set of why reserves need a market value of their own even though they have no market price."
   ],
   "conclusion": "The apportionment of the share price between capital and reserves is the examinable step.",
   "keywords": ["market value weights", "apportioned in the ratio", "floatation cost", "redeemable at a premium"]}),

 ("F04.22", {
   "id": "MTP-S25-S2-FQ1c", "marks": 5, "status": "VERIFIED",
   "question": "ABC Ltd. has the following capital structure, considered optimum as on 31st March 2025: 14% debentures ₹60,000; 11% preference shares ₹20,000; equity shares (10,000 shares) ₹3,20,000; total ₹4,00,000. The share has a market price of ₹19.67. Next year's dividend per share is 50% of the 2024 EPS. EPS has followed a uniform trend for ten years, from ₹1.00 in 2015 to ₹2.36 in 2024, which is expected to continue. New debentures carry 16% interest and the current market price of a debenture is ₹96. Preference shares of ₹9.20 (with an annual dividend of ₹1.1 per share) were also issued. The company is in the 50% tax bracket. Compute the after-tax cost of new debt, new preference shares and new equity, and the marginal cost of capital.",
   "answer_points": [
    "**Cost of new debt.** Kd = I(1 − t) ÷ P0 = ₹16(1 − 0.5) ÷ ₹96 = ₹8 ÷ ₹96 = **0.0833, or 8.33%**.",
    "**Cost of new preference shares.** Kp = PD ÷ P0 = ₹1.10 ÷ ₹9.20 = **0.12, or 12%**, with no tax adjustment.",
    "**Growth rate from the uniform EPS trend.** g = (EPS 2016 − EPS 2015) ÷ EPS 2015 = (₹1.10 − ₹1.00) ÷ ₹1.00 = **0.10, or 10%**, and the trend confirms it across the decade.",
    "**Next year's dividend.** D1 = 50% of the 2024 EPS = 50% of ₹2.36 = **₹1.18**.",
    "**Cost of new equity (from retained earnings).** Ke = D1 ÷ P0 + g = ₹1.18 ÷ ₹19.67 + 0.10 = 0.06 + 0.10 = **0.16, or 16%**.",
    "**Marginal cost of capital.** Weight the three costs at 0.15 debenture, 0.05 preference and 0.80 equity (the proportions of ₹60,000, ₹20,000 and ₹3,20,000 in ₹4,00,000): (0.15 × 8.33%) + (0.05 × 12%) + (0.80 × 16%) = 1.25% + 0.60% + 12.80% = **14.65%** on those weights.",
    "The study material's own Illustration 18 works this identical question with a market price of ₹23.60; the MTP simply reprices the share."
   ],
   "conclusion": "The uniform EPS trend gives g, and half the last EPS gives D1 — those two steps unlock everything.",
   "keywords": ["uniform trend", "growth rate", "50% of EPS", "marginal cost of capital"]}),

 ("F04.22", {
   "id": "MTP-S26-S1-FQ1c", "status": "VERIFIED",
   "question": "From the Sep 2026 Series I mock test paper: compute the weighted average cost of capital using market value weights, given 10% debentures of ₹105 each (5,000 debentures) and 5% preference shares, alongside equity whose cost was computed in part (b).",
   "answer_points": [
    "**Market values.** ICAI's answer file shows the 10% debentures at ₹105 × 5,000 = **₹5,25,000**, carrying a weight of 0.151 and a product of 0.0104 in the WACC table, with the 5% preference shares and equity weighted alongside.",
    "**Costs carried forward from part (b).** Ke = D1 ÷ (P0 − F) + g = ₹1 ÷ (₹24 − ₹4) + 0.05 = **10%**; the cost of debt and of preference capital are computed on their own market values net of any issue expenses.",
    "**Method (SM §9).** Total the market values, express each source as a proportion of that total, multiply each proportion by its cost, and aggregate — the four-step WACC routine.",
    "**Why market values (SM §9.1).** Market value weight is more correct and represents a firm's capital structure; it is preferable to use market value weights for equity, and reserves are ignored separately because they are in effect incorporated into the value of equity.",
    "Only the answer file of this mock test paper is on the ICAI portal; the question wording above is reconstructed from it."
   ],
   "conclusion": "A standard market-value WACC table; the costs come from the preceding part.",
   "keywords": ["market value weights", "weights and products", "four-step routine"]}),
]


def main():
    root = 'sources/f04'
    files = {f: json.load(io.open(os.path.join(root, f), encoding='utf-8'))
             for f in ('u1.json', 'u2.json', 'u3.json')}
    index = {}
    for fname, data in files.items():
        for blk in data.get('concepts', []):
            for part in [p.strip() for p in blk['code'].split('+')]:
                index.setdefault(part, blk)
    added = skipped = 0
    for code, entry in ENTRIES:
        if code not in index:
            sys.exit(f'no block for {code}')
        oq = index[code].setdefault('official_questions', [])
        if any(q.get('id') == entry['id'] for q in oq):
            skipped += 1
            continue
        oq.append(entry)
        added += 1
    for fname, data in files.items():
        json.dump(data, io.open(os.path.join(root, fname), 'w', encoding='utf-8'),
                  ensure_ascii=False, indent=1)
    print(f'added {added}, already present {skipped}')


if __name__ == '__main__':
    main()
