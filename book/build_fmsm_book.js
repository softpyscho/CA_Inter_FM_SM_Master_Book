/*
 * build_fmsm_book.js  —  CA Inter Paper 6 Financial Management & Strategic Management : WHOLE-BOOK DOCX Builder
 * -------------------------------------------------------------------------------
 * Usage:   node build_fmsm_book.js <book_dir> <output.docx>
 *          book_dir contains:  book.json (meta)  front.json (optional)  Ch01.json ... ChNN.json  back.json (optional)
 *          Chapters are included in file-name order; a missing chapter is shown as "NOT YET BUILT".
 *          TOC depth: HW_TOC_LEVELS=2 (default, chapters+sections) or 3 (adds concepts)
 * Fonts:   HW_HEAD_FONT="Ink Free" HW_BODY_FONT="Segoe Print" node build_fmsm_book.js book out.docx
 *          (defaults are Windows 10/11 built-in handwriting fonts; every font is set through
 *           Word Styles, so the student can change the whole book's font in one click)
 * Markup inside any text string:
 *          **bold keyword**   ==highlighted phrase==   __wavy-underlined exam trap__
 * Requires: npm package "docx" (docx-js).
 * Design rule: every box = a single-cell table with coloured fill + thick left border +
 *          an icon AND a text label (so meaning survives black-and-white printing).
 */
const fs = require('fs');
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, WidthType, ShadingType,
  BorderStyle, HeadingLevel, AlignmentType, TableOfContents, Footer, Header, PageNumber,
  LevelFormat, UnderlineType, PageBreak, Tab, TabStopType, LeaderType,
} = require('docx');

// ---------------------------------------------------------------- design tokens
const FONT_HEAD = process.env.HW_HEAD_FONT || 'Ink Free';
const FONT_BODY = process.env.HW_BODY_FONT || 'Segoe Print';
const FONT_EMOJI = 'Segoe UI Emoji';
const FONT_SYMBOL = 'Segoe UI Symbol';
const FONT_RUPEE = 'Segoe UI';
const INK = '1F2937';
const BLUE_INK = '1E3A8A';
const PAGE_W = 11906, PAGE_H = 16838, MARGIN = 1000;   // A4, ~0.7" margins
const CW = PAGE_W - 2 * MARGIN;                         // 9906 content width
const CELL_PAD = 160;
const INNER = CW - 2 * CELL_PAD;                        // width available inside a box

const TAGS = {
  snapshot:  { icon: '📘', label: 'CHAPTER SNAPSHOT',        fill: 'FFFBEB', border: 'B45309' },
  concept:   { icon: '🟦', label: 'UNDERSTAND IT',           fill: 'DBEAFE', border: '2563EB' },
  keyword:   { icon: '🟨', label: 'ICAI KEYWORDS',           fill: 'FEF9C3', border: 'CA8A04' },
  alert:     { icon: '🟥', label: 'EXAM ALERT',              fill: 'FEE2E2', border: 'DC2626' },
  memory:    { icon: '🟩', label: 'MEMORY TRICK',            fill: 'DCFCE7', border: '16A34A' },
  pyq:       { icon: '🟪', label: 'OFFICIAL ICAI QUESTION',  fill: 'EDE9FE', border: '7C3AED' },
  mistake:   { icon: '🟧', label: 'COMMON MISTAKE / CONFUSION', fill: 'FFEDD5', border: 'EA580C' },
  quick:     { icon: '⬜', label: 'QUICK RECAP',             fill: 'F3F4F6', border: '6B7280' },
  provision: { icon: '⚖️', label: 'KEY FRAMEWORK / FORMULA',    fill: 'E0F2FE', border: '0369A1' },
  amendment: { icon: '🔄', label: 'AMENDMENT / UPDATE',      fill: 'FCE7F3', border: 'DB2777' },
  face:      { icon: '🧭', label: 'HOW TO FACE IT IN THE EXAM', fill: 'CCFBF1', border: '0F766E' },
  write:     { icon: '✍️', label: 'WRITE THIS IN THE EXAM',  fill: 'ECFCCB', border: '65A30D' },
  avoid:     { icon: '🚫', label: "DON'T WRITE THIS",        fill: 'FEF2F2', border: '991B1B' },
  expected:  { icon: '🔮', label: 'EXPECTED QUESTION',       fill: 'E0E7FF', border: '4338CA' },
  mcq:       { icon: '☑️', label: 'MCQ',                     fill: 'F8FAFC', border: '334155' },
  casebox:   { icon: '🧪', label: 'CASE SCENARIO',           fill: 'FEF3C7', border: 'D97706' },
  link:      { icon: '🔗', label: 'INTEGRATION LINK',        fill: 'F0FDFA', border: '14B8A6' },
  verify:    { icon: '🛡️', label: 'VERIFICATION',            fill: 'F1F5F9', border: '475569' },
  mockq:     { icon: '📝', label: 'QUESTION',                fill: 'F8FAFC', border: '1E3A8A' },
  solution:  { icon: '📗', label: 'SUGGESTED ANSWER',        fill: 'F0FDF4', border: '15803D' },
};
const STATUS_ICON = { VERIFIED: '✅', PARTIAL: '🔶', UNVERIFIED: '❓', 'NOT AVAILABLE': '⛔' };
const ACTIVITY = {
  High: '🟥 High Exam Activity', Medium: '🟨 Medium Exam Activity',
  Foundation: '🟦 Conceptual Foundation', Low: '⬜ Low Exam Activity',
};

// ---------------------------------------------------------------- text helpers
const arr = (x) => (Array.isArray(x) ? x : x == null || x === '' ? [] : [x]);
const s = (x) => (x == null ? '' : String(x));

