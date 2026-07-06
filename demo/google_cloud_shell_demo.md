# Google Cloud Shell Demo Path

Use this path when Cloud Run billing activation is unavailable but a Google Cloud-based live demo is still needed.

## Why This Alternate Exists

AccessPrep AI is production-ready for Google Cloud Run through `Dockerfile`, `cloudbuild.yaml`, and `cloudrun-service.yaml`.

Google Cloud Run deployment requires billing to be linked because Cloud Build and Artifact Registry must be activated. When billing cannot be enabled for a hackathon account, Google Cloud Shell Web Preview is the recommended no-payment live demo path.

## What This Demonstrates

This alternate still runs the application inside Google Cloud infrastructure:

- Google Cloud Shell compute environment
- Streamlit web server on port `8080`
- Cloud Shell Web Preview URL
- Same GitHub repository and same application code
- Offline demo fallback when Gemini or Vision credentials are not configured

## Steps

Open Google Cloud Shell and run:

```bash
cd ~
rm -rf accessprep-ai
git clone https://github.com/kaaviya-ai/accessprep-ai.git
cd accessprep-ai
python3 -m pip install --user -r requirements.txt
python3 -m streamlit run app.py --server.port 8080 --server.address 0.0.0.0 --server.headless true
```

Then open:

```text
Cloud Shell Web Preview -> Preview on port 8080
```

Keep the Cloud Shell terminal running while presenting the demo.

## Demo Notes

- Use `demo/sample_exam_upload.png` or `demo/sample_exam_upload_text.pdf` on the Upload page.
- If cloud credentials are not configured, the app uses offline demo OCR and AI fallback responses.
- The full Cloud Run deployment path remains documented in `README.md`.

## Submission Statement

AccessPrep AI is designed for Google Cloud Run with Cloud Build, Artifact Registry, Vision API, Gemini, Vertex AI readiness, and optional BigQuery analytics. For the live hackathon demo, Google Cloud Shell Web Preview can be used as a no-billing Google Cloud execution environment when billing activation is unavailable.
