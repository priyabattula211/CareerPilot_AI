from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get('/')
async def home():
    return HTMLResponse(content="""
    <html>
      <head><title>CareerPilot AI</title></head>
      <body style="font-family:Arial,sans-serif; padding:40px;">
        <h1>CareerPilot AI</h1>
        <p>This project is prepared for Vercel deployment.</p>
        <p>To fully run the interactive Streamlit app, deploy it with Streamlit Cloud or host the app separately.</p>
      </body>
    </html>
    """)
