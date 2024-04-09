from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import os
import google.generativeai as genai

#genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

def get_gemini_response(cv, job_desc, prompt):
  model = genai.GenerativeModel('gemini-pro')
  response = model.generate_content([cv, job_desc, prompt])
  return response.text

def get_gemini_response_job_desc(job_desc, prompt):
  model = genai.GenerativeModel("gemini-pro")
  response = model.generate_content([job_desc, prompt])
  return response.text

# Streamlit App  
st.set_page_config(page_title='ATS Checker')
st.header('📑 CV Optimization 🔝')
jobdesc_txt = st.text_area(label="Job Description")
cv_txt = st.text_area(label="CV")

col1, col2, col3, col4 = st.columns(4)
with col1:
  submit1 = st.button('Review')
  
with col2:
  submit2 = st.button('Percentage Match')
  
with col3:
  submit3 = st.button("Find Keyword")
  
with col4:
  submit4 = st.button("Make Cover Letter")

input_prompt1 = """anda adalah HR yang sudah banyak memiliki pengalaman, tugas kamu adlaah mereview isi cv yang diberikan terhadap job description. berikan evaluasi anda terhadap kandidat ini, apakah profil kandidat berdasarkan cv ini cocok dengan pekerjaan yang diposting, highlight apa yang menjadi kelebihan dan kekurangan cv kandidat terhadap job deskripsi ini"""

input_prompt2 =  """anda adalah ATS (Applicant Tracking System) scanner dengan pemahaman yang mendalam tentang ATS, tugas anda adalah mengevaluasi CV terhadap job description yang diberikan. berikan persentase kecocokan cv ini dengan job description, berikan pendapat anda apa yang perlu dilakukan agar nilai presentasi ini bertambah
"""

input_prompt3 = """anda adalah seorang HR dengan pengalaman dibidang mencari keyword pada job description yang diberikan, tugas anda mencari keyword yang ada pada job descrition yang diberikan"""

input_prompt4 = """anda adalah orang yang memiliki banyak pengalaman dalam pembuatan cover letter untuk menacari kerja, tugas anda adalah untuk membuat cover letter seorang kandidat berdasarkan informasi cv dan job description yang diberikan, buat cover letter ini dalam bahasa indonesia"""

if submit1:
  response = get_gemini_response(cv_txt, jobdesc_txt, input_prompt1)
  st.write(response)
elif submit2:
  response = get_gemini_response(cv_txt, jobdesc_txt, input_prompt2)
  st.write(response)
elif submit3:
  response = get_gemini_response_job_desc(jobdesc_txt, input_prompt3)
  st.write(response)
elif submit4:
  response = get_gemini_response(cv_txt, jobdesc_txt, input_prompt4)
  st.write(response)
