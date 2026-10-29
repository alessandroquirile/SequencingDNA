# Spec di Design: Animazione Introduttiva sulla Classificazione DNA

## Obiettivo
Aggiungere all'inizio del file `dna_pipeline.py` (all'interno della classe `DNAPipelineAnimation`) una fase introduttiva ("FASE INTRO") che spieghi visivamente e didatticamente cosa significhi effettuare la classificazione di una sequenza di DNA:
- Visualizzazione della sequenza di nucleotidi in input (colori distinti per A, C, G, T).
- Elaborazione/lettura da parte dell'algoritmo di intelligenza artificiale mediante un effetto visivo di scansione ("lettura" delle basi).
- Smistamento visivo della sequenza verso una delle 7 classi molecolari (famiglie geniche/proteiche) target del dataset, con evidenziazione della classe predetta.

## Architettura e Posizionamento
- **File interessato**: `dna_pipeline.py`
- **Punto di inserimento**: All'inizio di `DNAPipelineAnimation.construct()`, subito dopo `self.camera.background_color = "#111111"` e prima di `# FASE 0: Dataset Originale (human.txt)`.
- **Durata stimata**: ~10-12 secondi di animazione fluida con pause didattiche.

## Dettaglio degli Elementi Visivi

### 1. Intestazione
- Titolo principale: `"Cos'è la Classificazione del DNA?"` (`font_size=24`, bianco, posizionato in alto con `to_edge(UP, buff=0.4)`).
- Sottotitolo: `"Assegnare una sequenza di nucleotidi a una classe funzionale"` (`font_size=13`, colore `GRAY_A`).

### 2. Disposizione dei Componenti (Layout a 3 colonne)
1. **Colonna Sinistra (Input - DNA)**:
   - Etichetta: `"Sequenza di DNA (Input)"` (`font_size=13`, colore `TEAL`).
   - Mobject Sequenza: Nucleotidi colorati individualmente per impatto biologico:
     - `A`: Verde (`#2ECC71` o `GREEN`)
     - `C`: Azzurro (`#3498DB` o `BLUE`)
     - `G`: Giallo/Oro (`#F39C12` o `GOLD`)
     - `T`: Rosso/Corallo (`#E74C3C` o `RED`)
     - Esempio di stringa: `"ATGCCCCAACTAAAT..."`
   - Bordo contenitore leggero attorno alla sequenza.

2. **Colonna Centrale (AI / Modello di Classificazione)**:
   - Box rettangolare arrotondato con bordo ciano/azzurro e sfondo semitrasparente.
   - Testo interno: `"Modello AI\n(Classificatore)"` (`font_size=14`, grassetto).
   - Animazione di scansione: una linea verticale dorata/ciano (`Line`) o box luminoso che scorre orizzontalmente attraverso i nucleotidi della sequenza per simulare la "lettura/estrazione delle feature".

3. **Colonna Destra (I 7 Target Funzionali)**:
   - Lista compatta dei 7 box/etichette corrispondenti alle 7 classi molecolari del dataset:
     - `0: Recettori GPCR`
     - `1: Tirosin-chinasi`
     - `2: Tirosina fosfatasi`
     - `3: Sintetasi`
     - `4: Sintasi`
     - `5: Canale ionico`
     - `6: Fattore di trascrizione`
   - Ogni classe racchiusa in un piccolo mobject/badge per simulare i "contenitori" o le categorie di destinazione.

### 3. Dinamica di Smistamento ed Output
- Una freccia curva (`CurvedArrow`) o particella/connessione luminosa parte dal blocco AI e punta direttamente al contenitore target (es. `Classe 4: Sintasi`).
- Il box della classe target subisce una trasformazione/ingrandimento con cambio colore (verde fluorescente / oro, es. `Indicate` o `SurroundingRectangle`).
- Appare un badge esplicativo vicino alla classe: `"✓ Predizione: Classe 4 (Sintasi)"`.
- In basso al centro compare una nota didattica di riepilogo:
  `"Input: Sequenza non etichettata ➔ Output: Categoria molecolare (0-6)"`.

### 4. Conclusione e Transizione
- `FadeOut` coordinato di tutti gli elementi della FASE INTRO.
- Breve `wait(0.5)` prima che inizi la FASE 0 già presente (`"Data set"`).
