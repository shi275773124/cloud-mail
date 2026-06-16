-- Cloudflare D1 durable capture schema for coffee_shop_opening_kit RFQ validation.
CREATE TABLE IF NOT EXISTS rfq_submissions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  received_at TEXT NOT NULL,
  event TEXT NOT NULL,
  qualified INTEGER NOT NULL DEFAULT 0,
  payload_json TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_rfq_submissions_received_at ON rfq_submissions(received_at);
CREATE INDEX IF NOT EXISTS idx_rfq_submissions_qualified ON rfq_submissions(qualified);
