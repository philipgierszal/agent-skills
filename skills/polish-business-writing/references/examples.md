# Before and after

The "before" sentences are modelled on a real draft chapter for a CFO about accounting in Odoo. Company names, person codes and figures are replaced; ticket and requirement numbers are kept in shape so the pattern is recognisable. Each pair names the rule it applies.

## Title page and status

**Przed:** Stan na 2026-11-21 (Z-620). Rozdział łączy strony procesów finansowych, rejestr wymagań Odoo i odpowiedzi głównej księgowej z 2026-11-19. Ludzie są podani tylko jako role i identyfikatory os-ID.

**Po:** Stan na 21 listopada 2026 r. Rozdział opisuje, jak dokumenty księgowe przechodzą przez systemy i kto za co odpowiada – dziś w Graffiti i od 1 stycznia 2027 r. w Odoo.

*Reguły:* jedna data słownie; bez numerów zgłoszeń; nie opisuj, z czego dokument powstał – czytelnika obchodzi, co z niego wynika.

**Przed:** Stany budowy: działa (sprawdzone na produkcji); zainstalowane (na produkcji, włączane 2027-01-01); sprawdzone na staging-1; napisane, niesprawdzone (kod na gałęzi, jeszcze nie na staging-1); niezbudowane; decyzja.

**Po:** Przy każdej funkcji podajemy jeden z czterech stanów: działa, uruchomimy 1 stycznia 2027 r., w przygotowaniu albo do decyzji.

*Reguły:* słownik statusów dla czytelnika, nie dla zespołu wdrożeniowego; bez nazw środowisk.

## Summary bullets

**Przed:** Faktury zakupu już dziś wpływają do Odoo z KSeF co 3 godziny (produkcja: 1 200 szkiców rachunków, 20 korekt, 2026-11-19), ale księguje je Graffiti do 2026-12-31.

**Po:** Faktury zakupu już dziś trafiają z KSeF do Odoo – co trzy godziny, w listopadzie około 1 200 faktur i 20 korekt. Do końca roku księgujemy je jednak w Graffiti; w Odoo czekają niezaksięgowane.

*Reguły:* „szkic rachunku" zastąpiony terminem księgowym; dwie myśli, dwa zdania; liczba zaokrąglona, bo to podsumowanie.

**Przed:** Obieg faktury kosztowej (EOD) w Odoo: blokada księgowania do zatwierdzenia (Odoo FR 105) jest zainstalowana na produkcji i włącza się 2027-01-01; opis automatyczny, macierz akceptacji, przypomnienia (Odoo FR 117, FR 118) oraz biała lista i plik dla banku (Odoo FR 104, FR 107) są napisane 2026-11-21, niesprawdzone.

**Po:** Od 1 stycznia 2027 r. faktury kosztowej nie da się zaksięgować, dopóki nie zaakceptuje jej kierownik MPK albo zarząd. W przygotowaniu są: automatyczny opis faktury (konto i MPK), przypomnienia o akceptacji, sprawdzanie rachunku dostawcy na białej liście przed zapłatą oraz plik przelewów dla banku.

*Reguły:* skutek dla czytelnika na początku; bez numerów wymagań; lista zamiast zdania ze średnikami; „napisane, niesprawdzone" → „w przygotowaniu".

**Przed:** Bank: 9 dzienników banku X i modele uzgodnień są na produkcji (Odoo FR 79); połączenie z bankiem robi właściciel w dniu przełączenia.

**Po:** Każdy z 9 rachunków w banku X ma w Odoo swoje dzienniki bankowe i reguły automatycznego rozliczania wyciągów. Połączenie z bankiem włączymy w dniu przejścia na Odoo.

*Reguły:* „modele uzgodnień" objaśnione funkcją; „właściciel" (rola w zespole) zastąpione podmiotem zbiorowym albo konkretnym stanowiskiem.

## Process and UI

**Przed:** Ścieżka w menu: Księgowość → Raportowanie → Sprawozdania z oświadczeń → Profit and Loss (na ekranie „Zyski i straty").

**Po:** Księgowość ▸ Raportowanie ▸ „Zyski i straty" (rachunek zysków i strat w wariancie porównawczym).

*Reguły:* błędnego tłumaczenia menu („Sprawozdania z oświadczeń") nie przepisujemy, tylko wskazujemy ekran tak, jak użytkownik go znajdzie; termin ustawowy w nawiasie.

**Przed:** Drill-down. Każdą liczbę można „przewiercić": kliknięcie kwoty otwiera pozycje, z których powstała.

**Po:** Każda kwota w raporcie prowadzi do zapisów i dokumentów, z których powstała – wystarczy ją kliknąć.

*Reguły:* bez kalki „drill-down" i neologizmu w cudzysłowie.

**Przed:** Opisz pozycje: konto, MPK, kategoria | automat | Odoo | opis z oznaczeniem „pewny".

**Po:** 3. Odoo samo podpowiada konto i MPK dla każdej pozycji faktury na podstawie poprzednich faktur tego dostawcy. Pozycje, których nie potrafi przypisać, trafiają na listę „Do opisu" dla księgowej.

*Reguły:* krok numerowany ze zdaniem i wykonawcą; wewnętrzne oznaczenie („pewny") zastąpione opisem działania.

**Przed:** W Odoo (wariant porównawczy, bez zespołu 5) kroki PK13–PK15 zastępuje reguła zmiany stanu produktów z MPK produkcji minus 711/712.

**Po:** Dziś koszt wytworzenia wyrobów rozliczamy w Graffiti trzema przeksięgowaniami: z konta 501 na 580, z 580 na 621 i z 621 na 711 i 712. W Odoo zespołu 5 nie ma, bo księgi prowadzimy w wariancie porównawczym. Koszt wytworzenia liczy zlecenie produkcyjne, a zmianę stanu produktów system księguje przy przyjęciu wyrobu na magazyn.

*Reguły:* najpierw stan dzisiejszy słowami księgowej i numerami kont, potem nowy; bez skrótów „PK13–PK15".

## Decisions

**Przed:** Do rozstrzygnięcia przed 2027-01-01: plan kont jeden do jednego z kontami segmentowymi (Odoo FR 123, niezbudowane), różnica między RZiS a wynikiem w bilansie, pytania do głównej księgowej (KSI-40, KSI-61).

**Po** (terminy przykładowe):

| Decyzja | Kto | Termin |
|---|---|---|
| Czy przenosimy plan kont Graffiti jeden do jednego, razem z kontami segmentowymi | dyrektor finansowy z główną księgową | 15 grudnia 2026 r. |
| Skąd bierze się różnica między wynikiem w rachunku zysków i strat a wynikiem w bilansie | główna księgowa | przed bilansem otwarcia |
| Czy JPK_KR_PD za 2026 r. wysyłamy z Graffiti | główna księgowa, doradca podatkowy | 31 marca 2027 r. |

*Reguły:* decyzje jako tabela z właścicielem i terminem; pytania opisane treścią, nie numerem.
