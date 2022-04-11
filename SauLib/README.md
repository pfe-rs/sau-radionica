# SauLib
Biblioteka za upravljanje aparaturom na vežbama iz sistema automatskog upravljanja.

## Instalacija
Potrebno je pokrenuti `pip install .` unutar ovog direktorijuma kako bi se instalirale biblioteke od koje ova biblioteka zavisi.

## Struktura
Biblioteka je struktuirana na sledeći način:
- `API`: Moduli specifični za svaku aparaturu koji krajnjim korisnicima izvoze jednu klasu koja nasleđuje `ApiBase`, omogućavajući im da implementiraju samo `control` metodu kako bi upravljali svojom aparaturom.
- `devices`: Pomoćni moduli za upravljanje uređajima, kao i implementacija UMAK protokola.
- `examples`: Deo koji se krajnjim korisnicima daje kao šablon sa ostavljenom `control` metodom za implementaciju. Za svaku vežbu postoji po jedan `test_api_*.py` fajl.
- `legacy`: Nekorišćeni moduli.
