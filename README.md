# Voice Based Form (Streamlit + SQLite)

A voice-enabled form built with Streamlit where users can fill in details 
(Name, Email, Age, Gender, Skills) using typing or voice input. 
Data is stored in SQLite database and can be downloaded as CSV.

## Features
- Voice input for each field (via Google Speech Recognition)
- Data saved in SQLite database
- Download all form entries as CSV
- Reset form and submit multiple entries

## Tech Stack
- Python
- Streamlit (frontend UI)
- SpeechRecognition + PyAudio (voice input)
- SQLite (database)
- Pandas (CSV export)

## Run the project
At Terminal Run -
git clone https://github.com/<tanishkavyas0603>/voice-form.git
cd voice-form
pip install -r requirements.txt
streamlit run main.py


