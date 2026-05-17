# EduRisk AI — Intelligent Classroom Intelligence Platform

---

## 🎓 Overview

EduRisk AI is an AI-powered teacher assistant. It solves a real problem in classrooms, teachers cannot individually monitor every student's attendance, quiz performance, assignment behavior, and learning gaps, especially in large classrooms.

The solution is a Streamlit-based web application where any teacher uploads their class CSV file and instantly gets AI-powered risk detection, assignment grading via OCR, personalized intervention plans, bilingual parent reports, and auto-generated worksheets — all in one platform powered by Groq API.

---

## 🚨 Problem Statement

In large classrooms across Pakistan, teachers struggle to:
- Track which students are falling behind before it's too late
- Grade assignments quickly and fairly with detailed feedback
- Write personalized improvement plans for every struggling student
- Communicate with parents in both English and Urdu
- Create topic-specific practice material for weak students

EduRisk AI automates all of this.

---

## 💡 Solution

Teachers upload any student data CSV → the AI analyzes it in seconds → risk scores are computed → all 6 agents unlock and work on that teacher's real data. No hardcoded data. No setup beyond uploading a file.

---

## 🤖 AI Agents

**1. Risk Detection Agent**
Scores every student from 0 to 100 using a weighted formula across attendance, quiz average, late submissions, participation level, and days since last login. Students are categorized as High Risk, Medium Risk, or Low Risk automatically.

**2. Assignment Grading Agent**
Teacher uploads a photo or PDF of a student's handwritten or typed answer sheet alongside a marking scheme. Groq's LLaMA 4 Scout vision model performs OCR to extract the student's text, then LLaMA 3.3 compares it to the marking scheme and returns a score, grade letter, per-question breakdown, missed points, weak topics identified, and constructive feedback.

**3. Intervention Planning Agent**
Select any at-risk student and generate a structured 2-week improvement plan covering Week 1 actions, Week 2 follow-up, parent involvement tasks, and measurable success metrics — all personalized to that student's exact data.

**4. Parent Communication Agent**
Generates formal parent letters in both English and Urdu with one click. The letter includes the student's attendance, quiz average, specific concerns with real numbers, and practical actions parents can take at home. Both versions are downloadable as text files.

**5. Worksheet Generator**
Select a student and their weak topic auto-populates. Choose difficulty, question types (MCQ, Short Answer, True/False, Fill in the Blank), and number of questions. The AI generates a complete quiz aligned to Pakistan's national curriculum for that grade level.

**6. EduSense AI Chatbot**
A natural language interface powered by LangChain and Groq. Teachers can ask questions like "Who are the High Risk students in Grade 10?" or "Which subject has the lowest quiz average?" and get instant answers from their own uploaded data.

---

## 🖥️ Features

- Upload any teacher's CSV — works on real classroom data, not just sample data
- Auto-computes risk score and risk level if not present in the uploaded file
- Auto-fills missing optional columns so partial CSVs never crash the app
- Downloadable template CSV so any teacher can get started immediately
- All pages locked behind a guard — friendly redirect shown if no data uploaded
- Dark themed UI with Plotly charts throughout the dashboard
- Bilingual parent reports with RTL Urdu text rendering
- Per-question breakdown table for graded assignments
- Download buttons for intervention plans, parent reports, and worksheets

---

## 📁 Project Structure

```
EduRisk-AI/
├── main.py                      # Landing page + CSV uploader
├── requirements.txt             # All dependencies
├── .gitignore
├── README.md
│
├── pages/
│   ├── 1_dashboard.py           # Class analytics and risk charts
│   ├── 2_grading_agent.py       # Assignment grading via OCR
│   ├── 3_intervention.py        # Intervention plan generator
│   ├── 4_parent_report.py       # Parent communication EN + UR
│   ├── 5_worksheet.py           # Worksheet and quiz generator
│   └── 6_chatbot.py             # EduSense AI chatbot
│
├── agents/
│   ├── __init__.py
│   ├── grading_agent.py         # OCR + Groq Vision grading pipeline
│   ├── intervention_agent.py    # LLM intervention planner
│   ├── parent_agent.py          # Bilingual report generator
│   ├── worksheet_agent.py       # Quiz generator
│   ├── chatbot_agent.py         # LangChain pandas agent
│   └── risk_agent.py            # Risk scoring formula
│
├── utils/
│   ├── __init__.py
│   ├── data_loader.py           # Session state CSV loader + validation
│   ├── page_guard.py            # Upload guard used by all pages
│   └── pdf_parser.py            # PyMuPDF text extraction
│
└── sample_data/
    └── students.csv             # 200-student template dataset
```

