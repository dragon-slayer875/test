import os
import sys
import subprocess
import requests
import tempfile
from dotenv import load_dotenv
from abc import ABC, abstractmethod

class RepoManager(ABC):
    @abstractmethod
    def create_directory(self, repo_name):
        pass

    @abstractmethod
    def init_git(self):
        pass

    @abstractmethod
    def create_github_repo(self, repo_name, github_token):
        pass

    @abstractmethod
    def add_remote_origin(self, ssh_url):
        pass

    @abstractmethod
    def create_readme(self, repo_name):
        pass

    @abstractmethod
    def list_user_repos(self, github_token):
        pass

class GitHubRepoManager(RepoManager):
    def create_directory(self, repo_name):
        os.mkdir(repo_name)
        os.chdir(repo_name)

    def init_git(self):
        subprocess.run(["git", "init"])

    def create_github_repo(self, repo_name):
        response = requests.post("https://api.github.com/user/repos", json={"name": repo_name}, headers={"Authorization": f"token {self.github_token}"})
        return response.json()["ssh_url"]
    
    def add_remote_origin(self, ssh_url):
        subprocess.run(["git", "remote", "add", "origin", ssh_url])

    def create_readme(self, repo_name):
        with tempfile.NamedTemporaryFile(suffix=".md", delete=False) as tf:
            subprocess.run(["nvim", tf.name])
            with open(tf.name, "r") as f:
                description = f.read()
            os.remove(tf.name)
        with open("README.md", "w") as f:
            f.write(f"# {repo_name}\n{description}")

    def list_user_repos(self, api_token):
        headers = {
            "Authorization": f"token {api_token}"
        }
        response = requests.get("https://api.github.com/user/repos", headers=headers)
        if response.status_code == 200:
            repos = response.json()
            for repo in repos:
                print(repo["name"])
        else:
            print(f"Failed to list repositories. Status code: {response.status_code}")

class RepoMenu:
    def __init__(self, repo_creator):
        self.repo_creator = repo_creator

    def run(self):
        load_dotenv()
        self.repo_creator.github_token = os.getenv("GITHUB_TOKEN")
        while True:
            print("\n1. Create new repository")
            print("2. List repositories")
            print("3. Exit")
            choice = input("Enter your choice: ")

            if choice == "1":
                repo_name = input("Enter the name of the repository: ")
                self.repo_creator.create_directory(repo_name)
                self.repo_creator.init_git()
                ssh_url = self.repo_creator.create_github_repo(repo_name)
                self.repo_creator.add_remote_origin(ssh_url)
                self.repo_creator.create_readme(repo_name)
            elif choice == "2":
                self.repo_creator.list_user_repos()
            elif choice == "3":
                sys.exit()
            else:
                print("Invalid choice. Please try again.")

def main():
    repo_creator = GitHubRepoManager()
    menu = RepoMenu(repo_creator)
    menu.run()

if __name__ == "__main__":
    main()