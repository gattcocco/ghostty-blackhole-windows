# Ghostty Blackhole — Windows experiment

Adattamento sperimentale di [s0xDk/ghostty-blackhole](https://github.com/s0xDk/ghostty-blackhole), licenza MIT conservata. Non è ancora una versione Windows verificata graficamente.

Lo shader originale è conservato. L'adattamento Python tenta di inviare OSC 12/112 a `CONOUT$`, senza scrivere sequenze nel canale stdout catturato da Claude. Non crea finestre console. Il terminale e ConPTY devono trasmettere quei comandi: una scrittura riuscita NON dimostra che il colore arrivi allo shader. Gli hook di Claude potrebbero inoltre non ereditare una console; questo caso resta da verificare in una sessione vera.

## Prima prova, un passo alla volta

1. Scarica il pacchetto Windows x64 dalle [release del port comunitario di Ghostty](https://github.com/shiweis/ghostty-windows/releases), estrailo conservando tutte le risorse. È un progetto separato da Ghostty ufficiale. La numerazione del port non coincide necessariamente con quella upstream: servono le uniform del cursore introdotte in Ghostty 1.3.
2. In PowerShell, dentro questa cartella, esegui `python prepare.py`. Genera solo file locali e percorsi adatti a questo PC.
3. Avvia l'eseguibile scaricato passando `--config-file=` con il percorso assoluto di `preview.ghostty`. Esempio: `& 'C:/percorso/ghostty.exe' '--config-file=C:/percorso/ghostty-blackhole-windows/preview.ghostty'`.
4. Nella finestra scrivi o fai scorrere testo. La preview imposta TOKEN_LEVEL=0.5: deve mostrare il buco anche senza Claude, se il cursore non contiene già un segnale valido. È una prova grafica, NON misura il contesto.
5. Chiudi quella finestra e avvia Ghostty usando `live.ghostty`. Qui il buco inizialmente deve essere assente. Entra nella cartella del progetto e prova `python bh-drive.py 0.5`, poi `python bh-drive.py off`.
6. Solo se entrambi funzionano, prova `python bh-drive.py sweep --seconds 35`. Questo è controllo manuale per riprese: va dichiarato come dimostrazione.
7. Solo dopo la prova manuale collega Claude Code. `claude-settings.example.json` contiene le voci da integrare nelle impostazioni esistenti, preservando altri hook e valutando l'eventuale statusline già configurata. Non sostituire tutto il file delle impostazioni. Questa integrazione non è stata applicata automaticamente.

## Diagnosi

- Preview assente: verificare log di compilazione shader, caricamento config e versione del terminale.
- Preview presente, live assente: verificare OSC 12/112 attraverso ConPTY e console ereditata; non intervenire sulla fisica dello shader.
- Manuale presente, Claude assente: verificare comando hook, Python, JSON ricevuto e accesso alla console dai processi hook.
- `No writable console`: il comando non ha accesso a una console Windows; eseguirlo nella finestra Ghostty.
- Non eseguire il controllo manuale nella stessa finestra di una sessione Claude attiva.

## Verifiche automatiche

`python -m unittest -v test_bridge.py`

Verifica tutti i 251 livelli del protocollo, firma e checksum, reset, propagazione degli errori di trasporto, percentuale contesto e output UTF-8 catturato. Non sostituisce la verifica visiva né la prova di hook in Claude.

## Provenienza

File recuperati tramite connettore GitHub il 9 settembre 2026, non tramite clone con cronologia:

- blackhole.glsl blob `2178eb16bb02bd1e89170efaa97ef28e1663590a`
- claude-token.py blob originale `d80871504c8ee61929d62ea5177c8a7508a554c4`
- LICENSE blob `40743ad7eb711fd00051ce93bee180cd54839c1a`

Il README originale è in README.upstream.md. Il fork online conserva il tuner macOS e i media originali; il pacchetto locale di prova contiene solo i file necessari all'esperimento. Nessun dato del PC, delle sessioni o delle credenziali è incluso nel codice pubblicato.
