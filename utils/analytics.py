from __future__ import annotations

import os
from datetime import datetime, timezone


def log_learning_event(event_name: str, payload: dict[str, object]) -> None:
    """Best-effort BigQuery event logging for Cloud Run deployments."""
    project_id = os.getenv("GCP_PROJECT_ID", "").strip()
    dataset = os.getenv("BIGQUERY_DATASET", "").strip()
    table = os.getenv("BIGQUERY_EVENTS_TABLE", "").strip()
    if not project_id or not dataset or not table:
        return

    try:
        from google.cloud import bigquery

        client = bigquery.Client(project=project_id)
        table_id = f"{project_id}.{dataset}.{table}"
        row = {
            "event_name": event_name,
            "event_time": datetime.now(timezone.utc).isoformat(),
            "payload": payload,
        }
        client.insert_rows_json(table_id, [row])
    except Exception:
        return
