# -*- coding: utf-8 -*-
"""Générateur du site atelierpaca.fr — lancer depuis la racine du site :
    python3 build/generer.py
Produit toutes les pages HTML, le sitemap et le plan du site à partir de build/donnees.py."""
import os, json, html as H, sys
sys.path.insert(0, os.path.dirname(__file__))
from donnees import *

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
E = ENTREPRISE
PAGES = []  # (fichier, priorité, changefreq)

# ---------------------------------------------------------------- icônes (inline SVG, 24px)
ICO = {
 "tel":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.37 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.33 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/></svg>',
 "wa":'<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M17.47 14.38c-.3-.15-1.76-.87-2.03-.97-.27-.1-.47-.15-.67.15-.2.3-.77.97-.94 1.16-.17.2-.35.22-.64.07-.3-.15-1.25-.46-2.39-1.47-.88-.79-1.48-1.76-1.65-2.06-.17-.3-.02-.46.13-.61.13-.13.3-.35.44-.52.15-.17.2-.3.3-.5.1-.2.05-.37-.02-.52-.08-.15-.67-1.61-.92-2.21-.24-.58-.49-.5-.67-.51h-.57c-.2 0-.52.07-.79.37-.27.3-1.04 1.02-1.04 2.48s1.06 2.88 1.21 3.07c.15.2 2.1 3.2 5.08 4.49.71.3 1.26.49 1.69.63.71.22 1.36.19 1.87.12.57-.09 1.76-.72 2-1.41.25-.7.25-1.29.17-1.41-.07-.12-.27-.2-.57-.35M12.05 21.79h-.01a9.87 9.87 0 0 1-5.03-1.38l-.36-.21-3.74.98 1-3.65-.24-.37a9.86 9.86 0 0 1-1.51-5.26c0-5.45 4.44-9.88 9.89-9.88 2.64 0 5.12 1.03 6.99 2.9a9.82 9.82 0 0 1 2.89 6.99c0 5.45-4.44 9.88-9.89 9.88M20.46 3.49A11.82 11.82 0 0 0 12.05 0C5.5 0 .16 5.34.16 11.89c0 2.1.55 4.14 1.59 5.95L.06 24l6.3-1.65a11.88 11.88 0 0 0 5.69 1.45h.01c6.55 0 11.89-5.34 11.89-11.89 0-3.18-1.24-6.17-3.49-8.42"/></svg>',
 "doc":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6"/><path d="m9 15 2 2 4-4"/></svg>',
 "clock":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>',
 "shield":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10"/><path d="m9 12 2 2 4-4"/></svg>',
 "star":'<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01z"/></svg>',
 "pin":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="3"/></svg>',
 "mail":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 7L2 7"/></svg>',
 "arrow":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
 "menu":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>',
 "one":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 11 12 3l9 8"/><path d="M5 10v10h14V10"/><path d="M10 20v-6h4v6"/></svg>',
 "euro":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M18 6a7 7 0 0 0-11 5 7 7 0 0 0 11 7"/><path d="M4 10h9M4 14h9"/></svg>',
 "fb":'<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M14 9h3V6h-3c-2.2 0-4 1.8-4 4v2H8v3h2v7h3v-7h3l1-3h-4v-2c0-.6.4-1 1-1z"/></svg>',
 "ig":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor"/></svg>',
 "g":'<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M21.6 12.2c0-.7-.1-1.3-.2-1.9H12v3.7h5.4c-.2 1.2-.9 2.3-2 3v2.5h3.2c1.9-1.7 3-4.3 3-7.3z"/><path d="M12 22c2.7 0 5-.9 6.6-2.4l-3.2-2.5c-.9.6-2 1-3.4 1-2.6 0-4.8-1.8-5.6-4.1H3.1v2.6C4.8 19.8 8.2 22 12 22z"/><path d="M6.4 14c-.2-.6-.3-1.3-.3-2s.1-1.4.3-2V7.4H3.1C2.4 8.8 2 10.4 2 12s.4 3.2 1.1 4.6L6.4 14z"/><path d="M12 5.9c1.5 0 2.8.5 3.8 1.5l2.9-2.9C17 2.9 14.7 2 12 2 8.2 2 4.8 4.2 3.1 7.4L6.4 10c.8-2.3 3-4.1 5.6-4.1z"/></svg>',
}
# icônes métiers (pictos de la charte : robinet, radiateur/flamme, flocon, éclair, volet, cadenas)
ICO_METIER = {
 "plomberie":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3v4"/><path d="M8 7h8"/><path d="M6 11h12v3a3 3 0 0 1-3 3h-2v4"/><path d="M18 11v2h3"/><path d="M6 11v2H3"/></svg>',
 "chauffage":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 22c4 0 7-3 7-7 0-3-2-5-3-7-1 2-2 3-3 3 0-3-1-6-4-8 0 4-4 6-4 11a7 7 0 0 0 7 8z"/></svg>',
 "climatisation":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 2v20M4.9 6.5l14.2 11M4.9 17.5l14.2-11"/><path d="m9 4 3 2 3-2M9 20l3-2 3 2M3.5 9l3.3 1-1 3.3M20.5 15l-3.3-1 1-3.3M20.5 9l-3.3 1 1 3.3M3.5 15l3.3-1-1-3.3"/></svg>',
 "electricite":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M13 2 4 14h7l-1 8 9-12h-7z"/></svg>',
 "volets":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 8h18M3 12h18M3 16h18"/></svg>',
 "serrurerie":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="4" y="11" width="16" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/><circle cx="12" cy="16" r="1.5"/></svg>',
}
LOGO_SVG = ('<svg viewBox="0 0 330 52" role="img" aria-label="Atelier PACA"><defs><linearGradient id="lgR" x1="0" x2="1"><stop offset="0" stop-color="#ff2e4c"/><stop offset="1" stop-color="#e3202e"/></linearGradient></defs>'
            '<path d="M5 30 24 10l9 9V12h6v13l5 5" fill="none" stroke="url(#lgR)" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>'
            '<path d="M11 30v12h26V30" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" opacity=".9"/>'
            '<text x="56" y="31" font-family="Sora,system-ui,sans-serif" font-weight="800" font-size="24" fill="#fff" letter-spacing="1">ATELIER</text>'
            '<text x="166" y="31" font-family="Sora,system-ui,sans-serif" font-weight="800" font-size="24" fill="#ff2e4c" letter-spacing="1">PACA</text>'
            '<text x="57" y="46" font-family="Inter,system-ui,sans-serif" font-weight="600" font-size="9" fill="#a9b8d3" letter-spacing="1.7">INSTALLATION · ENTRETIEN · DÉPANNAGE</text></svg>')
FAVICON_SVG = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48"><rect width="48" height="48" rx="10" fill="#050d1f"/><path d="M8 29 24 12l8 8v-5h5v10l4 4" fill="none" stroke="#ff2e4c" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round"/><path d="M13 29v10h22V29" fill="none" stroke="#2fb0ff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg>'

def esc(s): return H.escape(str(s), quote=True)
def jd(o): return json.dumps(o, ensure_ascii=False, separators=(",", ":"))

# ---------------------------------------------------------------- blocs communs
def fit(desc):
    if len(desc) <= 160: return desc
    d = desc[:157]; return d[:d.rfind(" ")].rstrip(",.;:") + "…"

def head(title, desc, canon, extra_ld=None, og_img="images/og-atelier-paca.jpg", preload=None):
    ld = "".join(f'<script type="application/ld+json">{jd(o)}</script>' for o in (extra_ld or []))
    pre = f'<link rel="preload" as="image" href="{preload}" fetchpriority="high">' if preload else ""
    return f'''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self'; connect-src 'self' https://api.web3forms.com; form-action 'self' https://api.web3forms.com; base-uri 'self'; object-src 'none'; upgrade-insecure-requests">
<meta name="referrer" content="strict-origin-when-cross-origin">
<title>{esc(title)}</title>
<meta name="description" content="{esc(fit(desc))}">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta name="author" content="Atelier PACA">
<meta name="geo.region" content="FR-06"><meta name="geo.placename" content="Antibes">
<link rel="canonical" href="{SITE}{canon}">
<link rel="icon" type="image/svg+xml" href="favicon.svg">
<meta property="og:type" content="website"><meta property="og:locale" content="fr_FR"><meta property="og:site_name" content="Atelier PACA">
<meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(fit(desc))}">
<meta property="og:url" content="{SITE}{canon}"><meta property="og:image" content="{SITE}{og_img}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{esc(title)}"><meta name="twitter:description" content="{esc(fit(desc))}"><meta name="twitter:image" content="{SITE}{og_img}">
<link rel="preload" as="font" type="font/woff2" href="fonts/sora-400-xMQ9uFFYT72X5wkB_18qmnndmSdSnh2BAfO5mnuyOo1lfiQwV6-x.woff2" crossorigin>
<link rel="preload" as="font" type="font/woff2" href="fonts/inter-400-UcC73FwrK3iLTeHuS_nVMrMxCp50SjIa1ZL7.woff2" crossorigin>
{pre}
<link rel="stylesheet" href="fonts/fonts.css">
<link rel="stylesheet" href="assets/site.css">
{ld}
</head>
<body>
'''

def header(cur=""):
    def a(href, label):
        c = ' aria-current="page"' if href == cur else ""
        return f'<a href="{href}"{c}>{label}</a>'
    nav = "".join(a(t["page"], "Volets" if t["cle"]=="volets" else t["nom"]) for t in TRADES) + a("depannage-antibes.html", "Villes") + a("avis-clients.html", "Avis")
    menu = "".join(f'<a href="{t["page"]}">{t["nom"]}</a>' for t in TRADES)
    return f'''<header class="hdr"><div class="wrap">
<a href="index.html" class="logo" aria-label="Atelier PACA, installation entretien dépannage — accueil">{LOGO_SVG}</a>
<nav class="nav" aria-label="Navigation principale">{nav}</nav>
<div class="hdr-cta"><a href="{E["tel_href"]}" class="tel-hdr" aria-label="Appeler Atelier PACA au {E["tel"]}">{ICO["tel"]}<span>{E["tel"]}</span></a>
<button class="burger" id="burger" aria-label="Menu" aria-expanded="false" aria-controls="menu-m">{ICO["menu"]}</button></div>
</div></header>
<div class="menu-m" id="menu-m">{menu}<a href="urgence-depannage-24h.html">Urgence 24h/24</a><a href="contrat-entretien.html">Contrats d'entretien</a><a href="professionnels-syndics.html">Syndics et professionnels</a><a href="depannage-antibes.html">Villes d'intervention</a><a href="avis-clients.html">Avis clients</a><a href="realisations.html">Réalisations</a><a href="blog.html">Conseils</a><a href="contact.html">Contact</a><p class="sub">{E["tel"]} · {E["email"]}</p></div>
'''

def villes_footer():
    """Pied de page : uniquement les pages hub par ville (les pages métier × ville sont reliées depuis les pages métier et les hubs)."""
    def grp(vs, titre):
        return f'<details><summary>{titre} — {len(vs)} villes</summary><div class="chips">' + "".join(f'<a href="depannage-{v["slug"]}.html">{v["nom"]}</a>' for v in vs) + '</div></details>'
    return grp(VILLES_06, "Alpes-Maritimes (06)") + grp(VILLES_83, "Var est (83)") + '<p style="margin-top:10px"><a href="plan-du-site.html">Toutes les pages métier par ville</a></p>'

def footer():
    return f'''<footer class="ftr"><div class="wrap">
<div class="g">
<div><a href="index.html" class="logo" aria-label="Atelier PACA, installation entretien dépannage — accueil">{LOGO_SVG}</a>
<p style="margin-top:14px;max-width:360px">Plomberie, chauffage, climatisation, électricité, volets roulants et serrurerie dans les Alpes-Maritimes et le Var, depuis {E["depuis"]}. Un seul numéro pour toute la maison.</p>
<p><strong>{E["note"]}/5</strong> sur {E["avis"]} avis Google · garantie décennale · astreinte 24h/24</p>
<div class="soc"><a href="{E["facebook"]}" target="_blank" rel="noopener" aria-label="Facebook Atelier PACA">{ICO["fb"]}</a><a href="{E["instagram"]}" target="_blank" rel="noopener" aria-label="Instagram Atelier PACA">{ICO["ig"]}</a><a href="{maps(AGENCES[0])}" target="_blank" rel="noopener" aria-label="Fiche Google Atelier PACA">{ICO["g"]}</a></div></div>
<div><h3>Nos métiers</h3>{"".join(f'<a href="{t["page"]}">{t["nom"]}</a>' for t in TRADES)}<a href="urgence-depannage-24h.html">Urgence 24h/24</a><a href="contrat-entretien.html">Contrats d'entretien</a><a href="professionnels-syndics.html">Syndics et professionnels</a></div>
<div><h3>Atelier PACA</h3><a href="a-propos.html">Qui sommes-nous</a><a href="avis-clients.html">Avis clients</a><a href="realisations.html">Réalisations</a><a href="marques.html">Marques installées</a><a href="blog.html">Conseils d'artisans</a><a href="faq.html">Questions fréquentes</a><a href="contact.html">Contact et devis</a></div>
<div><h3>Nos agences</h3>{"".join(f'<a href="{maps(a)}" target="_blank" rel="noopener">{a["nom"]} — {a["adresse"]}, {a["cp"]} {a["ville"]}</a>' for a in AGENCES)}<p style="margin-top:10px"><a href="{E["tel_href"]}"><strong>{E["tel"]}</strong></a><a href="mailto:{E["email"]}">{E["email"]}</a></p></div>
</div>
<div class="villes-f"><p style="margin-bottom:8px">Atelier PACA près de chez vous :</p>{villes_footer()}</div>
<div class="bas"><span>© 2026 Atelier PACA (SASU) — SIREN {E["siren"]} — Tous droits réservés</span><span><a href="mentions-legales.html">Mentions légales</a> · <a href="plan-du-site.html">Plan du site</a></span></div>
</div></footer>
<div class="bar-m"><div class="in"><a href="{E["tel_href"]}" class="a1">{ICO["tel"]} Appeler</a><a href="{E["wa"]}" class="a2" target="_blank" rel="noopener">{ICO["wa"]} WhatsApp</a><a href="contact.html#devis" class="a3">{ICO["doc"]} Devis</a></div></div>
<div class="flot"><a href="{E["wa"]}" class="wa" target="_blank" rel="noopener" aria-label="WhatsApp Atelier PACA"><span style="color:#fff;display:contents">{ICO["wa"]}</span></a><a href="{E["tel_href"]}" class="tel" aria-label="Appeler Atelier PACA"><span style="color:#fff;display:contents">{ICO["tel"]}</span></a></div>
<script src="assets/site.js" defer></script>
</body>
</html>
'''

def crumb(items):
    ld = {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":i+1,"name":n,"item":SITE+h} for i,(n,h) in enumerate(items)]}
    htm = '<nav class="crumb" aria-label="Fil d’Ariane">' + " › ".join(f'<a href="{h}">{n}</a>' if i < len(items)-1 else f'<span>{n}</span>' for i,(n,h) in enumerate(items)) + '</nav>'
    return htm, ld

def faq_block(items, titre="Questions fréquentes", ctx=None, cls=""):
    items = [(q.format(**ctx) if ctx else q, a.format(**ctx) if ctx else a) for q,a in items]
    htm = f'<h2>{titre}</h2><div class="faq{(" " + cls) if cls else ""}">' + "".join(f'<details><summary>{esc(q)}</summary><div class="a"><p>{esc(a)}</p></div></details>' for q,a in items) + '</div>'
    ld = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in items]}
    return htm, ld

