const GATEWAY = "https://openapi.alipay.com/gateway.do";
const SITE_URL = "https://mechatronics.farflight.cc";

/* ---------------- crypto helpers ---------------- */

function b64ToBytes(b64) {
  const bin = atob(b64);
  const bytes = new Uint8Array(bin.length);
  for (let i = 0; i < bin.length; i++) bytes[i] = bin.charCodeAt(i);
  return bytes;
}

function keyBody(raw) {
  const s = String(raw || "").trim();
  if (s.includes("-----BEGIN")) {
    return s.replace(/-----[^-]+-----/g, "").replace(/\s+/g, "");
  }
  return s.replace(/\s+/g, "");
}

function derLen(n) {
  if (n < 0x80) return [n];
  if (n < 0x100) return [0x81, n];
  return [0x82, (n >> 8) & 0xff, n & 0xff];
}

function pkcs1ToPkcs8(pkcs1) {
  const algId = [0x30, 0x0D, 0x06, 0x09, 0x2A, 0x86, 0x48, 0x86, 0xF7, 0x0D, 0x01, 0x01, 0x01, 0x05, 0x00];
  const octet = [0x04].concat(derLen(pkcs1.length), Array.from(pkcs1));
  const content = [0x02, 0x01, 0x00].concat(algId, octet);
  const seq = [0x30].concat(derLen(content.length), content);
  return new Uint8Array(seq);
}

async function importPrivateKey(raw) {
  const s = String(raw || "").trim();
  const der = b64ToBytes(keyBody(s));
  let pkcs8;
  if (s.includes("BEGIN RSA PRIVATE KEY") || (!s.includes("BEGIN") && der[7] === 0x02)) {
    pkcs8 = pkcs1ToPkcs8(der);
  } else {
    pkcs8 = der;
  }
  return crypto.subtle.importKey(
    "pkcs8", pkcs8,
    { name: "RSASSA-PKCS1-v1_5", hash: "SHA-256" },
    false, ["sign"]
  );
}

async function importPublicKey(raw) {
  const der = b64ToBytes(keyBody(raw));
  return crypto.subtle.importKey(
    "spki", der,
    { name: "RSASSA-PKCS1-v1_5", hash: "SHA-256" },
    false, ["verify"]
  );
}

function signContent(params) {
  return Object.keys(params)
    .filter(function (k) { return k !== "sign" && k !== "sign_type"; })
    .sort()
    .map(function (k) { return k + "=" + params[k]; })
    .join("&");
}

async function rsaSign(content, privateKeyRaw) {
  const key = await importPrivateKey(privateKeyRaw);
  const sig = await crypto.subtle.sign("RSASSA-PKCS1-v1_5", key, new TextEncoder().encode(content));
  const arr = new Uint8Array(sig);
  let bin = "";
  for (let i = 0; i < arr.length; i++) bin += String.fromCharCode(arr[i]);
  return btoa(bin);
}

async function rsaVerify(content, signatureB64, publicKeyRaw) {
  const key = await importPublicKey(publicKeyRaw);
  const sig = b64ToBytes(String(signatureB64 || "").replace(/\s+/g, ""));
  return crypto.subtle.verify("RSASSA-PKCS1-v1_5", key, sig, new TextEncoder().encode(content));
}

function nowBeijing() {
  const fmt = new Intl.DateTimeFormat("en-CA", {
    timeZone: "Asia/Shanghai",
    year: "numeric", month: "2-digit", day: "2-digit",
    hour: "2-digit", minute: "2-digit", second: "2-digit",
    hourCycle: "h23"
  });
  const p = {};
  for (const part of fmt.formatToParts(new Date())) p[part.type] = part.value;
  return p.year + "-" + p.month + "-" + p.day + " " + p.hour + ":" + p.minute + ":" + p.second;
}

function getConfig(env) {
  return {
    appId: env.ALIPAY_APP_ID || env.APP_ID || env.ALIPAY_APPID || "",
    privateKey: env.ALIPAY_PRIVATE_KEY || env.APP_PRIVATE_KEY || env.PRIVATE_KEY || "",
    publicKey: env.ALIPAY_PUBLIC_KEY || env.ALIPAY_ALIPAY_PUBLIC_KEY || ""
  };
}

/* ---------------- payment events ---------------- */

async function triggerEvents(p, env) {
  const details = [
    "=== Alipay Payment Received / 支付宝收款通知 ===",
    "Order No / 订单编号: " + (p.out_trade_no || ""),
    "Trade No / 支付宝交易号: " + (p.trade_no || ""),
    "Amount / 金额: CNY " + (p.total_amount || ""),
    "Status / 状态: " + (p.trade_status || ""),
    "Subject / 商品: " + (p.subject || ""),
    "Buyer / 买家: " + (p.buyer_logon_id || ""),
    "Paid At / 付款时间: " + (p.gmt_payment || "")
  ].join("\n");

  const jobs = [];

  const to = (env.PAYMENT_NOTIFY_EMAIL || "candy78hu@gmail.com").trim();
  jobs.push(
    fetch("https://formsubmit.co/ajax/" + to, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Origin": SITE_URL,
        "Referer": SITE_URL + "/payment.html"
      },
      body: JSON.stringify({
        name: "FarFlight Payment Bot",
        email: to,
        _subject: "[Payment Received] " + (p.out_trade_no || "") + " - CNY " + (p.total_amount || ""),
        message: details,
        _template: "table"
      })
    }).then(function (r) {
      if (!r.ok) throw new Error("email HTTP " + r.status);
    })
  );

  if (env.CALLMEBOT_APIKEY) {
    const phone = String(env.CALLMEBOT_PHONE || "8619860871978").replace(/\D/g, "");
    const text = encodeURIComponent("[FarFlight] Payment received / 收到付款: " + (p.out_trade_no || "") + " CNY " + (p.total_amount || ""));
    jobs.push(
      fetch("https://api.callmebot.com/whatsapp.php?phone=" + phone + "&text=" + text + "&apikey=" + encodeURIComponent(env.CALLMEBOT_APIKEY))
        .then(function (r) {
          if (!r.ok) throw new Error("whatsapp HTTP " + r.status);
        })
    );
  }

  if (env.PAYMENT_WEBHOOK_URL) {
    jobs.push(
      fetch(env.PAYMENT_WEBHOOK_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ type: "alipay.payment.received", params: p })
      }).then(function (r) {
        if (!r.ok) throw new Error("webhook HTTP " + r.status);
      })
    );
  }

  const results = await Promise.allSettled(jobs);
  return results.some(function (r) { return r.status === "fulfilled"; });
}

