# 🧪 AI Scientist

An experimental autonomous research assistant built with **Python, Streamlit, Groq, and arXiv**.

AI Scientist takes a research question and turns it into an automated research workflow:

Research Question
       ↓
   Literature Search
       ↓
 Hypothesis Generation
       ↓
 Experiment Selection
       ↓
 Python Code Generation
       ↓
   Experiment Execution
       ↓
   Results Analysis
       ↓
  Research Report
```

## 🚀 What It Does

AI Scientist is a prototype designed to explore how AI can assist with scientific research.

Given a research question, it can:

* 🔬 Understand a research question
* 📚 Search arXiv for relevant papers
* 🧠 Generate testable hypotheses
* 🎯 Select an experiment
* 🐍 Generate Python experiment code
* 🧪 Execute experiments locally
* 📊 Analyze experimental results
* 📝 Generate a final research report
* 💾 Save experiment results

## 🖥️ Tech Stack

* **Python 3.13**
* **Streamlit** — web interface
* **Groq** — LLM inference
* **OpenAI Python SDK** — Groq's OpenAI-compatible API
* **arXiv API** — scientific literature search
* **NumPy**
* **Pandas**
* **Scikit-learn**
* **Matplotlib**

## 📁 Project Structure

```text
ai-scientist/
│
├── app.py
├── scientist.py
├── requirements.txt
├── .gitignore
├── README.md
│
└── experiments/
    └── ...
```

## ⚙️ Installation

Clone the repository:

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd ai-scientist
```

Create a virtual environment:

### Windows

```powershell
python -m venv .venv
.venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## 🔑 API Key Setup

AI Scientist currently uses Groq for model inference.

Create a Groq API key and configure it as an environment variable.

### Local development

Create a `.env` file:

```text
GROQ_API_KEY=your_groq_api_key_here
```

**Never commit `.env` to GitHub.**

Your `.gitignore` should include:

```text
.env
.venv/
__pycache__/
*.pyc
```

## ▶️ Run Locally

Start Streamlit:

```bash
streamlit run app.py
```

Streamlit will provide a local URL, typically:

```text
http://localhost:8501
```

Open it in your browser and enter a research question.

## ☁️ Streamlit Deployment

The application can be deployed using Streamlit Community Cloud.

Connect your GitHub repository and select:

```text
app.py
```

For the API key, use Streamlit's Secrets configuration rather than committing the key to GitHub.

Add:

```toml
GROQ_API_KEY = "your_groq_api_key_here"
```

## 🧪 Example Research Question

Try something like:

```text
Can Random Forest outperform a single Decision Tree
on the Iris dataset?
```

The system may produce a workflow similar to:

```text
1. Search scientific literature
2. Generate hypotheses
3. Select a hypothesis
4. Generate an experiment
5. Run the Python experiment
6. Analyze the results
7. Generate a research report
```

## 🧠 Example Output

A generated experiment might compare:

```text
Majority Class Baseline
        ↓
Decision Tree
        ↓
Random Forest
```

and report metrics such as:

```text
Mean accuracy
Standard deviation
Model comparison
Experimental interpretation
```

## ⚠️ Prototype Status

This project is an **experimental prototype**, not a fully autonomous scientific discovery system.

AI-generated experiments can contain:

* Syntax errors
* Incorrect assumptions
* Statistical mistakes
* Invalid experimental designs
* Incorrect interpretations
* Dependency issues

Generated code should therefore be reviewed before being trusted for serious research.

The current prototype also executes AI-generated Python locally, so **do not use it with untrusted prompts or production systems without adding stronger sandboxing and security controls**.

## 🛠️ Roadmap

Potential future improvements include:

* [ ] Better experiment planning
* [ ] Automatic experiment iteration
* [ ] More robust code validation
* [ ] Sandboxed code execution
* [ ] Statistical significance testing
* [ ] More scientific databases
* [ ] Citation management
* [ ] Automatic literature synthesis
* [ ] Experiment reproducibility
* [ ] Research paper generation
* [ ] Persistent experiment database
* [ ] Multi-agent research workflows
* [ ] Visualization of experimental results
* [ ] Human approval checkpoints
* [ ] Docker-based experiment isolation

## 🎯 Long-Term Vision

The long-term goal is to explore an AI system that can assist researchers across the entire experimental loop:

```text
Question
   ↓
Research
   ↓
Hypothesis
   ↓
Experiment
   ↓
Results
   ↓
Analysis
   ↓
New Hypothesis
   ↓
New Experiment
   ↺


Rather than simply answering questions, the system is designed to **form hypotheses, test them, learn from results, and iterate**.

## 🤝 Contributing

Contributions, ideas, experiments, and improvements are welcome.

If you find a bug or have an idea for improving the research loop, open an issue or submit a pull request.

## 📜 License

Choose a license for the project before publishing it publicly.

For example, if you want a permissive open-source license, you can use the MIT License.

---

**AI Scientist is an ongoing experiment in AI-assisted scientific discovery.** 🧪🤖
