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
<a href="index.html" class="logo" aria-label="Atelier PACA — accueil">{LOGO_SVG}</a>
<nav class="nav" aria-label="Navigation principale">{nav}</nav>
<div class="hdr-cta"><a href="{E["tel_href"]}" class="tel-hdr">{ICO["tel"]}<span>{E["tel"]}</span></a>
<button class="burger" id="burger" aria-label="Menu" aria-expanded="false" aria-controls="menu-m">{ICO["menu"]}</button></div>
</div></header>
<div class="menu-m" id="menu-m">{menu}<a href="urgence-depannage-24h.html">Urgence 24h/24</a><a href="contrat-entretien.html">Contrats d'entretien</a><a href="depannage-antibes.html">Villes d'intervention</a><a href="avis-clients.html">Avis clients</a><a href="realisations.html">Réalisations</a><a href="blog.html">Conseils</a><a href="contact.html">Contact</a><p class="sub">{E["tel"]} · {E["email"]}</p></div>
'''

def villes_footer():
    out = []
    for t in TRADES:
        links = "".join(f'<a href="{t["prefix"]}-{v["slug"]}.html">{v["nom"]}</a>' for v in VILLES)
        out.append(f'<details><summary>{t["nom"]} — {len(VILLES)} villes</summary><div class="chips">{links}</div></details>')
    hubs = "".join(f'<a href="depannage-{v["slug"]}.html">{v["nom"]}</a>' for v in VILLES)
    out.append(f'<details><summary>Dépannage toutes prestations — {len(VILLES)} villes</summary><div class="chips">{hubs}</div></details>')
    return "".join(out)

def footer():
    return f'''<footer class="ftr"><div class="wrap">
<div class="g">
<div><a href="index.html" class="logo" aria-label="Atelier PACA">{LOGO_SVG}</a>
<p style="margin-top:14px;max-width:360px">Plomberie, chauffage, climatisation, électricité, volets roulants et serrurerie dans les Alpes-Maritimes et le Var, depuis {E["depuis"]}. Un seul numéro pour toute la maison.</p>
<p><strong>{E["note"]}/5</strong> sur {E["avis"]} avis Google · garantie décennale · astreinte 24h/24</p>
<div class="soc"><a href="{E["facebook"]}" target="_blank" rel="noopener" aria-label="Facebook Atelier PACA">{ICO["fb"]}</a><a href="{E["instagram"]}" target="_blank" rel="noopener" aria-label="Instagram Atelier PACA">{ICO["ig"]}</a><a href="{maps(AGENCES[0])}" target="_blank" rel="noopener" aria-label="Fiche Google Atelier PACA">{ICO["g"]}</a></div></div>
<div><h4>Nos métiers</h4>{"".join(f'<a href="{t["page"]}">{t["nom"]}</a>' for t in TRADES)}<a href="urgence-depannage-24h.html">Urgence 24h/24</a><a href="contrat-entretien.html">Contrats d'entretien</a></div>
<div><h4>Atelier PACA</h4><a href="a-propos.html">Qui sommes-nous</a><a href="avis-clients.html">Avis clients</a><a href="realisations.html">Réalisations</a><a href="marques.html">Marques installées</a><a href="blog.html">Conseils d'artisans</a><a href="faq.html">Questions fréquentes</a><a href="contact.html">Contact et devis</a></div>
<div><h4>Nos agences</h4>{"".join(f'<a href="{maps(a)}" target="_blank" rel="noopener">{a["nom"]} — {a["adresse"]}, {a["cp"]} {a["ville"]}</a>' for a in AGENCES)}<p style="margin-top:10px"><a href="{E["tel_href"]}"><strong>{E["tel"]}</strong></a><a href="mailto:{E["email"]}">{E["email"]}</a></p></div>
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

def faq_block(items, titre="Questions fréquentes", ctx=None):
    items = [(q.format(**ctx) if ctx else q, a.format(**ctx) if ctx else a) for q,a in items]
    htm = f'<h2>{titre}</h2><div class="faq">' + "".join(f'<details><summary>{esc(q)}</summary><div class="a"><p>{esc(a)}</p></div></details>' for q,a in items) + '</div>'
    ld = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in items]}
    return htm, ld

