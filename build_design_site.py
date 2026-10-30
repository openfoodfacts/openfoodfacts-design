#!/usr/bin/env python3
import os
import glob
import json
import re

repo_root = os.path.dirname(os.path.abspath(__file__))

# 1. Collect all assets
assets = []

# Language dictionary for multi-language assets (e.g. UN SDG Goals)
LANGUAGES = {
    'AR': {'name': 'Arabic', 'native': 'العربية', 'flag': '🇸🇦'},
    'CA': {'name': 'Catalan', 'native': 'Català', 'flag': '🇦🇩'},
    'DA': {'name': 'Danish', 'native': 'Dansk', 'flag': '🇩🇰'},
    'DE': {'name': 'German', 'native': 'Deutsch', 'flag': '🇩🇪'},
    'EL': {'name': 'Greek', 'native': 'Ελληνικά', 'flag': '🇬🇷'},
    'EN': {'name': 'English', 'native': 'English', 'flag': '🇬🇧'},
    'ES': {'name': 'Spanish', 'native': 'Español', 'flag': '🇪🇸'},
    'EU': {'name': 'Basque', 'native': 'Euskara', 'flag': '🇪🇸'},
    'FI': {'name': 'Finnish', 'native': 'Suomi', 'flag': '🇫🇮'},
    'FR': {'name': 'French', 'native': 'Français', 'flag': '🇫🇷'},
    'FY': {'name': 'Frisian', 'native': 'Frysk', 'flag': '🇳🇱'},
    'GA': {'name': 'Irish', 'native': 'Gaeilge', 'flag': '🇮🇪'},
    'GE': {'name': 'Georgian', 'native': 'ქართული', 'flag': '🇬🇪'},
    'HI': {'name': 'Hindi', 'native': 'हिन्दी', 'flag': '🇮🇳'},
    'HY': {'name': 'Armenian', 'native': 'Հայերեն', 'flag': '🇦🇲'},
    'IN': {'name': 'Indonesian', 'native': 'Bahasa Indonesia', 'flag': '🇮🇩'},
    'IS': {'name': 'Icelandic', 'native': 'Íslenska', 'flag': '🇮🇸'},
    'IT': {'name': 'Italian', 'native': 'Italiano', 'flag': '🇮🇹'},
    'JP': {'name': 'Japanese', 'native': '日本語', 'flag': '🇯🇵'},
    'NL': {'name': 'Dutch', 'native': 'Nederlands', 'flag': '🇳🇱'},
    'NO': {'name': 'Norwegian', 'native': 'Norsk', 'flag': '🇳🇴'},
    'PL': {'name': 'Polish', 'native': 'Polski', 'flag': '🇵🇱'},
    'PT': {'name': 'Portuguese', 'native': 'Português', 'flag': '🇵🇹'},
    'PT_BR': {'name': 'Portuguese (Brazil)', 'native': 'Português do Brasil', 'flag': '🇧🇷'},
    'RO': {'name': 'Romanian', 'native': 'Română', 'flag': '🇷🇴'},
    'RU': {'name': 'Russian', 'native': 'Русский', 'flag': '🇷🇺'},
    'SE': {'name': 'Swedish', 'native': 'Svenska', 'flag': '🇸🇪'},
    'SW': {'name': 'Swahili', 'native': 'Kiswahili', 'flag': '🇰🇪'},
    'ZH': {'name': 'Chinese', 'native': '中文', 'flag': '🇨🇳'},
}

categories = {
    'animated': {'name': '✨ Animated SVGs', 'count': 0},
    'food': {'name': '🥗 Food Illustrations', 'count': 0},
    'shared': {'name': '🤝 Shared Illustrations', 'count': 0},
    'logos': {'name': '🏷️ Brand Logos', 'count': 0},
    'nutriscore': {'name': '🚦 Nutri-Score', 'count': 0},
    'greenscore': {'name': '🌱 Green-Score', 'count': 0},
    'sdg': {'name': '🌐 UN SDG Goals', 'count': 0},
    'prices': {'name': '💰 Open Prices', 'count': 0},
    'products': {'name': '📦 Products', 'count': 0},
    'beauty': {'name': '🧴 Beauty', 'count': 0},
    'petfood': {'name': '🐾 Pet Food', 'count': 0},
    'avatars': {'name': '👤 Avatars', 'count': 0},
    'animations': {'name': '🎬 Motion & Videos', 'count': 0},
}

# Track indexed animations to avoid redundant duplicate cards between animations/ and animations/videos/
indexed_anim_basenames = set()

for root, dirs, files in os.walk(repo_root):
    if '.git' in root or 'node_modules' in root or 'scratch' in root or 'brain' in root:
        continue
    for f in sorted(files):
        ext = os.path.splitext(f)[1].lower()
        if ext in ['.svg', '.png', '.jpg', '.jpeg', '.gif', '.mp4', '.riv', '.webp']:
            full_path = os.path.join(root, f)
            rel_path = os.path.relpath(full_path, repo_root)
            size = os.path.getsize(full_path)
            
            # Avoid duplicate video cards if identical file already exists in animations/
            if 'animations/videos' in rel_path and ext == '.mp4':
                root_anim_path = os.path.join(repo_root, 'animations', f)
                if os.path.exists(root_anim_path):
                    continue

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
            if 'illustrations/food' in rel_path:
                cat = 'food'
            elif 'illustrations/shared' in rel_path:
                cat = 'shared'
            elif 'illustrations/prices' in rel_path or 'logos/openprices' in rel_path:
                cat = 'prices'
            elif 'illustrations/pet-food' in rel_path or 'logos/openpetfoodfacts' in rel_path or 'compare-graph-opff' in rel_path:
                cat = 'petfood'
            elif 'illustrations/beauty' in rel_path or 'logos/openbeautyfacts' in rel_path or 'compare-graph-obf' in rel_path:
                cat = 'beauty'
            elif 'illustrations/products' in rel_path or 'logos/openproductsfacts' in rel_path or 'compare-graph-opf' in rel_path:
                cat = 'products'
            elif 'animations' in rel_path or ext in ['.mp4', '.gif', '.riv']:
                cat = 'animations'
            elif 'un-sdg' in rel_path or 'logos/un-sdg-goals' in rel_path:
                cat = 'sdg'
            elif 'green-score' in rel_path or 'logos/green-score' in rel_path:
                cat = 'greenscore'
            elif 'nutriscore' in rel_path or 'nutri-score' in rel_path:
                cat = 'nutriscore'
            elif 'logos' in rel_path:
                cat = 'logos'
            elif 'avatars' in rel_path:
                cat = 'avatars'
            elif 'magnets' in rel_path:
                cat = 'shared'

            # Detect language for assets (e.g. UN SDG Goals multi-language files)
            lang_code = None
            lang_name = None
            lang_flag = None
            if cat == 'sdg' or 'un-sdg-goals' in rel_path:
                if f.startswith('PT_BR_'):
                    lang_code = 'PT_BR'
                else:
                    parts = f.split('_')
                    if len(parts) > 1 and len(parts[0]) == 2 and parts[0].isupper():
                        lang_code = parts[0]
                if lang_code in LANGUAGES:
                    lang_name = LANGUAGES[lang_code]['name']
                    lang_flag = LANGUAGES[lang_code]['flag']

            if is_animated:
                categories['animated']['count'] += 1
            if cat in categories:
                categories[cat]['count'] += 1

            # Check for alternate format counterpart (PNG for SVG, SVG for PNG)
            base_without_ext = os.path.splitext(full_path)[0]
            rel_base = os.path.splitext(rel_path)[0]
            has_png = os.path.exists(base_without_ext + '.png')
            has_svg = os.path.exists(base_without_ext + '.svg')

            assets.append({
                'name': f,
                'path': rel_path,
                'size': size,
                'category': cat,
                'animated': is_animated,
                'ext': ext.replace('.', ''),
                'png_path': (rel_base + '.png') if has_png else None,
                'svg_path': (rel_base + '.svg') if has_svg else None,
                'lang': lang_code,
                'lang_name': lang_name,
                'lang_flag': lang_flag
            })

