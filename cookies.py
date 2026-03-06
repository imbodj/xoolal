# ============================================
# Xoolal Browser v1.4
# © 2024 Ismaïla Mbodji
# Tous droits réservés / All rights reserved
# 🇸🇳 Navigateur sénégalais sécurisé
# ============================================

import sys
import os
import json
import urllib.request
from datetime import datetime
from bloqueur import DOMAINES_PUB, SCRIPT_BLOQUEUR, est_pub
from moteur import get_url_recherche, get_moteurs, MOTEURS
import moteur as MOTEUR_MODULE
from cookies import charger_config, sauvegarder_config, cookie_autorise, COOKIES_ESPIONS
from PyQt5.QtGui import QColor, QKeySequence
from PyQt5.QtWidgets import (QApplication, QMainWindow, QToolBar,
                              QLineEdit, QAction, QLabel, QTabWidget,
                              QDialog, QVBoxLayout, QHBoxLayout, QListWidget,
                              QPushButton, QInputDialog, QMessageBox,
                              QFileDialog, QMenu, QToolButton, QShortcut,
                              QComboBox, QCheckBox, QListWidgetItem)
from PyQt5.QtWebEngineWidgets import (QWebEngineView, QWebEnginePage,
                                      QWebEngineSettings, QWebEngineProfile,
                                      QWebEngineScript)
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
from PyQt5.QtCore import QUrl, Qt, QTimer

SITES_BLOQUES = ["malware.com", "phishing.com", "dangereux.net"]
SITES_DANGEREUX = ["free-virus-scan.com", "win-prize.com", "malware-site.net"]
MODE_ENFANT = False
SITES_ENFANT = ["wikipedia.org", "khanacademy.org", "education.fr", "youtube.com"]
MODE_SOMBRE = False
MODE_PRIVE = False
BLOQUEUR_ACTIF = True
ISOLATION_ACTIVE = True
MOT_DE_PASSE = "1234"
STATS_PUBS = {"bloquees": 0}
LISTE_NOIRE = set()
FICHIER_LISTE_NOIRE = "liste_noire.txt"
COMPTEUR_ONGLETS = 0

# Charger config cookies
CONFIG_COOKIES = charger_config()

def charger_liste_noire():
    global LISTE_NOIRE
    if os.path.exists(FICHIER_LISTE_NOIRE):
        with open(FICHIER_LISTE_NOIRE, "r") as f:
            for ligne in f:
                ligne = ligne.strip()
                if ligne and not ligne.startswith("#"):
                    parts = ligne.split()
                    if len(parts) >= 2:
                        LISTE_NOIRE.add(parts[1].lower())
    print(f"✅ Liste noire : {len(LISTE_NOIRE)} domaines")

def mettre_a_jour_liste_noire():
    try:
        url = "https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts"
        urllib.request.urlretrieve(url, FICHIER_LISTE_NOIRE)
        charger_liste_noire()
        return True
    except Exception as e:
        print(f"❌ Erreur : {e}")
        return False

STYLE_CLAIR = """
    QMainWindow { background-color: white; }
    QToolBar {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            stop:0 #00853F, stop:0.5 #FDEF42, stop:1 #E31B23);
        padding: 4px; spacing: 2px; border: none;
    }
    QToolButton {
        background-color: rgba(255,255,255,0.3);
        color: white; font-size: 13px; font-weight: bold;
        border-radius: 6px; padding: 4px 8px;
    }
    QToolButton:hover { background-color: rgba(255,255,255,0.6); color: black; }
    QToolButton::menu-indicator { image: none; }
    QLineEdit {
        background-color: white; border-radius: 15px;
        padding: 4px 15px; font-size: 14px; border: none; color: black;
    }
    QComboBox {
        background-color: rgba(255,255,255,0.3); color: white;
        font-size: 12px; font-weight: bold;
        border-radius: 6px; padding: 3px 8px; border: none;
    }
    QComboBox::drop-down { border: none; }
    QComboBox QAbstractItemView {
        background-color: white; color: black;
        border: 2px solid #00853F;
    }
    QTabBar::tab {
        background-color: #00853F; color: white;
        padding: 6px 12px; margin-right: 2px;
        border-radius: 5px 5px 0 0; font-weight: bold;
    }
    QTabBar::tab:selected { background-color: #FDEF42; color: black; }
    QTabBar::tab:hover { background-color: #E31B23; color: white; }
    QMenu {
        background-color: white; border: 2px solid #00853F;
        border-radius: 8px; padding: 5px;
    }
    QMenu::item { padding: 10px 20px; font-size: 14px; border-radius: 5px; }
    QMenu::item:selected { background-color: #00853F; color: white; }
    QMenu::separator { height: 1px; background-color: #ddd; margin: 4px 10px; }
"""

