from flask import Flask, request, render_template
import csv
import io
import json

from dq import MatchingRule, MasterRecordRule, DuplicateDetector

app = Flask(__name__)

def load_stream(file_storage):
    content = file_storage.stream.read().decode("utf-8")
    if file_storage.filename.endswith(".json"):
        return json.loads(content)
    if file_storage.filename.endswith(".csv"):
        reader = csv.DictReader(io.StringIO(content))
        return list(reader)
    raise ValueError("Unsupported file format")

@app.route("/", methods=["GET", "POST"])
def index():
    results = None
    error = None
    if request.method == "POST":
        try:
            file = request.files["file"]
            match_fields = [f.strip() for f in request.form["match_fields"].split(",") if f.strip()]
            master_field = request.form["master_field"]
            strategy = request.form["strategy"]
            data = load_stream(file)
            matching = MatchingRule(match_fields)
            master_rule = (
                MasterRecordRule.highest(master_field)
                if strategy == "highest"
                else MasterRecordRule.lowest(master_field)
            )
            detector = DuplicateDetector(matching, master_rule)
            results = detector.find_duplicates(data)
        except Exception as exc:  # pragma: no cover - UI feedback
            error = str(exc)
    return render_template("index.html", results=results, error=error)

if __name__ == "__main__":  # pragma: no cover - manual execution
    app.run(debug=True)
