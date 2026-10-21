# ☕ Brew Haven — Artisan Coffee Cafe

A single-file, fully self-contained coffee cafe website built with HTML, CSS, and
vanilla JavaScript. It blends rich coffee aesthetics with modern interactions —
a full-screen "visor" layout, animated content, a custom crosshair cursor, and a
working order & payment flow that records orders and exports them to Excel.

Everything (styles, scripts, and all images) is embedded in **`index.html`**, so
the site works offline — no build step, no server, no internet required.

---

## 🚀 Getting Started

Just open the file in any modern browser:

```
index.html
```

Double-click it, or serve the folder with any static server if you prefer:

```bash
# optional — any of these work
python3 -m http.server 8000
# then visit http://localhost:8000
```

> No dependencies, no installation. The Google Fonts link is the only remote
> resource; without internet the site falls back to system fonts (layout and
> images still work, since images are embedded).

---

## ✨ Features

### Design & Layout
- **Full-page "visor" snap mode** — each section (Hero, Showcase, About, Features,
  Menu, Gallery, Quote, Contact) fills the screen and snaps into place one at a time.
- **Fully responsive** across laptop, tablet, and mobile using dynamic viewport
  heights (`dvh`) so panels fill the real visible screen.
- **Blurred hero background** with crisp foreground text.
- **Silk mesh lettering** on the hero headline — a flowing gradient that ripples
  like silk in a breeze and billows on hover/touch.
- **3D letter-swap logo** — the navbar logo letters flip on hover.

### Interactions
- **Crosshair cursor** that tracks the pointer and **locks onto** links/buttons
  with a highlight frame.
- **Glow line trail** following the cursor — white over dark backgrounds, dark
  over light sections.
- **Animated content** — elements fade/slide in as they scroll into view.
- **Scroll-expand showcase** panel that grows to full-bleed when it enters view.
- **Count-up stats** in the About section that animate `0 → target` every time the
  section scrolls into view, and reset when it leaves.

### Ordering & Payment
- **Add-to-cart** buttons on every menu item (prices in ₹ INR).
- **Floating cart** with a live item count.
- **Checkout modal** showing the order summary (name + quantity per item),
  a running total, a customer name field, and payment methods: **UPI** and
  **Cash on Delivery**.
- **Order confirmation** with the items, name, total, and chosen payment method.

### 📊 Orders → Excel
Every placed order is saved in the browser (via `localStorage`) and accumulates
across orders. From the confirmation screen, click **“Export Orders to Excel”** to
download a single spreadsheet containing **all** recorded orders.

The exported file (`BrewHaven-Orders-<timestamp>.xls`) opens directly in Microsoft
Excel / LibreOffice / Google Sheets, with one row per order and these columns:

| Order # | Date & Time | Customer | Items | Total Qty | Total (INR) | Payment Method |
|---------|-------------|----------|-------|-----------|-------------|----------------|

**Notes**
- Orders persist in the browser they were placed in until you clear browser data.
- Because this is a static front-end site, orders are stored locally and exported
  on demand (no server-side database).

---

## 📁 Project Structure

```
coffee_store_website/
├── index.html      # the entire self-contained site (HTML + CSS + JS + images)
└── README.md       # this file
```

---

## ♿ Accessibility & Preferences
- Respects `prefers-reduced-motion` — animations, the custom cursor, and the silk
  ripple are disabled for users who opt out.
- The custom cursor only activates on fine-pointer (mouse) devices; touch devices
  keep the native behavior.

---

## 🛠️ Tech
- Plain **HTML5**, **CSS3**, and **vanilla JavaScript** — no frameworks.
- Images embedded as base64 **data-URIs** for full offline support.
- Excel export via native **SpreadsheetML (.xls)** XML — no external libraries.

---

_Brewed with ❤️ and plenty of caffeine._