// ---------------------------------------------------------------- reader-facing wording
// Internal IDs (PYQ-M25-Q4a, MTP-M26-S1-SQ2a, F01.07.01 …) stay in the JSON for tracking;
// the printed book shows readable names ("PYQ May 2025 · Q4(a)", "FM Ch 1 §7.1").
const MON = { M: 'May', S: 'Sep', J: 'Jan' };
const ROMAN = { 1: 'I', 2: 'II' };
let CONCEPT_INDEX = {};
// Question-part codes (Paper 6 has an FM section and an SM section):
//   MCQ9 · Q4a · Q4c-OR ........ past papers (Q1-Q4 = FM, Q5-Q8 = SM)
//   FQ12a · SQ7 · FQ8-i · SQ4b-OR  RTP / MTP descriptive, FM or SM section
//   SMCQ2 · SMCQ1-iv .......... RTP SM MCQs;  SMCQ-A-i · SMCQ-B-iii  MTP SM Part I
const PART_RE = '(?:[FS]?MCQ\\d+(?:-[ivx]+)?|Q\\d[a-e]?(?:-OR)?|[FS]Q\\d+[a-e]?(?:-[ivx]+)?(?:-OR)?|SMCQ-[AB]-[ivx]+)';
function partName(p) {
  let m;
  if ((m = p.match(/^MCQ(\d+)$/))) return `MCQ ${m[1]}`;
  if ((m = p.match(/^FMCQ(\d+)$/))) return `FM MCQ ${m[1]}`;
  if ((m = p.match(/^Q(\d)([a-e])?(-OR)?$/))) return `Q${m[1]}${m[2] ? `(${m[2]})` : ''}${m[3] ? ' (OR)' : ''}`;
  if ((m = p.match(/^([FS])Q(\d+)([a-e])?(?:-([ivx]+))?(-OR)?$/))) return `${m[1] === 'F' ? 'FM' : 'SM'} Q${m[2]}${m[3] ? `(${m[3]})` : ''}${m[4] ? `(${m[4]})` : ''}${m[5] ? ' (OR)' : ''}`;
  if ((m = p.match(/^SMCQ(\d+)(?:-([ivx]+))?$/))) return `SM MCQ ${m[1]}${m[2] ? `(${m[2]})` : ''}`;
  if ((m = p.match(/^SMCQ-([AB])-([ivx]+)$/))) return `SM MCQ 1(${m[1]})(${m[2]})`;
  return p;
}
function sourceName(id) {
  const m = s(id).match(new RegExp(`^(PYQ|RTP|MTP)-([MSJ])(\\d\\d)(?:-S([12]))?-(${PART_RE})$`));
  if (!m) return '';
  return `${m[1]} ${MON[m[2]]} 20${m[3]}${m[4] ? ` Series ${ROMAN[m[4]]}` : ''} · ${partName(m[5])}`;
}
function conceptRef(code) {
  const x = CONCEPT_INDEX[code];
  const sec = code[0] === 'F' ? 'FM' : 'SM';
  const ch = Number(code.slice(1, 3));
  return x ? `${sec} Ch ${ch} ${x.ref}` : `${sec} Ch ${ch}`;
}
function humanize(t) {
  t = s(t);
  t = t.replace(/\s*\[(?:PARAPHRASED|AI-GENERATED|OFFICIAL)[^\]]*\]/g, '');
  t = t.replace(/\[SECONDARY[^\]]*?—\s*([^,\]]+)(?:,[^\]]*)?\]/g, '($1)').replace(/\s*\[U\d\]/g, '');
  t = t.replace(/\(placed under ([^)]*)\)/g, '(see $1)');
  t = t.replace(/\bCASE-[FS]\d\d-INT-(\d+)/g, 'Integrated Case $1');
  t = t.replace(new RegExp(`\\b(PYQ|RTP|MTP)-([MSJ])(\\d\\d)(?:-S([12]))?-(${PART_RE})(?![\\w-])`, 'g'),
    (_, k, mo, yy, se, p) => `${k} ${MON[mo]} 20${yy}${se ? ` Series ${ROMAN[se]}` : ''} · ${partName(p)}`);
  t = t.replace(/(^|[\s(,;/])([MSJ])(2[4-7])-S([12])\b/g, (_, pre, mo, yy, se) => `${pre}${MON[mo]} 20${yy} Series ${ROMAN[se]}`);
  t = t.replace(/(^|[\s(,;/])([MSJ])(2[4-7])(?=[\s),;/]|$)/g, (_, pre, mo, yy) => `${pre}${MON[mo]} 20${yy}`);
  t = t.replace(/\b[FS]\d\d\.\d\d(?:\.\d\d)?\b/g, (code) => conceptRef(code));
  t = t.replace(/[✅🔶❓⛔]️?/gu, '').replace(/[ \t]{2,}/g, ' ');
  return t;
}
// internal repeat classes → plain words
// R1 near-identical repeat · R2 same topic, new wording · R3 same topic as a case · R4 combines topics · R5 first time · R topic seen before
function repeatText(r) {
  r = s(r).trim();
  if (!r || r === '—') return 'First time asked';
  const m = r.match(/^R(\d)?\s*(?:\(([^)]*)\)|(?:with|of)\s+(.*))?$/);
  if (!m) return humanize(r);
  const ref = m[2] || m[3] || '';
  const base = { 1: 'Repeat', 2: 'Same topic, new wording', 3: 'Same topic as a case', 4: 'Combines topics', 5: 'First time asked' }[m[1]] || 'Topic asked before';
  if (m[1] === '5' || /first appearance|case form/.test(ref)) return base;
  if (m[1] === '4') return ref ? `Combines ${humanize(ref.replace(/^combines\s*/i, '').replace(/(\d+(?:\.\d+)?)/g, '§$1'))}` : base;
  return ref ? `${base} — ${humanize(ref)}` : base;
}

function runs(text, base = {}) {
  text = humanize(text);
  const out = [];
  const re = /(\*\*[^*\s][^*]*?\*\*|==[^=\s][^=]*?==|__[^_\s][^_]*?__)/g;
  let last = 0, m;
  // v2 font fix (student request): handwriting fonts lack emoji, ₹, arrows, ticks, maths signs.
  // Every such character — wherever it sits — gets its own run in a font that has the glyph.
  const push = (t, extra = {}) => {
    if (!t) return;
    t = t.replace(/️/g, '');
    const parts = t.split(/(\p{Extended_Pictographic}+|[⬜✅⛔❓☑✔✗✘⏱➜→←↔⇒≈≥≤≠×½§₹]+)/u);
    for (const part of parts) {
      if (!part) continue;
      let font;
      if (/\p{Extended_Pictographic}|[⬜✅⛔❓☑]/u.test(part)) font = FONT_EMOJI;
      else if (/[✔✗✘⏱➜→←↔⇒≈≥≤≠×½§]/u.test(part)) font = FONT_SYMBOL;
      else if (/₹/u.test(part)) font = FONT_RUPEE;
      out.push(new TextRun({ ...base, ...extra, text: part, ...(font ? { font } : {}) }));
    }
  };
  while ((m = re.exec(text))) {
    push(text.slice(last, m.index));
    const tok = m[0], inner = tok.slice(2, -2);
    if (tok.startsWith('**')) push(inner, { bold: true, color: BLUE_INK });
    else if (tok.startsWith('==')) push(inner, { bold: true, shading: { type: ShadingType.CLEAR, color: 'auto', fill: 'FDE047' } });
    else push(inner, { underline: { type: UnderlineType.WAVE, color: 'DC2626' } });
    last = m.index + tok.length;
  }
  push(text.slice(last));
  return out;
}
const P = (text, run = {}, para = {}) =>
  new Paragraph({ children: runs(text, run), spacing: { after: 70, line: 290 }, ...para });
const B = (text, level = 0) =>
  new Paragraph({ children: runs(text), numbering: { reference: 'hw-bullets', level }, spacing: { after: 40, line: 280 } });
const LBL = (label, text, color = BLUE_INK) =>
  new Paragraph({ spacing: { after: 50, line: 280 }, children: [...runs(label + ' ', { bold: true, color, font: FONT_HEAD, size: 22 }), ...runs(text)] });
const SP = (after = 120) => new Paragraph({ children: [], spacing: { after } });
// headings are collected (when COLLECT is set) to build the printed index pages
let COLLECT = null;
const H_LEVEL = { [HeadingLevel.HEADING_1]: 1, [HeadingLevel.HEADING_2]: 2, [HeadingLevel.HEADING_3]: 3, [HeadingLevel.HEADING_4]: 4 };
const H = (level, text) => {
  if (COLLECT) COLLECT.push({ level: H_LEVEL[level] || 4, text: s(text) });
  return new Paragraph({ heading: level, children: runs(text) });
};
const PB = () => new Paragraph({ children: [new PageBreak()] });

