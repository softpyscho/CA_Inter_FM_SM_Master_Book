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
| SM Chapter 2 written and merged | Done — `book/Ch11.json` (24/24 headings, 91/91 atoms placed) |
| SM Chapter 3 written and merged | Done — `book/Ch12.json` (14/14 headings, 77/77 atoms placed) |

## Chapter numbering used in the book

`Ch01`–`Ch09` = FM chapters 1–9; `Ch10`–`Ch14` = SM chapters 1–5.
Topic codes: `F01.07.01` prints as "FM Ch 1 §7.1"; `S01.05.02` prints as "SM Ch 1 §1.5.2".

## Next steps (updated 04-10-2026)

1. SM Ch 4–5 (15 and 18 register headings) -> `book/Ch13.json` and `book/Ch14.json`.
2. Back-fill pass: the stray official questions listed at the end of this file (FM Ch 1, 3, 4, 5;
   SM Ch 3, 4, 5), then re-run `sources/coverage.py`.
3. Full front matter: chapter weightage chart from the mark counts, whole-paper trends,
   "changes to watch", diagnostic test.
4. Back matter: cross-chapter cases, two mock exams, study plans, mistake book, 24-hour book,
   master question index, PYQ/RTP/MTP matrix, dashboard.
5. Rebuild with `./make_pdf.ps1` (two passes so the index page numbers settle).

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
