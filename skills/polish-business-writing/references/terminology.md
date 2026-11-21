# Terminology

Use the accounting term in prose; quote the screen label once where the reader must find it. Screen labels below come from the Odoo 19 Polish translation file (`addons/account/i18n/pl.po`) unless marked "sprawdź w UI": translations change between versions and installations, so read the live screen before quoting.

## Odoo screen label ↔ accounting term

| Odoo (English) | Odoo (polski ekran) | Termin księgowy do tekstu | Uwagi |
|---|---|---|---|
| Chart of Accounts | Plan kont | zakładowy plan kont | Ustawa o rachunkowości, art. 10 ust. 1 pkt 3 lit. a. |
| Account | Konto | konto syntetyczne (księga główna) / konto analityczne (księgi pomocnicze) | Art. 16–17. Odoo nie rozróżnia poziomów; strukturę daje numeracja kont. |
| Analytic Account | Konto analityczne | MPK, projekt, wymiar analityczny | Pułapka: w polskiej rachunkowości „konto analityczne" to podkonto. Nie zostawiaj gołego terminu. |
| Analytic Plan | Plan analityczny | wymiar analityczny (np. MPK, projekty) | |
| Analytic Distribution | Rozbicie analityczne | podział na MPK / projekty | |
| Journal | Dziennik | dziennik częściowy; dla sprzedaży i zakupu także rejestr | Art. 14 ust. 3 dopuszcza dzienniki częściowe z miesięcznym zestawieniem obrotów. |
| Journal Entry | Zapis dziennika (też „Zapisy księgowe") | zapis księgowy; ręczny: polecenie księgowania | Odoo jest tu niespójne; w tekście pisz „zapis księgowy". |
| Journal Items | Pozycje dziennika | zapisy na kontach, obroty | |
| Post / Posted | Zaksięguj / Zaksięgowano | zaksięgować / zaksięgowany | Przycisk sprawdź w UI. |
| Draft | Projekt / Szkic (sprawdź w UI) | dokument niezaksięgowany, faktura do zaksięgowania | „Szkic rachunku" brzmi obco; pisz „faktura zakupu czekająca na zaksięgowanie". |
| Vendor Bill / Bill | Faktura zakupu (miejscami „Rachunek") | faktura zakupu, faktura kosztowa | „Rachunek" to w polszczyźnie inny dokument; nie używaj. |
| Customer Invoice | Faktura sprzedaży | faktura sprzedaży | |
| Credit Note | Nota Kredytowa | faktura korygująca | Ustawa o VAT, art. 106j. „Nota kredytowa" to kalka i w Polsce inny dokument. |
| Reconcile / Reconciliation | Uzgodnij / Uzgadnianie | rozliczyć rozrachunek; uzgodnić wyciąg bankowy | Rozrachunki się rozlicza, wyciąg się uzgadnia. |
| Register Payment | Zarejestruj płatność | zaksięgować zapłatę | |
| Batch Payment | Płatność zbiorcza (sprawdź w UI) | paczka przelewów | Tak mówią księgowe i banki. |
| Bank Synchronization | Synchronizacja bankowa | automatyczne pobieranie wyciągów | |
| Fiscal Position | Obszar podatkowy | reguły zamiany stawek VAT (np. WDT, import usług, odwrotne obciążenie) | Kalka; zawsze objaśnij. |
| Tax Report / Tax Return | Raport podatkowy (sprawdź w UI) | rejestr VAT; deklaracja i ewidencja JPK_V7M | |
| Lock Dates | Daty blokady (sprawdź w UI) | blokada okresu, zamknięcie miesiąca do zmian | Ostateczne zamknięcie ksiąg (art. 12) to coś więcej niż blokada daty. |
| Hard Lock Date | Data twardej blokady | trwała blokada okresu (bez możliwości odblokowania) | „Twarda blokada" to kalka. |
| Deferred Expense | Odroczone wydatki (sprawdź w UI) | rozliczenia międzyokresowe czynne kosztów | Art. 39 ust. 1. |
| Deferred Revenue | Odroczone przychody | rozliczenia międzyokresowe przychodów | Art. 41. |
| Accrual (accrued expense) | Naliczenie (sprawdź w UI) | rozliczenia międzyokresowe bierne kosztów, rezerwa | Art. 39 ust. 2. |
| Reversal / Reverse Entry | Odwrócenie / Data odwrócenia | storno (czerwone albo czarne), zapis odwracający | |
| Unrealized Currency Gains/Losses | Niezrealizowane zyski/straty (sprawdź w UI) | wycena bilansowa pozycji w walutach obcych, niezrealizowane różnice kursowe | Art. 30 ust. 1. |
| Exchange Difference | Różnica kursowa | różnica kursowa (zrealizowana) | |
| Inventory Valuation (automated) | Wycena zapasów (automatyczna) | ewidencja ciągła (ilościowo-wartościowa), księgowanie w czasie rzeczywistym | |
| Inventory Valuation (manual/periodic) | Ręczna / okresowa | ewidencja okresowa, wycena na podstawie spisu | |
| FIFO / AVCO / Standard Price | FIFO / Średni koszt / Cena standardowa | „pierwsze weszło, pierwsze wyszło" / cena przeciętna (średnia ważona) / cena ewidencyjna z odchyleniami | Art. 34 ust. 1 i 4. |
| Price Difference account | Różnica cen | odchylenia od cen ewidencyjnych | |
| Landed Costs | Koszty nabycia (sprawdź w UI) | koszty zakupu doliczane do ceny nabycia (transport, cło) | Art. 28 ust. 2. |
| Manufacturing Order | Zlecenie produkcyjne (sprawdź w UI) | zlecenie produkcyjne | |
| Bill of Materials | Zestawienie materiałowe (sprawdź w UI) | normatyw materiałowy, struktura wyrobu | |
| Work Center | Gniazdo produkcyjne (sprawdź w UI) | stanowisko (gniazdo) robocze, koszt godziny stanowiska | |
| Work in Progress (WIP) | Produkcja w toku (sprawdź w UI) | produkcja w toku | |
| MO cost / product cost | Koszt produkcji | koszt wytworzenia produktu; rozliczenie kosztów produkcji | Art. 28 ust. 3. |
| Budget | Budżet | budżet, plan kosztów | |
| Profit and Loss | Zyski i straty | rachunek zysków i strat (wariant porównawczy albo kalkulacyjny) | Załącznik nr 1 do ustawy. |
| Balance Sheet | Bilans | bilans | |
| General Ledger | Księga główna | księga główna, obroty i salda kont | |
| Aged Receivable / Payable | Należności / Zobowiązania wiekowane | wiekowanie należności i zobowiązań | |
| Audit Trail | Ścieżka audytu | ślad rewizyjny, historia zmian | |
| Approvals | Zatwierdzenia | akceptacja (obieg akceptacji) | |
| Statement reports | Sprawozdania z oświadczeń (sic) | sprawozdania finansowe | Błąd tłumaczenia; nigdy nie przepisuj do tekstu. |

## Polish compliance terms

| Termin | Pierwsze użycie w tekście | Potem |
|---|---|---|
| KSeF | Krajowy System e-Faktur (KSeF) | KSeF, numer KSeF, UPO (urzędowe poświadczenie odbioru) |
| JPK_V7M | jednolity plik kontrolny z deklaracją i ewidencją VAT (JPK_V7M) | JPK_V7M |
| JPK_KR_PD | księgi rachunkowe w formie jednolitego pliku kontrolnego dla CIT (JPK_KR_PD) | JPK_KR_PD |
| biała lista | wykaz podatników VAT (biała lista), ustawa o VAT art. 96b | biała lista; płatność powyżej 15 000 zł na rachunek spoza wykazu ma skutki w CIT i VAT |
| MPP | mechanizm podzielonej płatności | podzielona płatność |
| MPK | miejsce powstawania kosztów (MPK) | MPK |
| konta segmentowe | konta wieloczłonowe, których kolejne człony (segmenty) oznaczają np. MPK albo grupę produktów | konta segmentowe |

## Kalki i zamienniki

| Nie pisz | Pisz |
|---|---|
| workflow, flow, przepływ (o procesie) | obieg, przebieg, kolejne kroki |
| feature | funkcja |
| drill-down, przewiercić | przejść do zapisów źródłowych, rozwinąć do dokumentu |
| dashboard | pulpit, zestawienie |
| mapowanie | przyporządkowanie |
| dedykowany | przeznaczony do, osobny |
| implementować | wdrożyć, uruchomić |
| adresować problem | rozwiązać, zająć się |
| na ten moment | obecnie, dziś |
| w oparciu o | na podstawie |
| szkic rachunku | faktura zakupu czekająca na zaksięgowanie |
| odroczone wydatki | rozliczenia międzyokresowe kosztów |
| nota kredytowa | faktura korygująca |
| twarda blokada | trwała blokada okresu |
| strażnik, automat (o regule systemu) | system sam sprawdza / blokuje |
| ulubione RPT-002 | zapisany raport „Marża według zamówień" |