# Sort assets: animated first, then by category, then by name
assets.sort(key=lambda x: (not x['animated'], x['category'], x['name']))

# Compute language counts and generate options for the language selector
sdg_lang_counts = {}
for a in assets:
    if a.get('lang'):
        code = a['lang']
        sdg_lang_counts[code] = sdg_lang_counts.get(code, 0) + 1

lang_options_html = ['<option value="all">🌐 All Languages (All)</option>']
for code, count in sorted(sdg_lang_counts.items(), key=lambda x: LANGUAGES.get(x[0], {}).get('name', '')):
    info = LANGUAGES[code]
    flag = info['flag']
    name = info['name']
    lang_options_html.append(f'<option value="{code}">{flag} {name} - {code} ({count})</option>')
lang_options_str = '\n                    '.join(lang_options_html)

top_lang_codes = ['EN', 'FR', 'ES', 'DE', 'AR', 'ZH', 'IT', 'RU', 'NL', 'PT_BR', 'HI', 'JP']
quick_pills_html = [
    '<button onclick="setLanguageFilter(\'all\', this)" class="sdg-lang-pill active px-2.5 py-1 rounded-lg text-xs font-bold bg-orange-600 text-white transition cursor-pointer">All</button>'
]
for code in top_lang_codes:
    if code in sdg_lang_counts:
        info = LANGUAGES[code]
        count = sdg_lang_counts[code]
        flag = info['flag']
        name = info['name']
        native = info['native']
        quick_pills_html.append(
            f'<button onclick="setLanguageFilter(\'{code}\', this)" class="sdg-lang-pill px-2.5 py-1 rounded-lg text-xs font-semibold bg-stone-100 text-stone-700 hover:bg-stone-200 transition cursor-pointer" title="{name} ({native})">{flag} {code} ({count})</button>'
        )
quick_pills_str = '\n        '.join(quick_pills_html)

# 2. Collect all documentation pages (including root docs like README, DESIGN, CONTRIBUTING, RESSOURCES)
docs = []
for root, dirs, files in os.walk(repo_root):
    if '.git' in root or 'node_modules' in root or 'scratch' in root or 'brain' in root:
        continue
    for f in sorted(files):
        if f.endswith('.md'):
            full_path = os.path.join(root, f)
            rel_path = os.path.relpath(full_path, repo_root)
            with open(full_path, 'r', encoding='utf-8', errors='ignore') as fp:
                content = fp.read()

            cat = 'Core Documentation'
            clean_title = f.replace('.md', '').replace('_', ' ')
            is_design = False

            if rel_path in ['README.md', 'CONTRIBUTING.md', 'RESSOURCES.md', 'DESIGN.md', 'ACTING-ON-THE-CODE.md', 'CHANGELOG.md']:
                cat = 'Core Documentation'
                if rel_path == 'README.md':
                    clean_title = 'README — Design Overview & Plan'
                elif rel_path == 'DESIGN.md':
                    clean_title = 'DESIGN.md — Stitch Design Tokens Spec'
                    is_design = True
                elif rel_path == 'CONTRIBUTING.md':
                    clean_title = 'CONTRIBUTING — Onboarding & Guidelines'
                elif rel_path == 'RESSOURCES.md':
                    clean_title = 'RESSOURCES — UI Library & Foundations'
                elif rel_path == 'ACTING-ON-THE-CODE.md':
                    clean_title = 'ACTING ON THE CODE — Repos & Frontends'
                elif rel_path == 'CHANGELOG.md':
                    clean_title = 'CHANGELOG — Release Notes & History'
            elif 'graphic-charter' in rel_path:
                cat = 'Brand Charter'
                clean_title = 'Brand Guidelines Overview'
            elif 'UXR Ops' in rel_path:
                cat = 'UXR Operations'
            elif 'UXR Open Prices' in rel_path:
                cat = 'Open Prices UXR'
            elif 'UXR Reports' in rel_path:
                cat = 'Research Reports'
            elif 'UXR OFF' in rel_path:
                cat = 'UX Research'
            elif any(k in rel_path for k in ['avatars', 'designs', 'animations', 'illustrations', 'nutriscore']):
                cat = 'Asset & Tool Guides'
                if 'avatars' in rel_path:
                    clean_title = 'Avatar System & Inkscape Guide'
                elif 'magnets' in rel_path:
                    clean_title = 'Fridge Magnets Guidelines'
                elif 'scan-nutriscore' in rel_path:
                    clean_title = 'Rive Scan Animation Specs'
                elif 'animations/videos' in rel_path:
                    clean_title = 'Motion Showcase Videos'
                elif 'shared/README' in rel_path:
                    clean_title = 'Shared Illustrations Guide'
                elif 'prices/README' in rel_path:
                    clean_title = 'Open Prices Illustrations Guide'
                elif 'nutriscore/README' in rel_path:
                    clean_title = 'Nutri-Score Assets Guidelines'
                elif 'designs/README' in rel_path:
                    clean_title = 'Finished Designs Repository'

            docs.append({
                'title': clean_title,
                'path': rel_path,
                'category': cat,
                'content': content,
                'is_design_spec': is_design
            })

# Sort documentation: Core Docs first (README, DESIGN, CONTRIBUTING, RESSOURCES, ACTING, CHANGELOG),
# followed by Brand Charter, UXR docs, and Asset Guides.
def doc_sort_key(d):
    cat_order = {
        'Core Documentation': 0,
        'Brand Charter': 1,
        'UX Research': 2,
        'UXR Operations': 3,
        'Open Prices UXR': 4,
        'Research Reports': 5,
        'Asset & Tool Guides': 6
    }
    c_idx = cat_order.get(d['category'], 99)
    # Title order within Core Documentation
    t_order = {
        'README — Design Overview & Plan': 0,
        'DESIGN.md — Stitch Design Tokens Spec': 1,
        'CONTRIBUTING — Onboarding & Guidelines': 2,
        'RESSOURCES — UI Library & Foundations': 3,
        'ACTING ON THE CODE — Repos & Frontends': 4,
        'CHANGELOG — Release Notes & History': 5
    }
    t_idx = t_order.get(d['title'], 50)
    return (c_idx, t_idx, d['title'])

