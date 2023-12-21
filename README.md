# Github create remote repository

## Setup
- Create a `.env` file with your github token:
```
echo "GITHUB_TOKEN=<Your API Token>" >> .env

```

- Source venv and install dependencies
```
source venv/bin/activate
python -m pip install -r requirements.txt

```

## Usage
- Run:
```
python gh-create-repo.py <Repo Name>
```

