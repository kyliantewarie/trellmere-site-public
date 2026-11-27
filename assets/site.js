/* Shared storefront behaviour — product cards, buy buttons, marketplace links, nav. */
(function () {
  "use strict";

  const products = window.TRELLMERE_PRODUCTS || [];
  const config = window.TRELLMERE_CONFIG || {};

  function esc(s) {
    return String(s == null ? "" : s)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;").replace(/'/g, "&#39;");
  }

  function buyButton(p, cls) {
    const klass = "btn btn-primary " + esc(cls || "");
    if (p.published === false) {
      // Permalinks are kept in products.js but must not be presented as a
      // checkout link while the listing is unpublished (CRA gates closed).
      return '<span class="' + klass + ' is-disabled" ' +
        'title="Listing unpublished — pending CRA gates">Unavailable — pending republish</span>' +
        '<span class="not-configured">Checkout opens when the listing is republished</span>';
    }
    return '<a class="' + klass + '" href="' + esc(p.buyUrl) + '" rel="noopener">Buy now →</a>';
  }

  function cardHtml(p) {
    const tags = (p.tags || []).map(function (t) { return '<span class="tag">' + esc(t) + "</span>"; }).join("");
    const badge = p.badge ? '<span class="badge">' + esc(p.badge) + "</span>" : "";
    const thumb = p.thumb
      ? '<img class="card-thumb" src="' + esc(p.thumb) + '" alt="' + esc(p.name) + ' product image" loading="lazy">' +
        ''
      : '<div class="card-thumb card-thumb-empty" aria-hidden="true">' + esc((p.name || "?").charAt(0)) + '</div>';

    return '' +
      '<article class="card accent-' + esc(p.accent || "amber") + '">' +
        thumb +
        '<div class="card-top">' +
          '<span class="card-cat">' + esc(p.category) + "</span>" + badge +
        "</div>" +
        '<h3><a href="' + esc(p.url) + '">' + esc(p.name) + "</a></h3>" +
        '<p class="tagline">' + esc(p.tagline) + "</p>" +
        '<p class="summary">' + esc(p.summary) + "</p>" +
        '<div class="tags">' + tags + "</div>" +
        '<div class="card-foot">' +
          '<div class="price">' + esc(p.price) + "<small>" + esc(p.priceNote) + "</small></div>" +
          '<a class="btn btn-ghost btn-sm" href="' + esc(p.url) + '">Details</a>' +
        "</div>" +
      "</article>";
  }

  function renderGrids() {
    document.querySelectorAll("[data-product-grid]").forEach(function (el) {
      const filter = el.getAttribute("data-product-grid");
      let list = products;
      if (filter === "featured") {
        list = products.filter(function (p) { return p.featured; });
      } else if (filter && filter !== "all") {
        list = products.filter(function (p) { return p.tags.indexOf(filter) !== -1 || p.category.toLowerCase().indexOf(filter) !== -1; });
      }
      el.innerHTML = list.map(cardHtml).join("");
    });
  }

  function marketplaceButton(p) {
    const klass = "btn btn-ghost btn-block";
    if (!p.marketplaceUrl) {
      return '<span class="' + klass + ' is-disabled" title="Submitted for review">Superhive — pending approval</span>' +
        '<span class="not-configured">Marketplace review in progress</span>';
    }
    return '<a class="' + klass + '" href="' + esc(p.marketplaceUrl) + '" rel="noopener">Get it on Superhive →</a>';
  }

  function renderBuySlots() {
    document.querySelectorAll("[data-buy-for]").forEach(function (el) {
      const p = products.find(function (x) { return x.id === el.getAttribute("data-buy-for"); });
      if (p) el.innerHTML = buyButton(p, el.getAttribute("data-btn-class") || "");
    });
    document.querySelectorAll("[data-marketplace-for]").forEach(function (el) {
      const p = products.find(function (x) { return x.id === el.getAttribute("data-marketplace-for"); });
      if (p) el.innerHTML = marketplaceButton(p);
    });
  }

  function renderStoreLinks() {
    document.querySelectorAll("[data-store-link]").forEach(function (el) {
      if (config.storeUrl) {
        el.setAttribute("href", config.storeUrl);
        el.classList.remove("is-disabled");
      } else {
        el.setAttribute("title", "Set storeUrl in assets/products.js");
        el.classList.add("is-disabled");
      }
    });
  }

  function setActiveNav() {
    const here = location.pathname.replace(/^\//, "").replace(/^trellmere-site\//, "") || "index.html";
    document.querySelectorAll("[data-nav]").forEach(function (a) {
      const target = a.getAttribute("data-nav");
      const active = target === here
        || (here.startsWith("products/") && target === "catalog.html")
        || (here.startsWith("guides/") && target === "guides/index.html");
      if (active) a.classList.add("active");
    });
  }

  function setYear() {
    document.querySelectorAll("[data-year]").forEach(function (el) { el.textContent = new Date().getFullYear(); });
  }

  document.addEventListener("DOMContentLoaded", function () {
    renderGrids();
    renderBuySlots();
    renderStoreLinks();
    setActiveNav();
    setYear();
  });
})();
