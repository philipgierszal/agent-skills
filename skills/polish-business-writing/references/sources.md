# Sources

Read 2026-11-21. Used for patterns and terminology only; no text is copied.

## Law and official pages

- Ustawa z dnia 29 września 1994 r. o rachunkowości, tekst jednolity (ELI): https://eli.gov.pl/api/acts/DU/2021/217/text.html – terms used: zakładowy plan kont (art. 10), dzienniki częściowe (art. 14), konta syntetyczne i analityczne (art. 16–17), zamknięcie ksiąg (art. 12), cena nabycia i koszt wytworzenia (art. 28), wycena walut (art. 30), wycena rozchodu zapasów (art. 34), rozliczenia międzyokresowe (art. 39, 41). Check the current consolidated text before citing an article number; the Act is amended often.
- Krajowy System e-Faktur, Ministerstwo Finansów: https://ksef.podatki.gov.pl/
- Wykaz podatników VAT (biała lista): podatki.gov.pl, search "wykaz podatników VAT"; ustawa o VAT art. 96b.
- Rada Języka Polskiego, zasady pisowni obowiązujące od 1 stycznia 2026 r.: https://rjp.pan.pl/ (komunikat i załącznik „Zasady pisowni"); summary: https://www.gov.pl/web/uw-pomorski/od-1-stycznia-2026-r---ortografia-i-interpunkcja-po-nowemu
- Language advice: https://sjp.pwn.pl/poradnia and https://poradnik-jezykowy.uw.edu.pl (quotation marks „…", lower-case month names, anglicisms).

## Odoo

- Official documentation, version 19.0 (20.0 pages are still being written): https://www.odoo.com/documentation/19.0/applications/finance/accounting.html and https://www.odoo.com/documentation/19.0/applications/finance/fiscal_localizations/poland.html
- Polish UI strings: https://github.com/odoo/odoo/blob/19.0/addons/account/i18n/pl.po

## Implementation practice (patterns only)

- Pre-implementation analysis as the specification and the go / no-go basis; inputs such as the chart of accounts and VAT registers: https://www.benchmark.pl/uchwycic-stan-i-cele-przedsiebiorstwa-7263096794759745a
- Sections of a pre-implementation analysis (functional scope, processes and data, organisation, goals, schedule): https://yadda.icm.edu.pl/baztech/element/bwmeta1.element.baztech-5c131fae-314f-4644-bba9-13e256a18e6a/c/ZNPKosz_2013_5_12.pdf
- Business case and readiness: https://www.ey.com/pl_pl/insights/digital-first/system-erp-co-warto-wiedziec-przed-wdrozeniem
- Risk analysis as part of the analysis: https://itwiz.pl/?p=63707
- Steps of ERP selection and implementation: https://symfonia.pl/blog/finanse-i-ksiegowosc/finanse-miedzynarodowe/siedem-krokow-do-wyboru-najlepszego-dla-twojej-firmy-systemu-erp/

## Limits

- No published Polish template for a CFO functional-proof document was found; the template is a synthesis of the sources above and of in-house comparisons that readers rated well.
- Odoo Polish labels marked "sprawdź w UI" in the terminology table were not found in the translation file under that exact English string; read them on screen.
