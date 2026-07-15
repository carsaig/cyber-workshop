#!/usr/bin/env python3
# app.py  -  Cyber-Workshop: Passwort-Knacker (Mock-Ziel + Kinder-Werkzeug)
# Nur gegen dieses selbstgehostete Mock. Start: pip install -r requirements.txt ; python app.py
import os
from flask import Flask, request, jsonify

app = Flask(__name__)
GEHEIM = [p.strip() for p in os.environ.get("GEHEIM", "dientzenbach-gymnasium,hi").split(",") if p.strip()]

# Feste, thematisch passende Brute-Force-Ziele pro Laenge. Kein Zufall/Hash mehr:
# laengere/komplexere Ziele erfordern echte, groessere Suchraeume, dadurch
# korreliert die Knackzeit tatsaechlich mit Laenge und gewaehlten Zeichenarten.
BASIS_PRO_LAENGE = {
    2: "dg",
    3: "dg2",
    4: "dg26",
    5: "dg26!",
    6: "dg2026",
    7: "dg2026!",
}
ACHT_ZEICHEN_ZIEL = "Dg2026!#"

WORTLISTE = ["123456","passwort","password","hallo","qwertz","111111","fussball","schule",
"sonnenschein","ichliebedich","master","lassmichrein","admin","test","1234","hallo123",
"berlin","bayern","sommer","winter","engel","schatz","09876","dragon","monkey","letmein",
"pokemon","minecraft","fortnite","starwars","harrypotter","iloveyou","000000","abc123",
"Passwort1","qwerty","sommer2024","hunter2","superman","batman","football",
"123456789","12345678","1234567","12345","qwerty123","1q2w3e4r","000000","qwertyuiop",
"123321","666666","7777777","1qaz2wsx","zaq12wsx","qazwsx","password1","password123",
"welcome","welcome1","login","freedom","whatever","trustno1","princess","sunshine",
"shadow","ashley","michael","jennifer","jordan","hunter","killer","hockey","george",
"charlie","andrew","tigger","robert","thomas","hannah","daniel","joshua","matthew",
"amanda","samantha","summer","cheese","biteme","dallas","yankees","liverpool",
"chelsea","arsenal","internet","service","computer","corvette","mercedes","ferrari",
"jordan23","jasmine","natasha","abcdef","asdfgh","zxcvbn","abcabc","121212",
"112233","123abc","1a2b3c","q1w2e3","p@ssw0rd","passw0rd","adminadmin","letme1n",
"iloveyou1","loveyou","forever","friends","family","music","soccer","baseball",
"basketball","volleyball","gymnasium","klasse10","klasse9","pausenhof","hausaufgaben",
"ferien2025","ferien2026","sommerferien","schuljahr","klassenfahrt"]


def bruteforce_ziele(laenge: int) -> set[str]:
    """Menge der akzeptierten Brute-Force-Ziele fuer eine gegebene Laenge.

    Fuer Laenge 2-7 alle Gross-/Kleinschreibungs-Varianten der jeweiligen
    Basis (Ziffern/Sonderzeichen bleiben fix). Laenge 8 hat genau ein
    vollstaendig spezifiziertes Ziel. Andere Laengen haben kein definiertes
    Ziel (immer "nicht gefunden").
    """
    if laenge == 8:
        return {ACHT_ZEICHEN_ZIEL}
    basis = BASIS_PRO_LAENGE.get(laenge)
    if not basis:
        return set()
    varianten = {""}
    for zeichen in basis:
        neu = set()
        for prefix in varianten:
            if zeichen.isalpha():
                neu.add(prefix + zeichen.lower())
                neu.add(prefix + zeichen.upper())
            else:
                neu.add(prefix + zeichen)
        varianten = neu
    return varianten

