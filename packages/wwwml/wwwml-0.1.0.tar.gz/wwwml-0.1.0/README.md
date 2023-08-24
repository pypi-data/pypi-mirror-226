# wwwml
What's wrong with my linux? A LLM based tool to diagnose linux problems.

## Install
```bash
pip install -U wwwml
```

Or, to use Azure OpenAI endpoint, set following environment variable:
```

```bash
export OPENAI_API_KEY=
export OPENAI_API_BASE=
export OPENAI_API_TYPE=azure
export OPENAI_API_VERSION=2023-07-01-preview
# Use a deploymetn of gpt-3.5-turbo or gpt-4 with version 0613 or later
export WWWML_DEPLOYMENT=
```

## Usage
```bash
python -m wwwml
```
