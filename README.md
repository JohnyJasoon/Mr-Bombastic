**Mr Bombastic – project gry typu Bomberman obsługującej wielowątkowość**

**Opis Gry**

Gra Bomberman to klasyczna gra komputerowa, w której gracz porusza się po planszy, rozmieszcza bomby i unika wrogów, aby zdobyć punkty i przetrwać jak najdłużej. W tej implementacji gra została stworzona w języku Python z użyciem biblioteki curses do obsługi interfejsu tekstowego oraz mechanizmów wielowątkowości do zarządzania ruchem przeciwników, eksplozjami bomb sterowania.

**Funkcjonalności**

**Sterowanie**

- **Ruch**: Gracz porusza się za pomocą klawiszy strzałek.
  - **↑** - Ruch w górę
  - **→** - Ruch w prawo
  - **↓** - Ruch w dół
  - **←** - Ruch w lewo
- **Umieszczanie bomb**: Naciśnięcie spacji powoduje umieszczenie bomby na aktualnej pozycji gracza.

**Elementy Gry**

- **Gracz**: Reprezentowany przez znak „B”, może poruszać się po planszy, unikać wrogów i umieszczać bomby.
- **Wrogowie**: Reprezentowani przez znak E, poruszają się losowo po planszy. Dotknięcie wroga przez gracza kończy grę.
- **Bomba**: Reprezentowana przez znak o, eksploduje po 2 sekundach, tworząc eksplozję.
- **Eksplozja**: Reprezentowana przez znak \*, trwa przez krótki czas i niszczy wszystko w zasięgu, z wyjątkiem niektórych przeszkód.
- **Ściany**:
  - **Niezniszczalne**: Reprezentowane przez #, mogą być zniszczone przez eksplozje.
  - **Zniszczalne**: Reprezentowane przez &, nie mogą być zniszczone i blokują eksplozje.

**Zasady Gry**

- **Punkty**: Gracz zdobywa 10 punktów za każdego zniszczonego wroga.
- **Przegrana**: Gra kończy się, gdy gracz zostanie trafiony przez eksplozję bomby lub dotknie wroga.
- **Przeciwnicy**: Pojawiają się na planszy co 5 sekund, zwiększając poziom trudności gry.

**Uruchomienie Gry**

**Wymagania**

- Python 3.6 lub nowszy
- Biblioteka curses (wbudowana w standardową bibliotekę Pythona na systemach UNIX)

**Uruchomienie**

1. **Uruchomienie Gry**: W katalogu z plikiem gry uruchom:
```bash
  python3 bomberman.py
```
1. **Gra uruchomi się w terminalu**, a sterowanie odbywa się za pomocą klawiatury. Gra kończy się, gdy gracz zostanie zniszczony. Aby przerwać grę w dowolnym momencie, zamknij okno terminala.

**Struktura Kodu**

**Główne Klasy i Funkcje**

- **Board**: Klasa odpowiedzialna za logikę gry i przechowywanie stanu planszy. Obsługuje tworzenie ścian, rozmieszczanie bomb, kontrolę eksplozji, ruch wrogów i inne kluczowe aspekty gry.
- **Enemy**: Klasa reprezentująca wrogów, z metodami do poruszania się po planszy.
- **controller**: Funkcja obsługująca sterowanie gracza i interakcję z planszą.
- **start**: Funkcja uruchamiająca główne wątki gry i inicjalizująca główną pętlę gry, która aktualizuje stan planszy oraz wyświetla ją w terminalu.

**Mechanizmy Wielowątkowe**

Gra wykorzystuje wielowątkowość do równoległego wykonywania zadań, takich jak:

- Aktualizacja bomb i eksplozji
- Poruszanie wrogów
- Generowanie nowych wrogów
- Reagowanie na sterowanie gracza

Każda z tych funkcjonalności jest obsługiwana przez osobny wątek, co umożliwia płynne działanie gry bez opóźnień i zacięć.

**Uwagi Końcowe**

Gra Bomberman została zaprojektowana tak, aby była prosta do zrozumienia i modyfikowania. Możesz swobodnie eksperymentować z różnymi aspektami gry, takimi jak liczba wrogów, czas trwania eksplozji czy rozmiar planszy. Zachęcamy do dalszego rozwijania i dostosowywania gry według własnych pomysłów i preferencji.
