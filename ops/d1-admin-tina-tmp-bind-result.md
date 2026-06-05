# D1 admin Tina tmp bind result

- run_at_utc: 2026-06-05T21:26:49Z
- target: active `tmp-* @chrisshi168.dpdns.org` mailboxes from `user_id=1` to Tina `user_id=2`
- workflow: self-deleting one-shot

```json
├ Checking if file needs uploading
│
├ 🌀 Uploading 9f014d98-a910-4ea7-8e4b-9d0581889d0c.00ffb5ee8ccff8f1.sql
│ 🌀 Uploading complete.
│
[
  {
    "results": [
      {
        "Total queries executed": 4,
        "Rows read": 108,
        "Rows written": 14,
        "Database size (MB)": "2.10"
      }
    ],
    "success": true,
    "finalBookmark": "000000c5-00000006-00005081-eaa4022cbf751d42b5904ed69a8b5293",
    "meta": {
      "served_by": "v3-prod",
      "served_by_region": "APAC",
      "served_by_colo": "NRT",
      "served_by_primary": true,
      "timings": {
        "sql_duration_ms": 2.9017
      },
      "duration": 2.9017,
      "changes": 15,
      "last_row_id": 0,
      "changed_db": true,
      "size_after": 2097152,
      "rows_read": 108,
      "rows_written": 14,
      "num_tables": 12,
      "total_attempts": 1
    }
  }
]
```
