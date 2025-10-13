# Case-LLM for Legal Document Analysis

## Overview

This model leverages Large Language Models (LLMs) to perform sophisticated analysis of legal documents and case data. It can be used for a variety of tasks, including:

- **Case Summarization**: Generating concise summaries of complex legal cases.
- **Entity Extraction**: Identifying key entities (people, organizations, dates) from unstructured text.
- **Legal Brief Generation**: Automatically generating structured legal briefs from case data.
- **Case Strength Assessment**: Evaluating the strengths and weaknesses of a case.
- **Outcome Prediction**: Predicting the likely outcome of a case.

## How It Works

The model uses the OpenAI API to send prompts to a powerful LLM (e.g., GPT-4). The prompts are carefully engineered to elicit the desired analysis from the model. The model can also be run in a "mock" mode for development and testing without an API key.

## How to Run

The model can be run as a standalone script or as part of the unified simulation runner.

```bash
python models/case_llm/case_llm_model.py
```

This requires an OpenAI API key to be set as an environment variable (`OPENAI_API_KEY`). If the key is not present, the model will run in mock mode.