STYLE_SOMBRE = """
    QMainWindow { background-color: #1a1a1a; }
    QToolBar {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            stop:0 #005a2b, stop:0.5 #b8a000, stop:1 #9e1219);
        padding: 4px; spacing: 2px; border: none;
        border-bottom: 2px solid #00853F;
    }
    QToolButton {
        background-color: rgba(0,0,0,0.3); color: white;
        font-size: 13px; font-weight: bold;
        border-radius: 6px; padding: 4px 8px;
    }
    QToolButton:hover { background-color: rgba(255,255,255,0.2); color: white; }
    QToolButton::menu-indicator { image: none; }
    QLineEdit {
        background-color: #2d2d2d; border-radius: 15px;
        padding: 4px 15px; font-size: 14px;
        border: 1px solid #00853F; color: white;
    }
    QComboBox {
        background-color: rgba(0,0,0,0.3); color: white;
        font-size: 12px; font-weight: bold;
        border-radius: 6px; padding: 3px 8px; border: none;
    }
    QComboBox::drop-down { border: none; }
    QComboBox QAbstractItemView {
        background-color: #2d2d2d; color: white;
        border: 2px solid #00853F;
    }
    QTabBar::tab {
        background-color: #1a1a1a; color: #aaaaaa;
        padding: 6px 12px; margin-right: 2px;
        border-radius: 5px 5px 0 0; font-weight: bold;
        border-top: 2px solid #00853F;
    }
    QTabBar::tab:selected {
        background-color: #2d2d2d;
        color: #FDEF42; border-top: 2px solid #FDEF42;
    }
    QTabBar::tab:hover {
        background-color: #2d2d2d;
        color: #E31B23; border-top: 2px solid #E31B23;
    }
    QMenu {
        background-color: #2d2d2d; border: 2px solid #00853F;
        border-radius: 8px; padding: 5px; color: white;
    }
    QMenu::item { padding: 10px 20px; font-size: 14px; border-radius: 5px; }
    QMenu::item:selected { background-color: #00853F; color: white; }
    QMenu::separator { height: 1px; background-color: #555; margin: 4px 10px; }
    QDialog { background-color: #1a1a1a; color: white; }
    QListWidget { background-color: #2d2d2d; color: white; border: none; }
    QPushButton {
        background-color: #00853F; color: white;
        border-radius: 8px; padding: 8px; font-weight: bold;
    }
    QPushButton:hover { background-color: #E31B23; }
    QCheckBox { color: white; font-size: 13px; }
"""

FICHIER_FAVORIS = "favoris.json"
FICHIER_HISTORIQUE = "historique.json"

def charger_json(fichier):
    if os.path.exists(fichier):
        with open(fichier, "r") as f:
            return json.load(f)
    return []

def sauvegarder_json(fichier, data):
    with open(fichier, "w") as f:
        json.dump(data, f)

