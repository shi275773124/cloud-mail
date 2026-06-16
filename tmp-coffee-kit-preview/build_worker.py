from pathlib import Path
import json
html = Path("tmp-coffee-kit-preview/index.html").read_text(encoding="utf-8")
html = html.replace("const RFQ_ENDPOINT = window.RFQ_ENDPOINT || '/api/rfq';", "const RFQ_ENDPOINT = '/api/rfq';")
worker = """const HTML = __HTML_JSON__;

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const corsHeaders = {
      "Access-Control-Allow-Origin": env.ALLOWED_ORIGIN || "*",
      "Access-Control-Allow-Methods": "GET,POST,OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type",
    };

    if (request.method === "OPTIONS") return new Response(null, { status: 204, headers: corsHeaders });
    if (url.pathname === "/health") return json({ ok: true, service: "coffee-kit-rfq-preview", received_at: new Date().toISOString() }, corsHeaders);
    if ((url.pathname === "/" || url.pathname === "/custom-coffee-shop-opening-kit" || url.pathname === "/index.html") && request.method === "GET") {
      return new Response(HTML, { headers: { "Content-Type": "text/html; charset=utf-8", "Cache-Control": "no-store" } });
    }
    if (url.pathname !== "/api/rfq" || request.method !== "POST") return json({ ok: false, error: "not_found" }, corsHeaders, 404);

    let payload;
    try { payload = await request.json(); } catch (error) { return json({ ok: false, error: "invalid_json" }, corsHeaders, 400); }
    const required = ["name", "email", "country", "shop_type", "quantity", "components"];
    const missing = required.filter((key) => !payload[key] || (Array.isArray(payload[key]) && payload[key].length === 0));
    const receivedAt = new Date().toISOString();
    const record = {
      event: "rfq_submit", received_at: receivedAt,
      source: payload.source || "direct_or_unknown",
      utm_source: payload.utm_source || null, utm_medium: payload.utm_medium || null, utm_campaign: payload.utm_campaign || null,
      page_slug: payload.page_slug || "/custom-coffee-shop-opening-kit",
      validation: { missing, qualified: missing.length === 0 },
      user_agent: request.headers.get("User-Agent") || "", referer: request.headers.get("Referer") || "", payload,
    };
    if (!env.DB) return json({ ok: false, error: "d1_not_bound" }, corsHeaders, 500);
    await env.DB.prepare("INSERT INTO rfq_submissions (received_at, event, qualified, payload_json) VALUES (?1, ?2, ?3, ?4)")
      .bind(receivedAt, "rfq_submit", missing.length === 0 ? 1 : 0, JSON.stringify(record)).run();
    return json({ ok: true, qualified: missing.length === 0, missing, received_at: receivedAt }, corsHeaders);
  }
};
function json(payload, extraHeaders = {}, status = 200) {
  return new Response(JSON.stringify(payload), { status, headers: { "Content-Type": "application/json; charset=utf-8", ...extraHeaders } });
}
""".replace("__HTML_JSON__", json.dumps(html))
Path("tmp-coffee-kit-preview/worker.js").write_text(worker, encoding="utf-8")
