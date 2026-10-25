# -*- coding: utf-8 -*-
"""Static site generator for the FarFlight Mechatronics website.

Reads data/products.json and generates all HTML pages into the project root.
Run:  python tools/build.py
"""
import json
import os
import re
import datetime
from html import escape

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_ROOT = ROOT

with open(os.path.join(ROOT, "data", "products.json"), encoding="utf-8") as f:
    DATA = json.load(f)

SITE = DATA["site"]
PRODUCTS = DATA["products"]
GROUPS = ["Servo Motors", "Servo Drives", "VFD Inverters"]
YEAR = datetime.date.today().year

E = escape

# ---------------------------------------------------------------- SEO
# Live domain — set to the deployed URL (e.g. "https://mechatronics.example.com")
# before regenerating to produce sitemap.xml and the robots.txt Sitemap line.
DOMAIN = "https://mechatronics.farflight.cc"

SITE_KEYWORDS_EN = ("FarFlight Mechatronics, industrial servo motor, permanent magnet synchronous servo motor, "
    "servo drive system, servo drive, servo amplifier, VFD inverter, variable frequency drive, vector inverter, "
    "bus-type servo drive, EtherCAT servo drive, CANopen servo drive, dual-axis servo drive, IP66 inverter, "
    "IP67 inverter, motor-drive integrated inverter, water pump inverter, fan inverter, motion control, "
    "industrial automation, servo motor supplier, servo drive distributor, China servo motor, "
    "servo motor price, servo drive quotation, buy servo motor online, 23-bit absolute encoder, "
    "0.2-450 kW inverter, 40-180 mm servo motor, EURA DRIVES, FarFlight Trading")

SITE_KEYWORDS_ZH = ("工业伺服电机, 永磁同步伺服电机, 伺服电机, 伺服驱动器, 伺服驱动系统, 变频器, 矢量变频器, "
    "通用变频器, 总线型伺服驱动器, EtherCAT伺服驱动器, CANopen伺服驱动器, 双轴伺服驱动器, 高防护等级变频器, "
    "IP66变频器, IP67变频器, 电机驱动一体变频器, 水泵变频器, 风机变频器, 恒压供水变频器, 运动控制, 工业自动化, "
    "伺服电机供应商, 中国伺服电机, 伺服电机价格, 伺服驱动器报价, 在线购买伺服电机, 23位绝对值编码器, "
    "欧瑞传动, 远翔贸易")

DEFAULT_KEYWORDS = SITE_KEYWORDS_EN + ", " + SITE_KEYWORDS_ZH

SLUG_ZH_KEYWORDS = {
    "sm-series-servo-motor": "SM系列伺服电机, 永磁同步伺服电机, 伺服电机, 40-180mm伺服电机, 23位编码器伺服电机, 带刹车伺服电机, IP65伺服电机",
    "sd20-e-bus-servo-drive": "SD20-E总线型伺服驱动器, EtherCAT伺服驱动器, CANopen伺服驱动器, 总线型伺服, 3.2kHz伺服驱动, 高响应伺服驱动",
    "sd20-g-servo-drive": "SD20-G通用型伺服驱动器, 通用伺服驱动, 脉冲型伺服驱动器, 模拟量伺服驱动, Modbus伺服驱动",
    "sde20-g-servo-drive": "SDE20-G高性能伺服驱动器, 单板伺服驱动器, 薄型伺服驱动器, 4MHz脉冲伺服, 紧凑伺服驱动",
    "sd20-d-dual-axis-servo-drive": "SD20-D双轴伺服驱动器, 双轴伺服驱动, EtherCAT双轴驱动器, CANopen双轴驱动, 一体化双轴伺服",
    "em30-integrated-inverter": "EM30电机驱动一体变频器, IP67变频器, 电机安装式变频器, 一体化变频器, 水泵变频器, 防潮防尘变频器",
    "e800-vector-inverter": "E800通用矢量变频器, 矢量变频器, 通用变频器, 风机水泵变频器, 恒压供水变频器, 450kW变频器",
    "ep66-inverter": "EP66高防护等级变频器, IP66变频器, 防水变频器, 户外变频器, 无柜安装变频器, 重工况变频器",
}

# ---------------------------------------------------------------- icons
ICONS = {
    "bolt": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>',
    "gear": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>',
    "shield": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>',
    "globe": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>',
    "chip": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="4" width="16" height="16" rx="2"/><rect x="9" y="9" width="6" height="6"/><line x1="9" y1="1" x2="9" y2="4"/><line x1="15" y1="1" x2="15" y2="4"/><line x1="9" y1="20" x2="9" y2="23"/><line x1="15" y1="20" x2="15" y2="23"/><line x1="20" y1="9" x2="23" y2="9"/><line x1="20" y1="14" x2="23" y2="14"/><line x1="1" y1="9" x2="4" y2="9"/><line x1="1" y1="14" x2="4" y2="14"/></svg>',
    "activity": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>',
    "target": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg>',
    "clock": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>',
    "layers": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/></svg>',
    "wrench": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/></svg>',
    "box": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/><polyline points="3.27 6.96 12 12.01 20.73 6.96"/><line x1="12" y1="22.08" x2="12" y2="12"/></svg>',
    "mail": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>',
    "chat": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/></svg>',
    "cart": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/><path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"/></svg>',
    "arrow-up": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="18 15 12 9 6 15"/></svg>',
    "check": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>',
}

