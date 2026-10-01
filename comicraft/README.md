# ComicCraft

FastAPI + Gemini five-panel AI comic creator.

## Windows / VS Code

```powershell
py -3 -m venv venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
```

Put your Gemini key in `.env` and keep `IMAGE_BACKEND=placeholder` for the first test.

Run:

```powershell
python -m uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000
