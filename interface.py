import streamlit as st
import os
import requests
from datetime import datetime
import pandas as pd

# Configuration
st.set_page_config(page_title="Resume Parser", layout="wide")
API_BASE_URL = "http://localhost:8000"  # Update with your FastAPI server URL


# Helper functions
def upload_resume(file):
    try:
        files = {"file": file}
        response = requests.post(f"{API_BASE_URL}/upload_resume", files=files)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Error uploading resume: {str(e)}")
        return None


def get_all_resumes():
    try:
        response = requests.get(f"{API_BASE_URL}/get_resume/")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Error fetching resumes: {str(e)}")
        return []


def get_resume_details(resume_id):
    try:
        response = requests.get(f"{API_BASE_URL}/get_resume_id/{resume_id}")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Error fetching resume details: {str(e)}")
        return None


# Main app
def main():
    st.title("Resume Parser Dashboard")

    tab1, tab2 = st.tabs(["Upload New Resume", "View Past Resumes"])

    with tab1:
        st.header("Upload a New Resume")
        uploaded_file = st.file_uploader(
            "Choose a resume file (PDF, DOCX, DOC, TXT)",
            type=["pdf", "docx", "doc", "txt"]
        )

        if uploaded_file is not None:
            if st.button("Upload and Parse"):
                with st.spinner("Processing resume..."):
                    result = upload_resume(uploaded_file)

                if result:
                    st.success("Resume processed successfully!")
                    with st.expander("View Parsed Data"):
                        st.json(result)

    with tab2:
        st.header("Previously Uploaded Resumes")

        with st.spinner("Loading resumes..."):
            resumes = get_all_resumes()

        if not resumes:
            st.info("No resumes found in database.")
        else:
            # Prepare data for table
            df_data = []
            for resume in resumes:
                created_at = datetime.fromisoformat(resume["created_at"]).strftime("%Y-%m-%d %H:%M")
                df_data.append({
                    "ID": resume["id"],
                    "File Name": resume["file_name"],
                    "Name": resume["name"],
                    "Email": resume["email"],
                    "Phone": resume["phone"],
                    "Uploaded At": created_at,
                })

            df = pd.DataFrame(df_data)

            # Display the table
            st.dataframe(
                df,
                hide_index=True,
                use_container_width=True
            )

            # selectbox for details view
            selected_id = st.selectbox(
                "Select a resume to view details:",
                options=[r["id"] for r in resumes],
                format_func=lambda x: f"Resume ID: {x}",
                index=0
            )

            if selected_id:
                with st.spinner("Loading details..."):
                    details = get_resume_details(selected_id)

                if details:
                    with st.expander(f"Details for Resume ID: {selected_id}"):
                        col1, col2 = st.columns(2)

                        with col1:
                            st.subheader("Basic Information")
                            st.write(f"**File Name:** {details['file_name']}")
                            st.write(f"**Name:** {details['name']}")
                            st.write(f"**Email:** {details['email']}")
                            st.write(f"**Phone:** {details['phone']}")
                            st.write(
                                f"**Uploaded At:** {datetime.fromisoformat(details['created_at']).strftime('%Y-%m-%d %H:%M')}")

                        with col2:
                            st.subheader("Skills")
                            if details['skills']:
                                if isinstance(details['skills'], list):
                                    st.write("**Skills:**")
                                    for skill in details['skills']:
                                        st.write(f"- {skill}")
                                else:
                                    st.write(f"**Skills:** {details['skills']}")
                            else:
                                st.write("No skills listed")

                            st.subheader("Experience")
                            st.write(details['experience'] or "No experience listed")

                        st.subheader("Suggestions")
                        st.write(details['suggestions'] or "No suggestions available")

                        st.subheader("Recommended Skills")
                        if details['recommended_skills']:
                            if isinstance(details['recommended_skills'], list):
                                for skill in details['recommended_skills']:
                                    st.write(f"- {skill}")
                            else:
                                st.write(details['recommended_skills'])
                        else:
                            st.write("No recommended skills")


if __name__ == "__main__":
    main()