FEATURE_ICON_SEQ = ["bolt", "gear", "shield", "globe", "chip", "activity", "target", "clock"]
GROUP_ICON = {"Servo Motors": "activity", "Servo Drives": "chip", "VFD Inverters": "bolt"}

WHY_ITEMS = [
    ("box", "Quality-Sourced Products",
     "We supply EURA DRIVES motion and drive products — servo motors, servo drives and vector inverters engineered for demanding industrial duty."),
    ("globe", "Global Supply Chain",
     "A well-established supply chain and logistics network delivers to Europe, North America, Southeast Asia, the Middle East and Africa."),
    ("layers", "Flexible Trading Solutions",
     "From single-unit samples to volume orders, we tailor quotations, packaging and delivery terms to your project needs."),
    ("wrench", "Professional Service",
     "Our team supports model selection, technical documentation and after-sales coordination, with fast responses via email and WhatsApp."),
]

# ---------------------------------------------------------------- helpers

def product_url(p):
    return "product/%s.html" % p["slug"]


def wa_number_digits():
    return re.sub(r"\D", "", SITE["whatsapp_link"].split("/")[-1])


def head(title, description, active, depth=0, keywords=None):
    prefix = "../" * depth
    kw = keywords if keywords else DEFAULT_KEYWORDS
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="theme-color" content="#0a2540">
<title>{E(title)}</title>
<meta name="description" content="{E(description)}">
<meta name="keywords" content="{E(kw)}">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(description)}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="FarFlight Mechatronics">
<meta property="og:image" content="{prefix}assets/images/logo.png">
<meta name="twitter:card" content="summary">
<link rel="icon" type="image/png" href="{prefix}assets/images/favicon.png">
<link rel="stylesheet" href="{prefix}assets/css/style.css">
</head>
<body>"""


def header(active, depth=0):
    prefix = "../" * depth
    links = [
        ("index.html", "Home", "home"),
        ("products.html", "Products", "products"),
        ("about.html", "About", "about"),
        ("contact.html", "Contact", "contact"),
    ]
    nav = ""
    for href, label, key in links:
        cls = ' class="nav-link active"' if key == active else ' class="nav-link"'
        nav += f'<a{cls} href="{prefix}{href}">{label}</a>\n'
    return f"""
<header class="site-header">
  <div class="container header-inner">
    <a class="brand" href="{prefix}index.html">
      <img src="{prefix}assets/images/logo.png" alt="FarFlight logo">
      <span class="brand-text">
        <span class="name">FarFlight</span><br>
        <span class="sub">Mechatronics</span>
      </span>
    </a>
    <nav class="main-nav" id="main-nav">
{nav}      <a class="nav-cta" href="{prefix}payment.html">Order &amp; Pay</a>
    </nav>
    <button class="nav-toggle" aria-label="Toggle navigation"><span></span><span></span><span></span></button>
  </div>
</header>"""


def footer(depth=0):
    prefix = "../" * depth
    product_links = "\n".join(
        f'<li><a href="{prefix}{product_url(p)}">{E(p["short_name"])}</a></li>' for p in PRODUCTS
    )
    return f"""
<footer class="site-footer">
  <div class="container">
    <div class="footer-top">
      <div>
        <div class="footer-brand">
          <img src="{prefix}assets/images/logo.png" alt="FarFlight logo">
          <div>
            <div class="name">FarFlight Mechatronics</div>
            <div class="sub">Industrial Servo &amp; Drive Solutions</div>
          </div>
        </div>
        <p class="blurb">A division of FarFlight Trading Co., Ltd — your trusted bridge between China's leading drive manufacturers and the global market. Supplying EURA DRIVES servo motors, servo drives and vector inverters worldwide.</p>
      </div>
      <div>
        <h4>Products</h4>
        <ul>
{product_links}
        </ul>
      </div>
      <div>
        <h4>Company</h4>
        <ul>
          <li><a href="{prefix}index.html">Home</a></li>
          <li><a href="{prefix}products.html">All Products</a></li>
          <li><a href="{prefix}about.html">About Us</a></li>
          <li><a href="{prefix}contact.html">Contact Us</a></li>
          <li><a href="{prefix}payment.html">Order &amp; Payment</a></li>
        </ul>
      </div>
      <div>
        <h4>Contact</h4>
        <ul class="footer-contact">
          <li>{ICONS["mail"]}<a href="mailto:{SITE["email"]}">{SITE["email"]}</a></li>
          <li>{ICONS["chat"]}<a href="{SITE["whatsapp_link"]}" target="_blank" rel="noopener">{SITE["whatsapp_number"]} (WhatsApp)</a></li>
          <li>{ICONS["globe"]}Worldwide shipping from China</li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>&copy; <span class="js-year">{YEAR}</span> FarFlight Trading Co., Ltd. All rights reserved.</span>
      <span>Featuring EURA DRIVES motion &amp; drive products</span>
    </div>
  </div>
