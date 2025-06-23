# **FilterFlow AI: Intelligent Customer Service & Security**

**FilterFlow AI** is a cutting-edge, multi-agent AI system designed to revolutionize customer service interactions by intelligently handling abusive, prank, and potentially malicious interactions. It acts as a smart digital guardian, ensuring human agents focus their valuable time on legitimate, high-priority customer needs.

This project was initiated using the [`googleCloudPlatform/agent-starter-pack`]([https://github.com/GoogleCloudPlatform/agent-starter-pack](https://github.com/GoogleCloudPlatform/agent-starter-pack)) version `0.6.4` and developed based on its core architectural principles.

## **Project Story**

### **About the Project: Our Digital Bouncer for Customer Service**

Tired of draining valuable human potential on frustrating, off-topic, or even outright abusive customer interactions? So were we! **FilterFlow AI** is our answer: a smart, adaptive digital assistant designed to protect your team, streamline conversations, and ensure every customer experience is as smooth and productive as possible. We're transforming chaotic customer service into a clear, efficient flow.

### **What Inspired Us: The Fight for Efficiency and Sanity**

The inspiration for FilterFlow AI sparked from the raw frustration of seeing valuable human time and energy drained by interactions that go nowhere, or worse – by malicious actors probing for vulnerabilities. We wanted to build an AI that doesn't just answer questions, but **actively protects, filters, and optimizes** the entire customer service ecosystem, empowering humans by handling the "noise" so they can focus on the "signal."

### **How We Built It: A Multi-Agent Masterpiece**

FilterFlow AI's brain is a modular, multi-agent system, conceptualized and structured around the principles of the **Google Agent Development Kit (ADK)**. Our core components work in harmony:

* **`MainRouterAgent`:** The Maestro, directing the conversation flow, making adaptive decisions.
* **`AbuseDetectionAgent`:** Our vigilant watchdog, sniffing out problematic language and prank attempts.
* **`StandardQueryAgent`:** The ever-helpful assistant, ready to provide concise answers to legitimate questions.
* **`CustomerProfileTool` (Mocked):** Our memory, allowing the system to differentiate between a valued customer and a repeat troublemaker.

The system intelligently processes each interaction, making real-time decisions: offering grace, issuing firm warnings, re-steering off-topic chats, or even initiating an "AI-Only" mode for persistent issues. This dynamic adaptation is what makes FilterFlow AI a game-changer.

### **What We Learned: The Trials, Tribulations, and Triumphs of AI Development**

This project was a masterclass in resilience! We dove deep into the nuances of Python environments, `gcloud` CLI configurations, and the intricate dance of API authentication. The biggest takeaway? **Persistence pays off, even when the tech gods conspire!** We learned that sometimes, the most challenging part isn't the AI logic itself, but getting the underlying tools to simply "play nice."

### **The Challenges We Faced: A Bug-Hunt for the Ages**

Our journey was a gauntlet of unexpected environmental hurdles. We encountered a cascade of issues, each seemingly more stubborn than the last:

* **Python Environment Chaos:** Persistent `ModuleNotFoundError` for ADK and local modules, despite confirmed installations and multiple virtual environment rebuilds. This indicated a deeply unusual interaction within our specific local setup.
* **Google Cloud Authentication Labyrinth:** Errors like "JSON key file not found" (even when verified), "403 Permission denied" due to misaligned quota projects, and "404 Publisher Model not found" when trying to access Gemini, highlighting complex authentication and API availability challenges.

**Our Solution to These Challenges:**
To deliver a functional demonstration, we made strategic adaptations: we streamlined our `app/agent.py` to contain the core AI logic as a standalone application, **bypassing the direct `google-adk` framework dependency for the local demo** due to insurmountable environment issues. We also **mocked the calls to the Gemini API** within our `demo_runner.py` script to ensure the demonstration runs flawlessly. This approach ensures you can fully experience the project's intelligence, despite the underlying environmental quirks.

---

## **Project Structure**

This project is organized as follows:

filter-flow-ai/
├── app/                 # Core application code (includes agent definitions and local tools)
│   ├── agent.py         # Main agent logic for FilterFlow AI
│   ├── agent_engine_app.py # Agent Engine application logic (for intended deployment)
│   └── tools/           # Local utility modules (e.g., customer_profile_tool.py)
│   └── utils/           # Other utility functions and helpers
├── deployment/          # Infrastructure and deployment scripts (for intended GCP deployment)
├── notebooks/           # Jupyter notebooks for prototyping and evaluation
├── tests/               # Unit, integration, and load tests
├── Makefile             # Makefile for common commands (note: some require direct command execution on Windows)
└── pyproject.toml       # Project dependencies and configuration


## **Requirements (for running the demo)**

Before you begin, ensure you have:
* **Python 3.11** (from `python.org` with "Add to PATH" checked)
* **`uv`**: Python package manager - [Install](https://docs.astral.sh/uv/getting-started/installation/)
* **Google Cloud SDK (`gcloud CLI`)**: For GCP services and authentication - [Install](https://cloud.google.com/sdk/docs/install)

## **Quick Start (Local Demonstration of FilterFlow AI's Core Logic)**

This section guides you through setting up and running the command-line demo of FilterFlow AI.

1.  **Clone the Repository:**
    ```bash
    git clone [YOUR_GITHUB_REPO_URL_HERE]
    cd filter-flow-ai
    ```
2.  **Initialize & Activate Python Environment:**
    * Delete any existing virtual environments for a clean start:
        ```bash
        rmdir /s /q venv
        rmdir /s /q .venv
        ```
    * Create and install project dependencies using `uv`:
        ```bash
        uv sync --dev --extra jupyter --frozen
        ```
    * Activate the correct virtual environment:
        ```bash
        .\.venv\Scripts\activate
        ```
        (Your prompt should now start with `(filter-flow-ai)`)
3.  **Authenticate to Google Cloud (for API calls):**
    * Ensure your `gcloud CLI` is installed and updated (`gcloud components update`).
    * Log in for Application Default Credentials (ADC) and follow browser prompts:
        ```bash
        gcloud auth application-default login
        ```
    * Set the correct quota project for your credentials (Crucial for correct billing/quota for API calls):
        ```bash
        gcloud auth application-default set-quota-project filter-flow-ai
        ```
    * Clear old environment variables:
        ```bash
        set GOOGLE_APPLICATION_CREDENTIALS=
        ```
    * Set the project ID:
        ```bash
        set GCP_PROJECT_ID="filter-flow-ai"
        ```
        (Make sure `filter-flow-ai` is your actual Google Cloud Project ID)
4.  **Run the Demo:**
    * Execute the demonstration script from the project root:
        ```bash
        python demo_runner.py
        ```
    * The console output will display the full conversation flow, AI responses (simulated), and internal decision-making logs for multiple scenarios. This is your core functional demo.

---

## **Commands (For Development & Intended Deployment)**

*Note: For Windows users, if `make` is not recognized, you may need to manually execute the `uv` or `gcloud` commands listed in the `Makefile` or in the "Quick Start" section above.*

| Command | Description |
| :--- | :--- |
| `uv sync` | Install all required dependencies using `uv`. (Equivalent to `make install`) |
| `uv run adk web --port 8501` | Launch the Streamlit interface for testing agent locally. (Equivalent to `make playground`) |
| `make backend` | **(Intended Deployment)** Deploy agent to Vertex AI Agent Engine. |
| `make test` | Run unit and integration tests. |
| `make lint` | Run code quality checks (codespell, ruff, mypy). |
| `make setup-dev-env` | Set up development environment resources using Terraform. |
| `uv run jupyter lab` | Launch Jupyter notebook for prototyping. |

For full command options and usage, refer to the [Makefile](Makefile).

---

## **FilterFlow AI's Conceptual Architecture (Flowchart Blueprint)**

**(You will create a visual flowchart/diagram based on this description for your presentation/video. It should be a separate image in your submission.)**

Imagine FilterFlow AI as a highly specialized, adaptive assembly line for customer interactions:

1.  **Customer Input (Start):** A customer's message enters the system.
2.  **MainRouterAgent (The Central Brain):** This is the conductor. It grabs the message, consults the customer's "history book" (`CustomerProfileTool`), and prepares for analysis.
3.  **Parallel Analysis (The Listeners):**
    * **Abuse Detection Agent:** Simultaneously analyzes the message for tone (rude, prank, etc.).
    * **Focus Assessment (within MainRouterAgent):** Checks if the conversation is staying on topic or veering suspiciously.
    * **Standard Query Agent (Prepares Response):** Begins formulating a standard answer to the customer's literal query.
4.  **Decision Logic (MainRouterAgent Orchestration):** Based on insights from the listeners, customer history, and conversation turn count, the MainRouterAgent makes a real-time, adaptive decision.
5.  **Adaptive AI Response & Action (Branching Paths):**
    * **Security Alert:** If malicious off-topic content is detected, it triggers an immediate **ESCALATION to Security Specialists**.
    * **Prankster Protocol:** For known pranksters, the AI takes over with a **STRICT ORDER FOCUS**, ready to terminate irrelevance.
    * **Progressive Behavior Management:** For new or unvalued customers, it cycles through **GRACE PERIOD (soft warning)**, then **FORMAL NOTICE (stronger warning)** for repeated abuse, finally leading to **AI-ONLY MODE** or **TERMINATION** if behavior persists and is not business-critical.
    * **Valued Customer Service:** For high-value customers, it offers **PRIORITIZED SERVICE** even with abuse, with firm reminders, ensuring business needs are met.
    * **Conversation Re-steering:** For slight off-topic deviations, a **GENTLE NUDGE** guides the conversation back to core topics.
    * **Standard Assistance:** For genuinely polite and on-topic queries, the AI provides **DIRECT ANSWERS**.
6.  **End Interaction (Log & Store):** Every interaction is logged for review and future analysis.

---

## **Usage (Intended)**

This section describes how the template is *intended* to be used in a broader development and deployment workflow. FilterFlow AI followed this conceptual path, with adjustments made for the demo.

1.  **Prototype:** Build your Generative AI Agent logic using notebooks for guidance. Use Vertex AI Evaluation to assess performance.
2.  **Integrate:** Import your agent into the app by editing `app/agent.py`.
3.  **Test:** Explore your agent functionality using the Streamlit playground with `uv run adk web`. The playground offers features like chat history, user feedback, and various input types, and automatically reloads your agent on code changes. *(Note: For FilterFlow AI's demo, direct command-line testing via `demo_runner.py` was used due to local UI discovery issues.)*
4.  **Deploy:** Set up and initiate CI/CD pipelines, customizing tests as necessary. Refer to the [deployment section](#deployment) for comprehensive instructions. For streamlined infrastructure deployment, simply run `uvx agent-starter-pack setup-cicd`. Currently only supporting Github.
5.  **Monitor:** Track performance and gather insights using Cloud Logging, Tracing, and the Looker Studio dashboard to iterate on your application.

---

## **Deployment (Intended)**

> **Note:** For a streamlined one-command deployment of the entire CI/CD pipeline and infrastructure using Terraform, you can use the [`agent-starter-pack setup-cicd` CLI command]([https://googlecloudplatform.github.io/agent-starter-pack/cli/setup_cicd.html](https://googlecloudplatform.github.io/agent-starter-pack/cli/setup_cicd.html)). Currently only supporting Github.

### Dev Environment

You can test deployment towards a Dev Environment using the following command:

```bash
gcloud config set project <your-dev-project-id>
make backend