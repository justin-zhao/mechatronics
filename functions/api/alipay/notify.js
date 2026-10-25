import { rsaVerify, signContent, getConfig, triggerEvents } from "./_lib";

export async function onRequestPost(context) {
  const { request, env } = context;
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