</footer>

<div class="lightbox" id="lightbox"><button class="lb-close" aria-label="Close">&times;</button><img src="" alt="Product image"></div>
<button class="to-top" id="to-top" aria-label="Back to top">{ICONS["arrow-up"]}</button>
<script src="{prefix}assets/js/main.js"></script>
</body>
</html>"""


def cta_banner(depth=0):
    prefix = "../" * depth
    return f"""
<section class="section alt">
  <div class="container">
    <div class="cta-banner">
      <div>
        <h2>Need a quotation or technical advice?</h2>
        <p>Tell us your application and required ratings — we reply within 24 hours with pricing, lead time and shipping options.</p>
      </div>
      <div style="display:flex;gap:12px;flex-wrap:wrap;">
        <a class="btn btn-accent" href="{SITE['whatsapp_link']}" target="_blank" rel="noopener">{ICONS['chat']} WhatsApp Us</a>
        <a class="btn btn-outline" href="mailto:{SITE['email']}">{ICONS['mail']} Email Us</a>
      </div>
    </div>
  </div>
</section>"""


def product_card(p, depth=0):
    prefix = "../" * depth
    url = product_url(p) if depth == 0 else "%s.html" % p["slug"]
    img = prefix + p["images"]["photo"]
    specs = ""
    for ks in p["key_specs"][:3]:
        val = ks["value"]
        if len(val) > 42:
            val = val[:40] + "…"
        specs += f'<div><span class="k">{E(ks["label"])}</span><span class="v">{E(val)}</span></div>\n'
    return f"""<article class="product-card" data-group="{E(p['group'])}">
  <a class="media" href="{url}">
    <img src="{img}" alt="{E(p['name'])}" loading="lazy">
    <span class="badge">{E(p['badge'])}</span>
  </a>
  <div class="body">
    <span class="cat">{E(p['group'])}</span>
    <h3><a href="{url}">{E(p['name'])}</a></h3>
    <p class="tagline">{E(p['tagline'])}</p>
    <div class="specs">
{specs}    </div>
    <div class="foot">
      <span class="price-tag"><span class="q">?</span> Contact us</span>
      <a class="link-arrow" href="{url}">View Details &rarr;</a>
    </div>
  </div>
</article>"""


# ---------------------------------------------------------------- pages

def page_index():
    cards = "\n".join(product_card(p) for p in PRODUCTS)
    cats = ""
    for g in GROUPS:
        count = sum(1 for p in PRODUCTS if p["group"] == g)
        desc = {
            "Servo Motors": "Permanent magnet synchronous servo motors from 40 to 180 mm frames, with incremental and absolute encoders up to 23-bit.",
            "Servo Drives": "Bus-type, general-purpose, high-performance and dual-axis servo drives from 100 W to 110 kW with EtherCAT and CANopen options.",
            "VFD Inverters": "Vector inverters from 0.2 to 450 kW, including IP66/IP67 motor-integrated and high-protection models.",
        }[g]
        cats += f"""<a class="cat-tile" href="products.html#filter-{g.lower().replace(' ', '-')}">
  <div class="icon">{ICONS[GROUP_ICON[g]]}</div>
  <h3>{g}</h3>
  <p>{desc}</p>
  <span class="count">{count} series &rarr;</span>
</a>\n"""
    why = ""
    for icon, title, text in WHY_ITEMS:
        why += f"""<div class="why-item">
  <div class="icon">{ICONS[icon]}</div>
  <h3>{E(title)}</h3>
  <p>{E(text)}</p>
</div>\n"""

    body = f"""
<header class="hero">
  <div class="container">
    <h1>Industrial Servo &amp; Drive Solutions<br><span class="hl">for Global Automation</span></h1>
    <p class="lead">FarFlight Trading Co., Ltd supplies EURA DRIVES servo motors, servo drive systems and vector inverters — from 0.2 kW compact axes to 450 kW industrial power — to customers worldwide.</p>
    <div class="hero-actions">
      <a class="btn btn-accent" href="products.html">{ICONS['box']} Browse Products</a>
      <a class="btn btn-outline" href="contact.html">Get a Quote</a>
    </div>
    <div class="hero-badges">
      <span>EURA DRIVES products</span><span>0.2 – 450 kW</span><span>IP66 / IP67 options</span><span>Worldwide shipping</span>
    </div>
  </div>
</header>

