# AskEcomAI
├── ai_agent_ecommerce
│ ├── api
│ │ └── routes.py
│ ├── core
│ │ └── llm.py
│ └── db
│ └── setup_db.py
├── data
│ ├── Product-Level Ad Sales and Metrics (mapped).csv
│ ├── Product-Level Eligibility Table (mapped).csv
│ └── Product-Level Total Sales and Metrics (mapped).csv
├── frontend
│ └── index.html
├── ecommerce.db
├── main.py
├── .env
└── requirements.txt

## ⚙️ Setup Instructions

### 1. Clone the Repository
git clone https://github.com/your-username/EcomQueryAI.git
cd EcomQueryAI


### 2. Create and Activate Virtual Environment
python -m venv venv
venv\Scripts\activate
source venv/bin/activate

### 3. Install Dependencies
pip install -r requirements.txt

### 4. Add your `.env` file
Create a `.env` file in the root directory and add your Google Gemini API key:
GEMINI_API_KEY=your_google_gemini_api_key_here

### 5. Set Up the Database
This will populate `ecommerce.db` using the CSV files from the `data/` folder:
python ai_agent_ecommerce/db/setup_db.py

##  Run the App
Start the FastAPI server:
uvicorn main:app --reload
Open your browser and visit:
http://127.0.0.1:8000/frontend