function answerDivider(label = '✔ ANSWER') {
  return new Paragraph({
    spacing: { before: 100, after: 60 },
    border: { top: { style: BorderStyle.DASHED, size: 6, color: '94A3B8', space: 6 } },
    children: runs(label, { bold: true, font: FONT_HEAD, size: 22, color: '15803D' }),
  });
}

// ---------------------------------------------------------------- box + grid
function box(tagKey, title, children, width = CW) {
  const t = TAGS[tagKey] || TAGS.quick;
  const thin = { style: BorderStyle.SINGLE, size: 4, color: t.border };
  return [
    new Table({
      width: { size: width, type: WidthType.DXA },
      columnWidths: [width],
      rows: [new TableRow({
        cantSplit: false,
        children: [new TableCell({
          width: { size: width, type: WidthType.DXA },
          shading: { fill: t.fill, type: ShadingType.CLEAR, color: 'auto' },
          margins: { top: 90, bottom: 90, left: CELL_PAD, right: CELL_PAD },
          borders: { top: thin, bottom: thin, right: thin, left: { style: BorderStyle.SINGLE, size: 30, color: t.border } },
          children: [
            new Paragraph({
              spacing: { after: 60 },
              children: [
                new TextRun({ text: t.icon.replace(/️/g, '') + ' ', font: FONT_EMOJI, size: 22 }),
                new TextRun({ text: t.label, font: FONT_HEAD, bold: true, size: 24, color: t.border }),
                ...(title ? [new TextRun({ text: '  ·  ', color: t.border, size: 22 }), ...runs(title, { font: FONT_HEAD, size: 22, bold: true, color: INK })] : []),
              ],
            }),
            ...children.filter(Boolean),
          ],
        })],
      })],
    }),
    SP(110),
  ];
}

function grid(headers, rows, total = CW, widths, headFill = 'FDE68A') {
  const n = headers.length;
  if (!n) return [];
  if (!widths) { const w = Math.floor(total / n); widths = Array(n).fill(w); widths[n - 1] += total - w * n; }
  const border = { style: BorderStyle.SINGLE, size: 4, color: '9CA3AF' };
  const borders = { top: border, bottom: border, left: border, right: border };
  const cell = (txt, i, head) => new TableCell({
    width: { size: widths[i], type: WidthType.DXA },
    borders,
    shading: head ? { fill: headFill, type: ShadingType.CLEAR, color: 'auto' } : { fill: 'FFFFFF', type: ShadingType.CLEAR, color: 'auto' },
    margins: { top: 50, bottom: 50, left: 90, right: 90 },
    children: arr(txt).length ? arr(txt).map((x) => P(x, head ? { bold: true, font: FONT_HEAD, size: 21 } : { size: 19 }, { spacing: { after: 30, line: 260 } })) : [P('')],
  });
  return [
    new Table({
      width: { size: total, type: WidthType.DXA },
      columnWidths: widths,
      rows: [
        new TableRow({ tableHeader: true, children: headers.map((h, i) => cell(h, i, true)) }),
        ...rows.map((r) => new TableRow({ children: headers.map((_, i) => cell(r[i], i, false)) })),
      ],
    }),
    SP(110),
  ];
}

const statusTxt = () => '';   // status marks are kept in the registry only, not printed