<div class="stats-bar">
  <div class="container stats-grid">
    <div class="stat"><div class="num">8</div><div class="lbl">Product Series</div></div>
    <div class="stat"><div class="num">0.2–450 kW</div><div class="lbl">Power Range</div></div>
    <div class="stat"><div class="num">5</div><div class="lbl">Continents Served</div></div>
    <div class="stat"><div class="num">24h</div><div class="lbl">Response Target</div></div>
  </div>
</div>

<section class="section">
  <div class="container">
    <div class="section-head center">
      <span class="kicker">Product Lines</span>
      <h2>Motion Control for Every Axis</h2>
      <p>A complete mechatronics portfolio: servo motors, servo drives and frequency inverters for machine tools, robotics, packaging, pumps, fans and harsh-environment applications.</p>
    </div>
    <div class="cat-grid">
{cats}    </div>
  </div>
</section>

<section class="section alt">
  <div class="container">
    <div class="section-head">
      <span class="kicker">Our Products</span>
      <h2>Featured Series</h2>
      <p>Click any product to see detailed specifications, features and application notes. All prices on request — contact us for a quotation.</p>
    </div>
    <div class="product-grid">
{cards}
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-head center">
      <span class="kicker">Why FarFlight</span>
      <h2>A Trusted Bridge to China's Drive Industry</h2>
    </div>
    <div class="why-grid">
{why}    </div>
  </div>
</section>
{cta_banner()}"""

    return head("Industrial Servo Motors, Servo Drives & VFD Inverters | 工业伺服电机·伺服驱动器·变频器 | FarFlight Mechatronics",
                "FarFlight Mechatronics supplies EURA DRIVES servo motors (40–180 mm), servo drives (100 W–110 kW, EtherCAT/CANopen) and vector inverters (0.2–450 kW, up to IP67) worldwide. Contact us for pricing and quotations. 远翔贸易供应工业伺服电机、伺服驱动器与矢量变频器，支持 EtherCAT/CANopen，功率覆盖 0.2–450kW，全球发货，欢迎询价。",
                "home") + header("home") + body + footer()


def page_products():
    cards = "\n".join(product_card(p) for p in PRODUCTS)
    filters = '<button class="filter-btn active" data-filter="all">All Products</button>\n'
    for g in GROUPS:
        gid = g.lower().replace(" ", "-")
        filters += f'<button class="filter-btn" data-filter="{E(g)}" id="filter-{gid}">{E(g)}</button>\n'

    body = f"""
<div class="about-hero">
  <div class="container">
    <h1>Products</h1>
    <p>Eight industrial series spanning servo motors, servo drives and vector inverters. Detailed specifications, ordering codes and application notes on every product page.</p>
  </div>
</div>

<section class="section">
  <div class="container">
    <div class="filter-bar">
{filters}    </div>
    <div class="product-grid">
{cards}
    </div>
  </div>
</section>
{cta_banner()}"""

    return head("Products | FarFlight Mechatronics",
                "Browse EURA DRIVES servo motors, bus-type and dual-axis servo drives, and vector inverters from 0.2 to 450 kW — supplied worldwide by FarFlight Trading Co., Ltd.",
                "products") + header("products") + body + footer()


def page_product(p):
    depth = 1
    # gallery
    img_defs = [
        ("photo", "Product photo"),
        ("front", "Front view"),
        ("side", "Side view"),
        ("back", "Rear view"),
        ("detail", "Detail view"),
    ]
    first_img = "../" + p["images"]["photo"]
    thumbs = ""
    for i, (key, caption) in enumerate(img_defs):
        src = "../" + p["images"][key]
        cls = "thumb active" if i == 0 else "thumb"
        thumbs += f'<button class="{cls}" data-full="{src}" data-caption="{caption}"><img src="{src}" alt="{E(p["short_name"])} {caption}" loading="lazy"></button>\n'

    key_specs = ""
    for ks in p["key_specs"]:
        key_specs += f'<div class="ks-row"><div class="k">{E(ks["label"])}</div><div class="v">{E(ks["value"])}</div></div>\n'

    # features
    features = ""
    for i, ft in enumerate(p["features"]):
        icon = ICONS[FEATURE_ICON_SEQ[i % len(FEATURE_ICON_SEQ)]]
        features += f"""<div class="feature-item">
  <div class="f-icon">{icon}</div>
  <div><h3>{E(ft['title'])}</h3><p>{E(ft['text'])}</p></div>
</div>\n"""

    # specifications
    specs_html = ""
    for grp in p["specifications"]:
        rows = ""
        for item in grp["items"]:
            rows += f'<tr><th>{E(item["label"])}</th><td>{E(item["value"])}</td></tr>\n'
        specs_html += f'<div class="spec-group"><h3>{E(grp["group"])}</h3><table class="spec-table">\n{rows}</table></div>\n'

    apps = "\n".join(f'<span class="chip">{E(a)}</span>' for a in p["applications"])

    # related
    related = [x for x in PRODUCTS if x["group"] == p["group"] and x["slug"] != p["slug"]]
    others = [x for x in PRODUCTS if x["slug"] != p["slug"] and x not in related]
    related = (related + others)[:3]
    related_html = "\n".join(product_card(x, depth=1) for x in related)

    wa = wa_number_digits()
    desc = p["summary"]
    p_keywords = (p["name"] + ", " + p["category"] + ", " + SLUG_ZH_KEYWORDS.get(p["slug"], "") +
                  ", servo drive quotation, buy online, FarFlight Mechatronics")

    body = f"""
