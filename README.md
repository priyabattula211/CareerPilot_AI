# CareerPilot AI

CareerPilot AI is a Streamlit-based dashboard application that helps job seekers analyze their resumes, review GitHub profiles, match projects to career goals, and prepare for interviews using AI-powered insights.

## Key Features

- **Dashboard**: Overview of your career analytics.
- **GitHub Review**: Analyze GitHub repositories and code quality.
- **Resume Review**: Extract skills and experience from resumes.
- **Portfolio Match**: Match candidate experience to job opportunities.
- **Interview Readiness**: Generate interview preparation plans.
- **Settings**: Configure the AI model and API integrations.

## Project Structure

- `app.py` - Main Streamlit application entrypoint.
- `ai/` - AI integration logic using Google Gemini.
- `analysis/` - Resume and code quality scoring utilities.
- `components/` - Streamlit UI components and custom page styling.
- `database/` - Local settings and data service logic.
- `github/` - GitHub review and repository analysis helpers.
- `pages/` - Individual Streamlit page modules.
- `resume/` - Resume parsing utilities.
- `utils/` - Configuration and logging helpers.

## Setup

1. Create a virtual environment and activate it:

```bash
python -m venv venv
venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file from the example:

```bash
copy .env.example .env
```

4. Add your API keys to `.env`:

```ini
GEMINI_API_KEY=your_gemini_api_key
GITHUB_TOKEN=your_github_token
```

## Run the app

```bash
streamlit run app.py
```

Then open the provided Streamlit URL in your browser.

## Deploy to Render

This project includes a `render.yaml` file for Render deployment.

1. Push the repository to GitHub.
2. Create a Render account at https://render.com and connect your GitHub repo.
3. Add the following environment variables in Render:

```text
GEMINI_API_KEY
GITHUB_TOKEN
```

4. Use the default web service build command and start command from `render.yaml`:

```text
pip install -r requirements.txt
streamlit run app.py --server.port $PORT --server.address 0.0.0.0
```

5. Deploy the service on the `main` branch.

> Keep `.env` local and do not commit it. Render will use environment variables configured in the dashboard.

## Environment Variables

- `GEMINI_API_KEY`: API key for Google Gemini AI.
- `GITHUB_TOKEN`: GitHub personal access token for repository analysis.

> The `.env` file is intentionally ignored by Git to keep sensitive keys secret. Only `.env.example` should be checked in.

## Notes

- The app uses Streamlit navigation and custom UI components.
- Maintain API keys locally and avoid committing `.env` to the repository.
- If you share or publish the repo, rotate any API keys that were previously exposed.
