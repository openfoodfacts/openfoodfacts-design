#!/usr/bin/env python3
import os
import glob
import json
import re

repo_root = '/Users/pierre/development/openfoodfacts-design'

# 1. Collect all assets
assets = []
categories = {
    'animated': {'name': '✨ Animated SVGs', 'count': 0},
    'food': {'name': '🥗 Food Illustrations', 'count': 0},
    'shared': {'name': '🤝 Shared Illustrations', 'count': 0},
    'logos': {'name': '🏷️ Brand Logos', 'count': 0},
    'scores': {'name': '🚦 Nutri-Score & Green-Score', 'count': 0},
    'prices': {'name': '💰 Open Prices', 'count': 0},
    'products': {'name': '📦 Products', 'count': 0},
    'beauty': {'name': '🧴 Beauty', 'count': 0},
    'petfood': {'name': '🐾 Pet Food', 'count': 0},
    'animations': {'name': '🎬 Motion & Videos', 'count': 0},
}

for root, dirs, files in os.walk(repo_root):
    if '.git' in root or 'node_modules' in root:
        continue
    for f in files:
        ext = os.path.splitext(f)[1].lower()
        if ext in ['.svg', '.png', '.jpg', '.gif', '.mp4', '.riv']:
            full_path = os.path.join(root, f)
            rel_path = os.path.relpath(full_path, repo_root)
            size = os.path.getsize(full_path)
            
            # Check if animated SVG
            is_animated = False
            if ext == '.svg':
                try:
                    with open(full_path, 'r', encoding='utf-8', errors='ignore') as sfp:
                        sdata = sfp.read()
                        if '@keyframes' in sdata or '<animate' in sdata or 'animation:' in sdata:
                            is_animated = True
                except:
                    pass

            # Classify category
            cat = 'shared'
            if is_animated:
                cat = 'animated'
            elif 'illustrations/food' in rel_path:
                cat = 'food'
            elif 'illustrations/shared' in rel_path:
                cat = 'shared'
            elif 'illustrations/prices' in rel_path:
                cat = 'prices'
            elif 'illustrations/products' in rel_path:
                cat = 'products'
            elif 'illustrations/beauty' in rel_path:
                cat = 'beauty'
            elif 'illustrations/pet-food' in rel_path:
                cat = 'petfood'
            elif 'nutri-score' in rel_path or 'green-score' in rel_path or 'un-sdg' in rel_path:
                cat = 'scores'
            elif 'logos' in rel_path:
                cat = 'logos'
            elif 'animations' in rel_path or ext in ['.mp4', '.gif', '.riv']:
                cat = 'animations'

            if cat in categories:
                categories[cat]['count'] += 1

            assets.append({
                'name': f,
                'path': rel_path,
                'size': size,
                'category': cat,
                'animated': is_animated,
                'ext': ext.replace('.', '')
            })

# Sort assets
assets.sort(key=lambda x: (not x['animated'], x['category'], x['name']))

# 2. Collect UXR & Charter docs
uxr_docs = []
for root, dirs, files in os.walk(repo_root):
    if '.git' in root:
        continue
    for f in files:
        if f.endswith('.md') and any(k in root for k in ['UXR', 'graphic-charter', 'designs', 'animations']):
            full_path = os.path.join(root, f)
            rel_path = os.path.relpath(full_path, repo_root)
            with open(full_path, 'r', encoding='utf-8', errors='ignore') as fp:
                content = fp.read()
            doc_cat = 'UXR Research'
            if 'UXR Ops' in rel_path: doc_cat = 'UXR Operations'
            elif 'UXR Open Prices' in rel_path: doc_cat = 'Open Prices UXR'
            elif 'UXR Reports' in rel_path: doc_cat = 'Research Reports'
            elif 'graphic-charter' in rel_path: doc_cat = 'Brand Charter'
            
            clean_title = f.replace('.md', '').replace('_', ' ')
            uxr_docs.append({
                'title': clean_title,
                'path': rel_path,
                'category': doc_cat,
                'content': content
            })

uxr_docs.sort(key=lambda x: (x['category'], x['title']))

print(f"Collected {len(assets)} assets and {len(uxr_docs)} documentation guides.")

