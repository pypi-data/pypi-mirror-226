# wwwml [![PyPI version](https://badge.fury.io/py/wwwml.svg)](https://badge.fury.io/py/wwwml) [![Release Building](https://github.com/iaalm/wwwml/actions/workflows/release.yml/badge.svg)](https://github.com/iaalm/wwwml/actions/workflows/release.yml) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
What's wrong with my linux? A LLM based tool to diagnose linux problems.

## Install
```bash
pip install -U wwwml
```

Set environment variable in your `~/.bashrc`, `~/.zshrc`, etc.
```bash
export OPENAI_API_KEY=sk~XXXXXXXX
```
Or, to use Azure OpenAI endpoint, set following environment variable:
```bash
export OPENAI_API_KEY=XXXXXXXXXX
export OPENAI_API_BASE=https://XXXXXX.openai.azure.com/
export OPENAI_API_TYPE=azure
export OPENAI_API_VERSION=2023-07-01-preview
# Use a deploymetn of gpt-3.5-turbo or gpt-4 with version 0613 or later
export WWWML_DEPLOYMENT=gpt-35-turbo-16k
```

## Usage
```bash
python -m wwwml
# or
wwwml
```

## Dependency
This tool currently call following command to get system information
- sysstat
  - iostat
  - mpstat
  - vmstat
