# atelierpaca.fr — site Atelier PACA (version octobre 2026)

Site statique (GitHub Pages). **Ne pas modifier les pages HTML à la main** : elles sont générées.

## Modifier le site
1. Éditer `build/donnees.py` (textes, tarifs, villes, FAQ, articles, coordonnées) ou `assets/site.css` (design).
2. Lancer depuis la racine : `python3 build/generer.py`
3. Vérifier dans le navigateur, puis `git add . && git commit -m "..." && git push`.

## Structure
- `index.html` — accueil
- `climatisation.html`, `plomberie.html`, `electricite.html`, `chauffage.html`, `serrurerie.html`, `volets-roulants.html` — 6 pages métier
- `depannage-<ville>.html` — 26 pages « hub » ville (tous métiers)
- `<metier>-<ville>.html` — 156 pages métier × ville (URLs inchangées)
- `urgence-depannage-24h.html`, `contrat-entretien.html`, `avis-clients.html`, `a-propos.html`, `realisations.html`, `marques.html`, `faq.html`, `blog.html` + 3 articles, `contact.html`, `mentions-legales.html`, `plan-du-site.html`, `404.html`
- `assets/site.css`, `assets/site.js` — un seul CSS/JS pour tout le site
- `images/` — visuels WebP, `og-atelier-paca.jpg` (partage réseaux), `logo-atelier-paca.svg`
- `sitemap.xml`, `robots.txt`, `favicon.svg`, `.well-known/security.txt`, `CNAME`, fichier de vérification Google

## Règles à respecter (cohérence Google)
- NAP : Atelier PACA, 04 92 14 14 14, 48 chemin des Autrichiens, 06600 Antibes, contact@atelierpaca.fr
- Nombre d'avis affiché : 178 (champ `avis` dans `donnees.py`) — mettre à jour tous les 2-3 mois
- Les 4 agences / fiches Google sont dans `AGENCES` (donnees.py)