<div class="container">
  <nav class="breadcrumb">
    <a href="../index.html">Home</a><span class="sep">/</span><a href="../products.html">Products</a><span class="sep">/</span>{E(p['short_name'])}
  </nav>
</div>

<div class="product-detail container">
  <div class="detail-grid">
    <div class="gallery" data-gallery>
      <div class="main-img" data-lightbox="{first_img}"><img src="{first_img}" alt="{E(p['name'])}"></div>
      <div class="thumbs">
{thumbs}      </div>
      <div class="caption">Product photo</div>
    </div>

    <div class="detail-info">
      <span class="cat-chip">{E(p['category'])}</span>
      <h1>{E(p['name'])}</h1>
      <p class="tagline">{E(p['tagline'])}</p>
      <div class="key-specs">
{key_specs}      </div>
      <div class="price-box">
        <div class="label">Price</div>
        <div class="value">? &mdash; On Request</div>
        <div class="note">{E(p['price_note'])} — tell us your ratings, quantity and destination for a fast quotation.</div>
        <div class="actions">
          <a class="btn btn-primary btn-block" data-enquire="{E(p['name'])}" data-mail="{SITE['email']}" href="#">{ICONS['mail']} Email Enquiry</a>
          <a class="btn btn-primary btn-block wa-btn" data-enquire="{E(p['name'])}" data-wa="{wa}" href="#" target="_blank" rel="noopener">{ICONS['chat']} WhatsApp</a>
          <a class="btn btn-accent btn-block" style="grid-column:1/-1" href="../payment.html?product={p['slug']}">{ICONS['cart']} Order &amp; Pay</a>
        </div>
      </div>
    </div>
  </div>

  <div class="detail-sections">
    <div class="d-section">
      <h2>Overview</h2>
      {''.join('<p>%s</p>' % E(par) for par in p['description'])}
    </div>

    <div class="d-section">
      <h2>Key Features</h2>
      <div class="features-grid">
{features}      </div>
    </div>

    <div class="d-section">
      <h2>Specifications</h2>
{specs_html}    </div>

    <div class="d-section">
      <h2>Applications</h2>
      <div class="chips">
{apps}
      </div>
    </div>

    <div class="d-section">
      <h2>Models &amp; Ordering</h2>
      <div class="models-note">{E(p['models'])}</div>
      <p style="margin-top:16px;color:var(--muted);font-size:15px;">Not sure which model fits your machine? <a href="../contact.html"><strong>Contact us</strong></a> with your application details — our team will recommend the right drive, motor and options.</p>
    </div>
  </div>

  <div class="section-head" style="margin-top:60px;">
    <span class="kicker">Explore More</span>
    <h2>Related Products</h2>
  </div>
  <div class="product-grid cols-3">
{related_html}
  </div>
</div>
{cta_banner(1)}"""

    return head(f"{p['name']} | FarFlight Mechatronics", desc, "products", depth=1, keywords=p_keywords) + header("products", depth=1) + body + footer(depth=1)


def page_about():
    body = f"""
<div class="about-hero">
  <div class="container">
    <h1>About FarFlight</h1>
    <p>A comprehensive trading enterprise connecting China's manufacturing strength with the global market.</p>
  </div>
</div>

<section class="section">
  <div class="container about-body">
    <div class="main">
      <p>FarFlight Trading Co., Ltd is a comprehensive trading enterprise with extensive experience in cross-border commerce. We have mature expertise in the domestic and international distribution and sales of machinery &amp; electronics, household goods, and sports &amp; fitness products.</p>
      <p>Backed by a well-established global supply chain and sales network, our products are widely sold across Europe, North America, Southeast Asia, the Middle East, and Africa. With reliable product quality, flexible trading solutions, efficient logistics, and professional service, we have built long-term partnerships and earned the trust of clients worldwide.</p>
      <p>Our <strong>mechatronics division</strong> focuses on industrial motion control. We supply EURA DRIVES servo motors, servo drive systems and vector inverters — covering everything from compact 40 mm servo motors and slim single-board drives to 450 kW industrial inverters and IP67 motor-integrated units — helping machine builders, integrators and distributors worldwide keep their automation running.</p>
      <p>Looking ahead, FarFlight Trading remains committed to the principles of integrity, quality, and mutual benefit — continuously expanding our product lines and global reach, and serving as a trusted bridge between manufacturers and international markets.</p>
    </div>
    <aside class="about-aside">
      <div class="logo-panel">
        <img src="assets/images/logo.png" alt="FarFlight Trading Co., Ltd logo">
        <div class="co">远翔贸易有限公司</div>
        <div class="en">FarFlight Trading Co., Ltd</div>
      </div>
      <div class="fact-list">
        <h3>Company Facts</h3>
        <ul>
          <li>Product focus: servo motors, servo drives, VFD inverters</li>
          <li>Markets: Europe, North America, Southeast Asia, Middle East, Africa</li>
          <li>Values: integrity first, quality first, mutual benefit</li>
          <li>Support: model selection, quotations, logistics &amp; documentation</li>
          <li>Contact: email &amp; WhatsApp, replies within 24 hours</li>
        </ul>
      </div>
    </aside>
  </div>
