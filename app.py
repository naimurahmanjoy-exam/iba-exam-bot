import streamlit as st
from google import genai
import os

# ১. পেজ সেটআপ
st.set_page_config(page_title="IBA Prep Bot", page_icon="🎓")

st.title("🎓 IBA Admission Question Generator")
st.write("নিচের অপশনগুলো সিলেক্ট করে প্রশ্ন তৈরি করুন।")

# ২. সিক্রেট থেকে API Key নেওয়া (এটি ইউজার দেখতে পাবে না)
# আপনি যখন স্ট্রিমলিট ক্লাউডে অ্যাপটি সেটআপ করবেন, তখন সেখানে এই কি-টি বসাতে হবে।
api_key = st.secrets.get("GENAI_API_KEY")

if not api_key:
    st.error("API Key খুঁজে পাওয়া যায়নি! অনুগ্রহ করে Streamlit Secrets-এ কি (Key) যোগ করুন।")
    st.stop()

# ৩. ক্লায়েন্ট তৈরি
client = genai.Client(api_key=api_key)

# ৪. ড্রপডাউন মেনু (ইউজার ইন্টারফেস)
col1, col2 = st.columns(2)

with col1:
    subject = st.selectbox(
        "বিষয় (Subject):",
        ("Math", "Logical Reasoning", "English", "Analytical Ability")
    )

with col2:
    difficulty = st.selectbox(
        "কঠিন্য (Difficulty):",
        ("Easy", "Moderate", "Hard")
    )

# ৫. প্রশ্ন জেনারেট বাটন
if st.button("Generate New Question"):
    with st.spinner('Gemini প্রশ্ন তৈরি করছে... একটু অপেক্ষা করুন।'):
        try:
            prompt = f"""
            You are an IBA (Bangladesh) Admission Test setter. 
            Generate ONE multiple-choice question for {subject}. 
            Include 4 options (A/B/C/D), indicate the correct answer, and provide a brief explanation.
            Difficulty Level: {difficulty}
            """
            
            # মডেল থেকে রেসপন্স নেওয়া
            response = client.models.generate_content(
                model="gemini-2.0-flash", 
                contents=prompt
            )
            
            # ফলাফল স্ক্রিনে দেখানো
            st.markdown("---")
            st.markdown("### জেনারেটেড প্রশ্ন:")
            st.write(response.text)
            
        except Exception as e:
            st.error(f"দুঃখিত, একটি সমস্যা হয়েছে: {e}")

st.divider()
st.caption("Powered by Gemini AI | IBA Admission Helper")
