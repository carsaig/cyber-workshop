# Snap!-Übung: Passwort-Knacker selbst bauen

Warum Snap! und nicht mBlock: beide sind Scratch-Familie, aber Snap! (UC Berkeley) hat einen `url`-Block für echte Web-Anfragen; mBlock kann ohne Custom-Extension kein HTTP.

Ziel: alle Zweier-Kombis `a-z` durchprobieren, jede gegen den Endpunkt schicken, bei Treffer jubeln. Findet `hi`.

## Variablen

- `versuch`
- `alphabet`

## Skript

```
Wenn Fahne angeklickt
setze alphabet auf "abcdefghijklmnopqrstuvwxyz"
für jedes (b1) in (zerlege alphabet in Buchstaben)
    für jedes (b2) in (zerlege alphabet in Buchstaben)
        setze versuch auf (verbinde b1 b2)
        sage versuch
        falls ( (url [https://cyber.certain.cc/login?pw= + versuch]) = "GEKNACKT" )
            sage (verbinde "GEKNACKT! Passwort ist " versuch) für 999 Sek.
            stoppe alles
```

## Block-Fundorte

- `url` — Fühlen
- `zerlege … in Buchstaben`, `verbinde` — Operatoren
- `für jedes … in`, `sage`, Variablen — jeweils zugehörige Paletten

## Didaktik-Tipp

Gerüst (zwei Schleifen + `sage`) vorbauen, Kids setzen nur die zwei Zauber-Blöcke ein (`url`-Vergleich + "GEKNACKT"-Jubel).

## Offen

Optional eine fertige `.mblock`- bzw. Snap!-`.xml`-Lösungsdatei zum Importieren erzeugen (bisher nicht gebaut/getestet).
