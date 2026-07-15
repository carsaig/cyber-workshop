# Cyber-Workshop: Passwort-Knacker

Lern-Mock für einen Cybersecurity-Workshop mit Schüler:innen der Mittelstufe (~12–13 J.): eine absichtlich schwache Login-Seite + ein Browser-Werkzeug, mit dem die Kids per Brute-Force / Wortliste ein Passwort "knacken". Zusätzlich eine Snap!-Übung, die die Kids selbst bauen und gegen denselben Endpunkt laufen lassen.

Kein echtes System wird angegriffen. Ziel und Angreifer sind beide selbst gehostet und bewusst schwach — reines Didaktik-Setup.

## Lernziele

- Runde 1 "Wortliste": Geheimnis `Sommer2025!` steht in der Passwortliste → fällt in Sekunden. Lektion: *vorhersehbar = wertlos, egal wie lang.*
- Runde 2 "Brute-Force": Geheimnis `hi` (Kleinbuchstaben, Länge 2) → Kids sehen die Schleife `aa, ab, ac…` bis zum Treffer.
- Entropie-Anzeige: Zeichensatz/Länge verstellen → geschätzte Knackzeit springt von "sofort" auf "Milliarden Jahre".

## Seiten

- `/` — Mock-Login (das "Ziel")
- `/hack` — Passwort-Knacker (Kinder-Werkzeug)
- `/login` — Endpunkt: `POST` mit JSON-Body `{"pw": "..."}` fürs Web-Tool, `GET ?pw=...` mit Klartext-Antwort (`GEKNACKT`/`FALSCH`) für Snap!

## Konfiguration

| Env-Var | Default | Bedeutung |
|---|---|---|
| `GEHEIM` | `Sommer2025!,hi` | Kommagetrennte akzeptierte Passwörter. Frei änderbar. |

## Lokal testen

```
pip install -r requirements.txt
python app.py
curl "http://localhost:8080/login?pw=hi"   # -> GEKNACKT
```

## Snap!-Übung

Siehe [`docs/snap-uebung.md`](docs/snap-uebung.md).

## Deployment

Dokploy, Projekt `dientzenbach-gymnasium`, Dockerfile-basierte Application. Domain per Env-seitigem TLS-Setup — siehe Projekt-internes Ops-Log für Details.

Nach dem Workshop (ca. 3 Tage später): DNS-Eintrag entfernen, App bleibt für die nächste Session erhalten.
