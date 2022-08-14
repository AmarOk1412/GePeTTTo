# GepeTTTo

A simple GitLab bot working with GPT-3

## Preparation

### GitLab's token

Go to your GitLab's instance (https://<YOUR_GITLAB>/-/profile/applications) and generate a new token with `api`/`read_api`'s permissions.

### GPT-3's token

To get your GPT-3 token, connect to your OpenAI's account and generate a new token from this page: https://beta.openai.com/account/api-keys

### Prepare the environment file

Then, you simply need to create the environment file (default: `env`) like so:

```bash
export OPENAI_API_KEY="YOUR_OPENAI_API_KEY"
export GITLAB_API_KEY="YOUR_GITLAB_API_KEY"
export GITLAB_ENDPOINT="YOUR_GITLAB_INSTANCE"
export GITLAB_USERS="COMMA_SEPARATED_USERS" # Optional, if you want to train a custom model, e.g. 9,3,233
```

You also need to install `termcolor` (`pip3 install termcolor`)

## Usage

### Generate a new training dataset

```
make dataset
```

will use `src/gpt3-make-dataset.py` to create a new training dataset from your GitLab's instance

### Train a new model

```
make train
```

will run `src/train-openai.sh` with default parameters.

### Use it

```
make answer
```

will run `src/answer-last.py` to gather last issues and answer it.

## NOTE

Code in this directory is under BSD-3 License, rsc/custom.jsonl is mostly generated from the FAQ
from docs.jami.net (under GNU Free Documentation License v1.3) or my own comments.