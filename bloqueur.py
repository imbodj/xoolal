# ============================================
# Xoolal Browser - Bloqueur de publicités
# © 2024 Ismaïla Mbodji
# ============================================

DOMAINES_PUB = [
    "doubleclick.net", "googlesyndication.com",
    "googleadservices.com", "adservice.google.com",
    "pagead2.googlesyndication.com",
    "connect.facebook.net", "an.facebook.com",
    "google-analytics.com", "googletagmanager.com",
    "hotjar.com", "mixpanel.com", "segment.com",
    "advertising.com", "adnxs.com", "adsrvr.org",
    "pubmatic.com", "rubiconproject.com", "openx.net",
    "criteo.com", "taboola.com", "outbrain.com",
    "smartadserver.com", "adroll.com",
    "amazon-adsystem.com", "media.net",
    "scorecardresearch.com", "comscore.com",
    "quantserve.com", "chartbeat.com",
]

SCRIPT_BLOQUEUR = """
(function() {
    var selecteurs = [
        '[class*="ad-"]', '[class*="-ad"]',
        '[class*="ads-"]', '[class*="advert"]',
        '[id*="ad-"]', '[id*="advert"]',
        '[class*="sponsor"]', '[class*="promoted"]',
        'ins.adsbygoogle', '.adsbygoogle',
        '#google_ads_iframe', '.google-ad',
        '.ad-container', '.ad-wrapper',
        '.ad-banner', '.advertisement',
        'iframe[src*="doubleclick"]',
        'iframe[src*="googlesyndication"]',
    ];
    function masquerPubs() {
        selecteurs.forEach(function(sel) {
            try {
                document.querySelectorAll(sel).forEach(function(el) {
                    el.style.display = 'none';
                });
            } catch(e) {}
        });
    }
    masquerPubs();
    new MutationObserver(masquerPubs).observe(
        document.documentElement, {childList:true, subtree:true});
})();
"""

def est_pub(host):
    host = host.lower()
    for domaine in DOMAINES_PUB:
        if domaine in host:
            return True
    return False
