import sqlite3
conn = sqlite3.connect("form_data.db", check_same_thread=False)
c = conn.cursor()
c.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER,
    gender TEXT,
    skills TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')
conn.commit()

import streamlit as st
import speech_recognition as sr
def voice_input(prompt=""):
    r = sr.Recognizer()
    if prompt:
        st.info(prompt)
    with sr.Microphone() as source:
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio)
        st.success(f'You said: {text}')
        return text
    except sr.UnknownValueError:
        st.error('Sorry, I could not understand your voice')
        return ""
    except sr.RequestError:
        st.error('Could not connect to Speech Recognition service')
        return ""

st.title('VOICE-FORM')

if 'name' not in st.session_state:
    st.session_state.name=""
if 'email' not in st.session_state:
    st.session_state.email=""
if 'age' not in st.session_state:
    st.session_state.age=None
if 'gender' not in st.session_state:
    st.session_state.gender=None
if 'skills' not in st.session_state:
    st.session_state.skills=""
if 'submitted' not in st.session_state:
    st.session_state.submitted=None

# Create the form
with st.form("voice_form"):
    st.info("Please fill the form. You can type or use voice input.")
    
    name = st.text_input("Full Name:", value=st.session_state.name)
        
        # Voice input for name
    if st.form_submit_button("Speak Name", key="name_btn"):
        spoken = voice_input('Say your full name:')
        if spoken:
            st.session_state.name = spoken
            st.rerun()
    
    email=st.text_input("Email id:",value=st.session_state.email)
    email = st.text_input("Email Address:", value=st.session_state.email,
                         placeholder="example@gmail.com")
    
    #Voice input for email
    if st.form_submit_button("Speak Email"):
        spoken = voice_input('Say your email address slowly and clearly. For example: "john dot doe at gmail dot com"')
        if spoken:
            # Convert spoken email to proper format
            email_text = spoken.lower()
            email_text = email_text.replace(' at ', '@')
            email_text = email_text.replace(' dot ', '.')
            email_text = email_text.replace(' ', '')
            st.session_state.email = email_text
            st.rerun()
    
    age = st.number_input("Age:", min_value=1, max_value=100, step=1, 
                             value=st.session_state.age)
        
    # Voice input for age
    if st.form_submit_button("Speak Age", key="age_btn"):
        spoken = voice_input('Say your age:')
        if spoken and spoken.isdigit():
            st.session_state.age = int(spoken)
            st.rerun()
    
    # Gender selection
    gender_options = ['Male', 'Female', 'Transgender']
    gender = st.selectbox("Gender", options=gender_options, 
                         index=gender_options.index(st.session_state.gender) 
                         if st.session_state.gender in gender_options else 0)
    
    # Voice input for gender
    if st.form_submit_button("Speak Gender", key="gender_btn"):
        spoken = voice_input('Say Male, Female, or Transgender')
        if spoken.capitalize() in gender_options:
            st.session_state.gender = spoken.capitalize()
            st.rerun()
    
    # Skills input
    skills = st.text_area("Skills:", value=st.session_state.skills)
    
    # Voice input for skills
    if st.form_submit_button("Speak Skills", key="skills_btn"):
        spoken = voice_input("Say your skills (separated by commas):")
        if spoken:
            st.session_state.skills = spoken
            st.rerun()
    
    # Form submission button
    submitted = st.form_submit_button("Submit Form")

# Handle form submission outside the form
if submitted:
    # Update session state
    st.session_state.name = name
    st.session_state.email= email
    st.session_state.age = age
    st.session_state.gender = gender
    st.session_state.skills = skills
    st.session_state.submitted = True
    # Insert into DB
    c.execute(
        "INSERT INTO users (name, age, gender, skills) VALUES (?, ?, ?, ?)",
        (name, age, gender, skills)
    )
    conn.commit()

    st.success("✅ Data saved to database!")



# Display results if form was submitted
if st.session_state.submitted:
    st.success("Form submitted successfully!")
    st.write("Data Entered by You")
    st.write(f"Name: {st.session_state.name}")
    st.write(f"Email id:{st.session_state.email}")
    st.write(f"Age: {st.session_state.age}")
    st.write(f"Gender: {st.session_state.gender}")
    st.write(f"Skills: {st.session_state.skills.split(',') if st.session_state.skills else []}")


    
    # to reset the form
    if st.button("Fill Another Form"):
        st.session_state.submitted = False
        st.session_state.name = ""
        st.session_state.email=""
        st.session_state.age = None
        st.session_state.gender = None
        st.session_state.skills = ""
        st.rerun()
import pandas as pd
if st.button("⬇️ Download as CSV"):
    df = pd.read_sql_query("SELECT * FROM users", conn)
    st.download_button("Download CSV", df.to_csv(index=False), "form_data.csv", "text/csv")
