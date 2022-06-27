# Univerzalni Modularni Aparaturni Kontroler
Na SAU vežbama se koristi jedinstven program na Arduino mikrokontrolerima, koji služi kao most između aparature i `SauLib`, zvani Univerzalni Modularni Aparaturni Kontroler (UMAK). UMAK je takođe protokol kojim računar mora da komunicira sa kontrolerom kako bi obavio svoj posao, čiji se opis nalazi ispod. Komunikacija se obavlja preko UART.

## Pojmovi
### Kanal
UMAK dozvoljava da se preko jednog mikrokontrolera kontroliše više aparatura. Iz tog razloga, više komunikacionih kanala može da se koristi za komunikaciju sa različitim uređajima, dok god se ta komunikacija ne dešava u isto vreme. Kanali imaju identifikatore od 0 do 15. Trenutno je moguće da jedan ulazni i jedan izlazni uređaj koriste isti kanal, ali to nije preporučljivo.

### Komande
Komunikacija sa mikrokontrolerom preko UMAK protokola se obavlja slanjem komandi u vidu bajtova poslatih preko UART, jednu po jednu. UMAK definiše tri komande:
- `BIND`: Definiše preko kog UMAK kanala komunicira neki uređaj i podešava ga. Redosled bajtova kod ove komande je:
    1. Bajt sa vrednošću 253 (identifikator BIND komande)
    2. U zavisnosti od toga da li se podešava ulazni ili izlazni uređaj, komanda nastavlja na sledeći način:
        - Ukoliko se podešava ulazni uređaj:
            3. Bajt sa vrednošću 252 (identifikator podkomande za podešavanje ulaznog uređaja)
            4. Broj UMAK kanala na koji se ulazni uređaj podešava
            5. Parametar koji se prosleđuje ulaznom uređaju
                - Trenutno je moguće samo podesiti Arduino pin za ADC, tako da vrednosti od 100 do 105 odgovaraju pinovima A0 do A5
                - U slučaju temperaturnog senzora, SCL pin na Arduino je A5 a SDA je A4 i to nije moguće promeniti korišćenjem ovog parametra
            6. Identifikator tipa ulaznog uređaja:
                - 0: ADC
                - 1: Temperaturni senzor
        - Ukoliko se podešava izlazni uređaj:
            3. Bajt sa vrednošću 251 (identifikator podkomande za podešavanje izlaznog uređaja)
            4. Broj UMAK kanala na koji se izlazni uređaj podešava
            5. Identifikator tipa izlaznog uređaja:
                - 0: PWM na pinu 11, kome se tokom aktuacije šalju dva bajta (iz istorijskih razloga, iako `analogWrite()` koristi samo jedan)
                - 1: Servo na pinu 9, kome se tokom aktuacije šalje jedan bajt
                - 2: Servo na pinu 10, kome se tokom aktuacije šalje jedan bajt
- `ACT`: Šalje podatke izlaznom uređaju (aktuatoru). Redosled bajtova kod ove komande je:
    1. Bajt sa vrednošću 254 (identifikator ACT komande)
    2. Broj UMAK kanala na kome je podešen aktuator
    3. Bajtovi podataka za aktuaciju (broj bajtova definisan tipom izlaznog uređaja)
- `SENSOR`: Prima podatke od ulaznog uređaja (senzora). Redosled bajtova kod ove komande je:
    1. Bajt sa vrednošću 255 (identifikator SENSOR komande)
    2. Broj UMAK kanala na kome je podešen senzor

### Odgovori
Kao odgovor na komande preko UMAK protokola mikrokontroleru on može da vrati nekoliko tipova odgovora, u vidu bajta (karaktera) poslatog preko UART:
- `'A'`: *Acknowledge*. Mikrokontroler je ispravno primio podatke i reagovao na njih
- `'E'`: *Error*. Mikrokontroler je primio podatke i detektovao kršenje protokola ili neku drugu grešku (npr. pokušaj BIND za temperaturni senzor dok on nije ispravno inicijalizovan)
- `'S'`: *Sensor*. Poslata je `SENSOR` komanda i mikrokontroler šalje odgovor, u narednim bajtovima dolaze bajtovi odgovora, od nižih ka višim bajtovima

## Komunikacija
Sa mikrokontrolerom preko UMAK protokola se komunicira preko serijskog porta, na 19200 bauda. Računar šalje komande a mikrokontroler odgovore kao što je definisano u odeljku Pojmovi iznad. Za potrebe SAU radionice, preporučuje se korišćenje `Device` metoda `bind_input_device`, `bind_output_device`, `actuate` i `sensor` za komunikaciju preko UMAK.
