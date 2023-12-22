import os
import sys
import subprocess
import requests
from dotenv import load_dotenv

def create_directory(repo_name):
    os.mkdir(repo_name)
    os.chdir(repo_name)

def init_git():
    subprocess.run(["git", "init"])

def create_github_repo(repo_name, github_token):
    response = requests.post("https://api.github.com/user/repos", json={"name": repo_name}, headers={"Authorization": f"token {github_token}"})
    return response.json()["ssh_url"]

def add_remote_origin(ssh_url):
    subprocess.run(["git", "remote", "add", "origin", ssh_url])

def create_readme(repo_name):
    with open("README.md", "w") as f:
        f.write(f"# {repo_name}")
        print(f"Enter description for {repo_name} in markdown: ")
        description = input()
        f.write(f"\n{description}")

def main():
    load_dotenv()
    repo_name = str(sys.argv[1])
    github_token = os.getenv("GITHUB_TOKEN")
    
    create_directory(repo_name)
    init_git()
    ssh_url = create_github_repo(repo_name, github_token)
    add_remote_origin(ssh_url)
    create_readme(repo_name)

if __name__ == "__main__":
    main()