https://github.com/josepmariasiso/Projecte-Machine-Learning/sprint4.2.md

# Documentació del Procés de Bank Marketing relaciona amb les campanyes de telemarketing de bancs portuguesos
## 1. Fonts

**Identificació de Fonts:**
- https://archive.ics.uci.edu/dataset/222/bank+marketing

**Descripció de les Fonts:**
- Les dades estan relacionades amb campanyes de màrqueting directe d'una entitat bancària portuguesa. Les campanyes de màrqueting es van basar en trucades telefòniques. Sovint, calia més d'un contacte amb un mateix client, per poder accedir a si el producte (dipòsit a termini bancari) estaria subscrit ('sí') o no ('no').

  
## 2. Mètodes de recol·lecció de dades

**Procediments i Eines:**
- Exportació programada en format CSV, emmagatzemada en la esmentada web i alternativament al Github de ITACADEMY. Aquesta tasca la fa el departament d'IT.

**Freqüència de Recol·lecció:**
- Cada cop que hi hagi una actualitzacio. Darrera versio 13/02/2012
  
**Scripts de Descàrrega:**

```python
import pandas as pd

csv_url = "https://raw.githubusercontent.com/ITACADEMYprojectes/projecteML/refs/heads/main/bank_dataset.CSV"
df = pd.read_csv(csv_url)
print(df.info())

```

## 3. Format i Estructura de les Dades

**Tipus de Dades:**
- Numèrics: `age`, `balance`, `duration`, `campaign`, `pdays`,`previous`
- Categòric: `job`, `marital`, `education`,`contact`,`poutcome`
- Binari: `default`,`housing`,`loan`,`y`
- Data: `day_of_week`,`month`

**Format d'Emmagatzematge:**
- Dades tabulars emmagatzemades en fitxer csv.

## 4. Limitacions de les dades

- Diferents Temps d'Actualització: Les dades d'ús al
github i del lloc web poden ser recol·lectades i actualitzades al fitxer CSV en moments diferents.

## 5. Consideracions sobre Dades Sensibles

**Tipus de Dades Sensibles:**
- Informació Personal Identificable (PII): No n'hi ha
- Informació Financera Sensible: `default`,`balance`,`housing`,`loan`
- Dades Comportamentals Sensibles:`duration`

**Mesures de Protecció:**
- **Anonimització i Pseudonimització:**
  - Es poden aplicar escalats per a difuminar la informacio financera sensible
- **Accés Restringit:**
  - Accés a dades sensibles restringit només a personal autoritzat amb necessitat de conèixer aquestes dades per a fins específics del projecte.
- **Compliment de Regulacions:**
  - Compliment amb la GDRP