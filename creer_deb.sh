#!/bin/bash
# ============================================
# Xoolal Browser - Créateur de paquet .deb
# © 2024 Ismaïla Mbodji
# ============================================

echo "🚀 Création du paquet Xoolal .deb..."

# Créer la structure du paquet
mkdir -p xoolal-deb/DEBIAN
mkdir -p xoolal-deb/usr/local/bin/xoolal
mkdir -p xoolal-deb/usr/share/applications
mkdir -p xoolal-deb/usr/share/icons/hicolor/256x256/apps
mkdir -p xoolal-deb/usr/share/doc/xoolal

# Copier les fichiers
cp navigateur.py    xoolal-deb/usr/local/bin/xoolal/
cp accueil.html     xoolal-deb/usr/local/bin/xoolal/
cp bloqueur.py      xoolal-deb/usr/local/bin/xoolal/
cp moteur.py        xoolal-deb/usr/local/bin/xoolal/
cp cookies.py       xoolal-deb/usr/local/bin/xoolal/
cp xoolal_icon.png  xoolal-deb/usr/share/icons/hicolor/256x256/apps/xoolal.png

# Fichier de contrôle du paquet
cat > xoolal-deb/DEBIAN/control << EOF
Package: xoolal
Version: 1.4.0
Section: web
Priority: optional
Architecture: all
Depends: python3, python3-pyqt5, python3-pyqt5.qtwebengine
Maintainer: Ismaïla Mbodji <ismaelaembodji@email.com>
Description: Xoolal Browser - Navigateur sénégalais sécurisé
 Xoolal est un navigateur web sécurisé créé au Sénégal.
 Il inclut un bloqueur de publicités, isolation des onglets,
 gestion des cookies, mode privé et mode enfant.
 .
 © 2024 Ismaïla Mbodji - Tous droits réservés
EOF

# Script de lancement
cat > xoolal-deb/usr/local/bin/xoolal/xoolal.sh << 'EOF'
#!/bin/bash
cd /usr/local/bin/xoolal
python3 navigateur.py
EOF
chmod +x xoolal-deb/usr/local/bin/xoolal/xoolal.sh

# Lien symbolique pour lancer depuis terminal
mkdir -p xoolal-deb/usr/bin
ln -sf /usr/local/bin/xoolal/xoolal.sh xoolal-deb/usr/bin/xoolal

# Fichier .desktop (raccourci)
cat > xoolal-deb/usr/share/applications/xoolal.desktop << EOF
[Desktop Entry]
Name=Xoolal Browser
Name[fr]=Xoolal Browser
Comment=Navigateur sénégalais sécurisé
Comment[fr]=Navigateur sénégalais sécurisé
Exec=/usr/local/bin/xoolal/xoolal.sh
Icon=xoolal
Terminal=false
Type=Application
Categories=Network;WebBrowser;
StartupNotify=true
StartupWMClass=Xoolal
EOF

# Documentation
cat > xoolal-deb/usr/share/doc/xoolal/copyright << EOF
Xoolal Browser v1.4
© 2024 Ismaïla Mbodji
Tous droits réservés / All rights reserved
🇸🇳 Navigateur sénégalais sécurisé
EOF

# Script post-installation
cat > xoolal-deb/DEBIAN/postinst << 'EOF'
#!/bin/bash
update-desktop-database /usr/share/applications/
gtk-update-icon-cache /usr/share/icons/hicolor/ 2>/dev/null || true
echo "✅ Xoolal Browser installé avec succès !"
echo "🌐 Lance Xoolal depuis le menu Applications ou tape : xoolal"
EOF
chmod +x xoolal-deb/DEBIAN/postinst

# Construire le .deb
dpkg-deb --build xoolal-deb xoolal_1.4.0_all.deb

echo ""
echo "✅ Paquet créé : xoolal_1.4.0_all.deb"
echo "📦 Pour installer : sudo dpkg -i xoolal_1.4.0_all.deb"
echo "🗑️ Pour désinstaller : sudo dpkg -r xoolal"
