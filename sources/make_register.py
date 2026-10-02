"""Build sources/register.json and book/concept_index.json from the ICAI detailed contents (Study Material May 2026 edition).
Codes: F<ch>.<heading>[.<sub>] for Paper 6A (FM), S<ch>.<heading>[.<sub>] for Paper 6B (SM). Never renumber an issued code.
Only chapters whose headings have been reviewed are listed; later chapters are appended as they are built."""
import json, os

REG = {
    # ---- Paper 6A FM, Chapter 1 (SM pages 1.1-1.29)
    ('F', 1): [
        ('F01.01', '1', '1. Introduction', 'p2', ['stages of decision making for a new venture', 'three key questions: financing, investment, dividend']),
        ('F01.02', '2', '2. Meaning of Financial Management', 'p3', ['definitions', 'Phillippatus definition', 'two basic aspects']),
        ('F01.02.01', '2.1', '2.1 Procurement of Funds', 'p4', ['equity', 'debentures', 'funding from banks (fund / non-fund based)', 'international funding (FDI, FII, ADR, GDR)', 'angel financing', 'carbon credits', 'risk, cost and control']),
        ('F01.02.02', '2.2', '2.2 Effective Utilisation of Funds', 'p7', ['utilisation for fixed assets (capital budgeting)', 'utilisation for working capital']),
        ('F01.03', '3', '3. Evolution of Financial Management', 'p7', ['traditional phase', 'transitional phase', 'modern phase']),
        ('F01.04', '4', '4. Finance Functions / Finance Decision', 'p8', ['V = f(I, F, D)', 'investment decisions', 'financing decisions', 'dividend decisions', 'short-term: working capital management', 'decisions are inter-related']),
        ('F01.05', '5', '5. Importance of Financial Management', 'p10', ['seven tasks that show importance']),
        ('F01.06', '6', '6. Scope of Financial Management', 'p11', ['Ezra Solomon four aspects', 'role of financial controller', 'risk-return trade off']),
        ('F01.07', '7', '7. Objectives of Financial Management', 'p12', ['two objectives assumed']),
        ('F01.07.01', '7.1', '7.1 Profit Maximisation', 'p13', ['four problems / limitations']),
        ('F01.07.02', '7.2', '7.2 Wealth Maximisation / Value Creation', 'p14', ['cash flow, cost-benefit, time value of money', 'Van Horne on value of firm', 'value of firm formulae', 'other goals', 'why wealth maximisation works']),
        ('F01.08', '8', '8. Conflicts in Profit versus Value Maximisation Principle', 'p16', ['management vs stakeholders', 'advantages and disadvantages table', 'example', 'Illustration 1 (products X and Y)']),
        ('F01.09', '9', '9. Role of Finance Executive', 'p18', ['changing role (Jeff Thomson quote)', 'five responsibilities', 'organisation of finance function']),
        ('F01.09.01', '9.1', "9.1 Role of Finance Executive in Today's World vis-a-vis in the Past", 'p20', ['what a CFO used to do vs now does']),
        ('F01.10', '10', '10. Financial Distress and Insolvency', 'p21', ['meaning of financial distress', 'insolvency']),
        ('F01.11', '11', '11. Relationship of Financial Management with Related Disciplines', 'p21', []),
        ('F01.11.01', '11.1', '11.1 Financial Management and Accounting', 'p21', ['treatment of funds', 'decision-making']),
        ('F01.11.02', '11.2', '11.2 Financial Management and Other Related Disciplines', 'p23', ['marketing, production, quantitative methods, economics']),
        ('F01.12', '12', '12. Agency Problem and Agency Cost', 'p24', ['agency problem', 'agency cost - four types', 'addressing the agency problem']),
    ],
    # ---- Paper 6B SM, Chapter 1 (SM pages 1.1-1.42)
    ('S', 1): [
        ('S01.01', '1.1', '1.1 Introduction', 'p2', []),
        ('S01.02', '1.2', '1.2 Meaning and Nature of Strategic Management', 'p3', ['management in two senses', 'strategic management process activities']),
        ('S01.03', '1.3', '1.3 Concept of Strategy', 'p4', ['definitions (Ansoff, Glueck)', 'strategy not a substitute for sound management', 'levels of formulation', 'partly proactive and partly reactive', 'UPI example', 'ketchup example']),
        ('S01.04', '1.4', '1.4 Strategic Management - Importance and Limitations', 'p7', ['two-fold objective', 'meaning (process)', 'business policy']),
        ('S01.04.01', '1.4.1', '1.4.1 Importance of Strategic Management', 'p8', ['survival of the fittest', 'seven benefits', 'non-strategic decisions']),
        ('S01.04.02', '1.4.2', '1.4.2 Limitations of Strategic Management', 'p11', ['complex and turbulent environment', 'time-consuming', 'costly', 'difficult to estimate competitive responses', 'why firms still use it']),
        ('S01.05', '1.5', '1.5 Strategic Intent (Vision, Mission, Goals, Objectives and Values)', 'p13', ['meaning', 'components']),
        ('S01.05.01', '1.5.1', '1.5.1 Vision', 'p15', ['strategic vision', 'examples', 'essentials of a strategic vision']),
        ('S01.05.02', '1.5.2', '1.5.2 Mission', 'p16', ['why an organisation should have a mission', 'examples', 'writing a mission', 'Drucker and Levitt questions', 'what business are we in']),
        ('S01.05.03', '1.5.3', '1.5.3 Goals and Objectives', 'p19', ['characteristics of objectives', 'short-term and long-term objectives', 'seven long-term objective areas', 'benefits of objectives']),
        ('S01.05.04', '1.5.4', '1.5.4 Values', 'p22', ['importance of values', 'examples', 'intent vs values']),
        ('S01.06', '1.6', '1.6 Strategic Levels in Organisations', 'p23', ['corporate level', 'business level (SBU)', 'functional level', 'top-down vs bottom-up']),
        ('S01.06.01', '1.6.1', '1.6.1 Network of Relationship between the Three Levels', 'p27', ['functional and divisional', 'horizontal', 'matrix']),
    ],
}

reg, idx = [], {}
for (sec, ch), rows in REG.items():
    for code, ref, path, page, subs in rows:
        reg.append({'code': code, 'section': 'FM' if sec == 'F' else 'SM', 'ch': ch, 'path': path, 'ref': f'§{ref}', 'page': page, 'subpoints': subs})
        idx[code] = {'ref': f'§{ref}', 'title': path}

# ---- remaining chapters, read from the compact spec in sources/register_data.txt
import re
prefix = None
for line in open('sources/register_data.txt', encoding='utf-8'):
    line = line.rstrip('\n')
    if line.startswith('##'):
        prefix = line[2:].split('|')[0].strip()
        serial = 0
        continue
    if not line.strip() or line.startswith('#') or prefix is None:
        continue
    ref, title = line.split('|', 1)
    serial += 1
    code = f'{prefix}.{serial:02d}'
    reg.append({'code': code, 'section': 'FM' if prefix[0] == 'F' else 'SM', 'ch': int(prefix[1:]),
                'path': title.strip(), 'ref': f'§{ref.strip()}', 'page': '', 'subpoints': []})
    idx[code] = {'ref': f'§{ref.strip()}', 'title': title.strip()}
json.dump(reg, open('sources/register.json', 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
os.makedirs('book', exist_ok=True)
json.dump(idx, open('book/concept_index.json', 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
print('register rows', len(reg))
