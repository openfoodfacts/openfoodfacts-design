# Open Food Facts — Design System

> **Format:** This file follows the [Google Stitch DESIGN.md](https://stitch.withgoogle.com/docs/design-md/overview) specification — a standardised, agent-readable way for open-source projects to document their design system in a single, version-controlled file. Coding agents and UI generators must strictly adhere to these design tokens and constraints to ensure brand consistency.
>
> **Note:** This document is an experiment to help Large Language Models (LLMs) and AI coding agents respect the Open Food Facts graphic charter, design tokens, and components when generating UI code. As an evolving experiment, it might contain mistakes or discrepancies with live production implementations. Always cross-reference with the [Graphic Charter](./graphic-charter) and official product repositories.

---

## Table of Contents

1. [Overview](#1-overview)
2. [Brand Architecture](#2-brand-architecture)
3. [Design Tokens: Color Palette](#3-design-tokens-color-palette)
4. [Typography Rules](#4-typography-rules)
5. [Logo Implementation & Layout Constraints](#5-logo-implementation--layout-constraints)
6. [Design Principles](#6-design-principles)
7. [Visual Language](#7-visual-language)
   - [Iconography](#71-iconography)
   - [Grid & Spacing](#72-grid--spacing)
   - [Illustrations](#73-illustrations)
   - [Animations](#74-animations)
8. [UI Components](#8-ui-components)
   - [Buttons](#81-buttons)
   - [Forms & Inputs](#82-forms--inputs)
   - [Product Cards](#83-product-cards)
   - [Navigation Elements](#84-navigation-elements)
   - [Modals & Dialogs](#85-modals--dialogs)
   - [Data Visualization](#86-data-visualization)
   - [Tables](#87-tables)
9. [Page Templates](#9-page-templates)
10. [Avatar System](#10-avatar-system)
11. [Content & Communication](#11-content--communication)
12. [Accessibility](#12-accessibility)
13. [UX Research](#13-ux-research)
14. [Contributing](#14-contributing)
15. [Resources & Tools](#15-resources--tools)

---

## 1. Overview

**Open Food Facts** is a free, open, collaborative database of food products from around the world. This design system documents the visual identity, components, and UX patterns used across all Open Food Facts products — including the mobile app, website, Open Prices, and related tools.

### Products covered

| Product | Repository | Status |
|---|---|---|
| Mobile App (smooth-app) | [openfoodfacts/smooth-app](https://github.com/openfoodfacts/smooth-app) | Active |
| Website (server) | [openfoodfacts/openfoodfacts-server](https://github.com/openfoodfacts/openfoodfacts-server) | Active |
| Explorer (next-gen frontend) | [openfoodfacts/openfoodfacts-explorer](https://github.com/openfoodfacts/openfoodfacts-explorer) | Active |
| Open Prices | [openfoodfacts/open-prices-frontend](https://github.com/openfoodfacts/open-prices-frontend) | Active |
| Taxonomy Editor | [openfoodfacts/taxonomy-editor](https://github.com/openfoodfacts/taxonomy-editor) | Active |
| Hunger Games | [openfoodfacts/hunger-games](https://github.com/openfoodfacts/hunger-games) | Active |
| Web Components | [openfoodfacts/openfoodfacts-webcomponents](https://github.com/openfoodfacts/openfoodfacts-webcomponents) | Active |
| NutriPatrol | [openfoodfacts/nutripatrol-frontend](https://github.com/openfoodfacts/nutripatrol-frontend) | Active |

### Target audiences

- **Consumers** — People looking up product information
- **Journalists** — People researching food data
- **Contributors**
  - Catalogue contributors (adding/editing product data)
  - Developers (implementing features)
  - Designers (contributing to the design system)

---

## 2. Brand Architecture

The Open Food Facts ecosystem consists of four distinct sub-brands. The UI must dynamically adapt its primary accent color depending on the active brand context. All sub-brands share the same foundational design system (typography, spacing, components) but use their designated accent color as the primary UI action color.

| Sub-brand | Token | Hex | Usage context |
|---|---|---|---|
| **Open Food Facts** | `brand-food` | `#FF8714` | Food product pages, food-related flows |
| **Open Beauty Facts** | `brand-beauty` | `#008C8C` | Beauty product pages, beauty-related flows |
| **Open Pet Food Facts** | `brand-pet-food` | `#FF6E78` | Pet food product pages, pet food flows |
| **Open Products Facts** | `brand-products` | `#0064C8` | Generic product pages, fallback brand |

> **For coding agents:** Read the active brand from context (e.g., a `brand` prop, a CSS custom property `--brand-accent`, or a theme variable) and apply the corresponding token as the primary color for buttons, links, focus rings, and other accent elements.

---

## 3. Design Tokens: Color Palette

### Base & Structural Colors (Graphic Charter)

| Token | Hex | RGB | CMYK | Usage |
|---|---|---|---|---|
| `color-text-primary` | `#000000` | `0 / 0 / 0` | `0 / 0 / 0 / 100` | Primary text, headings, high-emphasis labels |
| `color-background-default` | `#F5F5F5` | `245 / 245 / 245` | `0 / 0 / 0 / 10` | Default page/screen background |
| `color-surface-white` | `#FFFFFF` | `255 / 255 / 255` | `0 / 0 / 0 / 0` | Card surfaces, modal backgrounds, input fills ("smile") |
| `color-grayscale` | 0%–100% `#000000` | 0%–100% Black | 0%–100% K | Dividers, disabled states, secondary text ("100 grays") |

### Brand Accent Colors

Map the primary brand accent color (`--brand-accent`) to the active brand:

| Token | Hex | RGB | CMYK | Brand |
|---|---|---|---|---|
| `brand-food` | `#FF8714` | `255 / 135 / 20` | `0 / 55 / 100 / 0` | Open Food Facts (Orange) |
| `brand-beauty` | `#008C8C` | `0 / 140 / 140` | `90 / 20 / 50 / 0` | Open Beauty Facts (Turquoise) |
| `brand-pet-food` | `#FF6E78` | `255 / 110 / 120` | `0 / 70 / 40 / 0` | Open Pet Food Facts (Pink) |
| `brand-products` | `#0064C8` | `0 / 100 / 200` | `90 / 55 / 0 / 0` | Open Products Facts (Blue) |

### Product UI Palette (Coffee / Espresso System)

In live production products (`world.openfoodfacts.org` and `smooth-app` v4.24.0), UI surfaces, buttons, and borders use a warm coffee-inspired neutral scale defined in `SmoothColorsThemeExtension`:

| Token (`smooth-app`) | Coffee Name | Hex | Usage |
|---|---|---|---|
| `primaryUltraBlack` | Ristretto | `#201A17` | Dark mode surface, deepest espresso ink |
| `primaryBlack` | Chocolate | `#341100` | Primary action buttons (`--editor-button-bg`), links, snackbar background |
| `primaryDark` | Cortado | `#483527` | Light mode FAB background, strong accents |
| `primarySemiDark` | Mocha | `#52443D` | Selected toggles/checkboxes (light), secondary dark text |
| `primaryTone` | Darker Macchiato | `#81756C` | Muted warm accents |
| `primaryAccent` | — | `#875737` | Warm brown highlight |
| `primaryNormal` | Macchiato | `#A08D84` | Dark mode secondary, borders, muted labels |
| `primaryMedium` | Cappuccino | `#EDE0DB` | Secondary button fill (`.button.secondary`), light mode secondary, switch track |
| `primaryLight` | Latte | `#F6F3F0` | Soft warm surface tint (`#FAF8F6` / `#FAFAFA` on web) |
| `secondaryNormal` | — | `#F2994A` | Warm orange UI accent |
| `secondaryVibrant` | — | `#FB8229` | High-emphasis orange highlight |
| `secondaryLight` | — | `#EE8858` | Soft orange highlight |

### Semantic & Nutrition Score Colors

| Token | Hex | Background Tint | Usage |
|---|---|---|---|
| `color-success` | `#219653` (web/app) / `#4FA125` (web CTA) | `#DEEDDB` | Confirming actions, Nutri-Score A / Green-Score A+–A (`#00641E`) |
| `color-success-light` | `#60AC0E` | `#E6FFCC` | Nutri-Score B / positive indicators |
| `color-warning` | `#FB8229` / `#F2994A` | `#F2E2D6` / `#FFE6CC` | Cautionary alerts, Nutri-Score D (`#E07312`) |
| `color-caution` | `#F2C94C` / `#C88F01` | `#FFFFCC` | Nutri-Score C / moderate indicators |
| `color-error` | `#EB5757` (web/app) / `#EA2B2B` (AMOLED) | `#F6E4E4` / `#FFCCCC` | Validation errors, destructive actions, Nutri-Score E |
| `color-info` | `#2D9CDB` (app) / `#00588D` (web) | `#F0F5F9` | Neutral informational messages, cropper/tool highlights (`#0064C8`) |

### Theme Modes (Mobile App)

| Mode | Surface | Scaffold / Canvas | Text / Primary | Notes |
|---|---|---|---|---|
| **Light** | `#FFFFFF` | `#F6F3F0` / `#FAF8F6` (odd rows) | `#000000` / `#85746C` | Default light theme |
| **Dark** | `#201A17` | `#303030` (scaffold), `#2D251E` (odd rows) | `#FFFFFF` / `#A08D84` | Warm espresso dark mode |
| **AMOLED (True Dark)** | `#000000` | `#000000` | User-selectable accent + contrast | Supports Low (`#969696`), Medium (`#CACACA`), High (`#FFFFFF`) text contrast |

### Grayscale System

The graphic charter defines a 100-step scale from 0% to 100% Black (`#000000` / CMYK K). Named steps in product UIs:

| Step | Hex | Usage |
|---|---|---|
| `gray-100` | `#F5F5F5` / `#F2F2F2` | Background fills |
| `gray-200` | `#E5E5E5` / `#E0E0E0` | Dividers (`#ECECEC`, `#DFDFDF`), borders |
| `gray-400` | `#BFBFBF` / `#BDBDBD` | Placeholder text, disabled borders |
| `gray-600` | `#757575` / `#6C6C6C` | Secondary text, captions (`greyNormal`) |
| `gray-800` | `#4F4F4F` / `#424242` | Sub-headings, strong secondary text (`PRIMARY_GREY_COLOR`) |
| `gray-900` | `#212121` | Near-black text |

### Accessibility

All color combinations must achieve a minimum contrast ratio of **4.5:1** for normal text and **3:1** for large text (18px+ bold or 24px+ regular), in accordance with WCAG 2.1 AA.

---

## 4. Typography Rules

Open Food Facts uses **Plus Jakarta Sans** as its official brand typeface (per the Graphic Charter), while live production platforms pair it with **Public Sans** (website) and **Open Sans** (mobile app) for high-legibility UI copy.

### Typefaces by Context

| Context | Primary Typeface | Fallbacks / Weights | License |
|---|---|---|---|
| **Brand, Logos & Marketing** | `Plus Jakarta Sans` | ExtraLight (`200`) – ExtraBold (`800`), normal & italic | Open Font License ([Google Fonts](https://fonts.google.com/specimen/Plus+Jakarta+Sans)) |
| **Website (`world.openfoodfacts.org`)** | `Public Sans` (UI/body), `Plus Jakarta Sans` (headings/brand) | `Helvetica, Roboto, Arial, sans-serif` | Open Font License |
| **Mobile App (`smooth-app` v4.24.0)** | `OpenSans` (`OpenSans-*.ttf`) | Regular (`400`), Medium (`500`), SemiBold (`600`), Bold (`700`) | Apache 2.0 |

### Plus Jakarta Sans Weights (Graphic Charter)

All weights support both normal and italic styles:

| Weight name | CSS weight value |
|---|---|
| ExtraLight | `200` |
| Light | `300` |
| Regular | `400` |
| Medium | `500` |
| SemiBold | `600` |
| Bold | `700` |
| ExtraBold | `800` |

### Type Scale (Web & Editorial)

| Role | Weight | Size (px) | Line height | Usage |
|---|---|---|---|---|
| Display | ExtraBold (800) | 48–64 | 1.1 | Hero headings, marketing |
| H1 | Bold (700) | 32–40 | 1.2 | Page titles |
| H2 | SemiBold (600) | 24–28 | 1.25 | Section headings |
| H3 | SemiBold (600) | 20–22 | 1.3 | Sub-section headings |
| Body Large | Regular (400) | 18 | 1.6 | Lead paragraphs, introductions |
| Body | Regular (400) | 16 (14px base on legacy server) | 1.5 | Main body copy |
| Body Small | Regular (400) | 14 | 1.5 | Captions, metadata |
| Label | Medium (500) | 12–14 | 1.4 | UI labels, badges, tags |

### Type Scale (Mobile App — `smooth-app` `TextTheme`)

| Flutter `TextTheme` Role | Weight | Size (px) | Notes |
|---|---|---|---|
| `displayLarge` | Bold (`700`) | `28.0` | Screen display titles |
| `displayMedium` | Bold (`700`) | `24.0` | Major section headers |
| `displaySmall` | Bold (`700`) | `18.0` | Sub-section headers |
| `headlineMedium` | Bold (`700`) | `16.0` (`LARGE_SPACE`) | Card & panel titles |
| `bodyMedium` | Regular (`400`) | `14.0` | Body copy (`letterSpacing: 0.5`) |
| `titleMedium` | Regular (`400`) | `14.0` | List titles, form labels |
| `titleSmall` | Regular (`400`) | `12.0` | Captions, helper text |

**Type rules:**
- Use **Plus Jakarta Sans** for all brand communications, logos, marketing pages, and new web frontends (e.g., Explorer)
- In `smooth-app`, always use `Theme.of(context).textTheme` with the bundled `OpenSans` family (supporting AMOLED Low/Medium/High contrast overrides)
- Minimum recommended body text size: **16px** for editorial/marketing web, **14px** for dense product UIs (never go below `12px` for labels/captions)
- For code snippets or technical content, use a system monospace font as a complement only

---

## 5. Logo Implementation & Layout Constraints

The logo is the primary brand asset. All implementations must follow these rules exactly.

### Available Logo Files

| Variant | File | Recommended use |
|---|---|---|
| Horizontal – Light | `images/logos/openfoodfacts/off-logo-horizontal-light.svg` | Light UI backgrounds |
| Horizontal – Dark | `images/logos/openfoodfacts/off-logo-horizontal-dark.svg` | Dark UI backgrounds |
| Horizontal – Mono Black | `images/logos/openfoodfacts/off-logo-horizontal-mono-black.svg` | Single-colour print |
| Horizontal – Mono White | `images/logos/openfoodfacts/off-logo-horizontal-mono-white.svg` | Photography overlays, dark print |
| Vertical – Light | `images/logos/openfoodfacts/off-logo-vertical-light.svg` | Light backgrounds, portrait format |
| Vertical – Dark | `images/logos/openfoodfacts/off-logo-vertical-dark.svg` | Dark backgrounds, portrait format |
| Icon – Light | `images/logos/openfoodfacts/off-logo-icon-light.svg` | App icons, favicons (light context) |
| Icon – Dark | `images/logos/openfoodfacts/off-logo-icon-dark.svg` | App icons, favicons (dark context) |
| Favicon | `images/logos/openfoodfacts/off-logo-favicon-light.png` | Browser tabs |

[![Figma](https://img.shields.io/badge/figma-%23F24E1E.svg?logo=figma&logoColor=white) Logo of Open Food Facts](https://www.figma.com/design/HKAAPSQq8CZZO5uAziabRY/New-Open-Food-Facts-logo?m=auto&t=bGdHdz45zaPlgTnW-6)

### Spatial Requirements & Construction Specs

- **Safety Margin:** A strict protection grid/safety margin (equal to the circular magnifying-glass unit) must be maintained around the horizontal, vertical, and single-icon logos at all times. No text, images, or other UI components may encroach on this padding. Refer to the [Brand Guidelines PDF](./graphic-charter/BRAND%20GUIDELINES_OFF_V1.pdf) (Page 5) for the protection grid.
- **Tilted Pill ("FOOD" / Category Badge) Construction (Graphic Charter Page 9):**
  - Base scale: `L: 500px / H: 180px`
  - Corner radius: `30px` (at scale)
  - Rotation: `5°` counter-clockwise
  - Horizontal padding inside pill: `40px` (at scale)
  - Typography: `Plus Jakarta Sans ExtraBold` (`158pt` at `500×180px` scale)
- **Small Scale Contexts:** For small UI areas (mobile app icons, social network avatars with circular cropping, browser favicons with a transparency zone), strictly use the synthetic single-icon version of the logo (`off-logo-icon-*.svg`) to guarantee legibility. Never use the full horizontal or vertical logo at small sizes.

### Background Adaptation & Color Treatments

The Graphic Charter (Pages 11–14) defines four official logo color treatments:

| Treatment | Light Background (`#FFFFFF`, `#F5F5F5`) | Dark Background (`#000000`, `#201A17`) |
|---|---|---|
| **Color** | Standard color icon + pill with black wordmark (`-light`) | Standard color icon + pill with white wordmark (`-dark`) |
| **Black & White** | Grayscale icon + pill with black wordmark | Grayscale icon + pill with white wordmark |
| **Monochrome / Color** | Single brand color (Orange/Turquoise/Pink/Blue) on light bg | Single brand color on dark bg |
| **Monochrome / B&W** | Solid black (`-mono-black`) — single-colour print | Solid white (`-mono-white`) — photography overlays, dark print |

### Visual Integrity — Strict "Do Nots"

> **For coding agents:** These constraints are non-negotiable. Any generated code that violates these rules must be corrected before shipping.

- ❌ **DO NOT** distort the proportions or aspect ratio of the logo (no non-uniform `width`/`height` or `transform: scale(x, y)` with differing values)
- ❌ **DO NOT** alter the core logo colors or apply CSS `filter` properties to the logo element
- ❌ **DO NOT** add `drop-shadow`, `box-shadow`, glows, gradients, or any other visual effects to the logo
- ❌ **DO NOT** apply the logo over non-uniform or low-contrast backgrounds that compromise readability
- ❌ **DO NOT** resize individual elements of the logo independently or remove any of its components
- ❌ **DO NOT** redraw or recreate the logo — always use the provided vector files from `images/logos/`
- ❌ **DO NOT** change the logo axis or rotate it

### Sister Brand Logos

Logos for all sister brands are available in `images/logos/` following the same file-naming conventions:

| Brand | Directory |
|---|---|
| Open Beauty Facts | `images/logos/openbeautyfacts/` |
| Open Pet Food Facts | `images/logos/openpetfoodfacts/` |
| Open Products Facts | `images/logos/openproductsfacts/` |
| Open Prices | `images/logos/openprices/` |
| Green Score | `images/logos/green-score/` |

---

## 6. Design Principles

These principles guide every design decision at Open Food Facts. When in doubt, refer back to them.

| Principle | Description |
|---|---|
| **Clarity** | Present complex nutritional and environmental data in a way that is immediately understandable to any user, regardless of their background. |
| **Data-Driven** | Ground every design decision in real user research and product data. Avoid assumptions; validate with evidence. |
| **Accessibility** | Ensure our products are usable by everyone — including people with disabilities, on slow connections, and on low-end devices. Follow WCAG 2.1 AA as a minimum. |
| **Community-Powered** | Design for contribution. Make it easy for anyone to add or improve product data, and celebrate the community's work. |
| **Iterative** | Ship early, learn fast, and improve continuously. Favour progress over perfection. |
| **Transparency** | Open Food Facts is built on openness — our design process, assets, and decisions should be as open as the data. |

---

## 7. Visual Language

### 7.1 Iconography

Open Food Facts uses icons from multiple sources across its products.

#### Website / Server Icons

The icons used on the Open Food Facts website (`world.openfoodfacts.org`) combine:
- **[Google Material Symbols and Icons](https://fonts.google.com/icons)** (`Material Icons` font & inline SVGs)
- **Custom `icomoon` icon font** and bespoke SVGs in the [`icons/` directory of `openfoodfacts-server`](https://github.com/openfoodfacts/openfoodfacts-server/tree/main/icons), including custom icons designed by [@stephanegigandet](https://github.com/stephanegigandet).

#### Mobile App Icons (`smooth-app` v4.24.0)

The mobile app bundles four icon fonts in `FontManifest.json` plus vector SVG assets:

- **Smooth Icons (`SmoothIcons.ttf`):** Custom app UI icon font (`assets/fonts/SmoothIcons.ttf`) for navigation, scanning, and product actions.
- **Food Icons (`FoodIcons.ttf`):** Handcrafted food & category icon font created by [@g123k](https://github.com/g123k), located at [`packages/smooth_app/assets/fonts/`](https://github.com/openfoodfacts/smooth-app/tree/develop/packages/smooth_app/assets/fonts).
- **Material Icons & Cupertino Icons:** Platform-adaptive icons (`MaterialIcons-Regular.otf`, `CupertinoIcons.ttf`).
- **Tintable & Vector Assets:** Additional SVG and `.svg.vec` assets in `assets/cacheTintable/` (e.g., `agriculture.svg`, `palm-oil.svg`, `monkey_happy.svg`, `vegetarian.svg`), `assets/icons/`, and `assets/packagings/`.

#### General Icon Library

For web tools and frontends, **Font Awesome** and **Material Icons** are also used as supplementary icon libraries.

**Usage guidelines:**
- Always pair icons with descriptive text labels when space permits, for accessibility
- Use consistent icon sizing within a given context (`24px` default, `DEFAULT_ICON_SIZE = 24.0` in `smooth-app`)
- Ensure icons meet colour contrast requirements against their background
- Do not use icons alone to convey critical information — always provide a text alternative
- When adding new icons to the server, prefer sourcing from [Google Material Symbols](https://fonts.google.com/icons) for consistency

---

### 7.2 Grid & Spacing

**Design system spacing scale:**
- Base unit: **8px** (with **4px** fine-adjustment step)
- General multiples: `4, 8, 16, 24, 32, 40, 48, 64, 80, 96…`

**Mobile App (`smooth-app`) spacing & border-radius tokens (`design_constants.dart`):**

| Token | Value | Usage |
|---|---|---|
| `VERY_SMALL_SPACE` | `4.0px` | Tight inline gaps, micro-padding |
| `SMALL_SPACE` | `8.0px` | Compact spacing, icon-to-label gaps |
| `BALANCED_SPACE` | `10.0px` | Balanced list/card internal padding |
| `MEDIUM_SPACE` | `12.0px` | Standard element separation |
| `LARGE_SPACE` | `16.0px` | Screen margins, section spacing |
| `VERY_LARGE_SPACE` | `20.0px` | Major section separation |
| `ANGULAR_RADIUS` | `8.0px` | Knowledge panels, full-screen action buttons |
| `ROUNDED_RADIUS` | `20.0px` | `SmoothCard` and content containers |
| `HEADER_ROUNDED_RADIUS` | `30.0px` | Top bar / sheet headers |
| `CIRCULAR_RADIUS` | `40.0px` | Pill buttons & text fields |
| `MAX_BORDER_RADIUS` | `100.0px` | Fully rounded badges / pills |

**Website (`world.openfoodfacts.org`) layout grid & breakpoints (Foundation, `14px` base `rem`):**
- Mobile (`small`): 4-column grid, 16px margins, `< 40.063em` (`≤ 640px`)
- Tablet (`medium`): 8-column grid, `min-width: 40.063em` (`641px`) / `45.786em` (`641px` at 14px rem)
- Desktop (`large`): 12-column grid, `min-width: 64em` (`1024px`)
- Wide (`xlarge` / `xxlarge`): `min-width: 90.063em` (`1441px`) and `120.063em` (`1921px`)

**Design principles for layout:**
- Maintain consistent vertical rhythm through spacing units
- Use grid alignment to create visual order and predictability
- Respect safe zones around the logo and key UI elements

---

### 7.3 Illustrations

Illustrations are available in `images/illustrations/` (178 SVGs + PNG exports across 6 categories) and in the mobile app (`packages/smooth_app/assets/`):

| Category | Directory | SVG Count | Description & Examples |
|---|---|---|---|
| **Food** | `images/illustrations/food/` | 47 | Food products & food UI (avocado, butter, cheese, chocolate bar, cereal pack, egg/carton, flour, fridge, pizza, donut, Nutri-Score/Green-Score scale, settings) |
| **Beauty** | `images/illustrations/beauty/` | 28 | Beauty & personal care (bottles, cream pot, deodorant, lipstick, nail polish, soap, sunscreen, toothbrush/toothpaste, facemask character) |
| **Pet Food** | `images/illustrations/pet-food/` | 9 | Pet food & care (bone, paw print, pet food bowl, kibble bag, kibbles, pâté) |
| **Products** | `images/illustrations/products/` | 15 | Non-food products (batteries, bicycle, drill, glasses, light bulbs, spray bottle, washing machine, weights) |
| **Open Prices** | `images/illustrations/prices/` | 18 | Price & receipt illustrations (coins, dollar bill, credit card, gold bag, piggy bank, loyalty cards, price tags, receipt extraction, store comparison) |
| **Shared** | `images/illustrations/shared/` | 61 | Cross-product UI & community (barcode, scientist characters, magnifying glasses for fat/salt/sugar/scan, donate heart, high-five, puzzle, camera, onboarding) |

- **Animated SVGs:** Several categories include CSS/SMIL-animated SVGs named `*-animated.svg` (e.g., `food-settings-animated.svg`, `greenscore-nutriscore-scale-animated.svg`, `crowdsourcing-icon-animated.svg`, `off-add-products-cosmetics-animated.svg`).
- **Light & Dark Mode Variants:** Illustrations for product UIs provide explicit light/dark pairs where needed (e.g., `Illustrations - Food settings - Dark mode.svg`, `magnifying-glass-ingredients-dark-mode.svg`, and in `smooth-app`: `product_completed_graphic_dark.svg` / `_light.svg`, `counter-dark.svg` / `-light.svg`).

[![Figma](https://img.shields.io/badge/figma-%23F24E1E.svg?logo=figma&logoColor=white) Illustrations for Open Food Facts](https://www.figma.com/design/aM6Yu2w3JGBuHTXDHoeUuf/Illustrations?m=auto&t=bGdHdz45zaPlgTnW-6)

#### 7.3.1 Flat Vector Illustration Style Guide

##### Core Visual Principles
Technique: Flat design vector illustration. The image must look as if it was created with vector paths and filled with solid colour (no raster effects, pencil lines, or texture).

Dimensionality: Strictly 2D. Do not include any depth cues, perspective lines, gradients, shadows (soft or hard), or highlights (unless rendered as solid shapes).

Linework: Avoid prominent black outlines. Prefer the contrast between adjacent coloured shapes to define form. If lines must be used (e.g., mouth, implied text on a label, a thin screen edge), they should be minimal, of uniform weight, and a dark, non-black colour.

Simplification: Reduce all elements (characters, objects, animals, etc.) to their most essential geometric forms. A face is a circle; a body is a rectangle. Simplify all details.

##### Character & Figure Guide
Anatomy: Heads are simple circles with dot eyes and a curved line for a mouth. No noses. Ears are simple semicircles. Hands and fingers are simplified to rectangular shapes. Feet are simple block shapes.

Clothing: Represented as simple blocks of solid colour. Features like buttons or pocket flaps are also rendered as simple, solid shapes.

Hair: Solid, blocky shapes without strands or gradients.

##### Colour Palette Guide
Colour Use: Use a limited, intentional, and high-contrast colour palette with no gradients. Adjacent shapes should have a clear visual separation.

Primary Illustration Tokens (observed across `images/illustrations/` and `smooth-app` SVGs):
- **Greens:** `#009A49`, `#009664`, `#00641E`, `#0B7A3E`
- **Blues / Cyans:** `#00BDF2`, `#00A4FF`, `#0077C8`, `#0078DB`, `#79E7FF`, `#DCF0F7`
- **Yellows / Oranges:** `#F8C100`, `#FFC412`, `#FFBE00`, `#FF6B35`, `#FFC88C`
- **Reds:** `#F03214`, `#DC3522`
- **Neutrals / Browns:** `#181818`, `#341100`, `#52443D`, `#606362`, `#999999`, `#E2E2E2`, `#FFFFFF`, `#955830`, `#6C3C00`

Secondary/Branding Colors: Light blues (`#79E7FF`, `#DCF0F7`) for screens or water, pinks and light purples (`#F1B0FF`) for products/fluids, warm skin/hair browns (`#FFC88C`, `#955830`, `#6C3C00`).

##### Object & Detail Guide
Objects: Simplify to geometric shapes. Appliances, tools, containers, etc., should be easily identifiable but minimally detailed.

Details: Intricacies are removed. Placeholder elements like text on a label are represented by a few solid parallel lines. Small, abstract floating elements (like small circles for liquid drops) are encouraged to suggest motion or fluid, but they must be flat and solid.

##### Environment & Context
Background: Use a clean, simple, solid-color background (or transparent) without any complex patterns or gradients.

Framing: The composition should be straightforward and centered.

##### Structured Prompt Template
You can use this structure for your prompts, but models work best by adding one or two sample images (an object and a person, and the official logo if needed). As of May 2026, ChatGPT was working well, while NanoBanana was not.

```text
[Subject, e.g., A developer at a desk with a laptop], 2D flat design vector illustration style.
The image uses clean geometric shapes and strictly solid, flat colors, with no gradients,
shadows, or realistic textures. No prominent outlines are present, with form defined by
contrasting color blocks. The character has simplified features: a simple geometric face with
dot eyes and a mouth curve, blocky hair, and clothing represented as simple colored rectangles.
The [Subject's action/objects] are similarly simplified to their essential shapes. Details are
minimal. The color palette is limited to specific oranges, teals, pinks, greys, and browns.
Clean, solid color background. Minimalist composition.
```

---

### 7.4 Animations

Rive animations are stored in `animations/` and bundled in `smooth-app` (`assets/animations/`).

| Animation | Location | Description |
|---|---|---|
| Scan + Nutri-Score + Green Score | `animations/scan-nutriscore-greenscore/` | Product scanning animation showing Nutri-Score and Green Score reveal |
| App Rive Animations | `smooth-app` `assets/animations/off.riv`, `explanations.riv` | Onboarding, mascot, and score explanation animations in the mobile app |
| Animated Illustrations | `images/illustrations/**/*-animated.svg` | Lightweight CSS/SMIL-animated SVGs for web & documentation |

**Tools:** Interactive animations are created in [Rive](https://rive.app/).

---

## 8. UI Components

The component library is maintained in Figma. Below are specifications and links for each component category.

> **Note:** All component specifications are subject to the design principles of Clarity, Accessibility, and Consistency outlined in [Section 6](#6-design-principles).

---

### 8.1 Buttons

| Variant | Usage | States |
|---|---|---|
| **Primary** | Main call to action (e.g., "Add Product", "Search") | Default, Hover, Active, Disabled, Loading |
| **Secondary** | Secondary actions (e.g., "Cancel", "Learn More") | Default, Hover, Active, Disabled |
| **Tertiary / Ghost** | Low-emphasis actions (e.g., "Skip", text links) | Default, Hover, Active, Disabled |
| **Destructive** | Irreversible actions (e.g., "Delete") | Default, Hover, Active, Disabled |
| **Icon Button** | Icon-only actions with tooltip | Default, Hover, Active, Disabled |

**Button rules:**
- Always include visible focus states for keyboard navigation
- Minimum touch target size: **44×44px** (web / iOS, WCAG 2.1 AAA SC 2.5.5) and **48×48dp** (`kMinInteractiveDimension` in `smooth-app` Android)
- **Web (`world.openfoodfacts.org`):** Primary/editor actions use `#341100` background with `#FFFFFF` text and `8px` radius (or `.round` pill shape); secondary actions (`.button.secondary`) use `#EDE0DB` background, `#CFAC9E` border, and `#333333` text; success CTAs (`.button.success`) use `#4FA125` background with `#3F811E` border.
- **Mobile (`smooth-app`):** Standard buttons use `CIRCULAR_BORDER_RADIUS` (`40px` pill), while full-screen / knowledge-panel buttons use `ANGULAR_BORDER_RADIUS` (`8px`).
- Disabled buttons must not convey interactivity (no hover effects)
- Loading states should provide feedback without blocking the UI

---

### 8.2 Forms & Inputs

| Element | States |
|---|---|
| Text field | Default, Focus, Filled, Error, Disabled |
| Textarea | Default, Focus, Filled, Error, Disabled |
| Dropdown / Select | Default, Open, Selected, Error, Disabled |
| Checkbox | Unchecked, Checked, Indeterminate, Disabled |
| Radio button | Unselected, Selected, Disabled |
| Toggle / Switch | Off, On, Disabled |
| File upload | Default, Dragging, Uploaded, Error |

**Form rules:**
- All inputs must have visible, descriptive labels (not just placeholder text)
- Error messages must be programmatically associated with their input (`aria-describedby`)
- Required fields must be clearly marked
- Form validation should occur on submission and, where appropriate, on blur

---

### 8.3 Product Cards

Product cards are the primary way products are displayed in search results and lists.

**Card structure:**
1. Product image (with placeholder for missing images)
2. Product name
3. Brand name
4. Nutri-Score badge (A–E)
5. Eco-Score / Green Score badge
6. NOVA group indicator
7. Quantity / weight

**Card variants:**
- **List card** — Horizontal layout for dense list views
- **Grid card** — Vertical layout for grid views
- **Mini card** — Compact version for suggestions / related products

---

### 8.4 Navigation Elements

| Element | Description |
|---|---|
| **Header / App bar** | Primary navigation with logo, search, and user account |
| **Footer** | Site-wide links, legal info, language selector |
| **Tab bar (mobile)** | Bottom navigation for primary app sections |
| **Breadcrumbs** | Hierarchical location indicator for web |
| **Side navigation** | Secondary navigation for settings/profile pages |
| **Search bar** | Prominent global search with autocomplete |

---

### 8.5 Modals & Dialogs

| Type | Usage |
|---|---|
| **Confirmation dialog** | Confirm irreversible actions (e.g., delete, submit) |
| **Information modal** | Display additional context or help content |
| **Form modal** | Collect user input within an overlay |
| **Alert / Toast** | Non-blocking success, error, or warning notifications |
| **Bottom sheet (mobile)** | Mobile-native overlay for contextual actions |

**Modal rules:**
- Always include a clear close/dismiss mechanism
- Trap focus within the modal while it is open
- Return focus to the trigger element on close
- Do not use modals for complex multi-step flows

---

### 8.6 Data Visualization

Open Food Facts relies on rich data scores and visualizations to communicate nutritional and environmental impact.

| Visualization | Description |
|---|---|
| **Nutri-Score** | A–E letter grade with colour coding for nutritional quality |
| **Eco-Score / Green Score** | A–E letter grade for environmental impact |
| **NOVA group** | 1–4 scale for degree of food processing |
| **Ingredient list** | Highlighted ingredient analysis |
| **Nutrient table** | Standard nutritional facts table |
| **Comparison charts** | Bar/radar charts for comparing products |

**Data visualization rules:**
- Never rely on colour alone to convey meaning — always use labels or patterns
- Provide accessible text alternatives for all charts and scores
- Maintain consistent colour coding across the product (e.g., green = good, red = poor)

---

### 8.7 Tables

| Variant | Usage |
|---|---|
| **Data table** | Nutritional facts, product comparisons |
| **Sortable table** | Lists with user-controlled ordering |
| **Responsive table** | Degrades gracefully on small screens (horizontal scroll or card layout) |

---

## 9. Page Templates

These templates define the standard layouts for key pages across Open Food Facts products.

### 9.1 Product Page

The standard layout for a single product's detail page.

**Key sections:**
1. Product header (image gallery, name, brand, quantity)
2. Scores summary (Nutri-Score, Eco-Score, NOVA)
3. Ingredients & allergens
4. Nutritional facts table
5. Environmental impact
6. Product history & edits
7. Related products
8. Contribute / Edit CTA

[![Figma](https://img.shields.io/badge/figma-%23F24E1E.svg?logo=figma&logoColor=white) Current Website Design](https://www.figma.com/design/Qg9URUyrjHgYmnDHXRsTTB/Current-Website-design?m=auto&t=jNwvjRR8nIgOzzJZ-6)

---

### 9.2 Search Results Page

**Key sections:**
1. Search bar (persistent, pre-filled with query)
2. Filter & facet panel
3. Results count & sort options
4. Product card grid/list
5. Pagination / infinite scroll

---

### 9.3 User Contribution Flow

**"Add a Product" flow:**
1. Barcode scan / manual entry
2. Product photos upload (front, ingredients, nutrition, other)
3. Basic info (name, brand, quantity)
4. Nutritional facts entry
5. Ingredient list entry
6. Confirmation & submission

**"Edit a Product" flow:**
1. Find product
2. Select field to edit
3. Make edit with source / evidence
4. Submit for review

---

### 9.4 Homepage Template

**Key sections:**
1. Hero / search prompt
2. How it works (3-step explainer)
3. Stats (number of products, contributors, countries)
4. Recent contributions / highlights
5. Mission statement
6. Get involved CTA

---

### 9.5 User Profile & Settings

**Key sections:**
1. Profile header (avatar, username, contribution count)
2. Contribution history
3. Badges / achievements
4. Account settings
5. Notification preferences
6. Privacy settings

---

## 10. Avatar System

The avatar system allows users to create personalised profile avatars using composable SVG components.

**Location (SVG assets):** `avatars/svg/`  
**System root (config / JS / HTML / CSS):** `avatars/`

**Structure:** Avatars are composed of stacked SVG layers:

| Body Part | Examples |
|---|---|
| Body | Base body shape |
| Hair | Short, long, curly, etc. |
| Top clothes | T-shirt, sweatshirt, etc. |
| Bottom clothes | Jeans, skirt, etc. |
| Shoes | Sneakers, boots, etc. |

**Technical specifications:**
- All SVG files must be **250×300px**
- Full-width/height canvases — components positioned by their placement within the canvas
- Colors applied directly on SVG elements (`fill:` / `stroke:`) — not via CSS classes
- Use **Inkscape** to create or edit SVG files (not Illustrator)
- Naming convention: `[part].[type].[component].svg` (e.g., `hair.long.top.svg`)

**Configuration:** See `avatars/avatars-config.js` for the full list of parts, types, components, and selectable colours.

---

## 11. Content & Communication

### 11.1 Voice & Tone

Open Food Facts speaks with a voice that is:

| Attribute | Description |
|---|---|
| **Informative** | We provide clear, factual information without overwhelming the user |
| **Neutral** | We present data without bias or judgment |
| **Encouraging** | We celebrate contribution and make users feel their effort matters |
| **Approachable** | We avoid jargon; scientific concepts are explained in plain language |
| **Inclusive** | We speak to all audiences — from curious consumers to expert contributors |

**Tone adapts by context:**

| Context | Tone |
|---|---|
| Product scores | Neutral, factual |
| Onboarding | Warm, encouraging |
| Error messages | Clear, non-blaming, helpful |
| Contribution prompts | Motivating, community-focused |
| Legal / Privacy | Clear, precise |

---

### 11.2 Editorial & Writing Style Guide

**General rules:**
- Use **sentence case** for UI labels, headings, and buttons (not Title Case or ALL CAPS)
- Use **plain language** — aim for a reading level of grade 8 or below for consumer-facing content
- Prefer **active voice** over passive voice
- Keep button labels **action-oriented** (e.g., "Add product", "Edit ingredients", "Save changes")
- Avoid double negatives in error messages or instructions

**Terminology standards:**

| Term | Use | Avoid |
|---|---|---|
| Open Food Facts | Full name on first mention | OFF (except in code/URLs) |
| Nutri-Score | With hyphen, both words capitalised | Nutriscore, nutri score |
| Eco-Score | With hyphen, both words capitalised | Ecoscore |
| Green Score | Two words, both capitalised | Greenscore |
| NOVA | All caps (it's an acronym) | Nova, nova |
| Contributor | Generic term for anyone adding data | User, member |
| Product | The item being catalogued | Item, entry |

**Microcopy guidelines:**
- Write labels for the component, not for the page
- Validation errors should explain what went wrong AND how to fix it
- Empty states should be helpful and encourage action
- Loading states should set expectations (e.g., "Searching products…")
- Follow platform conventions for platform-specific microcopy (iOS vs Android vs Web)

---

## 12. Accessibility

Open Food Facts is committed to making its products usable by everyone.

**Standard:** WCAG 2.1 Level AA

### 12.1 Checklist for Designers

**Colour & Contrast:**
- [ ] Text contrast ratio ≥ 4.5:1 (normal text), ≥ 3:1 (large text / UI components)
- [ ] Do not rely on colour alone to convey meaning
- [ ] Provide visible focus indicators on all interactive elements

**Typography & Readability:**
- [ ] Body text minimum 16px
- [ ] Text can be resized up to 200% without loss of content or functionality
- [ ] Line height ≥ 1.5 for body text

**Interaction:**
- [ ] All interactive elements are keyboard-navigable
- [ ] Touch targets are at least 44×44px (WCAG 2.1 AAA / internal best practice; stricter than our AA baseline)
- [ ] No interactions that require fine motor control only (e.g., hover-only)
- [ ] Provide alternatives for time-limited interactions

**Images & Media:**
- [ ] All meaningful images have descriptive `alt` text
- [ ] Decorative images have empty `alt=""` attribute
- [ ] Videos have captions; audio has transcripts

**Forms:**
- [ ] All inputs have visible labels
- [ ] Error messages are clear and programmatically associated
- [ ] Autocomplete attributes are used where appropriate

**Navigation:**
- [ ] Page titles are unique and descriptive
- [ ] Headings follow a logical hierarchy (H1 → H2 → H3)
- [ ] Skip-to-content link is available
- [ ] Focus order is logical and meaningful

**Assistive Technologies:**
- [ ] Tested with screen readers (e.g., NVDA, VoiceOver, TalkBack)
- [ ] ARIA roles and attributes used only when native HTML is insufficient
- [ ] Dynamic content updates are announced to screen readers

---

## 13. UX Research

UX research at Open Food Facts is conducted systematically to ensure design decisions are grounded in user needs.

### 13.1 Research Process

Research follows a structured 14-step process documented in [`UXR Ops/UX Research Process Flow Overview.md`](./UXR%20Ops/UX%20Research%20Process%20Flow%20Overview.md):

1. Identify the research need
2. Stakeholder interview (define goals, metrics, risks)
3. Identify target users
4. Choose research methods
5. Create research plan
6. Recruit participants
7. Create study materials
8. Conduct pilot study
9. Obtain informed consent (GDPR-compliant)
10. Conduct study
11. Analyse data
12. Share report
13. Discuss findings with team
14. Schedule follow-up

### 13.2 Research Methods Used

| Method | Phase | Output |
|---|---|---|
| UX Audit | Foundation | Heuristic issues, improvement areas |
| Heuristic Evaluation | Foundation | Usability violations (Nielsen's 10 principles) |
| Value Proposition Canvas | Foundation | User needs, gains, and pain points |
| User Interviews | Discovery | Proto-personas, JTBD, pain points |
| Survey | Validation | Quantitative JTBD validation, persona data |
| Usability Testing | Evaluation | UX issues, design recommendations |

### 13.3 Research Repository

Research reports are stored in [`UXR Reports Repository/`](./UXR%20Reports%20Repository/) following the naming convention:

```
[YYYY Q] Project Name: Topic
```

Example: `[2025 Q2] Open Prices: Onboarding Flow`

### 13.4 Active Research Areas

- **Open Food Facts (OFF):** General website UX audit — [`UXR OFF/`](./UXR%20OFF/)
- **Open Prices:** UX audit, usability testing, contribution flow research — [`UXR Open Prices/`](./UXR%20Open%20Prices/)

---

## 14. Contributing

We welcome contributions to the design system from designers, developers, and UX researchers.

### Getting started

1. Review the [Contributing Guide](./CONTRIBUTING.md)
2. Request access to [Figma](https://www.figma.com/) (view access by default; edit access on request)
3. Join the [#design channel on Slack](https://slack.openfoodfacts.org)

### Design contribution workflow

1. **Fork & branch** — Create a new branch for your work
2. **Propose in Figma** — Sketch your changes in the relevant Figma file
3. **Open an issue** — Describe the problem and your proposed solution
4. **Pull request** — Submit a PR with your changes (design files, documentation, or assets)
5. **Review** — Request feedback from the design team
6. **Merge** — After approval, your contribution is merged

### Design meetings

**Design team weekly (Fridays 09:00 Paris / 08:00 London / 11:30 IST):**
- Internal design discussions and decisions

**Office hours (Designers, Developers & Community — Fridays 09:00 Paris):**
- Open to everyone; integration of design into the development process

Add events via the [Open Food Facts Community Calendar](https://wiki.openfoodfacts.org/Events).

---

## 15. Resources & Tools

### 15.1 Design files by project

#### Mobile App
[![Figma](https://img.shields.io/badge/figma-%23F24E1E.svg?logo=figma&logoColor=white) Mobile App Design (current + future plans)](https://www.figma.com/file/nFMjewFAOa8c4ahtob7CAB/Mobile-App-Design-(Quentin)?node-id=0%3A1&t=SrBuT7gBdhapUerx-0)
[![Figma](https://img.shields.io/badge/figma-%23F24E1E.svg?logo=figma&logoColor=white) App Store / Play Store Vignettes](https://www.figma.com/file/loMFSX1wJ61jjuZkSeLV7e/Vignettes-App-Design-\(Quentin\)?node-id=3248%3A324)

#### Website
[![Figma](https://img.shields.io/badge/figma-%23F24E1E.svg?logo=figma&logoColor=white) Current Website Design](https://www.figma.com/design/Qg9URUyrjHgYmnDHXRsTTB/Current-Website-design?m=auto&t=jNwvjRR8nIgOzzJZ-6)
[![Figma](https://img.shields.io/badge/figma-%23F24E1E.svg?logo=figma&logoColor=white) Explorer — Next-gen Frontend](https://www.figma.com/design/pgWZAEX1ZoTt0f7Azek4AV/Open-Food-Facts-Explorer-(next-gen-frontend)?node-id=1-53&t=XfEkgmUsvs6qiKr9-0)

#### Open Prices
[![Figma](https://img.shields.io/badge/figma-%23F24E1E.svg?logo=figma&logoColor=white) Open Prices (Web)](https://www.figma.com/design/cIB7CInl2BfueMzWnz09t6/Open-Prices?node-id=0-1&p=f&t=LC7UvPjngw57NGSs-0)
[![Figma](https://img.shields.io/badge/figma-%23F24E1E.svg?logo=figma&logoColor=white) Open Prices (Mobile)](https://www.figma.com/design/nFMjewFAOa8c4ahtob7CAB/Mobile-App-Design--Quentin-?node-id=5816-22697&p=f&t=AkgTM9QzMK7tQeGC-0)
[![Figma](https://img.shields.io/badge/figma-%23F24E1E.svg?logo=figma&logoColor=white) Prixing Benchmark](https://www.figma.com/design/XQYkLGKlcotBPpwKMhDe1z/Prixing---Benchmark?m=auto&t=AkgTM9QzMK7tQeGC-6)

#### Web Tools & Extensions
[![Figma](https://img.shields.io/badge/figma-%23F24E1E.svg?logo=figma&logoColor=white) Taxonomy Editor](https://www.figma.com/file/7QxD2pOnVntjDPqbHHPGHv/Taxonomy-Editor?t=4YadI2GgSAXcPnlo-0)
[![Figma](https://img.shields.io/badge/figma-%23F24E1E.svg?logo=figma&logoColor=white) Hunger Games](https://www.figma.com/design/pngqJwPkytFik6h4EW396n/Hunger-Games?node-id=801-2&p=f&t=xQnrkht1cbTJGOw9-0)
[![Figma](https://img.shields.io/badge/figma-%23F24E1E.svg?logo=figma&logoColor=white) Web Components](https://www.figma.com/design/X8nBndPdBfikAcevBiBxKo/Web-Components?node-id=0-1&p=f&t=A7yCwKqyW9klqYq8-0)
[![Figma](https://img.shields.io/badge/figma-%23F24E1E.svg?logo=figma&logoColor=white) NutriPatrol](https://www.figma.com/design/SRU9iQ5DIpKNa6izKEiqyo/NutriPatrol--quality-?node-id=48-36&p=f&t=Ly2rYxJgs4fcTane-0)
[![Figma](https://img.shields.io/badge/figma-%23F24E1E.svg?logo=figma&logoColor=white) Folksonomy Engine](https://www.figma.com/design/uEtDC3hqIZZeOs6AQAed3D/Folksonomy-Engine--n%C3%A9e-OpenLists-?node-id=614-2&p=f&t=Ly2rYxJgs4fcTane-0)
[![Figma](https://img.shields.io/badge/figma-%23F24E1E.svg?logo=figma&logoColor=white) Search-A-Licious Logo](https://www.figma.com/design/gNnI56OF91Ugdd4fBaq5F8/Search-A-Licious-Logo?m=auto&t=bEHMawF1eequkY9w-6)
[![Figma](https://img.shields.io/badge/figma-%23F24E1E.svg?logo=figma&logoColor=white) DriveOFF (Browser Extension)](https://www.figma.com/design/DHvAhrqU1TBaVkzyTcqXOT/DriveOFF---Chrome-extension-for-shopping?m=auto&t=tdB5zkxiDiU0bMVh-6)

#### Brand & Identity
[![Figma](https://img.shields.io/badge/figma-%23F24E1E.svg?logo=figma&logoColor=white) Open Food Facts Logo](https://www.figma.com/design/HKAAPSQq8CZZO5uAziabRY/New-Open-Food-Facts-logo?m=auto&t=bGdHdz45zaPlgTnW-6)
[![Figma](https://img.shields.io/badge/figma-%23F24E1E.svg?logo=figma&logoColor=white) Illustrations](https://www.figma.com/design/aM6Yu2w3JGBuHTXDHoeUuf/Illustrations?m=auto&t=bGdHdz45zaPlgTnW-6)

---

### 15.2 Asset library (this repository)

| Asset type | Location |
|---|---|
| Open Food Facts logos | `images/logos/openfoodfacts/` |
| Open Beauty Facts logos | `images/logos/openbeautyfacts/` |
| Open Pet Food Facts logos | `images/logos/openpetfoodfacts/` |
| Open Products Facts logos | `images/logos/openproductsfacts/` |
| Open Prices logos | `images/logos/openprices/` |
| Green Score logos | `images/logos/green-score/` |
| UN SDG Goals | `images/logos/un-sdg-goals/` |
| Food illustrations | `images/illustrations/food/` |
| Beauty illustrations | `images/illustrations/beauty/` |
| Pet food illustrations | `images/illustrations/pet-food/` |
| Product illustrations | `images/illustrations/products/` |
| Open Prices illustrations | `images/illustrations/prices/` |
| Shared UI & community illustrations | `images/illustrations/shared/` |
| Rive animations | `animations/` |
| Avatar SVGs | `avatars/svg/` |
| Brand guidelines PDF | `graphic-charter/BRAND GUIDELINES_OFF_V1.pdf` |

---

### 15.3 External links

| Resource | Link |
|---|---|
| Open Food Facts website | [openfoodfacts.org](https://openfoodfacts.org/) |
| Open Food Facts GitHub | [github.com/openfoodfacts](https://github.com/openfoodfacts/) |
| Design Wiki | [wiki.openfoodfacts.org/Design](https://wiki.openfoodfacts.org/Design) |
| Slack #design channel | [slack.openfoodfacts.org](https://slack.openfoodfacts.org) |
| WCAG 2.1 Guidelines | [w3.org/WAI/standards-guidelines/wcag](https://www.w3.org/WAI/standards-guidelines/wcag/) |
| Design Community project | [github.com/orgs/openfoodfacts/projects/76](https://github.com/orgs/openfoodfacts/projects/76) |
| Design System project | [github.com/orgs/openfoodfacts/projects/75](https://github.com/orgs/openfoodfacts/projects/75) |
| UXR & Design backlog | [github.com/orgs/openfoodfacts/projects/11](https://github.com/orgs/openfoodfacts/projects/11) |
| Plus Jakarta Sans font | [fonts.google.com/specimen/Plus+Jakarta+Sans](https://fonts.google.com/specimen/Plus+Jakarta+Sans) |
| Google Stitch DESIGN.md spec | [stitch.withgoogle.com/docs/design-md/overview](https://stitch.withgoogle.com/docs/design-md/overview) |

---

*Last updated: April 2026 — Maintained by the Open Food Facts Design team. Contributions welcome via [GitHub issues](https://github.com/openfoodfacts/openfoodfacts-design/issues) or the [#design Slack channel](https://slack.openfoodfacts.org).*