PAGE_MOCK = """<!doctype html><html lang=de><meta charset=utf-8>
<meta name=viewport content="width=device-width,initial-scale=1"><title>Super-Sichere Bank 3000</title>
<style>body{font-family:system-ui,sans-serif;background:#161033;color:#e8e6ff;display:flex;
min-height:100vh;align-items:center;justify-content:center;margin:0}.b{background:#0d0a24;
padding:2rem 2.5rem;border-radius:18px;width:min(90vw,360px);text-align:center;box-shadow:0 20px 60px #0008}
h1{font-size:1.15rem}input{font-size:1.2rem;padding:.6rem;border-radius:10px;border:none;width:80%}
button{margin-top:1rem;padding:.7rem 1.4rem;border:none;border-radius:10px;background:#ffcf5c;
color:#161033;font-weight:800;cursor:pointer}#o{margin-top:1rem;font-weight:800;min-height:1.4rem}
a{color:#9d8cff;font-size:.8rem}</style>
<div class=b><h1>&#127974; Super-Sichere Bank 3000</h1><p>Geheimes Passwort:</p>
<input id=p type=password><br><button onclick=t()>Einloggen</button><div id=o></div>
<a href=/hack>&rarr; Passwort-Knacker &ouml;ffnen</a></div>
<script>async function t(){const r=await fetch('/login',{method:'POST',
headers:{'Content-Type':'application/json'},body:JSON.stringify({pw:p.value})});
const d=await r.json();o.textContent=d.ok?'GEKNACKT!':'Falsch.';
o.style.color=d.ok?'#4ef2c0':'#ff6b8a'}</script></html>"""

