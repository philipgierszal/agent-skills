# Templates

Patterns drawn from Polish pre-implementation analyses and functional comparisons (see [sources](sources.md)): the document fixes the scope, describes each process "as is / to be" with evidence, and ends with decisions and risks so the reader can say go, no-go or change the scope. Partner material for Odoo shows each accounting feature as a menu path, a short sequence of screenshots and a link to the official documentation.

## 1. CFO functional-proof document

Use when the question is "can the new system do everything the old one does, for our company?"

```
Tytuł: <Obszar> w <nowy system> – co dziś robi <stary system> i jak zrobimy to w <nowy system>
Podtytuł: dokument dla dyrektora finansowego
Stan na <dzień miesiąc rok> r. · poufne, zawiera dane finansowe (jeśli tak)

1. Najważniejsze w skrócie                         (1 strona)
   - Co działa już dziś (3–5 punktów, liczby).
   - Czego jeszcze brakuje i kiedy będzie.
   - Decyzje, których potrzebujemy od Pana/Pani (lista numerowana, każda z terminem).

2. Jak czytać dokument                              (pół strony)
   - Słowniczek statusów: działa / skonfigurowane, uruchomimy <data> / w przygotowaniu / do decyzji / poza systemem.
   - Skąd zrzuty ekranu (system produkcyjny albo testowy, dane rzeczywiste albo przykładowe).

3..N. Rozdział na każdy obszar
   N.1 Dziś w <stary system>
       Kto, co, jakim dokumentem, jak często; konta; znane problemy.
   N.2 W <nowy system>
       Ścieżka w menu, potem kroki:
       1. <Rola> <czynność> – przycisk „…”.  [Rysunek N.1]
       2. System <co robi sam>, np. tworzy zapis Wn 501 / Ma 201.  [Rysunek N.2]
       Wynik: <jaki dokument, raport albo zapis powstaje>.
   N.3 Co trzeba ustawić albo zdecydować
       Punkty z właścicielem decyzji, bez numerów zgłoszeń.
   N.4 Dokumentacja
       Odnośnik do oficjalnej dokumentacji wersji, której używamy.
   Status rozdziału: jedno słowo ze słowniczka.

N+1. Decyzje do podjęcia        (tabela: decyzja | warianty | rekomendacja | termin)
N+2. Ryzyka                     (tabela: ryzyko | skutek | jak ograniczamy | kto pilnuje)
N+3. Słowniczek                 (termin z ekranu ↔ termin księgowy)
Załącznik dla IT: moduły, mapa źródeł, numery zgłoszeń – poza tekstem dla czytelnika.
Źródła: ustawa, strony Ministerstwa Finansów, dokumentacja systemu, notatki z analizy.
```

Rules for the chapters:

- Start each chapter with the old system, in the reader's own vocabulary (the account numbers and document names the accountants use today). The reader trusts the new part only after recognising the old one.
- Show the result as an accounting entry when it matters: "Wn 640 / Ma 501" says more to a chief accountant than a paragraph.
- One screenshot per step, cropped, with the relevant field or button marked. Caption says what to look at, not just what the screen is.
- If the new system needs an add-on or a manual step, say so in the same chapter; do not hide it in the risks table.

## 2. Functional comparison table

```
| Funkcja | <System A>, jak go mamy | <System B> | Kto to robi |
```

- Rows are business functions in accounting language (odbiór faktur zakupu, obieg akceptacji, płatności i biała lista, JPK), not module names.
- Every cell that states a capability links to a source: documentation, vendor page, screenshot. "Niepotwierdzone" when no source was found.
- Put the recommendation in a separate section after the table, with the models or variants spelled out ("Model 1: …, Model 2: …").

## 3. Screenshot list (for the person who takes them)

```
| Rysunek | Rozdział | Ekran (ścieżka w menu) | Co pokazać | Dane | Środowisko |
```

- Prefer production for reports already in use; use the test environment for anything that changes data (posting, closing, revaluation).
- Read-only on production: open, filter, export. Never post, lock or reverse there to make a screenshot.
- Same zoom, same language (Polish UI), same user role as the reader would have.

## 4. Status vocabulary for readers

| Write | Instead of |
|---|---|
| działa | sprawdzone na produkcji |
| skonfigurowane, uruchomimy 1 stycznia 2027 r. | zainstalowane, włączane 2027-01-01 |
| sprawdzone na systemie testowym | sprawdzone na staging-1 |
| w przygotowaniu | napisane, niesprawdzone / kod na gałęzi |
| nie zaczęte | niezbudowane |
| do decyzji (kto) | decyzja, czeka na właściciela |
