# Build state — CA Inter Paper 6 (FM & SM) master book

Updated 03-10-2026. Target attempt: January 2027.

## Done

| Stage | Status |
|---|---|
| Sources collected (SM, past papers, RTPs, MTPs, examiners' comments) | Done — see `my_uploads/SOURCES_INVENTORY.md` |
| Heading register for FM Ch 1 and SM Ch 1 | Done — `sources/register.json` (32 headings), `book/concept_index.json` |
| Official questions mapped to those chapters | Done — `sources/atoms/atoms_F01.json` (30), `atoms_S01.json` (102) |
| FM Chapter 1 written and merged | Done — `book/Ch01.json` (19/19 headings, 30/30 questions placed) |
| SM Chapter 1 written and merged | Done — `book/Ch10.json` (13/13 headings, 102/102 questions placed) |
| Builder, merge/validate, bookmark, index-link and scan scripts | Done — adapted from the Audit book for Paper 6's two sections |
| Review PDF (front matter + both chapters) | Done — `CA_Inter_FMSM_Master_Book.pdf` |
| FM Chapters 2–9 written and merged | Done — `book/Ch02.json` to `book/Ch09.json`; **Section A (FM) is complete**; see the progress ledger below |
| SM Chapter 2 written and merged | Done — `book/Ch11.json` (24/24 headings, 99/99 atoms placed) |
| SM Chapter 3 written and merged | Done — `book/Ch12.json` (14/14 headings, 95/95 atoms placed) |
| SM Chapter 4 written and merged | Done — `book/Ch13.json` (15/15 headings, 86/86 atoms placed) |
| SM Chapter 5 written and merged | Done — `book/Ch14.json` (18/18 headings, 80/80 atoms placed); **Section B (SM) is complete** |
| Front matter written | Done — `book/front.json`, six sections (see below) |
| Back matter written | Done — `book/back.json`, eight appendices A–H (see below) |

## Chapter numbering used in the book

`Ch01`–`Ch09` = FM chapters 1–9; `Ch10`–`Ch14` = SM chapters 1–5.
Topic codes: `F01.07.01` prints as "FM Ch 1 §7.1"; `S01.05.02` prints as "SM Ch 1 §1.5.2".

## Next steps (updated 04-10-2026)

**All fourteen chapters are now written and merged — Section A (FM Ch 1–9) and Section B (SM Ch 1–5).**

1. Back-fill pass: the stray official questions listed at the end of this file (FM Ch 1, 3, 4, 5;
   SM Ch 3, 4, 5), then re-run `sources/coverage.py`.
2. ~~Full front matter~~ — **DONE 04-10-2026**, see the section below.
3. Back matter: cross-chapter cases, two mock exams, study plans, mistake book, 24-hour book,
   master question index, PYQ/RTP/MTP matrix, dashboard.
4. Rebuild with `./make_pdf.ps1` (two passes so the index page numbers settle).

## Known gaps carried forward

- ICAI publishes **no examiners' comments for Paper 6**; the book says so and invents none.
- MTP Series II for May 2026 is missing; MTP Series I for September 2026 has only the answer file.
- May 2024 suggested answers contain no MCQ part, so no May 2024 MCQs appear in the book.

## Progress ledger (18-09-2026)
- FM Ch 1 (Ch01.json) — complete: 19/19 headings, 30/30 atoms, keys A11 B11 C10 D10.
- SM Ch 1 (Ch10.json) — complete: 13/13 headings, 102/102 atoms.
- FM Ch 2 (Ch02.json) — complete: 25/25 headings, 29/29 atoms, 12 topic blocks,
  46 generated MCQs (A12 B12 C11 D11, deviation 1.1%), 2 integrated cases, 12+6 chapter test.
- Carried forward: RTP May 2026 FM Q8 (lease-rental computation) is filed by ICAI under
  Investment Decisions, so it belongs to FM Ch 3, not FM Ch 2. Place it when building F03.
- FM Ch 3 (Ch03.json) — complete: 22/22 headings, 33/33 atoms, 12 topic blocks,
  46 generated MCQs (A12 B11 C11 D12, deviation 1.1%), 2 integrated cases, 12+6 chapter test.
  Jan 2026 Q3(a) (external funds requirement) is printed as supplementary: the topic is
  not in the current Study Material but the question is solved with ratios that are.
- New tooling: sources/fm_map.py (question stems per paper), sources/rtp_topics.py
  (ICAI's own chapter label per RTP question — the key for the numerical chapters),
  sources/locate.py (which question a phrase sits in), sources/coverage.py (unplaced
  official questions across all chapters).
- Gap closed in FM Ch 1: Sep 2024 Q2(b) "Explain Angel Financing" was unplaced; it is now
  under FM Ch 1 §2.1 (31 atoms).
- FM Ch 4 (Ch04.json) — complete: 24/24 headings, 31/31 atoms, 12 topic blocks,
  46 generated MCQs (A11 B12 C11 D12, deviation 1.1%), 2 integrated cases, 12+6 chapter test.
- Cross-chapter corrections made while building Ch 4:
  RTP Jan 2026 FM Q6 is the continuation of that RTP's ratio question -> moved to FM Ch 3 (34 atoms).
  MTP Mar 2024 S1 FM Q1(b) (AN Ltd, net operating income) and MTP Mar 2024 S2 FM Q2(b)
  (GT Limited, EPS and P/E) are capital structure questions -> to be placed in FM Ch 5.
  RTP Jan 2026 FM Q7 (J Ltd, MM with taxes) -> FM Ch 5.
  MTP May 2026 S1 FM Q2(a) (Zanshu Ltd) and MTP Jan 2026 S1 FM Q3(a) (Vastupal) -> FM Ch 5.
  MTP Sep 2025 S1 FM Q1(a) (PQR dividend policy) -> FM Ch 8.
  Sep 2024 Q3(b) (ER Private Ltd) and Sep 2025 Q3(a) (AVS Limited) -> FM Ch 5.
- FM Ch 5 (Ch05.json) — complete: 19/19 headings, 36/36 atoms, 13 topic blocks,
  48 generated MCQs, 2 integrated cases, 12+6 chapter test.
- Gap closed in FM Ch 2: RTP Jan 2026 FM Q11(b) (spontaneous sources of finance) was
  unplaced; now under FM Ch 2 §7 (30 atoms).
- New tooling: sources/qstruct.py — the true question/sub-part structure of every paper's
  FM descriptive section, used to get atom ids right (embedded numbered lists inside a
  question otherwise derail the parser).
- PDF checkpoint after FM Ch 5: 742 pages, 222 bookmarks, 70 clickable index links,
  scan_pdf CLEAN. Builder fix: PART_RE in book/build_fmsm_book.js did not recognise the
  "FMCQ<n>" id form (FM MCQ in an MTP Part I), so one internal id printed in the text on
  a Ch 2 page. PART_RE now reads [FS]?MCQ<n> and partName renders "FM MCQ 4".
- Tooling note: do NOT write .js/.py test files through a bash heredoc when the content
  contains backslashes - the heredoc halves them and the test lies. Use the Write tool.

## FM Ch 6 — Financing Decisions: Leverages — DONE (22-09-2026)
- sources/f06/u1..u4.json -> book/Ch06.json
- SM headings 16/16 · official atoms 33/33 · 12 topic blocks · 17 official question entries
- Generated MCQ keys A13 B10 C12 D11 (46) · max deviation 3.3%
- Open items: OV-F06-01 (SM §4.2 calls ROI = interest unfavourable, §4.3 calls it neutral — both reproduced, not harmonised), OV-F06-02 (MTP Sep 2026 S1 question paper unavailable), OV-F06-03 (business vs financial risk assembled from §3/§4/§5.2)
- Correction made before merge: Integrated Case 2 q1 first draft argued itself to a different option than its answer field; rewritten so the answer (C) follows the reasoning. Same class of error as CASE-F03-INT-1. **Check every case MCQ's answer field against its own final line before merging.**

## FM Ch 7 — Investment Decisions — DONE (03-10-2026)
- sources/f07/u1..u4.json -> book/Ch07.json
- SM headings 33/33 · official atoms 35/35 · 18 topic blocks · 35 official question entries
- Generated MCQ keys A14 B14 C14 D14 (56) · max deviation 0.0%
- New atom id forms used, both already supported by PART_RE in book/build_fmsm_book.js:
  `PYQ-<paper>-MCQ<n>` for a past paper's Part I MCQ (Sep 2024 case scenario, May 2026 MCQs 7 and 8)
  and `MTP-<paper>-S<n>-FMCQ<n>` for an MTP Part I case (Sep 2025 S1 Baton/Katon, Sep 2026 S1 waste
  processing). Verified in the built docx: no raw ids leak, all forms render.
- Open items: OV-F07-01 (RTP Jan 2025 Q9 charges terminal-year depreciation although the asset is the
  only one in its block, which SM §6.1 Case 1 says carries none — both treatments reproduced),
  OV-F07-02 (MTP Mar 2024 S1 NC Ltd computes the capital-loss shield at 30% while the question's tax
  rate is 40%), OV-F07-03 (MTP Sep 2026 S1 question paper unavailable; its Part I case reconstructed
  from the answer file), OV-F07-04 (ICAI's May 2024 suggested answers print no mark allocation for
  Q3(a), and QP-M24.pdf has no text layer — marks recorded as null, evidence table shows a dash),
  OV-F07-05 (RTP Sep 2026 Q7 selects Machine I on a majority of three rankings although NPV and, given
  the unequal lives, the equivalent annualised criterion favour Machine II), OV-F07-06 (MTP Jan 2025 S1
  MCQ 7 prints "PVAF (15,4 years)" where the answer uses PVAF(10%, 5) = 3.79), OV-F07-07 (MTP Sep 2025
  S1 option (ii)(b) prints ₹(14,071) against the answer's ₹(14,077)), OV-F07-08 (capital rationing,
  SM §11.1, has not been asked in any past paper, RTP or MTP in the period reviewed — a standing gap,
  covered by a chapter-test descriptive question for that reason), OV-F07-09 (SM Illustration 18 and
  RTP May 2024 Q5 are the same HMR Ltd question with different figures and the two depreciation
  methods reversed).
- Every case MCQ answer field was checked against its own final reasoning line before merge, per the
  rule carried forward from FM Ch 6. Three chapter-test MCQs had their option order rotated purely to
  bring the key balance to an exact 25% each; their explanations do not reference option letters.
- Tooling note: LibreOffice in the cloud container cannot load any .docx produced by the `docx` npm
  package (a trivial one-paragraph file fails the same way), so the PDF cannot be rebuilt on Linux.
  The docx itself builds clean — `node book/build_fmsm_book.js book build/...docx`, 1.00 MB,
  1,725,318 characters of text, zero leaked internal ids. **The PDF still needs `./make_pdf.ps1` on
  Windows.** `build/` is now gitignored.
- Carried forward for the next chapter: PYQ-S24-Q1b (SK Limited, operating cycle method) is working
  capital, so it belongs to FM Ch 9, not FM Ch 7. MTP-J26-S2-FQ4b (meaning of cost of capital) and
  MTP-S25-S2-FQ2a (ABC Engineering, risk-return profile) were checked against Ch 7 and belong to
  FM Ch 4 and FM Ch 6 respectively.

## FM Ch 8 — Dividend Decisions — DONE (03-10-2026)
- sources/f08/u1..u4.json -> book/Ch08.json
- SM headings 16/16 · official atoms 38/38 · 10 topic blocks · 38 official question entries
- Generated MCQ keys A10 B10 C10 D10 (40) · max deviation 0.0%
- **Two topic blocks carry the same register code, F08.10**, because SM §8.2 "Dividend's Relevance
  Theory" holds both Walter's Model and Gordon's Model and 24 of the 38 atoms are primary to it.
  This is safe: `renderConcept` in book/build_fmsm_book.js prints only `c.title`, never the code, so
  the two render as "8.2 Dividend's Relevance Theory (i) — Walter's Model" and "(ii) — Gordon's
  Model, the Bird-in-hand Theory and the Dividend Discount Model".
- **Lintner's Model is placed in §7 (F08.07), not §8.** The SM body puts it under Practical
  Considerations in Dividend Policy and the §8.1 diagram shows only MM, Walter and Gordon; only the
  chapter-overview diagram on the opening page lists Lintner as a fourth theory. The register follows
  the body. MTP-S24-S1-FQ3b therefore carries primary code F08.07 — see OV-F08-01.
- Questions that value a share from a dividend and a growth rate are treated as Gordon / the Dividend
  Discount Model under F08.10, whatever the question calls them.
- Open items: OV-F08-01 (Lintner in §7 against the overview diagram), OV-F08-02 (RTP Sep 2026 Q6
  tests the "radical position", which is not in the current SM at all — printed with the theory
  supplied), OV-F08-03 (RTP May 2025 Q8 gives three probabilities summing to 1.40 and ICAI's answer
  still reports an expected ROI of 21% — reproduced, with the normalised 15% noted), OV-F08-04
  (ICAI's May 2024 answers print no mark allocation for Q3(b) and QP-M24.pdf has no text layer —
  marks null, evidence table shows a dash, the same position as Ch 7's Q3(a)), OV-F08-05 (SA-S25
  Q2(b) Saraswati Ltd renders its data column out of order; the arithmetic settles the reading),
  OV-F08-06 (RTP Jan 2026 Q10 "retention ratio reduced by 20 percent" taken by ICAI as 20 percentage
  points), OV-F08-07 (Walter's and Gordon's tables word the r = Ke case in opposite terms — both
  reproduced, neither harmonised, and the chapter test carries an MCQ on the distinction), OV-F08-08
  (Gordon gives a nil price at 100% retention and very large prices as br approaches Ke — properties
  of the model, flagged where they arise), OV-F08-09 (§3 and §6 taxation paragraphs are
  edition-sensitive and marked update_sensitive), OV-F08-10 (MTP May 2026 S1 Zanshu Ltd is a buyback
  financed by debt to change the capital structure — a Ch 5 question, already in atoms_F05.json).
- Every case MCQ answer field was checked against its own final reasoning line before merge, and all
  back-matter arithmetic was re-derived independently. One chapter-test MCQ had options C and D
  swapped purely to bring the key balance to an exact 25% each; its explanation references only
  option A, so no text changed.
- Chapter 4 defect found and fixed while scoping this chapter: the atom `PYQ-J26-Q1c` in
  `sources/atoms/atoms_F04.json` was in fact SA-J26 FM **Part I Case Scenario I** (AB Infra Projects
  Limited, MCQs 1–5), not Q1(c), and it occupied the id that Chapter 8 needs for the real Q1(c)
  (PQR Ltd — Gordon and MM). Renamed to **`PYQ-J26-MCQ1`** across `atoms_F04.json` and
  `sources/f04/u1..u3.json` (6 occurrences), and the pyq_table question text corrected from
  "PQR Ltd: CAPM, irredeemable preference…" to name AB Infra Projects Limited. `book/Ch04.json`
  regenerated; still ERRORS: none.
- Tooling note unchanged from Ch 7: the docx builds clean (1,989,256 characters of text, zero leaked
  internal ids, every PYQ/RTP/MTP label form rendering), but LibreOffice in the cloud container
  cannot load any .docx the `docx` npm package produces, so **the PDF still needs `./make_pdf.ps1`
  on Windows.**
- Carried forward: nothing new. PYQ-S24-Q1b remains queued for FM Ch 9.

## FM Ch 9 — Management of Working Capital — DONE (03-10-2026)
- sources/f09/u1..u9.json -> book/Ch09.json  (nine unit files, one per group of blocks)
- SM headings 68/68 · official atoms 51/51 · 26 topic blocks · 51 official question entries
- Generated MCQ keys A18 B18 C18 D18 (72) · max deviation 0.0%
- **The largest chapter in the paper and the most heavily examined**: 51 official question parts
  against Ch 7's 35 and Ch 8's 38. Two topics take almost a third of them — credit policy
  evaluation (8 questions) and factoring (9 questions).
- Block layout follows the SM's six units: 8 blocks for Unit I (F09.01–F09.16), 7 for Unit II
  (F09.17–F09.41), 7 for Units III–V (F09.42–F09.55) and 4 for Unit VI (F09.56–F09.68).
- Two new findings worth recording for later chapters:
  * **Five of the fourteen paper sets put a ten-mark working-capital case in Division A** —
    SA May 2025 (XYZ Ltd), SA Sep 2025 (RG Limited), RTP Jan 2025 (Samvar Ltd), RTP Jan 2026
    (PPW Ltd) and MTP Mar 2024 S1 (NV Industries). No other chapter is used that way.
  * **ICAI republishes whole questions across paper types.** MTP Mar 2024 S2 Q1(a) (Lever Ltd,
    5 marks descriptive) reappears unchanged as RTP Jan 2026's five-MCQ Division A case (PPW Ltd);
    MTP Mar 2024 S1's factoring case reappears as RTP Sep 2025 Q9 and RTP Sep 2026 Q8 with only
    the bad-debt percentage and the comparison rate changed.
- Open items OV-F09-01 to OV-F09-15. The substantive ones: Bright Ltd published with three
  different answers (7.504% / 6.730% / a 70-day variant); X Ltd applying the same 2% commission
  to credit sales in one place and to receivables in another; Parshvam's 15% safety margin applied
  to a base ₹25,000 above the stated excess; Nirmoh deducting the reserve before applying the
  lending percentage (a double haircut); the margin-of-safety wording differing between a mark-up
  and a gross-up across three questions; May 2026 MCQ 6 pairing the incremental investment with
  only the opportunity-cost saving and not the contribution; and MTP Sep 2026 S2 specifying
  2/15 net 60 then assuming the discount is not availed.
- Standing gaps recorded, not papered over: **no EOQ or inventory-valuation computation** has been
  asked in Paper 6A in the period reviewed (ICAI cross-refers Unit III to Paper 4 Ch 2), and
  **§10.3–§10.5 on managing collections and disbursements is unexamined** — both carry
  chapter-test questions for that reason.
- `RTP-J26-FQ11b` (spontaneous sources of finance) was already placed in FM Ch 2 under F02.22
  Short-term Sources of Finance. It is left there and cross-referenced from the §27.1 block rather
  than moved out of a merged chapter.
- Every case MCQ answer was checked against its own final reasoning line, and all generated
  arithmetic was re-derived independently before the merge. Case 1's two estimation methods were
  reconciled on purpose (₹8,80,000 by the operating cycle against ₹11,40,000 by the component
  statement, the difference being accruals, the cash balance and the prepayment) and the case asks
  the student to explain the gap. One chapter-test MCQ had a compounded-rate option corrected from
  29.8% to 28.0% after independent recomputation.
- Six MCQs had their option order rotated purely to bring the key balance to an exact 25% each;
  the explanations were updated where they referenced an option letter.
- Tooling note unchanged: the docx builds clean (2,653,835 characters of text, 1.43 MB, zero
  leaked internal ids), but LibreOffice in the cloud container cannot load anything the `docx` npm
  package produces, so **the PDF still needs `./make_pdf.ps1` on Windows.**

## SM Ch 2 — Strategic Analysis: External Environment — DONE (03-10-2026)

`book/Ch11.json`, built from `sources/s02/u1.json` to `u8.json` and `sources/atoms/atoms_S02.json`.

Merge output: 24/24 register headings covered, 91/91 official atoms placed, 19 topic blocks,
38 official question entries, 30 official MCQ entries, 64 generated MCQs with keys
**A16 B16 C16 D16 (deviation 0.0%)**, 2 integrated cases, 13+6 chapter test, zero errors and
zero placement warnings. Docx scan: no raw official ids, no `S02.xx` codes, no internal ids,
no placeholder words.

This is the largest SM chapter in the paper. Atom mix: 21 past-paper items, 17 RTP descriptive
questions, 17 RTP MCQ items, 29 MTP descriptive questions, 7 MTP case-MCQ items.
Heaviest headings: Porter's Five Forces (17 atoms), Competitive Landscape (16), PESTLE (10),
Value Chain (8), Product Life Cycle (7).

One atom was added after the first merge, while scoping SM Ch 3: RTP May 2026 SM Q11 sits
under ICAI's own "Chapter 3" label but its published answer is Strategic Group Mapping,
described there as "an important tool of industry (competitive) environment analysis". The
register has no strategic-group-mapping heading in Chapter 3, so it is placed at S02.23.

**The mapping discovery that made SM mapping tractable:** ICAI's RTPs print their own chapter
headings — "Chapter 2-Strategic Analysis: External Environment" — above the questions belonging
to each chapter, and every RTP from May 2024 to September 2026 places exactly two questions
(always numbered 9 and 10) under the Chapter 2 heading. For those 16 atoms the mapping is
transcription, not judgement. The same labels will carry SM Ch 3–5.

**Seven mapping corrections made after reading ICAI's published answers in full** (all recorded
in the chapter's `verification.open_items` and in the note field of `atoms_S02.json`):

- `PYQ-M25-MCQ15` removed — set "in a competitive landscape" but ICAI's key is *special alert
  control*, an SM Ch 5 concept. Back-fill to SM Ch 5.
- `PYQ-M25-MCQ12` removed — ICAI's key is *augmented marketing*, defined in SM Ch 3 under types
  of marketing, not in Chapter 2's value chain. Back-fill to SM Ch 3.
- `RTP-M24-SQ9` and `RTP-J26-SQ9` (Riya Sharma's confectionery) moved from S02.13/S02.14 to
  **S02.23** — the stem reads like industry rivalry but ICAI answers with the five steps of the
  competitive landscape.
- `PYQ-J26-Q5a` (Full Health Limited) moved from S02.15 to **S02.23** — reads like industry
  attractiveness but ICAI answers with strategic group mapping.
- `MTP-M25-S2-SQ1a` (ABC Tech) — S02.24 made primary; the stem names three value-chain
  activities but ICAI's answer is framed wholly as Key Success Factors.
- `RTP-S26-SMCQ3` (FreshKart Retail) — S02.06 made primary; the stem opens with changing
  customer preference but the published key is *technological environment*.

**ICAI inconsistencies documented rather than smoothed over:**

- The study material says consumer behaviour's influences fall into "three conceptual domains"
  and then prints **four** headings. ICAI's own answers resolve it both ways — MTP Jan 2025 S1
  avoids the number, MTP Jan 2026 S2 says "four major conceptual domains". The chapter says to
  write four.
- ICAI files **value chain analysis** under Chapter 2 in its RTP labels (Sep 2025 Q10 and
  Sep 2026 Q10 both sit under the Chapter 2 heading) although it is widely taught as internal
  analysis; and it files some **strategic group mapping** questions under Chapter 3 although the
  register places Competitive Landscape at S02.23. The register is followed; both are recorded.
- ICAI's PESTLE answers head the third factor "Social Factors" while the study material heads it
  "socio-cultural".

**Headings with no official question of their own:** S02.01 Introduction, S02.17 Value Creation,
S02.18 Market & Customer and S02.19 Customer carry no atom at all; S02.15 Attractiveness of
Industry, S02.20 Customer Analysis and S02.22 Competitive Strategy appear only as secondary
codes. All seven are written up in full with expected questions and chapter-test coverage,
because four of them are new in the 2026 syllabus edition and are overdue for examination.

**Tooling added for the SM section** (in the session scratchpad): `qa.py` resolves an atom id to
its full published question text plus ICAI's answer across SA, RTP and MTP files; `mcqd.py`
resolves an MCQ atom id to its stem and four options. Both will be reused for SM Ch 3–5.

## SM Ch 3 — Strategic Analysis: Internal Environment — DONE (04-10-2026)

`book/Ch12.json`, built from `sources/s03/u1.json` to `u5.json` and `sources/atoms/atoms_S03.json`.

Merge output: 14/14 register headings covered, 77/77 official atoms placed, 10 topic blocks,
26 official question entries, 30 official MCQ entries, 44 generated MCQs with keys
**A11 B11 C11 D11 (deviation 0.0%)**, 2 integrated cases, 13+6 chapter test, zero errors and
zero placement warnings. Docx scan: no raw official ids, no `S03.xx` codes, no internal ids,
no placeholder words. The whole book is now 3,393,608 characters.

Atom mix: 14 past-paper items, 22 RTP items, 41 MTP items. Heaviest headings: Porter's generic
strategies (23 atoms), Mendelow's Matrix (18), core competency (14 across §3.4 and §3.4.1),
strategic drivers (7), channels (6), SWOT (5).

**The RTP labelling pattern is now established as exact.** Across all nine RTPs from May 2024 to
September 2026, ICAI places Chapter 1 at questions 7–8, Chapter 2 at 9–10, Chapter 3 at 11–12,
Chapter 4 at 13–14 and Chapter 5 at 15–16, without exception. That converts RTP mapping for the
remaining SM chapters from judgement into transcription: **SM Ch 4 takes RTP Q13 and Q14, SM Ch 5
takes RTP Q15 and Q16**, nine papers each.

**Two labelling tensions recorded rather than smoothed over:**

- `RTP-M26-SQ11` is labelled Chapter 3 but answered as strategic group mapping, so it is held in
  `atoms_S02.json` at S02.23 (committed separately before this chapter).
- `RTP-S26-SQ13` is labelled Chapter 4 but answered as the Focused Differentiation Strategy, which
  Chapter 4's headings (stability, growth, exits, Ansoff, ADL, BCG, GE) have no home for, so it is
  placed here at S03.14.

**Three atoms excluded after reading the published answer in full** — each stem reads like
Chapter 3 but the answer belongs elsewhere (all three are in the back-fill list):

- `PYQ-S24-Q5a` (M/s MTS Ltd) — the stem ends "focusing on its core competencies" but ICAI's
  answer is the **Network Organizational Structure** -> SM Ch 5.
- `PYQ-J25-Q5c` and `MTP-J26-S1-SQ1c` (Organic Beverages) — answered with the **BCG matrix** -> SM Ch 4.
- `PYQ-M26-Q5c` (MM Company at maturity) — answered as **Stability Strategy** -> SM Ch 4.

**One atom moved in**: `PYQ-M25-MCQ12`, whose published key is "Augmented marketing", a term the
study material defines in this chapter at §3.3.3 under types of marketing. It had been removed
from SM Ch 2 for that reason and is now placed.

**The chapter's own hazard, handled with a dedicated table.** Three four-item lists and one
three-item list sit within four pages of each other and are examined separately: the three areas
of core competency (§3.4), the four criteria that qualify a capability as one (§3.4.1, VRIN), and
the four characteristics that determine how long the resulting advantage lasts (§3.6.1,
durability/transferability/imitability/appropriability). The back matter opens with a
trigger-word table that selects the right list from the stem's wording, because the registers of
the three stems are nearly identical.

**One atom added after the first merge**, while scoping SM Ch 4: `PYQ-S24-Q5c` (M/s. Maa ki
Pasand) is set in a Chapter 4-shaped case about new products for existing and new customers, but
the question asks which of **Porter's business-level strategies** applies and ICAI's answer is a
focus strategy combining focused cost leadership and focused differentiation. Placed at S03.14.

**Extraction note**: the automated sub-part slicer mis-aligned the (a)/(b) boundaries in the
May 2026 suggested answers, so the answers to PYQ May 2026 Q5(b) (Pearl India, differentiation)
and Q7(b) (channels) were read directly from `sources/sa/SA-M26.txt` at lines 1439–1475 and
1659–1695. The line numbers are recorded in the chapter's verification block so the quotations
can be re-checked.

## SM Ch 4 — Strategic Choices — DONE (04-10-2026)

`book/Ch13.json` — 15/15 register headings, 83/83 official atoms placed, 9 topic blocks,
28 official question entries, 32 official MCQs, 44 generated MCQs at
`{'A': 11, 'B': 11, 'C': 11, 'D': 11}` — **0.0% deviation on the first merge**, zero errors.

Block layout (`sources/s04/u1..u5.json`):

| Unit | Blocks | Codes |
| --- | --- | --- |
| u1 | 1–3 | `S04.01 + S04.02`, `S04.03 + S04.04 + S04.05` (Stability), `S04.06 + S04.07 + S04.08` (Growth) |
| u2 | 4 | `S04.09` — Types of Growth/Expansion, 23 atoms (the chapter's largest block) |
| u3 | 5–6 | `S04.10` Strategic Exits (10 atoms), `S04.11 + S04.12` Strategic Options and Ansoff (11 atoms) |
| u4 | 7–9 | `S04.13` ADL, `S04.14` BCG (10 atoms), `S04.15` GE Stop-Light |
| u5 | — | back matter: 3 Confusing Concepts tables, 2 integrated cases, 13+6 chapter test, recall, revision, one-pager, verification (9 open items) |

**The RTP chapter-label rule held exactly.** Every RTP from May 2024 to September 2026 prints
its own chapter headings over the SM descriptive questions, and **SM questions 13 and 14 are
Chapter 4** in all nine. Eighteen RTP questions, all on this chapter's material, with one
exception: `RTP-S26-SQ13` sits under the "Chapter 4" label but is answered as the **Focused
Differentiation Strategy**, which none of this chapter's fifteen headings can house — that atom
stays in `atoms_S03.json` at `S03.14`. A labelling artefact to know about: in several RTP files
the chapter-label line physically *follows* the question text, so `RTP-S25-SQ14` and
`RTP-M25-SQ14` appear in the raw text under a "Chapter 5" line that belongs to the next question.

**Two atoms moved in** after reading the published answers in full: `PYQ-J25-Q5c` with
`MTP-J26-S1-SQ1c` (Organic Beverages 'Say no to Sugar' — BCG classification, post-identification
strategies, limitations) and `PYQ-M26-Q5c` (MM Company at maturity — Stability Strategy). Both
were on the SM Ch 3 back-fill list and are now cleared.

**One atom clash resolved against this chapter.** `MTP-S25-S2-SMCQ-A-iv` appeared in both
`atoms_S01.json` and the S04 draft; its four options are corporate / business / functional /
network **level**, with ICAI's key (a) = corporate-level strategy, so S01 was right and the atom
was removed from S04.

**Three stems that look like Chapter 4 were excluded** after reading the answer:
`PYQ-S24-Q5c` (M/s. Maa ki Pasand — answered as a focus strategy, SM Ch 3), `PYQ-M24-Q5a`
(BOYA Ltd — answered with the McKinsey 7S Model, SM Ch 5) and `MTP-M24-S2` case A(iii)
(Café Delight — marketing tactics, no named growth strategy). A fourth, `MTP-S25-S2` case A(iv)
(Nav-Uday exporting to less competitive markets), looks like Ansoff market development but its
published key is "Corporate-level strategy", so it stays at `S01.06`.

**Two ICAI inconsistencies documented rather than smoothed over:**

1. **The GE colour-zone conflict.** The study material's printed nine-cell grid places
   *Low market attractiveness × Average business strength* in **Harvest/Divest**, which §4.4.4
   describes as the **red** zone ("the appropriate strategy should be retrenchment, divestment
   or liquidation"). ICAI's suggested answer to `RTP-S26-SQ14` calls the same cell the
   **"Yellow Zone (Selective Growth/Earnings Zone)"**. Both texts are quoted verbatim in the
   `S04.15` block, and the exam advice given is to lead with the substance both readings share —
   selective investment if the position can be improved, otherwise harvest or divest.
2. **Liquidation has no numbered sub-section.** The Chapter Overview diagram lists Liquidation as
   the third strategic exit, but §4.3 numbers only *I. Turnaround* and *II. Divestment*, defining
   liquidation in its lead-in sentence alone. It reappears in the BCG dog prescription and the
   GE red zone. Also noted: the heading "Major Reasons for Retrenchment/Turnaround Strategy"
   introduces a seven-item list that is really the five divestment reasons plus two more.

**Sixteen official MCQ atoms were added in a second pass.** The first pass mapped the descriptive
questions thoroughly but under-swept the Part-I MCQ bank. A systematic sweep of *every* unplaced SM
Part-I item across the SA, RTP and MTP files found sixteen that are Chapter 4 material: five on
diversification and alliances (`S04.09`), three on the strategic exits — including
`RTP-S26-SMCQ5`, **the only Liquidation MCQ in the whole official bank** — four on Ansoff
(`S04.12`), one on stability (`S04.04`), one on BCG resource allocation (`S04.14`) and two on the
GE matrix (`S04.15`). Note for the remaining chapters: **`mcqd.py` returns zero candidate blocks
for SA files**, so SA MCQ stems have to be read directly from `sources/sa/*.txt`, and the RTP MCQ
keys sit in a compact table under the *last* `SUGGESTED ANSWERS` heading of each RTP file.

**A third pass, sweeping the descriptive bank the same way, found three more.** `MTP-S24-S1-SQ1c`
(FreshDelight, answered as **market development** — a deliberate contrast with the ABC Fashion
diversification case, since only the market changed), `MTP-S25-S1-SQ1c` (ZephyrFit, answered as a
**divestment strategy**) and `PYQ-S24-MCQ15` (Always Ahead Ltd., key **Build**). The last was
invisible to the MCQ sweep because **`sa_smcq.py` does not cover SA-S24 at all** — that paper's
MCQ section has to be read straight out of `sources/sa/SA-S24.txt`, where the SM answer key sits
under the *second* `Answer Key` heading (MCQs 9–16). Worth knowing before the back-fill pass: the
same blind spot hides SA-S24 MCQs 10, 11 and 12, which belong to SM Ch 2 and Ch 3.

Four MCQ atoms found in the same sweep belong to other chapters and are queued for back-fill:
`RTP-M24-SMCQ5` (Mendelow, key b), `RTP-S24-SMCQ4` (core competency areas, key d),
`RTP-M26-SMCQ5` (differentiation, key c) and `PYQ-M26-MCQ14` (best-cost provider, key B) to
SM Ch 3; and `RTP-M25-SMCQ5` (experience curve, key a) once its heading is confirmed.

**Extractor note.** `PYQ-S25-MCQ14` (Bio Cure, ADL) returned no candidate block from `mcqd.py`,
so its stem and options were read directly from `sources/sa/SA-S25.txt` lines 208–220; recorded
in the chapter's `verification.open_items` so the quotation can be re-checked.

**The chapter's question profile**, for the front-matter weightage work: Ansoff's grid is the most
repeated single question (five near-identical appearances), concentric vs conglomerate the most
repeated distinguish (four), and BCG the most tested model (ten appearances, five of them MCQs).
Four of the last five sittings carried a strategic-exit case at Q5.

## SM Ch 5 — Strategy Implementation and Evaluation — DONE (04-10-2026)

`book/Ch14.json` — 18/18 register headings, 80/80 official atoms placed, 11 topic blocks,
28 official question entries, 24 official MCQs, 56 generated MCQs at
`{'A': 14, 'B': 14, 'C': 14, 'D': 14}` — **0.0% deviation**, zero errors.
**This completes Section B, and with it all fourteen chapters of the book.**

Block layout (`sources/s05/u1..u6.json`):

| Unit | Blocks | Codes |
| --- | --- | --- |
| u1 | 1–2 | `S05.01 + S05.02 + S05.03` (process and five stages), `S05.04` (formulation: strategic vs operational planning, strategic uncertainty) |
| u2 | 3–4 | `S05.05 + S05.06` (implementation, the A-B-C-D and efficiency matrices, the difference table), `S05.07` (linkages and issues) |
| u3 | 5–6 | `S05.08 + S05.09 + S05.10` (strategic change, Kurt Lewin, how digital transformation works), `S05.11 + S05.12` (the five SME best practices and the five pointers) |
| u4 | 7–8 | `S05.13` (McKinsey 7S, 10 atoms), `S05.14` (Organization Structure, **18 atoms — the largest heading in the book**) |
| u5 | 9–11 | `S05.15 + S05.16` (culture and strategic leadership), `S05.17` (strategic control), `S05.18` (strategic performance measures) |
| u6 | — | back matter: 3 Confusing Concepts tables, 2 integrated cases, 15+6 chapter test, recall, revision, one-pager, verification (10 open items) |

**The RTP chapter-label rule held again, and the count was corrected.** SM questions **15 and 16
are Chapter 5** in all eight RTPs from May 2024 to September 2026. Note the correction recorded in
`atoms_S05.json`: the note in `atoms_S04.json` says "all nine RTPs"; there are **eight** RTP files
(M24, S24, J25, M25, S25, J26, M26, S26). The pattern itself is unaffected.

**A wording trap worth carrying into the back-fill pass.** ICAI uses two near-identical phrasings
for two different printed lists. *"Most preferred practices"* for a small or mid-sized business
(Twaran, BrightWave, Nexora) → **§5.3.3's five best practices** (begin at the top; necessary and
desired; reduce disruption; encourage communication; change is the norm). *"Key strategies for
**navigating** change effectively"* (RTP-M24-SQ16) → **§5.3.4's five pointers** (specify aims;
always communicate; be ready for resistance; implement gradually; offer assistance and training).
The word *navigating* is §5.3.4's own heading, and the published answer to RTP-M24-SQ16 confirms
it, so that atom is filed at `S05.12`, not `S05.11`.

**Three stems that read like Chapter 5 were excluded** after reading the published answer:
`MTP-S24-S1-SQ1c` (FreshDelight — market development), `MTP-S25-S1-SQ1c` (ZephyrFit — divestment)
— both now placed in SM Ch 4 — and `MTP-M24-S2-SQ1c` (GreenThrift — threat of new entrants,
SM Ch 2). **Two atoms were moved in**: `PYQ-M24-Q5a` (BOYA Ltd., McKinsey 7S with limitations) and
`PYQ-M25-MCQ15` (key: special alert control).

**Extractor notes for the back-fill pass.** `qa.py` returns a wrong fragment for `PYQ-M26-Q8a`, so
that stem and answer were read directly from `sources/sa/SA-M26.txt` (lines 1694 and 1712 onward).
`RTP-J25-SMCQ1-ii` and `-iii` have truncated option lists in `mcqd.py` output. And, as recorded
under SM Ch 4, `sa_smcq.py` does not cover SA-S24 at all, whose SM answer key sits under the
**second** `Answer Key` heading of that file.

**The chapter's question profile**, for the front-matter weightage work: the most repeated question
in the chapter is the five **pointers for navigating change** (four appearances); the most repeated
case is **PQR Ltd.'s SBU restructuring** (four); **SPM** carries nine atoms across three different
lists (six types, four reasons, four selection factors), and **organization structure** eighteen,
of which the SBU takes seven and the matrix five. The **McKinsey 7S** is the most MCQ-heavy heading
in the paper, with seven of its ten atoms being MCQs. Nothing in the chapter is computational.

## Back-fill list found while scoping FM Ch 7 (coverage.py, 22-09-2026)
These official questions belong to chapters already merged and were not in their atom files. Add them in a back-fill pass after FM Ch 9:
- MTP-J26-S2-FQ4b (meaning of cost of capital + three reasons it matters) -> FM Ch 4
- MTP-M24-S1-FQ3a (Ram Ltd — rates on bank loan and debentures, PE multiple 4) -> FM Ch 4
- RTP-S26-FQ1 (AURO Engineering Pvt. Ltd. case scenario MCQs) -> FM Ch 4
- MTP-S24-S2-FQ1a (X Ltd — point of indifference, ₹84 lakh) -> FM Ch 5
- MTP-S25-S2-FQ4a (Project X vs Project Y — profit vs wealth maximisation vs value creation) -> FM Ch 1
- MTP-M24-S2-FQ4a and MTP-S26-S2-FQ4a (inter-relationship between investment, financing and dividend decisions) -> FM Ch 1

## Back-fill list found while scoping FM Ch 9 (03-10-2026)
These six match a working-capital keyword but are ratio-analysis questions, and belong to FM Ch 3:
- PYQ-J25-MCQ6 and PYQ-J25-MCQ7 (VP Ltd Case Scenario II — inventory, receivables, CA and CL from ratios)
- PYQ-J26-Q1a (AIL Limited — inventory, working capital and the Basic Defense Interval)
- PYQ-J26-Q4c-OR (BEE Ltd — whether each transaction improves or worsens a 2:1 current ratio)
- MTP-J26-S2-FQ1a (debtors and creditors velocity, stock turnover, fixed assets to turnover)
- MTP-S24-S1-FQ1a (Ananya Limited — total current assets from stock turnover and liquidity ratio)
- MTP-S25-S1-FQ1b (Gagan Pvt. Ltd. — current ratio and the components behind it)
- MTP-S26-S2-FMCQ1 (Solstice Biotech Part I case — current, quick, turnover, debt and profitability ratios)

## Back-fill list found while building SM Ch 2 (03-10-2026)
Two official SM MCQs were removed from `atoms_S02.json` because ICAI's published key names a
concept that belongs to another chapter. Place them when those chapters are built:
- PYQ-M25-MCQ15 (M/s A, B and C — merger forcing an intense review of strategy; key: special
  alert control) -> SM Ch 5
- PYQ-M25-MCQ12 (elevating customer service through a better interface, online repair and on-site
  service; key: augmented marketing) -> SM Ch 3

## Back-fill list found while building SM Ch 3 (04-10-2026)
Official SM questions whose published answer belongs to a chapter not yet built:
- PYQ-S24-Q5a (M/s MTS Ltd — outsourcing and core competencies; key: Network Organizational
  Structure, with merits and demerits) -> SM Ch 5 (S05.14)
- PYQ-J25-Q5c and MTP-J26-S1-SQ1c (Organic Beverages 'Say no to Sugar'; answered with the BCG
  growth-share matrix, the strategies after classification and the technique's limitations) -> SM Ch 4
- PYQ-M26-Q5c (MM Company's tubeless tyre at maturity; answered as Stability Strategy) -> SM Ch 4

## Back-fill list found while building SM Ch 4 (04-10-2026)
Cleared from the SM Ch 3 list: `PYQ-J25-Q5c`, `MTP-J26-S1-SQ1c` and `PYQ-M26-Q5c` are now placed
in `atoms_S04.json`. Still outstanding for SM Ch 5:
- PYQ-S24-Q5a (M/s MTS Ltd — Network Organizational Structure, with merits and demerits) -> SM Ch 5 (S05.14)
- PYQ-M24-Q5a (BOYA Ltd — answered with the **McKinsey 7S Model**) -> SM Ch 5
- PYQ-M25-MCQ15 (key: **special alert control**) -> SM Ch 5
- RTP-M24-SMCQ5 (Mendelow, key b), RTP-S24-SMCQ4 (core competency areas, key d), RTP-M26-SMCQ5
  (differentiation strategy, key c) and PYQ-M26-MCQ14 (best-cost provider strategy, key B) -> SM Ch 3
- RTP-M25-SMCQ5 and PYQ-S24-MCQ11 (experience curve, keys a and A) -> heading to be confirmed, then placed
- PYQ-S24-MCQ10 (product life cycle, maturity stage, key B) -> SM Ch 2 (S02.11)
- PYQ-S24-MCQ12 (focus differentiation strategy, key C) -> SM Ch 3 (S03.14)
- MTP-M24-S2-SQ1c (threat of new entrants) -> SM Ch 2; MTP-J25-S2-SQ1c (focused differentiation) -> SM Ch 3

## Back-fill list found while building SM Ch 5 (04-10-2026)
The SM Ch 5 sweep covered **every** unplaced SM Part-I item and descriptive sub-part. Everything
belonging to Ch 4 was placed there (19 atoms across three patches). What remains belongs to
SM Ch 1, 2 and 3 and is the full input to task #18:

**To SM Ch 2:** PYQ-S24-MCQ10 (product life cycle, maturity, key B) · MTP-M24-S2-SQ1c (threat of
new entrants) · RTP-M24-SMCQ1-ii (countering innovation risk with value-added services, key b)
**To SM Ch 3:** RTP-M24-SMCQ5 (Mendelow, key b) · RTP-S24-SMCQ4 (core competency areas, key d) ·
RTP-M26-SMCQ5 (differentiation, key c) · PYQ-M26-MCQ14 (best-cost provider, key B) ·
PYQ-S24-MCQ12 (focus differentiation, key C) · PYQ-J25-MCQ16 (internal analysis, key B) ·
PYQ-J26-MCQ10 (strength, key C) · PYQ-M26-MCQ9 (initial competitive strategy, key C) ·
RTP-J26-SMCQ1-v (differentiation, key b) · RTP-S26-SMCQ1-iii (best-cost, key c) ·
RTP-S25-SMCQ3 (SWOT, key b) · RTP-S25-SMCQ4 (Mendelow, key c) · RTP-S25-SMCQ1-iii ·
MTP-J25-S2-SQ1c (focused differentiation) · PYQ-J25-MCQ12 and MCQ13 (value chain) ·
PYQ-J26-MCQ16 (synchro-marketing, key D)
**To SM Ch 1 or 2, heading to be confirmed:** RTP-M25-SMCQ5 and PYQ-S24-MCQ11 (experience curve,
keys a and A) · RTP-M24-SMCQ3 (Kanika/Kolor, key b) · RTP-S24-SMCQ1-i/ii/iii/v (MuseoGoa) ·
PYQ-J26-MCQ12 (socio-cultural shift, key C) · PYQ-J26-MCQ13 (strategic driver, key A)
**Still outstanding from earlier lists:** the FM strays to FM Ch 1, 3, 4 and 5 listed above.

## Back-fill pass — SM half DONE (04-10-2026)

Every item on the SM back-fill lists above is now placed, and the three chapters re-merged clean.
**29 atoms in all**, all of them official MCQs or descriptive questions that earlier passes had
left unplaced:

| Target | Added | Where they went |
| --- | --- | --- |
| **SM Ch 2** (91 → 99) | 8 | `S02.02` determinants analysis · `S02.06` socio-cultural shift · `S02.11` PLC maturity · `S02.12` inbound logistics · `S02.14` threat of new entrants ×2 · `S02.16` experience curve ×2 |
| **SM Ch 3** (77 → 95) | 18 | `S03.03` Mendelow ×3 · `S03.07` marketing types and the product driver ×4 · `S03.10` core-competency areas · `S03.11` SWOT · **`S03.14` Porter's generic strategies ×9** |
| **SM Ch 4** (83 → 86) | 3 | `S04.09` strategic alliance ×2 · `S04.12` market development |

**Two headings confirmed in the process.** The **experience curve** is `S02.16` (§2.5.3), which is
where `PYQ-S24-MCQ11` and `RTP-M25-SMCQ5` now sit — both had been held back pending that
confirmation. And **determinants analysis** is `S02.02`: it appears in the *Framework of Strategic
Analysis* figure in SM Chapter 2 under Internal Analysis, not in SM Chapter 3, which is why
`PYQ-J25-MCQ16` reads like a Chapter 3 question and is not one.

**The marketing-strategy types live in SM Ch 3, not Ch 2.** Social, augmented, direct,
relationship, services, enlightened, differential and synchro marketing are all printed under
§3.3.3 Product/Services, as part of the **strategic drivers**. Four back-filled atoms sit there.
`RTP-M24-SMCQ1-ii` is the subtle one: its stem asks how a firm counters innovation risk, which
reads as SM Ch 2's technological environment, but the keyed option — "introducing value-added
services like telemedicine and wellness programs" — is ICAI's own definition of **augmented
marketing**, so the atom is filed at `S03.07`.

**`S03.14` is now the most MCQ-tested heading in SM Chapter 3** with 32 atoms, nine of them added
here. Learn the five answers it rotates between: cost leadership, differentiation, focused cost
leadership, focused differentiation and best-cost provider. The best-cost provider items are the
most reliable marks in the paper, because each is decided by spotting **both** limbs — a low cost
position *and* an upscale product — in the stem.

**One case scenario, four chapters.** RTP September 2024's MuseoGoa case has five parts, and they
are answered on Mendelow's matrix (Ch 3), cost leadership (Ch 3), market development (Ch 4), the
7S Model (Ch 5) and strategic partnerships (Ch 4). That spread is why three earlier passes missed
parts of it, and it is worth remembering when reading any ICAI case scenario: read each part on
its own facts rather than carrying the previous answer forward.

**Still outstanding: the FM half of the back-fill** — 15 items to FM Ch 1, 3, 4 and 5, listed in
the two FM sections above.

## Back-fill pass — FM half, explicit lists DONE (04-10-2026)

Every item on the two FM back-fill lists above is now placed. Most had already been cleared during
the chapter builds themselves — the lists were written early and never pruned — so only **eight
atoms** were genuinely outstanding:

| Target | Added | What |
| --- | --- | --- |
| **FM Ch 3** (34 → 41) | 7 | `PYQ-J25-MCQ6` and `MCQ7` (VP Ltd. Case Scenario II) · `MTP-S26-S2-FMCQ1` to `FMCQ5`, the whole Solstice Biotech Ltd. ratio case |
| **FM Ch 4** (31 → 32) | 1 | `MTP-J26-S2-FQ4b`, the meaning and significance of cost of capital |

**`sources/coverage.py` was fixed, and the fix matters.** The script scans SA, RTP and MTP files
for FM question parts, but RTP files (and some MTP question papers) carry the **suggested answers
in the same file**, and the script was scanning those too. That produced phantom "unplaced" parts
whose stem was a bare number or a stray phrase — `(a) 9.12%`, `(a) Gordon's formula`,
`(b) Other Shareholders' funds - 15%` — and buried the real gaps in noise. The patch cuts each FM
span at the suggested-answers heading and drops any remaining answer-shaped fragment. The unplaced
count fell from **196 to 50**, of which roughly 30 are real.

**A second blind spot, now documented:** `coverage.py` deliberately skips **Part I**, because an
MCQ's (a) to (d) would otherwise look like question sub-parts. That means **FM Part-I MCQs are
invisible to it** — which is exactly how `PYQ-J25-MCQ6`/`MCQ7` and the five Solstice items went
unnoticed. Any future audit of FM MCQ coverage has to read the Part I sections directly, the same
way SA MCQ stems have to be read directly because `sa_smcq.py` does not cover SA-S24.

## Back-fill residual — the real FM gaps found by the fixed coverage.py (04-10-2026)

These are genuine FM question parts that no chapter has placed. This is the remaining scope of the
back-fill task:

**FM Ch 1** — RTP-M26-FQ9b (the treasury department's evolving importance)
**FM Ch 2** — MTP-J25-S2-FQ4c (Drop-Lock Bonds) · MTP-M24-S2-FQ3b (financial instruments in the
international market) · MTP-M25-S1-FQ3b (Millenial Ltd., a Q-commerce startup's financing need) ·
MTP-S25-S1-FQ4c and its OR (an instrument giving fixed periodic returns; sources of long-term
funds) · MTP-S25-S2-FQ4c-OR (sale and leaseback) · RTP-M25-FQ9b (methods of venture capital
financing) · RTP-S26-FQ9b (Global Infra Ltd. raising funds from international markets)
**FM Ch 3** — MTP-S24-S1-FQ2a (Gurunath Ltd.) · RTP-S25-FQ4a/4b and RTP-S26-FQ4a/4b (operating
expenses and a balance sheet from ratios) · RTP-S26-FQ2b and FQ3a (ROCE; creditors turnover)
**FM Ch 4** — MTP-M26-S1-FQ1b (CAPM, a set of securities) · MTP-S26-S2-FQ2b (comparing the cost of
equity of two competitors on beta) · RTP-J25-FQ9b (four methods for computing the cost of equity) ·
RTP-S25-FQ5a/5b/5c (raising additional finance; post-tax cost of debt; cost of retained earnings
and equity) · the Solstice Part-I MCQs 7 and 8
**FM Ch 5** — MTP-S25-S1-FQ3b and RTP-M26-FQ6a/6b and RTP-S24-FQ7a/7b (the MM two-company
problem) · MTP-S25-S2-FQ3b (the process for analysing optimal capital structure) ·
MTP-S25-S2-FQ4c (practical factors for a debt-free company raising Rs 10 crore)
**FM Ch 6** — MTP-M24-S1-FQ1a (Xee Ltd.) · MTP-S25-S2-FQ2a (ABC Engineering's risk-return profile)
**FM Ch 7** — RTP-J25-FQ9c (do the profitability index and NPV give the same accept-reject
decision?) · RTP-M26-FQ9c (the IRR acceptance rule) · the Solstice Part-I MCQ 6
**FM Ch 8** — MTP-S24-S1-FQ5b (QB Ltd., Gordon) · MTP-S24-S2-FQ1b (Mr. Anand's share with a bonus)
**FM Ch 9** — RTP-S25-FQ9b (trade credit against bank overdraft) · RTP-S25-FQ9c (ABC Ltd.'s rapid
sales growth) · RTP-S26-FQ9c (Sunrise Healthcare's rising receivables) · RTP-S26-FQ7c (factors in
planning the working capital requirement)
**Needs a chapter decision** — MTP-J25-S1-FQ2c (Vyom Limited taking over Aryayash Limited, a
two-year-old startup: the valuation basis has to be read before it can be placed)

Known false positives still in the coverage output, for the record, so they are not chased again:
RTP-J25-FQ9a/9b and RTP-M24-FQ7a/7b and MTP-M26-S1-FQ3a/3b/3c are **sub-conditions inside one
question** (credit terms, ageing bands, stock and debtor assumptions), not separate parts;
MTP-S24-S1-FQ5a and RTP-J26-FQ5c are answer fragments.

## Front matter — DONE (04-10-2026)

`book/front.json` now carries six sections. The two review-build sections are unchanged; four are new.

**1. Where the Marks Actually Are — Chapter Weightage.** ICAI publishes no chapter weightage for
Paper 6, so this is **counted, not estimated**: every lettered part and Part-I MCQ from the seven
past papers (May 2024 to May 2026) mapped to the chapter its *published answer* belongs to, with
the marks added up. Two bar charts and two tables. The headline figures, which are reproducible
from the atom files:

| | FM | SM |
| --- | --- | --- |
| Past-paper marks over 7 papers | 356 | 410 |
| Atoms mapped | 327 | 462 |
| Heaviest chapter | **FM 9 Working Capital — 73 marks, 20.5%** | **SM 2 External Environment — 91 marks, 22.2%** |
| Lightest chapter | FM 5 Capital Structure — 24 marks, 6.7% | SM 3 Internal Environment — 72 marks, 17.6% |
| Spread | 6.7% to 20.5% — concentrated | 17.6% to 22.2% — flat |

Two findings worth carrying into the back matter: **FM 9, FM 4 and FM 7 are 48% of Section A on
three chapters**, and **SM has no light chapter**, which is why selective study fails there. The
totals exceed 50 marks per section because both limbs of an OR question are counted; the chart
states that caveat.

**2. Whole-Paper Trends.** Four trends, each stated so a reader can check it: the paper is built
from repeats (a table of the six most-repeated questions with their appearance counts); the stem is
designed to mislead and the published answer decides (six worked examples of the eleven
chapter-changing questions); FM is computational and SM is not; and the four places where ICAI's
own material disagrees with itself, with what to write in each case.

**3. Changes to Watch.** The eleven `update_sensitive` topic blocks, split into rate- and
rule-dependent content to verify against your edition (six, all in FM 7, 8 and 9) and syllabus
areas the examiner is still developing (four, led by SM 5's digital transformation). Closes with
what the book does not do.

**4. Diagnostic Test.** Eighteen MCQs, one or two per chapter, each labelled with its chapter so a
wrong answer points at where to start. Questions printed without answers, then an answer table with
a one-line reason for each, then a "reading your result" box with three score bands and the note
that a section imbalance matters more than the total. The questions are deliberately drawn from the
concepts the examiner reuses.

**Content inventory at this point:** 186 topic blocks · 608 MCQs · 437 official question entries ·
121 expected questions · 252 chapter-test items · 30 integrated cases · 38 Confusing Concepts
tables · 808 official atoms · 8 back-matter appendices.
tables · 789 official atoms.

## Back matter — DONE (04-10-2026)

`book/back.json`, eight parts. Each part renders as a HEADING_1 section, so each appears in the
static TOC and in the PDF bookmark panel alongside the chapters.

| Appendix | Content | Size |
| --- | --- | --- |
| A | Cross-Chapter Integrated Cases — Mahanadi Ceramics Ltd. (FM, five chapters) and Nilgiri Organics Ltd. (SM, all five) | 1 section, 8 blocks |
| B | Mock Exam 1 — full 100-mark paper plus answers and marking | 2 sections, 53 blocks |
| C | Mock Exam 2 — full 100-mark paper plus answers and marking | 2 sections, 51 blocks |
| D | Study Plans — 90-day, 45-day and 20-day plans, the last seven days, and what to cut when behind | 1 section, 14 blocks |
| E | The Mistake Book — nine failure patterns, then 70 curated chapter-by-chapter mistakes | 2 sections, 14 blocks |
| F | The 24-Hour Book — the six-hour last-day sequence, the FM formula sheet, twelve discriminators, nineteen SM frameworks, the exam-day minute plan | 1 section, 26 blocks |
| G | Master Question Index — all 789 official atoms by paper, with chapter and ICAI heading | 3 sections, 23 tables |
| H | Coverage Dashboard — the 14 × 8 chapter/sitting grid and the per-chapter atom counts | 1 section, 9 blocks |

**The mock papers follow ICAI's verified pattern** for Sep 2024 to May 2026: Part I is 30 marks of
MCQs (15 FM + 15 SM, each section being one five-MCQ case scenario plus two 2-mark and one 1-mark
independent MCQ); Part II is 70 marks descriptive, with Q1 and Q5 compulsory at 15 marks (5+5+5)
and any two of Q2–Q4 and any two of Q6–Q8 at 10 marks each. FM Q4 is theory in both mocks, which is
what the papers in the period reviewed do without exception.

**Every figure in both mock answer keys was computed independently in Python before the answer was
written**, including the two case scenarios (Tungabhadra Alloys: DOL 2.40, DCL 3.20, ROE 28.13%;
Kaveri Spinners: Ke 16%, Kp 11.43%, Kd 7.29%, WACC 13.68% on market weights and 12.08% on book
weights) and every descriptive part (NPV ₹11,81,800 and PI 1.394; WACC 11.55%; net working capital
₹11,68,750; EPS indifference ₹36,00,000; Walter ₹116.67/₹108.33/₹100.00; IRR 15.24%; Baumol
₹1,00,000 with 25 conversions and ₹10,000 total cost; cash-discount saving ₹10,000; Gordon
₹100/₹133.33; three-plan EPS ₹8.40/₹11.67/₹14.70; cash budget closings ₹24,000/₹31,000/₹16,000).

**The two mocks are complementary, not duplicative.** Mock 1 covers ratio analysis, cost of capital,
capital structure, leverage, capital budgeting, Walter and working-capital estimation on the FM
side, and value chain, core competence, five forces, diversification, 7S, turnaround, alliances and
GE on the SM side. Mock 2 deliberately takes the chapters Mock 1 left alone: market-value WACC, EOQ,
receivables, IRR, reverse leverage, cash budget, Baumol, cash discount, Gordon, three-plan EPS,
venture capital and factoring on the FM side; and PLC, Ansoff, formulation versus implementation,
PESTLE, competitive landscape, culture, strategic leadership, performance measures and stability on
the SM side. Between them the two papers touch all fourteen chapters.

**Every register reference in the back matter was looked up in `sources/register.json` rather than
written from memory.** Nine were wrong on the first pass and were corrected — the PLC is §2.4.1 not
§2.3.3, PESTLE is §2.3.3, formulation-versus-implementation is §5.2.4 not §5.2.6, Walter and Gordon
both sit under §8.2 Dividend's Relevance Theory, the Baumol model is §11.1 under §10.6, and the
factoring/bill-discounting comparison is §27.8 with bill discounting itself at §27.6.

### A renderer bug found and fixed while building this

`renderCase` in `book/build_fmsm_book.js` read only `q.answer` (a string) plus `q.reasoning[]`, and
`c.trap`. Twenty case answers written as `q.a[]` and eight `c.takeaway` fields were therefore being
**silently dropped from the printed book** — every answer in the SM Ch 4 and SM Ch 5 integrated
cases, and the takeaway of all four SM chapters' cases. The renderer now normalises both shapes
(`{answer, reasoning[]}` and `{a[]}`, where `a[0]` is the verdict) and prints `takeaway` under its
own label. Verified by scanning the rebuilt docx for answer text that previously had a zero count.

All 35 tables in `back.json` were also rescaled so their column widths sum to the content width of
9906 DXA; Word scales a table whose `columnWidths` disagree with its declared width, which was
distorting the wider tables.

## Back-fill residual — CLEARED (04-10-2026)

`python3 sources/coverage.py` now reports **placed 203 · unplaced 0** on the FM side. Getting there
took two separate pieces of work, and they are worth separating because only one of them was about
the book.

### 1. Nineteen genuine gaps, each read from the source before it was placed

Every item on the residual list was traced to its stem **and its published answer** before a chapter
was chosen. Four of the chapter guesses carried forward on the old list turned out to be wrong, so
reading the answer was not a formality:

| Atom | What it actually is | Guessed | Placed |
| --- | --- | --- | --- |
| `RTP-S26-FQ10b` | Global Infra Ltd. — the foreign bonds available to an Indian borrower | FM 2 | FM 2 §9, full entry |
| `MTP-M24-S2-FQ3b` | NAME the financial instruments of the international market | FM 2 | FM 2 §9, also-asked-as |
| `MTP-J25-S2-FQ4c` | drop lock bonds | FM 2 | FM 2 §3.5, full entry |
| `MTP-S25-S1-FQ4c` | identify the hybrid instrument — preference shares | FM 2 | FM 2 §3.2, full entry |
| `MTP-S25-S1-FQ4c-OR` | sources of long-term funds, supplier credit among them | FM 2 | FM 2 §2.2, full entry (block had no official question before) |
| `MTP-S25-S2-FQ4c-OR` | sale and leaseback — benefits and risks | FM 2 | FM 2 §6.2, also-asked-as |
| `RTP-J25-FQ11b` | four methods of computing the cost of equity | FM 4 | FM 4 §7, full entry |
| `MTP-M26-S1-FQ1b` | Mr. Raman's CAPM table (Rf 8%, Rm 14%, C Ltd 14.6%) | FM 4 | FM 4 §7.5, full entry |
| `MTP-S25-S1-FQ3b` | A Ltd / B Ltd under MM, with and without 40% tax | FM 5 | FM 5 §2.4, also-asked-as |
| `MTP-S25-S2-FQ2b` | Excellent Automation Ltd. — probable share price, loan ₹20.64 against equity ₹24.40 | **FM 5 (process for optimal capital structure)** | FM 5 §5, full entry |
| `MTP-S25-S2-FQ4c` | a debt-free company raising ₹10 crore — practical factors | FM 5 | FM 5 §3.2, full entry (block had no official question before) |
| `MTP-S26-S2-FQ2b` | Sunrise Foods Ltd. — EPS ₹27.42, DOL 1.20, DFL 1.06, DCL 1.28 | **FM 4** | FM 6 §5, full entry |
| `RTP-J25-FQ11c` | do PI and NPV give the same decision, and when do they conflict | FM 7 | FM 7 §9.2, full entry |
| `RTP-M26-FQ10c` | the IRR acceptance rule | FM 7 | FM 7 §9.3, also-asked-as |
| `MTP-M25-S1-FQ3b` | Millenial Ltd. — new against second-hand e-vehicles, NPV ₹16,60,441 | **FM 2** | FM 7 §9.1, also-asked-as |
| `MTP-S24-S2-FQ1b` | Mr. Anand's share with a 1:5 bonus — NPV ₹36.14 | FM 8 | FM 7 §9.1, full entry |
| `MTP-J25-S1-FQ2c` | Vyom Ltd. valuing Aryayash Ltd. — fair value ₹200.28 lakh | **undecided** | FM 7 §9.1, full entry |
| `MTP-M24-S1-FQ1a` | Xee Ltd. — Walter run backwards, payout 57.13% for a price of ₹120 | **FM 6** | FM 8 §8.2, full entry |
| `MTP-S24-S1-FQ2a` | Gurunath Ltd. — credit policy evaluation | **FM 3** | FM 9 §19, full entry |

Thirteen became full `official_questions` entries with a worked answer; six became `also_asked_as`
notes on the entry that already covers the ground. **Every figure quoted in the thirteen worked
answers was checked against ICAI's published answer**, which caught two of my own arithmetic slips
in the Vyom entry (the six-year discount factor product, and the 8%-growth stress test).

Two mislabelled ids were also corrected, which removed a duplicate id across two chapters:
`MTP-S25-S2-FQ2b` in FM 6 was really that paper's **Q2(a)** (ABC Engineering Ltd., DOL 1.67 → 1.57),
and `MTP-S25-S2-FQ4b` in FM 5 was really its **Q3(b)** (the optimal capital structure process) — the
genuine Q4(b) is FM 2's crowd funding against peer-to-peer lending.

All seven touched chapters re-merge with **ERRORS: none** and their MCQ keys still balanced:
FM 2 36/36, FM 4 34/34, FM 5 39/39, FM 6 34/34, FM 7 40/40, FM 8 39/39, FM 9 52/52.
Atom totals: FM 346, SM 462, **808** in all (up from 789).

### 2. Two real defects in `sources/coverage.py`, which produced most of the old list

Of the 38 items on the residual list, **19 were not gaps at all** — they were the script mis-reading
the papers. Both causes are now fixed in the script rather than worked around:

**(a) The Miscellaneous question head was invisible.** RTPs print their theory question as
`10.  (a) DISCUSS ...`, with the number and the first sub-part on one line. `QH` requires the number
alone on its line, so that head was never found and **every one of its sub-parts was attributed to
the question before it** — which is why the list showed `RTP-M26-FQ9b` for a part that is really
Q10(b), and `RTP-J25-FQ9b/9c` for parts that are really Q11(b) and Q11(c). Fixed by splitting the
number and the sub-part onto separate lines before scanning. The index in Appendix G now carries the
correct `FQ10a/b/c` and `FQ11a/b/c` labels.

**(b) A numbered condition inside a question was read as a question head.** MTP-S24-S1's Gurunath
Ltd. question carries five numbered conditions, and its `5.` was taken for Question 5 — pushing the
QB Ltd. part that follows out to `MTP-S24-S1-FQ5b`, a question number that paper does not have.
Fixed with a per-source cap: every MTP in this bank has exactly Q1–Q4 on the FM side, so a candidate
head above 4 is not one. (A sequence rule was tried first and rejected — one missed head shifts
every number after it, and it broke MTP-J25-S1.)

**(c) Sub-parts of whole-question atoms are now counted as covered.** Past-paper and RTP atoms are
deliberately recorded at question level (`RTP-S25-FQ4`, not `FQ4a` and `FQ4b`) because ICAI's own
answer treats those questions as one. The script now resolves a sub-part to its parent and marks it
`†`, which accounts for 21 of the 203 placed rows — `RTP-S25-FQ4a/4b`, `RTP-S26-FQ2b/FQ3a/FQ4a/4b`,
`RTP-S25-FQ5a/5b/5c`, `RTP-S24-FQ7a/7b`, `RTP-M26-FQ6a/6b` and the rest of the old false positives.

The upshot: the FM coverage figure went **196 → 50 → 31 → 0** across three passes, and only 19 of
those were ever missing content. The other 177 were tooling.