PAGE_HACK = """<!doctype html><html lang=de><meta charset=utf-8>
<meta name=viewport content="width=device-width,initial-scale=1"><title>Passwort-Knacker</title>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700&family=JetBrains+Mono:wght@700&display=swap" rel=stylesheet>
<style>:root{--bg:#161033;--pan:#0d0a24;--ink:#e8e6ff;--lab:#9d8cff;--gold:#ffcf5c;--mint:#4ef2c0;--cor:#ff6b8a}
*{box-sizing:border-box}body{margin:0;font-family:'Space Grotesk',system-ui,sans-serif;background:var(--bg);
color:var(--ink)}header{padding:1rem 1.5rem;font-weight:700;font-size:1.1rem;border-bottom:1px solid #ffffff18}
.wrap{display:grid;grid-template-columns:320px 1fr;gap:1.2rem;padding:1.2rem;max-width:1000px;margin:auto}
@media(max-width:760px){.wrap{grid-template-columns:1fr}}
.pan{background:var(--pan);border-radius:16px;padding:1.2rem}
.lab{color:var(--lab);font-size:.8rem;text-transform:uppercase;letter-spacing:.08em;margin:.8rem 0 .3rem}
label{display:block;margin:.3rem 0;cursor:pointer}textarea{width:100%;height:120px;background:#00000030;
color:var(--ink);border:1px solid #ffffff22;border-radius:10px;padding:.5rem;font-family:'JetBrains Mono',monospace;font-size:.8rem}
.seg{display:flex;gap:.4rem;margin-bottom:.5rem}.seg button{flex:1;padding:.5rem;border:1px solid #ffffff22;
background:transparent;color:var(--ink);border-radius:10px;cursor:pointer;font-weight:700}
.seg button.on{background:var(--gold);color:var(--bg);border-color:var(--gold)}
#start{width:100%;margin-top:1rem;padding:.9rem;border:none;border-radius:12px;background:var(--mint);
color:var(--bg);font-weight:800;font-size:1.05rem;cursor:pointer}
#start:disabled{opacity:.4;cursor:not-allowed}
.ticker{font-family:'JetBrains Mono',monospace;font-size:2.4rem;font-weight:700;color:var(--gold);
word-break:break-all;min-height:3rem}.stats{display:flex;gap:1.5rem;flex-wrap:wrap;margin:1rem 0}
.stat b{font-size:1.5rem;display:block;font-family:'JetBrains Mono',monospace}.stat span{color:var(--lab);font-size:.75rem}
.gauge{background:#00000030;border-radius:12px;padding:1rem;margin-top:1rem}
.gauge .row{display:flex;justify-content:space-between;padding:.25rem 0}.gauge b{font-family:'JetBrains Mono',monospace}
input[type=range]{width:100%}#win{position:fixed;inset:0;background:#161033f2;display:none;
flex-direction:column;align-items:center;justify-content:center;z-index:9}#win.show{display:flex}
#win h1{font-size:min(18vw,7rem);color:var(--mint);margin:0;letter-spacing:.05em}
#win .pw{font-family:'JetBrains Mono',monospace;font-size:1.8rem;color:var(--gold)}
#win button{margin-top:1.5rem;padding:.7rem 1.4rem;border:none;border-radius:10px;background:var(--gold);color:var(--bg);font-weight:800;cursor:pointer}
#meld{color:var(--cor);min-height:1.2rem;margin-top:.5rem}</style>
<header>Passwort-Knacker &middot; <span style=color:#9d8cff>Ziel: Super-Sichere Bank 3000</span></header>
<div class=wrap>
 <div class=pan>
  <div class=lab>Methode</div>
  <div class=seg><button id=m-wl class=on onclick=modus('wortliste')>Wortliste</button>
   <button id=m-bf onclick=modus('bruteforce')>Brute-Force</button></div>
  <div id=box-wl><div class=lab>Passwortliste</div>
   <p style="font-size:.75rem;color:var(--lab);margin:.2rem 0 .5rem">Was wuerde jemand von dieser Schule wohl als Passwort nehmen? Ergaenze eigene Vermutungen unten in der Liste (eine pro Zeile) und druecke Start.</p>
   <textarea id=woerter>%%WOERTER%%</textarea></div>
  <div id=box-bf style=display:none>
   <div class=lab>Zeichensatz</div>
   <label><input type=checkbox id=s-klein checked onchange="schaetz();pruefeEinstellungen()"> Kleinbuchstaben a-z</label>
   <label><input type=checkbox id=s-zahlen onchange="schaetz();pruefeEinstellungen()"> Zahlen 0-9</label>
   <label><input type=checkbox id=s-gross onchange="schaetz();pruefeEinstellungen()"> Grossbuchstaben A-Z</label>
   <label><input type=checkbox id=s-sonder onchange="schaetz();pruefeEinstellungen()"> Sonderzeichen !?-_@#</label>
   <div class=lab>Laenge: <span id=lval>2</span></div>
   <input type=range id=laenge min=1 max=8 value=2 oninput="lval.textContent=this.value;schaetz();pruefeEinstellungen()">
  </div>
  <button id=start onclick=toggle()>Start</button><div id=meld></div>
 </div>
 <div class=pan>
  <div class=lab>Aktueller Versuch</div><div class=ticker id=ticker>&middot;</div>
  <div class=stats><div class=stat><b id=n>0</b><span>Versuche</span></div>
   <div class=stat><b id=rate>0</b><span>pro Sekunde</span></div>
   <div class=stat><b id=zeitv>0,0 s</b><span>Zeit</span></div></div>
  <div class=gauge><div class=lab style=margin-top:0>Wie sicher waere so ein Passwort?</div>
   <div class=row><span>Moegliche Kombinationen</span><b id=kombis>-</b></div>
   <div class=row><span>Knackzeit online (10/Sek.)</span><b id=zon>-</b></div>
   <div class=row><span>Knackzeit fuer Profi (10 Mrd./Sek.)</span><b id=zoff>-</b></div></div>
 </div>
</div>
<div id=win><h1>GEKNACKT!</h1><div class=pw id=winpw></div><button onclick="win.classList.remove('show')">Nochmal</button></div>
<script>
const $=s=>document.querySelector(s);
const SETS={klein:"abcdefghijklmnopqrstuvwxyz",zahlen:"0123456789",
gross:"ABCDEFGHIJKLMNOPQRSTUVWXYZ",sonder:"!?-_@#"};
const MAX=2000,POOL=20;let laufen=false,versuche=0,t0=0,tick=null;
function modus(m){const wl=m==='wortliste';$('#box-wl').style.display=wl?'':'none';
 $('#box-bf').style.display=wl?'none':'';$('#m-wl').classList.toggle('on',wl);
 $('#m-bf').classList.toggle('on',!wl);}
function cs(){let s='';if($('#s-klein').checked)s+=SETS.klein;if($('#s-zahlen').checked)s+=SETS.zahlen;
 if($('#s-gross').checked)s+=SETS.gross;if($('#s-sonder').checked)s+=SETS.sonder;return s;}
function fmt(n){if(n<1000)return Math.round(n).toString();const e=['',' Tsd.',' Mio.',' Mrd.',' Bio.',' Brd.'];
 let i=0;while(n>=1000&&i<e.length-1){n/=1000;i++;}return n.toFixed(1).replace('.',',')+e[i];}
function zeit(s){if(s<1)return'sofort';const u=[['Jahre',31536000],['Tage',86400],['Std.',3600],['Min.',60],['Sek.',1]];
 for(const[nm,v]of u){if(s>=v){const x=s/v;return(nm==='Jahre'&&x>1e6?fmt(x):x.toFixed(x<10?1:0).replace('.',','))+' '+nm;}}return'sofort';}
function schaetz(){const k=Math.pow(cs().length||1,+$('#laenge').value);
 $('#kombis').textContent=fmt(k);$('#zon').textContent=zeit(k/10);$('#zoff').textContent=zeit(k/1e10);}
function aktiveKlassen(){let n=0;if($('#s-klein').checked)n++;if($('#s-zahlen').checked)n++;
 if($('#s-gross').checked)n++;if($('#s-sonder').checked)n++;return n;}
function pruefeEinstellungen(){const n=aktiveKlassen(),l=+$('#laenge').value;
 if(n>l){meld('Zu viele Zeichenarten fuer '+l+' Zeichen gewaehlt (max. '+l+').');$('#start').disabled=true;return false;}
 meld('');$('#start').disabled=false;return true;}
async function pruefe(pw){versuche++;const bf=$('#m-bf').classList.contains('on');
 const body=bf?{pw,modus:'bruteforce',laenge:+$('#laenge').value}:{pw,modus:'wortliste'};
 const r=await fetch('/login',{method:'POST',
 headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});return(await r.json()).ok;}
function* brute(chars,laenge){const a=chars.split('');if(laenge<=0)return;const idx=Array(laenge).fill(0);
 while(true){yield idx.map(i=>a[i]).join('');let p=laenge-1;while(p>=0){if(++idx[p]<a.length)break;idx[p]=0;p--;}if(p<0)break;}}
function stats(){const s=(performance.now()-t0)/1000;$('#n').textContent=versuche.toLocaleString('de-DE');
 $('#rate').textContent=s>0?Math.round(versuche/s).toLocaleString('de-DE'):'0';$('#zeitv').textContent=s.toFixed(1).replace('.',',')+' s';}
function toggle(){laufen?stopp():starte();}
function stopp(){laufen=false;$('#start').textContent='Start';if(tick)clearInterval(tick);}
function meld(x){$('#meld').textContent=x||'';}
async function starte(){laufen=true;versuche=0;t0=performance.now();meld('');$('#win').classList.remove('show');
 $('#start').textContent='Stopp';tick=setInterval(stats,100);
 const bf=$('#m-bf').classList.contains('on');let iter;
 if(bf){const c=cs();if(!c){meld('Bitte einen Zeichensatz waehlen.');stopp();return;}
  if(!pruefeEinstellungen()){stopp();return;}
  iter=brute(c,+$('#laenge').value);}
 else iter=$('#woerter').value.split('\\n').map(w=>w.trim()).filter(Boolean).values();
 let hit=null,stop=false;
 async function worker(){while(laufen&&!hit&&!stop){if(bf&&versuche>=MAX){stop=true;break;}
   const it=iter.next();if(it.done){stop=true;break;}$('#ticker').textContent=it.value||'.';
   if(await pruefe(it.value))hit=it.value;}}
 await Promise.all(Array.from({length:POOL},worker));
 clearInterval(tick);stats();
 if(hit){$('#winpw').textContent='Passwort: '+hit;$('#win').classList.add('show');}
 else if(laufen)meld(bf&&versuche>=MAX?'Abgebrochen nach '+MAX+' Versuchen - Suchraum zu gross (siehe Anzeige).':'Nicht gefunden.');
 stopp();}
schaetz();pruefeEinstellungen();
</script></html>"""

