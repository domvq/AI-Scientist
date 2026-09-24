import datetime
import os
import json
import arxiv

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

MODEL = "openai/gpt-oss-120b"


# ============================================================
# LLM
# ============================================================

def ask_scientist(prompt):

    # Absolute safety limit for our 8K TPM Groq account.
    prompt = prompt[:24000]

    response = client.responses.create(
        model=MODEL,
        input=prompt,
        max_output_tokens=1500
    )

    return response.output_text


# ============================================================
# LITERATURE
# ============================================================

def search_papers(query, max_results=3):

    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance
    )

    arxiv_client = arxiv.Client()

    papers = []

    for result in arxiv_client.results(search):

        papers.append({
            "title": result.title,
            "authors": [
                author.name
                for author in result.authors[:5]
            ],
            "abstract": result.summary[:1000],
            "url": result.entry_id,
            "published": str(result.published)
        })

    return papers


def format_papers(papers):

    if not papers:
        return "No literature found."

    output = []

    for i, paper in enumerate(papers[:3]):

        output.append(
            f"""
PAPER {i + 1}
Title: {paper.get("title", "")[:300]}
Authors: {", ".join(paper.get("authors", []))}
Abstract: {paper.get("abstract", "")[:1000]}
"""
        )

    return "\n".join(output)


# ============================================================
# HYPOTHESES
# ============================================================

