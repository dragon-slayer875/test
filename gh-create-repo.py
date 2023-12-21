# create a program that initializes a git repository and creates a new repo on github using SSH

import os
import sys
import subprocess
import requests

from dotenv import load_dotenv

load_dotenv()

# get the name of the repo from the command line
repo_name = str(sys.argv[1])

# create the directory
os.mkdir(repo_name)

# change into the directory
os.chdir(repo_name)

# initialize the git repository
subprocess.run(["git", "init"])

# create the github repo
# get the github token from the environment variable
github_token = os.getenv("GITHUB_TOKEN")

# create the github repo
response = requests.post("https://api.github.com/user/repos", json={"name": repo_name}, headers={"Authorization": f"token {github_token}"})

# get the ssh url from the response
ssh_url = response.json()["ssh_url"]

# add the remote origin
subprocess.run(["git", "remote", "add", "origin", ssh_url])

# create the readme file
with open("README.md", "w") as f:
    f.write(f"# {repo_name}")
    print(f"Enter description for {repo_name} in markdown: ")
    description = input()
    f.write(f"\n{description}")

# add the readme file
subprocess.run(["git", "add", "README.md"])

# commit the readme file
subprocess.run(["git", "commit", "-m", "Initial commit"])

# push the readme file
subprocess.run(["git", "push", "-u", "origin", "main"])
    
