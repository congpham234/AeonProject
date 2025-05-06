## 🛠️ Setup Instructions

1. **Clone the repo** (or download the source code)

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
3. **Install dependencies**
pip install -r requirements.txt

4. **Run the API server**
uvicorn app.main:app --reload

5. **Access Swagger**
Open your browser and go to:
http://127.0.0.1:8000/docs


Or access ReDoc docs:
http://127.0.0.1:8000/redoc


