# Snap!-Übung: Passwort-Knacker selbst bauen

Snap! (UC Berkeley) hat einen `url`-Block für echte Web-Anfragen (Palette **Fühlen**) — damit lassen sich beide Runden des Workshops eins zu eins nachbauen, nicht nur die Brute-Force-Runde. mBlock fällt raus: kein natives HTTP ohne Custom-Extension.

Beide Übungen sprechen denselben Endpunkt an: `https://cyber.certain.cc/login?pw=<versuch>`, optional mit `&laenge=<N>` für die Brute-Force-Runde. Antwort ist immer der reine Text `GEKNACKT` oder `FALSCH`.

## Übung 1 — Wortliste (die Haupt-Übung, hier wird geknobelt)

Kids überlegen sich selbst: Was würde jemand von dieser Schule wohl als Passwort nehmen? Sie bauen eine Liste eigener Vermutungen und lassen Snap! sie der Reihe nach durchprobieren.

**Variablen:** `verdachte` (Liste), `versuch`, `ergebnis`

**Skript:**
```
Wenn Fahne angeklickt
setze verdachte auf (Liste) [manuell befuellen, z.B. "dientzenbach", "dg-gymnasium", "schule2026", ...]
fuer jedes (versuch) in (verdachte)
    sage versuch
    setze ergebnis auf (url [https://cyber.certain.cc/login?pw= + versuch])
    falls (ergebnis = "GEKNACKT")
        sage (verbinde "GEKNACKT! Passwort ist " versuch) fuer 999 Sek.
        stoppe alles
```

**Block-Fundorte:** `url` — Fühlen · `verbinde` — Operatoren · `fuer jedes ... in`, `sage`, Variablen, Listen — jeweils zugehoerige Paletten.

**Didaktik:** Die Liste selbst ist der Lerninhalt — je besser die Kids über die Zielperson/-institution nachdenken (Schulname, Jahr, Kürzel, Leetspeak-Varianten), desto eher taucht das echte Passwort in ihrer eigenen Liste auf. Kein Geruest noetig, das ist bewusst offen zum Ausprobieren.

## Übung 2 — Brute-Force (Demonstration: warum reicht Raten nicht mehr?)

Nach der Wortliste-Runde: systematisch *alle* Kombinationen einer Länge durchprobieren, nicht nur Vermutungen. Ziel-Passwörter sind fest und wachsen mit der Länge: `dg` (2 Zeichen) → `dg2` (3) → `dg26` (4) → `dg26!` (5) → `dg2026` (6) → `dg2026!` (7) → `Dg2026!#` (8). Der Server prüft gegen das jeweils zur `laenge` passende Ziel — die URL braucht dafür `&laenge=N` zusätzlich zu `pw=`.

**Realistisch als Kids-Bauprojekt:** nur Länge 2, Kleinbuchstaben a-z (findet `dg`). Zwei verschachtelte Schleifen sind für die Zielgruppe gut machbar:

**Variablen:** `versuch`, `alphabet`

**Skript:**
```
Wenn Fahne angeklickt
setze alphabet auf "abcdefghijklmnopqrstuvwxyz"
fuer jedes (b1) in (zerlege alphabet in Buchstaben)
    fuer jedes (b2) in (zerlege alphabet in Buchstaben)
        setze versuch auf (verbinde b1 b2)
        sage versuch
        falls ( (url [https://cyber.certain.cc/login?pw= + versuch + &laenge=2]) = "GEKNACKT" )
            sage (verbinde "GEKNACKT! Passwort ist " versuch) fuer 999 Sek.
            stoppe alles
```

Findet `dg`. Tauscht man `alphabet` gegen Grossbuchstaben (`"ABCDEFGHIJKLMNOPQRSTUVWXYZ"`), findet dasselbe Skript `DG` — guter Show-Moment, um zu zeigen, dass die Wahl des Zeichensatzes das Ergebnis direkt bestimmt.

**Als Lehrer-Demo, nicht zum Selberbauen:** ein drittes verschachteltes `fuer jedes`-Loop plus Ziffern 0-9 im Alphabet und `&laenge=3` in der URL würde `dg2` suchen — aber schon das ist mit ~36³ Kombinationen praktisch aussichtslos in einer Unterrichtsstunde (das Web-Tool auf `/hack` zeigt exakt dasselbe Verhalten mit sichtbarem Zaehler, siehe README). Empfehlung: das *zeigen* (kurz laufen lassen, den Zähler wachsen sehen, dann abbrechen) statt die Kids ein drittes Loop von Hand bauen zu lassen — der Punkt ("das wird schnell unmöglich") kommt so schneller an als über zusätzliche Block-Verschachtelung.

## Didaktischer Ablauf (Vorschlag)

1. Wortliste zuerst: Kids raten, bauen ihre Verdächtigenliste, lassen Snap! durchlaufen. Meistens Erfolg, wenn sie klug raten.
2. Brute-Force Länge 2 als zweite Übung: zeigt, dass man auch *ohne* zu raten ans Ziel kommt, wenn der Raum klein genug ist.
3. Lehrer-Demo Länge 3+ (Web-Tool oder vorgebautes Snap!-Skript): zeigt live, wo Brute-Force aufhört, praktikabel zu sein — der eigentliche Payoff des ganzen Workshops.
