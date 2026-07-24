import requests
import base64
from utils.config import GITHUB_TOKEN
from utils.logger import get_logger

logger = get_logger(__name__)

class GitHubClient:
    def __init__(self):
        self.base_url = "https://api.github.com"
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
        }
        if GITHUB_TOKEN:
            self.headers["Authorization"] = f"token {GITHUB_TOKEN}"

    def get_user_profile(self, username):
        url = f"{self.base_url}/users/{username}"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        logger.error(f"Failed to fetch user {username}: {response.text}")
        return None

    def get_user_repos(self, username, limit=10):
        url = f"{self.base_url}/users/{username}/repos?sort=updated&per_page={limit}"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        return []

    def get_repo(self, owner, repo):
        url = f"{self.base_url}/repos/{owner}/{repo}"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        logger.error(f"Failed to fetch repo {owner}/{repo}: {response.text}")
        return None

    def get_repo_languages(self, owner, repo):
        url = f"{self.base_url}/repos/{owner}/{repo}/languages"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        return {}
        
    def get_all_user_languages(self, username):
        repos = self.get_user_repos(username, limit=30)
        langs = {}
        for r in repos:
            repo_langs = self.get_repo_languages(username, r['name'])
            for l, bytes_count in repo_langs.items():
                langs[l] = langs.get(l, 0) + bytes_count
        # Sort top
        sorted_langs = dict(sorted(langs.items(), key=lambda item: item[1], reverse=True)[:5])
        return sorted_langs

    def get_readme(self, owner, repo):
        url = f"{self.base_url}/repos/{owner}/{repo}/readme"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            return base64.b64decode(data['content']).decode('utf-8')
        return ""
