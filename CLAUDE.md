# CLAUDE.md — atelierpaca.fr

Site statique GitHub Pages, généré par `build/generer.py` à partir de `build/donnees.py`. Français partout (code, commits, docs).

Règles :
- Ne jamais éditer les pages HTML à la main : modifier `build/donnees.py` (ou `assets/site.css`), puis `python3 build/generer.py`.
- Conserver les URLs existantes (`<metier>-<ville>.html`, `depannage-<ville>.html`).
- NAP de référence : Atelier PACA, 04 92 14 14 14, 48 chemin des Autrichiens, 06600 Antibes, contact@atelierpaca.fr.
- Titres ≤ 60 caractères, descriptions ≤ 160, un seul H1 par page (vérifié par le générateur).
- Tarif minimum affiché : 110 € HT. Nombre d'avis : champ `avis` dans `donnees.py`.