def generate_hypotheses(question, papers=None):

    literature = format_papers(
        papers or []
    )

    prompt = f"""
You are an AI research scientist.

Research question:
{question[:2000]}

Relevant literature:
{literature}

Generate exactly 3 testable hypotheses.

Keep each hypothesis concise.

Return ONLY JSON:

[
  {{
    "hypothesis": "...",
    "reasoning": "...",
    "experiment": "...",
    "expected_result": "...",
    "falsification": "...",
    "novelty": "..."
  }}
]
"""

    result = ask_scientist(prompt)

    try:
        return json.loads(result)

    except Exception:

        cleaned = (
            result
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

        try:
            return json.loads(cleaned)

        except Exception:

            return [{
                "hypothesis": result,
                "reasoning": "",
                "experiment": "",
                "expected_result": "",
                "falsification": "",
                "novelty": ""
            }]


# ============================================================
# CHOOSE EXPERIMENT
# ============================================================

def choose_experiment(
    question,
    hypotheses,
    previous_results=None
):

    previous_results = previous_results or []

    # Only send compact history.
    compact_history = []

    for item in previous_results[-3:]:

        compact_history.append({
            "experiment": item.get("experiment"),
            "hypothesis": item.get("hypothesis", "")[:500],
            "output": item.get("output", "")[:1500],
            "analysis": item.get("analysis", "")[:1000]
        })

    prompt = f"""
You are an autonomous scientific researcher.

Question:
{question[:2000]}

Hypotheses:
{json.dumps(hypotheses)[:5000]}

Previous experiments:
{json.dumps(compact_history)[:5000]}

Choose the most informative next experiment.

Return ONLY JSON:

{{
  "selected_hypothesis": "...",
  "reason": "...",
  "experiment_goal": "...",
  "expected_result": "...",
  "success_metric": "..."
}}
"""

    result = ask_scientist(prompt)

    return parse_json(result)


# ============================================================
# EXPERIMENT CODE
# ============================================================

def generate_experiment(
    question,
    hypothesis,
    experiment_goal
):

    prompt = f"""
You are an AI scientist.

Question:
{question[:1500]}

Hypothesis:
{hypothesis[:1500]}

Experiment goal:
{experiment_goal[:1500]}

Write a complete Python experiment.

Allowed libraries:
numpy
pandas
scikit-learn
matplotlib

Requirements:

- Test the hypothesis.
- Include a baseline.
- Use a built-in sklearn dataset.
- Print numerical metrics.
- Use a fixed random seed.
- Finish within 30 seconds.
- Do not download anything.
- Do not access the filesystem.
- Return ONLY Python code.
"""

    return ask_scientist(prompt)


# ============================================================
# ANALYSIS
# ============================================================

def analyze_results(
    question,
    hypothesis,
    output
):

    prompt = f"""
You are a scientific reviewer.

Question:
{question[:1500]}

Hypothesis:
{hypothesis[:1500]}

Experiment results:
{output[:4000]}

Analyze:

1. What happened?
2. Important numbers
3. Was the hypothesis supported?
4. Limitations
5. Possible confounders
6. What should be tested next?

Do not claim that one experiment proves a scientific theory.

Keep the analysis concise.
"""

    return ask_scientist(prompt)


# ============================================================
# NEXT EXPERIMENT
# ============================================================

def propose_next_experiment(
    question,
    history
):

    compact_history = []

    for item in history[-3:]:

        compact_history.append({
            "hypothesis": item.get(
                "hypothesis", ""
            )[:500],

            "output": item.get(
                "output", ""
            )[:1200],

            "analysis": item.get(
                "analysis", ""
            )[:1000]
        })

    prompt = f"""
You are an autonomous scientist.

Research question:
{question[:1500]}

Previous experiments:
{json.dumps(compact_history)[:5000]}

Suggest ONE useful next experiment.

It should provide new information.

Return ONLY JSON:

{{
  "goal": "...",
  "hypothesis": "...",
  "reason": "...",
  "expected_result": "..."
}}
"""

    result = ask_scientist(prompt)

    return parse_json(result)


# ============================================================
# JSON HELPER
# ============================================================

def parse_json(result):

    cleaned = (
        result
        .replace("```json", "")
        .replace("```", "")
        .strip()
    )

    try:

        return json.loads(cleaned)

    except Exception:

        start = cleaned.find("{")
        end = cleaned.rfind("}")

        if start >= 0 and end > start:

            try:
                return json.loads(
                    cleaned[start:end + 1]
                )

            except Exception:
                pass

        start = cleaned.find("[")
        end = cleaned.rfind("]")

        if start >= 0 and end > start:

            try:
                return json.loads(
                    cleaned[start:end + 1]
                )

            except Exception:
                pass

        raise ValueError(
            "The AI returned invalid JSON:\n"
            + cleaned[:2000]
        )


def save_experiment(
    question,
    experiment_number,
    hypothesis,
    code,
    output,
    analysis
):

    os.makedirs("experiments", exist_ok=True)

    timestamp = datetime.datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    filename = (
        f"experiments/"
        f"experiment_{experiment_number}_"
        f"{timestamp}.json"
    )

    data = {
        "question": question,
        "experiment_number": experiment_number,
        "hypothesis": hypothesis,
        "code": code,
        "output": output,
        "analysis": analysis,
        "timestamp": timestamp
    }

    with open(
        filename,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            indent=2
        )

    return filename



def generate_final_report(
    question,
    papers,
    hypotheses,
    history
):

    compact_history = []

    for item in history:

        compact_history.append({
            "experiment": item.get(
                "experiment"
            ),

            "hypothesis": item.get(
                "hypothesis",
                ""
            )[:1000],

            "goal": item.get(
                "goal",
                ""
            )[:1000],

            "output": item.get(
                "output",
                ""
            )[:2000],

            "analysis": item.get(
                "analysis",
                ""
            )[:2000]
        })


    literature = []

    for paper in papers[:3]:

        literature.append({
            "title": paper.get(
                "title",
                ""
            )[:300],

            "abstract": paper.get(
                "abstract",
                ""
            )[:800]
        })


    prompt = f"""
You are writing a rigorous scientific research report.

Research question:
{question[:2000]}

Relevant literature:
{json.dumps(literature)}

Hypotheses:
{json.dumps(hypotheses)[:5000]}

Experiments:
{json.dumps(compact_history)[:10000]}

Write a concise research report using these sections:

# Abstract

# Research Question

# Literature Context

# Hypotheses

# Methods

# Results

# Discussion

# Limitations

# Conclusion

# Future Experiments

Important rules:

- Only make claims supported by the experiments.
- Clearly distinguish observations from interpretations.
- Do not claim causation unless the experiment supports it.
- Do not claim scientific novelty has been established.
- Mention important limitations.
- Include important numerical results.
- Be concise but scientifically rigorous.
IMPORTANT:
- Ensure the generated Python code is syntactically valid.
- Do not pass the same keyword argument twice.
- Before returning the code, check all **kwargs expansions for duplicate explicit arguments.
- For example, never write Model(**params, random_state=seed) if params may already contain random_state.
- The returned response must contain ONLY executable Python code.
"""

    result = ask_scientist(prompt)

    return clean_python_code(result)


def clean_python_code(code):
    code = str(code).strip()

    # Remove Markdown code fences.
    if "```" in code:
        parts = code.split("```")

        if len(parts) >= 2:
            code = parts[1].strip()

            lines = code.splitlines()

            if lines:
                first = lines[0].strip().lower()

                if first in ("python", "py"):
                    code = "\n".join(lines[1:])

    # Remove accidental leading/trailing fences.
    code = code.replace("```python", "")
    code = code.replace("```Python", "")
    code = code.replace("```PYTHON", "")
    code = code.replace("```", "")

    return code.strip()

