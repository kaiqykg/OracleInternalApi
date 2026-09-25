import os
import time
from flask import Flask, request, jsonify

from db import get_connection

app = Flask(__name__)

VALID_FORMATS = {"records", "table"}
DEFAULT_FORMAT = "records"


def row_to_dict(row, columns):
    return {columns[i]: row[i] for i in range(len(columns))}


@app.route("/query", methods=["POST"])
def query():
    body = request.get_json(silent=True)
    if not body:
        return jsonify({"success": False, "error": "JSON body obrigatório"}), 400

    sql = body.get("sql")
    if not sql or not sql.strip():
        return jsonify({"success": False, "error": "Campo 'sql' é obrigatório"}), 400

    params = body.get("params", {})
    fmt = body.get("format", DEFAULT_FORMAT)

    if fmt not in VALID_FORMATS:
        return jsonify({
            "success": False,
            "error": f"'format' inválido. Aceitos: {', '.join(sorted(VALID_FORMATS))}"
        }), 400

    start = time.time()
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, params)
                if cur.description:
                    columns = [desc[0] for desc in cur.description]
                    rows = cur.fetchall()
                    elapsed = round((time.time() - start) * 1000, 1)

                    if fmt == "table":
                        return jsonify({
                            "success": True,
                            "format": "table",
                            "totalRows": len(rows),
                            "executionTimeMs": elapsed,
                            "columns": columns,
                            "rows": [list(r) for r in rows]
                        })
                    return jsonify({
                        "success": True,
                        "format": "records",
                        "totalRows": len(rows),
                        "executionTimeMs": elapsed,
                        "data": [row_to_dict(r, columns) for r in rows]
                    })

                elapsed = round((time.time() - start) * 1000, 1)
                return jsonify({
                    "success": True,
                    "format": fmt,
                    "totalRows": 0,
                    "executionTimeMs": elapsed,
                    "data": []
                })

    except Exception as e:
        elapsed = round((time.time() - start) * 1000, 1)
        return jsonify({"success": False, "error": str(e), "executionTimeMs": elapsed}), 500


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)