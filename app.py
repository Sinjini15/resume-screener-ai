import streamlit as st
import requests

st.title("LLM Resume Matcher")

job_description = st.text_area("Paste the Job Description", height=200)
uploaded_files = st.file_uploader("Upload one or more resumes (PDF)", type="pdf", accept_multiple_files=True)

if st.button("Match"):
    if not job_description or not uploaded_files:
        st.warning("Please provide a job description and at least one resume.")
    else:
        results = []
        for file in uploaded_files:
            files = [('files', (file.name, file.read(), 'application/pdf'))]  # matches FastAPI's 'files' param
            data = {'job_description': job_description}

            try:
                response = requests.post("http://localhost:8000/match", files=files, data=data)
                #st.text(f"Raw response for {file.name}: {response.text}")  # optional: for debugging

                if response.status_code == 200:
                    json_data = response.json()
                    candidates = json_data.get("ranked_candidates", [])
                    if candidates:
                        score = candidates[0].get("match_score", "No score")
                    else:
                        score = "No match found"
                else:
                    score = f"Error ({response.status_code})"
            except Exception as e:
                score = f"Request failed: {e}"

            results.append((file.name, score))

        st.subheader("Match Results")
        for name, score in results:
            st.write(f"{name}: {score}")