---

## ⚙️ Tech Stack

| Layer | Technology |
|---|---|
| UI Framework | Streamlit |
| Data Processing | Pandas, NumPy |
| Charts | Plotly |
| AI / LLM Text | Groq API — LLaMA 3.3 70B Versatile |
| AI / LLM Vision | Groq API — LLaMA 4 Scout 17B (OCR) |
| Chatbot Framework | LangChain + LangChain-Groq |
| PDF Parsing | PyMuPDF |
| Environment Variables | python-dotenv |

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/EduRisk-AI.git
cd EduRisk-AI
```

### 2. Create and activate a virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install all dependencies
```bash
pip install -r requirements.txt
```

### 4. Create your .env file
Create a file named `.env` in the project root folder:
```
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxxxxx
```
Get a free API key at https://console.groq.com

### 5. Run the app
```bash
streamlit run main.py
```

---

## 📊 How to Use

1. Open the app in your browser
2. On the Home page click Download Template CSV to get the sample file
3. Fill the template with your real students or use the sample as-is
4. Upload the CSV using the uploader on the Home page
5. All 6 agents unlock immediately — navigate using the sidebar
6. For grading: upload a student answer image or PDF and paste the marking scheme

---

## 📋 CSV Template Columns

**Required columns** — the app will not load without these:

| Column | Description |
|---|---|
| name | Student full name |
| grade | e.g. Grade 8, Grade 9, Grade 10 |
| subject | e.g. Mathematics, Science, English |
| attendance_pct | Attendance percentage 0–100 |
| quiz_avg | Average quiz score 0–100 |
| overall_score | Overall grade percentage 0–100 |

**Optional columns** — auto-computed if missing:
section, semester, participation_level, late_submissions, missing_assignments,
weak_topic, second_weak_topic, days_since_login, parent_phone, parent_email,
risk_score, risk_level

---

## 🔢 Risk Scoring Formula

```
Risk Score =
  (1 - attendance / 100)          x 30%
  (1 - quiz_avg / 100)            x 25%
  (late_submissions / total)      x 20%
  (1 - participation_score)       x 15%
  (days_since_login / 30)         x 10%
```

| Score Range | Risk Level |
|---|---|
| 0 – 34 | Low Risk |
| 35 – 64 | Medium Risk |
| 65 – 100 | High Risk |

---

## 🌐 Deploying to Streamlit Cloud

1. Push your repo to GitHub making sure .env is in .gitignore
2. Go to share.streamlit.io and click New App
3. Select your repository and set main.py as the entry point
4. Under Settings → Secrets add:

```
GROQ_API_KEY = "gsk_xxxxxxxxxxxxxxxxxxxxxxxx"
```

5. Deploy — the app will be live at a public URL

---

## 👥 Team

Built at AI Hackathon 2025 by students of Sir Syed University of Engineering and Technology (SSUET), Karachi, Pakistan.

**Asad Ur Rehman**  
[LinkedIn](https://www.linkedin.com/in/asad-ur-rehman-108439285/) · [GitHub](https://github.com/Asad-Ur-R)

**Ali Sheikh**
[LinkedIn](https://www.linkedin.com/in/ali-sheikh-674298352?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app) · [GitHub](https://github.com/ALISHEIKH10)

**Huzaifa Imran** 
[LinkedIn](https://www.linkedin.com/in/huzaifa-imran-/) · [GitHub](https://github.com/Huzaifa823)

---

## APP
[StreamLit](https://edusenseai.streamlit.app/)
## 📄 License

This project is open source and available under the MIT License.
