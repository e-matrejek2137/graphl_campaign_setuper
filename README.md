# Campaign Setup Automator - RTB House

Aplikacja do automatycznego konfigurowania kampanii reklamowych w systemie RTB House za pomocą GraphQL API.

## Funkcjonalności

### 🔍 Health Check
- Sprawdzanie dostępności advertisera
- Walidacja konfiguracji systemu
- Wyświetlanie szczegółowych informacji o advertiserze
- Porównywanie z oczekiwanymi wartościami (PASUJE/NIE PASUJE/CZĘŚCIOWO PASUJE)

### ⚙️ Konfiguracja Kampanii
- Automatyczne ustawianie obowiązkowych pól:
  - Data Centers: `["ash", "phx", "sin", "ams"]`
  - GDPR Macros: `false`
  - Subcampaign Type: `"performance-retargeting"`
  - Landing Macro: `"https://www.rtbhouse.com/blog?utm_source=rtbhouse&utm_medium=performance&rtbhc={RTBHC}"`
  - User Segments: `["BUYERS", "NEW", "SHOPPERS", "VISITORS"]`
  - Allow One Tag Bids: `true`

- Konfiguracja pól wybranych przez użytkownika:
  - Podstawowe informacje (daty)
  - Limity budżetowe i impresji
  - Targeting policy (SSP, Deals, Device Types, Geotargeting)
  - Ad API Framework
  - Profile Identifiers
  - Mobile Placement
  - Bidding Model CPM
  - Creative IDs
  - Placement Environment

### 📊 Zmiana Statusu Kampanii
- Zmiana statusu kampanii (ACTIVE, PAUSED)
- Dodawanie komentarzy do zmian

### 💡 Podpowiedzi
- Automatyczne podpowiedzi dla pól konfiguracji
- Wyświetlanie możliwych wartości i formatów

### 🖥️ Interfejs użytkownika
- **Responsywny design** - okno automatycznie dostosowuje się do rozdzielczości ekranu (80% rozmiaru ekranu)
- **Przyciski zmiany rozmiaru** - możliwość szybkiej zmiany rozmiaru okna
- **Minimalny rozmiar** - zabezpieczenie przed zbyt małym oknem
- **Wyśrodkowane okno** - automatyczne wyśrodkowanie na ekranie

## Wymagania

- Python 3.6+
- Dostęp do internetu
- Konto RTB House z dostępem do GraphQL API

## Instalacja

1. Sklonuj repozytorium:
```bash
git clone https://github.com/e-matrejek2137/graphl_campaign_setuper.git
cd graphl_campaign_setuper
```

2. Zainstaluj wymagane biblioteki:
```bash
pip install -r requirements.txt
```

3. Uruchom aplikację:
```bash
python complete_mutations_app_enriched.py
```

## Użytkowanie

### 1. Health Check
1. Wprowadź ID advertisera (domyślnie: 63113)
2. Kliknij "🔍 Sprawdź advertisera"
3. Sprawdź wyniki w sekcji wyników

### 2. Konfiguracja Kampanii
1. Wprowadź ID kampanii
2. Wybierz pola do konfiguracji z listy
3. Wprowadź wartości w polach konfiguracji (z podpowiedziami)
4. Kliknij "Zapisz konfigurację"

### 3. Sprawdzenie Setupu Kampanii (NOWA FUNKCJONALNOŚĆ)
1. Wprowadź Campaign ID i Advertiser ID
2. Wybierz pola które chcesz sprawdzić (checkboxy)
3. **Opcjonalnie**: wprowadź oczekiwane wartości w polach tekstowych pod każdym checkboxem
4. Kliknij " Sprawdź setup kampanii"
5. Sprawdź wyniki:
   - Rzeczywiste wartości z kampanii
   - Status porównania (jeśli podano oczekiwane wartości)
   - Oczekiwane wartości (jeśli podano)

### 4. Zmiana Statusu
1. Wprowadź ID kampanii
2. Wybierz nowy status (ACTIVE/PAUSED)
3. Dodaj komentarz (opcjonalnie)
4. Kliknij "Zmień status"

## Konfiguracja API

Aplikacja używa następujących ustawień API:
- URL: `https://api.campaigns.rtbhouse.biz/api/campaigns/graphql`
- Autoryzacja: Basic Auth
- Username: `ei-inv-graphql-campaigns-api`

## Struktura Projektu

```
graphl_campaign_setuper/
├── complete_mutat
```

## Bezpieczeństwo

⚠️ **UWAGA**: Aplikacja wykonuje rzeczywiste mutacje w systemie RTB House. Zawsze sprawdź wprowadzone dane przed potwierdzeniem.

## Rozwiązywanie Problemów

### Błąd połączenia
- Sprawdź połączenie internetowe
- Zweryfikuj dostępność API RTB House

### Błąd mutacji GraphQL
- Sprawdź format wprowadzonych danych
- Zweryfikuj dostępność pól w API
- Sprawdź plik `update_kampanii.md` dla poprawnych formatów

## Wsparcie

W przypadku problemów skontaktuj się z wojciech.pawlik@rtbhouse.com lub sprawdź dokumentację API.

## Licencja

Projekt wewnętrzny RTB House - do użytku firmowego.