</section>
{cta_banner()}"""

    return head("About Us | FarFlight Mechatronics",
                "FarFlight Trading Co., Ltd is a cross-border trading enterprise supplying EURA DRIVES servo and drive products worldwide, guided by integrity, quality and mutual benefit.",
                "about") + header("about") + body + footer()


def page_contact():
    wa = wa_number_digits()
    body = f"""
<div class="about-hero">
  <div class="container">
    <h1>Contact Us</h1>
    <p>Quotations, technical advice, lead times and shipping — we reply within 24 hours.</p>
  </div>
</div>

<section class="section">
  <div class="container">
    <div class="contact-grid">
      <div class="contact-card">
        <div class="icon">{ICONS['mail']}</div>
        <h3>Email</h3>
        <p>Send us your enquiry anytime</p>
        <div class="val"><a href="mailto:{SITE['email']}">{SITE['email']}</a></div>
      </div>
      <div class="contact-card">
        <div class="icon">{ICONS['chat']}</div>
        <h3>WhatsApp</h3>
        <p>Fast chat for quotes &amp; support</p>
        <div class="val"><a href="{SITE['whatsapp_link']}" target="_blank" rel="noopener">{SITE['whatsapp_number']}</a></div>
      </div>
      <div class="contact-card">
        <div class="icon">{ICONS['cart']}</div>
        <h3>Ready to Order?</h3>
        <p>Generate your order number and pay</p>
        <div class="val"><a href="payment.html">Order &amp; Payment &rarr;</a></div>
      </div>
    </div>

    <div class="contact-wrap">
      <div class="form-card">
        <h2>Send Us a Message</h2>
        <p class="form-note">Sends your message straight to our inbox — no email app or account needed. (Clicking our email address opens your own mail app, e.g. Outlook.)</p>
        <form id="contact-form" action="https://formsubmit.co/{SITE['email']}" method="POST" data-mail="{SITE['email']}" data-wa="{wa}">
          <div class="form-row">
            <div class="form-group">
              <label for="cf-name">Your Name <span class="req">*</span></label>
              <input type="text" id="cf-name" name="name" required placeholder="John Smith">
            </div>
            <div class="form-group">
              <label for="cf-email">Your Email <span class="req">*</span></label>
              <input type="email" id="cf-email" name="email" required placeholder="you@company.com">
            </div>
          </div>
          <div class="form-group">
            <label for="cf-subject">Subject</label>
            <input type="text" id="cf-subject" name="_subject" placeholder="Quotation request: SD20-E servo drive">
          </div>
          <div class="form-group">
            <label for="cf-message">Message <span class="req">*</span></label>
            <textarea id="cf-message" name="message" required placeholder="Product, model / power rating, quantity, destination country, target price..."></textarea>
          </div>
          <input type="hidden" name="_template" value="table">
          <input type="hidden" name="_captcha" value="false">
          <input type="text" name="_honey" style="display:none" tabindex="-1" autocomplete="off">
          <div class="form-actions">
            <button type="submit" class="btn btn-primary" id="cf-submit">{ICONS['mail']} Send Message</button>
            <a class="btn btn-outline-dark" href="{SITE['whatsapp_link']}" target="_blank" rel="noopener">{ICONS['chat']} Chat on WhatsApp</a>
          </div>
          <p class="form-hint">Tip: including the product series, power rating, quantity and your country helps us quote faster. To write an email in your own mail app instead, click our email address above.</p>
          <div class="form-status" id="form-status" role="status"><span id="form-status-text"></span></div>
        </form>
      </div>
      <aside>
        <div class="fact-list" style="margin-top:0;">
          <h3>What to Include</h3>
          <ul>
            <li>Product series and model / power rating</li>
            <li>Quantity needed and target delivery date</li>
            <li>Destination country &amp; port (for shipping quote)</li>
            <li>Your company name and contact details</li>
          </ul>
        </div>
        <div class="fact-list" style="margin-top:22px;">
          <h3>Business Hours</h3>
          <ul>
            <li>Monday &ndash; Friday, 9:00 &ndash; 18:00 (GMT+8)</li>
            <li>WhatsApp messages answered within 24 hours</li>
            <li>Worldwide shipping via express, air &amp; sea freight</li>
          </ul>
        </div>
      </aside>
    </div>
  </div>