// horizontal bar chart drawn with table cells (stays editable, prints in colour or grey)
function barChart(b) {
  const labelW = 2600, valW = 800, barW = CW - labelW - valW;
  const none = { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' };
  const nob = { top: none, bottom: none, left: none, right: none };
  const max = b.max || Math.max(...arr(b.series).flatMap((sr) => arr(sr.values)), 1);
  const rows = [];
  arr(b.labels).forEach((lab, i) => {
    arr(b.series).forEach((sr, j) => {
      const v = Number(sr.values[i]) || 0;
      const w = Math.max(60, Math.round((barW - 40) * v / max));
      const bar = new Table({
        width: { size: barW - 40, type: WidthType.DXA }, columnWidths: [w, Math.max(40, barW - 40 - w)],
        rows: [new TableRow({ children: [
          new TableCell({ width: { size: w, type: WidthType.DXA }, borders: nob, shading: { fill: v ? sr.color : 'FFFFFF', type: ShadingType.CLEAR, color: 'auto' }, children: [new Paragraph({ spacing: { after: 0, line: 200 }, children: [new TextRun({ text: ' ', size: 14 })] })] }),
          new TableCell({ width: { size: Math.max(40, barW - 40 - w), type: WidthType.DXA }, borders: nob, children: [new Paragraph({ spacing: { after: 0, line: 200 }, children: [new TextRun({ text: ' ', size: 14 })] })] }),
        ] })],
      });
      const nS = arr(b.series).length;
      rows.push(new TableRow({ children: [
        ...(j === 0 ? [new TableCell({ width: { size: labelW, type: WidthType.DXA }, rowSpan: nS, verticalAlign: 'center', borders: { ...nob, top: i ? { style: BorderStyle.DOTTED, size: 4, color: 'D1D5DB' } : none }, margins: { top: 10, bottom: 10, left: 60, right: 60 }, children: [P(lab, { size: 18, bold: true }, { spacing: { after: 0, line: 230 } })] })] : []),
        new TableCell({ width: { size: barW, type: WidthType.DXA }, borders: nob, margins: { top: 20, bottom: 20, left: 20, right: 20 }, children: [bar] }),
        new TableCell({ width: { size: valW, type: WidthType.DXA }, borders: nob, margins: { top: 10, bottom: 10, left: 60, right: 20 }, children: [P(`${v}${b.unit || ''}`, { size: 17, color: sr.color }, { spacing: { after: 0, line: 230 } })] }),
      ] }));
    });
  });
  const legend = new Paragraph({ spacing: { after: 80 }, children: arr(b.series).flatMap((sr) => [
    new TextRun({ text: '■ ', font: FONT_SYMBOL, color: sr.color, size: 22 }), new TextRun({ text: `${sr.name}     `, size: 19 })]) });
  return [
    ...(b.title ? [P(b.title, { bold: true, font: FONT_HEAD, size: 24, color: '1D4ED8' }, { spacing: { after: 40 } })] : []),
    legend,
    new Table({ width: { size: CW, type: WidthType.DXA }, columnWidths: [labelW, barW, valW], rows }),
    ...(b.note ? [P(b.note, { italics: true, size: 17, color: '6B7280' })] : []),
    SP(140),
  ];
}

// ---------------------------------------------------------------- question renderers
function renderDescriptive(q, tagKey) {
  const src = sourceName(q.id);
  const form = src ? '' : s(q.form).replace(/\s*\(\d+\s*marks?\)/i, '');
  const head = [q.label || src || (tagKey === 'pyq' ? '' : 'Practice question'), form, q.marks ? `${q.marks} marks` : ''].filter(Boolean).join('  ·  ');
  return box(tagKey, head, [
    P(q.question, { bold: true }),
    ...(q.hint ? [LBL('Hint:', q.hint, '0F766E')] : []),
    answerDivider('✔ MODEL ANSWER'),
    ...(q.provision ? [LBL('Provision:', q.provision)] : []),
    ...arr(q.answer_points).map((x) => B(x)),
    ...(q.facts_analysis ? [LBL('Facts & analysis:', q.facts_analysis)] : []),
    ...(q.conclusion ? [LBL('Conclusion:', q.conclusion, '15803D')] : []),
    ...(arr(q.keywords).length ? [LBL('🔑 Keywords:', arr(q.keywords).map((k) => `==${k}==`).join('  ·  '))] : []),
    ...(q.marks_split ? [LBL('Marks split:', q.marks_split, '6B21A8')] : []),
    ...(q.mistake ? [LBL('🟧 Common mistake:', q.mistake, 'C2410C')] : []),
    ...(q.also_asked_as ? [LBL('🔁 Also asked as:', arr(q.also_asked_as).join(' | '), '4338CA')] : []),
    ...(q.examiner ? [LBL('📜 What ICAI examiners said:', q.examiner, 'B91C1C')] : []),
    ...(arr(q.topics).length ? [LBL('🗺 Topics tested:', arr(q.topics).join(', '), '475569')] : []),
  ]);
}

function renderMCQ(m, withAnswer = true, title) {
  const src = sourceName(m.id);
  const head = title || [src || 'Practice MCQ', src ? '' : m.angle, src ? '' : m.difficulty].filter(Boolean).join('  ·  ');
  const opts = m.options || {};
  const body = [
    P(m.question, { bold: true }),
    ...['A', 'B', 'C', 'D'].filter((k) => opts[k] != null).map((k) => P(`(${k})  ${opts[k]}`, {}, { indent: { left: 240 }, spacing: { after: 30, line: 270 } })),
  ];
  if (withAnswer) {
    body.push(answerDivider(`✔ ANSWER: (${s(m.answer)})`));
    if (m.explanation) body.push(P(m.explanation));
    const ww = m.why_wrong || {};
    Object.keys(ww).forEach((k) => body.push(B(`(${k}) ✗ ${ww[k]}`)));
    if (m.trap) body.push(LBL('🪤 Trap:', m.trap, 'C2410C'));
    if (m.concept) body.push(LBL('Topic:', m.concept, '475569'));
  }
  return box('mcq', head, body);
}

function renderCase(c, withAnswers = true) {
  const body = [
    ...arr(c.facts).map((f) => P(f)),
    new Paragraph({ spacing: { before: 80, after: 40 }, children: [new TextRun({ text: 'Questions', bold: true, font: FONT_HEAD, size: 23, color: 'B45309' })] }),
  ];
  arr(c.questions).forEach((q, i) => {
    body.push(P(`Q${(c.start || 1) + i}. ${s(q.q)}${q.marks ? `  [${q.marks} marks]` : ''}`, { bold: true }));
    const o = q.options || {};
    ['A', 'B', 'C', 'D'].filter((k) => o[k] != null).forEach((k) => body.push(P(`(${k})  ${o[k]}`, {}, { indent: { left: 240 }, spacing: { after: 20 } })));
  });
  if (withAnswers) {
    body.push(answerDivider('✔ ANSWERS'));
    arr(c.questions).forEach((q, i) => {
      // Two shapes are in use: {answer, reasoning[]} and {a[]}, where a[0] is the
      // verdict and the rest are the working. Normalise so neither is dropped.
      const lines = q.answer != null ? [s(q.answer), ...arr(q.reasoning)] : arr(q.a).map(s);
      body.push(LBL(`Q${(c.start || 1) + i}:`, lines[0] || '', '15803D'));
      lines.slice(1).forEach((r) => body.push(B(r)));
    });
    if (arr(c.concepts).length) body.push(LBL('🗺 Topics tested:', arr(c.concepts).join(', '), '475569'));
    if (c.trap) body.push(LBL('🪤 Trap:', c.trap, 'C2410C'));
    if (c.takeaway) body.push(LBL('🎯 Takeaway:', c.takeaway, '15803D'));
  }
  return box('casebox', c.title || '', body);
}

// ---------------------------------------------------------------- section renderers
function renderGeneric(sec) {
  const out = [];
  if (sec.heading) out.push(H(sec.level === 3 ? HeadingLevel.HEADING_3 : HeadingLevel.HEADING_2, sec.heading));
  arr(sec.blocks).forEach((b) => {
    if (b.type === 'para') out.push(P(b.text));
    else if (b.type === 'bullets') arr(b.items).forEach((x) => out.push(B(x)));
    else if (b.type === 'table') out.push(...grid(b.headers || [], b.rows || [], CW, b.widths));
    else if (b.type === 'box') out.push(...box(b.tag, b.title, [...arr(b.paras).map((x) => P(x)), ...arr(b.bullets).map((x) => B(x))]));
    else if (b.type === 'pagebreak') out.push(PB());
    else if (b.type === 'h3') out.push(H(HeadingLevel.HEADING_3, b.text));
    else if (b.type === 'barchart') out.push(...barChart(b));
    else if (b.type === 'mcq') out.push(...renderMCQ(b, b.with_answer !== false, b.label));
    else if (b.type === 'case') out.push(...renderCase(b, b.with_answer !== false));
    else if (b.type === 'question') out.push(...(b.with_answer === false
      ? box(b.tag || 'expected', [b.label || sourceName(b.id) || 'Practice question', b.marks ? `${b.marks} marks` : ''].filter(Boolean).join('  ·  '), [P(b.question, { bold: true })])
      : renderDescriptive(b, b.tag || 'expected')));
  });
  return out;
}

function renderSnapshot(sn) {
  if (!sn) return [];
  const body = [];
  if (sn.about) body.push(LBL('What it is about:', sn.about));
  if (sn.why) body.push(LBL('Why it matters:', sn.why));
  const list = (label, items) => { if (arr(items).length) { body.push(LBL(label, '')); arr(items).forEach((x) => body.push(B(typeof x === 'string' ? x : `${x.text}${x.evidence ? `  — evidence: ${x.evidence}` : ''}`))); } };
  list('Core concepts:', sn.core_concepts);
  list('Key provisions / standards:', sn.key_provisions);
  list('Most tested areas (evidence-based):', sn.tested_areas);
  list('Top student mistakes:', sn.mistakes);
  list('Integration links:', sn.links);
  if (sn.revision_path) body.push(LBL('⏱ Revision path:', sn.revision_path, '0F766E'));
  return [H(HeadingLevel.HEADING_2, 'Chapter Snapshot'), ...box('snapshot', null, body)];
}

function renderEvidence(ev) {
  if (!ev) return [];
  const out = [H(HeadingLevel.HEADING_2, 'What ICAI Has Actually Tested')];
  if (arr(ev.pyq_table).length) {
    out.push(...grid(['Paper & question', 'What was asked', 'Topic', 'Marks', 'Type', 'Topic asked before?'],
      ev.pyq_table.map((r) => [sourceName(r.id) || r.id, r.question, r.concept, s(r.marks), r.type, repeatText(r.repeat)]),
      CW, [1900, 3100, 1100, 700, 1400, 1706]));
  }
  if (arr(ev.trend).length) out.push(...box('alert', 'Trends in ICAI questions', arr(ev.trend).map((x) => B(x))));
  if (arr(ev.rtp_takeaways).length) out.push(...box('pyq', 'RTP takeaways', arr(ev.rtp_takeaways).map((x) => B(x))));
  if (arr(ev.mtp_takeaways).length) out.push(...box('pyq', 'MTP takeaways', arr(ev.mtp_takeaways).map((x) => B(x))));
  if (ev.note) out.push(P(ev.note, { italics: true, size: 18, color: '6B7280' }));
  return out;
}

function renderConcept(c) {
  const out = [];
  out.push(H(HeadingLevel.HEADING_3, s(c.title)));
  const chips = [ACTIVITY[c.activity] || '', c.update_sensitive ? '🔄 Watch for updates' : '', c.multi_source ? '🎯 Asked across PYQ / RTP / MTP' : '', c.evidence && /[1-9]/.test(c.evidence) ? `Asked: ${c.evidence}` : ''].filter(Boolean).join('   |   ');
  if (chips) out.push(P(chips, { size: 18, color: '475569' }, { spacing: { after: 90 } }));

  if (arr(c.understand).length || c.example) {
    out.push(...box('concept', null, [...arr(c.understand).map((x) => P(x)), ...(c.example ? [LBL('e.g.', c.example, '1D4ED8')] : [])]));
  }
  arr(c.amendments).forEach((a) => out.push(...box('amendment', a.title, [P(a.text), ...(a.effective ? [LBL('Effective for:', a.effective)] : []), ...(a.status ? [P(statusTxt(a.status), { size: 18 })] : [])])));
  arr(c.provisions).forEach((p) => out.push(...box('provision', [p.ref, statusTxt(p.status)].filter(Boolean).join('  '), [
    ...(p.requirement ? [LBL('Requirement:', p.requirement)] : []),
    ...(p.applies_when ? [LBL('Applies when:', p.applies_when)] : []),
    ...(p.responsibility ? [LBL('Responsibility of:', p.responsibility)] : []),
    ...(p.exceptions ? [LBL('Exceptions / conditions:', p.exceptions)] : []),
    ...(p.consequence ? [LBL('Documentation / reporting consequence:', p.consequence)] : []),
    ...(p.exam_angle ? [LBL('Exam angle:', p.exam_angle, 'B91C1C')] : []),
  ])));
  if (arr(c.keywords).length) out.push(...box('keyword', null, [P(arr(c.keywords).map((k) => `==${k}==`).join('  ·  '))]));
  if (c.memory && (c.memory.trick || arr(c.memory.key).length)) {
    const mb = [];
    if (c.memory.trick) mb.push(P(c.memory.trick, { bold: true }));
    if (arr(c.memory.key).length) mb.push(...grid(['Cue', 'Stands for'], c.memory.key, INNER, [1600, INNER - 1600], 'BBF7D0'));
    if (c.memory.recall_trigger) mb.push(LBL('⚡ 3-second trigger:', c.memory.recall_trigger, '15803D'));
    out.push(...box('memory', null, mb));
  }
  if (arr(c.mistakes).length || c.compare) {
    const mb = arr(c.mistakes).map((x) => B(x));
    if (c.compare) {
      mb.push(...grid(c.compare.headers || [], c.compare.rows || [], INNER, null, 'FED7AA'));
      if (c.compare.spot_it) mb.push(LBL('🧪 Spot it in a case:', c.compare.spot_it, 'B45309'));
    }
    out.push(...box('mistake', null, mb));
  }
  arr(c.links).forEach((l) => out.push(...box('link', null, [P(l)])));
  arr(c.enrichment).forEach((e) => out.push(...box(e.tag || 'concept', `${s(e.title)}${e.author ? ` (${e.author})` : ''}`, arr(e.bullets).map((x) => B(x)))));
  if (c.face_in_exam) {
    const f = c.face_in_exam, fb = [];
    if (arr(f.forms).length) { fb.push(LBL('Can be asked as:', '')); arr(f.forms).forEach((x) => fb.push(B(x))); }
    if (arr(f.approach).length) { fb.push(LBL('How to attack it:', '')); arr(f.approach).forEach((x) => fb.push(B(x))); }
    if (f.official_pattern) fb.push(LBL('📜 What ICAI has done so far:', f.official_pattern, '6B21A8'));
    if (f.time_tip) fb.push(LBL('⏱ Time / length guide (study guidance):', f.time_tip, '0F766E'));
    out.push(...box('face', null, fb));
  }
  if (c.write) {
    const w = c.write, wb = [];
    if (arr(w.structure).length) { wb.push(LBL('Structure:', '')); arr(w.structure).forEach((x) => wb.push(B(x))); }
    if (arr(w.keywords).length) wb.push(LBL('🔑 Keywords:', arr(w.keywords).map((k) => `==${k}==`).join('  ·  ')));
    if (w.length) wb.push(LBL('📏 Ideal length:', w.length));
    if (w.conclusion) wb.push(LBL('🏁 Conclusion pattern:', w.conclusion, '15803D'));
    out.push(...box('write', null, wb));
    if (arr(w.avoid).length) out.push(...box('avoid', null, arr(w.avoid).map((x) => B(x))));
  }

  const hasQ = arr(c.official_questions).length || arr(c.expected_questions).length || arr(c.mcqs).length || c.mini_case;
  if (hasQ) {
    out.push(H(HeadingLevel.HEADING_4, '📚 Questions on this topic — ICAI questions first, then practice'));
    arr(c.official_questions).forEach((q) => out.push(...renderDescriptive(q, 'pyq')));
    arr(c.expected_questions).forEach((q) => out.push(...renderDescriptive(q, 'expected')));
    arr(c.mcqs).forEach((m) => out.push(...renderMCQ(m, true)));
    if (c.mini_case) out.push(...renderCase(c.mini_case, true));
  }
  if (arr(c.recap).length) out.push(...box('quick', null, arr(c.recap).map((x) => B(x))));
  return out;
}

function renderRecall(r) {
  if (!r) return { q: [], a: [] };
  const q = [H(HeadingLevel.HEADING_2, 'Active-Recall Tests (answers in Answer Keys)')];
  const a = [H(HeadingLevel.HEADING_3, 'Active-recall answers')];
  const sec = (title, items, qf, af) => {
    if (!arr(items).length) return;
    q.push(H(HeadingLevel.HEADING_3, title)); a.push(P(title, { bold: true, font: FONT_HEAD, size: 23, color: 'B45309' }));
    arr(items).forEach((it, i) => { q.push(P(`${i + 1}. ${qf(it)}`)); a.push(P(`${i + 1}. ${af(it)}`)); });
  };
  sec('10 Quick Questions', r.quick, (x) => x.q, (x) => x.a);
  sec('Fill in the Blanks', r.fill, (x) => x.q, (x) => x.a);
  sec('True / False', r.true_false, (x) => x.s, (x) => `${x.a} — ${s(x.reason)}`);
  sec('One-Word Recall', r.one_word, (x) => x.q, (x) => x.a);
  if (r.match && arr(r.match.left).length) {
    q.push(H(HeadingLevel.HEADING_3, 'Match the Concept'));
    const n = Math.max(r.match.left.length, arr(r.match.right).length);
    q.push(...grid(['Column A', 'Column B'], Array.from({ length: n }, (_, i) => [`${i + 1}. ${s(r.match.left[i])}`, `${String.fromCharCode(97 + i)}. ${s(arr(r.match.right)[i])}`])));
    a.push(P('Match the Concept', { bold: true, font: FONT_HEAD, size: 23, color: 'B45309' }), P(arr(r.match.key).join('   ')));
  }
  sec('Differentiate', r.differentiate, (x) => x.q, (x) => x.a);
  if (r.flowchart && arr(r.flowchart.steps).length) {
    q.push(H(HeadingLevel.HEADING_3, 'Complete the Flowchart'));
    q.push(P(r.flowchart.steps.map((st, i) => (arr(r.flowchart.blanks).includes(i) ? '[ ? ]' : st)).join('  ➜  ')));
    a.push(P('Complete the Flowchart', { bold: true, font: FONT_HEAD, size: 23, color: 'B45309' }), P(r.flowchart.steps.join('  ➜  ')));
  }
  return { q, a };
}

function renderOnePage(op) {
  if (!op || !arr(op.sections).length) return [];
  const out = [PB(), H(HeadingLevel.HEADING_2, 'One-Page Chapter Sheet')];
  const secs = op.sections, half = Math.floor(CW / 2);
  const border = { style: BorderStyle.SINGLE, size: 6, color: 'F59E0B' };
  const colCell = (sec) => new TableCell({
    width: { size: half, type: WidthType.DXA },
    borders: { top: border, bottom: border, left: border, right: border },
    shading: { fill: 'FFFBEB', type: ShadingType.CLEAR, color: 'auto' },
    margins: { top: 50, bottom: 50, left: 100, right: 100 },
    children: sec ? [P(sec.title, { bold: true, font: FONT_HEAD, size: 21, color: 'B45309' }, { spacing: { after: 20 } }), ...arr(sec.points).map((x) => P(`• ${x}`, { size: 16 }, { spacing: { after: 10, line: 230 } }))] : [P('')],
  });
  const rows = [];
  for (let i = 0; i < secs.length; i += 2) rows.push(new TableRow({ children: [colCell(secs[i]), colCell(secs[i + 1])] }));
  out.push(new Table({ width: { size: half * 2, type: WidthType.DXA }, columnWidths: [half, half], rows }));
  return out;
}

// ---------------------------------------------------------------- document

// ---------------------------------------------------------------- chapter body (no cover / TOC)
function renderChapterBody(data) {
  const meta = data.meta || {};
  const children = [];
  children.push(
    new Paragraph({ heading: HeadingLevel.HEADING_1, alignment: AlignmentType.CENTER, spacing: { before: 1800, after: 200 }, children: runs(s(meta.chapter_title || 'Chapter')) }),
    P(s(meta.module), { font: FONT_HEAD, size: 28, color: '0F766E' }, { alignment: AlignmentType.CENTER }),
    P(`Based on: ${s(meta.sm_edition)}`, { size: 19 }, { alignment: AlignmentType.CENTER, spacing: { before: 300 } }),
    PB(),
  );
  arr(data.sections_before).forEach((sec) => children.push(...renderGeneric(sec)));
  children.push(...renderSnapshot(data.snapshot));
  children.push(...renderEvidence(data.evidence));
  if (arr(data.concepts).length) {
    children.push(PB(), H(HeadingLevel.HEADING_2, 'Topic-wise Notes with All Related Questions'));
    arr(data.concepts).forEach((c, i) => { if (i) children.push(SP(160)); children.push(...renderConcept(c)); });
  }
  if (arr(data.confusing).length) {
    children.push(PB(), H(HeadingLevel.HEADING_2, 'Most Confusing Concepts'));
    data.confusing.forEach((cf) => {
      children.push(H(HeadingLevel.HEADING_3, cf.title), ...grid(cf.headers || [], cf.rows || [], CW, null, 'FED7AA'));
      if (cf.spot_it) children.push(...box('casebox', 'Spot it in a case', [P(cf.spot_it)]));
    });
  }
  if (arr(data.cases).length) {
    children.push(PB(), H(HeadingLevel.HEADING_2, 'Integrated Case Scenarios'));
    data.cases.forEach((c) => children.push(...renderCase(c, true)));
  }
  const keys = [];
  if (data.chapter_test && (arr(data.chapter_test.mcqs).length || arr(data.chapter_test.descriptive).length)) {
    children.push(PB(), H(HeadingLevel.HEADING_2, 'Chapter Test — attempt before looking at the Answer Keys'));
    arr(data.chapter_test.mcqs).forEach((m, i) => children.push(...renderMCQ(m, false, `Test MCQ ${i + 1}`)));
    arr(data.chapter_test.descriptive).forEach((q, i) => children.push(...box('expected', [`Test question ${i + 1}`, q.marks ? `${q.marks} marks` : ''].filter(Boolean).join('  ·  '), [P(q.question, { bold: true })])));
    keys.push(H(HeadingLevel.HEADING_3, 'Chapter test — MCQ key'));
    if (arr(data.chapter_test.mcqs).length) keys.push(...grid(['MCQ', 'Answer', 'Why'], data.chapter_test.mcqs.map((m, i) => [String(i + 1), s(m.answer), s(m.explanation)]), CW, [1000, 1100, CW - 2100]));
    arr(data.chapter_test.descriptive).forEach((q, i) => keys.push(...box('expected', [`Test question ${i + 1} — model answer`, q.marks ? `${q.marks} marks` : ''].filter(Boolean).join('  ·  '), [
      P(q.question, { bold: true }), answerDivider('✔ MODEL ANSWER'), ...arr(q.answer_points).map((x) => B(x)),
      ...(q.conclusion ? [LBL('Conclusion:', q.conclusion, '15803D')] : []),
      ...(arr(q.keywords).length ? [LBL('🔑 Keywords:', arr(q.keywords).map((k) => `==${k}==`).join('  ·  '))] : [])])));
  }
  const rc = renderRecall(data.recall);
  if (rc.q.length > 1) { children.push(PB(), ...rc.q); keys.push(...rc.a); }
  if (keys.length) children.push(PB(), H(HeadingLevel.HEADING_2, 'Answer Keys'), ...keys);
  if (data.revision) {
    const r = data.revision;
    children.push(PB(), H(HeadingLevel.HEADING_2, 'Rapid Revision Ladder'));
    [['5-MINUTE', r.five], ['15-MINUTE', r.fifteen], ['30-MINUTE', r.thirty], ['60-MINUTE', r.sixty]].forEach(([t, items]) => {
      if (arr(items).length) children.push(...box('quick', `${t} REVISION`, arr(items).map((x) => B(x))));
    });
  }
  children.push(...renderOnePage(data.one_page));
  arr(data.sections_after).forEach((sec) => children.push(...renderGeneric(sec)));
  // data.verification (sources, open checks, QA) is kept in the JSON / registry only — not printed
  return children;
}

// ---------------------------------------------------------------- whole book
function buildBook(dir) {
  const path = require('path');
  const read = (f) => JSON.parse(fs.readFileSync(path.join(dir, f), 'utf8'));
  const exists = (f) => fs.existsSync(path.join(dir, f));
  if (exists('concept_index.json')) CONCEPT_INDEX = read('concept_index.json');
  const book = exists('book.json') ? read('book.json') : {};
  const plan = arr(book.chapter_plan); // [{no, title, file}]
  const chapterFiles = fs.readdirSync(dir).filter((f) => /^Ch\d+.*\.json$/i.test(f)).sort();
  const hf = (txt) => [new Paragraph({ alignment: AlignmentType.RIGHT, children: [new TextRun({ text: txt, font: FONT_HEAD, size: 18, color: '9CA3AF' })] })];
  const footer = new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: 'Page ', font: FONT_HEAD, size: 18, color: '9CA3AF' }), new TextRun({ children: [PageNumber.CURRENT], font: FONT_HEAD, size: 18, color: '9CA3AF' })] })] });
  const pageProps = { page: { size: { width: PAGE_W, height: PAGE_H }, margin: { top: MARGIN, bottom: MARGIN, left: MARGIN, right: MARGIN } } };
  const sec = (headerTxt, children) => ({ properties: pageProps, headers: { default: new Header({ children: hf(headerTxt) }) }, footers: { default: footer }, children });
  const title = s(book.title || 'CA Intermediate · Paper 6 · Financial Management & Strategic Management — Master Book');

  // ---- render bodies first so their headings can feed the index pages
  const withCollect = (fn) => { COLLECT = []; const out = fn(); const got = COLLECT; COLLECT = null; return [out, got]; };
  const [frontBody, frontHeads] = withCollect(() => { const o = []; if (exists('front.json')) arr(read('front.json').sections).forEach((x) => o.push(...renderGeneric(x))); return o; });
  const chapterRender = chapterFiles.map((f) => {
    const data = read(f);
    const [body, heads] = withCollect(() => renderChapterBody(data));
    return { data, body, heads: [{ level: 1, text: s((data.meta || {}).chapter_title) }, ...heads] };
  });
  const backRender = exists('back.json') ? arr(read('back.json').parts).map((part) => {
    const [body, heads] = withCollect(() => {
      const kids = [new Paragraph({ heading: HeadingLevel.HEADING_1, children: runs(s(part.title)) })];
      arr(part.sections).forEach((x) => kids.push(...renderGeneric(x)));
      return kids;
    });
    return { part, body, heads: [{ level: 1, text: s(part.title) }, ...heads] };
  }) : [];
  // page numbers from the previous pass (book/page_map.json, written by sources/make_page_map.py)
  const normH = (t) => humanize(s(t)).replace(/\*\*|==|__/g, '').toLowerCase().replace(/[^a-z0-9]/g, '').slice(0, 30);
  const PAGE_MAP = exists('page_map.json') ? read('page_map.json') : [];
  {
    // split the map at each level-1 bookmark and match each chapter/part only inside its own segment
    const segs = []; let cur = { head: null, items: [] }; segs.push(cur);
    PAGE_MAP.forEach((m) => { if (m.level === 1) { cur = { head: m.norm, items: [m] }; segs.push(cur); } else cur.items.push(m); });
    const matchIn = (items, heads) => {
      let ptr = 0; const used = new Set();
      const take = (j, e) => { e.page = items[j].page; used.add(j); ptr = j + 1; return true; };
      heads.forEach((e) => {
        if (e.level > 3) return;
        const n = normH(e.text); e.norm = n;
        for (let j = ptr; j < items.length; j++) if (!used.has(j) && items[j].norm === n && take(j, e)) return;
        // headings created out of document order (e.g. answer-key headings) — first unused match anywhere in the segment
        for (let j = 0; j < items.length; j++) if (!used.has(j) && items[j].norm === n) { e.page = items[j].page; used.add(j); return; }
      });
    };
    const firstChapterSeg = segs.findIndex((g) => g.head && /^(fm|sm)chapter\d/.test(g.head));
    matchIn(segs.slice(0, firstChapterSeg < 0 ? 1 : firstChapterSeg).flatMap((g) => g.items), frontHeads);
    [...chapterRender, ...backRender].forEach((r) => {
      const g = segs.find((x) => x.head === normH(r.heads[0].text));
      if (g) matchIn(g.items, r.heads);
    });
    if (process.env.HW_DEBUG_INDEX) fs.writeFileSync('build/index_debug.json', JSON.stringify([...frontHeads, ...chapterRender.flatMap((c) => c.heads), ...backRender.flatMap((b) => b.heads)], null, 0));
  }
  const cut = (t, n = 100) => { t = humanize(s(t)).replace(/\*\*|==|__/g, ''); return t.length <= n ? t : `${t.slice(0, n).replace(/\s+\S*$/, '')} …`; };
  const IDX = (text, page, { level = 0, bold = false } = {}) => new Paragraph({
    tabStops: [{ type: TabStopType.RIGHT, position: CW - 20, leader: LeaderType.DOT }],
    indent: { left: level * 400 }, spacing: { after: bold ? 30 : 15, before: bold ? 70 : 0, line: 250 },
    children: [...runs(cut(text), { bold, size: 19, ...(bold ? { color: BLUE_INK } : {}) }), new TextRun({ children: [new Tab(), page ? String(page) : '0000'], size: 19, bold })],
  });
  const IDXHEAD = (t) => P(t, { bold: true, font: FONT_HEAD, size: 24, color: '1D4ED8' }, { spacing: { before: 160, after: 60 } });
  const chapterIndex = (heads) => {
    const out = [P('Chapter Index', { font: FONT_HEAD, size: 28, bold: true, color: 'B91C1C' }, { spacing: { after: 60 } }),
      P('Page numbers are printed at the foot of each page. In the PDF, click a line to jump to it.', { italics: true, size: 17, color: '6B7280' })];
    let inTopics = false;
    heads.slice(1).forEach((e) => {
      if (e.level === 2) { inTopics = /^Topic-wise Notes/.test(e.text); out.push(IDX(e.text, e.page, { bold: true })); }
      else if (e.level === 3 && inTopics) out.push(IDX(e.text, e.page, { level: 1 }));
    });
    out.push(PB());
    return out;
  };

  // front
  const front = [
    P('CA INTERMEDIATE · PAPER 6', { font: FONT_HEAD, size: 30, color: '6B7280' }, { alignment: AlignmentType.CENTER, spacing: { before: 1400, after: 200 } }),
    new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 200 }, children: [new TextRun({ text: 'FM & SM', font: FONT_HEAD, size: 80, bold: true, color: 'B91C1C' })] }),
    P('6A Financial Management  ·  6B Strategic Management', { font: FONT_HEAD, size: 32, color: '0F766E' }, { alignment: AlignmentType.CENTER, spacing: { after: 160 } }),
    P('The Master Book', { font: FONT_HEAD, size: 40, color: '1D4ED8' }, { alignment: AlignmentType.CENTER }),
    P('Concept notes · Every official question under its concept · Expected questions · MCQs · Cases · Exam strategy · Revision · Mocks', { size: 20, color: '374151' }, { alignment: AlignmentType.CENTER, spacing: { before: 300 } }),
    P(`Target attempt: ${s(book.attempt)}   ·   Applicable study material: ${s(book.sm_edition)}`, { size: 20 }, { alignment: AlignmentType.CENTER, spacing: { before: 500 } }),
    P('ICAI questions (PYQ, RTP, MTP) are presented in our own words with answers based on ICAI\'s suggested answers; practice questions are written for this book on ICAI topics.', { italics: true, size: 18, color: '6B7280' }, { alignment: AlignmentType.CENTER, spacing: { before: 300 } }),
    PB(),
    H(HeadingLevel.HEADING_2, 'Colour & Symbol Legend'),
    ...grid(['Tag', 'Meaning', 'Tag', 'Meaning'], (() => {
      const k = Object.keys(TAGS).filter((x) => x !== 'verify'), rows = [];
      for (let i = 0; i < k.length; i += 2) rows.push([`${TAGS[k[i]].icon} ${TAGS[k[i]].label}`, LEGEND_TEXT[k[i]] || '', k[i + 1] ? `${TAGS[k[i + 1]].icon} ${TAGS[k[i + 1]].label}` : '', k[i + 1] ? LEGEND_TEXT[k[i + 1]] || '' : '']);
      return rows;
    })(), CW, [2300, 2653, 2300, 2653]),
    P('PYQ = previous ICAI exam paper · RTP = ICAI Revision Test Paper · MTP = ICAI Mock Test Paper · FM Ch 1 §7 = Financial Management Chapter 1, study-material heading 7 · SM Ch 1 §1.5 = Strategic Management Chapter 1, heading 1.5', { size: 18 }),
    P('Markup: **bold** = ICAI keyword · ==highlight== = must-remember phrase · __wavy underline__ = exam trap', { size: 18 }),
    PB(), new Paragraph({ heading: HeadingLevel.HEADING_2, children: runs(process.env.HW_STATIC_TOC ? 'Index' : 'Contents') }),
    ...(process.env.HW_STATIC_TOC
      // PDF build: Word's TOC field update hangs on this document, so write a static list;
      // the PDF bookmark panel (added by sources/add_bookmarks.py) gives clickable navigation.
      ? [
          P('Chapters with their sections, and the front and back matter. Each chapter also opens with its own Chapter Index listing every topic. In the PDF, click a line (or use the Bookmarks panel) to jump to it.', { size: 19 }),
          IDXHEAD('Front matter'),
          ...frontHeads.filter((e) => e.level === 2).map((e) => IDX(e.text, e.page)),
          IDXHEAD('Chapters'),
          ...chapterRender.flatMap((c) => c.heads.filter((e) => e.level <= 2).map((e) => IDX(e.text, e.page, { bold: e.level === 1, level: e.level === 1 ? 0 : 1 }))),
          ...(backRender.length ? [IDXHEAD('Back matter'), ...backRender.flatMap((b) => b.heads.filter((e) => e.level <= 2).map((e) => IDX(e.text, e.page, { bold: e.level === 1, level: e.level === 1 ? 0 : 1 })))] : []),
        ]
      : [
          new TableOfContents('Contents', { hyperlink: true, headingStyleRange: `1-${process.env.HW_TOC_LEVELS || 2}` }),
          P('(If the contents list is empty: right-click it → Update Field → Update entire table. Use View → Navigation Pane to jump to any concept.)', { italics: true, size: 18, color: '6B7280' }),
        ]),
    PB(),
  ];
  front.push(...frontBody);
  const sections = [sec(title, front)];

  // chapters (each opens with its Chapter Index after the cover page)
  chapterRender.forEach(({ data, body, heads }) => {
    const kids = process.env.HW_STATIC_TOC ? [...body.slice(0, 4), ...chapterIndex(heads), ...body.slice(4)] : body;
    sections.push(sec(`FM & SM · ${s((data.meta || {}).short_title || (data.meta || {}).chapter_title)}`, kids));
  });
  // chapters not yet written are simply left out of the printed book

  // back matter
  backRender.forEach(({ part, body }) => sections.push(sec(`FM & SM · ${s(part.title)}`, body)));

  return new Document({
    creator: 'CA Inter FM & SM Master System',
    title,
    features: { updateFields: !process.env.HW_NO_UPDATEFIELDS }, // PDF export sets HW_NO_UPDATEFIELDS to avoid Word's 'update fields?' prompt
    styles: {
      default: { document: { run: { font: FONT_BODY, size: 20, color: INK } } },
      paragraphStyles: [
        { id: 'Heading1', name: 'Heading 1', basedOn: 'Normal', next: 'Normal', quickFormat: true, run: { font: FONT_HEAD, size: 52, bold: true, color: 'B91C1C' }, paragraph: { spacing: { before: 240, after: 200 }, outlineLevel: 0 } },
        { id: 'Heading2', name: 'Heading 2', basedOn: 'Normal', next: 'Normal', quickFormat: true, run: { font: FONT_HEAD, size: 36, bold: true, color: '1D4ED8' }, paragraph: { spacing: { before: 200, after: 140 }, outlineLevel: 1, border: { bottom: { style: BorderStyle.SINGLE, size: 12, color: 'FDE047', space: 2 } } } },
        { id: 'Heading3', name: 'Heading 3', basedOn: 'Normal', next: 'Normal', quickFormat: true, run: { font: FONT_HEAD, size: 30, bold: true, color: '7C2D12' }, paragraph: { spacing: { before: 200, after: 80 }, outlineLevel: 2, shading: { type: ShadingType.CLEAR, color: 'auto', fill: 'FEF3C7' } } },
        { id: 'Heading4', name: 'Heading 4', basedOn: 'Normal', next: 'Normal', quickFormat: true, run: { font: FONT_HEAD, size: 26, bold: true, color: '6B21A8' }, paragraph: { spacing: { before: 160, after: 90 }, outlineLevel: 3 } },
      ],
    },
    numbering: {
      config: [{
        reference: 'hw-bullets',
        levels: [
          { level: 0, format: LevelFormat.BULLET, text: '•', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 400, hanging: 240 } }, run: { color: 'DC2626' } } },
          { level: 1, format: LevelFormat.BULLET, text: '◦', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 800, hanging: 240 } }, run: { color: '2563EB' } } },
        ],
      }],
    },
    sections,
  });
}

const LEGEND_TEXT = {
  snapshot: 'One-page overview of the chapter', concept: 'Plain-language understanding', keyword: 'Words ICAI expects in answers',
  alert: 'Frequently tested / high exam activity', memory: 'Mnemonic or recall trigger', pyq: 'ICAI question — PYQ / RTP / MTP',
  mistake: 'What students get wrong', quick: 'Condensed recap', provision: 'Formula, rule or ICAI framework to apply',
  amendment: 'Changed or newly applicable content', face: 'Forms it is asked in + how to attack', write: 'Answer structure to use',
  avoid: 'Wrong or irrelevant wording', expected: 'Practice question with model answer', mcq: 'Practice MCQ with key',
  casebox: 'Case facts + linked questions', link: 'Connection to another chapter', verify: 'Sources, open checks, QA',
};

if (require.main === module) {
  const [, , dir, outp] = process.argv;
  if (!dir || !outp) { console.error('Usage: node build_fmsm_book.js <book_dir> <output.docx>'); process.exit(1); }
  Packer.toBuffer(buildBook(dir)).then((buf) => { fs.writeFileSync(outp, buf); console.log('Built', outp); });
}
module.exports = { buildBook };



