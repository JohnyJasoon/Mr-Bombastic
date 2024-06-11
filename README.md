## Mr Bombastic – project gry typu Bomberman obsługującej wielowątkowość

### Opis Gry

Gra Bomberman to klasyczna gra komputerowa, w której gracz porusza się po planszy, rozmieszcza bomby i unika wrogów, aby zdobyć punkty i przetrwać jak najdłużej. W tej implementacji gra została stworzona w języku Python z użyciem biblioteki curses do obsługi interfejsu tekstowego oraz mechanizmów wielowątkowości do zarządzania ruchem przeciwników, eksplozjami bomb sterowania.

### Funkcjonalności

### Sterowanie

- **Ruch**: Gracz porusza się za pomocą klawiszy strzałek.
  - **↑** - Ruch w górę
  - **→** - Ruch w prawo
  - **↓** - Ruch w dół
  - **←** - Ruch w lewo
- **Umieszczanie bomb**: Naciśnięcie spacji powoduje umieszczenie bomby na aktualnej pozycji gracza.

### Elementy Gry

- **Gracz**: Reprezentowany przez znak „B”, może poruszać się po planszy, unikać wrogów i umieszczać bomby.
- **Wrogowie**: Reprezentowani przez znak E, poruszają się losowo po planszy. Dotknięcie wroga przez gracza kończy grę.
- **Bomba**: Reprezentowana przez znak o, eksploduje po 2 sekundach, tworząc eksplozję.
- **Eksplozja**: Reprezentowana przez znak \*, trwa przez krótki czas i niszczy wszystko w zasięgu, z wyjątkiem niektórych przeszkód.
- **Ściany**:
  - **Niezniszczalne**: Reprezentowane przez #, mogą być zniszczone przez eksplozje.
  - **Zniszczalne**: Reprezentowane przez &, nie mogą być zniszczone i blokują eksplozje.

### Zasady Gry

- **Punkty**: Gracz zdobywa 10 punktów za każdego zniszczonego wroga.
- **Przegrana**: Gra kończy się, gdy gracz zostanie trafiony przez eksplozję bomby lub dotknie wroga.
- **Przeciwnicy**: Pojawiają się na planszy co 5 sekund, zwiększając poziom trudności gry.

### Uruchomienie Gry

**Wymagania**

- Python 3.6 lub nowszy
- Biblioteka curses (wbudowana w standardową bibliotekę Pythona na systemach UNIX)

**Uruchomienie**

1. **Uruchomienie Gry**: W katalogu z plikiem gry uruchom:
```bash
  python3 ./bomberman.py
```
1. **Gra uruchomi się w terminalu**, a sterowanie odbywa się za pomocą klawiatury. Gra kończy się, gdy gracz zostanie zniszczony. Aby przerwać grę w dowolnym momencie, zamknij okno terminala.

### Struktura Kodu

**Główne Klasy i Funkcje**

- **Board**: Klasa odpowiedzialna za logikę gry i przechowywanie stanu planszy. Obsługuje tworzenie ścian, rozmieszczanie bomb, kontrolę eksplozji, ruch wrogów i inne kluczowe aspekty gry.
- **Enemy**: Klasa reprezentująca wrogów, z metodami do poruszania się po planszy.
- **controller**: Funkcja obsługująca sterowanie gracza i interakcję z planszą.
- **start**: Funkcja uruchamiająca główne wątki gry i inicjalizująca główną pętlę gry, która aktualizuje stan planszy oraz wyświetla ją w terminalu.

**Mechanizmy Wielowątkowe**

Gra wykorzystuje wielowątkowość do równoległego wykonywania zadań, takich jak:

- **Sterowanie Graczem**: Wątek nasłuchuje na klawisze i odpowiednio porusza graczem (control_thread).
- **Aktualizacja Bomb**: Wątek sprawdza czas wybuchu bomb i inicjuje eksplozje (bomb_thread).
- **Czyszczenie Eksplozji**: Wątek usuwa stare eksplozje z planszy (explosion_clean_thread).
- **Ruch Wrogów**: Wątek losowo przesuwa wrogów po planszy (enemy_move_thread).
- **Generowanie Wrogów**: Wątek dodaje nowych wrogów na planszy co określony czas (enemy_spawn_thread).

**Mutexy (Mutual Exclusion)**

Mutexy są stosowane do synchronizacji dostępu do współdzielonych zasobów, aby uniknąć problemów takich jak wyścigi.

-**self.lock**: Zapewnia bezpieczną aktualizację stanu planszy i gracza, blokując dostęp do tych zasobów dla innych wątków podczas modyfikacji.
```bash
with self.lock:
    self.player = (new_row, new_col)
```
**Semafory**

Semafory zarządzają dostępem do zasobów, umożliwiając wielokrotny dostęp równocześnie.

-**self.bomb_sem**: Kontroluje dostęp do listy bomb, zapewniając, że tylko jeden wątek może jednocześnie modyfikować listę bomb.
```bash
self.bomb_sem.acquire()
# Dodawanie lub usuwanie bomb
self.bomb_sem.release()
```
-**self.enemy_sem**: Kontroluje dostęp do listy wrogów, zapewniając bezpieczne dodawanie nowych wrogów i aktualizację ich pozycji.
```bash
self.enemy_sem.acquire()
# Dodawanie nowych wrogów
self.enemy_sem.release()
```

### Koncepcja wyglądu gry

![bomber](https://github.com/JohnyJasoon/Mr-Bombastic/assets/45130672/738fe2b2-28d2-4cdb-976d-ac86ef7a788e)

- **Pełne kwadraty** - ściany niezniszczalne
- **Puste kwadraty** - ściany zniszczalne
- **Koło** - gracz
- **Okręgi** - przeciwnicy
- **Gwiazdki** - bomba w trakcie wybuchu

### Uwagi Końcowe

Gra Bomberman została zaprojektowana tak, aby była prosta do zrozumienia i modyfikowania. Możesz swobodnie eksperymentować z różnymi aspektami gry, takimi jak liczba wrogów, czas trwania eksplozji czy rozmiar planszy. Zachęcamy do dalszego rozwijania i dostosowywania gry według własnych pomysłów i preferencji.