class PageSecurisee(QWebEnginePage):
    def __init__(self, profile, parent=None):
        super().__init__(profile, parent)
        self.injecter_bloqueur()

    def injecter_bloqueur(self):
        script = QWebEngineScript()
        script.setName("xoolal_bloqueur")
        script.setSourceCode(SCRIPT_BLOQUEUR)
        script.setInjectionPoint(QWebEngineScript.DocumentReady)
        script.setWorldId(QWebEngineScript.MainWorld)
        script.setRunsOnSubFrames(True)
        self.scripts().insert(script)

    def acceptNavigationRequest(self, url, nav_type, is_main_frame):
        host = url.host().lower()
        if BLOQUEUR_ACTIF and est_pub(host):
            STATS_PUBS["bloquees"] += 1
            return False
        for site in SITES_DANGEREUX:
            if site in host:
                reponse = QMessageBox.warning(
                    None, "⚠️ Site Dangereux !",
                    f"🛡️ Site dangereux !\n🔗 {host}\n\nContinuer ?",
                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if reponse == QMessageBox.No:
                    return False
        if host in LISTE_NOIRE:
            return False
        if MODE_ENFANT:
            if not any(s in host for s in SITES_ENFANT):
                return False
        for site in SITES_BLOQUES:
            if site in host:
                return False
        return True

class Navigateur(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Xoolal 🇸🇳")
        self.setGeometry(100, 100, 1400, 800)
        self.favoris = charger_json(FICHIER_FAVORIS)
        self.historique = charger_json(FICHIER_HISTORIQUE)
        self.telechargements = []
        self.zoom_actuel = 1.0
        self.profils_onglets = {}
        self.setStyleSheet(STYLE_CLAIR)

        charger_liste_noire()

        self.profil_normal = QWebEngineProfile.defaultProfile()
        self.profil_prive_partage = QWebEngineProfile(self)
        self.profil_prive_partage.setHttpCacheType(QWebEngineProfile.NoCache)
        self.profil_prive_partage.setPersistentCookiesPolicy(
            QWebEngineProfile.NoPersistentCookies)

        barre = QToolBar()
        barre.setMovable(False)
        self.addToolBar(barre)

        btn_accueil = QAction("🏠", self)
        btn_accueil.triggered.connect(self.aller_accueil)
        barre.addAction(btn_accueil)

        btn_retour = QAction("◀", self)
        btn_retour.triggered.connect(lambda: self.onglets.currentWidget().back())
        barre.addAction(btn_retour)

        btn_suivant = QAction("▶", self)
        btn_suivant.triggered.connect(
            lambda: self.onglets.currentWidget().forward())
        barre.addAction(btn_suivant)

        btn_recharger = QAction("🔄", self)
        btn_recharger.triggered.connect(
            lambda: self.onglets.currentWidget().reload())
        barre.addAction(btn_recharger)

        btn_onglet = QAction("➕", self)
        btn_onglet.triggered.connect(lambda: self.nouvel_onglet())
        barre.addAction(btn_onglet)

        self.combo_moteur = QComboBox()
        for nom in get_moteurs():
            self.combo_moteur.addItem(nom)
        self.combo_moteur.setFixedWidth(110)
        self.combo_moteur.currentTextChanged.connect(self.changer_moteur)
        barre.addWidget(self.combo_moteur)

        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("🔍 Rechercher ou taper une adresse...")
        self.url_bar.setFixedWidth(400)
        self.url_bar.returnPressed.connect(self.naviguer)
        barre.addWidget(self.url_bar)

        self.label_pubs = QLabel("🚫 0 pubs")
        self.label_pubs.setStyleSheet(
            "color: white; font-size: 12px; padding: 2px 6px;"
            "background: rgba(0,0,0,0.2); border-radius: 10px;")
        self.label_pubs.mousePressEvent = lambda e: self.stats_bloqueur()
        barre.addWidget(self.label_pubs)

        self.label_isolation = QLabel("🛡️ Isolé")
        self.label_isolation.setStyleSheet(
            "color: #90EE90; font-size: 12px; padding: 2px 6px;"
            "background: rgba(0,0,0,0.2); border-radius: 10px;")
        barre.addWidget(self.label_isolation)

        # 🍪 Indicateur cookies
        self.label_cookies = QLabel("🍪 Protégé")
        self.label_cookies.setStyleSheet(
            "color: #90EE90; font-size: 12px; padding: 2px 6px;"
            "background: rgba(0,0,0,0.2); border-radius: 10px;")
        self.label_cookies.mousePressEvent = lambda e: self.gerer_cookies()
        barre.addWidget(self.label_cookies)

        btn_zoom_moins = QAction("🔎-", self)
        btn_zoom_moins.triggered.connect(self.zoom_moins)
        barre.addAction(btn_zoom_moins)

        self.label_zoom = QLabel("100%")
        self.label_zoom.setStyleSheet(
            "color: white; font-size: 12px; padding: 2px 5px;")
        barre.addWidget(self.label_zoom)

        btn_zoom_plus = QAction("🔎+", self)
        btn_zoom_plus.triggered.connect(self.zoom_plus)
        barre.addAction(btn_zoom_plus)

        btn_chercher = QAction("🔍", self)
        btn_chercher.triggered.connect(self.chercher_dans_page)
        barre.addAction(btn_chercher)

        self.securite = QLabel("🔒 Sécurisé")
        self.securite.setStyleSheet(
            "color: #90EE90; font-size: 13px; padding: 4px;")
        barre.addWidget(self.securite)

        self.btn_menu = QToolButton()
        self.btn_menu.setText("⚙️ Menu ▼")
        self.btn_menu.setPopupMode(QToolButton.InstantPopup)
        self.menu = QMenu()

        self.menu.addAction("⭐ Ajouter aux favoris", self.ajouter_favori)
        self.menu.addAction("📋 Voir mes favoris", self.voir_favoris)
        self.menu.addSeparator()
        self.menu.addAction("📜 Historique", self.voir_historique)
        self.menu.addAction("📥 Téléchargements", self.voir_telechargements)
        self.menu.addSeparator()
        self.menu.addAction("🖨️ Imprimer", self.imprimer)
        self.action_marque = QAction("🔖 Marquer cette page", self)
        self.action_marque.triggered.connect(self.marquer_page)
        self.menu.addAction(self.action_marque)
        self.menu.addAction("🌍 Traduire la page", self.traduire_page)
        self.menu.addAction("📤 Partager cette page", self.partager_page)
        self.menu.addSeparator()
        self.action_bloqueur = QAction("🚫✅ Bloqueur de pubs ON", self)
        self.action_bloqueur.triggered.connect(self.toggle_bloqueur)
        self.menu.addAction(self.action_bloqueur)
        self.menu.addAction("📊 Stats du bloqueur", self.stats_bloqueur)
        self.menu.addSeparator()
        self.action_isolation = QAction("🛡️✅ Isolation des onglets ON", self)
        self.action_isolation.triggered.connect(self.toggle_isolation)
        self.menu.addAction(self.action_isolation)
        self.menu.addSeparator()

        # 🍪 Cookies
        self.menu.addAction("🍪 Gérer les cookies", self.gerer_cookies)
        self.menu.addAction("🗑️ Effacer tous les cookies", self.effacer_cookies)
        self.menu.addSeparator()

        menu_moteur = QMenu("🔍 Moteur de recherche", self.menu)
        self.actions_moteurs = {}
        for nom in get_moteurs():
            action = QAction(nom, self)
            action.setCheckable(True)
            action.setChecked(nom == "Google")
            action.triggered.connect(
                lambda checked, n=nom: self.changer_moteur(n))
            menu_moteur.addAction(action)
            self.actions_moteurs[nom] = action
        self.menu.addMenu(menu_moteur)
        self.menu.addSeparator()

        self.menu.addAction("📊 Infos sur la page", self.infos_page)
        self.menu.addAction("⌨️ Raccourcis clavier", self.voir_raccourcis)
        self.menu.addSeparator()
        self.action_prive = QAction("🕵️ Activer navigation privée", self)
        self.action_prive.triggered.connect(self.toggle_mode_prive)
        self.menu.addAction(self.action_prive)
        self.menu.addAction("🔄 Mettre à jour liste noire", self.maj_liste_noire)
        self.menu.addSeparator()
        self.action_enfant = QAction("👶 Activer mode enfant", self)
        self.action_enfant.triggered.connect(self.toggle_mode_enfant)
        self.menu.addAction(self.action_enfant)
        self.action_sombre = QAction("🌙 Activer mode sombre", self)
        self.action_sombre.triggered.connect(self.toggle_mode_sombre)
        self.menu.addAction(self.action_sombre)
        self.menu.addSeparator()
        self.menu.addAction("ℹ️ À propos de Xoolal", self.a_propos)

        self.btn_menu.setMenu(self.menu)
        barre.addWidget(self.btn_menu)

        self.barre_recherche = QToolBar()
        self.barre_recherche.setMovable(False)
        self.barre_recherche.setVisible(False)
        self.addToolBar(Qt.BottomToolBarArea, self.barre_recherche)

        self.champ_recherche = QLineEdit()
        self.champ_recherche.setPlaceholderText("🔍 Rechercher dans la page...")
        self.champ_recherche.setFixedWidth(300)
        self.champ_recherche.textChanged.connect(self.rechercher_texte)
        self.barre_recherche.addWidget(self.champ_recherche)

        btn_suiv = QAction("⬇️ Suivant", self)
        btn_suiv.triggered.connect(self.recherche_suivante)
        self.barre_recherche.addAction(btn_suiv)

        btn_prec = QAction("⬆️ Précédent", self)
        btn_prec.triggered.connect(self.recherche_precedente)
        self.barre_recherche.addAction(btn_prec)

        btn_fermer_rech = QAction("✖️ Fermer", self)
        btn_fermer_rech.triggered.connect(
            lambda: self.barre_recherche.setVisible(False))
        self.barre_recherche.addAction(btn_fermer_rech)

        self.onglets = QTabWidget()
        self.onglets.setTabsClosable(True)
        self.onglets.tabCloseRequested.connect(self.fermer_onglet)
        self.setCentralWidget(self.onglets)

        QShortcut(QKeySequence("Ctrl+T"), self, self.nouvel_onglet)
        QShortcut(QKeySequence("Ctrl+W"), self, self.fermer_onglet_actif)
        QShortcut(QKeySequence("Ctrl+R"), self,
                  lambda: self.onglets.currentWidget().reload())
        QShortcut(QKeySequence("F5"), self,
                  lambda: self.onglets.currentWidget().reload())
        QShortcut(QKeySequence("Ctrl+L"), self, lambda: self.url_bar.setFocus())
        QShortcut(QKeySequence("Ctrl+F"), self, self.chercher_dans_page)
        QShortcut(QKeySequence("Ctrl++"), self, self.zoom_plus)
        QShortcut(QKeySequence("Ctrl+-"), self, self.zoom_moins)
        QShortcut(QKeySequence("Ctrl+0"), self, self.zoom_reset)
        QShortcut(QKeySequence("Alt+Left"), self,
                  lambda: self.onglets.currentWidget().back())
        QShortcut(QKeySequence("Alt+Right"), self,
                  lambda: self.onglets.currentWidget().forward())
        QShortcut(QKeySequence("Ctrl+H"), self, self.voir_historique)
        QShortcut(QKeySequence("Ctrl+D"), self, self.ajouter_favori)
        QShortcut(QKeySequence("Ctrl+P"), self, self.imprimer)

        self.nouvel_onglet()

        self.timer = QTimer()
        self.timer.timeout.connect(self.mettre_a_jour_compteur)
        self.timer.start(1000)

    # ============================================
    # 🍪 GESTION DES COOKIES
    # ============================================
    def gerer_cookies(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("🍪 Gestion des Cookies")
        dialog.setFixedSize(550, 500)
        layout = QVBoxLayout()

        # Titre
        titre = QLabel("🍪 Paramètres des Cookies")
        titre.setStyleSheet(
            "font-size: 16px; font-weight: bold; padding: 5px;")
        layout.addWidget(titre)

        # Options principales
        self.check_espions = QCheckBox(
            "🚫 Bloquer les cookies espions (Google, Facebook...)")
        self.check_espions.setChecked(
            CONFIG_COOKIES.get("bloquer_espions", True))
        layout.addWidget(self.check_espions)

        self.check_tiers = QCheckBox(
            "🚫 Bloquer les cookies tiers")
        self.check_tiers.setChecked(
            CONFIG_COOKIES.get("bloquer_tiers", True))
        layout.addWidget(self.check_tiers)

        # Sites bloqués
        label_bloques = QLabel("🔴 Sites dont les cookies sont bloqués :")
        label_bloques.setStyleSheet("font-weight: bold; margin-top: 10px;")
        layout.addWidget(label_bloques)

        self.liste_bloques = QListWidget()
        for site in CONFIG_COOKIES.get("sites_bloques", []):
            self.liste_bloques.addItem(f"🔴 {site}")
        self.liste_bloques.setMaximumHeight(100)
        layout.addWidget(self.liste_bloques)

        hbox1 = QHBoxLayout()
        btn_ajouter_bloque = QPushButton("➕ Bloquer un site")
        btn_ajouter_bloque.clicked.connect(self.bloquer_site_cookie)
        hbox1.addWidget(btn_ajouter_bloque)
        btn_suppr_bloque = QPushButton("🗑️ Supprimer")
        btn_suppr_bloque.clicked.connect(
            lambda: self.supprimer_site_cookie(self.liste_bloques, "sites_bloques"))
        hbox1.addWidget(btn_suppr_bloque)
        layout.addLayout(hbox1)

        # Sites autorisés
        label_autorises = QLabel("🟢 Sites dont les cookies sont autorisés :")
        label_autorises.setStyleSheet("font-weight: bold; margin-top: 10px;")
        layout.addWidget(label_autorises)

        self.liste_autorises = QListWidget()
        for site in CONFIG_COOKIES.get("sites_autorises", []):
            self.liste_autorises.addItem(f"🟢 {site}")
        self.liste_autorises.setMaximumHeight(100)
        layout.addWidget(self.liste_autorises)

        hbox2 = QHBoxLayout()
        btn_ajouter_autorise = QPushButton("➕ Autoriser un site")
        btn_ajouter_autorise.clicked.connect(self.autoriser_site_cookie)
        hbox2.addWidget(btn_ajouter_autorise)
        btn_suppr_autorise = QPushButton("🗑️ Supprimer")
        btn_suppr_autorise.clicked.connect(
            lambda: self.supprimer_site_cookie(
                self.liste_autorises, "sites_autorises"))
        hbox2.addWidget(btn_suppr_autorise)
        layout.addLayout(hbox2)

        # Cookies espions connus
        label_espions = QLabel(
            f"🕵️ {len(COOKIES_ESPIONS)} trackers connus bloqués automatiquement")
        label_espions.setStyleSheet("color: #aaa; font-size: 12px;")
        layout.addWidget(label_espions)

        # Bouton sauvegarder
        btn_sauv = QPushButton("💾 Sauvegarder")
        btn_sauv.clicked.connect(lambda: self.sauvegarder_cookies(dialog))
        layout.addWidget(btn_sauv)

        dialog.setLayout(layout)
        dialog.exec_()

    def bloquer_site_cookie(self):
        site, ok = QInputDialog.getText(self, "🔴 Bloquer cookies",
            "Site à bloquer (ex: facebook.com) :")
        if ok and site:
            site = site.strip().lower()
            if site not in CONFIG_COOKIES["sites_bloques"]:
                CONFIG_COOKIES["sites_bloques"].append(site)
                self.liste_bloques.addItem(f"🔴 {site}")

    def autoriser_site_cookie(self):
        site, ok = QInputDialog.getText(self, "🟢 Autoriser cookies",
            "Site à autoriser (ex: seneweb.com) :")
        if ok and site:
            site = site.strip().lower()
            if site not in CONFIG_COOKIES["sites_autorises"]:
                CONFIG_COOKIES["sites_autorises"].append(site)
                self.liste_autorises.addItem(f"🟢 {site}")

    def supprimer_site_cookie(self, liste, cle):
        i = liste.currentRow()
        if i >= 0:
            texte = liste.item(i).text().replace("🔴 ", "").replace("🟢 ", "")
            if texte in CONFIG_COOKIES[cle]:
                CONFIG_COOKIES[cle].remove(texte)
            liste.takeItem(i)

    def sauvegarder_cookies(self, dialog):
        CONFIG_COOKIES["bloquer_espions"] = self.check_espions.isChecked()
        CONFIG_COOKIES["bloquer_tiers"] = self.check_tiers.isChecked()
        sauvegarder_config(CONFIG_COOKIES)
        # Mettre à jour indicateur
        if CONFIG_COOKIES["bloquer_espions"]:
            self.label_cookies.setText("🍪 Protégé")
            self.label_cookies.setStyleSheet(
                "color: #90EE90; font-size: 12px; padding: 2px 6px;"
                "background: rgba(0,0,0,0.2); border-radius: 10px;")
        else:
            self.label_cookies.setText("🍪 Non protégé")
            self.label_cookies.setStyleSheet(
                "color: #FFD700; font-size: 12px; padding: 2px 6px;"
                "background: rgba(0,0,0,0.2); border-radius: 10px;")
        QMessageBox.information(self, "Xoolal",
            "💾 Paramètres cookies sauvegardés !")
        dialog.close()

    def effacer_cookies(self):
        reponse = QMessageBox.question(self, "🗑️ Effacer cookies",
            "Voulez-vous effacer TOUS les cookies ?\n"
            "Vous serez déconnecté de tous les sites !",
            QMessageBox.Yes | QMessageBox.No)
        if reponse == QMessageBox.Yes:
            # Effacer cookies du profil normal
            self.profil_normal.cookieStore().deleteAllCookies()
            # Effacer cookies de tous les profils isolés
            for profil in self.profils_onglets.values():
                profil.cookieStore().deleteAllCookies()
            QMessageBox.information(self, "Xoolal",
                "✅ Tous les cookies ont été effacés !\n"
                "Rechargez les pages pour continuer.")

    # ============================================
    # 🛡️ ISOLATION DES ONGLETS
    # ============================================
    def creer_profil_isole(self, id_onglet):
        profil = QWebEngineProfile(f"onglet_{id_onglet}", self)
        profil.setCachePath(f"/tmp/xoolal_cache_{id_onglet}")
        profil.setPersistentStoragePath(f"/tmp/xoolal_storage_{id_onglet}")
        profil.setPersistentCookiesPolicy(
            QWebEngineProfile.AllowPersistentCookies)
        return profil

    def get_profil_pour_onglet(self, id_onglet):
        if MODE_PRIVE:
            return self.profil_prive_partage
        if ISOLATION_ACTIVE:
            if id_onglet not in self.profils_onglets:
                self.profils_onglets[id_onglet] = self.creer_profil_isole(
                    id_onglet)
            return self.profils_onglets[id_onglet]
        return self.profil_normal

    def toggle_isolation(self):
        global ISOLATION_ACTIVE
        ISOLATION_ACTIVE = not ISOLATION_ACTIVE
        if ISOLATION_ACTIVE:
            self.action_isolation.setText("🛡️✅ Isolation des onglets ON")
            self.label_isolation.setText("🛡️ Isolé")
            self.label_isolation.setStyleSheet(
                "color: #90EE90; font-size: 12px; padding: 2px 6px;"
                "background: rgba(0,0,0,0.2); border-radius: 10px;")
            QMessageBox.information(self, "Xoolal",
                "🛡️ Isolation activée !")
        else:
            self.action_isolation.setText("🛡️❌ Isolation des onglets OFF")
            self.label_isolation.setText("🛡️ Partagé")
            self.label_isolation.setStyleSheet(
                "color: #FFD700; font-size: 12px; padding: 2px 6px;"
                "background: rgba(0,0,0,0.2); border-radius: 10px;")
            QMessageBox.information(self, "Xoolal",
                "❌ Isolation désactivée.")

    def mettre_a_jour_compteur(self):
        self.label_pubs.setText(f"🚫 {STATS_PUBS['bloquees']} pubs")

    def changer_moteur(self, nom):
        MOTEUR_MODULE.MOTEUR_ACTUEL = nom
        index = self.combo_moteur.findText(nom)
        if index >= 0:
            self.combo_moteur.setCurrentIndex(index)
        for n, action in self.actions_moteurs.items():
            action.setChecked(n == nom)

    def nouvel_onglet(self):
        global COMPTEUR_ONGLETS
        COMPTEUR_ONGLETS += 1
        id_onglet = COMPTEUR_ONGLETS
        chemin = os.path.abspath("accueil.html")
        browser = QWebEngineView()
        profil = self.get_profil_pour_onglet(id_onglet)
        page = PageSecurisee(profil, browser)
        page.settings().setAttribute(
            QWebEngineSettings.JavascriptCanOpenWindows, False)
        page.settings().setAttribute(
            QWebEngineSettings.LocalStorageEnabled, not MODE_PRIVE)
        browser.id_onglet = id_onglet
        browser.setPage(page)
        browser.setUrl(QUrl(f"file://{chemin}"))
        browser.setZoomFactor(self.zoom_actuel)
        browser.titleChanged.connect(
            lambda t, b=browser: self.onglets.setTabText(
                self.onglets.indexOf(b), t[:15]))
        browser.urlChanged.connect(self.mettre_a_jour_url)
        page.profile().downloadRequested.connect(self.gerer_telechargement)
        if MODE_SOMBRE:
            browser.page().setBackgroundColor(QColor(26, 26, 26))
            browser.settings().setAttribute(
                QWebEngineSettings.ForceDarkMode, True)
        if MODE_PRIVE:
            titre = "🕵️ Privé"
        elif ISOLATION_ACTIVE:
            titre = "🛡️ Xoolal"
        else:
            titre = "Xoolal"
        index = self.onglets.addTab(browser, titre)
        self.onglets.setCurrentIndex(index)

    def fermer_onglet(self, index=None):
        if index is None:
            index = self.onglets.currentIndex()
        if self.onglets.count() > 1:
            browser = self.onglets.widget(index)
            if hasattr(browser, 'id_onglet'):
                id_onglet = browser.id_onglet
                if id_onglet in self.profils_onglets:
                    del self.profils_onglets[id_onglet]
            self.onglets.removeTab(index)

    def fermer_onglet_actif(self):
        self.fermer_onglet(self.onglets.currentIndex())

    def aller_accueil(self):
        chemin = os.path.abspath("accueil.html")
        self.onglets.currentWidget().setUrl(QUrl(f"file://{chemin}"))

    def naviguer(self):
        texte = self.url_bar.text().strip()
        if "." in texte and " " not in texte:
            if not texte.startswith("http"):
                texte = "https://" + texte
            self.onglets.currentWidget().setUrl(QUrl(texte))
        else:
            self.onglets.currentWidget().setUrl(QUrl(get_url_recherche(texte)))

    def mettre_a_jour_url(self, url):
        self.url_bar.setText(url.toString())
        if url.scheme() == "https":
            self.securite.setText("🔒 Sécurisé")
            self.securite.setStyleSheet(
                "color: #90EE90; font-size: 13px; padding: 4px;")
        else:
            self.securite.setText("⚠️ Attention")
            self.securite.setStyleSheet(
                "color: #FFD700; font-size: 13px; padding: 4px;")
        adresse = url.toString()
        if adresse.startswith("http") and not MODE_PRIVE:
            self.historique.insert(0, {
                "url": adresse,
                "date": datetime.now().strftime("%d/%m/%Y %H:%M")
            })
            self.historique = self.historique[:100]
            sauvegarder_json(FICHIER_HISTORIQUE, self.historique)

    def toggle_bloqueur(self):
        global BLOQUEUR_ACTIF
        BLOQUEUR_ACTIF = not BLOQUEUR_ACTIF
        self.action_bloqueur.setText(
            "🚫✅ Bloqueur de pubs ON" if BLOQUEUR_ACTIF
            else "🚫❌ Bloqueur de pubs OFF")
        QMessageBox.information(self, "Xoolal",
            "🚫 Bloqueur activé !" if BLOQUEUR_ACTIF
            else "✅ Bloqueur désactivé.")

    def stats_bloqueur(self):
        QMessageBox.information(self, "📊 Stats Bloqueur",
            f"🚫 Pubs bloquées : {STATS_PUBS['bloquees']}\n"
            f"📋 Domaines bloqués : {len(DOMAINES_PUB)}\n"
            f"{'✅ Actif' if BLOQUEUR_ACTIF else '❌ Désactivé'}")

    def zoom_plus(self):
        self.zoom_actuel = min(self.zoom_actuel + 0.1, 3.0)
        self.onglets.currentWidget().setZoomFactor(self.zoom_actuel)
        self.label_zoom.setText(f"{int(self.zoom_actuel * 100)}%")

    def zoom_moins(self):
        self.zoom_actuel = max(self.zoom_actuel - 0.1, 0.3)
        self.onglets.currentWidget().setZoomFactor(self.zoom_actuel)
        self.label_zoom.setText(f"{int(self.zoom_actuel * 100)}%")

    def zoom_reset(self):
        self.zoom_actuel = 1.0
        self.onglets.currentWidget().setZoomFactor(1.0)
        self.label_zoom.setText("100%")

    def chercher_dans_page(self):
        self.barre_recherche.setVisible(True)
        self.champ_recherche.setFocus()

    def rechercher_texte(self, texte):
        self.onglets.currentWidget().findText(texte)

    def recherche_suivante(self):
        self.onglets.currentWidget().findText(self.champ_recherche.text())

    def recherche_precedente(self):
        self.onglets.currentWidget().findText(
            self.champ_recherche.text(), QWebEnginePage.FindBackward)

    def ajouter_favori(self):
        url = self.url_bar.text()
        nom, ok = QInputDialog.getText(self, "Favori", "Nom :", text=url)
        if ok and nom:
            self.favoris.append({"nom": nom, "url": url})
            sauvegarder_json(FICHIER_FAVORIS, self.favoris)
            QMessageBox.information(self, "Xoolal", f"⭐ '{nom}' ajouté !")

    def voir_favoris(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("⭐ Mes Favoris")
        dialog.setFixedSize(450, 350)
        layout = QVBoxLayout()
        liste = QListWidget()
        for f in self.favoris:
            liste.addItem(f"{f['nom']} — {f['url']}")
        layout.addWidget(liste)
        btn = QPushButton("🌐 Ouvrir")
        btn.clicked.connect(lambda: self.ouvrir_favori(liste, dialog))
        layout.addWidget(btn)
        btn2 = QPushButton("🗑️ Supprimer")
        btn2.clicked.connect(lambda: self.supprimer_favori(liste))
        layout.addWidget(btn2)
        dialog.setLayout(layout)
        dialog.exec_()

    def ouvrir_favori(self, liste, dialog):
        i = liste.currentRow()
        if i >= 0:
            self.nouvel_onglet()
            self.onglets.currentWidget().setUrl(QUrl(self.favoris[i]["url"]))
            dialog.close()

    def supprimer_favori(self, liste):
        i = liste.currentRow()
        if i >= 0:
            self.favoris.pop(i)
            liste.takeItem(i)
            sauvegarder_json(FICHIER_FAVORIS, self.favoris)

    def voir_historique(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("📜 Historique")
        dialog.setFixedSize(550, 400)
        layout = QVBoxLayout()
        liste = QListWidget()
        for h in self.historique:
            liste.addItem(f"🕐 {h['date']} — {h['url']}")
        layout.addWidget(liste)
        btn = QPushButton("🌐 Ouvrir")
        btn.clicked.connect(lambda: self.ouvrir_historique(liste, dialog))
        layout.addWidget(btn)
        btn2 = QPushButton("🗑️ Effacer tout")
        btn2.clicked.connect(lambda: self.effacer_historique(liste))
        layout.addWidget(btn2)
        dialog.setLayout(layout)
        dialog.exec_()

    def ouvrir_historique(self, liste, dialog):
        i = liste.currentRow()
        if i >= 0:
            self.nouvel_onglet()
            self.onglets.currentWidget().setUrl(QUrl(self.historique[i]["url"]))
            dialog.close()

    def effacer_historique(self, liste):
        self.historique = []
        sauvegarder_json(FICHIER_HISTORIQUE, self.historique)
        liste.clear()
        QMessageBox.information(self, "Xoolal", "🗑️ Historique effacé !")

    def gerer_telechargement(self, download):
        chemin, _ = QFileDialog.getSaveFileName(
            self, "Sauvegarder",
            os.path.join(os.path.expanduser("~"), download.suggestedFileName()))
        if chemin:
            download.setPath(chemin)
            download.accept()
            self.telechargements.append({
                "nom": os.path.basename(chemin),
                "chemin": chemin, "statut": "⏳ En cours..."})
            download.finished.connect(
                lambda: self.telechargement_termine(chemin))
        else:
            download.cancel()

    def telechargement_termine(self, chemin):
        for t in self.telechargements:
            if t["chemin"] == chemin:
                t["statut"] = "✅ Terminé"
        QMessageBox.information(self, "Xoolal",
            f"✅ Terminé !\n{os.path.basename(chemin)}")

    def voir_telechargements(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("📥 Téléchargements")
        dialog.setFixedSize(550, 400)
        layout = QVBoxLayout()
        liste = QListWidget()
        if not self.telechargements:
            liste.addItem("Aucun téléchargement pour l'instant")
        for t in self.telechargements:
            liste.addItem(f"{t['statut']} — {t['nom']}")
        layout.addWidget(liste)
        btn = QPushButton("📂 Ouvrir dossier")
        btn.clicked.connect(
            lambda: os.system(f"xdg-open '{os.path.expanduser('~')}'"))
        layout.addWidget(btn)
        btn2 = QPushButton("🗑️ Effacer liste")
        btn2.clicked.connect(
            lambda: [self.telechargements.clear(), liste.clear()])
        layout.addWidget(btn2)
        dialog.setLayout(layout)
        dialog.exec_()

    def imprimer(self):
        printer = QPrinter()
        dialog = QPrintDialog(printer, self)
        if dialog.exec_() == QPrintDialog.Accepted:
            self.onglets.currentWidget().page().print(printer, lambda ok: None)

    def marquer_page(self):
        url = self.url_bar.text()
        titre = self.onglets.tabText(self.onglets.currentIndex())
        for f in self.favoris:
            if f["url"] == url:
                reponse = QMessageBox.question(self, "Xoolal",
                    "🔖 Déjà marquée ! Supprimer ?",
                    QMessageBox.Yes | QMessageBox.No)
                if reponse == QMessageBox.Yes:
                    self.favoris = [f for f in self.favoris if f["url"] != url]
                    sauvegarder_json(FICHIER_FAVORIS, self.favoris)
                    self.action_marque.setText("🔖 Marquer cette page")
                return
        self.favoris.append({"nom": titre, "url": url})
        sauvegarder_json(FICHIER_FAVORIS, self.favoris)
        self.action_marque.setText("🔖✅ Page marquée !")
        QMessageBox.information(self, "Xoolal", "🔖 Page marquée !")

    def traduire_page(self):
        url = self.url_bar.text()
        if url.startswith("http"):
            self.nouvel_onglet()
            self.onglets.currentWidget().setUrl(QUrl(
                f"https://translate.google.com/translate?sl=auto&tl=fr&u={url}"))
        else:
            QMessageBox.warning(self, "Xoolal", "⚠️ Navigue d'abord sur un site !")

    def partager_page(self):
        url = self.url_bar.text()
        if not url.startswith("http"):
            QMessageBox.warning(self, "Xoolal", "⚠️ Navigue d'abord sur un site !")
            return
        dialog = QDialog(self)
        dialog.setWindowTitle("📤 Partager")
        dialog.setFixedSize(450, 320)
        layout = QVBoxLayout()
        label = QLabel(f"🔗 {url}")
        label.setWordWrap(True)
        layout.addWidget(label)
        for texte, commande in [
            ("📋 Copier le lien", lambda: [
                QApplication.clipboard().setText(url),
                QMessageBox.information(self, "Xoolal", "📋 Copié !")]),
            ("💬 WhatsApp", lambda: os.system(
                f"xdg-open 'https://api.whatsapp.com/send?text={url}'")),
            ("📧 Email", lambda: os.system(
                f"xdg-open 'mailto:?subject=Regarde ce site&body={url}'")),
            ("📘 Facebook", lambda: os.system(
                f"xdg-open 'https://www.facebook.com/sharer/sharer.php?u={url}'")),
        ]:
            btn = QPushButton(texte)
            btn.clicked.connect(commande)
            layout.addWidget(btn)
        dialog.setLayout(layout)
        dialog.exec_()

    def infos_page(self):
        url = self.url_bar.text()
        titre = self.onglets.tabText(self.onglets.currentIndex())
        QMessageBox.information(self, "📊 Infos sur la page",
            f"📄 Titre : {titre}\n"
            f"🔗 URL : {url}\n"
            f"🔒 HTTPS : {'✅' if url.startswith('https') else '❌'}\n"
            f"🔍 Moteur : {MOTEUR_MODULE.MOTEUR_ACTUEL}\n"
            f"🛡️ Isolation : {'✅' if ISOLATION_ACTIVE else '❌'}\n"
            f"🍪 Cookies protégés : {'✅' if CONFIG_COOKIES.get('bloquer_espions') else '❌'}\n"
            f"🚫 Pubs bloquées : {STATS_PUBS['bloquees']}\n"
            f"🕵️ Mode privé : {'✅' if MODE_PRIVE else '❌'}\n"
            f"👶 Mode enfant : {'✅' if MODE_ENFANT else '❌'}\n"
            f"🌙 Mode sombre : {'✅' if MODE_SOMBRE else '❌'}"
        )

    def voir_raccourcis(self):
        QMessageBox.information(self, "⌨️ Raccourcis Clavier",
            "🆕 Ctrl+T — Nouvel onglet\n"
            "❌ Ctrl+W — Fermer l'onglet\n"
            "🔄 Ctrl+R / F5 — Recharger\n"
            "🔍 Ctrl+F — Chercher dans la page\n"
            "📍 Ctrl+L — Barre d'adresse\n"
            "🔎 Ctrl++ — Zoom avant\n"
            "🔎 Ctrl+- — Zoom arrière\n"
            "🔎 Ctrl+0 — Zoom normal\n"
            "◀ Alt+← — Page précédente\n"
            "▶ Alt+→ — Page suivante\n"
            "📜 Ctrl+H — Historique\n"
            "⭐ Ctrl+D — Ajouter aux favoris\n"
            "🖨️ Ctrl+P — Imprimer"
        )

    def a_propos(self):
        QMessageBox.information(self, "ℹ️ À propos de Xoolal",
            "╔══════════════════════════════╗\n"
            "║      🌐 XOOLAL BROWSER       ║\n"
            "║         Version 1.4          ║\n"
            "╚══════════════════════════════╝\n\n"
            "© 2024 Ismaïla Mbodji\n"
            "Tous droits réservés.\n\n"
            "🇸🇳 Navigateur sénégalais sécurisé\n"
            "Créé avec Python & PyQt5\n\n"
            "🛡️ Fonctionnalités :\n"
            "  • Gestion avancée des cookies\n"
            "  • Isolation des onglets\n"
            "  • Moteur de recherche au choix\n"
            "  • Bloqueur de publicités\n"
            "  • Navigation privée\n"
            "  • Mode enfant sécurisé\n"
            "  • Mode sombre 🌙\n\n"
            "📧 Contact : ismaelaembodji@email.com"
        )

    def toggle_mode_prive(self):
        global MODE_PRIVE
        MODE_PRIVE = not MODE_PRIVE
        if MODE_PRIVE:
            self.action_prive.setText("🕵️✅ Désactiver navigation privée")
            self.setWindowTitle("Xoolal 🕵️ — Navigation Privée")
            QMessageBox.information(self, "Xoolal",
                "🕵️ Navigation privée activée !\n\n"
                "✅ Pas d'historique\n✅ Pas de cookies\n✅ Pas de cache")
        else:
            self.action_prive.setText("🕵️ Activer navigation privée")
            self.setWindowTitle("Xoolal 🇸🇳")
            self.setStyleSheet(STYLE_SOMBRE if MODE_SOMBRE else STYLE_CLAIR)
            QMessageBox.information(self, "Xoolal",
                "✅ Navigation normale réactivée !")

    def maj_liste_noire(self):
        QMessageBox.information(self, "Xoolal", "🔄 Mise à jour en cours...")
        succes = mettre_a_jour_liste_noire()
        if succes:
            QMessageBox.information(self, "Xoolal",
                f"✅ Liste noire mise à jour !\n{len(LISTE_NOIRE)} domaines.")
        else:
            QMessageBox.warning(self, "Xoolal", "❌ Échec. Vérifie ta connexion.")

    def toggle_mode_enfant(self):
        global MODE_ENFANT
        if not MODE_ENFANT:
            mdp, ok = QInputDialog.getText(self, "🔐 Mot de passe",
                "Entrez le mot de passe :", QLineEdit.Password)
            if ok and mdp == MOT_DE_PASSE:
                MODE_ENFANT = True
                self.action_enfant.setText("👶✅ Désactiver mode enfant")
                QMessageBox.information(self, "Xoolal", "👶 Mode enfant activé !")
            elif ok:
                QMessageBox.warning(self, "Xoolal", "❌ Mot de passe incorrect !")
        else:
            mdp, ok = QInputDialog.getText(self, "🔐 Mot de passe",
                "Entrez le mot de passe :", QLineEdit.Password)
            if ok and mdp == MOT_DE_PASSE:
                MODE_ENFANT = False
                self.action_enfant.setText("👶 Activer mode enfant")
                QMessageBox.information(self, "Xoolal", "✅ Mode enfant désactivé !")
            elif ok:
                QMessageBox.warning(self, "Xoolal", "❌ Mot de passe incorrect !")

    def toggle_mode_sombre(self):
        global MODE_SOMBRE
        MODE_SOMBRE = not MODE_SOMBRE
        if MODE_SOMBRE:
            self.setStyleSheet(STYLE_SOMBRE)
            self.action_sombre.setText("☀️ Désactiver mode sombre")
            for i in range(self.onglets.count()):
                b = self.onglets.widget(i)
                b.page().setBackgroundColor(QColor(26, 26, 26))
                b.settings().setAttribute(QWebEngineSettings.ForceDarkMode, True)
        else:
            self.setStyleSheet(STYLE_CLAIR)
            self.action_sombre.setText("🌙 Activer mode sombre")
            for i in range(self.onglets.count()):
                b = self.onglets.widget(i)
                b.page().setBackgroundColor(QColor(255, 255, 255))
                b.settings().setAttribute(QWebEngineSettings.ForceDarkMode, False)

app = QApplication(sys.argv)
fenetre = Navigateur()
fenetre.show()
sys.exit(app.exec_())
