"""Python script for populating seed data in a fresh database with data from GitHub."""

import os

import requests
from loguru import logger
from pydantic import BaseModel


class GitHubConentLinks(BaseModel):
    """GitHub links."""

    self: str
    git: str
    html: str


class GitHubConent(BaseModel):
    """GitHub query response."""

    name: str
    path: str
    sha: str
    size: int
    url: str
    html_url: str
    git_url: str
    download_url: str
    type: str
    _links: GitHubConentLinks


OWNER = "humoroushorse"
USER = "humoroushorse"
REPO = "ttrpg-data"
DATA_REPO_PATH = f"https://api.github.com/repos/{OWNER}/{REPO}/contents"
GITHUB_ACCESS_TOKEN = os.environ.get("GITHUB_ACCESS_TOKEN")


headers = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {GITHUB_ACCESS_TOKEN}",
    "X-GitHub-Api-Version": "2022-11-28",
    "User-Agent": "{USER}",
}

github_repo_contents_response = requests.get(url=f"{DATA_REPO_PATH}/data_final", headers=headers)
github_repo_contents = [GitHubConent(**j) for j in github_repo_contents_response.json()]
spells_list = [s.name for s in github_repo_contents if s.name.startswith("spells_")]
for s in spells_list:
    logger.debug(s)
