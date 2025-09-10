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

### Sprawdzenie Setupu Kampanii
- **Sprawdzanie aktualnej konfiguracji kampanii** - pobiera rzeczywiste dane z GraphQL API
- **Wybór pól do sprawdzenia** - użytkownik może wybrać które pola chce sprawdzić
- **Wprowadzanie oczekiwanych wartości** - dla każdego pola można wprowadzić oczekiwaną wartość
- **Automatyczne porównywanie** - porównuje rzeczywiste wartości z oczekiwanymi
- **Status porównania**:
  - ✅ **PASUJE** - wartość dokładnie się zgadza
  - ⚠️ **CZĘŚCIOWO PASUJE** - wartość częściowo się zgadza
  - ❌ **NIE PASUJE** - wartość się nie zgadza

#### Dostępne pola do sprawdzenia:
- **Podstawowe informacje**: nazwa kampanii, status, daty, typ subkampanii, data centers, landing URL
- **Budżety i limity**: budżet dzienny/miesięczny, impresje, limity wydatków
- **Targeting Policy**: SSP, Deals, Hosty, App IDs, URL Labels
- **Ad API Framework**: obsługiwane frameworki
- **Profile Identifiers**: dozwolone/niedozwolone typy
- **Mobile Placement**: ustawienia fullscreen
- **Bidding Model CPM**: wartości CPM dla różnych segmentów
- **Device Types**: dozwolone/niedozwolone typy urządzeń
- **Geotargeting**: kraje, regiony, miasta
- **User Segments**: segmenty użytkowników
- **Creative IDs**: przypisane kreacje
- **Placement Environment**: środowiska umieszczania
- **Traffic Quality**: Max BR, Min VCR, Viewability
- **Cookie Types**: dozwolone typy cookies
- **Fraud Prevention**: zabronione etykiety

### 📊 Zmiana Statusu Kampanii
- Zmiana statusu kampanii (ACTIVE, PAUSED)
- Dodawanie komentarzy do zmian

### 💡 Podpowiedzi
- Automatyczne podpowiedzi dla pól konfiguracji
- Wyświetlanie możliwych wartości i formatów

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
python campaign_setuper.py
```

## Użytkowanie

### 1. Health Check
1. Wprowadź ID advertisera (domyślnie: 63113)
2. Kliknij "🔍 Sprawdź advertisera"
3. Sprawdź wyniki w sekcji wyników

### 2. Sprawdzenie Setupu Kampanii
1. Wprowadź Campaign ID i Advertiser ID
2. Wybierz pola które chcesz sprawdzić (checkboxy)
3. **Opcjonalnie**: wprowadź oczekiwane wartości w polach tekstowych pod każdym checkboxem
4. Kliknij " Sprawdź setup kampanii"
5. Sprawdź wyniki:
   - Rzeczywiste wartości z kampanii
   - Status porównania (jeśli podano oczekiwane wartości)
   - Oczekiwane wartości (jeśli podano)

### 3. Konfiguracja Kampanii
1. Wprowadź ID kampanii
2. Wybierz pola do konfiguracji z listy
3. Wprowadź wartości w polach konfiguracji (z podpowiedziami)
4. Kliknij "Zapisz konfigurację"

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
├── campaign_setuper.py # Główna aplikacja (z funkcją sprawdzania setupu)
├── previous_version.py # Poprzednia wersja (bez sprawdzania ustawień)
├── get-campaign-info.md # Referencja zapytań GraphQL
├── update_kampanii.md # Referencja mutacji GraphQL
├── requirements.txt # Wymagane biblioteki
└── README.md # Ten plik
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
