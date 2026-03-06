# ============================================
# Xoolal Browser - Moteur de recherche
# © 2024 Ismaïla Mbodji
# ============================================

MOTEURS = {
    "Google":     "https://www.google.com/search?q=",
    "Bing":       "https://www.bing.com/search?q=",
    "DuckDuckGo": "https://duckduckgo.com/?q=",
    "Qwant":      "https://www.qwant.com/?q=",
    "Yahoo":      "https://search.yahoo.com/search?p=",
    "Ecosia":     "https://www.ecosia.org/search?q=",
}

MOTEUR_ACTUEL = "Google"

def get_url_recherche(texte):
    base = MOTEURS.get(MOTEUR_ACTUEL, MOTEURS["Google"])
    return base + texte.replace(" ", "+")

def get_moteurs():
    return list(MOTEURS.keys())