# 3. Generate index.html
assets_json = json.dumps(assets)
uxr_json = json.dumps(uxr_docs)

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Open Food Facts — Design System &amp; Asset Hub</title>
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
    <!-- Marked for Markdown rendering -->
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <style>
        body {{
            font-family: 'Plus Jakarta Sans', sans-serif;
        }}
        pre, code {{
            font-family: 'JetBrains Mono', monospace;
        }}
        .brand-gradient {{
            background: linear-gradient(135deg, #ed8857 0%, #ea580c 50%, #c2410c 100%);
        }}
        .glass-header {{
            background: rgba(255, 255, 255, 0.92);
            backdrop-filter: blur(12px);
        }}
        .nav-link.active {{
            background-color: #ffedd5;
            color: #c2410c;
            font-weight: 700;
        }}
        /* Animation Pause/Play helper */
        svg.paused * {{
            animation-play-state: paused !important;
        }}
        /* Custom scrollbar */
        ::-webkit-scrollbar {{ width: 8px; height: 8px; }}
        ::-webkit-scrollbar-track {{ background: #f1f5f9; }}
        ::-webkit-scrollbar-thumb {{ background: #cbd5e1; border-radius: 4px; }}
        ::-webkit-scrollbar-thumb:hover {{ background: #94a3b8; }}
    </style>
</head>
<body class="bg-stone-50 text-stone-900 antialiased min-h-screen flex flex-col">

    <!-- Top Announcement & Repo Bar -->
    <div class="bg-stone-900 text-stone-300 text-xs py-2 px-4 flex flex-wrap items-center justify-between gap-2 border-b border-stone-800">
        <div class="flex items-center gap-2">
            <span class="inline-block w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
            <span>Open Food Facts Design Hub &bull; Automatic GitHub Pages Deployment Active</span>
        </div>
        <div class="flex items-center gap-4">
            <a href="https://github.com/openfoodfacts/openfoodfacts-design" target="_blank" rel="noopener noreferrer" class="hover:text-white transition flex items-center gap-1.5 font-medium">
                <svg class="w-4 h-4 fill-current" viewBox="0 0 24 24"><path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0 0 24 12c0-6.63-5.37-12-12-12z"/></svg>
                <span>GitHub Repository</span>
            </a>
            <a href="https://slack.openfoodfacts.org" target="_blank" rel="noopener noreferrer" class="hover:text-white transition">
                💬 #design on Slack
            </a>
        </div>
    </div>

    <!-- Main Navigation Header -->
    <header class="sticky top-0 z-40 glass-header border-b border-stone-200/80 shadow-xs">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex items-center justify-between h-16 gap-4">
                
                <!-- Logo & Brand Title -->
                <div class="flex items-center gap-3">
                    <img src="images/logos/openfoodfacts/off-logo-icon-light.svg" alt="Open Food Facts" class="w-9 h-9">
                    <div>
                        <span class="text-lg font-black tracking-tight text-stone-900 block leading-tight">Open Food Facts</span>
                        <span class="text-[11px] font-bold text-orange-600 tracking-wider uppercase block">Design System &amp; Assets</span>
                    </div>
                </div>

                <!-- Navigation Tabs -->
                <nav class="hidden md:flex items-center gap-1">
                    <button onclick="switchTab('catalog')" id="nav-catalog" class="nav-link active px-3.5 py-2 rounded-xl text-xs font-semibold text-stone-600 hover:text-stone-900 hover:bg-stone-100 transition cursor-pointer">
                        🖼️ Asset Catalog
                    </button>
                    <button onclick="switchTab('charter')" id="nav-charter" class="nav-link px-3.5 py-2 rounded-xl text-xs font-semibold text-stone-600 hover:text-stone-900 hover:bg-stone-100 transition cursor-pointer">
                        🎨 Graphic Charter
                    </button>
                    <button onclick="switchTab('hand')" id="nav-hand" class="nav-link px-3.5 py-2 rounded-xl text-xs font-semibold text-stone-600 hover:text-stone-900 hover:bg-stone-100 transition cursor-pointer">
                        📱 Hand Mockup Generator
                    </button>
                    <button onclick="switchTab('avatar')" id="nav-avatar" class="nav-link px-3.5 py-2 rounded-xl text-xs font-semibold text-stone-600 hover:text-stone-900 hover:bg-stone-100 transition cursor-pointer">
                        👤 Avatar Creator
                    </button>
                    <button onclick="switchTab('uxr')" id="nav-uxr" class="nav-link px-3.5 py-2 rounded-xl text-xs font-semibold text-stone-600 hover:text-stone-900 hover:bg-stone-100 transition cursor-pointer">
                        🔬 UX Research (UXR)
                    </button>
                    <button onclick="switchTab('motion')" id="nav-motion" class="nav-link px-3.5 py-2 rounded-xl text-xs font-semibold text-stone-600 hover:text-stone-900 hover:bg-stone-100 transition cursor-pointer">
                        🎬 Motion &amp; Videos
                    </button>
                </nav>

                <!-- Mobile Menu Button -->
                <div class="md:hidden flex items-center">
                    <select onchange="switchTab(this.value)" class="text-xs font-bold bg-white border border-stone-300 rounded-lg px-2.5 py-1.5 text-stone-800">
                        <option value="catalog">🖼️ Assets Catalog</option>
                        <option value="charter">🎨 Graphic Charter</option>
                        <option value="hand">📱 Hand Generator</option>
                        <option value="avatar">👤 Avatar Creator</option>
                        <option value="uxr">🔬 UX Research</option>
                        <option value="motion">🎬 Motion &amp; Videos</option>
                    </select>
                </div>
            </div>
        </div>
    </header>

    <!-- Content Sections -->
    <main class="flex-grow max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">

        <!-- ============================================================== -->
        <!-- TAB 1: ASSETS CATALOG                                          -->
        <!-- ============================================================== -->
        <section id="tab-catalog" class="space-y-6">
            <!-- Hero Banner -->
            <div class="bg-gradient-to-r from-orange-50 via-amber-50 to-orange-100/60 border border-orange-200/80 rounded-3xl p-6 sm:p-8 flex flex-wrap items-center justify-between gap-6 shadow-xs">
                <div class="max-w-2xl">
                    <span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold bg-orange-200/60 text-orange-800 uppercase tracking-wide mb-3">
                        ⚡ Official Vector &amp; Motion Assets
                    </span>
                    <h1 class="text-3xl font-black text-stone-900 tracking-tight leading-tight">
                        Explore Open Food Facts Design Assets
                    </h1>
                    <p class="text-stone-600 text-sm sm:text-base mt-2 leading-relaxed">
                        Discover 650+ production-grade illustrations, animated SVGs, logos, and iconography for web, mobile apps, and community campaigns.
                    </p>
                </div>
                <div class="flex flex-wrap items-center gap-2">
                    <div class="bg-white/90 backdrop-blur rounded-2xl p-4 border border-orange-200 shadow-xs text-center min-w-[110px]">
                        <span class="block text-2xl font-black text-orange-600">{len(assets)}</span>
                        <span class="text-xs font-bold text-stone-500 uppercase">Total Assets</span>
                    </div>
                    <div class="bg-white/90 backdrop-blur rounded-2xl p-4 border border-orange-200 shadow-xs text-center min-w-[110px]">
                        <span class="block text-2xl font-black text-emerald-600">30+</span>
                        <span class="text-xs font-bold text-stone-500 uppercase">Animated SVGs</span>
                    </div>
                </div>
            </div>

            <!-- Search & Filter Controls -->
            <div class="bg-white rounded-2xl border border-stone-200 p-4 shadow-xs space-y-3">
                <div class="flex flex-wrap items-center justify-between gap-3">
                    <div class="relative flex-grow max-w-md">
                        <input type="text" id="asset-search" placeholder="Search 650+ assets by name, keyword..." oninput="filterAssets()" class="w-full pl-10 pr-4 py-2.5 text-sm bg-stone-50 border border-stone-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-orange-500/30 focus:border-orange-500 transition">
                        <svg class="w-4 h-4 text-stone-400 absolute left-3.5 top-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>
                    </div>

                    <div class="flex items-center gap-2 text-xs font-medium text-stone-500">
                        <span id="results-count" class="font-bold text-stone-800">Showing {len(assets)} assets</span>
                    </div>
                </div>

                <!-- Category Filter Pills -->
                <div class="flex flex-wrap gap-1.5 pt-2 border-t border-stone-100" id="category-pills">
                    <button onclick="setCategoryFilter('all')" class="cat-pill active px-3 py-1.5 rounded-lg text-xs font-semibold bg-orange-600 text-white transition">
                        All ({len(assets)})
                    </button>
                    <button onclick="setCategoryFilter('animated')" class="cat-pill px-3 py-1.5 rounded-lg text-xs font-semibold bg-stone-100 text-stone-600 hover:bg-stone-200 transition">
                        ✨ Animated SVGs
                    </button>
                    <button onclick="setCategoryFilter('food')" class="cat-pill px-3 py-1.5 rounded-lg text-xs font-semibold bg-stone-100 text-stone-600 hover:bg-stone-200 transition">
                        🥗 Food Illustrations
                    </button>
                    <button onclick="setCategoryFilter('shared')" class="cat-pill px-3 py-1.5 rounded-lg text-xs font-semibold bg-stone-100 text-stone-600 hover:bg-stone-200 transition">
                        🤝 Community &amp; Shared
                    </button>
                    <button onclick="setCategoryFilter('logos')" class="cat-pill px-3 py-1.5 rounded-lg text-xs font-semibold bg-stone-100 text-stone-600 hover:bg-stone-200 transition">
                        🏷️ Brand Logos
                    </button>
                    <button onclick="setCategoryFilter('scores')" class="cat-pill px-3 py-1.5 rounded-lg text-xs font-semibold bg-stone-100 text-stone-600 hover:bg-stone-200 transition">
                        🚦 Nutri &amp; Green-Score
                    </button>
                    <button onclick="setCategoryFilter('prices')" class="cat-pill px-3 py-1.5 rounded-lg text-xs font-semibold bg-stone-100 text-stone-600 hover:bg-stone-200 transition">
                        💰 Open Prices
                    </button>
                    <button onclick="setCategoryFilter('products')" class="cat-pill px-3 py-1.5 rounded-lg text-xs font-semibold bg-stone-100 text-stone-600 hover:bg-stone-200 transition">
                        📦 Products
                    </button>
                    <button onclick="setCategoryFilter('beauty')" class="cat-pill px-3 py-1.5 rounded-lg text-xs font-semibold bg-stone-100 text-stone-600 hover:bg-stone-200 transition">
                        🧴 Beauty
                    </button>
                    <button onclick="setCategoryFilter('petfood')" class="cat-pill px-3 py-1.5 rounded-lg text-xs font-semibold bg-stone-100 text-stone-600 hover:bg-stone-200 transition">
                        🐾 Pet Food
                    </button>
                    <button onclick="setCategoryFilter('animations')" class="cat-pill px-3 py-1.5 rounded-lg text-xs font-semibold bg-stone-100 text-stone-600 hover:bg-stone-200 transition">
                        🎬 Videos &amp; Motion
                    </button>
                </div>
            </div>

            <!-- Asset Cards Grid -->
            <div id="assets-grid" class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
                <!-- Dynamically rendered via JS -->
            </div>
        </section>

        <!-- ============================================================== -->
        <!-- TAB 2: GRAPHIC CHARTER & BRAND GUIDELINES                      -->
        <!-- ============================================================== -->
        <section id="tab-charter" class="hidden space-y-8">
            <div class="bg-white rounded-3xl border border-stone-200 p-6 sm:p-10 shadow-xs">
                <div class="flex flex-wrap items-center justify-between gap-4 pb-6 border-b border-stone-200">
                    <div>
                        <span class="text-xs font-bold text-orange-600 tracking-wider uppercase block">Visual Identity &bull; Version 1</span>
                        <h1 class="text-3xl font-black text-stone-900 tracking-tight mt-1">Open Food Facts Graphic Charter</h1>
                        <p class="text-stone-500 text-sm mt-1">Design rules, logo construction, color palettes, and typography specifications.</p>
                    </div>
                    <a href="graphic-charter/BRAND%20GUIDELINES_OFF_V1.pdf" target="_blank" class="px-5 py-2.5 rounded-xl text-sm font-bold bg-orange-600 hover:bg-orange-700 text-white shadow-sm transition flex items-center gap-2 cursor-pointer">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>
                        Download Full Brand Guidelines (PDF)
                    </a>
                </div>

                <!-- Logo Systems -->
                <div class="mt-8">
                    <h2 class="text-xl font-bold text-stone-900 mb-4">1. The Logo System</h2>
                    <p class="text-sm text-stone-600 mb-6 leading-relaxed">
                        The Open Food Facts logo consists of a barcode smiling face symbol and clean lowercase wordmark set in Plus Jakarta Sans. Always ensure safe margins equal to the width of the barcode bars around the logo.
                    </p>

                    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <!-- Horizontal Logo -->
                        <div class="bg-stone-50 border border-stone-200 rounded-2xl p-6 flex flex-col items-center justify-center">
                            <span class="text-xs font-bold text-stone-500 uppercase tracking-wide mb-4">Primary Horizontal Logo</span>
                            <div class="bg-white p-6 rounded-xl border border-stone-200 w-full flex items-center justify-center min-h-[120px]">
                                <img src="images/logos/openfoodfacts/off-logo-horizontal-light.svg" alt="Open Food Facts Horizontal Logo" class="max-h-12 w-auto">
                            </div>
                            <span class="text-xs text-stone-400 mt-3">Used for navigation bars, headers, and official letterheads.</span>
                        </div>

                        <!-- Dark Mode Horizontal Logo -->
                        <div class="bg-stone-900 border border-stone-800 rounded-2xl p-6 flex flex-col items-center justify-center">
                            <span class="text-xs font-bold text-stone-400 uppercase tracking-wide mb-4">Dark Mode Application</span>
                            <div class="bg-stone-950 p-6 rounded-xl border border-stone-800 w-full flex items-center justify-center min-h-[120px]">
                                <img src="images/logos/openfoodfacts/off-logo-horizontal-dark.svg" alt="Open Food Facts Dark Horizontal Logo" class="max-h-12 w-auto">
                            </div>
                            <span class="text-xs text-stone-400 mt-3">Used against dark backgrounds and dark mode interfaces.</span>
                        </div>
                    </div>
                </div>

                <!-- Color Palette -->
                <div class="mt-12">
                    <h2 class="text-xl font-bold text-stone-900 mb-2">2. Color Palette &amp; Sister Projects</h2>
                    <p class="text-sm text-stone-600 mb-6 leading-relaxed">
                        Each universe has a distinct primary hue while sharing our warm neutral core. Click on any color swatch to copy its HEX code:
                    </p>

                    <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-4">
                        <!-- OFF Orange -->
                        <div onclick="copyColor('#ed8857', this)" class="bg-stone-50 p-3 rounded-2xl border border-stone-200 text-center cursor-pointer hover:border-orange-500 transition group">
                            <div class="w-full h-16 rounded-xl bg-[#ed8857] shadow-xs group-hover:scale-105 transition"></div>
                            <span class="block text-xs font-bold text-stone-900 mt-2">Food Orange</span>
                            <span class="text-[11px] font-mono text-stone-500">#ed8857</span>
                        </div>

                        <!-- Espresso -->
                        <div onclick="copyColor('#341100', this)" class="bg-stone-50 p-3 rounded-2xl border border-stone-200 text-center cursor-pointer hover:border-orange-500 transition group">
                            <div class="w-full h-16 rounded-xl bg-[#341100] shadow-xs group-hover:scale-105 transition"></div>
                            <span class="block text-xs font-bold text-stone-900 mt-2">Deep Espresso</span>
                            <span class="text-[11px] font-mono text-stone-500">#341100</span>
                        </div>

                        <!-- Beauty Turquoise -->
                        <div onclick="copyColor('#00b0ff', this)" class="bg-stone-50 p-3 rounded-2xl border border-stone-200 text-center cursor-pointer hover:border-sky-500 transition group">
                            <div class="w-full h-16 rounded-xl bg-[#00b0ff] shadow-xs group-hover:scale-105 transition"></div>
                            <span class="block text-xs font-bold text-stone-900 mt-2">Beauty Cyan</span>
                            <span class="text-[11px] font-mono text-stone-500">#00b0ff</span>
                        </div>

                        <!-- Pet Food Pink -->
                        <div onclick="copyColor('#f06292', this)" class="bg-stone-50 p-3 rounded-2xl border border-stone-200 text-center cursor-pointer hover:border-pink-500 transition group">
                            <div class="w-full h-16 rounded-xl bg-[#f06292] shadow-xs group-hover:scale-105 transition"></div>
                            <span class="block text-xs font-bold text-stone-900 mt-2">Pet Food Pink</span>
                            <span class="text-[11px] font-mono text-stone-500">#f06292</span>
                        </div>

                        <!-- Products Blue -->
                        <div onclick="copyColor('#2196f3', this)" class="bg-stone-50 p-3 rounded-2xl border border-stone-200 text-center cursor-pointer hover:border-blue-500 transition group">
                            <div class="w-full h-16 rounded-xl bg-[#2196f3] shadow-xs group-hover:scale-105 transition"></div>
                            <span class="block text-xs font-bold text-stone-900 mt-2">Products Blue</span>
                            <span class="text-[11px] font-mono text-stone-500">#2196f3</span>
                        </div>

                        <!-- Prices Green -->
                        <div onclick="copyColor('#10b981', this)" class="bg-stone-50 p-3 rounded-2xl border border-stone-200 text-center cursor-pointer hover:border-emerald-500 transition group">
                            <div class="w-full h-16 rounded-xl bg-[#10b981] shadow-xs group-hover:scale-105 transition"></div>
                            <span class="block text-xs font-bold text-stone-900 mt-2">Open Prices</span>
                            <span class="text-[11px] font-mono text-stone-500">#10b981</span>
                        </div>
                    </div>
                </div>

                <!-- Typography -->
                <div class="mt-12">
                    <h2 class="text-xl font-bold text-stone-900 mb-2">3. Typography</h2>
                    <p class="text-sm text-stone-600 mb-6 leading-relaxed">
                        Our primary corporate typeface is <strong>Plus Jakarta Sans</strong>, an open-source geometric sans-serif designed for clean legibility at both headline and caption scales.
                    </p>

                    <div class="bg-stone-50 border border-stone-200 rounded-2xl p-6 space-y-4">
                        <div>
                            <span class="text-xs font-bold text-stone-400 uppercase">Heading 1 &bull; 900 Black</span>
                            <div class="text-3xl font-black text-stone-900">Better food choices for a healthier planet.</div>
                        </div>
                        <div>
                            <span class="text-xs font-bold text-stone-400 uppercase">Heading 2 &bull; 700 Bold</span>
                            <div class="text-xl font-bold text-stone-800">Collaborative, free, and open database of food products.</div>
                        </div>
                        <div>
                            <span class="text-xs font-bold text-stone-400 uppercase">Body &bull; 400 Regular &amp; 600 Semi-Bold</span>
                            <p class="text-sm text-stone-600 leading-relaxed max-w-3xl">
                                Open Food Facts gathers information and data on food products from around the world. We decode labels, calculate Nutri-Score, Eco-Score, and NOVA groups, and make data available to consumers and researchers.
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- ============================================================== -->
        <!-- TAB 3: HAND SCREENSHOT GENERATOR TOOL                          -->
        <!-- ============================================================== -->
        <section id="tab-hand" class="hidden space-y-6">
            <div class="bg-white rounded-3xl border border-stone-200 p-6 sm:p-10 shadow-xs">
                <div class="flex flex-wrap items-center justify-between gap-4 pb-6 border-b border-stone-200">
                    <div>
                        <span class="text-xs font-bold text-indigo-600 tracking-wider uppercase block">Branded Mockup Tool</span>
                        <h1 class="text-3xl font-black text-stone-900 tracking-tight mt-1">Animated Smartphone Hand Generator</h1>
                        <p class="text-stone-500 text-sm mt-1">Upload your mobile app screenshot into an animated hand frame with customizable skin tones.</p>
                    </div>
                    <a href="tools/hand-screenshot-generator/animated_smartphone_hand_svg_off.html" target="_blank" class="px-5 py-2.5 rounded-xl text-sm font-bold bg-indigo-600 hover:bg-indigo-700 text-white shadow-sm transition flex items-center gap-2 cursor-pointer">
                        <span>Open Standalone Tool</span>
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/></svg>
                    </a>
                </div>

                <!-- Iframe Embed of the Tool -->
                <div class="mt-6 border border-stone-200 rounded-2xl overflow-hidden shadow-inner bg-slate-50 min-h-[720px]">
                    <iframe src="tools/hand-screenshot-generator/animated_smartphone_hand_svg_off.html" class="w-full h-[720px] border-0" title="Hand Screenshot Generator"></iframe>
                </div>
            </div>
        </section>

        <!-- ============================================================== -->
        <!-- TAB 4: AVATAR CREATOR (FIXED & POLISHED)                       -->
        <!-- ============================================================== -->
        <section id="tab-avatar" class="hidden space-y-6">
            <div class="bg-white rounded-3xl border border-stone-200 p-6 sm:p-10 shadow-xs">
                <div class="flex flex-wrap items-center justify-between gap-4 pb-6 border-b border-stone-200">
                    <div>
                        <span class="text-xs font-bold text-orange-600 tracking-wider uppercase block">Community Profiles &bull; Fixed Prototype</span>
                        <h1 class="text-3xl font-black text-stone-900 tracking-tight mt-1">Open Food Facts Avatar Creator</h1>
                        <p class="text-stone-500 text-sm mt-1">Mix and match hairstyles, skin tones, facial expressions, and branded t-shirts.</p>
                    </div>
                    <div class="flex items-center gap-2">
                        <a href="avatars/avatars.html" target="_blank" class="px-4 py-2 rounded-xl text-sm font-bold bg-stone-100 hover:bg-stone-200 text-stone-700 transition">
                            Open Standalone
                        </a>
                    </div>
                </div>

                <!-- Embedded Generator Frame -->
                <div class="mt-6 border border-stone-200 rounded-2xl overflow-hidden shadow-inner bg-stone-50 min-h-[760px]">
                    <iframe src="avatars/avatars.html" class="w-full h-[760px] border-0" title="Avatars Generator"></iframe>
                </div>
            </div>
        </section>

        <!-- ============================================================== -->
        <!-- TAB 5: UX RESEARCH (UXR HUB)                                   -->
        <!-- ============================================================== -->
        <section id="tab-uxr" class="hidden space-y-6">
            <div class="bg-white rounded-3xl border border-stone-200 p-6 sm:p-10 shadow-xs">
                <div class="pb-6 border-b border-stone-200">
                    <span class="text-xs font-bold text-purple-600 tracking-wider uppercase block">User Experience Research</span>
                    <h1 class="text-3xl font-black text-stone-900 tracking-tight mt-1">UX Research Repository &amp; Operations</h1>
                    <p class="text-stone-500 text-sm mt-1">Guides, templates, heuristics, and user research findings across Open Food Facts projects.</p>
                </div>

                <!-- Two-Column UXR Explorer -->
                <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 mt-6">
                    <!-- Left: Doc Navigation Tree -->
                    <div class="lg:col-span-4 space-y-4">
                        <div class="bg-stone-50 rounded-2xl p-4 border border-stone-200">
                            <h3 class="text-xs font-bold text-stone-400 uppercase tracking-wide mb-3">Available Documentation</h3>
                            <div id="uxr-doc-list" class="space-y-1">
                                <!-- Populated dynamically -->
                            </div>
                        </div>
                    </div>

                    <!-- Right: Formatted Markdown Reader -->
                    <div class="lg:col-span-8 bg-stone-50/50 rounded-2xl p-6 sm:p-8 border border-stone-200 min-h-[500px]">
                        <div class="flex items-center justify-between pb-4 border-b border-stone-200 mb-6">
                            <div>
                                <span id="reader-category" class="text-xs font-bold text-orange-600 uppercase tracking-wide">Category</span>
                                <h2 id="reader-title" class="text-xl font-black text-stone-900 mt-0.5">Select a document</h2>
                            </div>
                            <span id="reader-path" class="text-xs font-mono text-stone-400">path</span>
                        </div>
                        <div id="reader-body" class="prose prose-stone max-w-none text-sm leading-relaxed">
                            <p class="text-stone-500 italic">Select any document from the list on the left to read its full content.</p>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- ============================================================== -->
        <!-- TAB 6: MOTION & ANIMATIONS                                     -->
        <!-- ============================================================== -->
        <section id="tab-motion" class="hidden space-y-6">
            <div class="bg-white rounded-3xl border border-stone-200 p-6 sm:p-10 shadow-xs">
                <div class="pb-6 border-b border-stone-200">
                    <span class="text-xs font-bold text-rose-600 tracking-wider uppercase block">Motion Graphics</span>
                    <h1 class="text-3xl font-black text-stone-900 tracking-tight mt-1">Animations, Rive &amp; Video Assets</h1>
                    <p class="text-stone-500 text-sm mt-1">Interactive vector animations, Nutri-Score &amp; Green-Score scans, and brand videos.</p>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mt-8">
                    <!-- Video 1: Sunrise Open Food Facts -->
                    <div class="bg-stone-50 rounded-2xl border border-stone-200 overflow-hidden shadow-xs">
                        <div class="aspect-video bg-black flex items-center justify-center">
                            <video controls class="w-full h-full object-cover">
                                <source src="animations/videos/sunrise-open-food-facts.mp4" type="video/mp4">
                                Your browser does not support the video tag.
                            </video>
                        </div>
                        <div class="p-4">
                            <h3 class="font-bold text-stone-900 text-sm">Sunrise Open Food Facts</h3>
                            <p class="text-xs text-stone-500 mt-1">animations/videos/sunrise-open-food-facts.mp4</p>
                        </div>
                    </div>

                    <!-- Video 2: Icons Open Food Facts -->
                    <div class="bg-stone-50 rounded-2xl border border-stone-200 overflow-hidden shadow-xs">
                        <div class="aspect-video bg-black flex items-center justify-center">
                            <video controls class="w-full h-full object-cover">
                                <source src="animations/videos/icons-open-food-facts.mp4" type="video/mp4">
                                Your browser does not support the video tag.
                            </video>
                        </div>
                        <div class="p-4">
                            <h3 class="font-bold text-stone-900 text-sm">Icons Open Food Facts</h3>
                            <p class="text-xs text-stone-500 mt-1">animations/videos/icons-open-food-facts.mp4</p>
                        </div>
                    </div>

                    <!-- Video 3: Universes OXF -->
                    <div class="bg-stone-50 rounded-2xl border border-stone-200 overflow-hidden shadow-xs">
                        <div class="aspect-video bg-black flex items-center justify-center">
                            <video controls class="w-full h-full object-cover">
                                <source src="animations/videos/universes-oxf.mp4" type="video/mp4">
                                Your browser does not support the video tag.
                            </video>
                        </div>
                        <div class="p-4">
                            <h3 class="font-bold text-stone-900 text-sm">Universes OXF (OFF, OBF, OPFF, OPF)</h3>
                            <p class="text-xs text-stone-500 mt-1">animations/videos/universes-oxf.mp4</p>
                        </div>
                    </div>

                    <!-- Scan Nutriscore & Greenscore -->
                    <div class="bg-stone-50 rounded-2xl border border-stone-200 overflow-hidden shadow-xs">
                        <div class="aspect-video bg-white flex items-center justify-center p-4">
                            <img src="animations/scan-nutriscore-greenscore/scan-nutriscore-greenscore.gif" alt="Scan Animation GIF" class="max-h-full max-w-full object-contain">
                        </div>
                        <div class="p-4">
                            <h3 class="font-bold text-stone-900 text-sm">Scan Nutri-Score &amp; Green-Score</h3>
                            <p class="text-xs text-stone-500 mt-1">Rive &amp; GIF animation format</p>
                            <a href="animations/scan-nutriscore-greenscore/scan-nutriscore-greenscore.riv" download class="mt-2 inline-flex items-center gap-1 text-xs font-bold text-orange-600 hover:text-orange-700">
                                📥 Download .riv File
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        </section>

    </main>

    <!-- Modal for Previewing & Exporting Individual Assets -->
    <div id="asset-modal" class="fixed inset-0 z-50 bg-stone-900/60 backdrop-blur-xs hidden flex items-center justify-center p-4">
        <div class="bg-white rounded-3xl max-w-2xl w-full border border-stone-200 shadow-2xl overflow-hidden flex flex-col max-h-[90vh]">
            <!-- Modal Header -->
            <div class="p-5 border-b border-stone-100 flex items-center justify-between">
                <div>
                    <h3 id="modal-title" class="font-bold text-stone-900 text-base">Asset Title</h3>
                    <p id="modal-path" class="text-xs font-mono text-stone-400 mt-0.5">path/to/asset.svg</p>
                </div>
                <button onclick="closeModal()" class="w-8 h-8 rounded-full bg-stone-100 hover:bg-stone-200 text-stone-600 flex items-center justify-center transition cursor-pointer">
                    &times;
                </button>
            </div>

            <!-- Modal Stage Preview -->
            <div id="modal-stage" class="p-8 bg-stone-50 flex items-center justify-center min-h-[260px] overflow-hidden">
                <!-- Image or SVG rendered here -->
            </div>

            <!-- Modal Actions -->
            <div class="p-5 border-t border-stone-100 bg-white flex flex-wrap items-center justify-between gap-3">
                <div class="flex items-center gap-2">
                    <button id="modal-pause-btn" onclick="toggleModalAnimation()" class="px-3.5 py-2 rounded-xl text-xs font-bold bg-stone-100 hover:bg-stone-200 text-stone-700 transition cursor-pointer hidden">
                        ⏸ Pause Animation
                    </button>
                </div>
                <div class="flex items-center gap-2">
                    <button id="modal-copy-link" onclick="copyAssetMarkdown()" class="px-3.5 py-2 rounded-xl text-xs font-bold bg-white border border-stone-200 hover:bg-stone-50 text-stone-700 transition cursor-pointer">
                        📋 Copy Markdown
                    </button>
                    <a id="modal-download" href="#" download class="px-4 py-2 rounded-xl text-xs font-bold bg-orange-600 hover:bg-orange-700 text-white shadow-xs transition cursor-pointer">
                        📥 Download Asset
                    </a>
                </div>
            </div>
        </div>
    </div>

    <!-- Data Injection -->
    <script>
        const ALL_ASSETS = {assets_json};
        const ALL_UXR_DOCS = {uxr_json};

        let currentCategory = 'all';
        let currentModalAsset = null;
        let isModalPaused = false;

        function switchTab(tabId) {{
            const tabs = ['catalog', 'charter', 'hand', 'avatar', 'uxr', 'motion'];
            tabs.forEach(t => {{
                const el = document.getElementById('tab-' + t);
                const nav = document.getElementById('nav-' + t);
                if (t === tabId) {{
                    el.classList.remove('hidden');
                    if (nav) nav.classList.add('active');
                }} else {{
                    el.classList.add('hidden');
                    if (nav) nav.classList.remove('active');
                }}
            }});
            window.scrollTo({{ top: 0, behavior: 'smooth' }});
        }}

        function setCategoryFilter(cat) {{
            currentCategory = cat;
            document.querySelectorAll('#category-pills button').forEach(b => {{
                b.className = 'cat-pill px-3 py-1.5 rounded-lg text-xs font-semibold bg-stone-100 text-stone-600 hover:bg-stone-200 transition cursor-pointer';
            }});
            event.target.className = 'cat-pill active px-3 py-1.5 rounded-lg text-xs font-semibold bg-orange-600 text-white transition cursor-pointer';
            filterAssets();
        }}

        function filterAssets() {{
            const query = (document.getElementById('asset-search').value || '').toLowerCase().trim();
            const grid = document.getElementById('assets-grid');
            grid.innerHTML = '';

            const filtered = ALL_ASSETS.filter(a => {{
                const matchesCat = currentCategory === 'all' || a.category === currentCategory || (currentCategory === 'animated' && a.animated);
                const matchesQuery = !query || a.name.toLowerCase().includes(query) || a.path.toLowerCase().includes(query);
                return matchesCat && matchesQuery;
            }});

            document.getElementById('results-count').innerText = `Showing ${{filtered.length}} of ${{ALL_ASSETS.length}} assets`;

            filtered.slice(0, 100).forEach(asset => {{
                const card = document.createElement('div');
                card.className = 'bg-white rounded-2xl border border-stone-200/80 p-3 shadow-xs hover:shadow-md hover:border-orange-400 transition flex flex-col group cursor-pointer';
                card.onclick = () => openModal(asset);

                // Preview wrapper
                const preview = document.createElement('div');
                preview.className = 'w-full aspect-square bg-stone-50 rounded-xl flex items-center justify-center p-3 mb-2.5 overflow-hidden relative';

                if (asset.ext === 'mp4') {{
                    preview.innerHTML = '<span class="text-3xl">🎬</span>';
                }} else {{
                    const img = document.createElement('img');
                    img.src = asset.path;
                    img.alt = asset.name;
                    img.loading = 'lazy';
                    img.className = 'max-w-full max-h-full object-contain group-hover:scale-105 transition';
                    preview.appendChild(img);
                }}

                if (asset.animated) {{
                    const animBadge = document.createElement('span');
                    animBadge.className = 'absolute top-1.5 right-1.5 px-1.5 py-0.5 rounded text-[10px] font-bold bg-orange-500 text-white shadow-xs';
                    animBadge.innerText = 'ANIM';
                    preview.appendChild(animBadge);
                }}

                card.appendChild(preview);

                // Title & Details
                const title = document.createElement('span');
                title.className = 'text-xs font-bold text-stone-800 truncate block';
                title.title = asset.name;
                title.innerText = asset.name;
                card.appendChild(title);

                const sizeSpan = document.createElement('span');
                sizeSpan.className = 'text-[10px] text-stone-400 uppercase mt-0.5';
                sizeSpan.innerText = `${{asset.ext.toUpperCase()}} &bull; ${{Math.round(asset.size / 1024)}} KB`;
                card.appendChild(sizeSpan);

                grid.appendChild(card);
            }});
        }}

        function openModal(asset) {{
            currentModalAsset = asset;
            document.getElementById('modal-title').innerText = asset.name;
            document.getElementById('modal-path').innerText = asset.path;
            document.getElementById('modal-download').href = asset.path;
            document.getElementById('modal-download').download = asset.name;

            const stage = document.getElementById('modal-stage');
            stage.innerHTML = '';

            const pauseBtn = document.getElementById('modal-pause-btn');
            if (asset.animated) {{
                pauseBtn.classList.remove('hidden');
                pauseBtn.innerText = '⏸ Pause Animation';
                isModalPaused = false;
            }} else {{
                pauseBtn.classList.add('hidden');
            }}

            if (asset.ext === 'mp4') {{
                stage.innerHTML = `<video controls class="max-h-[300px] rounded-lg"><source src="${{asset.path}}" type="video/mp4"></video>`;
            }} else {{
                const img = document.createElement('img');
                img.src = asset.path;
                img.id = 'modal-img';
                img.className = 'max-h-[260px] max-w-full object-contain';
                stage.appendChild(img);
            }}

            document.getElementById('asset-modal').classList.remove('hidden');
        }}

        function closeModal() {{
            document.getElementById('asset-modal').classList.add('hidden');
        }}

        function toggleModalAnimation() {{
            const img = document.getElementById('modal-img');
            const btn = document.getElementById('modal-pause-btn');
            if (!img) return;
            isModalPaused = !isModalPaused;
            if (isModalPaused) {{
                img.classList.add('paused');
                btn.innerText = '▶ Resume Animation';
            }} else {{
                img.classList.remove('paused');
                btn.innerText = '⏸ Pause Animation';
            }}
        }}

        function copyAssetMarkdown() {{
            if (!currentModalAsset) return;
            const text = `![${{currentModalAsset.name}}](${{currentModalAsset.path}})`;
            navigator.clipboard.writeText(text).then(() => {{
                const btn = document.getElementById('modal-copy-link');
                const orig = btn.innerText;
                btn.innerText = '✓ Copied Markdown!';
                setTimeout(() => {{ btn.innerText = orig; }}, 2000);
            }});
        }}

        function copyColor(hex, el) {{
            navigator.clipboard.writeText(hex).then(() => {{
                const orig = el.querySelector('span:last-child').innerText;
                el.querySelector('span:last-child').innerText = '✓ Copied!';
                setTimeout(() => {{
                    el.querySelector('span:last-child').innerText = orig;
                }}, 1500);
            }});
        }}

        // Initialize UXR Viewer
        function initUxrViewer() {{
            const listContainer = document.getElementById('uxr-doc-list');
            listContainer.innerHTML = '';

            ALL_UXR_DOCS.forEach((doc, idx) => {{
                const item = document.createElement('button');
                item.className = 'w-full text-left px-3 py-2 rounded-xl text-xs font-semibold text-stone-700 hover:bg-stone-200/60 transition flex items-center justify-between cursor-pointer';
                item.innerHTML = `<span>${{doc.title}}</span><span class="text-[10px] text-stone-400">${{doc.category}}</span>`;
                item.onclick = () => loadUxrDoc(doc, item);
                listContainer.appendChild(item);

                if (idx === 0) loadUxrDoc(doc, item);
            }});
        }}

        function loadUxrDoc(doc, itemEl) {{
            document.querySelectorAll('#uxr-doc-list button').forEach(b => b.classList.remove('bg-orange-100', 'text-orange-800'));
            if (itemEl) itemEl.classList.add('bg-orange-100', 'text-orange-800');

            document.getElementById('reader-title').innerText = doc.title;
            document.getElementById('reader-category').innerText = doc.category;
            document.getElementById('reader-path').innerText = doc.path;

            if (typeof marked !== 'undefined') {{
                document.getElementById('reader-body').innerHTML = marked.parse(doc.content);
            }} else {{
                document.getElementById('reader-body').innerText = doc.content;
            }}
        }}

        // Initialize on load
        document.addEventListener('DOMContentLoaded', () => {{
            filterAssets();
            initUxrViewer();
        }});
    </script>

</body>
</html>
"""

output_path = os.path.join(repo_root, 'index.html')
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"Generated {output_path} successfully ({os.path.getsize(output_path)} bytes).")
