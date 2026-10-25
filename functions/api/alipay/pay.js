import { GATEWAY, SITE_URL, rsaSign, signContent, nowBeijing, getConfig } from "./_lib";

export async function onRequestPost(context) {
  const { request, env } = context;
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