@app.after_request
def cors(r):
    r.headers["Access-Control-Allow-Origin"] = "*"   # damit Snap! den Endpunkt ansprechen darf
    return r

@app.route("/")
def index():
    return PAGE_MOCK

@app.route("/hack")
def hack():
    return PAGE_HACK.replace("%%WOERTER%%", "\n".join(WORTLISTE))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":                       # fuers Web-Tool (JSON)
        body = request.get_json(silent=True) or {}
        pw = str(body.get("pw", ""))
        if body.get("modus") == "bruteforce":
            try:
                laenge = int(body.get("laenge", 0))
            except (TypeError, ValueError):
                laenge = 0
            return jsonify(ok=(pw in bruteforce_ziele(laenge)))
        return jsonify(ok=(pw in GEHEIM))               # Wortliste + Mock-Login
    pw = request.args.get("pw", "")                    # fuer Snap! (Klartext)
    laenge_param = request.args.get("laenge")
    if laenge_param is not None:                        # Snap!-Brute-Force: ?pw=..&laenge=N
        try:
            laenge = int(laenge_param)
        except ValueError:
            laenge = 0
        ok = pw in bruteforce_ziele(laenge)
    else:                                                # Snap!-Wortliste: ?pw=.. (kein laenge)
        ok = pw in GEHEIM
    return "GEKNACKT" if ok else "FALSCH"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
