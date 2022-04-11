# sau-radionica
Repozitorijum sa vežbama iz sistema automatskog upravljanja.

## Instalacija
Potrebni alati za pokretanje vežbi mogu se instalirati navigacijom u `SauLib` direktorijum i instaliranjem te biblioteke.
```
cd SauLib
pip install .
```
Ukoliko je UMAK spušten na mikrokontroler koji koristite prilikom izrade vežbi, možete nastaviti na deo o pokretanju vežbe.

### UMAK
Univerzalni Modularni Aparaturni Kontroler (UMAK) je jedinstveni program koji za potrebe SAU vežbi služi kao most između Python programa i Arduino mikrokontrolera. Za njegovu instalaciju potrebno je instalirati [Arduino IDE](https://www.arduino.cc/en/software) i u njemu instalirati Servo biblioteku, zatim spustiti program na Arduino.

## Pokretanje
U `SauLib/examples` direktorijumu mogu se naći `test_api_*.py` datoteke u kojima stoje označeni delovi koda koje treba dopuniti kako bi se kontrolisala vežba. Kod za dopunu nalazi se unutar `control` metode koja kao argument prima pobudu sistema a vraća novu vrednost koju treba upisati na senzor koji se koristi na toj vežbi (opseg vrednosti opisan je u samoj datoteci).

## Struktura
Projekat je struktuiran na sledeći način:
- `SauLib`: Python biblioteka za upravljanje aparaturama za SAU vežbe
- `UMAK`: Univerzalni Modularni Aparaturni Kontroler
- `workshop`: Jupyter sveske sa vežbi iz SAU

Više o samim delovima možete pročitati iz README fajlova tih delova.
