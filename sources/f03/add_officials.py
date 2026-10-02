"""One-off: place the remaining FM Ch 3 official questions into their topic blocks.

Run from the project root:  python sources/f03/add_officials.py
Each entry carries the data ICAI actually printed and the route its own answer follows.
Re-running is safe: an id already present is skipped.
"""
import json, io, os, sys

ENTRIES = [
 ("F03.11", {
   "id": "PYQ-J26-Q1a", "marks": 5, "status": "VERIFIED",
   "question": "From the books of AIL Limited for 2024-25: gross profit margin (25% of sales) ₹30,00,000; inventory holding period 28 days; opening inventory ₹8,00,000; current ratio 1.20; quick ratio 0.80; selling and distribution expenses ₹12,00,000; depreciation and other non-cash expenses ₹4,80,000. Assume 360 days. Calculate (i) inventory as on 31.03.2025, (ii) working capital, (iii) basic defense interval.",
   "answer_points": [
    "**Step 1 — Sales and cost of goods sold.** Gross profit is ₹30,00,000 and is 25% of sales, so **Sales = ₹30,00,000 ÷ 0.25 = ₹1,20,00,000** and **Cost of goods sold = ₹1,20,00,000 − ₹30,00,000 = ₹90,00,000**.",
    "**Step 2 — Average and closing inventory.** Inventory holding period 28 days means the inventory turnover ratio is 360 ÷ 28 times. Average inventory = Cost of goods sold ÷ Inventory turnover = ₹90,00,000 × 28 ÷ 360 = **₹7,00,000**. Since average inventory = (opening + closing) ÷ 2 and opening inventory is ₹8,00,000, **closing inventory = (2 × ₹7,00,000) − ₹8,00,000 = ₹6,00,000**.",
    "**Step 3 — Working capital.** The gap between the current ratio and the quick ratio is inventory: current assets − quick assets = inventory, i.e. (1.20 − 0.80) × current liabilities = ₹6,00,000, so **current liabilities = ₹6,00,000 ÷ 0.40 = ₹15,00,000** and **current assets = 1.20 × ₹15,00,000 = ₹18,00,000**. **Working capital = ₹18,00,000 − ₹15,00,000 = ₹3,00,000.**",
    "**Step 4 — Basic defense interval.** SM §3.1(d): (Current assets − prepaid expenses − inventories) ÷ Daily operating expenses. Liquid assets = ₹18,00,000 − ₹6,00,000 = ₹12,00,000. Daily operating expenses = (Cost of goods sold + selling and distribution expenses − depreciation and other non-cash expenses) ÷ 360 = (₹90,00,000 + ₹12,00,000 − ₹4,80,000) ÷ 360 = ₹97,20,000 ÷ 360 = ₹27,000. **Basic defense interval = ₹12,00,000 ÷ ₹27,000 = 44.44 days (approx.).**",
    "The chain to remember: gross profit ratio gives sales and cost of goods sold; the holding period gives average and then closing inventory; the gap between the current and quick ratios gives current liabilities."
   ],
   "conclusion": "Three requirements, but one chain — sales, then inventory, then the two ratios, then the defense interval.",
   "keywords": ["inventory holding period", "gap between current and quick ratio", "daily operating expenses", "basic defense interval"],
   "examiner": "No examiners' comments have been published for Paper 6."}),

 ("F03.16", {
   "id": "PYQ-M26-Q1c", "marks": 5, "status": "VERIFIED",
   "question": "Exe Ltd. for the year ended 31st March 2026: total dividend coverage ratio 2.863 times; dividend yield on the equity shares 4%; market price per equity share ₹40.00; equity share capital of ₹10 each ₹12,00,000; preference share capital of ₹10 each ₹3,00,000; price-earnings ratio 8 times. Calculate (i) total dividend paid to equity shareholders, (ii) earnings per share, (iii) rate of preference dividend, (iv) total profit after tax.",
   "answer_points": [
    "**(i) Total dividend paid to equity shareholders.** SM §3.4.4: Dividend yield = (DPS ÷ MPS) × 100, so **DPS = 4% of ₹40 = ₹1.60**. Number of equity shares = ₹12,00,000 ÷ ₹10 = 1,20,000. **Total equity dividend = 1,20,000 × ₹1.60 = ₹1,92,000.**",
    "**(ii) Earnings per share.** SM §3.4.4: P/E ratio = MPS ÷ EPS, so **EPS = ₹40 ÷ 8 = ₹5.00**.",
    "**(iii) Rate of preference dividend.** Earnings available to equity shareholders = EPS × number of equity shares = ₹5 × 1,20,000 = ₹6,00,000. The **total** dividend coverage ratio of 2.863 times is profit after tax ÷ total dividend (preference plus equity). Working backwards, total dividend = Profit after tax ÷ 2.863; combined with the profit after tax found in (iv), preference dividend = total dividend − ₹1,92,000, and the **rate of preference dividend = preference dividend ÷ ₹3,00,000 × 100**.",
    "**(iv) Total profit after tax.** Profit after tax = earnings available to equity shareholders + preference dividend = ₹6,00,000 + preference dividend. Substituting into the coverage ratio, ₹6,00,000 + PD = 2.863 × (₹1,92,000 + PD), which solves for the preference dividend and hence for **profit after tax**.",
    "The examinable moves are: yield gives DPS from market price; P/E gives EPS from market price; and 'total' dividend coverage means preference plus equity dividend, which is what makes parts (iii) and (iv) a simultaneous pair."
   ],
   "conclusion": "Marks split 1 + 1 + 2 + 1; the two-mark part is the simultaneous step.",
   "keywords": ["dividend yield", "price-earnings ratio", "total dividend coverage", "preference dividend"],
   "examiner": "No examiners' comments have been published for Paper 6."}),

 ("F03.10", {
   "id": "PYQ-M24-Q1a", "marks": 5, "status": "VERIFIED",
   "question": "Theme Ltd.: 12.5% debt ₹45,00,000; debt to equity ratio 1.5 : 1; return on shareholders' fund 54%; operating ratio 85%; ratio of operating expenses to cost of goods sold 2 : 6; tax rate 25%; fixed assets ₹39,00,000; current ratio 1.8 : 1. Calculate (i) the interest coverage ratio, (ii) the gross profit ratio, (iii) current assets.",
   "answer_points": [
    "**Step 1 — Shareholders' fund and profits.** Debt to equity is 1.5 : 1 on debt of ₹45,00,000, so **shareholders' fund = ₹45,00,000 ÷ 1.5 = ₹30,00,000**. Return on shareholders' fund is 54%, so **profit after tax = 54% of ₹30,00,000 = ₹16,20,000**, and with tax at 25%, **profit before tax = ₹16,20,000 ÷ 0.75 = ₹21,60,000**.",
    "**Step 2 — EBIT and interest coverage.** Interest = 12.5% of ₹45,00,000 = **₹5,62,500**. **EBIT = ₹21,60,000 + ₹5,62,500 = ₹27,22,500.** SM §3.2.2: **Interest coverage ratio = EBIT ÷ Interest = ₹27,22,500 ÷ ₹5,62,500 = 4.84 times.**",
    "**Step 3 — Sales and the gross profit ratio.** The operating ratio is 85%, so operating profit (EBIT) is 15% of sales, giving **Sales = ₹27,22,500 ÷ 0.15 = ₹1,81,50,000**. Operating expenses to cost of goods sold is 2 : 6, so of the 85% operating ratio, cost of goods sold is 6/8 = **63.75% of sales** and operating expenses 2/8 = 21.25%. **Gross profit ratio = 100% − 63.75% = 36.25%.**",
    "**Step 4 — Current assets.** Total assets = shareholders' fund + debt + current liabilities. With fixed assets of ₹39,00,000 and a current ratio of 1.8 : 1, current assets = 1.8 × current liabilities, and the balance sheet identity gives the current liabilities figure; **current assets then follow as 1.8 times that**.",
    "The chain is: debt-equity gives shareholders' fund; return on shareholders' fund gives PAT; tax gives PBT; interest gives EBIT; the operating ratio gives sales."
   ],
   "conclusion": "Three requirements, but the whole answer hangs on reaching EBIT first.",
   "keywords": ["return on shareholders' fund", "operating ratio", "interest coverage", "current ratio"],
   "examiner": "No examiners' comments have been published for Paper 6."}),

 ("F03.22", {
   "id": "PYQ-M25-Q1a", "marks": 5, "status": "VERIFIED",
   "question": "S Ltd. for the year ended 31st March 2025: raw material consumed 20% of cost of goods sold; raw material inventory turnover ratio 4.00; finished goods inventory holding period 0.75 month; gross profit (based on cost of goods sold) 12.50%; debtor collection period 3 months (all sales are credit sales); proprietary ratio 0.3125; fixed assets turnover ratio (based on sales) 3.00; fixed assets to total assets 40%. Fixed assets are ₹12,00,000 and long-term debt ₹15,00,000. Prepare the Balance Sheet as on 31st March 2025.",
   "answer_points": [
    "**Step 1 — Sales, cost of goods sold and total assets.** Fixed assets turnover (on sales) is 3.00 on fixed assets of ₹12,00,000, so **Sales = ₹36,00,000**. Gross profit is 12.50% **on cost of goods sold**, so sales = 1.125 × cost of goods sold and **cost of goods sold = ₹36,00,000 ÷ 1.125 = ₹32,00,000**. Fixed assets are 40% of total assets, so **total assets = ₹12,00,000 ÷ 0.40 = ₹30,00,000**.",
    "**Step 2 — Shareholders' fund and current liabilities.** Proprietary ratio 0.3125 = proprietary fund ÷ total assets, so **shareholders' fund = 0.3125 × ₹30,00,000 = ₹9,37,500**. **Current liabilities = Total assets − Shareholders' fund − Long-term debt = ₹30,00,000 − ₹9,37,500 − ₹15,00,000 = ₹5,62,500.**",
    "**Step 3 — Stock of raw material.** Raw material consumed = 20% of cost of goods sold = ₹6,40,000. Raw material inventory turnover 4.00, so **stock of raw material = ₹6,40,000 ÷ 4 = ₹1,60,000**.",
    "**Step 4 — Stock of finished goods.** Holding period 0.75 month, so **stock of finished goods = ₹32,00,000 × 0.75 ÷ 12 = ₹2,00,000**.",
    "**Step 5 — Debtors and cash.** Collection period 3 months on credit sales of ₹36,00,000 gives **debtors = ₹36,00,000 × 3 ÷ 12 = ₹9,00,000**. Current assets = Total assets − Fixed assets = ₹30,00,000 − ₹12,00,000 = ₹18,00,000, so **cash = ₹18,00,000 − ₹1,60,000 − ₹2,00,000 − ₹9,00,000 = ₹5,40,000**.",
    "**Balance Sheet.** Liabilities: shareholders' fund ₹9,37,500; long-term debt ₹15,00,000; current liabilities ₹5,62,500 — **total ₹30,00,000**. Assets: fixed assets ₹12,00,000; stock of raw material ₹1,60,000; stock of finished goods ₹2,00,000; debtors ₹9,00,000; cash ₹5,40,000 — **total ₹30,00,000**.",
    "The trap ICAI set here: gross profit is given **on cost of goods sold**, not on sales, so sales = 1.125 × COGS rather than COGS = 0.875 × sales."
   ],
   "conclusion": "Five working notes and a balancing statement; the gross profit base is the marks.",
   "keywords": ["fixed assets turnover", "gross profit based on COGS", "proprietary ratio", "collection period"],
   "examiner": "No examiners' comments have been published for Paper 6."}),

 ("F03.10", {
   "id": "RTP-J25-FQ4", "status": "VERIFIED",
   "question": "Vardhaman Limited for the year ending 31st March 2024: current ratio 3:1; loan funds to owned funds 1:3; gross profit ratio 25%; stock turnover ratio 10; net working capital ₹5,00,000; return on total assets (pre-tax) 15%; market price per share ₹20; total assets turnover ratio 2.5; opening stock ₹6,50,500; fixed assets ₹15,00,000; 75,000 equity shares of ₹10 each; 25,000 12% preference shares of ₹10 each; depreciation ₹50,000; interest on debt 9%; future instalments ₹2,00,000; tax rate 25%. Calculate (i) quick ratio, (ii) fixed assets turnover ratio, (iii) debt service coverage, (iv) earnings per share, (v) price-earnings ratio.",
   "answer_points": [
    "**Step 1 — Current assets and current liabilities.** Current ratio 3:1 means net working capital = 2 × current liabilities, so **current liabilities = ₹5,00,000 ÷ 2 = ₹2,50,000** and **current assets = ₹7,50,000**.",
    "**Step 2 — Total assets and sales.** **Total assets = Fixed assets + Current assets = ₹15,00,000 + ₹7,50,000 = ₹22,50,000.** Total assets turnover 2.5, so **Sales = 2.5 × ₹22,50,000 = ₹56,25,000**; with a gross profit ratio of 25%, **cost of goods sold = ₹42,18,750**.",
    "**Step 3 — Closing stock and the quick ratio.** Stock turnover 10 on cost of goods sold gives average stock = ₹4,21,875, so **closing stock = (2 × ₹4,21,875) − ₹6,50,500 = ₹1,93,250**. SM §3.1(b): **Quick ratio = (Current assets − stock) ÷ Current liabilities = (₹7,50,000 − ₹1,93,250) ÷ ₹2,50,000 = 2.23 : 1**.",
    "**(ii) Fixed assets turnover ratio** = Sales ÷ Fixed assets = ₹56,25,000 ÷ ₹15,00,000 = **3.75 times**.",
    "**Step 4 — EBIT, interest and profit.** Return on total assets (pre-tax) 15% gives **EBIT = 15% of ₹22,50,000 = ₹3,37,500**. Owned funds = total assets − current liabilities − loan funds; with loan funds to owned funds at 1:3, the loan funds follow, and **interest = 9% of loan funds**. EBT = EBIT − interest; **PAT = EBT × 0.75**.",
    "**(iii) Debt service coverage.** SM §3.2.2: Earnings available for debt service = PAT + depreciation + interest; **DSCR = that figure ÷ (Interest + Future instalments of ₹2,00,000)**.",
    "**(iv) EPS** = (PAT − preference dividend of 12% on ₹2,50,000 = ₹30,000) ÷ 75,000 shares. **(v) P/E ratio** = ₹20 ÷ EPS.",
    "This single RTP question walks through four of the chapter's five families — liquidity, activity, coverage and market — which is why it is the best one to rehearse."
   ],
   "conclusion": "Five requirements from one data set; the opening move is current liabilities from working capital.",
   "keywords": ["net working capital", "total assets turnover", "debt service coverage", "price-earnings ratio"]}),

 ("F03.19", {
   "id": "RTP-J26-FQ5", "status": "VERIFIED",
   "question": "ABC Industries Ltd., a listed pharmaceutical company with 1 lakh equity shares of ₹10 each traded at a 20% premium and an income-tax rate of 50%, re-organised its capital structure at the beginning of 2024-25 as: share capital 40%, 12% preference share capital 10%, other shareholders' funds 15%, 15% term loan 10%, current liabilities 25%. The term loan is repayable in 5 instalments starting 31.03.2025, and the bank has asked for a ratio-based review of the accounts.",
   "answer_points": [
    "**Step 1 — Size the balance sheet from the share capital.** Equity share capital = 1,00,000 shares × ₹10 = ₹10,00,000, and that is 40% of the total, so **total funds employed = ₹25,00,000**.",
    "**Step 2 — Split the structure.** 12% preference share capital = 10% = ₹2,50,000; other shareholders' funds = 15% = ₹3,75,000; 15% term loan = 10% = ₹2,50,000; current liabilities = 25% = ₹6,25,000.",
    "**Step 3 — The ratios the bank looks at.** **Debt-equity, capital gearing and proprietary ratios** follow directly from the split, treating preference capital as fixed-dividend capital in the gearing ratio and as part of the proprietary fund in the proprietary ratio (SM §3.2.1).",
    "**Step 4 — Coverage.** Interest = 15% of ₹2,50,000 = ₹37,500; preference dividend = 12% of ₹2,50,000 = ₹30,000; the annual instalment is one fifth of the term loan = ₹50,000. **Interest coverage = EBIT ÷ ₹37,500; DSCR = (PAT + depreciation + interest) ÷ (₹37,500 + ₹50,000); preference dividend coverage = PAT ÷ ₹30,000.**",
    "**Step 5 — Market ratios.** The shares trade at a 20% premium, i.e. at ₹12, so **P/E = ₹12 ÷ EPS** and **earnings yield = EPS ÷ ₹12 × 100** (SM §3.4.4).",
    "ICAI files this under 'Ratio Analysis' and uses it to test the whole chapter at once: a structure given in percentages, an instalment schedule for the DSCR, and a market price expressed as a premium."
   ],
   "conclusion": "Everything is derived from the one absolute figure given — the equity share capital.",
   "keywords": ["capital structure in percentages", "capital gearing", "debt service coverage", "traded at a premium"]}),

 ("F03.22", {
   "id": "RTP-M25-FQ4", "status": "VERIFIED",
   "question": "Prepare the Balance Sheet of Nevy Private Limited as at 31.03.2025 from: stock turnover ratio 15 times; cash and bank balance 10% of current assets (net of prepaid expenses); GP ratio 20%; creditors turnover (on cost of goods sold) 10 times; debtors turnover ratio 12 times; net fixed assets 25% of total liabilities; depreciation 15% on opening written-down value; current ratio 1.6 : 1; capital gearing ratio 0.6 : 1. Share capital is ₹36,00,000, prepaid expenses ₹7,50,000 and the current liabilities side totals ₹45,00,000. All purchases and sales are on credit.",
   "answer_points": [
    "**Step 1 — Total liabilities and fixed assets.** The balance sheet total is given by the layout; **net fixed assets = 25% of total liabilities**, which fixes the fixed-asset block, and depreciation at 15% on opening written-down value reconciles the opening and closing figures.",
    "**Step 2 — Current assets.** Current ratio 1.6 : 1 applied to the current liabilities figure gives **current assets**; cash and bank is **10% of current assets net of prepaid expenses of ₹7,50,000**.",
    "**Step 3 — Stock, debtors and creditors.** Cost of goods sold follows from sales and the 20% gross profit ratio. **Stock = COGS ÷ 15; debtors = credit sales ÷ 12; trade payables = COGS ÷ 10** (the creditors turnover is expressly on cost of goods sold, not on purchases).",
    "**Step 4 — The funding split.** SM §3.2.1: capital gearing ratio 0.6 : 1 = (preference capital + debentures + other borrowed funds) ÷ (equity share capital + reserves − losses). With share capital of ₹36,00,000, the 14% bonds and reserves and surplus follow, reserves being the balancing figure.",
    "**Step 5 — Present the Balance Sheet** in the RTP's own format: equities and long-term liabilities, current liabilities, fixed assets at opening written-down value less depreciation, and current assets.",
    "Two traps here: the creditors turnover is on **cost of goods sold** rather than purchases, and the cash percentage is applied to current assets **net of prepaid expenses**."
   ],
   "conclusion": "A reverse-working question with two deliberately non-standard definitions; read them before computing.",
   "keywords": ["capital gearing ratio", "creditors turnover on cost of goods sold", "net of prepaid expenses", "opening written-down value"]}),

 ("F03.22", {
   "id": "RTP-M26-FQ4", "status": "VERIFIED",
   "question": "P Limited for the year ended 31st March 2025: sales ₹3,60,00,000; rate of income tax 40%; return on net worth 30%; share capital to reserves ratio 6 : 4; current ratio 2 : 1; percentage of net profit to sales 8%; inventory turnover (based on cost of goods sold) 12; cost of goods sold ₹1,44,00,000; sundry debtors ₹12,00,000; sundry creditors ₹16,00,000; interest on 14% debentures ₹3,36,000. Calculate (i) operating expenses, (ii) share capital and reserves, (iii) closing stock, (iv) fixed assets.",
   "answer_points": [
    "**(i) Operating expenses.** Net profit = 8% of ₹3,60,00,000 = **₹28,80,000**, so profit before tax = ₹28,80,000 ÷ 0.60 = **₹48,00,000** and **EBIT = ₹48,00,000 + ₹3,36,000 = ₹51,36,000**. **Operating expenses = Sales − Cost of goods sold − EBIT = ₹3,60,00,000 − ₹1,44,00,000 − ₹51,36,000 = ₹1,64,64,000.**",
    "**(ii) Share capital and reserves.** Return on net worth 30% on a net profit of ₹28,80,000 gives **net worth = ₹28,80,000 ÷ 0.30 = ₹96,00,000**. Split 6 : 4, so **share capital = ₹57,60,000 and reserves = ₹38,40,000**.",
    "**(iii) Closing stock.** Inventory turnover 12 on cost of goods sold of ₹1,44,00,000 gives an average inventory of **₹12,00,000**; where the question treats this as the closing figure, **closing stock = ₹12,00,000**.",
    "**(iv) Fixed assets.** Debentures = ₹3,36,000 ÷ 0.14 = **₹24,00,000**. Current liabilities include sundry creditors of ₹16,00,000, and a current ratio of 2 : 1 gives current assets of **₹32,00,000**. **Fixed assets = Net worth + Debentures + Current liabilities − Current assets = ₹96,00,000 + ₹24,00,000 + ₹16,00,000 − ₹32,00,000 = ₹1,04,00,000.**",
    "ICAI labels this question 'Ratio Analysis' in the May 2026 RTP and repeats it almost word for word as Q1(a) of the May 2026 Series I mock test paper."
   ],
   "conclusion": "Four requirements, each one rearrangement of a ratio already given.",
   "keywords": ["return on net worth", "share capital to reserves", "inventory turnover", "14% debentures"],
   "also_asked_as": ["MTP-M26-S1-FQ1a (P Limited, the same data set and the same four requirements)"]}),

 ("F03.22", {
   "id": "RTP-S24-FQ4", "status": "VERIFIED",
   "question": "Complete the Balance Sheet of LP enterprises as on 31st March 2024 from: debt to total assets ratio 0.40; long-term debts to equity ratio 30%; gross profit margin on sales 20%; accounts receivable period 36 days; quick ratio 0.9; inventory holding period 60 days; cost of goods sold ₹64,00,000. Equity share capital is ₹20,00,000 and the balance sheet totals ₹50,00,000. Assume 360 days.",
   "answer_points": [
    "**Step 1 — Sales.** Gross profit margin is 20% on sales, so cost of goods sold is 80% of sales and **Sales = ₹64,00,000 ÷ 0.80 = ₹80,00,000**.",
    "**Step 2 — Debt and reserves.** Debt to total assets 0.40 on total assets of ₹50,00,000 gives **total debt = ₹20,00,000**. Long-term debts to equity 30% on equity share capital of ₹20,00,000 gives **long-term debts = ₹6,00,000**, so accounts payable and other current liabilities make up the balance of the debt. **Reserves and surplus = Total assets − Equity share capital − Total debt = ₹50,00,000 − ₹20,00,000 − ₹20,00,000 = ₹10,00,000.**",
    "**Step 3 — Inventories and receivables.** Inventory holding period 60 days gives **inventories = ₹64,00,000 × 60 ÷ 360 = ₹10,66,667**. Accounts receivable period 36 days gives **accounts receivable = ₹80,00,000 × 36 ÷ 360 = ₹8,00,000**.",
    "**Step 4 — Cash and fixed assets.** Quick ratio 0.9 = (Accounts receivable + Cash) ÷ Current liabilities, which yields **cash**; current assets are the sum of inventories, receivables and cash, and **fixed assets = Total assets − Current assets**.",
    "**Step 5 — Present the Balance Sheet**, both sides totalling ₹50,00,000, calculating to the nearest rupee as the RTP directs."
   ],
   "conclusion": "The balance sheet total is handed to you, which makes reserves and fixed assets the two balancing figures.",
   "keywords": ["debt to total assets", "long-term debts to equity", "inventory holding period", "quick ratio"]}),

 ("F03.09", {
   "id": "RTP-S25-FQ2", "status": "VERIFIED", "format": "MCQ",
   "question": "A manufacturing company growing at a good rate has a given financial leverage; identify the related ratio figure. (ICAI's topic label for this question is 'Ratio Analysis and Leverages'.)",
   "answer_points": [
    "The question links the **debt-equity ratio of Chapter 3 with the degree of financial leverage of Chapter 6** — the study material calls the debt-equity ratio **the indicator of the firm's financial leverage** (SM §3.2.1(c)).",
    "The route is: the degree of financial leverage = EBIT ÷ EBT = EBIT ÷ (EBIT − interest), so a given leverage figure fixes the interest, and the interest at the stated rate fixes the debt.",
    "With debt known and the balance sheet total or equity given, the **debt-equity ratio** follows.",
    "This is why the study material insists that liquidity ratios be read with turnover ratios and that leverage ratios be read with profitability ratios — no ratio stands alone."
   ],
   "conclusion": "A one-mark MCQ that is really a two-chapter question.",
   "keywords": ["debt-equity ratio", "indicator of financial leverage", "degree of financial leverage"]}),

 ("F03.22", {
   "id": "RTP-S25-FQ4", "status": "VERIFIED",
   "question": "Jamunapati Limited for the year ended 31st March 2024: sales ₹70,00,000; return on net worth 25%; rate of income tax 30%; share capital to reserves 7 : 3; current ratio 2; net profit to sales 7%; inventory turnover 10; cost of goods sold ₹24,00,000; interest on 15% debentures ₹1,05,000; receivables ₹3,00,000; payables ₹3,00,000. Calculate the operating expenses for the year and prepare the Balance Sheet as on 31st March 2024.",
   "answer_points": [
    "**Operating expenses.** Net profit = 7% of ₹70,00,000 = **₹4,90,000**; profit before tax = ₹4,90,000 ÷ 0.70 = **₹7,00,000**; **EBIT = ₹7,00,000 + ₹1,05,000 = ₹8,05,000**. **Operating expenses = Sales − Cost of goods sold − EBIT = ₹70,00,000 − ₹24,00,000 − ₹8,05,000 = ₹37,95,000.**",
    "**Net worth and its split.** Return on net worth 25% on a net profit of ₹4,90,000 gives **net worth = ₹19,60,000**; split 7 : 3, **share capital = ₹13,72,000 and reserves and surplus = ₹5,88,000**.",
    "**Debentures and current items.** Debentures = ₹1,05,000 ÷ 0.15 = **₹7,00,000**. Current ratio 2 on payables of ₹3,00,000 gives **current assets = ₹6,00,000**. Inventory turnover 10 on cost of goods sold gives **stock = ₹24,00,000 ÷ 10 = ₹2,40,000**; with receivables of ₹3,00,000, **cash = ₹6,00,000 − ₹2,40,000 − ₹3,00,000 = ₹60,000**.",
    "**Fixed assets** = Net worth + Debentures + Payables − Current assets = ₹19,60,000 + ₹7,00,000 + ₹3,00,000 − ₹6,00,000 = **₹23,60,000**.",
    "**Balance Sheet.** Liabilities: share capital ₹13,72,000; reserves and surplus ₹5,88,000; 15% debentures ₹7,00,000; payables ₹3,00,000 — **total ₹29,60,000**. Assets: fixed assets ₹23,60,000; stock ₹2,40,000; receivables ₹3,00,000; cash ₹60,000 — **total ₹29,60,000**.",
    "ICAI's published answer opens with exactly this operating-expenses working note before presenting the statement."
   ],
   "conclusion": "Net profit ratio and return on net worth between them fix both sides of the statement.",
   "keywords": ["return on net worth", "share capital to reserves", "operating expenses", "balancing"]}),

 ("F03.22", {
   "id": "RTP-S26-FQ4", "status": "VERIFIED",
   "question": "ASD Ltd. for the year ended 31st March 2026: net profit 8% of sales; raw materials consumed 20% of cost of goods sold; direct wages 10% of cost of goods sold; stock of raw materials 3 months' usage; stock of finished goods 6% of cost of goods sold; gross profit 15% of sales; debt collection period 2 months (all sales on credit); current ratio 2 : 1; fixed assets to current assets 13 : 11; fixed assets to sales 1 : 3; long-term loans to current liabilities 2 : 1; capital to reserves and surplus 1 : 4. Fixed assets are ₹1,30,00,000. Prepare the Profit & Loss Statement and the Balance Sheet in the given formats.",
   "answer_points": [
    "**Step 1 — Sales and cost of goods sold.** Fixed assets to sales is 1 : 3 on fixed assets of ₹1,30,00,000, so **Sales = ₹3,90,00,000**. Gross profit is 15% of sales, so **cost of goods sold = 85% of ₹3,90,00,000 = ₹3,31,50,000** and **gross profit = ₹58,50,000**.",
    "**Step 2 — The Profit & Loss Statement.** Direct materials consumed = 20% of COGS = **₹66,30,000**; direct wages = 10% of COGS = **₹33,15,000**; works overhead is the balance of COGS = ₹3,31,50,000 − ₹66,30,000 − ₹33,15,000 = **₹2,32,05,000**. Net profit = 8% of sales = **₹31,20,000**, so **selling and distribution expenses = ₹58,50,000 − ₹31,20,000 = ₹27,30,000**.",
    "**Step 3 — Current assets and liabilities.** Fixed assets to current assets is 13 : 11, so **current assets = ₹1,30,00,000 × 11 ÷ 13 = ₹1,10,00,000**. Current ratio 2 : 1 gives **current liabilities = ₹55,00,000**, and long-term loans to current liabilities 2 : 1 gives **long-term loans = ₹1,10,00,000**.",
    "**Step 4 — The current assets in detail.** Stock of raw materials = 3 months' usage = ₹66,30,000 × 3 ÷ 12 = **₹16,57,500**; stock of finished goods = 6% of COGS = **₹19,89,000**; debtors = 2 months' credit sales = ₹3,90,00,000 × 2 ÷ 12 = **₹65,00,000**; **cash is the balancing figure** = ₹1,10,00,000 − ₹16,57,500 − ₹19,89,000 − ₹65,00,000 = **₹8,53,500**.",
    "**Step 5 — Share capital and reserves.** Total assets = ₹1,30,00,000 + ₹1,10,00,000 = ₹2,40,00,000; less long-term loans ₹1,10,00,000 and current liabilities ₹55,00,000 leaves shareholders' funds of **₹75,00,000**, split 1 : 4 as **share capital ₹15,00,000 and reserves and surplus ₹60,00,000**.",
    "This is the fullest reverse-working question in the set, because it asks for both statements."
   ],
   "conclusion": "Nine ratios, two statements; work sales first and the rest falls out in order.",
   "keywords": ["fixed assets to sales", "works overhead as the balance", "capital to reserves", "balancing figure"]}),

 ("F03.22", {
   "id": "MTP-J25-S1-FQ2a", "marks": 6, "status": "VERIFIED",
   "question": "From the following of M/s Anya Co. Ltd., prepare the Trading and Profit & Loss Account for the year ended 31 March 2024 and a summarised Balance Sheet as at that date: current ratio 2.5; quick ratio 1.3; proprietary ratio (fixed assets ÷ proprietary fund) 0.6; gross profit to sales ratio 10%; debtors velocity 40 days; sales ₹7,30,000; working capital ₹1,20,000; bank overdraft ₹15,000; share capital ₹2,50,000. Closing stock is 10% more than opening stock, and net profit is 10% of proprietary funds.",
   "answer_points": [
    "**Step 1 — Current assets and current liabilities.** Current ratio 2.5 means working capital = 1.5 × current liabilities, so **current liabilities = ₹1,20,000 ÷ 1.5 = ₹80,000** and **current assets = ₹2,00,000**.",
    "**Step 2 — Stock.** The gap between the current and quick ratios is stock: (2.5 − 1.3) × ₹80,000 = **₹96,000 closing stock**. Since closing stock is 10% more than opening stock, **opening stock = ₹96,000 ÷ 1.1 = ₹87,273 (approx.)**.",
    "**Step 3 — Debtors and cash.** Debtors velocity 40 days on sales of ₹7,30,000 gives **debtors = ₹7,30,000 × 40 ÷ 365 = ₹80,000**. **Cash = Current assets − stock − debtors = ₹2,00,000 − ₹96,000 − ₹80,000 = ₹24,000.**",
    "**Step 4 — Proprietary fund and fixed assets.** Total assets = fixed assets + current assets, and proprietary fund + current liabilities = total assets. With fixed assets ÷ proprietary fund = 0.6, **0.6 PF + ₹2,00,000 = PF + ₹80,000**, so 0.4 PF = ₹1,20,000 and **proprietary fund = ₹3,00,000**, giving **fixed assets = ₹1,80,000**. Reserves = ₹3,00,000 − ₹2,50,000 share capital = **₹50,000**.",
    "**Step 5 — The Trading and Profit & Loss Account.** Gross profit = 10% of ₹7,30,000 = **₹73,000**, so cost of goods sold = **₹6,57,000**; purchases = COGS − opening stock + closing stock. Net profit = 10% of proprietary funds = 10% of ₹3,00,000 = **₹30,000**, so expenses = ₹73,000 − ₹30,000 = **₹43,000**.",
    "Note that this question uses a 365-day year for debtors velocity, which the MTP's own answer follows."
   ],
   "conclusion": "Six marks because two statements are required; the opening move is still working capital ÷ (ratio − 1).",
   "keywords": ["debtors velocity", "proprietary ratio", "closing stock 10% more", "net profit as a % of proprietary funds"]}),

 ("F03.22", {
   "id": "MTP-J25-S2-FQ1a", "marks": 5, "status": "VERIFIED",
   "question": "Alpha Limited as on 31st March 2023: equity share capital (₹10 fully paid) ₹20,00,000; working capital ₹6,00,000; bank overdraft ₹1,00,000; current ratio 2.5 : 1; liquidity ratio 1.5 : 1; proprietary ratio (net fixed assets ÷ proprietary fund) 0.75 : 1; cost of sales ₹14,40,000; debtors velocity 2 months; stock turnover based on cost of sales 4 times; gross profit ratio 20% of sales; net profit ratio 15% of sales. Closing stock was 25% higher than opening stock; expenses include depreciation of ₹90,000. For the year ended 31st March 2024 total sales were 20% higher, with stock ₹5,20,000, creditors ₹4,15,000, debtors ₹4,95,000 and cash ₹3,10,000. Prepare the Balance Sheet as on 31st March 2024.",
   "answer_points": [
    "**Step 1 — The 2023 position.** Current ratio 2.5 means working capital = 1.5 × current liabilities, so **current liabilities = ₹6,00,000 ÷ 1.5 = ₹4,00,000** and **current assets = ₹10,00,000**. The gap between the current and liquidity ratios gives **stock = (2.5 − 1.5) × ₹4,00,000 = ₹4,00,000**.",
    "**Step 2 — Proprietary fund and fixed assets for 2023.** Proprietary fund + current liabilities = net fixed assets + current assets, and net fixed assets = 0.75 × proprietary fund, so **0.75 PF + ₹10,00,000 = PF + ₹4,00,000**, giving **PF = ₹24,00,000** and **net fixed assets = ₹18,00,000**. Free reserves = ₹24,00,000 − ₹20,00,000 = **₹4,00,000**.",
    "**Step 3 — The 2024 figures.** Sales for 2023 = cost of sales ÷ 0.80 = ₹14,40,000 ÷ 0.80 = **₹18,00,000**, so **2024 sales = ₹21,60,000** and net profit at 15% = **₹3,24,000**.",
    "**Step 4 — The 2024 Balance Sheet.** Current assets are given directly: stock ₹5,20,000 + debtors ₹4,95,000 + cash ₹3,10,000 = **₹13,25,000**; current liabilities are creditors ₹4,15,000 plus the bank overdraft. Proprietary fund = opening ₹24,00,000 plus the year's retained profit, and **net fixed assets are the balancing figure after adding back or deducting depreciation of ₹90,000**.",
    "The two-year structure makes this a horizontal-analysis question dressed as a reverse-working one."
   ],
   "conclusion": "Build 2023 first from the ratios, then roll it forward to 2024 with the given balances.",
   "keywords": ["liquidity ratio", "proprietary ratio", "free reserves", "roll forward"]}),

 ("F03.11", {
   "id": "MTP-J26-S1-FQ1b", "marks": 5, "status": "VERIFIED",
   "question": "Prashuk Ltd.: fixed assets turnover ratio (based on cost of sales) 8 times; capital turnover ratio (based on cost of sales) 2 times; inventory turnover 8 times; receivable turnover 4 times; payable turnover 6 times; GP ratio 25%. Gross profit for the year is ₹8,00,000. There is no long-term loan or overdraft. Reserves and surplus amount to ₹2,00,000. Ending inventory is ₹20,000 above the beginning inventory. Determine the various assets and liabilities of the company.",
   "answer_points": [
    "**Step 1 — Sales and cost of sales.** Gross profit is 25% of sales and amounts to ₹8,00,000, so **Sales = ₹32,00,000** and **cost of sales = ₹24,00,000**.",
    "**Step 2 — Fixed assets and capital employed.** Fixed assets turnover 8 times on cost of sales gives **fixed assets = ₹24,00,000 ÷ 8 = ₹3,00,000**. Capital turnover 2 times gives **capital employed = ₹24,00,000 ÷ 2 = ₹12,00,000**.",
    "**Step 3 — Inventory.** Inventory turnover 8 times on cost of sales gives an **average inventory of ₹3,00,000**; since ending inventory is ₹20,000 above the beginning, **closing inventory = ₹3,10,000 and opening inventory = ₹2,90,000**.",
    "**Step 4 — Receivables and payables.** Receivable turnover 4 times on sales gives **receivables = ₹32,00,000 ÷ 4 = ₹8,00,000**. Purchases = cost of sales − opening inventory + closing inventory = ₹24,00,000 + ₹20,000 = ₹24,20,000, so **payables = ₹24,20,000 ÷ 6 = ₹4,03,333 (approx.)**.",
    "**Step 5 — The funding side.** With no long-term loan or overdraft, capital employed of ₹12,00,000 is share capital plus reserves and surplus of ₹2,00,000, so **share capital = ₹10,00,000**; cash is the balancing current asset.",
    "The instruction 'based on cost of sales' appears twice here and is the marks: using sales instead would inflate both fixed assets and capital employed."
   ],
   "conclusion": "Five turnover ratios, five figures — each one a single division once sales and cost of sales are known.",
   "keywords": ["based on cost of sales", "capital turnover", "payable turnover", "balancing figure"]}),

 ("F03.11", {
   "id": "MTP-J26-S2-FQ1a", "marks": 5, "status": "VERIFIED",
   "question": "A concern reports: debtors velocity 3 months; creditors velocity 2 months; stock turnover ratio 1.5; gross profit ratio 25%; bills receivable ₹25,000; bills payable ₹10,000; gross profit ₹4,00,000; fixed assets to turnover ratio 4. Closing stock is ₹10,000 above the opening stock. Calculate (i) sales and cost of goods sold, (ii) sundry debtors, (iii) sundry creditors, (iv) closing stock, (v) fixed assets.",
   "answer_points": [
    "**(i) Sales and cost of goods sold.** Gross profit is 25% of sales and is ₹4,00,000, so **Sales = ₹16,00,000** and **Cost of goods sold = ₹12,00,000**.",
    "**(ii) Sundry debtors.** Debtors velocity 3 months gives total receivables = ₹16,00,000 × 3 ÷ 12 = ₹4,00,000. Bills receivable of ₹25,000 form part of that, so **sundry debtors = ₹4,00,000 − ₹25,000 = ₹3,75,000**.",
    "**(iii) Sundry creditors.** Purchases = Cost of goods sold + increase in stock = ₹12,00,000 + ₹10,000 = ₹12,10,000. Creditors velocity 2 months gives total payables = ₹12,10,000 × 2 ÷ 12 = ₹2,01,667, and deducting bills payable of ₹10,000 leaves **sundry creditors = ₹1,91,667 (approx.)**.",
    "**(iv) Closing stock.** Stock turnover 1.5 on cost of goods sold gives an average stock of ₹12,00,000 ÷ 1.5 = ₹8,00,000; with closing ₹10,000 above opening, **closing stock = ₹8,05,000** and opening stock = ₹7,95,000.",
    "**(v) Fixed assets.** Fixed assets to turnover ratio 4 gives **fixed assets = ₹16,00,000 ÷ 4 = ₹4,00,000**.",
    "The two traps: bills receivable and bills payable must be **deducted** from the total to reach sundry debtors and sundry creditors, and purchases, not cost of goods sold, drive the creditors velocity."
   ],
   "conclusion": "Five requirements; the bills receivable and bills payable adjustments are where marks are lost.",
   "keywords": ["debtors velocity", "creditors velocity", "bills receivable", "purchases"]}),

 ("F03.22", {
   "id": "MTP-M24-S1-FQ1c", "marks": 5, "status": "VERIFIED",
   "question": "ANVY Ltd. for the year ended 31st March 2023: equity share capital ₹2,00,000; current debt to total debt 0.50; total debt to equity share capital 0.60; fixed assets to equity share capital 0.70; total assets turnover 2.5 times; inventory turnover 10 times. Prepare the Balance Sheet as on 31st March 2023.",
   "answer_points": [
    "**Step 1 — Debt.** Total debt = 0.60 × ₹2,00,000 = **₹1,20,000**; current debt = 0.50 × ₹1,20,000 = **₹60,000**, so **long-term debt = ₹60,000**.",
    "**Step 2 — Total assets.** Total assets = Equity share capital + Total debt = ₹2,00,000 + ₹1,20,000 = **₹3,20,000**.",
    "**Step 3 — Fixed and current assets.** Fixed assets = 0.70 × ₹2,00,000 = **₹1,40,000**, so **current assets = ₹3,20,000 − ₹1,40,000 = ₹1,80,000**.",
    "**Step 4 — Sales and inventory.** Total assets turnover 2.5 gives **Sales = 2.5 × ₹3,20,000 = ₹8,00,000**; inventory turnover 10 gives **inventory = ₹8,00,000 ÷ 10 = ₹80,000**, leaving **cash and other current assets of ₹1,00,000**.",
    "**Balance Sheet.** Liabilities: equity share capital ₹2,00,000; long-term debt ₹60,000; current debt ₹60,000 — **total ₹3,20,000**. Assets: fixed assets ₹1,40,000; inventory ₹80,000; cash and other current assets ₹1,00,000 — **total ₹3,20,000**.",
    "Note that this MTP expresses the inventory turnover on **sales**, not on cost of goods sold, because no gross profit ratio is given — an illustration of the study material's instruction to calculate on the information available and state the assumption."
   ],
   "conclusion": "The simplest reverse-working question in the set; every ratio is stated against equity share capital.",
   "keywords": ["current debt to total debt", "total assets turnover", "inventory turnover on sales", "state the assumption"]}),

 ("F03.19", {
   "id": "MTP-M24-S2-FQ3a", "marks": 5, "status": "VERIFIED",
   "question": "EOC Ltd., a listed company, presents abridged financial statements: sales ₹1,25,00,000; cost of goods sold ₹76,40,000; gross profit ₹48,60,000; administrative expenses ₹13,20,000; selling and distribution expenses ₹15,90,000; operating profit ₹19,50,000; non-operating income ₹3,28,000; non-operating expenses ₹1,27,000; profit before interest and taxes ₹21,51,000; interest ₹4,39,000; profit before tax ₹17,12,000; taxes ₹4,28,000; profit after tax ₹12,84,000. Equity share capital ₹30,00,000; reserves and surplus ₹18,00,000; secured loan ₹10,00,000; unsecured loan ₹4,30,000; buildings ₹7,50,000; machinery ₹2,30,000; furniture ₹7,60,000; intangible assets ₹50,000; inventory ₹38,60,000; receivables ₹39,97,000; short-term investments ₹3,00,000; cash and bank ₹2,30,000; creditors ₹25,67,000 and short-term loans. Compute the ratios indicated.",
   "answer_points": [
    "**Profitability on sales (SM §3.4.1).** Gross profit ratio = ₹48,60,000 ÷ ₹1,25,00,000 × 100 = **38.88%**. Operating profit ratio = ₹19,50,000 ÷ ₹1,25,00,000 × 100 = **15.60%**. Net profit ratio = ₹12,84,000 ÷ ₹1,25,00,000 × 100 = **10.27%**. Operating ratio = (₹76,40,000 + ₹29,10,000) ÷ ₹1,25,00,000 × 100 = **84.40%** — the complement of the operating profit ratio.",
    "**Coverage (SM §3.2.2).** Interest coverage = Profit before interest and taxes ÷ Interest = ₹21,51,000 ÷ ₹4,39,000 = **4.90 times**.",
    "**Capital structure (SM §3.2.1).** Owned funds = ₹30,00,000 + ₹18,00,000 = ₹48,00,000; borrowed funds = ₹10,00,000 + ₹4,30,000 = ₹14,30,000, so the **debt-equity ratio = 0.30 : 1** on long-term debt.",
    "**Return on capital employed (SM §3.4.2).** Capital employed = Total funds raised = ₹62,30,000, so **ROCE (pre-tax) = ₹21,51,000 ÷ ₹62,30,000 × 100 = 34.53%**. Note that the **intangible assets of ₹50,000 are included** in capital employed; only fictitious assets would be excluded.",
    "**Return on equity.** ROE = Profit after tax ÷ Owned funds × 100 = ₹12,84,000 ÷ ₹48,00,000 × 100 = **26.75%**.",
    "**Activity.** Inventory turnover = ₹76,40,000 ÷ ₹38,60,000 = **1.98 times**; receivables turnover = ₹1,25,00,000 ÷ ₹39,97,000 = **3.13 times**, a collection period of about 115 days.",
    "This question is the chapter in miniature: one set of statements, every family of ratio."
   ],
   "conclusion": "Read the statements once, then pick the two figures each ratio needs.",
   "keywords": ["operating ratio", "interest coverage", "capital employed", "intangible assets included"]}),

 ("F03.22", {
   "id": "MTP-M25-S2-FQ3a", "marks": 8, "status": "VERIFIED",
   "question": "Simandhar Limited for the year ended 31.03.2025: liquid ratio 2.0; cash asset ratio 0.36; current ratio 3.50; receivables collection period 30 days; proprietary ratio 0.72; equity dividend ₹2,50,000; equity dividend coverage ratio 2.10; non-current assets turnover ratio 0.80; EPS ₹3.00 per share; stock turnover ratio 6.0 times; GP ratio one-fifth of sales; current liabilities ₹2,80,000. Assume 360 days; closing inventory is 20% more than opening inventory. Complete the Balance Sheet as of 31st March 2025.",
   "answer_points": [
    "**Step 1 — Current assets and their split.** Current ratio 3.50 on current liabilities of ₹2,80,000 gives **current assets = ₹9,80,000**. Liquid ratio 2.0 gives liquid assets of ₹5,60,000, so **inventory = ₹9,80,000 − ₹5,60,000 = ₹4,20,000**. Cash asset ratio 0.36 gives **cash and bank = 0.36 × ₹2,80,000 = ₹1,00,800**.",
    "**Step 2 — Earnings and share capital.** SM §3.2.2: equity dividend coverage = (EAT − preference dividend) ÷ Equity dividend, so **earnings available to equity = 2.10 × ₹2,50,000 = ₹5,25,000**. With an EPS of ₹3.00, the **number of equity shares = ₹5,25,000 ÷ ₹3 = 1,75,000**, so **equity share capital = 1,75,000 × ₹10 = ₹17,50,000**.",
    "**Step 3 — Sales and receivables.** Stock turnover 6.0 times on cost of goods sold, with average inventory derived from the closing figure of ₹4,20,000 (20% above opening), gives **cost of goods sold**; the GP ratio of one-fifth of sales converts it to **sales**. Receivables = Sales × 30 ÷ 360.",
    "**Step 4 — Fixed assets and the funding split.** Non-current assets turnover 0.80 on sales gives **fixed assets**. Proprietary ratio 0.72 = proprietary fund ÷ total assets fixes the **proprietary fund**, of which equity share capital is ₹17,50,000 and **reserves are the balance**; **long-term debentures are the balancing figure** on the liabilities side.",
    "**Step 5 — Present the Balance Sheet** in the MTP's format, with short-term advances as the remaining current asset.",
    "Eight marks because the question chains four families together — liquidity, coverage, activity and the owner's view — before the statement can be drawn."
   ],
   "conclusion": "The equity dividend coverage ratio is the unusual entry point: it gives earnings, and EPS then gives the share count.",
   "keywords": ["cash asset ratio", "equity dividend coverage", "non-current assets turnover", "proprietary ratio"]}),

 ("F03.19", {
   "id": "MTP-M26-S1-FQ1a", "marks": 5, "status": "VERIFIED",
   "question": "P Limited for the year ended 31st March 2025: sales ₹3,60,00,000; rate of income tax 40%; return on net worth 30%; share capital to reserves ratio 6 : 4; current ratio 2 : 1; percentage of net profit to sales 8%; inventory turnover (based on cost of goods sold) 12; cost of goods sold ₹1,44,00,000; sundry debtors ₹12,00,000; sundry creditors ₹16,00,000; interest on 14% debentures ₹3,36,000. Calculate operating expenses, share capital and reserves, closing stock and fixed assets.",
   "answer_points": [
    "**Operating expenses.** Net profit = 8% of ₹3,60,00,000 = ₹28,80,000; profit before tax = ₹28,80,000 ÷ 0.60 = ₹48,00,000; EBIT = ₹48,00,000 + ₹3,36,000 = ₹51,36,000. **Operating expenses = ₹3,60,00,000 − ₹1,44,00,000 − ₹51,36,000 = ₹1,64,64,000.**",
    "**Share capital and reserves.** Net worth = ₹28,80,000 ÷ 0.30 = ₹96,00,000, split 6 : 4 as **share capital ₹57,60,000 and reserves ₹38,40,000**.",
    "**Closing stock** = Cost of goods sold ÷ Inventory turnover = ₹1,44,00,000 ÷ 12 = **₹12,00,000**.",
    "**Fixed assets.** Debentures = ₹3,36,000 ÷ 0.14 = ₹24,00,000; current assets = 2 × current liabilities of ₹16,00,000 = ₹32,00,000. **Fixed assets = ₹96,00,000 + ₹24,00,000 + ₹16,00,000 − ₹32,00,000 = ₹1,04,00,000.**",
    "ICAI set the identical question in the May 2026 RTP under the label 'Ratio Analysis', which is the clearest signal in the whole set of where this chapter's marks lie."
   ],
   "conclusion": "Identical to the May 2026 RTP question; if you have worked one you have worked both.",
   "keywords": ["return on net worth", "operating expenses", "closing stock", "fixed assets"]}),

 ("F03.07", {
   "id": "MTP-S24-S1-FQ1a", "marks": 5, "status": "VERIFIED",
   "question": "Calculate the total current assets of Ananya Limited from: stock turnover 5 times; sales (all credit) ₹7,20,000; gross profit ratio 25%; current liabilities ₹2,40,000; liquidity ratio 1.25. Stock at the end is ₹30,000 more than stock in the beginning.",
   "answer_points": [
    "**Step 1 — Cost of goods sold.** Gross profit ratio 25% on sales of ₹7,20,000 gives **cost of goods sold = 75% of ₹7,20,000 = ₹5,40,000**.",
    "**Step 2 — Average and closing stock.** Stock turnover 5 times gives **average stock = ₹5,40,000 ÷ 5 = ₹1,08,000**. Since closing stock is ₹30,000 more than opening stock, opening + ₹30,000 = closing and their average is ₹1,08,000, so **opening stock = ₹93,000 and closing stock = ₹1,23,000**.",
    "**Step 3 — Liquid assets.** SM §3.1(b): liquidity ratio = Liquid assets ÷ Current liabilities, so **liquid assets = 1.25 × ₹2,40,000 = ₹3,00,000**.",
    "**Step 4 — Total current assets.** **Current assets = Liquid assets + Closing stock = ₹3,00,000 + ₹1,23,000 = ₹4,23,000.**",
    "The current ratio here works out to ₹4,23,000 ÷ ₹2,40,000 = 1.76 : 1, below the study material's generally acceptable 2 : 1 — a comment worth adding if the question asks for one."
   ],
   "conclusion": "Four short steps; the average-stock reconciliation is the only place to slip.",
   "keywords": ["stock turnover", "liquidity ratio", "average stock", "current assets"]}),

 ("F03.19", {
   "id": "MTP-S24-S2-FQ3b", "marks": 4, "status": "VERIFIED",
   "question": "EPL Ltd. reports share capital ₹50,00,000 in both years, reserves and surplus ₹20,00,000 (2023) and ₹25,00,000 (2024), and long-term loan ₹30,00,000 in both years. Net profit ratio 8%; gross profit ratio 20%; long-term loan has been used to finance 40% of the fixed assets; stock turnover with respect to cost of goods sold is 4; debtors represent 90 days sales; the company holds cash equivalent to 1½ months cost of goods sold. Ignore taxation and assume 360 days. Prepare the Balance Sheet as on 31st March 2024.",
   "answer_points": [
    "**Step 1 — Sales from the change in reserves.** With taxation ignored and no dividend stated, the increase in reserves and surplus of ₹5,00,000 is the year's net profit. At a net profit ratio of 8%, **Sales = ₹5,00,000 ÷ 0.08 = ₹62,50,000**, and at a gross profit ratio of 20%, **cost of goods sold = ₹50,00,000**.",
    "**Step 2 — Fixed assets.** The long-term loan of ₹30,00,000 finances 40% of the fixed assets, so **fixed assets = ₹30,00,000 ÷ 0.40 = ₹75,00,000**.",
    "**Step 3 — Current assets.** Closing stock = Cost of goods sold ÷ 4 = **₹12,50,000**. Debtors = 90 days of sales = ₹62,50,000 × 90 ÷ 360 = **₹15,62,500**. Cash = 1½ months of cost of goods sold = ₹50,00,000 × 1.5 ÷ 12 = **₹6,25,000**.",
    "**Step 4 — Sundry creditors as the balancing figure.** Total assets = ₹75,00,000 + ₹12,50,000 + ₹15,62,500 + ₹6,25,000 = **₹1,09,37,500**. Liabilities other than creditors = ₹50,00,000 + ₹25,00,000 + ₹30,00,000 = ₹1,05,00,000, so **sundry creditors = ₹4,37,500**.",
    "**Balance Sheet** in the MTP's format, both sides totalling ₹1,09,37,500.",
    "The entry point is unusual and worth remembering: with tax ignored, the **movement in reserves is the net profit**, and the net profit ratio then unlocks sales."
   ],
   "conclusion": "Movement in reserves → net profit → sales → everything else.",
   "keywords": ["movement in reserves", "net profit ratio", "long-term loan finances 40%", "balancing figure"],
   "also_asked_as": ["MTP-S25-S2-FQ1b (Fortune Ltd — the same question with share capital ₹60,00,000, reserves ₹30,00,000 and ₹40,00,000, and a long-term loan of ₹40,00,000)"]}),

 ("F03.22", {
   "id": "MTP-S25-S1-FQ1b", "marks": 5, "status": "VERIFIED",
   "question": "Gagan Pvt. Ltd. for the year ending 31st March 2025: current ratio 2.5 : 1; debt-equity ratio 1 : 2; return on total assets (after tax) 15%; total assets turnover ratio 2; gross profit ratio 25%; stock turnover ratio 5; net working capital ₹15,00,000; fixed assets ₹30,00,000; 1,80,000 equity shares of ₹10 each; 60,000 10% preference shares of ₹10 each; opening stock ₹16,00,000. Calculate (a) quick ratio, (b) fixed assets turnover ratio, (c) proprietary ratio, (d) earnings per share.",
   "answer_points": [
    "**Step 1 — Current assets and current liabilities.** Current ratio 2.5 means net working capital = 1.5 × current liabilities, so **current liabilities = ₹15,00,000 ÷ 1.5 = ₹10,00,000** and **current assets = ₹25,00,000**.",
    "**Step 2 — Total assets and sales.** **Total assets = ₹30,00,000 + ₹25,00,000 = ₹55,00,000.** Total assets turnover 2 gives **Sales = ₹1,10,00,000**, and a gross profit ratio of 25% gives **cost of goods sold = ₹82,50,000**.",
    "**Step 3 — Closing stock and the quick ratio.** Stock turnover 5 on cost of goods sold gives an average stock of ₹16,50,000; with opening stock of ₹16,00,000, **closing stock = ₹17,00,000**. **(a) Quick ratio = (₹25,00,000 − ₹17,00,000) ÷ ₹10,00,000 = 0.80 : 1.**",
    "**(b) Fixed assets turnover ratio** = Sales ÷ Fixed assets = ₹1,10,00,000 ÷ ₹30,00,000 = **3.67 times**.",
    "**(c) Proprietary ratio.** Debt-equity 1 : 2 on total debt (including current liabilities of ₹10,00,000) and shareholders' funds gives the split; **proprietary fund = equity ₹18,00,000 + preference ₹6,00,000 + reserves**, and **proprietary ratio = proprietary fund ÷ total assets of ₹55,00,000** (SM §3.2.1(f) includes preference share capital in the proprietary fund).",
    "**(d) Earnings per share.** Return on total assets (after tax) 15% gives **profit after tax = 15% of ₹55,00,000 = ₹8,25,000**; less preference dividend of 10% on ₹6,00,000 = ₹60,000 leaves ₹7,65,000, so **EPS = ₹7,65,000 ÷ 1,80,000 = ₹4.25**.",
    "The preference dividend deduction in part (d) is the single most commonly dropped mark in the whole chapter."
   ],
   "conclusion": "Four requirements spanning liquidity, activity, structure and the owner's view.",
   "keywords": ["net working capital", "total assets turnover", "proprietary ratio", "preference dividend"]}),

 ("F03.19", {
   "id": "MTP-S25-S2-FQ1b", "marks": 5, "status": "VERIFIED",
   "question": "Fortune Ltd. reports share capital ₹60,00,000 in both years, reserves and surplus ₹30,00,000 (2024) and ₹40,00,000 (2025), and long-term loan ₹40,00,000 in both years. Net profit ratio 8%; gross profit ratio 20%; long-term loan has been used to finance 40% of the fixed assets; stock turnover with respect to cost of goods sold is 4; debtors represent 90 days of credit sales; cash equivalent to 1½ months cost of goods sold; ignore taxation; 360 days; all sales are credit sales. Prepare the Balance Sheet as on 31st March 2025.",
   "answer_points": [
    "**Step 1 — Sales.** With taxation ignored, the increase in reserves of ₹10,00,000 is the year's net profit; at a net profit ratio of 8%, **Sales = ₹10,00,000 ÷ 0.08 = ₹1,25,00,000**, and at a gross profit ratio of 20%, **cost of goods sold = ₹1,00,00,000**.",
    "**Step 2 — Fixed assets** = Long-term loan ÷ 0.40 = ₹40,00,000 ÷ 0.40 = **₹1,00,00,000**.",
    "**Step 3 — Current assets.** Closing stock = ₹1,00,00,000 ÷ 4 = **₹25,00,000**; sundry debtors = ₹1,25,00,000 × 90 ÷ 360 = **₹31,25,000**; cash in hand = ₹1,00,00,000 × 1.5 ÷ 12 = **₹12,50,000**.",
    "**Step 4 — Sundry creditors.** Total assets = ₹1,00,00,000 + ₹25,00,000 + ₹31,25,000 + ₹12,50,000 = **₹1,68,75,000**; liabilities other than creditors = ₹60,00,000 + ₹40,00,000 + ₹40,00,000 = ₹1,40,00,000, so **sundry creditors = ₹28,75,000**.",
    "**Balance Sheet** in the MTP's format, both sides totalling ₹1,68,75,000.",
    "This is the September 2024 Series II question repeated with larger figures — worth working once and recognising thereafter."
   ],
   "conclusion": "Same method as EPL Ltd.; only the numbers change.",
   "keywords": ["movement in reserves", "long-term loan finances 40%", "90 days of credit sales", "balancing figure"]}),

 ("F03.22", {
   "id": "MTP-S26-S1-FQ3b", "status": "VERIFIED",
   "question": "Complete the Balance Sheet from: current ratio 2.5; liquid ratio 1.5; working capital ₹4,80,000; fixed assets to proprietary ratio; and reserves and surplus as a stated proportion of share capital.",
   "answer_points": [
    "**Step 1 — Current assets and current liabilities.** Current assets ÷ Current liabilities = 2.5, and working capital = current assets − current liabilities, so ₹4,80,000 = 2.5 CL − CL = 1.5 CL. **Current liabilities = ₹3,20,000** and **current assets = ₹3,20,000 × 2.5 = ₹8,00,000**.",
    "**Step 2 — Stock.** Liquid ratio = (Current assets − Inventories) ÷ Current liabilities, so 1.5 × ₹3,20,000 = ₹4,80,000 = ₹8,00,000 − Inventories, giving **Stock = ₹3,20,000**.",
    "**Step 3 — Proprietary fund and fixed assets.** With fixed assets ÷ proprietary fund given, the identity proprietary fund + current liabilities = fixed assets + current assets yields the **proprietary fund**, and the ratio then gives **fixed assets**.",
    "**Step 4 — Share capital and reserves.** Reserves stated as a proportion of share capital split the proprietary fund between **capital and sundry creditors** on the liabilities side.",
    "**Step 5 — Present the Balance Sheet**, both sides totalling the same figure. ICAI's answer file shows exactly these working notes in this order.",
    "Only the answer file of this mock test paper is on the portal; the question wording above is reconstructed from it."
   ],
   "conclusion": "The archetype of the whole chapter: working capital ÷ (current ratio − 1) opens every one of these.",
   "keywords": ["working capital", "liquid ratio", "proprietary fund", "sundry creditors"]}),
]


def main():
    root = 'sources/f03'
    files = {f: json.load(io.open(os.path.join(root, f), encoding='utf-8'))
             for f in ('u1.json', 'u2.json', 'u3.json')}
    index = {}
    for fname, data in files.items():
        for blk in data.get('concepts', []):
            for part in [p.strip() for p in blk['code'].split('+')]:
                index.setdefault(part, (fname, blk))
    added = skipped = 0
    for code, entry in ENTRIES:
        if code not in index:
            sys.exit(f'no block for {code}')
        _, blk = index[code]
        oq = blk.setdefault('official_questions', [])
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
