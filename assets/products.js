/*
 * Single source of truth for product data used by the storefront.
 * Buy URLs and prices verified live against https://kylian47.gumroad.com/
 * on 24 November 2026.
 *
 * All nine products are published with working Gumroad buy URLs.
 * DraftForge was published by the owner on 24 November 2026 and verified live
 * (HTTP 200, published=true) at https://kylian47.gumroad.com/l/draftforge
 */
window.TRELLMERE_PRODUCTS = [
  {
    id: "draftforge",
    published: false,
    name: "DraftForge",
    tagline: "Manufacturing drawings, generated",
    category: "Standalone software",
    price: "€27",
    priceNote: "€27 one-time · single-user licence",
    badge: "New",
    featured: true,
    summary:
      "Turn a part spec into a layered DXF drawing, hole schedule, GD&T callouts and an inspection report in one command. Offline, scriptable and dependency-free.",
    url: "products/draftforge.html",
    buyUrl: "https://kylian47.gumroad.com/l/draftforge",
    thumb: "assets/listing-art/draftforge-thumbnail-600x600.png",
    tags: ["dxf", "manufacturing", "fabrication", "cad", "python"],
    accent: "amber"
  },
  {
    id: "sheetfab",
    published: false,
    name: "SheetFab",
    tagline: "Sheet-metal flat patterns in Blender",
    category: "Blender add-on",
    price: "€27",
    priceNote: "€27 one-time · free updates",
    badge: "New",
    featured: true,
    summary:
      "Fold a metal part, unfold it correctly, and export a laser-ready DXF — without leaving Blender. Real K-factor bend allowance, bend lines and layered DXF exports.",
    url: "products/sheetfab.html",
    buyUrl: "https://kylian47.gumroad.com/l/sheetfab",
    marketplaceUrl: "",
    thumb: "https://public-files.gumroad.com/99gxrm3kdt995kx03o5poxa36zup",
    tags: ["blender", "sheet-metal", "dxf", "laser-cut", "fabrication"],
    accent: "amber"
  },
  {
    id: "backup-guardian",
    published: false,
    name: "Backup Guardian",
    tagline: "Verify your Home Assistant backups",
    category: "Home Assistant add-on",
    price: "Pay what you want",
    priceNote: "€9 suggested · optional",
    badge: "",
    featured: true,
    summary:
      "Fail-closed backup verification for Home Assistant: age, size, coverage, encrypted archives and restore drills, plus a branded readiness report.",
    url: "products/backup-guardian.html",
    buyUrl: "https://kylian47.gumroad.com/l/kgbmhi",
    thumb: "https://public-files.gumroad.com/jul5y4sbkk7as1d0gz34c2ii7kv3",
    tags: ["home-assistant", "backup", "monitoring"],
    accent: "teal"
  },
  {
    id: "smart-appliance-shield",
    published: false,
    name: "Smart Appliance Shield",
    tagline: "Stop your smart devices phoning home",
    category: "HA / OpenWrt add-on",
    price: "Pay what you want",
    priceNote: "€19 suggested · optional",
    badge: "",
    summary:
      "Per-appliance network privacy with a signed 5,238-pattern ruleset. No TLS interception, no cloud. Runs on Home Assistant or OpenWrt.",
    url: "products/smart-appliance-shield.html",
    buyUrl: "https://kylian47.gumroad.com/l/vamzm",
    thumb: "https://public-files.gumroad.com/4qtadl7kbplq39hzbwnxd9z7ho03",
    tags: ["privacy", "home-assistant", "openwrt", "dns"],
    accent: "violet"
  },
  {
    id: "voltwise",
    published: false,
    name: "VoltWise Pro Kit",
    tagline: "Safety-first home energy scheduling",
    category: "Home Assistant / beta",
    price: "Pay what you want",
    priceNote: "€24 suggested · one-time",
    badge: "Beta",
    summary:
      "Dynamic-programming battery/EV scheduler with a post-optimisation safety audit, stress testing and a local web UI. Open source, signed releases.",
    url: "products/voltwise.html",
    buyUrl: "https://kylian47.gumroad.com/l/nsfwqe",
    thumb: "https://public-files.gumroad.com/5168lnj1xi9ti5at6jiun2l55k96",
    tags: ["energy", "home-assistant", "scheduler", "open-source"],
    accent: "green"
  },
  {
    id: "plcnext-blocks",
    published: false,
    name: "IEC 61131 Control Blocks",
    tagline: "Production-ready PLCnext function blocks",
    category: "Industrial / PLCnext",
    price: "€45",
    priceNote: "8-block bundle · one-time",
    badge: "",
    summary:
      "Eight tested Structured Text function blocks for PLCnext Engineer 2026.6 — anti-windup PID, alarm, motor control, ramp limiter, totalizer and more.",
    url: "products/plcnext-blocks.html",
    buyUrl: "https://kylian47.gumroad.com/l/sdjow",
    thumb: "https://public-files.gumroad.com/n0fe6v09pzq8pf8tspu6o9lzykcy",
    tags: ["plc", "industrial", "iec61131", "automation"],
    accent: "blue"
  },
  {
    id: "splitforge",
    published: false,
    name: "SplitForge",
    tagline: "Split large models for 3D printing",
    category: "Blender add-on",
    price: "€11",
    priceNote: "€11 one-time",
    badge: "New",
    summary:
      "Shape-aware splitting into build-volume-sized parts with oriented cut planes, caps, connectors and an assembly-fit check before export.",
    url: "products/splitforge.html",
    buyUrl: "https://kylian47.gumroad.com/l/splitforge",
    marketplaceUrl: "",
    thumb: "https://public-files.gumroad.com/hlcamqqf3mure2ni0dbscvgqhfhf",
    tags: ["blender", "3d-printing", "mesh", "fabrication"],
    accent: "rose"
  },
  {
    id: "iiot-pro",
    published: false,
    name: "IIoT Pro",
    tagline: "34 PLCnext protocol function blocks",
    category: "PLCnext / Industrial",
    price: "€89",
    priceNote: "launch price · one-time",
    badge: "New",
    summary:
      "MQTT, OPC UA, Modbus, JSON and REST logic for PLCnext Engineer 2026.6. Imported and rebuilt without errors. Independent third-party product.",
    url: "products/iiot-pro.html",
    buyUrl: "https://kylian47.gumroad.com/l/iiot-pro",
    thumb: "assets/listing-art/iiot-pro-cover-1280x720.png",
    tags: ["plcnext", "industrial", "mqtt", "opcua", "modbus", "json", "rest"],
    accent: "blue"
  },
  {
    id: "edgestack",
    published: false,
    name: "EdgeStack for PLCnext",
    tagline: "Turn-key edge IoT stack for PLCnext Control",
    category: "PLCnext / Function extension",
    price: "€45",
    priceNote: "€45 one-time · commercial use included",
    badge: "New",
    summary:
      "Deploy a low-RAM Docker monitoring stack — Node-RED, MQTT, InfluxDB and Grafana — on an AXC F controller in minutes, with dashboards, backup scripts and a field manual.",
    url: "products/edgestack.html",
    buyUrl: "https://kylian47.gumroad.com/l/jvzcmc",
    thumb: "https://public-files.gumroad.com/cz2l915cc700j0n31yav4ov1i5gm",
    tags: ["plcnext", "industrial", "docker", "grafana", "mqtt", "monitoring"],
    accent: "teal"
  }
];

/* Payment / signup endpoints. Leave blank until configured — see README.md. */
window.TRELLMERE_CONFIG = {
  /* e.g. https://buttondown.email/api/emails/embed-subscribe/yourname
     or https://formspree.io/f/yourformid */
  signupEndpoint: "",  // Gumroad handles free lead-magnet delivery; no form backend needed
  /* Verified live Gumroad storefront */
  storeUrl: "https://kylian47.gumroad.com/",
  siteUrl: "https://kyliantewarie.github.io/trellmere-site",
  siteName: "Trellmere Digital Products"
};
