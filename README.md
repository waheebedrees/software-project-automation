# Software Project Automation

This project is an automated software project generator and workflow orchestrator built in Python. It leverages agent-based architecture to generate, validate, and document software projects based on a given specification. The system is designed to streamline the process of creating new software projects, including code, tests, documentation, and build/run scripts, using a set of specialized agents.

## Features

- **Automated Project Generation:** Reads a project specification and generates code, tests, documentation, and interface definitions.
- **Agent-Based Architecture:** Utilizes multiple agents (code, docs, manifest, IDL, review, run, test) to handle different aspects of project creation and validation.
- **Retry and Error Handling:** Robust retry logic for API rate limits and HTTP errors.
- **Review Loop:** Automated review and approval of generated code with the ability to iterate on feedback.
- **Extensible:** Easily add new agents or extend existing ones for more complex workflows.

## Project Structure

```
src/
  main.py                # Main workflow orchestrator
  agents/                # Agent definitions (code, docs, manifest, etc.)
  config/
    project_spec.txt     # Project specification input
  generated_projects/    # Output directory for generated projects
  tools/
    file_hanler.py       # File handling utilities
  utils/
    custom_logger.py     # Logging utilities
    utils.py             # Helper functions
```

## How It Works

1. **Specification Input:** Reads a project specification from `config/project_spec.txt`.
2. **Agent Initialization:** Sets up agents for manifest creation, IDL, code, tests, documentation, review, and run scripts.
3. **Manifest Generation:** Generates a manifest describing the files to be created.
4. **Task Execution:** Each agent generates its respective output (code, tests, docs, etc.).
5. **Review Loop:** The generated code is reviewed and iterated upon if necessary.
6. **Output:** All generated files are saved in a timestamped directory under `generated_projects/`.

## Requirements

- Python 3.11+
- [CrewAI](https://github.com/joaomdmoura/crewAI)
- [OpenAI](https://github.com/openai/openai-python)
- [httpx](https://www.python-httpx.org/)
- [tenacity](https://tenacity.readthedocs.io/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)

Install dependencies:

```bash
pip install -r requirements.txt
```


## License

MIT License