docs.sort(key=doc_sort_key)

print(f"Collected {len(assets)} assets and {len(docs)} documentation guides.")

# 3. Generate index.html
assets_json = json.dumps(assets)
docs_json = json.dumps(docs)
categories_json = json.dumps(categories)

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Open Food Facts — Design System &amp; Asset Hub</title>
    <!-- Tailwind CSS with Typography Plugin -->
    <script>
        // Suppress Tailwind Play CDN advisory warning in console
        (function() {{
            const origWarn = console.warn;
            console.warn = function(...args) {{
                if (args[0] && typeof args[0] === 'string' && args[0].includes('cdn.tailwindcss.com should not be used in production')) return;
                origWarn.apply(console, args);
            }};
        }})();
    </script>
    <script src="https://cdn.tailwindcss.com?plugins=typography"></script>
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
            background: rgba(255, 255, 255, 0.94);
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
        /* Markdown reader table & code enhancements */
        #reader-body table {{
            width: 100%;
            border-collapse: collapse;
            margin: 1.25rem 0;
            font-size: 0.875rem;
        }}
        #reader-body th {{
            background-color: #f8fafc;
            border: 1px solid #e2e8f0;
            padding: 0.625rem 0.875rem;
            text-align: left;
            font-weight: 700;
            color: #1e293b;
        }}
        #reader-body td {{
            border: 1px solid #e2e8f0;
            padding: 0.5rem 0.875rem;
            color: #334155;
        }}
        #reader-body tr:nth-child(even) td {{
            background-color: #fbfcfe;
        }}
        #reader-body blockquote {{
            border-left: 4px solid #ea580c;
            background-color: #fffaf5;
            padding: 0.75rem 1.25rem;
            margin: 1rem 0;
            border-radius: 0 0.75rem 0.75rem 0;
            color: #7c2d12;
            font-style: normal;
        }}
        #reader-body pre {{
            background-color: #1e293b;
            color: #f8fafc;
            padding: 1rem;
            border-radius: 0.875rem;
            overflow-x: auto;
            margin: 1rem 0;
        }}
        #reader-body code:not(pre code) {{
            background-color: #f1f5f9;
            color: #c2410c;
            padding: 0.15rem 0.4rem;
            border-radius: 0.375rem;
            font-size: 0.85em;
            font-weight: 600;
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
                <div class="flex items-center gap-3 cursor-pointer" onclick="switchTab('catalog')">
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
                    <button onclick="switchTab('docs')" id="nav-docs" class="nav-link px-3.5 py-2 rounded-xl text-xs font-semibold text-stone-600 hover:text-stone-900 hover:bg-stone-100 transition cursor-pointer">
                        📚 Documentation &amp; Research
                    </button>
                    <button onclick="switchTab('hand')" id="nav-hand" class="nav-link px-3.5 py-2 rounded-xl text-xs font-semibold text-stone-600 hover:text-stone-900 hover:bg-stone-100 transition cursor-pointer">
                        📱 Hand Mockup Generator
                    </button>
                    <button onclick="switchTab('avatar')" id="nav-avatar" class="nav-link px-3.5 py-2 rounded-xl text-xs font-semibold text-stone-600 hover:text-stone-900 hover:bg-stone-100 transition cursor-pointer">
                        👤 Avatar Creator
                    </button>
                    <button onclick="switchTab('motion')" id="nav-motion" class="nav-link px-3.5 py-2 rounded-xl text-xs font-semibold text-stone-600 hover:text-stone-900 hover:bg-stone-100 transition cursor-pointer">
                        🎬 Motion &amp; Videos
                    </button>
                </nav>

                <!-- Mobile Menu Button -->
                <div class="md:hidden flex items-center">
                    <select id="mobile-nav-select" onchange="switchTab(this.value)" class="text-xs font-bold bg-white border border-stone-300 rounded-lg px-2.5 py-1.5 text-stone-800">
                        <option value="catalog">🖼️ Assets Catalog</option>
                        <option value="charter">🎨 Graphic Charter</option>
                        <option value="docs">📚 Documentation &amp; Research</option>
                        <option value="hand">📱 Hand Generator</option>
                        <option value="avatar">👤 Avatar Creator</option>
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
                        Discover 650+ production-grade illustrations, animated SVGs, logos, Nutri-Scores, and iconography for web, mobile apps, and community campaigns.
                    </p>
                </div>
                <div class="flex flex-wrap items-center gap-2">
                    <div class="bg-white/90 backdrop-blur rounded-2xl p-4 border border-orange-200 shadow-xs text-center min-w-[110px]">
                        <span class="block text-2xl font-black text-orange-600">{len(assets)}</span>
                        <span class="text-xs font-bold text-stone-500 uppercase">Total Assets</span>
                    </div>
                    <div class="bg-white/90 backdrop-blur rounded-2xl p-4 border border-orange-200 shadow-xs text-center min-w-[110px]">
                        <span class="block text-2xl font-black text-emerald-600">{categories['animated']['count']}</span>
                        <span class="text-xs font-bold text-stone-500 uppercase">Animated SVGs</span>
                    </div>
                    <div class="bg-white/90 backdrop-blur rounded-2xl p-4 border border-orange-200 shadow-xs text-center min-w-[110px]">
                        <span class="block text-2xl font-black text-sky-600">{len(sdg_lang_counts)}</span>
                        <span class="text-xs font-bold text-stone-500 uppercase">SDG Languages</span>
                    </div>
                </div>
            </div>

            <!-- Search & Filter Controls -->
            <div class="bg-white rounded-2xl border border-stone-200 p-4 shadow-xs space-y-3">
                <div class="flex flex-wrap items-center justify-between gap-3">
                    <div class="flex flex-wrap items-center gap-3 flex-grow">
                        <div class="relative flex-grow min-w-[220px] max-w-md">
                            <input type="text" id="asset-search" placeholder="Search {len(assets)} assets by name, category, language, or path..." oninput="filterAssets()" class="w-full pl-10 pr-9 py-2.5 text-sm bg-stone-50 border border-stone-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-orange-500/30 focus:border-orange-500 transition">
                            <svg class="w-4 h-4 text-stone-400 absolute left-3.5 top-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>
                            <button id="clear-search-btn" onclick="clearSearch()" class="hidden absolute right-3 top-3 text-stone-400 hover:text-stone-700 text-sm font-bold">&times;</button>
                        </div>

                        <!-- Language Filter Select -->
                        <div class="flex items-center gap-1.5 transition" id="language-filter-wrapper">
                            <label for="language-filter" class="text-xs font-bold text-stone-500 whitespace-nowrap flex items-center gap-1">
                                🌐 <span class="hidden sm:inline">Language:</span>
                            </label>
                            <select id="language-filter" onchange="setLanguageFilter(this.value)" class="text-xs font-semibold bg-stone-50 hover:bg-stone-100 border border-stone-200 rounded-xl px-3 py-2 text-stone-700 focus:outline-none focus:ring-2 focus:ring-orange-500/30 focus:border-orange-500 transition cursor-pointer">
                                {lang_options_str}
                            </select>
                        </div>
                    </div>

                    <div class="flex items-center gap-2 text-xs font-medium text-stone-500">
                        <span id="results-count" class="font-bold text-stone-800">Showing {len(assets)} assets</span>
                        <button id="quick-show-all-btn" onclick="loadMoreAssets('all')" class="hidden px-2.5 py-1 rounded-lg bg-orange-100 hover:bg-orange-200 text-orange-800 font-bold transition cursor-pointer">
                            Show All
                        </button>
                    </div>
                </div>

                <!-- Quick Language Pills for SDG -->
                <div id="sdg-lang-quickpills" class="flex flex-wrap items-center gap-1.5 pt-2 border-t border-stone-100 text-xs">
                    <span class="font-bold text-stone-500 text-[11px] mr-1 flex items-center gap-1">
                        🌐 SDG Quick Langs:
                    </span>
                    {quick_pills_str}
                </div>

                <!-- Category Filter Pills -->
                <div class="flex flex-wrap gap-1.5 pt-2 border-t border-stone-100" id="category-pills">
                    <button onclick="setCategoryFilter('all', this)" class="cat-pill active px-3 py-1.5 rounded-lg text-xs font-semibold bg-orange-600 text-white transition cursor-pointer">
                        All ({len(assets)})
                    </button>
                    <button onclick="setCategoryFilter('animated', this)" class="cat-pill px-3 py-1.5 rounded-lg text-xs font-semibold bg-stone-100 text-stone-600 hover:bg-stone-200 transition cursor-pointer">
                        ✨ Animated SVGs ({categories['animated']['count']})
                    </button>
                    <button onclick="setCategoryFilter('food', this)" class="cat-pill px-3 py-1.5 rounded-lg text-xs font-semibold bg-stone-100 text-stone-600 hover:bg-stone-200 transition cursor-pointer">
                        🥗 Food Illustrations ({categories['food']['count']})
                    </button>
                    <button onclick="setCategoryFilter('shared', this)" class="cat-pill px-3 py-1.5 rounded-lg text-xs font-semibold bg-stone-100 text-stone-600 hover:bg-stone-200 transition cursor-pointer">
                        🤝 Community &amp; Shared ({categories['shared']['count']})
                    </button>
                    <button onclick="setCategoryFilter('logos', this)" class="cat-pill px-3 py-1.5 rounded-lg text-xs font-semibold bg-stone-100 text-stone-600 hover:bg-stone-200 transition cursor-pointer">
                        🏷️ Brand Logos ({categories['logos']['count']})
                    </button>
                    <button onclick="setCategoryFilter('nutriscore', this)" class="cat-pill px-3 py-1.5 rounded-lg text-xs font-semibold bg-stone-100 text-stone-600 hover:bg-stone-200 transition cursor-pointer">
                        🚦 Nutri-Score ({categories['nutriscore']['count']})
                    </button>
                    <button onclick="setCategoryFilter('greenscore', this)" class="cat-pill px-3 py-1.5 rounded-lg text-xs font-semibold bg-stone-100 text-stone-600 hover:bg-stone-200 transition cursor-pointer">
                        🌱 Green-Score ({categories['greenscore']['count']})
                    </button>
                    <button onclick="setCategoryFilter('sdg', this)" class="cat-pill px-3 py-1.5 rounded-lg text-xs font-semibold bg-stone-100 text-stone-600 hover:bg-stone-200 transition cursor-pointer">
                        🌐 UN SDG Goals ({categories['sdg']['count']})
                    </button>
                    <button onclick="setCategoryFilter('prices', this)" class="cat-pill px-3 py-1.5 rounded-lg text-xs font-semibold bg-stone-100 text-stone-600 hover:bg-stone-200 transition cursor-pointer">
                        💰 Open Prices ({categories['prices']['count']})
                    </button>
                    <button onclick="setCategoryFilter('products', this)" class="cat-pill px-3 py-1.5 rounded-lg text-xs font-semibold bg-stone-100 text-stone-600 hover:bg-stone-200 transition cursor-pointer">
                        📦 Products ({categories['products']['count']})
                    </button>
                    <button onclick="setCategoryFilter('beauty', this)" class="cat-pill px-3 py-1.5 rounded-lg text-xs font-semibold bg-stone-100 text-stone-600 hover:bg-stone-200 transition cursor-pointer">
                        🧴 Beauty ({categories['beauty']['count']})
                    </button>
                    <button onclick="setCategoryFilter('petfood', this)" class="cat-pill px-3 py-1.5 rounded-lg text-xs font-semibold bg-stone-100 text-stone-600 hover:bg-stone-200 transition cursor-pointer">
                        🐾 Pet Food ({categories['petfood']['count']})
                    </button>
                    <button onclick="setCategoryFilter('avatars', this)" class="cat-pill px-3 py-1.5 rounded-lg text-xs font-semibold bg-stone-100 text-stone-600 hover:bg-stone-200 transition cursor-pointer">
                        👤 Avatars ({categories['avatars']['count']})
                    </button>
                    <button onclick="setCategoryFilter('animations', this)" class="cat-pill px-3 py-1.5 rounded-lg text-xs font-semibold bg-stone-100 text-stone-600 hover:bg-stone-200 transition cursor-pointer">
                        🎬 Videos &amp; Motion ({categories['animations']['count']})
                    </button>
                </div>
            </div>

            <!-- Asset Cards Grid -->
            <div id="assets-grid" class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-4">
                <!-- Dynamically rendered via JS -->
            </div>

            <!-- Infinite Scroll Sentinel & Pagination Controls -->
            <div id="pagination-controls" class="py-8 flex flex-col items-center justify-center gap-3">
                <div class="flex flex-wrap items-center justify-center gap-3">
                    <button id="load-more-btn" onclick="loadMoreAssets(60)" class="px-6 py-2.5 rounded-xl text-sm font-bold bg-white border border-stone-300 hover:bg-stone-100 text-stone-700 shadow-xs transition flex items-center gap-2 cursor-pointer">
                        <span>⬇️ Load More Assets</span>
                    </button>
                    <button id="show-all-btn" onclick="loadMoreAssets('all')" class="px-6 py-2.5 rounded-xl text-sm font-bold bg-orange-600 hover:bg-orange-700 text-white shadow-xs transition flex items-center gap-2 cursor-pointer">
                        <span>⚡ Show All Assets</span>
                    </button>
                </div>
                <p id="pagination-status" class="text-xs font-medium text-stone-500 text-center">
                    Scrolling down will automatically load more assets.
                </p>
                <!-- Sentinel element for IntersectionObserver -->
                <div id="scroll-sentinel" class="w-full h-8"></div>
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
        <!-- TAB 3: DOCUMENTATION & RESEARCH (EXPANDED TO ALL DOCS)          -->
        <!-- ============================================================== -->
        <section id="tab-docs" class="hidden space-y-6">
            <div class="bg-white rounded-3xl border border-stone-200 p-6 sm:p-10 shadow-xs">
                <div class="pb-6 border-b border-stone-200">
                    <div class="flex flex-wrap items-center justify-between gap-4">
                        <div>
                            <span class="text-xs font-bold text-indigo-600 tracking-wider uppercase block">Design Knowledge &amp; Research Base</span>
                            <h1 class="text-3xl font-black text-stone-900 tracking-tight mt-1">Documentation, Guidelines &amp; UXR</h1>
                            <p class="text-stone-500 text-sm mt-1">Official design system specifications, onboarding guides, Google Stitch tokens, and UX research findings.</p>
                        </div>
                        <div class="flex items-center gap-2">
                            <a id="doc-github-link" href="https://github.com/openfoodfacts/openfoodfacts-design" target="_blank" class="px-4 py-2 rounded-xl text-xs font-bold bg-stone-100 hover:bg-stone-200 text-stone-700 transition flex items-center gap-1.5 cursor-pointer">
                                <svg class="w-4 h-4 fill-current" viewBox="0 0 24 24"><path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0 0 24 12c0-6.63-5.37-12-12-12z"/></svg>
                                <span>View on GitHub</span>
                            </a>
                        </div>
                    </div>
                </div>

                <!-- Two-Column Documentation Explorer -->
                <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 mt-6">
                    <!-- Left: Navigation Tree with Search -->
                    <div class="lg:col-span-4 space-y-4">
                        <div class="bg-stone-50 rounded-2xl p-4 border border-stone-200 space-y-3">
                            <div class="relative">
                                <input type="text" id="doc-search" placeholder="Filter documentation..." oninput="filterDocs()" class="w-full pl-9 pr-3 py-2 text-xs bg-white border border-stone-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500/30 focus:border-indigo-500 transition">
                                <svg class="w-3.5 h-3.5 text-stone-400 absolute left-3 top-2.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>
                            </div>
                            
                            <div id="doc-list-container" class="space-y-4 max-h-[680px] overflow-y-auto pr-1">
                                <!-- Populated dynamically by categories -->
                            </div>
                        </div>
                    </div>

                    <!-- Right: Formatted Markdown Reader -->
                    <div class="lg:col-span-8 bg-stone-50/50 rounded-2xl p-6 sm:p-8 border border-stone-200 min-h-[600px] flex flex-col">
                        <div class="flex flex-wrap items-center justify-between gap-3 pb-4 border-b border-stone-200 mb-6">
                            <div>
                                <span id="reader-category" class="text-xs font-bold text-orange-600 uppercase tracking-wide">Category</span>
                                <h2 id="reader-title" class="text-xl font-black text-stone-900 mt-0.5">Select a document</h2>
                            </div>
                            <div class="flex items-center gap-2">
                                <span id="reader-path" class="text-xs font-mono text-stone-400 bg-stone-100 px-2.5 py-1 rounded-md">path</span>
                                <button onclick="copyDocPath()" class="text-xs font-bold text-stone-500 hover:text-stone-800 transition cursor-pointer" title="Copy relative file path">
                                    📋
                                </button>
                            </div>
                        </div>

                        <!-- Special Alert for DESIGN.md -->
                        <div id="design-experiment-banner" class="hidden mb-6 p-4 rounded-2xl bg-amber-50 border border-amber-200/90 text-amber-900 shadow-xs">
                            <div class="flex items-start gap-3">
                                <span class="text-2xl select-none">🧪</span>
                                <div>
                                    <h4 class="font-bold text-sm text-amber-900">Experimental LLM Design System Document (Google Stitch)</h4>
                                    <p class="text-xs text-amber-800/90 mt-1 leading-relaxed">
                                        <code>DESIGN.md</code> follows the Google Stitch specification as an experiment to help Large Language Models (LLMs) and autonomous AI coding agents respect the Open Food Facts graphic charter, design tokens, and components when creating or updating UI.
                                    </p>
                                    <p class="text-xs text-amber-800/90 mt-1 font-semibold">
                                        ⚠️ Please note: Because this is an evolving experiment, it might contain mistakes, omissions, or slight discrepancies with live production code. Always verify critical visual identity decisions against the official <a href="javascript:switchTab('charter')" class="underline hover:text-amber-950">Brand Charter</a> and live repositories.
                                    </p>
                                </div>
                            </div>
                        </div>

                        <!-- Rendered Content Body -->
                        <div id="reader-body" class="prose prose-stone max-w-none text-sm leading-relaxed flex-grow">
                            <p class="text-stone-500 italic">Select any document from the list on the left to read its full content.</p>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- ============================================================== -->
        <!-- TAB 4: HAND SCREENSHOT GENERATOR TOOL                          -->
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
        <!-- TAB 5: AVATAR CREATOR (FIXED & POLISHED)                       -->
        <!-- ============================================================== -->
        <section id="tab-avatar" class="hidden space-y-6">
            <div class="bg-white rounded-3xl border border-stone-200 p-6 sm:p-10 shadow-xs">
                <div class="flex flex-wrap items-center justify-between gap-4 pb-6 border-b border-stone-200">
                    <div>
                        <span class="text-xs font-bold text-orange-600 tracking-wider uppercase block">Community Profiles &bull; Modular SVG System</span>
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
        <!-- TAB 6: MOTION & ANIMATIONS                                     -->
        <!-- ============================================================== -->
        <section id="tab-motion" class="hidden space-y-6">
            <div class="bg-white rounded-3xl border border-stone-200 p-6 sm:p-10 shadow-xs">
                <div class="pb-6 border-b border-stone-200">
                    <span class="text-xs font-bold text-rose-600 tracking-wider uppercase block">Motion Graphics</span>
                    <h1 class="text-3xl font-black text-stone-900 tracking-tight mt-1">Animations, Rive &amp; Video Assets</h1>
                    <p class="text-stone-500 text-sm mt-1">Interactive vector animations, Nutri-Score &amp; Green-Score scans, and brand showcase videos.</p>
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
                    <div class="flex items-center gap-2 mt-0.5">
                        <p id="modal-path" class="text-xs font-mono text-stone-400">path/to/asset.svg</p>
                        <span id="modal-lang-badge" class="hidden px-2 py-0.5 rounded text-[10px] font-bold bg-stone-100 text-stone-700 border border-stone-200"></span>
                    </div>
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
                    <button id="modal-copy-path" onclick="copyAssetPath()" class="px-3.5 py-2 rounded-xl text-xs font-bold bg-white border border-stone-200 hover:bg-stone-50 text-stone-700 transition cursor-pointer">
                        📋 Copy Path
                    </button>
                    <button id="modal-copy-link" onclick="copyAssetMarkdown()" class="px-3.5 py-2 rounded-xl text-xs font-bold bg-white border border-stone-200 hover:bg-stone-50 text-stone-700 transition cursor-pointer">
                        📋 Copy Markdown
                    </button>
                    <a id="modal-alt-download" href="#" download class="hidden px-4 py-2 rounded-xl text-xs font-bold bg-stone-100 hover:bg-stone-200 text-stone-700 shadow-xs transition cursor-pointer">
                        📥 Download PNG
                    </a>
                    <a id="modal-download" href="#" download class="px-4 py-2 rounded-xl text-xs font-bold bg-orange-600 hover:bg-orange-700 text-white shadow-xs transition cursor-pointer">
                        📥 Download Asset
                    </a>
                </div>
            </div>
        </div>
    </div>

    <!-- Data Injection & Runtime Logic -->
    <script>
        const ALL_ASSETS = {assets_json};
        const ALL_DOCS = {docs_json};

        let currentCategory = 'all';
        let currentLanguage = 'all';
        let currentModalAsset = null;
        let isModalPaused = false;
        let displayedCount = 60;
        const PAGE_SIZE = 60;
        let activeFilteredAssets = [];
        let scrollObserver = null;

        function switchTab(tabId) {{
            // Support legacy 'uxr' tab ID
            if (tabId === 'uxr') tabId = 'docs';

            const tabs = ['catalog', 'charter', 'docs', 'hand', 'avatar', 'motion'];
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

            const mobileSelect = document.getElementById('mobile-nav-select');
            if (mobileSelect) mobileSelect.value = tabId;

            window.scrollTo({{ top: 0, behavior: 'smooth' }});
        }}

        function setCategoryFilter(cat, btnEl) {{
            currentCategory = cat;
            document.querySelectorAll('#category-pills button').forEach(b => {{
                b.className = 'cat-pill px-3 py-1.5 rounded-lg text-xs font-semibold bg-stone-100 text-stone-600 hover:bg-stone-200 transition cursor-pointer';
            }});
            if (btnEl) {{
                btnEl.className = 'cat-pill active px-3 py-1.5 rounded-lg text-xs font-semibold bg-orange-600 text-white transition cursor-pointer';
            }}

            // If switching away from all or sdg to a category with no languages, reset language filter
            if (cat !== 'all' && cat !== 'sdg' && currentLanguage !== 'all') {{
                currentLanguage = 'all';
                const langSelect = document.getElementById('language-filter');
                if (langSelect) langSelect.value = 'all';
                document.querySelectorAll('#sdg-lang-quickpills button').forEach(b => {{
                    b.className = 'sdg-lang-pill px-2.5 py-1 rounded-lg text-xs font-semibold bg-stone-100 text-stone-700 hover:bg-stone-200 transition cursor-pointer';
                }});
                const allLangBtn = document.querySelector('#sdg-lang-quickpills button');
                if (allLangBtn) allLangBtn.className = 'sdg-lang-pill active px-2.5 py-1 rounded-lg text-xs font-bold bg-orange-600 text-white transition cursor-pointer';
            }}

            // Toggle SDG quick language pills visibility
            const sdgQuickPills = document.getElementById('sdg-lang-quickpills');
            const langWrapper = document.getElementById('language-filter-wrapper');
            if (sdgQuickPills) {{
                if (cat === 'sdg') {{
                    sdgQuickPills.classList.remove('hidden');
                    if (langWrapper) langWrapper.classList.add('ring-2', 'ring-orange-500/40', 'rounded-xl');
                }} else if (cat === 'all') {{
                    sdgQuickPills.classList.remove('hidden');
                    if (langWrapper) langWrapper.classList.remove('ring-2', 'ring-orange-500/40', 'rounded-xl');
                }} else {{
                    sdgQuickPills.classList.add('hidden');
                    if (langWrapper) langWrapper.classList.remove('ring-2', 'ring-orange-500/40', 'rounded-xl');
                }}
            }}

            displayedCount = PAGE_SIZE;
            filterAssets();
        }}

        function setLanguageFilter(lang, btnEl) {{
            currentLanguage = lang;

            // If a specific language is chosen and current category has no multi-language assets, auto-switch category to sdg
            if (lang !== 'all' && currentCategory !== 'all' && currentCategory !== 'sdg') {{
                currentCategory = 'sdg';
                document.querySelectorAll('#category-pills button').forEach(b => {{
                    const onclickAttr = b.getAttribute('onclick') || '';
                    if (onclickAttr.includes("'sdg'")) {{
                        b.className = 'cat-pill active px-3 py-1.5 rounded-lg text-xs font-semibold bg-orange-600 text-white transition cursor-pointer';
                    }} else {{
                        b.className = 'cat-pill px-3 py-1.5 rounded-lg text-xs font-semibold bg-stone-100 text-stone-600 hover:bg-stone-200 transition cursor-pointer';
                    }}
                }});
            }}

            // Sync select dropdown
            const langSelect = document.getElementById('language-filter');
            if (langSelect && langSelect.value !== lang) {{
                langSelect.value = lang;
            }}

            // Sync quick pills
            document.querySelectorAll('#sdg-lang-quickpills button').forEach(b => {{
                b.className = 'sdg-lang-pill px-2.5 py-1 rounded-lg text-xs font-semibold bg-stone-100 text-stone-700 hover:bg-stone-200 transition cursor-pointer';
            }});
            if (btnEl) {{
                btnEl.className = 'sdg-lang-pill active px-2.5 py-1 rounded-lg text-xs font-bold bg-orange-600 text-white transition cursor-pointer';
            }} else {{
                document.querySelectorAll('#sdg-lang-quickpills button').forEach(b => {{
                    const onclickAttr = b.getAttribute('onclick') || '';
                    if (onclickAttr.includes(`'${{lang}}'`)) {{
                        b.className = 'sdg-lang-pill active px-2.5 py-1 rounded-lg text-xs font-bold bg-orange-600 text-white transition cursor-pointer';
                    }}
                }});
            }}

            displayedCount = PAGE_SIZE;
            filterAssets();
        }}

        function clearSearch() {{
            const input = document.getElementById('asset-search');
            input.value = '';
            document.getElementById('clear-search-btn').classList.add('hidden');
            displayedCount = PAGE_SIZE;
            filterAssets();
        }}

        function filterAssets() {{
            const query = (document.getElementById('asset-search').value || '').toLowerCase().trim();
            const clearBtn = document.getElementById('clear-search-btn');
            if (query) {{
                clearBtn.classList.remove('hidden');
            }} else {{
                clearBtn.classList.add('hidden');
            }}

            activeFilteredAssets = ALL_ASSETS.filter(a => {{
                const matchesCat = currentCategory === 'all' 
                    || a.category === currentCategory 
                    || (currentCategory === 'animated' && a.animated);

                const matchesLang = currentLanguage === 'all'
                    || (a.lang && a.lang.toLowerCase() === currentLanguage.toLowerCase());

                const matchesQuery = !query 
                    || a.name.toLowerCase().includes(query) 
                    || a.path.toLowerCase().includes(query)
                    || a.category.toLowerCase().includes(query)
                    || (a.lang && a.lang.toLowerCase().includes(query))
                    || (a.lang_name && a.lang_name.toLowerCase().includes(query));

                return matchesCat && matchesLang && matchesQuery;
            }});

            renderAssetGrid(true);
        }}

        function renderAssetGrid(reset = false) {{
            const grid = document.getElementById('assets-grid');
            if (reset) {{
                grid.innerHTML = '';
            }}

            const startIdx = reset ? 0 : grid.children.length;
            const endIdx = Math.min(displayedCount, activeFilteredAssets.length);
            const sliceToRender = activeFilteredAssets.slice(startIdx, endIdx);

            sliceToRender.forEach(asset => {{
                const card = document.createElement('div');
                card.className = 'bg-white rounded-2xl border border-stone-200/80 p-3 shadow-xs hover:shadow-md hover:border-orange-400 transition flex flex-col group cursor-pointer';
                card.onclick = () => openModal(asset);

                // Preview wrapper
                const preview = document.createElement('div');
                preview.className = 'w-full aspect-square bg-stone-50 rounded-xl flex items-center justify-center p-3 mb-2.5 overflow-hidden relative';

                if (asset.ext === 'mp4') {{
                    preview.innerHTML = '<span class="text-3xl select-none">🎬</span>';
                }} else if (asset.ext === 'riv') {{
                    preview.innerHTML = '<div class="text-center"><span class="text-3xl select-none">📐</span><span class="block text-[10px] font-bold text-rose-600 mt-1 uppercase">Rive</span></div>';
                }} else {{
                    const img = document.createElement('img');
                    img.src = asset.path;
                    img.alt = asset.name;
                    img.loading = 'lazy';
                    img.className = 'max-w-full max-h-full object-contain group-hover:scale-105 transition';
                    img.onerror = () => {{
                        preview.innerHTML = '<span class="text-xs font-bold text-stone-400">Preview</span>';
                    }};
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
                sizeSpan.className = 'text-[10px] text-stone-400 uppercase mt-0.5 flex items-center justify-between';
                let langBadge = '';
                if (asset.lang) {{
                    langBadge = `<span class="px-1.5 py-0.5 rounded text-[9px] font-bold bg-stone-100 text-stone-600 border border-stone-200" title="${{asset.lang_name || asset.lang}}">${{asset.lang_flag || '🌐'}} ${{asset.lang}}</span>`;
                }}
                sizeSpan.innerHTML = `<span>${{asset.ext.toUpperCase()}} &bull; ${{Math.round(asset.size / 1024)}} KB</span>${{langBadge}}`;
                card.appendChild(sizeSpan);

                grid.appendChild(card);
            }});

            // Update status & pagination UI
            const resultsCountEl = document.getElementById('results-count');
            const quickShowAllBtn = document.getElementById('quick-show-all-btn');
            const loadMoreBtn = document.getElementById('load-more-btn');
            const showAllBtn = document.getElementById('show-all-btn');
            const paginationStatus = document.getElementById('pagination-status');

            const total = activeFilteredAssets.length;
            const shown = Math.min(displayedCount, total);

            resultsCountEl.innerText = `Showing ${{shown}} of ${{total}} assets ${{total === ALL_ASSETS.length ? '(All Assets)' : ''}}`;

            if (shown < total) {{
                quickShowAllBtn.classList.remove('hidden');
                loadMoreBtn.classList.remove('hidden');
                showAllBtn.classList.remove('hidden');
                const remaining = total - shown;
                loadMoreBtn.querySelector('span').innerText = `⬇️ Load More (${{Math.min(PAGE_SIZE, remaining)}} more)`;
                showAllBtn.querySelector('span').innerText = `⚡ Show All (${{total}} assets)`;
                paginationStatus.innerText = `${{remaining}} more assets available. Scroll down or click below to load.`;
            }} else {{
                quickShowAllBtn.classList.add('hidden');
                loadMoreBtn.classList.add('hidden');
                showAllBtn.classList.add('hidden');
                paginationStatus.innerHTML = `✓ All ${{total}} assets displayed. <a href="javascript:window.scrollTo({{top:0, behavior:'smooth'}})" class="text-orange-600 font-bold hover:underline">Back to top &uarr;</a>`;
            }}
        }}

        function loadMoreAssets(amount) {{
            if (amount === 'all') {{
                displayedCount = activeFilteredAssets.length;
            }} else {{
                displayedCount += (amount || PAGE_SIZE);
            }}
            renderAssetGrid(false);
        }}

        // Setup Infinite Scroll via IntersectionObserver
        function setupInfiniteScroll() {{
            const sentinel = document.getElementById('scroll-sentinel');
            if (!sentinel || !window.IntersectionObserver) return;

            if (scrollObserver) {{
                scrollObserver.disconnect();
            }}

            scrollObserver = new IntersectionObserver((entries) => {{
                entries.forEach(entry => {{
                    if (entry.isIntersecting) {{
                        if (displayedCount < activeFilteredAssets.length) {{
                            loadMoreAssets(PAGE_SIZE);
                        }}
                    }}
                }});
            }}, {{ rootMargin: '400px' }});

            scrollObserver.observe(sentinel);
        }}

        function openModal(asset) {{
            currentModalAsset = asset;
            document.getElementById('modal-title').innerText = asset.name;
            document.getElementById('modal-path').innerText = asset.path;

            const langBadge = document.getElementById('modal-lang-badge');
            if (langBadge) {{
                if (asset.lang) {{
                    langBadge.classList.remove('hidden');
                    langBadge.innerText = `${{asset.lang_flag || '🌐'}} ${{asset.lang_name || asset.lang}} (${{asset.lang}})`;
                }} else {{
                    langBadge.classList.add('hidden');
                }}
            }}
            
            const downloadBtn = document.getElementById('modal-download');
            downloadBtn.href = asset.path;
            downloadBtn.download = asset.name;
            downloadBtn.innerText = `📥 Download ${{asset.ext.toUpperCase()}}`;

            const altBtn = document.getElementById('modal-alt-download');
            if (asset.ext === 'svg' && asset.png_path) {{
                altBtn.classList.remove('hidden');
                altBtn.href = asset.png_path;
                altBtn.download = asset.name.replace(/\\.svg$/i, '.png');
                altBtn.innerText = '📥 Download PNG';
            }} else if (asset.ext === 'png' && asset.svg_path) {{
                altBtn.classList.remove('hidden');
                altBtn.href = asset.svg_path;
                altBtn.download = asset.name.replace(/\\.png$/i, '.svg');
                altBtn.innerText = '📥 Download SVG';
            }} else {{
                altBtn.classList.add('hidden');
            }}

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
                stage.innerHTML = `<video controls autoplay loop class="max-h-[300px] rounded-lg shadow-sm"><source src="${{asset.path}}" type="video/mp4"></video>`;
            }} else if (asset.ext === 'riv') {{
                stage.innerHTML = `<div class="text-center p-6"><span class="text-5xl block mb-2">📐</span><span class="font-bold text-stone-800 text-sm">Rive Vector Animation (.riv)</span><p class="text-xs text-stone-500 mt-1">Interactive runtime format. Download to open in Rive editor or embed in application runtime.</p></div>`;
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

        function copyAssetPath() {{
            if (!currentModalAsset) return;
            navigator.clipboard.writeText(currentModalAsset.path).then(() => {{
                const btn = document.getElementById('modal-copy-path');
                const orig = btn.innerText;
                btn.innerText = '✓ Copied Path!';
                setTimeout(() => {{ btn.innerText = orig; }}, 2000);
            }});
        }}

        function copyDocPath() {{
            const p = document.getElementById('reader-path').innerText;
            if (!p) return;
            navigator.clipboard.writeText(p).then(() => {{
                const el = document.getElementById('reader-path');
                const orig = el.innerText;
                el.innerText = '✓ Copied!';
                setTimeout(() => {{ el.innerText = orig; }}, 1500);
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

        // Initialize Documentation & Research Explorer
        let currentSelectedDoc = null;

        function initDocViewer() {{
            filterDocs();
        }}

        function filterDocs() {{
            const query = (document.getElementById('doc-search').value || '').toLowerCase().trim();
            const container = document.getElementById('doc-list-container');
            container.innerHTML = '';

            const filteredDocs = ALL_DOCS.filter(d => {{
                return !query || d.title.toLowerCase().includes(query) || d.path.toLowerCase().includes(query) || d.category.toLowerCase().includes(query);
            }});

            if (filteredDocs.length === 0) {{
                container.innerHTML = '<p class="text-xs text-stone-400 py-3 text-center">No matching documents found.</p>';
                return;
            }}

            // Group by category
            const groups = {{}};
            filteredDocs.forEach(d => {{
                if (!groups[d.category]) groups[d.category] = [];
                groups[d.category].push(d);
            }});

            let isFirst = true;

            for (const [catName, catDocs] of Object.entries(groups)) {{
                const groupDiv = document.createElement('div');
                groupDiv.className = 'space-y-1';

                const groupHeader = document.createElement('div');
                groupHeader.className = 'text-[11px] font-bold text-stone-400 uppercase tracking-wider px-2 py-1 flex items-center justify-between';
                groupHeader.innerHTML = `<span>${{catName}}</span><span class="text-[10px] font-normal text-stone-400">${{catDocs.length}}</span>`;
                groupDiv.appendChild(groupHeader);

                catDocs.forEach(doc => {{
                    const item = document.createElement('button');
                    item.className = 'doc-nav-item w-full text-left px-3 py-2 rounded-xl text-xs font-semibold text-stone-700 hover:bg-stone-200/60 transition flex items-center justify-between cursor-pointer gap-2';
                    
                    let badgeHtml = '';
                    if (doc.is_design_spec) {{
                        badgeHtml = '<span class="px-1.5 py-0.5 rounded text-[9px] font-bold bg-amber-200 text-amber-900 shrink-0">AI Spec</span>';
                    }} else if (doc.path.includes('Consent') || doc.path.includes('Privacy')) {{
                        badgeHtml = '<span class="px-1.5 py-0.5 rounded text-[9px] font-bold bg-purple-100 text-purple-800 shrink-0">GDPR</span>';
                    }}

                    item.innerHTML = `<span class="truncate">${{doc.title}}</span>${{badgeHtml}}`;
                    item.onclick = () => loadDoc(doc, item);
                    groupDiv.appendChild(item);

                    if (!currentSelectedDoc && isFirst) {{
                        loadDoc(doc, item);
                        isFirst = false;
                    }} else if (currentSelectedDoc && currentSelectedDoc.path === doc.path) {{
                        item.classList.add('bg-orange-100', 'text-orange-900', 'font-bold');
                    }}
                }});

                container.appendChild(groupDiv);
            }}
        }}

        function loadDoc(doc, itemEl) {{
            currentSelectedDoc = doc;

            document.querySelectorAll('.doc-nav-item').forEach(b => {{
                b.classList.remove('bg-orange-100', 'text-orange-900', 'font-bold');
            }});
            if (itemEl) {{
                itemEl.classList.add('bg-orange-100', 'text-orange-900', 'font-bold');
            }}

            document.getElementById('reader-title').innerText = doc.title;
            document.getElementById('reader-category').innerText = doc.category;
            document.getElementById('reader-path').innerText = doc.path;

            const githubBtn = document.getElementById('doc-github-link');
            if (githubBtn) {{
                githubBtn.href = `https://github.com/openfoodfacts/openfoodfacts-design/blob/main/${{encodeURIComponent(doc.path)}}`;
            }}

            // Show or hide experimental banner for DESIGN.md
            const banner = document.getElementById('design-experiment-banner');
            if (doc.is_design_spec || doc.path === 'DESIGN.md') {{
                banner.classList.remove('hidden');
            }} else {{
                banner.classList.add('hidden');
            }}

            const readerBody = document.getElementById('reader-body');
            if (typeof marked !== 'undefined') {{
                readerBody.innerHTML = marked.parse(doc.content);

                // Intercept relative markdown links to switch docs within the reader
                readerBody.querySelectorAll('a').forEach(a => {{
                    const href = a.getAttribute('href');
                    if (href && (href.endsWith('.md') || href.includes('.md#'))) {{
                        const cleanDocPath = href.split('#')[0].replace(/^\\.\\//, '');
                        const targetDoc = ALL_DOCS.find(d => d.path === cleanDocPath || d.path.endsWith(cleanDocPath) || cleanDocPath.endsWith(d.path));
                        if (targetDoc) {{
                            a.onclick = (e) => {{
                                e.preventDefault();
                                loadDoc(targetDoc, null);
                            }};
                            a.title = `Read ${{targetDoc.title}} in documentation viewer`;
                        }}
                    }}
                }});
            }} else {{
                readerBody.innerText = doc.content;
            }}
        }}

        // Initialize on load
        document.addEventListener('DOMContentLoaded', () => {{
            filterAssets();
            setupInfiniteScroll();
            initDocViewer();
        }});
    </script>

</body>
</html>
"""

output_path = os.path.join(repo_root, 'index.html')
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"Generated {output_path} successfully ({os.path.getsize(output_path)} bytes).")