def ld_business(extra_type=None, agence=None):
    a = agence or AGENCES[0]
    types = ["LocalBusiness","Plumber","HVACBusiness","Electrician","Locksmith"]
    if extra_type and extra_type not in types: types.insert(1, extra_type)
    return {"@context":"https://schema.org","@type":types,"@id":SITE+"#organisation","name":"Atelier PACA",
      "url":SITE,"telephone":E["tel_intl"],"email":E["email"],"image":SITE+"images/og-atelier-paca.jpg","logo":SITE+"images/logo-atelier-paca.svg",
      "foundingDate":E["depuis"],"legalName":"Atelier PACA","slogan":"Un seul numéro pour toute votre maison",
      "description":"Atelier PACA est une entreprise artisanale d'Antibes (Alpes-Maritimes) fondée en 2015, qui regroupe six métiers du bâtiment : plomberie, chauffage, climatisation, électricité, volets roulants et serrurerie. Dépannage 24h/24, entretien et installation dans les Alpes-Maritimes (rayon de 30 km autour d'Antibes) et le Var est (Fréjus, Saint-Raphaël, pays de Fayence). Quatre agences : Antibes, Juan-les-Pins, Cagnes-sur-Mer, Le Cannet. Tarif minimum d'intervention 110 € HT, devis gratuit, garantie décennale.",
      "knowsAbout":["Plomberie","Dépannage plomberie","Chauffage","Entretien de chaudière","Pompe à chaleur","Climatisation réversible","Entretien de climatisation","Électricité","Mise aux normes électrique","Tableau électrique","Volets roulants","Motorisation de volets","Serrurerie","Ouverture de porte","Contrat d'entretien","Dépannage d'urgence 24h/24"],
      "priceRange":"€€","currenciesAccepted":"EUR","paymentAccepted":"Carte bancaire, virement, chèque, espèces",
      "address":{"@type":"PostalAddress","streetAddress":a["adresse"],"addressLocality":a["ville"],"postalCode":a["cp"],"addressRegion":"Provence-Alpes-Côte d'Azur","addressCountry":"FR"},
      "geo":{"@type":"GeoCoordinates","latitude":a["lat"],"longitude":a["lng"]},
      "hasMap":maps(a),
      "openingHoursSpecification":[{"@type":"OpeningHoursSpecification","dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],"opens":"00:00","closes":"23:59"}],
      "aggregateRating":{"@type":"AggregateRating","ratingValue":E["note"].replace(",","."),"reviewCount":E["avis"],"bestRating":"5","worstRating":"1"},
      "sameAs":[E["facebook"],E["instagram"]]+[maps(x) for x in AGENCES],
      "areaServed":[{"@type":"AdministrativeArea","name":"Alpes-Maritimes"},{"@type":"AdministrativeArea","name":"Var"}]+[{"@type":"City","name":v["nom"]} for v in VILLES],
      "department":[{"@type":"LocalBusiness","name":"Atelier PACA "+x["nom"],"telephone":E["tel_intl"],"address":{"@type":"PostalAddress","streetAddress":x["adresse"],"addressLocality":x["ville"],"postalCode":x["cp"],"addressCountry":"FR"},"hasMap":maps(x)} for x in AGENCES[1:]],
      "hasOfferCatalog":{"@type":"OfferCatalog","name":"Prestations Atelier PACA","itemListElement":[{"@type":"Offer","itemOffered":{"@type":"Service","name":t["nom"],"url":SITE+t["page"]}} for t in TRADES]}}

def cta_final(titre="Une panne, un projet ? Parlons-en.", sous="Devis gratuit sous 24 h, intervention sous 48 h dans le 06 et le Var, urgences 24h/24."):
    return f'''<section class="sec" style="padding-top:20px"><div class="wrap"><div class="cta-f"><h2>{titre}</h2><p>{sous}</p>
<div class="btns"><a href="{E["tel_href"]}" class="btn btn-rouge">{ICO["tel"]} {E["tel"]}</a><a href="{E["wa"]}" class="btn btn-wa" target="_blank" rel="noopener">{ICO["wa"]} WhatsApp</a><a href="contact.html#devis" class="btn btn-bleu">{ICO["doc"]} Devis gratuit</a></div></div></div></section>'''

def form_devis(service_defaut=None):
    opts = "".join(f'<option{" selected" if service_defaut==t["nom"] else ""}>{t["nom"]}</option>' for t in TRADES) + '<option>Contrat d’entretien</option><option>Autre / plusieurs métiers</option>'
    return f'''<form class="form" id="devis-form" action="https://api.web3forms.com/submit" method="POST">
<input type="hidden" name="access_key" value="{E["web3forms"]}"><input type="hidden" name="subject" value="Nouvelle demande de devis — atelierpaca.fr"><input type="hidden" name="from_name" value="Site atelierpaca.fr">
<input type="checkbox" name="botcheck" class="hp" tabindex="-1" aria-hidden="true">
<div class="row"><div class="g"><label for="f-nom">Nom</label><input id="f-nom" name="nom" type="text" autocomplete="name" required placeholder="Votre nom"></div>
<div class="g"><label for="f-tel">Téléphone</label><input id="f-tel" name="telephone" type="tel" autocomplete="tel" required placeholder="06 00 00 00 00"></div></div>
<div class="row"><div class="g"><label for="f-ville">Ville</label><input id="f-ville" name="ville" type="text" autocomplete="address-level2" placeholder="Antibes, Cagnes-sur-Mer…"></div>
<div class="g"><label for="f-service">Prestation</label><select id="f-service" name="prestation">{opts}</select></div></div>
<div class="g"><label for="f-msg">Votre besoin</label><textarea id="f-msg" name="message" placeholder="Décrivez la panne ou le projet, et le meilleur moment pour vous rappeler."></textarea></div>
<button type="submit" class="btn btn-rouge">Recevoir mon devis gratuit</button>
<div class="res" role="status" aria-live="polite"></div>
<p style="font-size:12.5px;color:var(--mut2);margin-top:12px;max-width:none">Réponse sous 2 h en journée. Vos coordonnées servent uniquement à vous rappeler.</p>
</form>'''

def coord_block():
    return f'''<div class="coord">
<div class="c"><div class="ic">{ICO["tel"]}</div><div><b>Téléphone — 24h/24</b><a href="{E["tel_href"]}">{E["tel"]}</a><a href="{E["wa"]}" target="_blank" rel="noopener">WhatsApp {E["mobile"]}</a></div></div>
<div class="c"><div class="ic">{ICO["mail"]}</div><div><b>E-mail</b><a href="mailto:{E["email"]}">{E["email"]}</a></div></div>
<div class="c"><div class="ic">{ICO["pin"]}</div><div><b>Siège — Antibes</b><span>{E["adresse"]}, {E["cp"]} {E["ville"]}</span><a href="{maps(AGENCES[0])}" target="_blank" rel="noopener">Itinéraire et avis Google</a></div></div>
<div class="c"><div class="ic">{ICO["clock"]}</div><div><b>Horaires</b><span>Astreinte 7 j/7, 24 h/24 pour les urgences. Devis et rendez-vous du lundi au vendredi.</span></div></div>
</div>'''

def write(fn, content, prio="0.6", freq="monthly"):
    with open(os.path.join(ROOT, fn), "w", encoding="utf-8") as f: f.write(content)
    PAGES.append((fn, prio, freq))

def chips_villes(prefix, cur=None):
    def grp(vs, titre, code):
        return f'<div><h3>{ICO["pin"]} {titre} <small>({code})</small></h3><div class="chips">' + "".join(f'<a href="{prefix}-{v["slug"]}.html"{" class=on" if v["slug"]==cur else ""}>{v["nom"]}</a>' for v in vs) + '</div></div>'
    return '<div class="villes">' + grp(VILLES_06, "Alpes-Maritimes", "06") + grp(VILLES_83, "Var est — Fréjus, Saint-Raphaël, pays de Fayence", "83") + '</div>'

def date_fr(iso):
    m = ["janvier","février","mars","avril","mai","juin","juillet","août","septembre","octobre","novembre","décembre"]
    y, mo, d = iso.split("-"); return f"{int(d)} {m[int(mo)-1]} {y}"

def de_(x):
    """« de » + lieu avec élision/contraction : d'Antibes, du Suquet, des Semboules, de la Bocca."""
    low = x.lower()
    if low.startswith("haut"): return "du " + x
    for pre, rep in (("le ", "du "), ("les ", "des "), ("la ", "de la "), ("l'", "de l'")):
        if low.startswith(pre): return rep + x[len(pre):]
    return ("d'" if low[0] in "aeiouyéèêàâîôûœ" else "de ") + x

def a_(x):
    """« à » + lieu : à Juan-les-Pins, au Suquet, aux Prés, à la Bocca."""
    low = x.lower()
    if low.startswith("haut"): return "au " + x
    for pre, rep in (("le ", "au "), ("les ", "aux ")):
        if low.startswith(pre): return rep + x[len(pre):]
    return "à " + x

def local_paras(v):
    """Texte local d'une ville : chaîne (1 paragraphe) ou liste de paragraphes."""
    loc = v.get("local")
    if not loc: return []
    return [loc] if isinstance(loc, str) else list(loc)

# ---------------------------------------------------------------- AVIS GOOGLE RÉELS
AGENCE_BY_KEY = {a["cle"]: a for a in AGENCES}
def agence_proche(v):
    """Agence (fiche Google) la plus proche d'une ville : son agence déclarée, sinon la plus proche à vol d'oiseau."""
    if v.get("agence"): return AGENCE_BY_KEY[v["agence"]]
    return min(AGENCES, key=lambda a: (a["lat"]-v["lat"])**2 + (a["lng"]-v["lng"])**2)
def mois_fr(aaaa_mm):
    m = ["janvier","février","mars","avril","mai","juin","juillet","août","septembre","octobre","novembre","décembre"]
    y, mo = aaaa_mm.split("-"); return f"{m[int(mo)-1]} {y}"
def avis_google_pour(agence, metier=None, n=2, exclure=()):
    """Sélection d'avis réels : d'abord la fiche de l'agence et le métier demandé, puis le métier sur les autres fiches, puis les avis généraux de la fiche."""
    pris, vus = [], set(exclure)
    def ajoute(cands):
        for a in cands:
            if len(pris) >= n: return
            k = (a["auteur"], a["texte"][:30])
            if k in vus: continue
            vus.add(k); pris.append(a)
    if metier:
        ajoute([a for a in AVIS_GOOGLE if a["agence"] == agence["cle"] and a["metier"] == metier])
        ajoute([a for a in AVIS_GOOGLE if a["metier"] == metier])
    ajoute([a for a in AVIS_GOOGLE if a["agence"] == agence["cle"] and a["metier"] is None])
    ajoute([a for a in AVIS_GOOGLE if a["metier"] is None])
    ajoute([a for a in AVIS_GOOGLE if a["agence"] == agence["cle"]])
    return pris
def avis_metier(agence, t, n, titre_metier, titre_general):
    """Bloc d'avis pour un métier ; si aucun avis ne concerne ce métier (ex. serrurerie), titre général."""
    items = avis_google_pour(agence, t["cle"], n)
    titre = titre_metier if any(a["metier"] == t["cle"] for a in items) else titre_general
    return avis_block(items, titre, agence, min(n, 3))
def avis_card(a):
    ag = AGENCE_BY_KEY[a["agence"]]
    return f'<div class="avis"><div class="st" aria-label="5 étoiles sur 5">★★★★★</div><p>« {esc(a["texte"])} »</p><div class="qui">{esc(a["auteur"])}<span>Avis Google · fiche {esc(ag["nom"])} · {mois_fr(a["date"])}</span></div></div>'
def avis_block(items, titre, agence, cols=None):
    if not items: return ""
    cols = cols or min(len(items), 3)
    cards = "".join(avis_card(a) for a in items)
    return f'<h2>{titre}</h2><p>Avis publiés par nos clients sur Google, repris tels quels (texte et notation inchangés). <a href="{maps(agence)}" target="_blank" rel="noopener">Lire tous les avis de la fiche {esc(agence["nom"])}</a> ou <a href="avis-clients.html">voir nos avis par agence</a>.</p><div class="avis-wrap c{cols}">{cards}</div>'

def tarifs_block(t):
    cards = "".join(f'<div class="tarif"><div><b>{esc(n)}</b><p>{esc(d)}</p></div><div class="px"><b>{esc(p)}</b><small>{esc(u)}</small></div></div>' for _,n,d,p,u in t["prestations"])
    return f'<div class="tarifs">{cards}</div><p class="note">Tarif minimum d\'intervention : 110 € HT (TVA à 10 % ou 20 % selon la nature des travaux et l\'ancienneté du logement). Autres prix indicatifs 2026. Majoration possible la nuit, le week-end et les jours fériés, toujours annoncée avant le déplacement. Tarif définitif communiqué avant toute intervention.</p>'

# ---------------------------------------------------------------- ACCUEIL
def page_index():
    faq_htm, faq_ld = faq_block([
        ("Quels métiers Atelier PACA couvre-t-il à Antibes et sur la Côte d'Azur ?","Plombier, chauffagiste, installateur de climatisation, électricien, technicien volets roulants et serrurier : six métiers, une seule équipe basée à Antibes. Un seul numéro et une seule facture, y compris quand un chantier mêle plusieurs métiers, par exemple une salle de bain ou une pompe à chaleur."),
        ("En combien de temps intervient un plombier ou un électricien à Antibes ?","Sous 48 h pour une intervention classique, souvent le jour même en urgence : fuite d'eau, panne de courant, chaudière en sécurité, porte claquée, volet bloqué ouvert. L'astreinte fonctionne 24h/24 et 7j/7, et le prix est annoncé au téléphone avant le déplacement."),
        ("Faites-vous le dépannage à Cagnes-sur-Mer, Cannes, Nice ou Villeneuve-Loubet ?","Oui. Nos agences d'Antibes, Juan-les-Pins, Cagnes-sur-Mer et Le Cannet couvrent toute la bande côtière de Mandelieu à Nice et Saint-Laurent-du-Var, l'arrière-pays jusqu'à Grasse et Vence, et le Var est : Fréjus, Saint-Raphaël et le pays de Fayence. Chaque ville a sa page avec nos délais."),
        ("Le devis est-il vraiment gratuit ?","Oui, le devis et la visite technique sont gratuits et sans engagement, pour une climatisation, une pompe à chaleur, un tableau électrique ou une salle de bain. Pour un dépannage, le prix est annoncé avant l'intervention, majoration de nuit ou de week-end comprise."),
        ("Combien coûte une intervention Atelier PACA ?","Le tarif minimum d'intervention est de 110 € HT (dépannage simple, pose de prise, entretien de clim ou de chaudière). Les autres prix sont indicatifs et affichés sur chaque page métier ; le tarif définitif est toujours communiqué avant de commencer."),
        ("Vos travaux sont-ils garantis ?","Oui : garantie décennale sur les travaux, matériel de grandes marques (Daikin, Mitsubishi Electric, Atlantic, Somfy, Legrand), facture détaillée utilisable pour votre assurance et une équipe joignable après l'intervention."),
    ], cls="g2")
    ld = [ld_business(), {"@context":"https://schema.org","@type":"WebSite","@id":SITE+"#site","url":SITE,"name":"Atelier PACA","inLanguage":"fr-FR","publisher":{"@id":SITE+"#organisation"}}, faq_ld]
    metiers = "".join(f'''<a class="metier" href="{t["page"]}"><img src="images/{t["img"]}-480.webp" srcset="images/{t["img"]}-480.webp 480w, images/{t["img"]}.webp 900w" sizes="(max-width:560px) 100vw, (max-width:900px) 50vw, 380px" alt="{esc(t["alt"])}" loading="lazy" width="743" height="586">
<div class="in"><div class="ic">{ICO_METIER[t["cle"]]}</div><h3>{t["nom"]}</h3><p>{t["desc_court"]}</p></div><span class="go">{ICO["arrow"]}</span></a>''' for t in TRADES)
    # Accueil : 3 avis Google réels récents (clim Antibes, plomberie Le Cannet, électricité Cagnes)
    accueil = [a for a in AVIS_GOOGLE if a["auteur"] in ("Lial H.", "Merissa G.", "Foued B.")]
    avis = "".join(avis_card(a) for a in accueil)
    fiches = "".join(f'<div class="fiche"><b>{a["nom"]}</b><span>{a["adresse"]}, {a["cp"]} {a["ville"]}</span><span>{a["note"]}/5 · {a["avis"]} avis</span><div class="l"><a href="{maps(a)}" target="_blank" rel="noopener">Voir la fiche</a><a href="{avis_url(a)}" target="_blank" rel="noopener">Laisser un avis</a></div></div>' for a in AGENCES)
    def hubs_replies(vs, n_visibles, label):
        """Accueil : les villes principales visibles, le reste replié (liens toujours dans le HTML pour le référencement)."""
        a = lambda v: f'<a href="depannage-{v["slug"]}.html">{v["nom"]}</a>'
        vis, rest = vs[:n_visibles], vs[n_visibles:]
        htm = "".join(a(v) for v in vis)
        if rest:
            htm += f'</div><details class="plus"><summary>Voir les {len(vs)} villes {label}</summary><div class="chips">' + "".join(a(v) for v in rest) + '</div></details><div class="chips" hidden>'
        return htm
    hubs06 = hubs_replies(VILLES_06, 9, "des Alpes-Maritimes")
    hubs83 = hubs_replies(VILLES_83, 3, "du Var est")
    body = header("index.html") + f'''
<main>
<section class="hero"><div class="wrap">
<div>
<span class="badge247"><i></i> Dépannage 24h/24 · 7j/7 — Antibes, Alpes-Maritimes et Var est</span>
<h1><span class="pre">Plombier, chauffagiste, électricien à Antibes</span><span class="neon">Un seul numéro</span> pour toute votre maison.</h1>
<p class="lead">Plomberie, chauffage, climatisation, électricité, volets roulants et serrurerie : une équipe locale basée à Antibes<span class="plus">, avec des agences à Juan-les-Pins, Cagnes-sur-Mer et Le Cannet, qui dépanne, entretient et installe dans les Alpes-Maritimes et le Var est</span>. Intervention sous 48 h, urgences 24h/24, devis gratuit.</p>
<div class="btns"><a href="{E["tel_href"]}" class="btn btn-rouge">{ICO["tel"]} {E["tel"]}</a><a href="contact.html#devis" class="btn btn-bleu">{ICO["doc"]} Devis gratuit</a></div>
<div class="proof"><span>{ICO["star"]}<b>{E["note"]}/5</b> — {E["avis"]} avis Google</span><span>{ICO["shield"]}<b>Garantie décennale</b></span><span>{ICO["clock"]}<b>Prix annoncé</b> avant intervention</span></div>
</div>
<div style="position:relative"><div class="frame auto"><img src="images/hero-equipe.webp" srcset="images/hero-equipe-480.webp 480w, images/hero-equipe.webp 936w" sizes="(max-width:900px) 100vw, 540px" alt="Technicien Atelier PACA devant le camion d'intervention, baie de Cannes" width="936" height="638" fetchpriority="high" decoding="sync"><div class="hero-pictos" aria-hidden="true"><span><i>{ICO_METIER["plomberie"]}</i>Plomberie</span><span><i>{ICO_METIER["chauffage"]}</i>Chauffage</span><span><i>{ICO_METIER["climatisation"]}</i>Climatisation</span><span><i>{ICO_METIER["electricite"]}</i>Électricité</span><span><i>{ICO_METIER["volets"]}</i>Volets</span><span><i>{ICO_METIER["serrurerie"]}</i>Serrurerie</span></div></div></div>
</div></section>

<section class="wrap"><div class="chiffres">
<div class="chiffre"><b>{E["interventions"]}+</b><span>interventions réalisées depuis {E["depuis"]}</span></div>
<div class="chiffre"><b>{E["note"]}/5</b><span>sur {E["avis"]} avis Google vérifiés</span></div>
<div class="chiffre"><b>48 h</b><span>délai d'intervention, moins en urgence</span></div>
<div class="chiffre"><b>10 ans</b><span>de garantie décennale sur les travaux</span></div>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-h"><p class="kicker">Nos métiers</p><h2>Dépannage et travaux dans les Alpes-Maritimes : six métiers, une seule équipe</h2><p>Chaque technicien est spécialisé dans son métier : plombier, chauffagiste, frigoriste, électricien, technicien volets, serrurier. Ensemble, ils couvrent tout ce qui peut tomber en panne chez vous, sans que vous ayez à coordonner trois artisans.</p></div>
<div class="metiers">{metiers}</div>
</div></section>

<section class="sec" style="padding-top:0"><div class="wrap"><div class="offres">
<div class="offre r"><div><span class="tag">Avant l'hiver</span><h3>Entretien de chaudière avec attestation</h3><p>Nettoyage, réglage, contrôle sécurité et CO. Obligatoire chaque année pour le gaz, et la meilleure assurance contre la panne du premier soir froid.</p></div><div class="prix"><b>110 € HT</b><small>à partir de</small><a href="chauffage.html" class="btn btn-rouge btn-sm">Programmer l'entretien</a></div></div>
<div class="offre b"><div><span class="tag">Toute l'année</span><h3>Contrat d'entretien clim ou chaudière</h3><p>Visite annuelle programmée, dépannage sous 48 h, 10 % de remise sur les pièces détachées. Vous n'y pensez plus, on s'en occupe.</p></div><div class="prix"><b>1 visite</b><small>par an, programmée</small><a href="contrat-entretien.html" class="btn btn-bleu btn-sm">Voir les contrats</a></div></div>
</div>
<div class="encart" style="margin-top:18px"><div><b>Syndic, agence immobilière, commerce ou bureaux ?</b><span>Six métiers, un interlocuteur, contrats d'entretien multi-sites, facture détaillée par immeuble, astreinte 24h/24.</span></div><a href="professionnels-syndics.html" class="btn btn-bleu btn-sm">Offre professionnelle</a></div>
</div></section>

<section class="sec" style="padding-top:0"><div class="wrap"><div class="pourquoi">
<div><div class="sec-h"><p class="kicker">Pourquoi Atelier PACA</p><h2>Pourquoi choisir un artisan d'Antibes plutôt qu'un dépanneur anonyme</h2></div>
<div class="raisons">
<div class="raison"><div class="ic">{ICO["one"]}</div><div><b>Un numéro, six métiers</b><p>Fuite d'eau, panne de chauffage, clim en panne, tableau électrique, volet bloqué, porte claquée : le même numéro, la même équipe, et une seule facture quand plusieurs métiers sont nécessaires.</p></div></div>
<div class="raison"><div class="ic">{ICO["euro"]}</div><div><b>Le prix avant, pas après</b><p>Tarif annoncé au téléphone ou sur devis avant toute intervention, nuit et week-end compris. Tarif minimum 110 € HT, majoration éventuelle dite avant le déplacement. Pas de surprise à la fin.</p></div></div>
<div class="raison"><div class="ic">{ICO["pin"]}</div><div><b>Une entreprise d'ici, depuis {E["depuis"]}</b><p>Siège à Antibes, agences à Juan-les-Pins, Cagnes-sur-Mer et Le Cannet, plus de {E["interventions"]} interventions : nos techniciens connaissent les copropriétés, les villas, l'air salin et l'eau calcaire de la côte.</p></div></div>
<div class="raison"><div class="ic">{ICO["shield"]}</div><div><b>Garantie décennale et grandes marques</b><p>Daikin, Mitsubishi Electric, Atlantic, Somfy, Legrand, Schneider : du matériel qui dure, posé par des techniciens formés, garanti 10 ans, avec une facture détaillée pour votre assurance.</p></div></div>
</div></div>
<div><div class="frame auto"><img src="images/hero-nuit.webp" srcset="images/hero-nuit-480.webp 480w, images/hero-nuit.webp 529w" sizes="(max-width:900px) 100vw, 520px" alt="Technicien Atelier PACA en dépannage de nuit sur une climatisation, astreinte 24h/24 à Antibes" loading="lazy" width="529" height="774" style="max-height:560px;object-fit:cover"></div></div>
</div></div></section>

<section class="sec clair" id="avis"><div class="wrap">
<div class="sec-h c"><p class="kicker" style="justify-content:center">Avis clients</p><h2>{E["note"]}/5 sur {E["avis"]} avis Google</h2><p>Quatre fiches Google, plus de 450 avis au total, repris tels quels. Les avis sont publics et vérifiables sur chaque fiche. <a href="avis-clients.html">Voir nos avis par agence</a>.</p></div>
<div class="avis-wrap">{avis}</div>
<div class="fiches">{fiches}</div>
<div class="sec-h" style="margin-top:56px"><p class="kicker">Comment ça se passe</p><h2>Votre dépannage ou vos travaux en quatre étapes</h2></div>
<div class="etapes">
<div class="etape"><span class="n">1</span><b>Vous appelez ou écrivez</b><p>Téléphone, WhatsApp ou formulaire. Un technicien vous répond sous 2 h en journée, immédiatement pour une urgence, et vous donne les premiers gestes à faire.</p></div>
<div class="etape"><span class="n">2</span><b>Diagnostic et prix annoncé</b><p>Le technicien évalue le besoin et fixe un prix ferme, validé avant de commencer. Pour les travaux, visite technique et devis gratuits sous 24 h.</p></div>
<div class="etape"><span class="n">3</span><b>Intervention soignée</b><p>Pièces courantes en stock pour finir en une visite, protection des lieux, travail dans les règles de l'art, chantier laissé propre.</p></div>
<div class="etape"><span class="n">4</span><b>Facture et garantie</b><p>Facture détaillée pour votre assurance ou votre syndic, garantie décennale, et une équipe joignable après l'intervention.</p></div>
</div></div></section>

<section class="sec"><div class="wrap">
<div class="sec-h"><p class="kicker">Zone d'intervention</p><h2>Dépannage à Antibes, Cagnes-sur-Mer, Cannes, Nice et dans tout le 06</h2><p>Plombier, chauffagiste, électricien, climatisation, volets et serrurier dans toutes les communes ci-dessous, avec le même numéro et les mêmes tarifs, de Mandelieu à Menton et jusqu'au Var est. Choisissez votre ville pour voir nos délais et nos prestations sur place.</p></div>
<div class="villes"><div><h3>{ICO["pin"]} Alpes-Maritimes <small>(06)</small></h3><div class="chips">{hubs06}</div></div><div><h3>{ICO["pin"]} Var est <small>(83)</small></h3><div class="chips">{hubs83}</div></div></div>
</div></section>

<section class="sec" style="padding-top:0"><div class="wrap"><p class="kicker">Vos questions</p>{faq_htm}</div></section>

<section class="sec" id="devis" style="padding-top:0"><div class="wrap">
<div class="sec-h"><p class="kicker">Contact</p><h2>Demandez un devis gratuit à Antibes ou près de chez vous</h2><p>Réponse sous 2 h en journée, visite technique gratuite. Pour un dépannage urgent, appelez directement : {E["tel"]}.</p></div>
<div class="contact">{coord_block()}{form_devis()}</div>
</div></section>
</main>
''' + footer()
    write("index.html", head("Plombier, chauffagiste, électricien Antibes | Atelier PACA",
          "Atelier PACA, Antibes : plomberie, chauffage, clim, électricité, volets et serrurerie dans le 06 et le Var. Un seul numéro, devis gratuit, 4,9/5 sur 178 avis.",
          "", ld, preload="images/hero-equipe.webp") + body, "1.0", "weekly")

# ---------------------------------------------------------------- PAGES MÉTIER
def page_metier(t):
    c_htm, c_ld = crumb([("Accueil","index.html"),(t["nom"],t["page"])])
    faq_htm, faq_ld = faq_block(t["faq"], f"Questions fréquentes — {t['nom'].lower()}")
    svc_ld = {"@context":"https://schema.org","@type":"Service","name":f"{t['nom']} — Atelier PACA","serviceType":t["nom"],"provider":{"@id":SITE+"#organisation"},"areaServed":[{"@type":"AdministrativeArea","name":"Alpes-Maritimes"},{"@type":"AdministrativeArea","name":"Var"}],"url":SITE+t["page"],
              "offers":[{"@type":"Offer","name":n,"priceCurrency":"EUR","price":p.replace(" €","").replace(" ","").replace("Surdevis","0"),"description":d} for _,n,d,p,u in t["prestations"] if "€" in p]}
    ld = [ld_business(t["schema"]), svc_ld, c_ld, faq_ld]
    services = "".join(f'<li>{esc(s)}</li>' for s in t["services"])
    exp = "".join(f'<div class="t"><b>{esc(a)}</b><p>{esc(b)}</p></div>' for a,b in t["expertise"])
    marques = "".join(f'<span>{esc(m)}</span>' for m in t["marques"])
    autres = "".join(f'<a href="{x["page"]}">{x["nom"]}</a>' for x in TRADES if x is not t)
    body = header(t["page"]) + f'''
<main>
<section class="hero hero-mini"><div class="wrap">{c_htm}<p class="kicker">{t["accroche"]}</p><h1>{t["h1"]}</h1>
<p class="lead">{esc(t["intro"][0])}</p>
<div class="btns" style="margin-top:22px"><a href="{E["tel_href"]}" class="btn btn-rouge">{ICO["tel"]} {E["tel"]}</a><a href="contact.html#devis" class="btn btn-bleu">{ICO["doc"]} Devis gratuit</a></div>
<div class="proof"><span>{ICO["star"]}<b>{E["note"]}/5</b> — {E["avis"]} avis</span><span>{ICO["clock"]}<b>Sous 48 h</b>, moins en urgence</span><span>{ICO["shield"]}<b>Décennale</b></span></div>
</div></section>
<section class="sec" style="padding-top:28px"><div class="wrap"><div class="page">
<div class="main">
<div class="photo-p"><img src="images/{t["img"]}.webp" srcset="images/{t["img"]}-480.webp 480w, images/{t["img"]}.webp 900w" sizes="(max-width:960px) 100vw, 780px" alt="{esc(t["alt"])}, Alpes-Maritimes" width="886" height="481" loading="eager" decoding="async"></div>
<h2>Tarifs {t["nom"].lower()} dans les Alpes-Maritimes et le Var</h2>
{tarifs_block(t)}
<h2>Dépannage {t["nom"].lower()} et travaux : ce que nous faisons</h2>
<p>{esc(t["intro"][1])}</p>
<ul class="liste">{services}</ul>
<h2>Pourquoi choisir Atelier PACA comme {t["metier_min"]}</h2>
<div class="trio">{exp}</div>
<h2>Marques installées et dépannées</h2>
<div class="marques">{marques}</div>
{avis_metier(AGENCES[0], t, 3, f"Avis Google de nos clients en {t['nom'].lower()}", "Avis Google de nos clients")}
<div class="encart"><div><b>Besoin d'un autre métier sur le même chantier ?</b><span>Nos plombiers, électriciens, chauffagistes et frigoristes travaillent ensemble : un interlocuteur, une facture.</span></div><a href="contact.html#devis" class="btn btn-rouge btn-sm">Demander un devis</a></div>
{faq_htm}
<h2>{t["metier"]} à Antibes, Cagnes-sur-Mer, Cannes, Nice… ville par ville</h2>
<p>Retrouvez nos délais, nos tarifs et nos conseils adaptés à votre commune : plus de 50 villes dans les Alpes-Maritimes, de Mandelieu à Menton, et dans le Var est. Dépannage {t["nom"].lower()} sous 48 h, plus vite en urgence.</p>
{chips_villes(t["prefix"])}
</div>
<aside class="side">
<div class="card"><h3>Appeler un {t["metier_min"]}</h3><p>Astreinte 24h/24, prix annoncé avant le déplacement, devis gratuit pour les travaux.</p><a href="{E["tel_href"]}" class="btn btn-rouge">{ICO["tel"]} {E["tel"]}</a><a href="{E["wa"]}" class="btn btn-wa" target="_blank" rel="noopener">{ICO["wa"]} WhatsApp</a><a href="contact.html#devis" class="btn btn-bleu">{ICO["doc"]} Devis gratuit</a></div>
<div class="card"><h3>Atelier PACA</h3><p class="nap"><b>Siège Antibes</b><br>{E["adresse"]}<br>{E["cp"]} {E["ville"]}<br>{E["email"]}</p><p class="nap">{E["note"]}/5 — {E["avis"]} avis Google<br>Depuis {E["depuis"]} · {E["interventions"]}+ interventions</p></div>
<div class="card"><h3>Autres métiers</h3><div class="liens">{autres}<a href="urgence-depannage-24h.html">Urgence 24h/24</a><a href="contrat-entretien.html">Contrats d'entretien</a></div></div>
</aside>
</div></div></section>
{cta_final(f"Un projet ou une panne en {t['nom'].lower()} ?")}
</main>
''' + footer()
    write(t["page"], head(t["title"], t["meta"], t["page"], ld, og_img=f"images/og-{t['img']}.jpg") + body, "0.9", "monthly")

# ---------------------------------------------------------------- PAGES MÉTIER × VILLE
def page_metier_ville(t, v):
    fn = f'{t["prefix"]}-{v["slug"]}.html'
    depuis = "à deux pas de notre siège, chemin des Autrichiens" if v["slug"] == "antibes" else f'à {v["minutes"]} de notre siège d\'Antibes'
    ctx = {"ville": v["nom"], "cp": v["cp"], "minutes": v["minutes"], "depuis": depuis,
           "q0": v["quartiers"][0], "q1": v["quartiers"][1] if len(v["quartiers"]) > 1 else "ses environs", "habitat": v["habitat"]}
    ctx["de_q0"] = de_(ctx["q0"]); ctx["a_q1"] = a_(ctx["q1"])
    agence = next((a for a in AGENCES if a["cle"] == v.get("agence")), None)
    c_htm, c_ld = crumb([("Accueil","index.html"),(t["nom"],t["page"]),(v["nom"],fn)])
    faq_htm, faq_ld = faq_block(t["faq_ville"], f"Questions fréquentes — {t['nom'].lower()} à {v['nom']}", ctx)
    svc_ld = {"@context":"https://schema.org","@type":"Service","name":f"{t['nom']} à {v['nom']}","serviceType":t["nom"],"provider":{"@id":SITE+"#organisation"},"areaServed":{"@type":"City","name":v["nom"],"postalCode":v["cp"]},"url":SITE+fn,
              "offers":[{"@type":"Offer","name":n,"priceCurrency":"EUR","price":p.replace(" €","").replace(" ","").replace("Surdevis","0"),"description":d,"areaServed":{"@type":"City","name":v["nom"]}} for _,n,d,p,u in t["prestations"] if "€" in p]}
    ld = [ld_business(t["schema"], agence), svc_ld, c_ld, faq_ld]
    quartiers = ", ".join(v["quartiers"])
    services = "".join(f'<li>{esc(s)}</li>' for s in t["services"])
    autres = "".join(f'<a href="{x["prefix"]}-{v["slug"]}.html">{x["nom"]} {v["nom"]}</a>' for x in TRADES if x is not t)
    voisines = "".join(f'<a href="{t["prefix"]}-{s}.html">{VILLE_BY_SLUG[s]["nom"]}</a>' for s in v["voisines"])
    if agence:
        local = f'<div class="loc"><div class="l"><b>Agence Atelier PACA — {agence["nom"]}</b><span>{agence["adresse"]}, {agence["cp"]} {agence["ville"]} · {agence["note"]}/5 sur {agence["avis"]} avis · <a href="{maps(agence)}" target="_blank" rel="noopener">voir la fiche Google</a></span></div><div class="l"><b>Délai à {v["nom"]}</b><span>Intervention sous 48 h, souvent le jour même en urgence. Siège et stock à Antibes.</span></div></div>'
    else:
        local = f'<div class="loc"><div class="l"><b>Depuis Antibes</b><span>{v["nom"]} est à {v["minutes"]} de notre siège (48 chemin des Autrichiens). Stock de pièces et matériel embarqué.</span></div><div class="l"><b>Délai à {v["nom"]}</b><span>{"Intervention sous 48 h, souvent le jour même en urgence." if v["prio"] or v["dept"]=="06" else "Intervention sous 48 h ; urgences selon la disponibilité des équipes mobiles."}</span></div></div>'
    loc_p = "".join(f'<p>{esc(x)}</p>' for x in local_paras(v))
    prio_txt = f'<h2>Atelier PACA, {t["metier_min"]} à {v["nom"]} depuis {E["depuis"]}</h2>{loc_p or "<p>" + esc(v["intro"]) + "</p>"}'
    intro_v = "".join(f'<p>{esc(x.format(**ctx))}</p>' for x in t["intro_ville"])
    body = header(t["page"]) + f'''
<main>
<section class="hero hero-mini"><div class="wrap">{c_htm}<p class="kicker">{t["sous_ville"]}</p><h1>{t["h1_ville"].format(**ctx)}</h1>
<p class="lead">{esc(t["metier"])} à {v["nom"]} ({v["cp"]}) : {t["accroche"].lower()} par l'équipe Atelier PACA, {depuis}. Dépannage sous 48 h, plus vite en urgence, prix annoncé avant intervention, devis gratuit.</p>
<div class="btns" style="margin-top:22px"><a href="{E["tel_href"]}" class="btn btn-rouge">{ICO["tel"]} {E["tel"]}</a><a href="contact.html#devis" class="btn btn-bleu">{ICO["doc"]} Devis gratuit</a></div>
<div class="proof"><span>{ICO["star"]}<b>{E["note"]}/5</b> — {E["avis"]} avis</span><span>{ICO["pin"]}<b>{v["nom"]}</b> et {ctx["q1"]}</span><span>{ICO["shield"]}<b>Décennale</b></span></div>
</div></section>
<section class="sec" style="padding-top:28px"><div class="wrap"><div class="page">
<div class="main">
<div class="photo-p"><img src="images/{t["img"]}.webp" srcset="images/{t["img"]}-480.webp 480w, images/{t["img"]}.webp 900w" sizes="(max-width:960px) 100vw, 780px" alt="{esc(t["alt"])}, intervention à {esc(v["nom"])}" width="886" height="481" loading="eager" decoding="async"></div>
<h2>{esc(t["h2_ville"].format(**ctx))}</h2>
{intro_v}
<ul class="liste">{services}</ul>
{local}
{prio_txt}
<h2>Tarifs {t["nom"].lower()} à {v["nom"]}</h2>
{tarifs_block(t)}
{avis_metier(agence_proche(v), t, 2, f"Avis Google — {t['nom'].lower()} près de {v['nom']}", f"Avis Google de nos clients près de {v['nom']}")}
<h3>Quartiers couverts à {v["nom"]}</h3>
<p>Nous intervenons dans toute la commune : {esc(quartiers)}. {esc(t["habitat_ville"].format(**ctx))}</p>
{faq_htm}
<h2>Les autres métiers Atelier PACA à {v["nom"]}</h2>
<p>Un seul numéro pour toute la maison : si votre {t["nom"].lower()} s'accompagne d'un autre besoin, la même équipe s'en charge.</p>
<div class="chips">{autres}<a href="depannage-{v["slug"]}.html" class="on">Tout le dépannage à {v["nom"]}</a></div>
<h3>{t["metier"]} dans les villes voisines de {v["nom"]}</h3>
<div class="chips">{voisines}<a href="{t["page"]}">{t["metier"]} dans tout le 06 et le Var</a></div>
</div>
<aside class="side">
<div class="card"><h3>{t["metier"]} à {v["nom"]}</h3><p>Astreinte 24h/24, prix annoncé avant le déplacement, devis gratuit.</p><a href="{E["tel_href"]}" class="btn btn-rouge">{ICO["tel"]} {E["tel"]}</a><a href="{E["wa"]}" class="btn btn-wa" target="_blank" rel="noopener">{ICO["wa"]} WhatsApp</a><a href="contact.html#devis" class="btn btn-bleu">{ICO["doc"]} Devis gratuit</a></div>
<div class="card"><h3>{"Agence " + agence["nom"] if agence else "Atelier PACA — siège"}</h3><p class="nap">{(agence["adresse"] + "<br>" + agence["cp"] + " " + agence["ville"]) if agence else (E["adresse"] + "<br>" + E["cp"] + " " + E["ville"])}<br><a href="{maps(agence or AGENCES[0])}" target="_blank" rel="noopener">Itinéraire et avis Google</a></p><p class="nap">{(agence or AGENCES[0])["note"]}/5 — {(agence or AGENCES[0])["avis"]} avis Google sur cette fiche<br>Depuis {E["depuis"]} · {E["interventions"]}+ interventions</p></div>
<div class="card"><h3>À lire</h3><div class="liens">{"".join(f'<a href="{a["slug"]}">{esc(a["titre"])}</a>' for a in ARTICLES)}</div></div>
</aside>
</div></div></section>
{cta_final(f"{t['metier']} à {v['nom']} : on vous rappelle sous 2 h", "Appelez, écrivez sur WhatsApp ou laissez vos coordonnées : un technicien vous répond avec un prix clair.")}
</main>
''' + footer()
    tt = t["title_ville"].format(**ctx)
    if len(tt) > 60: tt = t["title_court"].format(**ctx)
    write(fn, head(tt, t["meta_ville"].format(**ctx), fn, ld, og_img=f"images/og-{t['img']}.jpg") + body, "0.8" if v["prio"] else "0.6", "monthly")

# ---------------------------------------------------------------- HUB VILLE
def page_hub(v):
    fn = f'depannage-{v["slug"]}.html'
    agence = next((a for a in AGENCES if a["cle"] == v.get("agence")), None)
    c_htm, c_ld = crumb([("Accueil","index.html"),("Villes","depannage-antibes.html"),(v["nom"],fn)])
    depuis = "notre siège et nos stocks sont à Antibes même, chemin des Autrichiens" if v["slug"] == "antibes" else f"{v['nom']} est à {v['minutes']} de notre siège d'Antibes"
    faq_htm, faq_ld = faq_block([
        (f"Quel artisan appeler pour un dépannage à {v['nom']} ?", f"Le même numéro pour tout : plombier, chauffagiste, climatisation, électricien, volets roulants et serrurier à {v['nom']}, en dépannage, entretien et installation. Un technicien de garde répond 24h/24 et annonce le prix avant de se déplacer."),
        (f"Sous quel délai intervenez-vous à {v['nom']} ?", f"Sous 48 h pour une intervention classique ; plus vite en urgence (fuite d'eau, panne de courant, porte claquée, chaudière en sécurité) grâce à l'astreinte 24h/24 : {depuis}, et nos équipes mobiles ont les pièces courantes en stock."),
        (f"Le devis est-il gratuit à {v['nom']} ?", f"Oui, devis et visite technique sont gratuits et sans engagement à {v['nom']}, pour une climatisation, une pompe à chaleur, un tableau électrique ou une salle de bain. Pour un dépannage, le prix est annoncé avant l'intervention, nuit et week-end compris."),
        (f"Combien coûte un dépannage à {v['nom']} ?", f"Le tarif minimum d'intervention est de 110 € HT, pour un dépannage simple, une petite réparation ou un entretien. Les autres prix indicatifs sont détaillés sur chaque page métier de {v['nom']} ; le tarif définitif est toujours communiqué avant de commencer, majoration éventuelle comprise."),
    ], f"Questions fréquentes — dépannage à {v['nom']}")
    ld = [ld_business(None, agence), c_ld, faq_ld]
    hub = "".join(f'<a href="{t["prefix"]}-{v["slug"]}.html"><span class="ic">{ICO_METIER[t["cle"]]}</span><span><b>{t["metier"]} {v["nom"]}</b><span>{t["accroche"]}</span></span></a>' for t in TRADES)
    voisines = "".join(f'<a href="depannage-{s}.html">Dépannage {VILLE_BY_SLUG[s]["nom"]}</a>' for s in v["voisines"])
    local = "".join(f'<p>{esc(x)}</p>' for x in local_paras(v))
    agence_htm = f'<div class="loc"><div class="l"><b>Agence Atelier PACA — {agence["nom"]}</b><span>{agence["adresse"]}, {agence["cp"]} {agence["ville"]} · {agence["note"]}/5 sur {agence["avis"]} avis · <a href="{maps(agence)}" target="_blank" rel="noopener">fiche Google</a> · <a href="{avis_url(agence)}" target="_blank" rel="noopener">laisser un avis</a></span></div><div class="l"><b>Quartiers</b><span>{esc(", ".join(v["quartiers"]))}</span></div></div>' if agence else f'<div class="loc"><div class="l"><b>Depuis notre siège d\'Antibes</b><span>{v["nom"]} est à {v["minutes"]}. Équipes mobiles avec stock embarqué.</span></div><div class="l"><b>Quartiers</b><span>{esc(", ".join(v["quartiers"]))}</span></div></div>'
    body = header("depannage-antibes.html") + f'''
<main>
<section class="hero hero-mini"><div class="wrap">{c_htm}<p class="kicker">Dépannage, entretien, installation</p><h1>Dépannage et artisan à {v["nom"]} : six métiers, un seul numéro</h1>
<p class="lead">Plombier, chauffagiste, climatisation, électricien, volets roulants et serrurier à {v["nom"]} ({v["cp"]}), 24h/24 pour les urgences. {esc(v["intro"])}</p>
<div class="btns" style="margin-top:22px"><a href="{E["tel_href"]}" class="btn btn-rouge">{ICO["tel"]} {E["tel"]}</a><a href="contact.html#devis" class="btn btn-bleu">{ICO["doc"]} Devis gratuit</a></div>
<div class="proof"><span>{ICO["star"]}<b>{E["note"]}/5</b> — {E["avis"]} avis</span><span>{ICO["clock"]}<b>Sous 48 h</b>, moins en urgence</span><span>{ICO["shield"]}<b>Décennale</b></span></div>
</div></section>
<section class="sec" style="padding-top:28px"><div class="wrap"><div class="page">
<div class="main">
<div class="photo-p"><img src="images/equipe-camion.webp" srcset="images/equipe-camion-480.webp 480w, images/equipe-camion.webp 904w" sizes="(max-width:960px) 100vw, 780px" alt="Équipe Atelier PACA et camion d'intervention : dépannage plomberie, chauffage, climatisation et électricité à {esc(v["nom"])}" width="904" height="459" loading="eager" decoding="async"></div>
<h2>Dépannage à {v["nom"]} : choisissez votre métier</h2>
<p>Fuite d'eau, chaudière en panne, clim qui ne refroidit plus, panne de courant, volet bloqué, porte claquée : un seul numéro, {E["tel"]}, et le prix annoncé avant le déplacement.</p>
<div class="hub">{hub}</div>
{agence_htm}
<h2>Atelier PACA à {v["nom"]} : ce que nous y faisons</h2>
{local}
<p>Habitat le plus fréquent à {v["nom"]} : {esc(v["habitat"])}. Nos techniciens adaptent le matériel aux contraintes locales (air salin, eau calcaire, copropriétés, résidences secondaires) et arrivent avec les pièces courantes pour finir en une visite.</p>
<h2>Pourquoi appeler Atelier PACA à {v["nom"]}</h2>
<ul class="liste"><li>Intervention sous 48 h, plus vite en urgence (astreinte 24h/24, 7j/7)</li><li>Prix annoncé avant intervention, tarif minimum 110 € HT, devis gratuit pour les travaux</li><li>Garantie décennale, grandes marques, facture détaillée pour votre assurance ou votre syndic</li><li>Entreprise d'Antibes depuis {E["depuis"]} : plus de {E["interventions"]} interventions, {E["note"]}/5 sur {E["avis"]} avis Google</li></ul>
{avis_block(avis_google_pour(agence_proche(v), None, 3), f"Avis Google de nos clients près de {v['nom']}", agence_proche(v))}
{faq_htm}
<h3>Dépannage dans les villes voisines de {v["nom"]}</h3><div class="chips">{voisines}</div>
</div>
<aside class="side">
<div class="card"><h3>Dépannage à {v["nom"]}</h3><p>Un technicien vous répond et annonce le prix avant de se déplacer. Devis gratuit pour les travaux.</p><a href="{E["tel_href"]}" class="btn btn-rouge">{ICO["tel"]} {E["tel"]}</a><a href="{E["wa"]}" class="btn btn-wa" target="_blank" rel="noopener">{ICO["wa"]} WhatsApp</a><a href="contact.html#devis" class="btn btn-bleu">{ICO["doc"]} Devis gratuit</a></div>
<div class="card"><h3>Urgence</h3><p>Fuite, panne de chauffage, porte claquée, volet bloqué ouvert : l'astreinte fonctionne 24h/24.</p><div class="liens"><a href="urgence-depannage-24h.html">Dépannage urgent 24h/24</a><a href="contrat-entretien.html">Contrats d'entretien</a><a href="avis-clients.html">Avis clients</a></div></div>
</aside>
</div></div></section>
{cta_final(f"Un artisan à {v['nom']} ?")}
</main>
''' + footer()
    tt = f"Dépannage {v['nom']} : plombier, électricien | Atelier PACA"
    if len(tt) > 60: tt = f"Dépannage & artisan {v['nom']} | Atelier PACA"
    if len(tt) > 60: tt = f"Dépannage {v['nom']} | Atelier PACA"
    write(fn, head(tt, f"Dépannage et travaux à {v['nom']} ({v['cp']}) : plombier, chauffagiste, climatisation, électricien, volets, serrurier. 24h/24, un numéro, devis gratuit, 4,9/5.", fn, ld) + body, "0.8" if v["prio"] else "0.6", "monthly")

# ---------------------------------------------------------------- PAGES ANNEXES
def page_simple(fn, title, desc, h1, kicker, contenu, side=None, ld_extra=None, cta=True, prio="0.5", crumbs=None, lead=""):
    c_htm, c_ld = crumb(crumbs or [("Accueil","index.html"),(h1,fn)])
    ld = [ld_business(), c_ld] + (ld_extra or [])
    side = side or f'''<aside class="side"><div class="card"><h3>Besoin d'un artisan ?</h3><p>Astreinte 24h/24, prix annoncé avant le déplacement.</p><a href="{E["tel_href"]}" class="btn btn-rouge">{ICO["tel"]} {E["tel"]}</a><a href="{E["wa"]}" class="btn btn-wa" target="_blank" rel="noopener">{ICO["wa"]} WhatsApp</a><a href="contact.html#devis" class="btn btn-bleu">{ICO["doc"]} Devis gratuit</a></div>
<div class="card"><h3>Nos métiers</h3><div class="liens">{"".join(f'<a href="{t["page"]}">{t["nom"]}</a>' for t in TRADES)}</div></div></aside>'''
    body = header(fn) + f'''<main>
<section class="hero hero-mini"><div class="wrap">{c_htm}<p class="kicker">{kicker}</p><h1>{h1}</h1>{f'<p class="lead">{lead}</p>' if lead else ''}</div></section>
<section class="sec" style="padding-top:28px"><div class="wrap"><div class="page"><div class="main">{contenu}</div>{side}</div></div></section>
{cta_final() if cta else ""}
</main>''' + footer()
    write(fn, head(title, desc, fn, ld) + body, prio)

def pages_annexes():
    # Urgence
    faq_htm, faq_ld = faq_block([
        ("Qu'est-ce qui est considéré comme une urgence ?","Une fuite d'eau que vous ne pouvez pas stopper, une absence totale de chauffage ou d'eau chaude en hiver, une panne électrique générale ou une odeur de brûlé, une porte claquée ou une serrure forcée, un volet bloqué ouvert. Dans ces cas, nous intervenons sans attendre, 24h/24, à Antibes et dans tout le 06."),
        ("Combien coûte un dépannage de nuit ou le week-end ?","Le tarif minimum d'intervention est de 110 € HT en journée ; hors horaires ouvrés, une majoration s'applique. Elle vous est annoncée au téléphone avant tout déplacement, avec le tarif de base : vous décidez en connaissance de cause, et rien n'est ajouté sur place."),
        ("Que faire en attendant le technicien ?","Fuite : fermez le robinet d'arrêt général près du compteur. Électricité : coupez le disjoncteur si l'eau est proche des prises. Gaz : aérez, ne touchez à aucun interrupteur, sortez. Porte claquée : n'essayez pas de forcer, vous abîmeriez la serrure. Nous vous guidons au téléphone."),
        ("Dans quelles villes intervenez-vous en urgence ?","Dans toutes les Alpes-Maritimes, en priorité autour de nos quatre agences : Antibes, Juan-les-Pins, Cagnes-sur-Mer et Le Cannet, puis Villeneuve-Loubet, Cannes, Mandelieu, Nice, Saint-Laurent-du-Var et jusqu'à Grasse, Vence et Menton. Dans le Var est (Fréjus, Saint-Raphaël, pays de Fayence), selon la disponibilité des équipes mobiles."),
    ], "Questions sur le dépannage d'urgence")
    urg = "".join(f'<a href="{t["page"]}"><span class="ic">{ICO_METIER[t["cle"]]}</span><span><b>Urgence {t["nom"].lower()}</b><span>{t["accroche"]}</span></span></a>' for t in TRADES)
    page_simple("urgence-depannage-24h.html","Dépannage urgent 24h/24 Antibes, 06 & Var | Atelier PACA","Dépannage d'urgence 24h/24 à Antibes, dans le 06 et le Var est : fuite d'eau, panne de chauffage, panne électrique, porte claquée, volet bloqué. Prix annoncé avant déplacement.",
        "Dépannage urgent 24h/24 à Antibes et dans les Alpes-Maritimes","Astreinte 7j/7",
        f'''<p>Un technicien de garde répond à toute heure au {E["tel"]}. Il évalue la situation, vous donne les gestes de sécurité et annonce le prix avant de partir. Objectif : stopper les dégâts dans l'heure, puis réparer proprement. Plombier, chauffagiste, électricien, serrurier, climatisation ou volets : choisissez le métier concerné.</p>
<div class="hub">{urg}</div>
<h2>Comment se passe un dépannage d'urgence</h2>
<div class="etapes"><div class="etape"><span class="n">1</span><b>Vous appelez</b><p>{E["tel"]}, 24h/24. Décrivez la panne : nous vous indiquons tout de suite les gestes à faire pour limiter les dégâts.</p></div><div class="etape"><span class="n">2</span><b>Prix annoncé</b><p>Déplacement et tarif de base annoncés au téléphone, majoration incluse si hors horaires. Vous validez avant que le technicien parte.</p></div><div class="etape"><span class="n">3</span><b>Mise en sécurité</b><p>Le technicien stoppe le problème (fuite, court-circuit, porte, volet) et sécurise les lieux, avec les pièces courantes en stock.</p></div><div class="etape"><span class="n">4</span><b>Réparation</b><p>Réparation immédiate quand c'est possible, sinon devis gratuit pour la suite, sous 24 h, et facture détaillée pour votre assurance.</p></div></div>
<h2>Les urgences les plus fréquentes sur la Côte d'Azur</h2>
<ul class="liste"><li><a href="plomberie.html">Fuite d'eau</a>, canalisation bouchée avec refoulement, chauffe-eau qui fuit</li><li><a href="chauffage.html">Chaudière en sécurité</a>, plus d'eau chaude, pompe à chaleur en défaut en plein hiver</li><li><a href="electricite.html">Panne de courant</a>, disjoncteur qui saute en boucle, odeur de brûlé au tableau</li><li><a href="serrurerie.html">Porte claquée</a>, clés perdues, serrure forcée après une effraction</li><li><a href="volets-roulants.html">Volet roulant bloqué ouvert</a> en rez-de-chaussée ou dans une résidence secondaire</li><li><a href="climatisation.html">Climatisation en panne</a> en période de canicule</li></ul>
{faq_htm}''', ld_extra=[faq_ld], prio="0.8", lead="Fuite d'eau, chaudière en panne, coupure de courant, porte claquée, volet bloqué : un technicien de garde répond jour et nuit, week-end et jours fériés, à Antibes, Cagnes-sur-Mer, Cannes, Nice et dans tout le 06.")

    # Contrat d'entretien
    faq_htm, faq_ld = faq_block([
        ("Que comprend le contrat d'entretien ?","Une visite annuelle programmée (nettoyage, contrôles, réglages, attestation pour les chaudières), le dépannage sous 48 h en cas de panne, et 10 % de remise sur les pièces détachées. Le technicien vous appelle pour fixer la date : vous n'avez rien à retenir."),
        ("Combien coûte un contrat d'entretien de chaudière ou de climatisation ?","À partir de 110 € HT par an pour une chaudière gaz, et 110 € HT par an et par split pour une climatisation, visite annuelle comprise. Le tarif est dégressif à partir du deuxième équipement, et le devis est gratuit pour une pompe à chaleur air/eau ou un parc de copropriété."),
        ("Puis-je regrouper plusieurs équipements ?","Oui : chaudière + climatisation, plusieurs splits, ou chaudière + chauffe-eau, sur un même contrat avec une seule visite quand c'est possible. Le tarif est dégressif à partir du deuxième équipement."),
        ("Le contrat est-il valable dans toute votre zone ?","Oui, dans toutes les Alpes-Maritimes, d'Antibes et Cagnes-sur-Mer à Cannes, Nice ou Grasse, et dans le Var est. Pour les communes éloignées, nous groupons les visites d'entretien par tournées afin de tenir la date prévue."),
        ("Comment résilier ?","Le contrat est annuel, sans reconduction forcée : vous restez libre chaque année. Si vous vendez le logement, le contrat et l'historique d'entretien peuvent être transmis à l'acheteur."),
    ], "Questions sur les contrats d'entretien")
    page_simple("contrat-entretien.html","Contrat d'entretien clim & chaudière Antibes | Atelier PACA","Contrat d'entretien annuel clim et chaudière à Antibes, dans le 06 et le Var est : visite programmée dès 110 € HT, attestation, dépannage sous 48 h, 10 % sur les pièces.",
        "Contrat d'entretien climatisation et chaudière à Antibes et dans le 06","Vous n'y pensez plus, on s'en occupe",
        f'''<p>L'entretien annuel est la différence entre un appareil qui dure quinze ans et un appareil remplacé au bout de sept. Avec un contrat d'entretien Atelier PACA, la visite est programmée chaque année à la bonne saison (automne pour la chaudière, printemps pour la climatisation), vous recevez l'attestation, et vous passez en priorité en cas de panne, avec dépannage sous 48 h et 10 % de remise sur les pièces.</p>
<h2>Les formules de contrat d'entretien</h2>
<div class="tarifs">
<div class="tarif"><div><b>Chaudière gaz</b><p>Visite annuelle avant l'hiver, nettoyage du corps de chauffe, contrôle de combustion et de CO, attestation d'entretien, dépannage sous 48 h, 10 % de remise sur les pièces.</p></div><div class="px"><b>dès 110 € HT</b><small>par an</small></div></div>
<div class="tarif"><div><b>Climatisation</b><p>Visite annuelle au printemps, nettoyage des filtres et désinfection, contrôle du circuit et des pressions, dépannage sous 48 h, 10 % de remise sur les pièces.</p></div><div class="px"><b>dès 110 € HT</b><small>par an et par split</small></div></div>
<div class="tarif"><div><b>Pompe à chaleur air/eau</b><p>Visite annuelle, contrôle d'étanchéité, filtres, régulation, dépannage sous 48 h, 10 % de remise sur les pièces.</p></div><div class="px"><b>Sur devis</b><small>gratuit</small></div></div>
<div class="tarif"><div><b>Copropriétés et professionnels</b><p>Parc d'équipements, plusieurs sites, interlocuteur dédié. Syndics, agences, commerces et bureaux : voir notre <a href="professionnels-syndics.html">offre professionnelle</a>.</p></div><div class="px"><b>Sur devis</b><small>gratuit</small></div></div>
</div>
<p class="note">Tarif dégressif à partir du deuxième équipement. Contrat annuel sans reconduction forcée. TVA à 10 % ou 20 % selon l'ancienneté du logement.</p>
<h2>Ce que vous gagnez avec un contrat d'entretien</h2>
<ul class="liste"><li>La visite est programmée par nos soins, à la bonne saison : vous n'avez rien à retenir</li><li>Dépannage sous 48 h en cas de panne, avant les clients sans contrat</li><li>10 % de remise sur les pièces détachées</li><li>Attestation d'entretien pour votre assureur ou votre propriétaire (chaudière)</li><li>Historique des interventions conservé : utile à la revente ou pour un sinistre</li><li>Pour les résidences secondaires : visite coordonnée avec le gardien ou l'agence, compte rendu envoyé à distance</li></ul>
<h2>Comment souscrire</h2>
<p>Appelez le {E["tel"]}, écrivez sur WhatsApp ou remplissez le <a href="contact.html#devis">formulaire de devis</a> en indiquant votre équipement (marque, année si vous la connaissez) et votre ville. Nous vous confirmons le tarif et la première date de visite sous 24 h. Si votre appareil est en panne aujourd'hui, nous commençons par le <a href="urgence-depannage-24h.html">dépannage</a>.</p>
{faq_htm}''', ld_extra=[faq_ld], prio="0.8", lead="Visite annuelle programmée dès 110 € HT, dépannage sous 48 h et 10 % de remise sur les pièces détachées, pour votre chaudière ou votre climatisation, dans les Alpes-Maritimes et le Var est.")

    # Professionnels, syndics, copropriétés
    faq_htm, faq_ld = faq_block([
        ("Travaillez-vous avec les syndics de copropriété ?","Oui. Nous intervenons pour les syndics et les conseils syndicaux sur les parties communes (colonnes d'eau, chaufferie, éclairage et tableaux des communs, serrurerie des halls, volets et stores collectifs) et chez les copropriétaires qui le souhaitent. Devis gratuit, facture détaillée, rapport d'intervention avec photos, coordination avec le gardien."),
        ("Proposez-vous un contrat d'entretien pour plusieurs sites ou plusieurs équipements ?","Oui. Le contrat couvre un parc de climatisations, de chaudières ou de chauffe-eau sur un ou plusieurs immeubles, avec un calendrier de visites, le dépannage sous 48 h et 10 % de remise sur les pièces détachées. Tarif dégressif à partir du deuxième équipement, devis gratuit pour un parc."),
        ("Quel est le délai d'intervention pour un professionnel ?","Sous 48 h pour une intervention planifiée, plus vite en urgence grâce à l'astreinte 24h/24, 7j/7. Les clients sous contrat d'entretien passent avant les autres demandes. Nos quatre agences (Antibes, Juan-les-Pins, Cagnes-sur-Mer, Le Cannet) couvrent la côte de Mandelieu à Nice et le Var est."),
        ("Comment se passe la facturation ?","Un devis gratuit avant les travaux, un prix annoncé avant tout dépannage, puis une facture détaillée par site ou par lot, utilisable pour l'assurance, le syndic ou la comptabilité. Un seul interlocuteur suit vos demandes, quel que soit le métier concerné."),
        ("Êtes-vous assurés pour les chantiers professionnels ?","Oui : responsabilité civile professionnelle et garantie décennale sur les travaux, attestations fournies avec le devis. Entreprise d'Antibes depuis 2015, SIREN 814 736 781, plus de 10 800 interventions réalisées."),
    ], "Questions des syndics et des professionnels")
    cibles = "".join(f'<div class="t"><b>{esc(a)}</b><p>{esc(b)}</p></div>' for a,b in [
        ("Syndics et copropriétés","Colonnes d'eau, chaufferie, éclairage et tableaux des parties communes, serrurerie des halls, volets collectifs, interventions chez les copropriétaires. Rapport d'intervention avec photos pour le conseil syndical."),
        ("Agences immobilières et gestionnaires","Dépannages entre deux locataires, remises aux normes avant location, états des lieux techniques, résidences secondaires suivies à distance avec compte rendu envoyé au propriétaire."),
        ("Commerces, bureaux, restaurants","Climatisation tertiaire, électricité, plomberie et chauffe-eau de grande capacité, serrurerie et volets de devanture, contrats d'entretien pour éviter la panne un jour d'ouverture."),
        ("Résidences de tourisme et conciergeries","Interventions coordonnées avec le gardien ou la conciergerie, clés et accès gérés, entretien des climatisations avant la saison, dépannage pendant les locations."),
    ])
    page_simple("professionnels-syndics.html","Syndics, copropriétés & professionnels | Atelier PACA","Artisan multi-métiers pour syndics, copropriétés, agences, commerces et bureaux à Antibes, dans le 06 et le Var est : contrats d'entretien, dépannage 24h/24, un interlocuteur.",
        "Syndics, copropriétés et professionnels : six métiers, un interlocuteur","Offre professionnelle",
        f'''<p>Gérer un immeuble, un parc de logements ou un commerce, c'est jongler entre un plombier, un électricien, un chauffagiste, un frigoriste, un serrurier et un volettiste. Atelier PACA réunit les six métiers dans une seule entreprise d'Antibes, avec un seul numéro, un interlocuteur qui suit vos demandes, une facture détaillée par site et une astreinte 24h/24. Quatre agences (Antibes, Juan-les-Pins, Cagnes-sur-Mer, Le Cannet) couvrent les Alpes-Maritimes de Mandelieu à Nice et le Var est.</p>
<h2>Pour qui</h2>
<div class="trio" style="grid-template-columns:1fr 1fr">{cibles}</div>
<h2>Ce que nous apportons aux professionnels</h2>
<ul class="liste"><li><b>Un interlocuteur unique</b> pour les six métiers : plomberie, chauffage, climatisation, électricité, volets roulants, serrurerie</li><li><b>Dépannage sous 48 h</b>, plus vite en urgence, astreinte 24h/24 et 7j/7, prix annoncé avant le déplacement</li><li><b>Contrats d'entretien multi-équipements et multi-sites</b> : visites programmées, dépannage sous 48 h, 10 % de remise sur les pièces détachées, tarif dégressif</li><li><b>Devis gratuit</b> et facture détaillée par site ou par lot, rapport d'intervention avec photos sur demande</li><li><b>Garantie décennale et responsabilité civile</b>, attestations jointes au devis, matériel de grandes marques</li><li><b>Coordination sur place</b> avec le gardien, la conciergerie ou le locataire ; compte rendu envoyé au gestionnaire absent</li></ul>
<h2>Les prestations les plus demandées</h2>
<div class="tarifs">
<div class="tarif"><div><b>Contrat d'entretien de parc</b><p>Climatisations, chaudières, chauffe-eau sur un ou plusieurs immeubles : calendrier de visites, attestations, dépannage prioritaire.</p></div><div class="px"><b>Sur devis</b><small>gratuit, dégressif</small></div></div>
<div class="tarif"><div><b>Dépannage parties communes</b><p>Fuite sur colonne, panne d'éclairage ou de tableau des communs, porte de hall, volet ou store collectif bloqué.</p></div><div class="px"><b>dès 110 € HT</b><small>prix annoncé avant</small></div></div>
<div class="tarif"><div><b>Remise aux normes avant location</b><p>Tableau électrique, prises et mise à la terre, robinetterie et chauffe-eau, serrure, pour louer sans réserve.</p></div><div class="px"><b>Sur devis</b><small>gratuit sous 24 h</small></div></div>
<div class="tarif"><div><b>Climatisation tertiaire</b><p>Pose, remplacement et entretien de climatisations pour bureaux, commerces et restaurants, avec intervention hors horaires d'ouverture si besoin.</p></div><div class="px"><b>Sur devis</b><small>visite gratuite</small></div></div>
</div>
<p class="note">Tarif minimum d'intervention : 110 € HT. TVA à 10 % ou 20 % selon la nature des travaux et l'ancienneté du bâtiment. Devis gratuit, prix définitif communiqué avant toute intervention.</p>
<h2>Comment ça se passe</h2>
<div class="etapes"><div class="etape"><span class="n">1</span><b>Vous nous appelez ou écrivez</b><p>{E["tel"]} ou <a href="mailto:{E["email"]}">{E["email"]}</a> : décrivez le site, les équipements et le besoin ; nous répondons sous 2 h en journée.</p></div><div class="etape"><span class="n">2</span><b>Visite et devis gratuits</b><p>Un technicien se déplace, relève les équipements et vous remet un devis clair sous 24 h, attestations d'assurance jointes.</p></div><div class="etape"><span class="n">3</span><b>Intervention coordonnée</b><p>Date fixée avec le gardien, le gestionnaire ou le locataire ; intervention propre, photos avant/après.</p></div><div class="etape"><span class="n">4</span><b>Facture et suivi</b><p>Facture détaillée par site, rapport d'intervention, historique conservé pour l'entretien et les sinistres.</p></div></div>
{avis_block([a for a in AVIS_GOOGLE if a["auteur"] in ("Foued B.", "Akram B.", "Abdelmoumene D.")], "Ce que disent nos clients sur Google", AGENCES[0])}
{faq_htm}
<h2>Demander un devis professionnel</h2>
<p>Appelez le {E["tel"]}, écrivez à <a href="mailto:{E["email"]}">{E["email"]}</a> ou utilisez le <a href="contact.html#devis">formulaire</a> en précisant « syndic », « agence » ou « professionnel », le nombre de sites et les équipements concernés. Pour un entretien récurrent, voyez aussi la page <a href="contrat-entretien.html">contrats d'entretien</a>.</p>''', ld_extra=[faq_ld], prio="0.8", lead="Un seul numéro pour vos immeubles, vos locaux et vos biens gérés : plomberie, chauffage, climatisation, électricité, volets et serrurerie, contrats d'entretien, dépannage 24h/24, facture détaillée par site.")

    # Avis clients : avis Google réels, regroupés par fiche
    par_fiche = ""
    for ag in AGENCES:
        items = [a for a in AVIS_GOOGLE if a["agence"] == ag["cle"]]
        if not items: continue
        par_fiche += f'<h2 id="avis-{ag["cle"]}">Avis Google — fiche {esc(ag["nom"])} ({ag["note"]}/5, {ag["avis"]} avis)</h2><p>{esc(ag["adresse"])}, {ag["cp"]} {esc(ag["ville"])} · <a href="{maps(ag)}" target="_blank" rel="noopener">voir la fiche et tous les avis</a> · <a href="{avis_url(ag)}" target="_blank" rel="noopener">laisser un avis</a></p><div class="avis-wrap c2">' + "".join(avis_card(a) for a in items) + '</div>'
    avis = par_fiche
    fiches = "".join(f'<div class="fiche"><b>{a["nom"]}</b><span>{a["adresse"]}, {a["cp"]} {a["ville"]}</span><span>{a["note"]}/5 · {a["avis"]} avis</span><div class="l"><a href="{maps(a)}" target="_blank" rel="noopener">Voir la fiche</a><a href="{avis_url(a)}" target="_blank" rel="noopener">Laisser un avis</a></div></div>' for a in AGENCES)
    page_simple("avis-clients.html","Avis clients Atelier PACA — 4,9/5 sur Google | Antibes","Les avis Google des clients d'Atelier PACA : 4,9/5 sur 178 avis à Antibes et plus de 450 avis sur nos 4 fiches (Antibes, Juan-les-Pins, Cagnes, Le Cannet).",
        f"{E['note']}/5 — ce que disent nos clients","Avis vérifiables sur Google",
        f'''<p>Nous n'offrons rien en échange d'un avis : tout ce qui est écrit sur nos fiches Google est public, daté et vérifiable. Voici une sélection d'avis 5 étoiles repris tels quels (texte inchangé, prénom et initiale), fiche par fiche, avec le lien pour lire l'ensemble des avis, bons comme moins bons. Quatre fiches : <a href="#avis-antibes">Antibes</a>, <a href="#avis-juan-les-pins">Juan-les-Pins</a>, <a href="#avis-cagnes-sur-mer">Cagnes-sur-Mer</a>, <a href="#avis-le-cannet">Le Cannet</a>.</p>
{avis}
<h2>Nos quatre fiches Google</h2>
<div class="fiches" style="grid-template-columns:1fr 1fr">{fiches}</div>
<h2>Vous avez fait appel à nous ?</h2>
<p>Un avis prend deux minutes et aide les habitants de votre ville à choisir un artisan sérieux. Choisissez la fiche de l'agence la plus proche de chez vous ci-dessus et cliquez sur « Laisser un avis ».</p>''', prio="0.7", lead="Quatre fiches Google, plus de 450 avis publics. Nous n'offrons rien contre un avis et ne trions pas les clients.")

    # À propos
    page_simple("a-propos.html","Artisans à Antibes depuis 2015 | Atelier PACA","Atelier PACA, entreprise artisanale d'Antibes depuis 2015 : plombiers, chauffagistes, électriciens, serruriers, garantie décennale, 10 800 interventions, 4,9/5.",
        "Atelier PACA : une entreprise d'artisans à Antibes, six métiers, depuis 2015","Qui sommes-nous",
        f'''<div class="photo-p"><img src="images/equipe-camion.webp" alt="Technicien Atelier PACA et camion d'intervention équipé pour six métiers, Antibes" width="904" height="459" loading="eager"></div>
<p>Atelier PACA est née à Antibes en {E["depuis"]} avec une idée simple : les habitants de la côte n'ont pas envie de chercher un plombier, puis un électricien, puis un frigoriste. Ils veulent un numéro, un interlocuteur qui connaît leur logement, et une facture claire. C'est devenu notre promesse : un seul numéro pour toute votre maison.</p>
<p>Dix ans plus tard, l'équipe a réalisé plus de {E["interventions"]} interventions dans les Alpes-Maritimes et le Var est, de Juan-les-Pins à Nice et de Cannes à Grasse, et quatre fiches Google (Antibes, Juan-les-Pins, Cagnes-sur-Mer, Le Cannet) cumulent plus de 450 avis à {E["note"]}/5. Le siège, le stock de pièces et l'atelier sont toujours chemin des Autrichiens, à Antibes.</p>
<h2>Ce qui nous distingue d'un dépanneur classique</h2>
<div class="trio">
<div class="t"><b>Garantie décennale</b><p>Tous nos travaux sont couverts dix ans. Attestation d'assurance fournie sur demande, avant le chantier.</p></div>
<div class="t"><b>Prix avant intervention</b><p>Tarif annoncé au téléphone ou sur devis, majoration de nuit ou de week-end annoncée aussi. Tarif minimum 110 € HT.</p></div>
<div class="t"><b>Astreinte 24h/24</b><p>Un technicien de garde chaque nuit, chaque week-end, chaque jour férié, pour les urgences de plomberie, chauffage, électricité et serrurerie.</p></div>
<div class="t"><b>Techniciens spécialisés</b><p>Chacun exerce son métier (électriciens habilités, frigoristes, plombiers, serruriers) ; l'équipe couvre les six et se coordonne en interne.</p></div>
<div class="t"><b>Grandes marques</b><p>Daikin, Mitsubishi Electric, Atlantic, Somfy, Legrand, Schneider, Vaillant : des pièces disponibles dans dix ans.</p></div>
<div class="t"><b>Fournisseurs locaux</b><p>Stock au siège d'Antibes et partenaires de proximité pour les pièces : la plupart des dépannages se terminent en une visite.</p></div>
</div>
<h2>Atelier PACA en bref</h2>
<ul class="liste"><li><b>Qui :</b> entreprise artisanale d'Antibes (SASU, SIREN {E["siren"]}) fondée en {E["depuis"]}</li><li><b>Quoi :</b> six métiers du bâtiment, plomberie, chauffage, climatisation, électricité, volets roulants, serrurerie, en dépannage, entretien et installation</li><li><b>Où :</b> Alpes-Maritimes dans un rayon de 30 km autour d'Antibes (Cannes, Nice, Cagnes-sur-Mer, Grasse, Menton…) et Var est (Fréjus, Saint-Raphaël, pays de Fayence) ; quatre agences : Antibes, Juan-les-Pins, Cagnes-sur-Mer, Le Cannet</li><li><b>Quand :</b> astreinte 24h/24 et 7j/7, intervention sous 48 h, souvent le jour même en urgence</li><li><b>Combien :</b> tarif minimum d'intervention 110 € HT, prix annoncé avant toute intervention, devis et visite technique gratuits, contrat d'entretien dès 110 € HT par an</li><li><b>Garanties :</b> garantie décennale, responsabilité civile professionnelle, facture détaillée, {E["note"]}/5 sur {E["avis"]} avis Google</li><li><b>Contact :</b> {E["tel"]}, {E["email"]}, {E["adresse"]}, {E["cp"]} {E["ville"]}</li></ul>
<h2>Nos clients : particuliers, copropriétés, professionnels</h2>
<p>Propriétaires et locataires en appartement ou en villa, résidences secondaires gérées à distance avec un gardien ou une agence, syndics de copropriété pour les colonnes d'eau, la serrurerie des parties communes et les contrats d'entretien, commerces et bureaux pour l'électricité et la climatisation tertiaire. Dans tous les cas : prix annoncé, facture détaillée, rapport d'intervention sur demande. Syndics et gestionnaires : voir notre <a href="professionnels-syndics.html">offre professionnelle</a>.</p>
<h2>Nos agences</h2>
<div class="fiches" style="grid-template-columns:1fr 1fr">{"".join(f'<div class="fiche"><b>{a["nom"]}</b><span>{a["adresse"]}, {a["cp"]} {a["ville"]}</span><span>{a["note"]}/5 · {a["avis"]} avis</span><div class="l"><a href="{maps(a)}" target="_blank" rel="noopener">Fiche Google</a></div></div>' for a in AGENCES)}</div>
<h2>Notre plaquette</h2><div class="galerie" style="grid-template-columns:1fr 1fr"><figure><a href="images/plaquette-atelier-paca.jpg" target="_blank" rel="noopener"><img src="images/plaquette-atelier-paca.webp" alt="Plaquette commerciale Atelier PACA : six métiers, installation, entretien, dépannage à Antibes" loading="lazy" width="800" height="1132" style="aspect-ratio:auto"></a><figcaption>Plaquette commerciale — cliquez pour l'ouvrir en grand.</figcaption></figure><figure><img src="images/avis-clients-google.webp" alt="Technicien Atelier PACA et avis clients Google 4,9/5" loading="lazy" width="900" height="520" style="aspect-ratio:auto"><figcaption>Vos avis Google font notre réputation : plus de 450 avis publics sur nos quatre fiches.</figcaption></figure></div><h2>Informations légales</h2>
<p>Atelier PACA, SASU — SIREN {E["siren"]} — siège : {E["adresse"]}, {E["cp"]} {E["ville"]}. Assurance responsabilité civile et décennale. <a href="mentions-legales.html">Mentions légales</a>.</p>''', prio="0.6")

    # Réalisations
    gal = [("chantier-clim-interieur","Pose d'une unité intérieure de climatisation murale, appartement à Antibes","Climatisation"),
           ("chantier-clim-groupe-exterieur","Unité extérieure de climatisation sur supports antivibratiles, villa du Cap d'Antibes","Climatisation"),
           ("chantier-douche-italienne","Douche à l'italienne carrelée, rénovation complète de salle de bain dans les Alpes-Maritimes","Plomberie"),
           ("chantier-salle-de-bain","Salle de bain rénovée par Atelier PACA : plomberie, électricité et finitions","Plomberie et électricité"),
           ("chantier-wc-suspendu","WC suspendu avec bâti-support posé à Cagnes-sur-Mer","Plomberie"),
           ("volets-cote-azur","Volets roulants motorisés posés sur une façade de la Côte d'Azur","Volets roulants"),
           ("serrurerie-porte-blindee","Serrure multipoints haute sécurité installée sur une porte blindée","Serrurerie"),
           ("entretien-clim-avant-apres","Entretien de climatisation : filtres et échangeur avant et après nettoyage","Climatisation"),
           ("camion-fondu","Camion d'intervention Atelier PACA équipé pour six métiers, Antibes","Équipe")]
    galerie = "".join(f'<figure><img src="images/{i}.webp" alt="{esc(c)}" loading="lazy" width="800" height="600"><figcaption><strong>{m}</strong> — {esc(c)}</figcaption></figure>' for i,c,m in gal)
    page_simple("realisations.html","Réalisations Atelier PACA — Chantiers dans le 06 et le Var","Photos de chantiers Atelier PACA : climatisation, salle de bain, électricité, volets roulants et serrurerie dans les Alpes-Maritimes et le Var.",
        "Nos réalisations à Antibes et sur la Côte d'Azur","Chantiers récents",
        f'<p>Quelques chantiers récents de climatisation, salle de bain, électricité, volets et serrurerie, photographiés par nos techniciens à Antibes, Cagnes-sur-Mer, Cannes et dans les Alpes-Maritimes. Nous ajoutons de nouvelles photos chaque semaine sur nos fiches Google et nos réseaux. Un projet similaire ? <a href="contact.html#devis">Demandez un devis gratuit</a>.</p><div class="galerie">{galerie}</div>', prio="0.6")

    # Marques
    marques = "".join(f'<h3>{t["nom"]}</h3><div class="marques">{"".join(f"<span>{esc(m)}</span>" for m in t["marques"])}</div>' for t in TRADES)
    page_simple("marques.html","Marques : Daikin, Mitsubishi, Atlantic, Somfy | Atelier PACA","Les marques installées et dépannées par Atelier PACA dans le 06 et le Var : Daikin, Mitsubishi Electric, Atlantic, Vaillant, Somfy, Legrand, Schneider, Fichet.",
        "Les marques que nous installons et dépannons","Matériel de grandes marques",
        f'<p>Nous choisissons des marques pour leur fiabilité et la disponibilité des pièces dans dix ans. Nos techniciens sont formés sur ces gammes et dépannent aussi les autres marques du marché.</p>{marques}', prio="0.5")

    # FAQ générale
    allfaq = []
    for t in TRADES: allfaq += t["faq"][:3]
    faq_htm, faq_ld = faq_block([("Sous quel délai intervenez-vous à Antibes et dans les Alpes-Maritimes ?","Sous 48 h pour une intervention classique, souvent le jour même pour une urgence (fuite, panne de courant, porte claquée, chaudière en sécurité) grâce à l'astreinte 24h/24 et 7j/7. Le délai exact vous est donné au téléphone, selon votre ville et l'heure."),
                                 ("Le devis est-il gratuit ?","Oui, devis et visite technique sont gratuits et sans engagement, pour tous nos métiers. Pour un dépannage, le prix est annoncé avant l'intervention, majoration de nuit ou de week-end comprise ; le tarif minimum d'intervention est de 110 € HT."),
                                 ("Quelle zone couvrez-vous ?","Les Alpes-Maritimes, d'Antibes à Nice et de Cannes à Grasse (Mandelieu, Le Cannet, Vallauris, Villeneuve-Loubet, Cagnes-sur-Mer, Saint-Laurent-du-Var, Vence, jusqu'à Menton), et le Var est : Fréjus, Saint-Raphaël et le pays de Fayence. Chaque commune a sa page avec nos délais."),
                                 ("Comment payer ?","Carte bancaire, virement, chèque ou espèces, à la fin de l'intervention ou selon l'échéancier du devis pour les travaux. Facture détaillée remise à chaque intervention, par e-mail ou sur place."),
                                 ("Travaillez-vous avec les assurances et les syndics ?","Oui : rapport d'intervention avec photos et facture détaillée pour les déclarations de sinistre (dégât des eaux, effraction), documents techniques pour les demandes aux syndics (climatisation, borne de recharge), contrats d'entretien pour les copropriétés."),
                                 ("Qui intervient chez moi ?","Un technicien Atelier PACA, spécialisé dans le métier concerné et identifiable : tenue, véhicule, nom de société et SIREN 814 736 781 sur la facture. Vous pouvez vérifier nos avis sur nos quatre fiches Google.")] + allfaq, "Toutes les questions")
    page_simple("faq.html","Questions fréquentes — Délais, devis, tarifs | Atelier PACA","Les réponses d'Atelier PACA sur les délais, le devis gratuit, les tarifs, les urgences 24h/24, les garanties et la zone d'intervention à Antibes, dans le 06 et le Var.",
        "Questions fréquentes sur nos dépannages et travaux","Délais, prix, garanties", f'<p>Les questions que nos clients d\'Antibes, Cagnes-sur-Mer, Cannes et Nice nous posent le plus souvent, par téléphone ou sur nos fiches Google. Vous ne trouvez pas la vôtre ? Appelez le {E["tel"]} ou écrivez-nous sur WhatsApp : un technicien répond.</p>{faq_htm}', ld_extra=[faq_ld], prio="0.5")

    # Contact
    cp_ld = {"@context":"https://schema.org","@type":"ContactPage","url":SITE+"contact.html","name":"Contact Atelier PACA"}
    agences = "".join(f'<div class="fiche"><b>{a["nom"]}</b><span>{a["adresse"]}, {a["cp"]} {a["ville"]}</span><span>{a["note"]}/5 · {a["avis"]} avis</span><div class="l"><a href="{maps(a)}" target="_blank" rel="noopener">Itinéraire</a></div></div>' for a in AGENCES)
    c_htm, c_ld = crumb([("Accueil","index.html"),("Contact","contact.html")])
    body = header("contact.html") + f'''<main>
<section class="hero hero-mini"><div class="wrap">{c_htm}<p class="kicker">Devis gratuit, réponse sous 2 h</p><h1>Contactez Atelier PACA, artisans à Antibes</h1><p class="lead">Pour un dépannage urgent, appelez le {E["tel"]} : un technicien de garde répond 24h/24 et annonce le prix avant de se déplacer. Pour un devis (climatisation, chaudière, électricité, salle de bain, serrurerie, volets), laissez vos coordonnées et nous vous rappelons sous 2 h en journée.</p></div></section>
<section class="sec" style="padding-top:28px" id="devis"><div class="wrap"><div class="contact">{coord_block()}{form_devis()}</div>
<h2 style="margin-top:50px">Nos agences à Antibes, Juan-les-Pins, Cagnes-sur-Mer et Le Cannet</h2><p>Quatre fiches Google, un seul numéro. Les visites se font chez vous : pas besoin de passer à l'agence.</p><div class="fiches">{agences}</div></div></section>
</main>''' + footer()
    write("contact.html", head("Contact — Devis gratuit, 04 92 14 14 14 | Atelier PACA","Contactez Atelier PACA : 04 92 14 14 14 (24h/24), WhatsApp, formulaire de devis gratuit. Agences à Antibes, Juan-les-Pins, Cagnes-sur-Mer et Le Cannet.","contact.html",[ld_business(),cp_ld,c_ld]) + body, "0.8")

    # Blog + articles
    posts = "".join(f'<a class="post" href="{a["slug"]}"><img src="images/{a["img"]}-480.webp" alt="{esc(TRADE_BY_KEY[a["metier"]]["alt"])}" loading="lazy" width="480" height="300"><div class="in"><h3>{esc(a["titre"])}</h3><p>{esc(a["resume"])}</p><small>Lire le conseil</small></div></a>' for a in ARTICLES)
    page_simple("blog.html","Conseils clim, chauffage, plomberie | Atelier PACA","Les conseils d'Atelier PACA : entretien de chaudière, prix d'une climatisation dans le 06, gestes en cas de fuite d'eau. Écrits par nos techniciens d'Antibes.",
        "Conseils d'artisans d'Antibes : chauffage, climatisation, plomberie","Le blog Atelier PACA", f'<p>Des articles courts, écrits par nos techniciens d\'Antibes, pour vous aider à décider, à comparer les devis et à éviter les pannes dans les Alpes-Maritimes.</p><div class="posts" style="grid-template-columns:1fr">{posts}</div>', prio="0.6")
    for a in ARTICLES:
        c_htm, c_ld = crumb([("Accueil","index.html"),("Conseils","blog.html"),(a["titre"],a["slug"])])
        art_ld = {"@context":"https://schema.org","@type":"Article","headline":a["titre"],"description":a["desc"],"datePublished":a["date"],"dateModified":a["date"],"inLanguage":"fr-FR","image":SITE+f"images/{a['img']}.webp","author":{"@type":"Organization","name":"Atelier PACA","url":SITE},"publisher":{"@id":SITE+"#organisation"},"mainEntityOfPage":SITE+a["slug"]}
        body = header("blog.html") + f'''<main>
<section class="hero hero-mini"><div class="wrap">{c_htm}<p class="kicker">Conseil d'artisan</p><h1>{esc(a["titre"])}</h1><p class="meta" style="color:var(--mut2);font-size:13.5px;margin-top:10px">Publié le {date_fr(a["date"])} par l'équipe Atelier PACA, Antibes · {esc(a["resume"])}</p></div></section>
<section class="sec" style="padding-top:28px"><div class="wrap"><div class="page"><div class="main article"><div class="photo-p"><img src="images/{a["img"]}.webp" alt="{esc(TRADE_BY_KEY[a["metier"]]["alt"])}" width="886" height="481" loading="eager"></div>{a["corps"]}
<div class="encart"><div><b>Une question sur votre installation ?</b><span>Devis gratuit, réponse sous 2 h en journée, dans tout le 06 et le Var est.</span></div><a href="{TRADE_BY_KEY[a["metier"]]["page"]}" class="btn btn-rouge btn-sm">Voir nos prestations {TRADE_BY_KEY[a["metier"]]["nom"].lower()}</a></div>
<h3>Autres conseils de nos techniciens</h3><div class="chips">{"".join(f'<a href="{x["slug"]}">{esc(x["titre"])}</a>' for x in ARTICLES if x is not a)}</div></div>
<aside class="side"><div class="card"><h3>Besoin d'un artisan ?</h3><p>Astreinte 24h/24, prix annoncé avant le déplacement.</p><a href="{E["tel_href"]}" class="btn btn-rouge">{ICO["tel"]} {E["tel"]}</a><a href="contact.html#devis" class="btn btn-bleu">{ICO["doc"]} Devis gratuit</a></div><div class="card"><h3>Nos métiers</h3><div class="liens">{"".join(f'<a href="{t["page"]}">{t["nom"]}</a>' for t in TRADES)}</div></div></aside>
</div></div></section>{cta_final()}</main>''' + footer()
        write(a["slug"], head(a["titre_court"], a["desc"], a["slug"], [ld_business(), c_ld, art_ld], og_img=f"images/{a['img']}.webp") + body, "0.6")

    # Mentions légales
    page_simple("mentions-legales.html","Mentions légales | Atelier PACA","Mentions légales du site atelierpaca.fr, édité par Atelier PACA (SASU), Antibes.","Mentions légales","Informations légales",
        f'''<h2>Éditeur du site</h2><p>Le site atelierpaca.fr est édité par Atelier PACA, société par actions simplifiée unipersonnelle (SASU). Siège social : {E["adresse"]}, {E["cp"]} {E["ville"]}. SIREN {E["siren"]} — SIRET {E["siret"]}. Téléphone : {E["tel"]}. E-mail : {E["email"]}.</p>
<h2>Hébergement</h2><p>Le site est hébergé par GitHub, Inc. (GitHub Pages), 88 Colin P. Kelly Jr. Street, San Francisco, CA 94107, États-Unis.</p>
<h2>Propriété intellectuelle</h2><p>L'ensemble des éléments de ce site (textes, logo, images, mise en page) est la propriété d'Atelier PACA, sauf mention contraire. Toute reproduction sans autorisation écrite est interdite.</p>
<h2>Données personnelles</h2><p>Les informations transmises via le formulaire (nom, téléphone, ville, message) servent uniquement à répondre à votre demande. Elles ne sont ni vendues ni cédées. Conformément au RGPD, vous disposez d'un droit d'accès, de rectification et de suppression : écrivez à {E["email"]}.</p>
<h2>Cookies</h2><p>Ce site n'utilise ni cookies publicitaires ni traceurs. Aucun cookie n'est déposé par le site lui-même.</p>
<h2>Tarifs</h2><p>Les tarifs affichés sont indicatifs (TTC, 2026) et peuvent être modifiés à tout moment. Le tarif définitif est communiqué avant toute intervention.</p>
<h2>Droit applicable</h2><p>Les présentes mentions sont régies par le droit français. En cas de litige, les tribunaux du ressort du siège social d'Atelier PACA sont compétents.</p>''', cta=False, prio="0.2")

    # 404
    body = header() + f'''<main><section class="hero hero-mini"><div class="wrap"><p class="kicker">Erreur 404</p><h1>Cette page n'existe pas (ou plus)</h1><p class="lead">L'adresse a peut-être changé. Voici les pages les plus utiles.</p><div class="btns" style="margin-top:22px"><a href="index.html" class="btn btn-rouge">Retour à l'accueil</a><a href="{E["tel_href"]}" class="btn btn-bleu">{ICO["tel"]} {E["tel"]}</a></div><div class="chips" style="margin-top:28px">{"".join(f'<a href="{t["page"]}">{t["nom"]}</a>' for t in TRADES)}<a href="urgence-depannage-24h.html">Urgence 24h/24</a><a href="contact.html">Contact</a></div></div></section></main>''' + footer()
    with open(os.path.join(ROOT,"404.html"),"w",encoding="utf-8") as f:
        f.write(head("Page introuvable | Atelier PACA","Page introuvable.","404.html").replace('<meta name="robots" content="index,follow,max-image-preview:large">','<meta name="robots" content="noindex">') + body)

def pages_redirections():
    """Anciennes URLs des villes hors zone : renvoi immédiat vers la page métier (noindex, canonical métier)."""
    for slug in VILLES_RETIREES:
        cibles = [(f'{t["prefix"]}-{slug}.html', t["page"]) for t in TRADES] + [(f'depannage-{slug}.html', 'index.html')]
        for fn, cible in cibles:
            htm = f'<!DOCTYPE html><html lang="fr"><head><meta charset="utf-8"><title>Redirection — Atelier PACA</title><meta name="robots" content="noindex,follow"><link rel="canonical" href="{SITE}{cible if cible!="index.html" else ""}"><meta http-equiv="refresh" content="0;url={cible}"></head><body><p>Cette page a été déplacée : <a href="{cible}">continuer</a>.</p></body></html>'
            with open(os.path.join(ROOT, fn), "w", encoding="utf-8") as f: f.write(htm)

def page_plan():
    sec = f'<h2>Pages principales</h2><ul class="liste"><li><a href="index.html">Accueil</a></li>' + "".join(f'<li><a href="{t["page"]}">{t["nom"]}</a></li>' for t in TRADES) + '<li><a href="urgence-depannage-24h.html">Dépannage urgent 24h/24</a></li><li><a href="contrat-entretien.html">Contrats d\'entretien</a></li><li><a href="professionnels-syndics.html">Syndics, copropriétés et professionnels</a></li><li><a href="avis-clients.html">Avis clients</a></li><li><a href="a-propos.html">Qui sommes-nous</a></li><li><a href="realisations.html">Réalisations</a></li><li><a href="marques.html">Marques</a></li><li><a href="faq.html">Questions fréquentes</a></li><li><a href="blog.html">Conseils</a></li>' + "".join(f'<li><a href="{a["slug"]}">{esc(a["titre"])}</a></li>' for a in ARTICLES) + '<li><a href="contact.html">Contact</a></li><li><a href="mentions-legales.html">Mentions légales</a></li></ul>'
    sec += '<h2>Villes (toutes prestations)</h2><div class="chips">' + "".join(f'<a href="depannage-{v["slug"]}.html">{v["nom"]}</a>' for v in VILLES) + '</div>'
    for t in TRADES:
        sec += f'<h3>{t["nom"]} par ville</h3><div class="chips">' + "".join(f'<a href="{t["prefix"]}-{v["slug"]}.html">{v["nom"]}</a>' for v in VILLES) + '</div>'
    page_simple("plan-du-site.html","Plan du site | Atelier PACA","Toutes les pages du site atelierpaca.fr : métiers, villes d'intervention, conseils et contact.","Plan du site","Toutes les pages", sec, cta=False, prio="0.3")

def sitemap():
    out = ['<?xml version="1.0" encoding="UTF-8"?>','<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for fn, prio, freq in PAGES:
        loc = SITE + ("" if fn == "index.html" else fn)
        out.append(f'<url><loc>{loc}</loc><lastmod>{DATE_MAJ}</lastmod><changefreq>{freq}</changefreq><priority>{prio}</priority></url>')
    out.append('</urlset>')
    with open(os.path.join(ROOT,"sitemap.xml"),"w",encoding="utf-8") as f: f.write("\n".join(out))
    # robots.txt : tout autorisé, avec autorisation explicite des robots des moteurs IA (ChatGPT, Claude, Gemini, Perplexity, Bing/Copilot, Apple, Meta)
    bots = ["GPTBot","OAI-SearchBot","ChatGPT-User","ClaudeBot","Claude-SearchBot","Claude-User","anthropic-ai","Google-Extended","Googlebot","Bingbot","PerplexityBot","Perplexity-User","Applebot","Applebot-Extended","Meta-ExternalAgent","Meta-ExternalFetcher","Amazonbot","DuckAssistBot","MistralAI-User","CCBot","YouBot"]
    rb = "".join(f"User-agent: {b}\nAllow: /\n\n" for b in bots)
    with open(os.path.join(ROOT,"robots.txt"),"w",encoding="utf-8") as f: f.write(f"# Atelier PACA — contenu ouvert aux moteurs de recherche et aux assistants IA\nUser-agent: *\nAllow: /\nDisallow: /build/\n\n{rb}Sitemap: {SITE}sitemap.xml\n")
    llms()

def llms():
    """llms.txt (résumé) et llms-full.txt (fiche complète) : fiche d'identité lisible par les assistants IA."""
    villes06 = ", ".join(v["nom"] for v in VILLES_06); villes83 = ", ".join(v["nom"] for v in VILLES_83)
    agences = "\n".join(f"- {a['nom']} : {a['adresse']}, {a['cp']} {a['ville']} — fiche Google {a['note']}/5 ({a['avis']} avis) : {maps(a)}" for a in AGENCES)
    metiers = "\n".join(f"- [{t['nom']}]({SITE}{t['page']}) : {t['desc_court']}" for t in TRADES)
    court = f"""# Atelier PACA

> Entreprise artisanale d'Antibes (Alpes-Maritimes, France) fondée en {E['depuis']} : plombier, chauffagiste, installateur de climatisation, électricien, volets roulants et serrurier. Dépannage 24h/24, entretien et installation dans les Alpes-Maritimes (30 km autour d'Antibes) et le Var est (Fréjus, Saint-Raphaël, pays de Fayence). Un seul numéro pour les six métiers : {E['tel']}.

## Faits clés
- Nom : Atelier PACA (SASU, SIREN {E['siren']}), siège {E['adresse']}, {E['cp']} {E['ville']}
- Téléphone : {E['tel']} (astreinte 24h/24, 7j/7) — e-mail : {E['email']} — site : {SITE}
- Métiers : plomberie, chauffage (chaudière, pompe à chaleur), climatisation, électricité, volets roulants, serrurerie
- Tarif minimum d'intervention : 110 € HT ; prix annoncé avant toute intervention ; devis et visite technique gratuits
- Délais : intervention sous 48 h, souvent le jour même en urgence
- Contrat d'entretien (chaudière, climatisation) : visite annuelle dès 110 € HT, dépannage sous 48 h, 10 % de remise sur les pièces détachées
- Garanties : garantie décennale, responsabilité civile professionnelle, facture détaillée
- Avis : {E['note']}/5 sur {E['avis']} avis Google (siège), plus de 450 avis sur 4 fiches
- Clients : particuliers, syndics de copropriété, agences immobilières, commerces et bureaux

## Agences
{agences}

## Pages principales
{metiers}
- [Dépannage urgent 24h/24]({SITE}urgence-depannage-24h.html)
- [Contrats d'entretien]({SITE}contrat-entretien.html)
- [Syndics, copropriétés et professionnels]({SITE}professionnels-syndics.html)
- [Avis clients]({SITE}avis-clients.html)
- [Villes d'intervention]({SITE}depannage-antibes.html) — une page par ville : {SITE}depannage-<ville>.html et {SITE}<metier>-<ville>.html
- [Qui sommes-nous]({SITE}a-propos.html) · [Contact]({SITE}contact.html) · [Plan du site]({SITE}plan-du-site.html)

## Zone d'intervention
- Alpes-Maritimes (06) : {villes06}
- Var est (83) : {villes83}

## Fiche complète
{SITE}llms-full.txt
"""
    with open(os.path.join(ROOT,"llms.txt"),"w",encoding="utf-8") as f: f.write(court)
    # version complète : prestations et tarifs par métier, FAQ
    blocs = []
    for t in TRADES:
        prest = "\n".join(f"- {n} : {p} {u} — {d}" for _,n,d,p,u in t["prestations"])
        faq = "\n".join(f"**{q}** {r}" for q,r in t["faq"])
        blocs.append(f"## {t['nom']} — {SITE}{t['page']}\n{t['intro'][0]}\n\n### Prestations et prix indicatifs 2026\n{prest}\n\n### Questions fréquentes\n{faq}\n")
    arts = "\n".join(f"- [{a['titre']}]({SITE}{a['slug']}) — {a['resume']}" for a in ARTICLES)
    full = court.replace("## Fiche complète\n"+SITE+"llms-full.txt\n","") + "\n# Détail par métier\n\n" + "\n".join(blocs) + f"\n# Conseils d'artisans\n{arts}\n\nDernière mise à jour : {DATE_MAJ}. Contenu publié par Atelier PACA, {SITE}\n"
    with open(os.path.join(ROOT,"llms-full.txt"),"w",encoding="utf-8") as f: f.write(full)
    with open(os.path.join(ROOT,"favicon.svg"),"w",encoding="utf-8") as f: f.write(FAVICON_SVG)
    with open(os.path.join(ROOT,"images","logo-atelier-paca.svg"),"w",encoding="utf-8") as f: f.write(LOGO_SVG.replace('<svg ','<svg xmlns="http://www.w3.org/2000/svg" ',1))
    os.makedirs(os.path.join(ROOT,".well-known"),exist_ok=True)
    with open(os.path.join(ROOT,".well-known","security.txt"),"w",encoding="utf-8") as f: f.write(f"Contact: mailto:{E['email']}\nPreferred-Languages: fr\nCanonical: {SITE}.well-known/security.txt\nExpires: 2027-10-14T00:00:00.000Z\n")

def page_liens():
    """Page « lien en bio » pour Instagram / Facebook : appel en un clic + accès direct aux 6 métiers.
    Non indexée (noindex) et hors sitemap : c'est une page de passage, pas une page de référencement."""
    titre = "Atelier PACA — Appeler, devis, nos 6 métiers"
    desc = "Atelier PACA, artisan à Antibes : appelez en un clic, demandez un devis gratuit ou choisissez votre métier (plomberie, chauffage, clim, électricité, volets, serrurerie)."
    htm = head(titre, desc, "liens.html").replace('<meta name="robots" content="index,follow,max-image-preview:large">', '<meta name="robots" content="noindex,follow">')
    css = """<style>
.lb{max-width:520px;margin:0 auto;padding:34px 18px 60px;text-align:center}
.lb .logo svg{width:250px;height:auto}
.lb .acc{color:var(--mut);margin:10px 0 6px;font-size:15px}
.lb .note{border:0;padding:0;background:none;display:inline-flex;align-items:center;gap:6px;font-size:14px;color:var(--or);margin-bottom:22px}
.lb .note svg{width:16px;height:16px}
.lb .btn{width:100%;margin-bottom:12px;font-size:18px;padding:18px 20px}
.lb .btn small{display:block;font-family:var(--inter);font-weight:500;font-size:13px;opacity:.85}
.lb h2{font-family:var(--sora);font-size:16px;letter-spacing:.5px;text-transform:uppercase;color:var(--mut);margin:26px 0 12px}
.lb .m{display:flex;align-items:center;gap:14px;text-align:left;padding:14px 16px;margin-bottom:10px;border:1px solid var(--line);border-radius:14px;background:rgba(255,255,255,.04);color:var(--txt);text-decoration:none}
.lb .m:hover{border-color:var(--line2);background:rgba(47,176,255,.08)}
.lb .m .ic{flex:none;width:42px;height:42px;border-radius:12px;display:grid;place-items:center;background:rgba(255,46,76,.12);color:var(--rouge2)}
.lb .m .ic svg{width:22px;height:22px}
.lb .m b{display:block;font-family:var(--sora);font-size:16px}
.lb .m span span{display:block;font-size:13px;color:var(--mut)}
.lb .m .fl{margin-left:auto;width:18px;height:18px;color:var(--mut2)}
.lb .pied{margin-top:28px;font-size:13px;color:var(--mut2)}
.lb .pied a{color:var(--mut)}
</style>"""
    metiers = "".join(f'<a class="m" href="{t["page"]}"><span class="ic">{ICO_METIER[t["cle"]]}</span><span><b>{t["nom"]}</b><span>{t["accroche"]}</span></span><span class="fl">{ICO["arrow"]}</span></a>' for t in TRADES)
    plus = (f'<a class="m" href="contrat-entretien.html"><span class="ic">{ICO["shield"]}</span><span><b>Contrat d&#39;entretien</b><span>Dépannage sous 48 h + 10 % sur les pièces</span></span><span class="fl">{ICO["arrow"]}</span></a>'
            f'<a class="m" href="avis-clients.html"><span class="ic">{ICO["star"]}</span><span><b>Avis clients</b><span>{E["note"]}/5 sur {E["avis"]} avis Google</span></span><span class="fl">{ICO["arrow"]}</span></a>'
            f'<a class="m" href="index.html"><span class="ic">{ICO["one"]}</span><span><b>Notre site</b><span>Villes d&#39;intervention, réalisations, conseils</span></span><span class="fl">{ICO["arrow"]}</span></a>')
    body = f'''<main class="lb">
<a href="index.html" class="logo" aria-label="Atelier PACA — accueil">{LOGO_SVG}</a>
<h1 class="acc">Plombier, chauffagiste, climatisation, électricien, volets et serrurier — Antibes, Alpes-Maritimes et Var est</h1>
<p class="note">{ICO["star"]}{ICO["star"]}{ICO["star"]}{ICO["star"]}{ICO["star"]} {E["note"]}/5 · {E["avis"]} avis Google</p>
<a href="{E["tel_href"]}" class="btn btn-rouge">{ICO["tel"]}<span>Appeler {E["tel"]}<small>Devis gratuit · intervention sous 48 h</small></span></a>
<a href="{E["wa"]}" class="btn btn-wa" target="_blank" rel="noopener">{ICO["wa"]}<span>WhatsApp {E["mobile"]}<small>Envoyez une photo de la panne</small></span></a>
<a href="contact.html#devis" class="btn btn-bleu">{ICO["doc"]}<span>Demander un devis en ligne</span></a>
<h2>Nos 6 métiers</h2>
{metiers}
<h2>Aussi</h2>
{plus}
<p class="pied">{E["nom"]} · {E["adresse"]}, {E["cp"]} {E["ville"]}<br><a href="mailto:{E["email"]}">{E["email"]}</a></p>
</main>
<script src="assets/site.js" defer></script>
</body>
</html>
'''
    with open(os.path.join(ROOT, "liens.html"), "w", encoding="utf-8") as f: f.write(htm.replace("</head>", css + "\n</head>") + body)

if __name__ == "__main__":
    page_index()
    for t in TRADES: page_metier(t)
    for v in VILLES: page_hub(v)
    for t in TRADES:
        for v in VILLES: page_metier_ville(t, v)
    pages_annexes()
    page_plan()
    pages_redirections()
    page_liens()
    sitemap()
    print(f"{len(PAGES)} pages générées (+ 404).")