def ld_business(extra_type=None, agence=None):
    a = agence or AGENCES[0]
    types = ["LocalBusiness","Plumber","HVACBusiness","Electrician","Locksmith"]
    if extra_type and extra_type not in types: types.insert(1, extra_type)
    return {"@context":"https://schema.org","@type":types,"@id":SITE+"#organisation","name":"Atelier PACA",
      "url":SITE,"telephone":E["tel_intl"],"email":E["email"],"image":SITE+"images/og-atelier-paca.jpg","logo":SITE+"images/logo-atelier-paca.svg",
      "foundingDate":E["depuis"],"priceRange":"€€","currenciesAccepted":"EUR","paymentAccepted":"Carte bancaire, virement, chèque, espèces",
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
<div class="c"><div class="ic">{ICO["clock"]}</div><div><b>Horaires</b><span>Astreinte 7 j/7, 24 h/24 pour les urgences. Devis et rendez-vous du lundi au samedi.</span></div></div>
</div>'''

def write(fn, content, prio="0.6", freq="monthly"):
    with open(os.path.join(ROOT, fn), "w", encoding="utf-8") as f: f.write(content)
    PAGES.append((fn, prio, freq))

def chips_villes(prefix, cur=None):
    def grp(vs, titre, code):
        return f'<div><h3>{ICO["pin"]} {titre} <small>({code})</small></h3><div class="chips">' + "".join(f'<a href="{prefix}-{v["slug"]}.html"{" class=on" if v["slug"]==cur else ""}>{v["nom"]}</a>' for v in vs) + '</div></div>'
    return '<div class="villes">' + grp(VILLES_06, "Alpes-Maritimes", "06") + grp(VILLES_83, "Var est — Fréjus, Saint-Raphaël, pays de Fayence", "83") + '</div>'

def tarifs_block(t):
    cards = "".join(f'<div class="tarif"><div><b>{esc(n)}</b><p>{esc(d)}</p></div><div class="px"><b>{esc(p)}</b><small>{esc(u)}</small></div></div>' for _,n,d,p,u in t["prestations"])
    return f'<div class="tarifs">{cards}</div><p class="note">Tarif minimum d\'intervention : 110 € HT (TVA à 10 % ou 20 % selon la nature des travaux et l\'ancienneté du logement). Autres prix indicatifs 2026. Majoration possible la nuit, le week-end et les jours fériés, toujours annoncée avant le déplacement. Tarif définitif communiqué avant toute intervention.</p>'

# ---------------------------------------------------------------- ACCUEIL
def page_index():
    faq_htm, faq_ld = faq_block([
        ("Intervenez-vous vraiment pour tous les métiers de la maison ?","Oui : plomberie, chauffage, climatisation, électricité, volets roulants et serrurerie. Un seul numéro, une seule équipe, une seule facture, y compris quand un chantier mêle plusieurs métiers."),
        ("Sous quel délai intervenez-vous ?","Sous 48 h pour une intervention classique, plus vite pour une urgence (fuite, panne de chauffage, porte bloquée) grâce à l'astreinte 24h/24 et 7j/7."),
        ("Le devis est-il vraiment gratuit ?","Oui, le devis et la visite technique sont gratuits et sans engagement. Pour un dépannage, le prix est annoncé avant l'intervention."),
        ("Quelle zone couvrez-vous ?","Antibes et 20 km autour en priorité (Cagnes-sur-Mer, Villeneuve-Loubet, Cannes, Le Cannet, Mandelieu, Nice, Saint-Laurent-du-Var), les Alpes-Maritimes, et dans le Var : Fréjus, Saint-Raphaël et le pays de Fayence (10 km autour)."),
        ("Vos travaux sont-ils garantis ?","Oui : garantie décennale sur les travaux, matériel de grandes marques, facture détaillée et équipe joignable après l'intervention."),
    ])
    ld = [ld_business(), {"@context":"https://schema.org","@type":"WebSite","@id":SITE+"#site","url":SITE,"name":"Atelier PACA","inLanguage":"fr-FR","publisher":{"@id":SITE+"#organisation"}}, faq_ld]
    metiers = "".join(f'''<a class="metier" href="{t["page"]}"><img src="images/{t["img"]}-480.webp" srcset="images/{t["img"]}-480.webp 480w, images/{t["img"]}.webp 900w" sizes="(max-width:560px) 100vw, (max-width:900px) 50vw, 380px" alt="{esc(t["metier"])} Atelier PACA en intervention" loading="lazy" width="743" height="586">
<div class="in"><div class="ic">{ICO_METIER[t["cle"]]}</div><h3>{t["nom"]}</h3><p>{t["desc_court"]}</p></div><span class="go">{ICO["arrow"]}</span></a>''' for t in TRADES)
    avis = "".join(f'<div class="avis"><div class="st">★★★★★</div><p>« {esc(a)} »</p><div class="qui">{esc(n)}<span>{esc(w)}</span></div></div>' for a,n,w in AVIS)
    fiches = "".join(f'<div class="fiche"><b>{a["nom"]}</b><span>{a["adresse"]}, {a["cp"]} {a["ville"]}</span><span>{E["note"]}/5 · {a["avis"]} avis</span><div class="l"><a href="{maps(a)}" target="_blank" rel="noopener">Voir la fiche</a><a href="{avis_url(a)}" target="_blank" rel="noopener">Laisser un avis</a></div></div>' for a in AGENCES)
    hubs06 = "".join(f'<a href="depannage-{v["slug"]}.html">{v["nom"]}</a>' for v in VILLES_06)
    hubs83 = "".join(f'<a href="depannage-{v["slug"]}.html">{v["nom"]}</a>' for v in VILLES_83)
    body = header("index.html") + f'''
<main>
<section class="hero"><div class="wrap">
<div>
<span class="badge247"><i></i> Astreinte 24h/24 · 7j/7 — Antibes et Côte d'Azur</span>
<h1>Un seul numéro pour <span class="neon">toute votre maison</span>.</h1>
<p class="lead">Plomberie, chauffage, climatisation, électricité, volets roulants et serrurerie : une équipe locale basée à Antibes qui dépanne, entretient et installe dans les Alpes-Maritimes et le Var. Intervention sous 48 h, plus vite en urgence.</p>
<div class="btns"><a href="{E["tel_href"]}" class="btn btn-rouge">{ICO["tel"]} {E["tel"]}</a><a href="contact.html#devis" class="btn btn-bleu">{ICO["doc"]} Devis gratuit</a></div>
<div class="proof"><span>{ICO["star"]}<b>{E["note"]}/5</b> — {E["avis"]} avis Google</span><span>{ICO["shield"]}<b>Garantie décennale</b></span><span>{ICO["clock"]}<b>Prix annoncé</b> avant intervention</span></div>
</div>
<div style="position:relative"><div class="frame"><img src="images/hero-nuit.webp" srcset="images/hero-nuit-480.webp 480w, images/hero-nuit.webp 529w" sizes="(max-width:900px) 100vw, 480px" alt="Technicien Atelier PACA en intervention de nuit sur une climatisation, Côte d'Azur" width="529" height="774" fetchpriority="high" decoding="async"></div>
<div class="float f1"><div class="ic r">{ICO["clock"]}</div><div><b>Intervention sous 48 h</b><span>plus vite en urgence</span></div></div>
<div class="float f2"><div class="ic">{ICO["one"]}</div><div><b>6 métiers, 1 équipe</b><span>une seule facture</span></div></div></div>
</div></section>

<section class="wrap"><div class="chiffres">
<div class="chiffre"><b>{E["interventions"]}+</b><span>interventions réalisées depuis {E["depuis"]}</span></div>
<div class="chiffre"><b>{E["note"]}/5</b><span>sur {E["avis"]} avis Google vérifiés</span></div>
<div class="chiffre"><b>48 h</b><span>délai d'intervention, moins en urgence</span></div>
<div class="chiffre"><b>10 ans</b><span>de garantie décennale sur les travaux</span></div>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-h"><p class="kicker">Nos métiers</p><h2>Six métiers, une seule équipe</h2><p>Chaque technicien est spécialisé dans son métier. Ensemble, ils couvrent tout ce qui peut tomber en panne chez vous, sans que vous ayez à coordonner trois artisans.</p></div>
<div class="metiers">{metiers}</div>
</div></section>

<section class="sec" style="padding-top:0"><div class="wrap"><div class="offres">
<div class="offre r"><div><span class="tag">Avant l'hiver</span><h3>Entretien de chaudière avec attestation</h3><p>Nettoyage, réglage, contrôle sécurité et CO. Obligatoire chaque année pour le gaz, et la meilleure assurance contre la panne du premier soir froid.</p></div><div class="prix"><b>110 € HT</b><small>à partir de</small><a href="chauffage.html" class="btn btn-rouge btn-sm">Programmer l'entretien</a></div></div>
<div class="offre b"><div><span class="tag">Toute l'année</span><h3>Contrat d'entretien clim ou chaudière</h3><p>Visite annuelle programmée, dépannage sous 48 h, 10 % de remise sur les pièces détachées. Vous n'y pensez plus, on s'en occupe.</p></div><div class="prix"><b>1 visite</b><small>par an, programmée</small><a href="contrat-entretien.html" class="btn btn-bleu btn-sm">Voir les contrats</a></div></div>
</div></div></section>

<section class="sec" style="padding-top:0"><div class="wrap"><div class="pourquoi">
<div><div class="sec-h"><p class="kicker">Pourquoi Atelier PACA</p><h2>Ce qui change par rapport à un dépanneur classique</h2></div>
<div class="raisons">
<div class="raison"><div class="ic">{ICO["one"]}</div><div><b>Un numéro, six métiers</b><p>Fuite, panne de chauffage, clim, tableau électrique, volet bloqué, porte claquée : le même numéro, la même équipe, et une seule facture quand plusieurs métiers sont nécessaires.</p></div></div>
<div class="raison"><div class="ic">{ICO["euro"]}</div><div><b>Le prix avant, pas après</b><p>Tarif annoncé au téléphone ou sur devis avant toute intervention, nuit et week-end compris. Pas de surprise à la fin.</p></div></div>
<div class="raison"><div class="ic">{ICO["pin"]}</div><div><b>Une entreprise d'ici</b><p>Siège à Antibes, agences à Juan-les-Pins, Cagnes-sur-Mer et Le Cannet : nos techniciens connaissent les copropriétés, les villas et les contraintes de la côte.</p></div></div>
<div class="raison"><div class="ic">{ICO["shield"]}</div><div><b>Garantie décennale et grandes marques</b><p>Daikin, Mitsubishi Electric, Atlantic, Somfy, Legrand, Schneider : du matériel qui dure, posé par des techniciens formés, et garanti 10 ans.</p></div></div>
</div></div>
<div><div class="frame auto"><img src="images/equipe-camion.webp" srcset="images/equipe-camion-480.webp 480w, images/equipe-camion.webp 904w" sizes="(max-width:900px) 100vw, 520px" alt="Technicien Atelier PACA devant le camion d'intervention, baie de Cannes" loading="lazy" width="904" height="459" style="aspect-ratio:auto"></div></div>
</div></div></section>

<section class="sec" id="avis" style="padding-top:0"><div class="wrap">
<div class="sec-h c"><p class="kicker" style="justify-content:center">Avis clients</p><h2>{E["note"]}/5 sur {E["avis"]} avis Google</h2><p>Quatre fiches Google, plus de 450 avis au total. Les avis sont publics et vérifiables sur chaque fiche.</p></div>
<div class="avis-wrap">{avis}</div>
<div class="fiches">{fiches}</div>
</div></section>

<section class="sec" style="padding-top:0"><div class="wrap">
<div class="sec-h"><p class="kicker">Comment ça se passe</p><h2>Votre intervention en quatre étapes</h2></div>
<div class="etapes">
<div class="etape"><span class="n">1</span><b>Vous appelez ou écrivez</b><p>Téléphone, WhatsApp ou formulaire. Premier retour sous 2 h en journée, immédiat pour les urgences.</p></div>
<div class="etape"><span class="n">2</span><b>Diagnostic et prix</b><p>Un technicien évalue le besoin et fixe un prix ferme, validé avant de commencer. Devis gratuit pour les travaux.</p></div>
<div class="etape"><span class="n">3</span><b>Intervention soignée</b><p>Protection des lieux, travail dans les règles de l'art, chantier laissé propre.</p></div>
<div class="etape"><span class="n">4</span><b>Facture et garantie</b><p>Facture détaillée, garantie décennale, et une équipe joignable après l'intervention.</p></div>
</div></div></section>

<section class="sec" style="padding-top:0"><div class="wrap">
<div class="sec-h"><p class="kicker">Zone d'intervention</p><h2>Antibes, 20 km autour, et le proche Var</h2><p>Notre zone prioritaire va de Mandelieu à Nice. Dans le Var, nous couvrons Fréjus, Saint-Raphaël et le pays de Fayence, dans un rayon de 10 km autour de ces villes.</p></div>
<div class="villes"><div><h3>{ICO["pin"]} Alpes-Maritimes <small>(06)</small></h3><div class="chips">{hubs06}</div></div><div><h3>{ICO["pin"]} Var est <small>(83)</small></h3><div class="chips">{hubs83}</div></div></div>
</div></section>

<section class="sec" style="padding-top:0"><div class="wrap">{faq_htm}</div></section>

<section class="sec" id="devis" style="padding-top:0"><div class="wrap">
<div class="sec-h"><p class="kicker">Contact</p><h2>Demandez un devis gratuit</h2><p>Réponse sous 2 h en journée. Pour une urgence, appelez directement : {E["tel"]}.</p></div>
<div class="contact">{coord_block()}{form_devis()}</div>
</div></section>
</main>
''' + footer()
    write("index.html", head("Plombier, chauffagiste, électricien Antibes | Atelier PACA",
          "Atelier PACA, Antibes : plomberie, chauffage, clim, électricité, volets et serrurerie dans le 06 et le Var. Un seul numéro, devis gratuit, 4,9/5 sur 178 avis.",
          "", ld, preload="images/hero-nuit.webp") + body, "1.0", "weekly")

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
<section class="hero hero-mini"><div class="wrap">{c_htm}<p class="kicker">{t["accroche"]}</p><h1>{t["nom"]} dans les Alpes-Maritimes et le Var</h1>
<p class="lead">{esc(t["intro"][0])}</p>
<div class="btns" style="margin-top:22px"><a href="{E["tel_href"]}" class="btn btn-rouge">{ICO["tel"]} {E["tel"]}</a><a href="contact.html#devis" class="btn btn-bleu">{ICO["doc"]} Devis gratuit</a></div>
<div class="proof"><span>{ICO["star"]}<b>{E["note"]}/5</b> — {E["avis"]} avis</span><span>{ICO["clock"]}<b>Sous 48 h</b>, moins en urgence</span><span>{ICO["shield"]}<b>Décennale</b></span></div>
</div></section>
<section class="sec" style="padding-top:28px"><div class="wrap"><div class="page">
<div class="main">
<div class="photo-p"><img src="images/{t["img"]}.webp" srcset="images/{t["img"]}-480.webp 480w, images/{t["img"]}.webp 900w" sizes="(max-width:960px) 100vw, 780px" alt="{esc(t["metier"])} Atelier PACA en intervention dans les Alpes-Maritimes" width="886" height="481" loading="eager" decoding="async"></div>
<h2>Prestations et tarifs indicatifs</h2>
{tarifs_block(t)}
<h2>Ce que nous faisons en {t["nom"].lower()}</h2>
<p>{esc(t["intro"][1])}</p>
<ul class="liste">{services}</ul>
<h2>Notre façon de travailler</h2>
<div class="trio">{exp}</div>
<h2>Marques installées et dépannées</h2>
<div class="marques">{marques}</div>
<div class="encart"><div><b>Besoin d'un autre métier sur le même chantier ?</b><span>Nos plombiers, électriciens, chauffagistes et frigoristes travaillent ensemble : un interlocuteur, une facture.</span></div><a href="contact.html#devis" class="btn btn-rouge btn-sm">Demander un devis</a></div>
{faq_htm}
<h2>{t["nom"]} ville par ville</h2>
<p>Retrouvez nos délais, nos tarifs et nos conseils adaptés à votre commune.</p>
{chips_villes(t["prefix"])}
</div>
<aside class="side">
<div class="card"><h3>Appeler un {t["metier_min"]}</h3><p>Astreinte 24h/24, prix annoncé avant le déplacement.</p><a href="{E["tel_href"]}" class="btn btn-rouge">{ICO["tel"]} {E["tel"]}</a><a href="{E["wa"]}" class="btn btn-wa" target="_blank" rel="noopener">{ICO["wa"]} WhatsApp</a><a href="contact.html#devis" class="btn btn-bleu">{ICO["doc"]} Devis gratuit</a></div>
<div class="card"><h3>Atelier PACA</h3><p class="nap"><b>Siège Antibes</b><br>{E["adresse"]}<br>{E["cp"]} {E["ville"]}<br>{E["email"]}</p><p class="nap">{E["note"]}/5 — {E["avis"]} avis Google<br>Depuis {E["depuis"]} · {E["interventions"]}+ interventions</p></div>
<div class="card"><h3>Autres métiers</h3><div class="liens">{autres}<a href="urgence-depannage-24h.html">Urgence 24h/24</a><a href="contrat-entretien.html">Contrats d'entretien</a></div></div>
</aside>
</div></div></section>
{cta_final(f"Un projet ou une panne en {t['nom'].lower()} ?")}
</main>
''' + footer()
    write(t["page"], head(t["title"], t["meta"], t["page"], ld) + body, "0.9", "monthly")

# ---------------------------------------------------------------- PAGES MÉTIER × VILLE
def page_metier_ville(t, v):
    fn = f'{t["prefix"]}-{v["slug"]}.html'
    ctx = {"ville": v["nom"], "cp": v["cp"], "minutes": v["minutes"]}
    agence = next((a for a in AGENCES if a["cle"] == v.get("agence")), None)
    c_htm, c_ld = crumb([("Accueil","index.html"),(t["nom"],t["page"]),(v["nom"],fn)])
    faq_htm, faq_ld = faq_block(t["faq_ville"], f"Questions fréquentes — {t['nom'].lower()} à {v['nom']}", ctx)
    svc_ld = {"@context":"https://schema.org","@type":"Service","name":f"{t['nom']} à {v['nom']}","serviceType":t["nom"],"provider":{"@id":SITE+"#organisation"},"areaServed":{"@type":"City","name":v["nom"],"postalCode":v["cp"]},"url":SITE+fn}
    ld = [ld_business(t["schema"], agence), svc_ld, c_ld, faq_ld]
    quartiers = ", ".join(v["quartiers"])
    services = "".join(f'<li>{esc(s)}</li>' for s in t["services"])
    autres = "".join(f'<a href="{x["prefix"]}-{v["slug"]}.html">{x["nom"]} {v["nom"]}</a>' for x in TRADES if x is not t)
    voisines = "".join(f'<a href="{t["prefix"]}-{s}.html">{VILLE_BY_SLUG[s]["nom"]}</a>' for s in v["voisines"])
    if agence:
        local = f'<div class="loc"><div class="l"><b>Agence Atelier PACA — {agence["nom"]}</b><span>{agence["adresse"]}, {agence["cp"]} {agence["ville"]} · {E["note"]}/5 sur {agence["avis"]} avis · <a href="{maps(agence)}" target="_blank" rel="noopener">voir la fiche Google</a></span></div><div class="l"><b>Délai à {v["nom"]}</b><span>Intervention sous 48 h, souvent le jour même en urgence. Siège et stock à Antibes.</span></div></div>'
    else:
        local = f'<div class="loc"><div class="l"><b>Depuis Antibes</b><span>{v["nom"]} est à {v["minutes"]} de notre siège (48 chemin des Autrichiens). Stock de pièces et matériel embarqué.</span></div><div class="l"><b>Délai à {v["nom"]}</b><span>{"Intervention sous 48 h, souvent le jour même en urgence." if v["prio"] or v["dept"]=="06" else "Intervention sous 48 h ; urgences selon la disponibilité des équipes mobiles."}</span></div></div>'
    prio_txt = f'<h2>Atelier PACA à {v["nom"]}</h2><p>{esc(v["intro"])}</p><p>{esc(v["local"])}</p>' if v.get("local") else f'<h2>Atelier PACA à {v["nom"]}</h2><p>{esc(v["intro"])}</p>'
    body = header(t["page"]) + f'''
<main>
<section class="hero hero-mini"><div class="wrap">{c_htm}<p class="kicker">{t["sous_ville"]}</p><h1>{t["h1_ville"].format(**ctx)}</h1>
<p class="lead">{esc(t["metier"])} à {v["nom"]} ({v["cp"]}) : {t["accroche"].lower()} par l'équipe Atelier PACA, basée à Antibes. Prix annoncé avant intervention, devis gratuit, astreinte 24h/24.</p>
<div class="btns" style="margin-top:22px"><a href="{E["tel_href"]}" class="btn btn-rouge">{ICO["tel"]} {E["tel"]}</a><a href="contact.html#devis" class="btn btn-bleu">{ICO["doc"]} Devis gratuit</a></div>
<div class="proof"><span>{ICO["star"]}<b>{E["note"]}/5</b> — {E["avis"]} avis</span><span>{ICO["pin"]}<b>{v["nom"]}</b> et {v["quartiers"][1] if len(v["quartiers"])>1 else "ses environs"}</span><span>{ICO["shield"]}<b>Décennale</b></span></div>
</div></section>
<section class="sec" style="padding-top:28px"><div class="wrap"><div class="page">
<div class="main">
<div class="photo-p"><img src="images/{t["img"]}.webp" srcset="images/{t["img"]}-480.webp 480w, images/{t["img"]}.webp 900w" sizes="(max-width:960px) 100vw, 780px" alt="{esc(t["metier"])} Atelier PACA à {esc(v["nom"])}" width="886" height="481" loading="eager" decoding="async"></div>
{prio_txt}
{local}
<h2>Nos prestations {t["nom"].lower()} à {v["nom"]}</h2>
<p>{esc(t["intro"][0])}</p>
<ul class="liste">{services}</ul>
<h2>Tarifs indicatifs à {v["nom"]}</h2>
{tarifs_block(t)}
<h3>Quartiers couverts à {v["nom"]}</h3>
<p>Nous intervenons dans toute la commune : {esc(quartiers)}. Habitat le plus fréquent : {esc(v["habitat"])}.</p>
{faq_htm}
<h2>Les autres métiers Atelier PACA à {v["nom"]}</h2>
<div class="chips">{autres}<a href="depannage-{v["slug"]}.html" class="on">Tout le dépannage à {v["nom"]}</a></div>
<h3>{t["nom"]} dans les villes voisines</h3>
<div class="chips">{voisines}<a href="{t["page"]}">Toutes les villes</a></div>
</div>
<aside class="side">
<div class="card"><h3>{t["metier"]} à {v["nom"]}</h3><p>Astreinte 24h/24, prix annoncé avant le déplacement.</p><a href="{E["tel_href"]}" class="btn btn-rouge">{ICO["tel"]} {E["tel"]}</a><a href="{E["wa"]}" class="btn btn-wa" target="_blank" rel="noopener">{ICO["wa"]} WhatsApp</a><a href="contact.html#devis" class="btn btn-bleu">{ICO["doc"]} Devis gratuit</a></div>
<div class="card"><h3>{"Agence " + agence["nom"] if agence else "Atelier PACA — siège"}</h3><p class="nap">{(agence["adresse"] + "<br>" + agence["cp"] + " " + agence["ville"]) if agence else (E["adresse"] + "<br>" + E["cp"] + " " + E["ville"])}<br><a href="{maps(agence or AGENCES[0])}" target="_blank" rel="noopener">Itinéraire et avis Google</a></p><p class="nap">{E["note"]}/5 — {E["avis"]} avis Google<br>Depuis {E["depuis"]} · {E["interventions"]}+ interventions</p></div>
<div class="card"><h3>À lire</h3><div class="liens">{"".join(f'<a href="{a["slug"]}">{esc(a["titre"])}</a>' for a in ARTICLES)}</div></div>
</aside>
</div></div></section>
{cta_final(f"{t['metier']} à {v['nom']} : on vous rappelle sous 2 h", "Appelez, écrivez sur WhatsApp ou laissez vos coordonnées : un technicien vous répond avec un prix clair.")}
</main>
''' + footer()
    tt = t["title_ville"].format(**ctx)
    if len(tt) > 60: tt = t["title_court"].format(**ctx)
    write(fn, head(tt, t["meta_ville"].format(**ctx), fn, ld) + body, "0.8" if v["prio"] else "0.6", "monthly")

# ---------------------------------------------------------------- HUB VILLE
def page_hub(v):
    fn = f'depannage-{v["slug"]}.html'
    agence = next((a for a in AGENCES if a["cle"] == v.get("agence")), None)
    c_htm, c_ld = crumb([("Accueil","index.html"),("Villes","depannage-antibes.html"),(v["nom"],fn)])
    faq_htm, faq_ld = faq_block([
        (f"Quels métiers Atelier PACA couvre-t-il à {v['nom']} ?", "Plomberie, chauffage, climatisation, électricité, volets roulants et serrurerie, en dépannage, entretien et installation. Un seul numéro pour toute la maison."),
        (f"Sous quel délai intervenez-vous à {v['nom']} ?", f"Sous 48 h pour une intervention classique ; plus vite en urgence grâce à l'astreinte 24h/24. {v['nom']} est à {v['minutes']} de notre siège d'Antibes." if v["slug"]!="antibes" else "Sous 48 h pour une intervention classique, souvent le jour même en urgence : notre siège et nos stocks sont à Antibes."),
        (f"Le devis est-il gratuit à {v['nom']} ?", "Oui, devis et visite technique sont gratuits et sans engagement. Pour un dépannage, le prix est annoncé avant l'intervention, nuit et week-end compris."),
    ], f"Questions fréquentes — {v['nom']}")
    ld = [ld_business(None, agence), c_ld, faq_ld]
    hub = "".join(f'<a href="{t["prefix"]}-{v["slug"]}.html"><span class="ic">{ICO_METIER[t["cle"]]}</span><span><b>{t["metier"]} {v["nom"]}</b><span>{t["accroche"]}</span></span></a>' for t in TRADES)
    voisines = "".join(f'<a href="depannage-{s}.html">{VILLE_BY_SLUG[s]["nom"]}</a>' for s in v["voisines"])
    local = f'<p>{esc(v["local"])}</p>' if v.get("local") else ""
    agence_htm = f'<div class="loc"><div class="l"><b>Agence Atelier PACA — {agence["nom"]}</b><span>{agence["adresse"]}, {agence["cp"]} {agence["ville"]} · {E["note"]}/5 sur {agence["avis"]} avis · <a href="{maps(agence)}" target="_blank" rel="noopener">fiche Google</a> · <a href="{avis_url(agence)}" target="_blank" rel="noopener">laisser un avis</a></span></div><div class="l"><b>Quartiers</b><span>{esc(", ".join(v["quartiers"]))}</span></div></div>' if agence else f'<div class="loc"><div class="l"><b>Depuis notre siège d\'Antibes</b><span>{v["nom"]} est à {v["minutes"]}. Équipes mobiles avec stock embarqué.</span></div><div class="l"><b>Quartiers</b><span>{esc(", ".join(v["quartiers"]))}</span></div></div>'
    body = header("depannage-antibes.html") + f'''
<main>
<section class="hero hero-mini"><div class="wrap">{c_htm}<p class="kicker">Dépannage, entretien, installation</p><h1>Artisan à {v["nom"]} : six métiers, un numéro</h1>
<p class="lead">Plombier, chauffagiste, climatisation, électricien, volets roulants et serrurier à {v["nom"]} ({v["cp"]}). {esc(v["intro"])}</p>
<div class="btns" style="margin-top:22px"><a href="{E["tel_href"]}" class="btn btn-rouge">{ICO["tel"]} {E["tel"]}</a><a href="contact.html#devis" class="btn btn-bleu">{ICO["doc"]} Devis gratuit</a></div>
</div></section>
<section class="sec" style="padding-top:28px"><div class="wrap"><div class="page">
<div class="main">
<h2>Six métiers à {v["nom"]}, un seul numéro</h2>
<div class="hub">{hub}</div>
{agence_htm}
<h2>Atelier PACA à {v["nom"]}</h2>
{local}
<p>Habitat le plus fréquent à {v["nom"]} : {esc(v["habitat"])}. Nos techniciens adaptent le matériel aux contraintes locales (air salin, eau calcaire, copropriétés, résidences secondaires) et arrivent avec les pièces courantes pour finir en une visite.</p>
<ul class="liste"><li>Intervention sous 48 h, plus vite en urgence (astreinte 24h/24, 7j/7)</li><li>Prix annoncé avant intervention, devis gratuit pour les travaux</li><li>Garantie décennale, grandes marques, facture détaillée pour votre assurance</li><li>Plus de {E["interventions"]} interventions depuis {E["depuis"]}, {E["note"]}/5 sur {E["avis"]} avis Google</li></ul>
{faq_htm}
<h3>Villes voisines</h3><div class="chips">{voisines}</div>
</div>
<aside class="side">
<div class="card"><h3>Dépannage à {v["nom"]}</h3><p>Un technicien vous répond et annonce le prix avant de se déplacer.</p><a href="{E["tel_href"]}" class="btn btn-rouge">{ICO["tel"]} {E["tel"]}</a><a href="{E["wa"]}" class="btn btn-wa" target="_blank" rel="noopener">{ICO["wa"]} WhatsApp</a><a href="contact.html#devis" class="btn btn-bleu">{ICO["doc"]} Devis gratuit</a></div>
<div class="card"><h3>Urgence</h3><p>Fuite, panne de chauffage, porte claquée, volet bloqué ouvert : l'astreinte fonctionne 24h/24.</p><div class="liens"><a href="urgence-depannage-24h.html">Dépannage urgent 24h/24</a><a href="contrat-entretien.html">Contrats d'entretien</a><a href="avis-clients.html">Avis clients</a></div></div>
</aside>
</div></div></section>
{cta_final(f"Un artisan à {v['nom']} ?")}
</main>
''' + footer()
    tt = f"Artisan {v['nom']} — Plombier, électricien, clim | Atelier PACA"
    if len(tt) > 60: tt = f"Artisan {v['nom']} | Atelier PACA"
    write(fn, head(tt, f"Dépannage et travaux à {v['nom']} ({v['cp']}) : plomberie, chauffage, climatisation, électricité, volets, serrurerie. Un numéro, devis gratuit, 4,9/5.", fn, ld) + body, "0.8" if v["prio"] else "0.6", "monthly")

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
        ("Qu'est-ce qui est considéré comme une urgence ?","Une fuite que vous ne pouvez pas stopper, une absence totale de chauffage ou d'eau chaude en hiver, une panne électrique générale, une porte claquée ou une serrure forcée, un volet bloqué ouvert. Dans ces cas, nous intervenons sans attendre, 24h/24."),
        ("Combien coûte un dépannage de nuit ou le week-end ?","Le tarif de base est majoré hors horaires ouvrés. Cette majoration vous est annoncée au téléphone avant tout déplacement : vous décidez en connaissance de cause."),
        ("Que faire en attendant le technicien ?","Fuite : fermez le robinet d'arrêt général. Électricité : coupez le disjoncteur si l'eau est proche. Gaz : aérez, ne touchez à aucun interrupteur, sortez. Nous vous guidons au téléphone."),
    ], "Questions sur les urgences")
    urg = "".join(f'<a href="{t["page"]}"><span class="ic">{ICO_METIER[t["cle"]]}</span><span><b>{t["nom"]}</b><span>{t["accroche"]}</span></span></a>' for t in TRADES)
    page_simple("urgence-depannage-24h.html","Dépannage urgent 24h/24 Antibes, 06 & Var | Atelier PACA","Dépannage d'urgence 24h/24 dans le 06 et le Var : fuite d'eau, panne de chauffage, panne électrique, porte claquée, volet bloqué. Prix annoncé avant déplacement.",
        "Dépannage urgent 24h/24 dans les Alpes-Maritimes et le Var","Astreinte 7j/7",
        f'''<p>Une astreinte répond à toute heure. Le technicien de garde évalue la situation, vous donne les gestes de sécurité et annonce le prix avant de partir. Objectif : stopper les dégâts, puis réparer proprement.</p>
<div class="hub">{urg}</div>
<h2>Comment se passe une urgence</h2>
<div class="etapes"><div class="etape"><span class="n">1</span><b>Vous appelez</b><p>{E["tel"]}, 24h/24. Décrivez la panne : nous vous indiquons tout de suite les gestes à faire.</p></div><div class="etape"><span class="n">2</span><b>Prix annoncé</b><p>Déplacement et tarif de base annoncés au téléphone, majoration incluse si hors horaires.</p></div><div class="etape"><span class="n">3</span><b>Mise en sécurité</b><p>Le technicien stoppe le problème (fuite, court-circuit, porte) et sécurise les lieux.</p></div><div class="etape"><span class="n">4</span><b>Réparation</b><p>Réparation immédiate quand c'est possible, sinon devis gratuit pour la suite, sous 24 h.</p></div></div>
{faq_htm}''', ld_extra=[faq_ld], prio="0.8", lead="Fuite d'eau, chaudière en panne, coupure de courant, porte claquée, volet bloqué : un technicien de garde répond jour et nuit, week-end et jours fériés.")

    # Contrat d'entretien
    faq_htm, faq_ld = faq_block([
        ("Que comprend le contrat d'entretien ?","Une visite annuelle programmée (nettoyage, contrôles, réglages, attestation pour les chaudières), le dépannage sous 48 h en cas de panne, et 10 % de remise sur les pièces détachées."),
        ("Puis-je regrouper plusieurs équipements ?","Oui : chaudière + climatisation, ou plusieurs splits, sur un même contrat. Le tarif est dégressif à partir du deuxième équipement."),
        ("Comment résilier ?","Le contrat est annuel, sans reconduction forcée : vous restez libre chaque année."),
    ], "Questions sur les contrats")
    page_simple("contrat-entretien.html","Contrat d'entretien clim & chaudière Antibes | Atelier PACA","Contrat d'entretien annuel clim et chaudière dans le 06 et le Var : visite programmée, attestation, dépannage sous 48 h, 10 % de remise sur les pièces.",
        "Contrats d'entretien climatisation et chaudière","Vous n'y pensez plus, on s'en occupe",
        f'''<p>L'entretien annuel est la différence entre un appareil qui dure quinze ans et un appareil remplacé au bout de sept. Avec un contrat, la visite est programmée chaque année à la bonne saison, et vous passez en priorité en cas de panne.</p>
<h2>Les formules</h2>
<div class="tarifs">
<div class="tarif"><div><b>Chaudière gaz</b><p>Visite annuelle avant l'hiver, contrôle de combustion et de CO, attestation d'entretien, dépannage sous 48 h, 10 % de remise sur les pièces.</p></div><div class="px"><b>dès 110 € HT</b><small>TTC / an</small></div></div>
<div class="tarif"><div><b>Climatisation</b><p>Visite annuelle au printemps, nettoyage et désinfection, contrôle du circuit et des pressions, dépannage sous 48 h, 10 % de remise sur les pièces.</p></div><div class="px"><b>dès 110 € HT</b><small>TTC / an / split</small></div></div>
<div class="tarif"><div><b>Pompe à chaleur air/eau</b><p>Visite annuelle, contrôle d'étanchéité, filtres, régulation, dépannage sous 48 h, 10 % de remise sur les pièces.</p></div><div class="px"><b>Sur devis</b><small>gratuit</small></div></div>
<div class="tarif"><div><b>Copropriétés et professionnels</b><p>Parc d'équipements, plusieurs sites, interlocuteur dédié et reporting annuel.</p></div><div class="px"><b>Sur devis</b><small>gratuit</small></div></div>
</div>
<p class="note">Tarif dégressif à partir du deuxième équipement. Contrat annuel sans reconduction forcée.</p>
<h2>Ce que vous gagnez</h2>
<ul class="liste"><li>La visite est programmée par nos soins, à la bonne saison : vous n'avez rien à retenir</li><li>Dépannage sous 48 h en cas de panne</li><li>10 % de remise sur les pièces détachées</li><li>Attestation d'entretien pour votre assureur ou votre propriétaire (chaudière)</li><li>Historique des interventions conservé : utile à la revente ou pour un sinistre</li></ul>
{faq_htm}''', ld_extra=[faq_ld], prio="0.8", lead="Visite annuelle programmée, dépannage sous 48 h et 10 % de remise sur les pièces détachées, pour votre chaudière ou votre climatisation.")

    # Avis clients
    avis = "".join(f'<div class="avis"><div class="st">★★★★★</div><p>« {esc(a)} »</p><div class="qui">{esc(n)}<span>{esc(w)}</span></div></div>' for a,n,w in AVIS)
    fiches = "".join(f'<div class="fiche"><b>{a["nom"]}</b><span>{a["adresse"]}, {a["cp"]} {a["ville"]}</span><span>{E["note"]}/5 · {a["avis"]} avis</span><div class="l"><a href="{maps(a)}" target="_blank" rel="noopener">Voir la fiche</a><a href="{avis_url(a)}" target="_blank" rel="noopener">Laisser un avis</a></div></div>' for a in AGENCES)
    page_simple("avis-clients.html","Avis clients Atelier PACA — 4,9/5 sur Google | Antibes","Les avis Google des clients d'Atelier PACA : 4,9/5 sur 178 avis à Antibes et plus de 450 avis sur nos 4 fiches (Antibes, Juan-les-Pins, Cagnes, Le Cannet).",
        f"{E['note']}/5 — ce que disent nos clients","Avis vérifiables sur Google",
        f'''<p>Nous ne sélectionnons pas les avis et nous n'offrons rien en échange : tout ce qui est écrit sur nos fiches Google est public, daté et vérifiable. Voici quelques-uns des derniers retours, et les liens vers chaque fiche.</p>
<div class="avis-wrap" style="grid-template-columns:1fr">{avis}</div>
<h2>Nos quatre fiches Google</h2>
<div class="fiches" style="grid-template-columns:1fr 1fr">{fiches}</div>
<h2>Vous avez fait appel à nous ?</h2>
<p>Un avis prend deux minutes et aide les habitants de votre ville à choisir un artisan sérieux. Choisissez la fiche de l'agence la plus proche de chez vous ci-dessus et cliquez sur « Laisser un avis ».</p>''', prio="0.7", lead="Quatre fiches Google, plus de 450 avis publics. Nous n'offrons rien contre un avis et ne trions pas les clients.")

    # À propos
    page_simple("a-propos.html","Artisans à Antibes depuis 2015 | Atelier PACA","Atelier PACA, entreprise artisanale d'Antibes depuis 2015 : six métiers de la maison, garantie décennale, 10 800 interventions, 4,9/5 sur Google.",
        "Une entreprise d'Antibes, six métiers, depuis 2015","Qui sommes-nous",
        f'''<div class="photo-p"><img src="images/equipe-camion.webp" alt="Technicien Atelier PACA et camion d'intervention sur la Côte d'Azur" width="904" height="459" loading="eager"></div>
<p>Atelier PACA est née à Antibes en {E["depuis"]} avec une idée simple : les habitants de la côte n'ont pas envie de chercher un plombier, puis un électricien, puis un frigoriste. Ils veulent un numéro, un interlocuteur qui connaît leur logement, et une facture claire.</p>
<p>Dix ans plus tard, l'équipe a réalisé plus de {E["interventions"]} interventions dans les Alpes-Maritimes et le Var, et quatre fiches Google (Antibes, Juan-les-Pins, Cagnes-sur-Mer, Le Cannet) cumulent plus de 450 avis à {E["note"]}/5.</p>
<h2>Ce qui nous distingue</h2>
<div class="trio">
<div class="t"><b>Garantie décennale</b><p>Tous nos travaux sont couverts dix ans. Attestation fournie sur demande.</p></div>
<div class="t"><b>Prix avant intervention</b><p>Tarif annoncé au téléphone ou sur devis, majoration de nuit annoncée aussi.</p></div>
<div class="t"><b>Astreinte 24h/24</b><p>Un technicien de garde chaque nuit, chaque week-end, chaque jour férié.</p></div>
<div class="t"><b>Techniciens spécialisés</b><p>Chacun exerce son métier ; l'équipe couvre les six.</p></div>
<div class="t"><b>Grandes marques</b><p>Daikin, Mitsubishi Electric, Atlantic, Somfy, Legrand, Schneider, Vaillant.</p></div>
<div class="t"><b>Fournisseurs locaux</b><p>Stock au siège d'Antibes et partenaires de proximité pour les pièces.</p></div>
</div>
<h2>Nos agences</h2>
<div class="fiches" style="grid-template-columns:1fr 1fr">{"".join(f'<div class="fiche"><b>{a["nom"]}</b><span>{a["adresse"]}, {a["cp"]} {a["ville"]}</span><span>{E["note"]}/5 · {a["avis"]} avis</span><div class="l"><a href="{maps(a)}" target="_blank" rel="noopener">Fiche Google</a></div></div>' for a in AGENCES)}</div>
<h2>Informations légales</h2>
<p>Atelier PACA, SASU — SIREN {E["siren"]} — siège : {E["adresse"]}, {E["cp"]} {E["ville"]}. Assurance responsabilité civile et décennale. <a href="mentions-legales.html">Mentions légales</a>.</p>''', prio="0.6")

    # Réalisations
    gal = [("chantier-clim-interieur","Pose d'une unité intérieure de climatisation, appartement à Antibes","Climatisation"),
           ("chantier-clim-groupe-exterieur","Unité extérieure sur supports antivibratiles, villa du Cap d'Antibes","Climatisation"),
           ("chantier-douche-italienne","Douche à l'italienne, rénovation complète de salle de bain","Plomberie"),
           ("chantier-salle-de-bain","Salle de bain rénovée : plomberie, électricité et finitions","Plomberie et électricité"),
           ("chantier-wc-suspendu","WC suspendu avec bâti-support, Cagnes-sur-Mer","Plomberie"),
           ("volets-cote-azur","Volets roulants motorisés sur façade azuréenne","Volets roulants"),
           ("serrurerie-porte-blindee","Serrure multipoints haute sécurité sur porte blindée","Serrurerie"),
           ("entretien-clim-avant-apres","Entretien de climatisation : avant / après nettoyage des filtres et de l'échangeur","Climatisation"),
           ("camion-fondu","Le camion d'intervention Atelier PACA, équipé pour six métiers","Équipe")]
    galerie = "".join(f'<figure><img src="images/{i}.webp" alt="{esc(c)}" loading="lazy" width="800" height="600"><figcaption><strong>{m}</strong> — {esc(c)}</figcaption></figure>' for i,c,m in gal)
    page_simple("realisations.html","Réalisations Atelier PACA — Chantiers dans le 06 et le Var","Photos de chantiers Atelier PACA : climatisation, salle de bain, électricité, volets roulants et serrurerie dans les Alpes-Maritimes et le Var.",
        "Nos réalisations sur la Côte d'Azur","Chantiers récents",
        f'<p>Quelques chantiers récents, photographiés par nos techniciens. Nous ajoutons de nouvelles photos chaque semaine sur nos fiches Google et nos réseaux.</p><div class="galerie">{galerie}</div>', prio="0.6")

    # Marques
    marques = "".join(f'<h3>{t["nom"]}</h3><div class="marques">{"".join(f"<span>{esc(m)}</span>" for m in t["marques"])}</div>' for t in TRADES)
    page_simple("marques.html","Marques : Daikin, Mitsubishi, Atlantic, Somfy | Atelier PACA","Les marques installées et dépannées par Atelier PACA dans le 06 et le Var : Daikin, Mitsubishi Electric, Atlantic, Vaillant, Somfy, Legrand, Schneider, Fichet.",
        "Les marques que nous installons et dépannons","Matériel de grandes marques",
        f'<p>Nous choisissons des marques pour leur fiabilité et la disponibilité des pièces dans dix ans. Nos techniciens sont formés sur ces gammes et dépannent aussi les autres marques du marché.</p>{marques}', prio="0.5")

    # FAQ générale
    allfaq = []
    for t in TRADES: allfaq += t["faq"][:3]
    faq_htm, faq_ld = faq_block([("Sous quel délai intervenez-vous ?","Sous 48 h pour une intervention classique, plus vite pour une urgence grâce à l'astreinte 24h/24 et 7j/7."),
                                 ("Le devis est-il gratuit ?","Oui, devis et visite technique sont gratuits et sans engagement. Pour un dépannage, le prix est annoncé avant l'intervention."),
                                 ("Quelle zone couvrez-vous ?","Antibes et 20 km autour en priorité, les Alpes-Maritimes, et dans le Var : Fréjus, Saint-Raphaël et le pays de Fayence (10 km autour)."),
                                 ("Comment payer ?","Carte bancaire, virement, chèque ou espèces. Facture détaillée remise à chaque intervention."),
                                 ("Travaillez-vous avec les assurances et les syndics ?","Oui : rapport d'intervention et facture détaillée pour les déclarations de sinistre, documents techniques pour les demandes aux syndics.")] + allfaq, "Toutes les questions")
    page_simple("faq.html","Questions fréquentes — Délais, devis, tarifs | Atelier PACA","Les réponses d'Atelier PACA sur les délais, le devis gratuit, les tarifs, les urgences 24h/24, les garanties et la zone d'intervention dans le 06 et le Var.",
        "Questions fréquentes","Délais, prix, garanties", faq_htm, ld_extra=[faq_ld], prio="0.5")

    # Contact
    cp_ld = {"@context":"https://schema.org","@type":"ContactPage","url":SITE+"contact.html","name":"Contact Atelier PACA"}
    agences = "".join(f'<div class="fiche"><b>{a["nom"]}</b><span>{a["adresse"]}, {a["cp"]} {a["ville"]}</span><span>{E["note"]}/5 · {a["avis"]} avis</span><div class="l"><a href="{maps(a)}" target="_blank" rel="noopener">Itinéraire</a></div></div>' for a in AGENCES)
    c_htm, c_ld = crumb([("Accueil","index.html"),("Contact","contact.html")])
    body = header("contact.html") + f'''<main>
<section class="hero hero-mini"><div class="wrap">{c_htm}<p class="kicker">Devis gratuit, réponse sous 2 h</p><h1>Contactez Atelier PACA</h1><p class="lead">Pour une urgence, appelez : un technicien de garde répond 24h/24. Pour un devis, laissez vos coordonnées et nous vous rappelons sous 2 h en journée.</p></div></section>
<section class="sec" style="padding-top:28px" id="devis"><div class="wrap"><div class="contact">{coord_block()}{form_devis()}</div>
<h2 style="margin-top:50px">Nos agences</h2><div class="fiches">{agences}</div></div></section>
</main>''' + footer()
    write("contact.html", head("Contact — Devis gratuit, 04 92 14 14 14 | Atelier PACA","Contactez Atelier PACA : 04 92 14 14 14 (24h/24), WhatsApp, formulaire de devis gratuit. Agences à Antibes, Juan-les-Pins, Cagnes-sur-Mer et Le Cannet.","contact.html",[ld_business(),cp_ld,c_ld]) + body, "0.8")

    # Blog + articles
    posts = "".join(f'<a class="post" href="{a["slug"]}"><img src="images/{a["img"]}-480.webp" alt="" loading="lazy" width="480" height="300"><div class="in"><h3>{esc(a["titre"])}</h3><p>{esc(a["resume"])}</p><small>Lire l\'article</small></div></a>' for a in ARTICLES)
    page_simple("blog.html","Conseils clim, chauffage, plomberie | Atelier PACA","Les conseils d'Atelier PACA : entretien de chaudière, prix d'une climatisation dans le 06, gestes en cas de fuite d'eau. Écrits par nos techniciens d'Antibes.",
        "Conseils d'artisans","Le blog Atelier PACA", f'<p>Des articles courts, écrits par nos techniciens, pour vous aider à décider et à éviter les pannes.</p><div class="posts" style="grid-template-columns:1fr">{posts}</div>', prio="0.6")
    for a in ARTICLES:
        c_htm, c_ld = crumb([("Accueil","index.html"),("Conseils","blog.html"),(a["titre"],a["slug"])])
        art_ld = {"@context":"https://schema.org","@type":"Article","headline":a["titre"],"description":a["desc"],"datePublished":a["date"],"dateModified":a["date"],"inLanguage":"fr-FR","image":SITE+f"images/{a['img']}.webp","author":{"@type":"Organization","name":"Atelier PACA","url":SITE},"publisher":{"@id":SITE+"#organisation"},"mainEntityOfPage":SITE+a["slug"]}
        body = header("blog.html") + f'''<main>
<section class="hero hero-mini"><div class="wrap">{c_htm}<p class="kicker">Conseil d'artisan</p><h1>{esc(a["titre"])}</h1><p class="meta" style="color:var(--mut2);font-size:13.5px;margin-top:10px">Publié le 14 octobre 2026 par l'équipe Atelier PACA, Antibes</p></div></section>
<section class="sec" style="padding-top:28px"><div class="wrap"><div class="page"><div class="main article"><div class="photo-p"><img src="images/{a["img"]}.webp" alt="" width="886" height="481" loading="eager"></div>{a["corps"]}
<div class="encart"><div><b>Une question sur votre installation ?</b><span>Devis gratuit, réponse sous 2 h en journée.</span></div><a href="contact.html#devis" class="btn btn-rouge btn-sm">Demander un devis</a></div>
<h3>Autres conseils</h3><div class="chips">{"".join(f'<a href="{x["slug"]}">{esc(x["titre"])}</a>' for x in ARTICLES if x is not a)}</div></div>
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
    sec = f'<h2>Pages principales</h2><ul class="liste"><li><a href="index.html">Accueil</a></li>' + "".join(f'<li><a href="{t["page"]}">{t["nom"]}</a></li>' for t in TRADES) + '<li><a href="urgence-depannage-24h.html">Dépannage urgent 24h/24</a></li><li><a href="contrat-entretien.html">Contrats d\'entretien</a></li><li><a href="avis-clients.html">Avis clients</a></li><li><a href="a-propos.html">Qui sommes-nous</a></li><li><a href="realisations.html">Réalisations</a></li><li><a href="marques.html">Marques</a></li><li><a href="faq.html">Questions fréquentes</a></li><li><a href="blog.html">Conseils</a></li>' + "".join(f'<li><a href="{a["slug"]}">{esc(a["titre"])}</a></li>' for a in ARTICLES) + '<li><a href="contact.html">Contact</a></li><li><a href="mentions-legales.html">Mentions légales</a></li></ul>'
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
    with open(os.path.join(ROOT,"robots.txt"),"w",encoding="utf-8") as f: f.write(f"User-agent: *\nAllow: /\nDisallow: /build/\n\nSitemap: {SITE}sitemap.xml\n")
    with open(os.path.join(ROOT,"favicon.svg"),"w",encoding="utf-8") as f: f.write(FAVICON_SVG)
    with open(os.path.join(ROOT,"images","logo-atelier-paca.svg"),"w",encoding="utf-8") as f: f.write(LOGO_SVG.replace('<svg ','<svg xmlns="http://www.w3.org/2000/svg" ',1))
    os.makedirs(os.path.join(ROOT,".well-known"),exist_ok=True)
    with open(os.path.join(ROOT,".well-known","security.txt"),"w",encoding="utf-8") as f: f.write(f"Contact: mailto:{E['email']}\nPreferred-Languages: fr\nCanonical: {SITE}.well-known/security.txt\nExpires: 2027-10-14T00:00:00.000Z\n")

if __name__ == "__main__":
    page_index()
    for t in TRADES: page_metier(t)
    for v in VILLES: page_hub(v)
    for t in TRADES:
        for v in VILLES: page_metier_ville(t, v)
    pages_annexes()
    page_plan()
    pages_redirections()
    sitemap()
    print(f"{len(PAGES)} pages générées (+ 404).")
