---
name: polish-business-writing
description: Use when writing, rewriting or reviewing a Polish document for a CFO, board, chief accountant or other business reader - an ERP concept or pre-implementation analysis (koncepcja wdrożenia, analiza przedwdrożeniowa), a functional comparison of systems, a "today vs. new system" walkthrough with screenshots, or any finance and accounting text about Odoo or another ERP - and when the Polish reads unnatural, calqued from English, full of ticket numbers, internal IDs, time stamps or agent jargon.
license: MIT
metadata:
  author: philipgierszal
  compatibility: Requires Git and Python 3.10+ only for repository checks; the guidance itself needs no runtime. Reading the live ERP user interface (for exact screen labels) is optional but recommended.
---

# Polish Business Writing

Write Polish that a CFO or chief accountant reads as if a senior implementation consultant wrote it: accounting terms from the Accounting Act, short sentences, one claim per sentence, every claim backed by a screenshot, a document link or a number. The reader decides; the document makes the decision easy.

This skill only guides writing. It never changes the systems it describes.

## When to use

- A document for a finance reader: CFO, board, chief accountant, accounting office, auditor.
- A functional proof ("can the new system do everything the old one does?"), a pre-implementation analysis, a system comparison or a step-by-step process description with screenshots.
- A review of Polish text that sounds machine-made: English calques, raw UI labels, internal codes, status jargon.

Not for: code comments, commit messages, internal engineering notes, legal opinions.

## Workflow

1. **Name the reader and the decision.** One sentence at the top of your notes: who reads, what they must decide or approve, by when. Everything that does not serve that decision goes to an appendix or out.
2. **Pick the template.** For a functional proof or ERP concept use [the CFO document template](references/templates.md). For a comparison use its comparison table pattern.
3. **Collect evidence before prose.** For each chapter: what the old system does today (from discovery notes or interviews), the new system's menu path and screens, the official documentation URL, and the screenshot list. Read exact screen labels from the live UI in the reader's language; never guess a translation.
4. **Write in accounting language, quote the screen.** Describe the operation in the accountant's term and give the screen label once in quotes. Use [the terminology table](references/terminology.md).
5. **Strip the workshop.** Remove every ticket number, requirement ID, person ID, role code, branch, server or environment name, build state, and per-sentence date. Keep them in a hidden source map (appendix or a separate file), not in the reader's text.
6. **Run the checklist below** on the whole text, then read it aloud once. Rewrite any sentence you would not say to the CFO across a table.

## Style checklist

Structure
- [ ] The first page answers: what this is, what works, what is missing, what we need you to decide. At most five bullets plus a decision list.
- [ ] Each chapter follows: today in the old system → how the new system does it (numbered steps, screenshots) → what remains to be set or decided → documentation link.
- [ ] One paragraph, one idea. One numbered step, one action by one person or by the system.
- [ ] Headings say the content ("Zamknięcie miesiąca: rozliczenia międzyokresowe i blokada okresu"), not the form ("Sekcja 7").

Wording
- [ ] Accounting terms follow the Accounting Act and practice: zakładowy plan kont, konto syntetyczne i analityczne, zapis księgowy, polecenie księgowania, przeksięgowanie, rozliczenia międzyokresowe, wycena rozchodu, koszt wytworzenia, zamknięcie ksiąg.
- [ ] No English calques: "workflow", "flow", "feature", "drill-down", "dedykowany", "adresować", "implementować", "na ten moment", "zrobić sens", "w oparciu o" (prefer "na podstawie"). See [the calque list](references/terminology.md#kalki-i-zamienniki).
- [ ] Odoo's "konto analityczne" is never left bare: write "MPK", "projekt" or "wymiar analityczny", because in Polish accounting a "konto analityczne" is a ledger sub-account.
- [ ] Active voice, a named actor: "Księgowa zatwierdza fakturę", not "Faktura jest zatwierdzana".
- [ ] Abbreviations: only official symbols (VAT, KSeF, JPK_V7M, JPK_KR_PD, CIT-8, NIP, MPK after first full form) and system names. Spell out document names: "faktura korygująca", not "FK".
- [ ] Numbers with a (non-breaking) space for thousands and a comma for decimals: 1 234 567,89 zł. Pick one percent style ("4%" or "4 %") and keep it through the document.

Status and dates
- [ ] One date for the whole document, on the title page, in words: "Stan na 21 listopada 2026 r." Dates inside the text only where the date is the fact (a deadline, a legal change, a cut-over day).
- [ ] Status in plain words from a fixed set: "działa", "skonfigurowane, uruchomimy 1 stycznia 2027 r.", "w przygotowaniu", "do decyzji", "poza Odoo". Never engineering states ("napisane, niesprawdzone", "zainstalowane na gałęzi").
- [ ] No ticket numbers, requirement IDs, person IDs, role codes, module technical names, environment or server names in the body. A module may appear once in an appendix for IT.

User interface
- [ ] Menu path with the arrow "▸" (or "→") and screen labels in Polish quotes exactly as on screen: Księgowość ▸ Raportowanie ▸ „Bilans".
- [ ] Buttons: przycisk „Zaksięguj"; fields: pole „Data księgowania"; tabs: zakładka „Pozycje faktury". Quote the label, then say what it does in accounting terms.
- [ ] If the UI label is English or a poor translation, quote it once with the accounting meaning: raport „Profit and Loss" (rachunek zysków i strat). Do not repeat the odd label afterwards.

Evidence
- [ ] Every screenshot has a caption "Rysunek n. <what it shows and what to look at>", a crop on the relevant area, and real or clearly marked sample data.
- [ ] Every claim about the system links to the official documentation for the version in use, or to a screenshot. Unknowns are said plainly: "Tego jeszcze nie sprawdziliśmy" beats a vague hedge.
- [ ] External facts (law, deadlines, thresholds) cite the primary source: the Act's article, the Ministry of Finance page.

Typography (Polish)
- [ ] Quotes „…" (inner «…»), dash " – " (półpauza) between words, no English quotes "…" in prose.
- [ ] Month names lower-case; "r." after a year in prose ("w 2027 r.").
- [ ] No title-case headings: "Plan kont i konta segmentowe", not "Plan Kont I Konta Segmentowe".

## References

- [CFO document template and comparison patterns](references/templates.md)
- [Terminology: Odoo screen labels vs. accounting terms, calques](references/terminology.md)
- [Before and after examples](references/examples.md)
- [Sources and how they were used](references/sources.md)
