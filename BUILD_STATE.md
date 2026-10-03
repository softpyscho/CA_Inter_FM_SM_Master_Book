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
| FM Chapters 2–7 written and merged | Done — `book/Ch02.json` to `book/Ch07.json`; see the progress ledger below |

## Chapter numbering used in the book

`Ch01`–`Ch09` = FM chapters 1–9; `Ch10`–`Ch14` = SM chapters 1–5.
Topic codes: `F01.07.01` prints as "FM Ch 1 §7.1"; `S01.05.02` prints as "SM Ch 1 §1.5.2".

## Next steps (updated 03-10-2026)

1. FM Ch 8 Dividend Decision, then FM Ch 9 Management of Working Capital (68 register headings, the
   largest chapter in the paper). After Ch 9, run the back-fill pass listed at the end of this file.
2. SM Ch 2–5.
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

## Back-fill list found while scoping FM Ch 7 (coverage.py, 22-09-2026)
These official questions belong to chapters already merged and were not in their atom files. Add them in a back-fill pass after FM Ch 9:
- MTP-J26-S2-FQ4b (meaning of cost of capital + three reasons it matters) -> FM Ch 4
- MTP-M24-S1-FQ3a (Ram Ltd — rates on bank loan and debentures, PE multiple 4) -> FM Ch 4
- RTP-S26-FQ1 (AURO Engineering Pvt. Ltd. case scenario MCQs) -> FM Ch 4
- MTP-S24-S2-FQ1a (X Ltd — point of indifference, ₹84 lakh) -> FM Ch 5
- MTP-S25-S2-FQ4a (Project X vs Project Y — profit vs wealth maximisation vs value creation) -> FM Ch 1
- MTP-M24-S2-FQ4a and MTP-S26-S2-FQ4a (inter-relationship between investment, financing and dividend decisions) -> FM Ch 1