</section>"""

    return head("Contact Us | FarFlight Mechatronics",
                f"Contact FarFlight Mechatronics by email ({SITE['email']}) or WhatsApp ({SITE['whatsapp_number']}) for quotations on EURA DRIVES servo motors, drives and inverters.",
                "contact") + header("contact") + body + footer()


def page_payment():
    wa = wa_number_digits()
    options = "\n".join(
        f'<option value="{p["slug"]}" data-name="{E(p["name"])}">{E(p["name"])}</option>' for p in PRODUCTS
    )
    body = f"""
<div class="about-hero">
  <div class="container">
    <h1>Order &amp; Payment <span style="color:#f5a623;">/</span> 订单与支付</h1>
    <p>Place your order and pay securely via Alipay. Bilingual instructions below. / 提交订单并通过支付宝付款，中英文双语说明如下。</p>
  </div>
</div>

<section class="section">
  <div class="container">
    <div class="form-status ok" id="paid-banner" style="display:none;margin-bottom:26px;">
      <strong>✓ Payment successful / 支付成功！</strong> We have received your payment for order <strong id="paid-order"></strong>. A confirmation will be sent to you shortly. / 我们已收到您的款项，将尽快与您联系确认订单。
    </div>
    <div class="pay-steps">
      <div class="pay-step">
        <div class="step-num">1</div>
        <h3>Submit Order Details / 提交订单</h3>
        <p>Select the product, enter the model, quantity and your contact details, then generate your order number.</p>
        <p class="zh">选择商品，填写型号、数量和联系方式，生成订单编号。</p>
      </div>
      <div class="pay-step">
        <div class="step-num">2</div>
        <h3>Pay via Alipay / 支付宝付款</h3>
        <p>Scan the Alipay QR code, or click <strong>Pay Online with Alipay</strong> (shown after you generate your order number) to pay directly on the official Alipay page. Online payments are confirmed to us automatically.</p>
        <p class="zh">扫描支付宝二维码，或生成订单编号后点击<strong>「支付宝在线支付」</strong>按钮，跳转支付宝官方收银台直接付款，付款后系统自动通知我们。</p>
      </div>
      <div class="pay-step">
        <div class="step-num">3</div>
        <h3>Confirm Your Order / 确认订单</h3>
        <p>Send us your order confirmation by email or WhatsApp so we can verify the payment and arrange shipment.</p>
        <p class="zh">通过邮件或 WhatsApp 发送订单确认，以便我们核对款项并安排发货。</p>
      </div>
    </div>

    <div class="pay-wrap">
      <div class="form-card">
        <h2>Your Order / 您的订单</h2>
        <p class="form-note">Fields marked <span class="req" style="color:#d05050">*</span> are required. / 带 <span style="color:#d05050">*</span> 为必填项。</p>
        <form id="order-form" data-mail="{SITE['email']}" data-wa="{wa}">
          <div class="form-group">
            <label for="of-product">Product / 商品 <span style="color:#d05050">*</span></label>
            <select id="of-product" required>
              <option value="">— Select a product / 请选择商品 —</option>
{options}
            </select>
          </div>
          <div class="form-group">
            <label for="of-model">Model / Power Rating / 型号·功率</label>
            <input type="text" id="of-model" placeholder="e.g. SD20-E102T2M2 / 1 kW">
          </div>
          <div class="form-row">
            <div class="form-group">
              <label for="of-qty">Quantity / 数量 <span style="color:#d05050">*</span></label>
              <input type="number" id="of-qty" min="1" value="1" required>
            </div>
            <div class="form-group">
              <label for="of-amount">Amount (CNY) / 付款金额（元） <span style="color:#d05050">*</span></label>
              <input type="number" id="of-amount" min="0.01" step="0.01" placeholder="e.g. 5800.00">
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label for="of-name">Your Name / 姓名 <span style="color:#d05050">*</span></label>
              <input type="text" id="of-name" required placeholder="John Smith">
            </div>
            <div class="form-group">
              <label for="of-contact">Email / WhatsApp / Phone / 联系方式 <span style="color:#d05050">*</span></label>
              <input type="text" id="of-contact" required placeholder="you@company.com / +1 ...">
            </div>
          </div>
          <div class="form-group">
            <label for="of-note">Remarks / 备注</label>
            <textarea id="of-note" placeholder="Delivery address, shipping method, special requirements... / 收货地址、运输方式、特殊要求..."></textarea>
          </div>
          <div class="form-actions">
            <button type="button" class="btn btn-primary" id="gen-order">{ICONS['check']} Generate Order Number / 生成订单编号</button>
            <a class="btn btn-accent" id="pay-alipay" href="#" style="opacity:0.55;cursor:not-allowed;" title="Generate your order number first / 请先生成订单编号">{ICONS['cart']} Pay Online with Alipay / 支付宝在线支付</a>
          </div>

          <div class="order-summary" id="order-summary">
            <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:8px;">
              <div><strong>Order Number / 订单编号:</strong> <span class="onum" id="order-number">—</span></div>
              <button type="button" class="copy-btn" id="copy-order">Copy payment note</button>
            </div>
            <div style="margin-top:12px;">
              <strong>Payment note / 付款备注:</strong>
              <div id="sum-note" style="margin-top:6px;background:#fff;border:1px dashed #c3d3e2;border-radius:6px;padding:10px 12px;font-family:monospace;font-size:13px;">
                Order &lt;number&gt; | &lt;product&gt; model &lt;model&gt; x&lt;qty&gt; | &lt;name&gt; | &lt;contact&gt;
              </div>
              <table style="width:100%;margin-top:10px;font-size:13.5px;border-collapse:collapse;">
                <tr><td style="padding:4px 0;color:var(--muted);">Product / 商品:</td><td id="sum-product" style="text-align:right;font-weight:700;">—</td></tr>
                <tr><td style="padding:4px 0;color:var(--muted);">Model / 型号:</td><td id="sum-model" style="text-align:right;font-weight:700;">—</td></tr>
                <tr><td style="padding:4px 0;color:var(--muted);">Quantity / 数量:</td><td id="sum-qty" style="text-align:right;font-weight:700;">—</td></tr>
                <tr><td style="padding:4px 0;color:var(--muted);">Name / 姓名:</td><td id="sum-name" style="text-align:right;font-weight:700;">—</td></tr>
                <tr><td style="padding:4px 0;color:var(--muted);">Contact / 联系方式:</td><td id="sum-contact" style="text-align:right;font-weight:700;">—</td></tr>
              </table>
            </div>
            <div style="display:flex;gap:10px;flex-wrap:wrap;margin-top:16px;">
              <a class="btn btn-primary btn-sm" id="confirm-mail" href="#" style="display:none;">{ICONS['mail']} Confirm by Email / 邮件确认</a>
              <a class="btn btn-primary btn-sm" id="confirm-wa" href="#" target="_blank" rel="noopener" style="display:none;">{ICONS['chat']} Confirm on WhatsApp / WhatsApp 确认</a>
            </div>
          </div>
          <div class="form-status" id="pay-status"><span id="pay-status-text"></span></div>
        </form>
      </div>

      <aside class="qr-panel">
        <h3>Alipay / 支付宝</h3>
        <div class="qr-box">
          <img src="{SITE['alipay_qr']}" alt="Alipay payment QR code / 支付宝收款码">
        </div>
        <p class="en">Scan to pay with the Alipay app</p>
        <p class="zh">请使用支付宝 App 扫码付款</p>
        <div class="pay-alert">
          <strong>Payment Reminder / 付款提示</strong><br>
          When paying, please add a note with your <strong>Order Number, Product Model, Quantity and Contact Information</strong> so we can match your payment quickly.<br>
          付款时请务必备注<strong>订单编号、商品型号、数量、联系方式</strong>，以便我们快速核对您的款项并安排发货。
        </div>
      </aside>
    </div>
  </div>