/* ---------------- API handlers ---------------- */

async function handlePay(request, env) {
  const cfg = getConfig(env);
  if (!cfg.appId || !cfg.privateKey) {
    return Response.json(
      { ok: false, error: "Alipay API is not configured. Set ALIPAY_APP_ID and ALIPAY_PRIVATE_KEY in Cloudflare environment variables (Production)." },
      { status: 500 }
    );
  }

  let data;
  try {
    data = await request.json();
  } catch (e) {
    return Response.json({ ok: false, error: "Invalid JSON body" }, { status: 400 });
  }

  const orderNo = String(data.orderNo || "").trim();
  const amount = Number(data.amount);
  const subject = String(data.subject || "").trim().slice(0, 256);
  const body = String(data.body || "").trim().slice(0, 128);

  if (!/^[A-Za-z0-9_-]{6,64}$/.test(orderNo)) {
    return Response.json({ ok: false, error: "Invalid order number (6-64 chars, letters/digits/-/_)" }, { status: 400 });
  }
  if (!amount || amount < 0.01 || amount > 100000 || isNaN(amount)) {
    return Response.json({ ok: false, error: "Invalid amount (0.01 - 100000 CNY)" }, { status: 400 });
  }
  if (!subject) {
    return Response.json({ ok: false, error: "Missing subject" }, { status: 400 });
  }

  const params = {
    app_id: cfg.appId,
    method: "alipay.trade.page.pay",
    charset: "utf-8",
    sign_type: "RSA2",
    timestamp: nowBeijing(),
    version: "1.0",
    notify_url: SITE_URL + "/api/alipay/notify",
    return_url: SITE_URL + "/api/alipay/return",
    biz_content: JSON.stringify({
      out_trade_no: orderNo,
      product_code: "FAST_INSTANT_TRADE_PAY",
      total_amount: amount.toFixed(2),
      subject: subject,
      body: body
    })
  };

  try {
    params.sign = await rsaSign(signContent(params), cfg.privateKey);
  } catch (e) {
    return Response.json({ ok: false, error: "Signing failed: " + (e && e.message ? e.message : e) }, { status: 500 });
  }

  return Response.json({ ok: true, gateway: GATEWAY, params: params });
}

async function handleNotify(request, env) {
  const cfg = getConfig(env);
  if (!cfg.publicKey) {
    return new Response("failure");
  }

  const params = {};
  try {
    const form = await request.formData();
    for (const entry of form.entries()) {
      if (typeof entry[1] === "string") params[entry[0]] = entry[1];
    }
  } catch (e) {
    return new Response("failure");
  }

  if (!params.sign) return new Response("failure");

  let verified = false;
  try {
    verified = await rsaVerify(signContent(params), params.sign, cfg.publicKey);
  } catch (e) {
    verified = false;
  }
  if (!verified) return new Response("failure");

  const status = params.trade_status || "";
  if (status === "TRADE_SUCCESS" || status === "TRADE_FINISHED") {
    const anySent = await triggerEvents(params, env);
    return new Response(anySent ? "success" : "failure");
  }

  return new Response("success");
}

async function handleReturn(request, env) {
  const url = new URL(request.url);
  const params = {};
  url.searchParams.forEach(function (v, k) { params[k] = v; });

  let ok = false;
  try {
    const cfg = getConfig(env);
    if (cfg.publicKey && params.sign) {
      ok = await rsaVerify(signContent(params), params.sign, cfg.publicKey);
    }
  } catch (e) {
    ok = false;
  }

  const orderNo = params.out_trade_no || "";
  return Response.redirect(
    SITE_URL + "/payment.html?paid=" + (ok ? "1" : "0") + "&order=" + encodeURIComponent(orderNo),
    302
  );
}

/* ---------------- worker entry ---------------- */

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const path = url.pathname;

    if (path === "/api/alipay/pay" && request.method === "POST") return handlePay(request, env);
    if (path === "/api/alipay/notify" && request.method === "POST") return handleNotify(request, env);
    if (path === "/api/alipay/return" && request.method === "GET") return handleReturn(request, env);

    if (path.startsWith("/api/")) {
      return Response.json({ ok: false, error: "Not found" }, { status: 404 });
    }

    const assetRes = await env.ASSETS.fetch(request);
    if (assetRes.status === 404) {
      const nf = await env.ASSETS.fetch(new Request(new URL("/404.html", url).toString()));
      if (nf.status === 200) {
        return new Response(nf.body, {
          status: 404,
          headers: { "Content-Type": "text/html; charset=utf-8" }
        });
      }
    }
    return assetRes;
  }
};
