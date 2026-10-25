import { SITE_URL, rsaVerify, signContent, getConfig } from "./_lib";

export async function onRequestGet(context) {
  const { request, env } = context;
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