</section>"""

    return head("Order & Payment | FarFlight Mechatronics",
                "Place your order and pay via Alipay. Include your order number, product model, quantity and contact in the payment note. 订单与支付：付款请备注订单编号、商品型号、数量及联系方式。",
                "contact") + header("contact") + body + footer()


def page_404():
    body = """
<div class="about-hero">
  <div class="container">
    <h1>404 — Page Not Found</h1>
    <p>The page you are looking for does not exist or has been moved.</p>
  </div>
</div>
<section class="section">
  <div class="container" style="text-align:center;">
    <a class="btn btn-primary" href="index.html">Back to Home</a>
  </div>
</section>"""
    return head("Page Not Found | FarFlight Mechatronics", "Page not found.", "") + header("") + body + footer()


def write_file(rel_path, content):
    path = os.path.join(OUT_ROOT, rel_path)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    print("Generated", rel_path)


def main():
    write_file("index.html", page_index())
    write_file("products.html", page_products())
    for p in PRODUCTS:
        write_file(product_url(p), page_product(p))
    write_file("about.html", page_about())
    write_file("contact.html", page_contact())
    write_file("payment.html", page_payment())
    write_file("404.html", page_404())
    robots = "User-agent: *\nAllow: /\n"
    if DOMAIN:
        pages = [""] + ["product/%s" % p["slug"] for p in PRODUCTS] + \
                ["products", "about", "contact", "payment"]
        sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n'
        sitemap += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        for pg in pages:
            sitemap += "  <url>\n    <loc>%s/%s</loc>\n  </url>\n" % (DOMAIN.rstrip("/"), pg + ".html" if pg else "")
        sitemap += "</urlset>\n"
        write_file("sitemap.xml", sitemap)
        robots += "Sitemap: %s/sitemap.xml\n" % DOMAIN.rstrip("/")
    else:
        print("NOTE: DOMAIN not set - sitemap.xml skipped (set DOMAIN in tools/build.py after deployment)")
    write_file("robots.txt", robots)
    print("Done: %d products generated." % len(PRODUCTS))


if __name__ == "__main__":
    main()
