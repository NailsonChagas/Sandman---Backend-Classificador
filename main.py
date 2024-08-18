from flask import Flask, request, jsonify
import uuid

app = Flask(__name__)
jobs = {}

@app.route("/classifier/exam", methods=["POST"])
def send_exam():
    data: dict = request.get_json()
    eeg_reading = data.get("eeg_reading")
    
    job_id = str(uuid.uuid4())
    
    jobs[job_id] = {
        "eeg_reading": eeg_reading,
        "classified": False,
        "classified_eeg_reading": None,
        "plots": {
            "eeg_reading_plot": None,
            "classified_eeg_reading_plot": None,
            "sleep_stages_distribution_plot": None
        }
    }
    
    return jsonify({"job_id": job_id})

@app.route("/classifier/exam/<job_id>", methods=["GET"])
def get_exam(job_id):
    job = jobs.get(job_id)
    
    if not job:
        return jsonify({"error": "Job not found"}), 404
    
    return jsonify({
        "done": job["classified"],
        "classified_eeg_reading": job["classified_eeg_reading"],
        "eeg_reading_plot": job["plots"]["eeg_reading_plot"],
        "classified_eeg_reading_plot": job["plots"]["classified_eeg_reading_plot"],
        "sleep_stages_distribution_plot": job["plots"]["sleep_stages_distribution_plot"]
    })

@app.route("/classifier/generate_report", methods=["POST"])
def generate_report():
    data: dict = request.get_json()
    job_id = data.get("job_id")
    notes = data.get("notes")
    
    job = jobs.get(job_id)
    
    if not job: return jsonify({"error": "Job not found"}), 404
    if not job["classified"]: return jsonify({"error": "Classification not completed"}), 404
    
    report_pdf = "Simulated PDF content in Base64: " + notes

    return jsonify({"report_pdf": report_pdf})

if __name__ == "__main__":
    app.run(debug=True)