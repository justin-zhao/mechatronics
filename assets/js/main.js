(function () {
  "use strict";

  var $ = function (sel, ctx) { return (ctx || document).querySelector(sel); };
  var $$ = function (sel, ctx) { return Array.prototype.slice.call((ctx || document).querySelectorAll(sel)); };

  /* Mobile nav */
  var navToggle = $(".nav-toggle");
  var mainNav = $("#main-nav");
  if (navToggle && mainNav) {
    navToggle.addEventListener("click", function () {
      navToggle.classList.toggle("open");
      mainNav.classList.toggle("open");
    });
  }

  /* Footer year */
  $$(".js-year").forEach(function (el) { el.textContent = new Date().getFullYear(); });

  /* Product gallery */
  var gallery = $("[data-gallery]");
  if (gallery) {
    var mainImg = $(".main-img img", gallery);
    var mainLink = $(".main-img", gallery);
    var caption = $(".caption", gallery);
    var thumbs = $$(".thumb", gallery);
    thumbs.forEach(function (t) {
      t.addEventListener("click", function () {
        thumbs.forEach(function (x) { x.classList.remove("active"); });
        t.classList.add("active");
        mainImg.src = t.getAttribute("data-full");
        mainLink.setAttribute("data-lightbox", t.getAttribute("data-full"));
        if (caption) caption.textContent = t.getAttribute("data-caption") || "";
      });
    });
  }

  /* Lightbox */
  var lb = $("#lightbox");
  if (lb) {
    var lbImg = $("img", lb);
    var openLb = function (src) { lbImg.src = src; lb.classList.add("open"); document.body.style.overflow = "hidden"; };
    var closeLb = function () { lb.classList.remove("open"); document.body.style.overflow = ""; };
    var lbMain = $("[data-gallery] .main-img");
    if (lbMain) {
      lbMain.addEventListener("click", function () {
        var src = this.getAttribute("data-lightbox") || ($("img", this) || {}).src;
        if (src) openLb(src);
      });
    }
    $(".lb-close", lb).addEventListener("click", closeLb);
    lb.addEventListener("click", function (e) { if (e.target === lb) closeLb(); });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape") closeLb(); });
  }

  /* Products filter */
  var filterBtns = $$(".filter-btn");
  var cards = $$("[data-group]");
  if (filterBtns.length && cards.length) {
    filterBtns.forEach(function (btn) {
      btn.addEventListener("click", function () {
        filterBtns.forEach(function (b) { b.classList.remove("active"); });
        btn.classList.add("active");
        var f = btn.getAttribute("data-filter");
        cards.forEach(function (c) {
          c.style.display = (f === "all" || c.getAttribute("data-group") === f) ? "" : "none";
        });
      });
    });
  }

  /* Enquiry links with product prefill */
  $$("[data-enquire]").forEach(function (el) {
    var name = el.getAttribute("data-enquire");
    var mail = el.getAttribute("data-mail");
    var wa = el.getAttribute("data-wa");
    var href;
    if (el.classList.contains("wa-btn") && wa) {
      href = "https://wa.me/" + wa + "?text=" + encodeURIComponent("Hello, I am interested in " + name + ". Could you please send me a quotation?");
    } else if (mail) {
      href = "mailto:" + mail + "?subject=" + encodeURIComponent("Enquiry: " + name) +
        "&body=" + encodeURIComponent("Hello FarFlight team,\n\nI am interested in the " + name + ".\nPlease send me a quotation and lead-time information.\n\nProduct page: " + location.href + "\n\nName:\nCompany:\nCountry:\nQuantity needed:\n");
    }
    if (href) el.setAttribute("href", href);
  });

  /* Contact form -> FormSubmit (direct email delivery) */
  var contactForm = $("#contact-form");
  if (contactForm) {
    var showStatus = function (html, cls) {
      var st = $("#form-status");
      if (!st) return;
      st.className = "form-status show" + (cls ? " " + cls : "");
      $("#form-status-text").innerHTML = html;
      st.scrollIntoView({ behavior: "smooth", block: "center" });
    };
    var restoreBtn = function () {
      var btn = $("#cf-submit");
      if (btn) { btn.disabled = false; btn.style.opacity = ""; }
    };
    var fallbackHtml = function (to, wa) {
      return "<strong>Automatic sending failed.</strong> Please try again, " +
        'email us directly at <a href="mailto:' + to + '">' + to + "</a> " +
        '(opens your mail app, e.g. Outlook), or chat on <a href="https://wa.me/' + wa + '" target="_blank" rel="noopener">WhatsApp</a>.';
    };
    contactForm.addEventListener("submit", function (e) {
      e.preventDefault();
      var to = contactForm.getAttribute("data-mail");
      var wa = contactForm.getAttribute("data-wa");
      var name = $("#cf-name").value.trim();
      var email = $("#cf-email").value.trim();
      var subject = $("#cf-subject").value.trim() || "Website enquiry";
      var message = $("#cf-message").value.trim();
      if (!name || !email || !message) { alert("Please fill in your name, email and message."); return; }
      var btn = $("#cf-submit");
      if (btn) { btn.disabled = true; btn.style.opacity = "0.6"; }
      showStatus("Sending your message…", "");
      fetch("https://formsubmit.co/ajax/" + to, {
        method: "POST",
        headers: { "Content-Type": "application/json", "Accept": "application/json" },
        body: JSON.stringify({
          name: name,
          email: email,
          _subject: subject,
          message: message,
          _template: "table",
          _captcha: "false"
        })
      }).then(function (r) {
        return r.json().then(function (d) { return { ok: r.ok, d: d }; });
      }).then(function (res) {
        if (res.ok && (res.d.success === "true" || res.d.success === true)) {
          showStatus("<strong>✓ Message sent successfully!</strong> Thank you, " + name + ". We have received your message and will reply to <strong>" + email + "</strong> within 24 hours.", "ok");
          contactForm.reset();
        } else {
          showStatus(fallbackHtml(to, wa), "err");
        }
        restoreBtn();
      }).catch(function () {
        showStatus(fallbackHtml(to, wa), "err");
        restoreBtn();
      });
    });
  }

  /* Payment order form */
  var orderForm = $("#order-form");
  if (orderForm) {
    var productSel = $("#of-product");
    var params = new URLSearchParams(location.search);
    var pre = params.get("product");
    if (pre && productSel) {
      $$("option", productSel).forEach(function (o) {
        if (o.value === pre) productSel.value = pre;
      });
    }

    var genBtn = $("#gen-order");
    var summary = $("#order-summary");
    var onumEl = $("#order-number");

    var genOrderNo = function () {
      var d = new Date();
      var pad = function (n) { return (n < 10 ? "0" : "") + n; };
      var rnd = Math.floor(1000 + Math.random() * 9000);
      return "FF-" + d.getFullYear() + pad(d.getMonth() + 1) + pad(d.getDate()) + "-" + rnd;
    };

    var collect = function () {
      var opt = productSel && productSel.selectedOptions ? productSel.selectedOptions[0] : null;
      var pname = opt ? (opt.getAttribute("data-name") || opt.textContent) : "";
      return {
        product: pname,
        model: $("#of-model").value.trim(),
        qty: $("#of-qty").value,
        name: $("#of-name").value.trim(),
        contact: $("#of-contact").value.trim(),
        note: $("#of-note").value.trim()
      };
    };

    var valid = function (o) {
      if (!o.product) { alert("Please select a product / 请选择商品"); return false; }
      if (!o.qty || o.qty < 1) { alert("Please enter a quantity / 请填写数量"); return false; }
      if (!o.name) { alert("Please enter your name / 请填写您的姓名"); return false; }
      if (!o.contact) { alert("Please enter your contact (email / WhatsApp / phone) / 请填写联系方式"); return false; }
      return true;
    };

    var noteText = function (o, num) {
      return "Order " + num + " | " + o.product + (o.model ? " model " + o.model : "") + " x" + o.qty + " | " + o.name + " | " + o.contact;
    };

    if (genBtn) {
      genBtn.addEventListener("click", function () {
        var o = collect();
        if (!valid(o)) return;
        var num = genOrderNo();
        onumEl.textContent = num;
        $("#sum-product").textContent = o.product;
        $("#sum-model").textContent = o.model || "-";
        $("#sum-qty").textContent = o.qty;
        $("#sum-name").textContent = o.name;
        $("#sum-contact").textContent = o.contact;
        $("#sum-note").textContent = noteText(o, num);
        summary.classList.add("show");
        summary.scrollIntoView({ behavior: "smooth", block: "center" });

        var text = noteText(o, num);
        var mailto = $("#confirm-mail");
        var wame = $("#confirm-wa");
        var mail = orderForm.getAttribute("data-mail");
        var wa = orderForm.getAttribute("data-wa");
        mailto.setAttribute("href", "mailto:" + mail +
          "?subject=" + encodeURIComponent("Payment confirmation - " + num) +
          "&body=" + encodeURIComponent("Hello FarFlight team,\n\nI have completed the payment for:\n\nOrder number: " + num +
            "\nProduct: " + o.product + "\nModel: " + (o.model || "-") + "\nQuantity: " + o.qty +
            "\nMy name: " + o.name + "\nMy contact: " + o.contact +
            "\nPayment note used: " + text + "\n\nPlease confirm receipt and delivery details.\n\n" + o.note));
        wame.setAttribute("href", "https://wa.me/" + wa + "?text=" + encodeURIComponent(
          "Hello FarFlight, I have paid. " + text));
        mailto.style.display = "";
        wame.style.display = "";
      });
    }

    var copyBtn = $("#copy-order");
    if (copyBtn) {
      copyBtn.addEventListener("click", function () {
        var o = collect();
        var num = onumEl.textContent;
        if (!num || num === "—") return;
        var text = noteText(o, num);
        var done = function () { copyBtn.textContent = "Copied ✓"; setTimeout(function () { copyBtn.textContent = "Copy payment note"; }, 2000); };
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(text).then(done);
        } else {
          var ta = document.createElement("textarea");
          ta.value = text; document.body.appendChild(ta); ta.select();
          try { document.execCommand("copy"); done(); } catch (err) {}
          document.body.removeChild(ta);
        }
      });
    }
  }

  /* Back to top */
  var toTop = $("#to-top");
  if (toTop) {
    window.addEventListener("scroll", function () {
      toTop.classList.toggle("show", window.scrollY > 500);
    });
    toTop.addEventListener("click", function () { window.scrollTo({ top: 0, behavior: "smooth" }); });
  }
})();
