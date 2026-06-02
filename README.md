# 🥗 AI Nutrition Coach

> A multimodal AI-powered nutrition assistant that analyzes food images, provides nutritional insights, and generates personalized recipe suggestions using a Multi-Agent System (MAS) and Gradio.

---

## 📌 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Agents](#agents)
- [Workflows](#workflows)
- [Setup & Installation](#setup--installation)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Disclaimer](#disclaimer)
- [License](#license)

---

## Overview

AI NourishBot is an intelligent dietary assistant that leverages **Meta's Llama 3.2 90B Vision Instruct** model inside a **Multi-Agent System** to analyze meals from images and deliver:

- Detailed nutritional breakdowns
- Personalized recipe suggestions based on dietary preferences
- Health evaluations and improvement tips

The app is served through a clean **Gradio** web interface, making it accessible to non-technical users with zero setup friction.

---

## Features

| Feature | Description |
|---|---|
| 🍽️ Food Image Analysis | Upload a meal photo; get calories, macros, and micronutrients |
| 🥦 Dietary Filtering | Supports Vegan, Vegetarian, Gluten-Free, and Keto filters |
| 📋 Recipe Generation | Suggests recipes based on detected ingredients and diet restrictions |
| 💡 Health Evaluation | Rates meal healthiness and recommends nutritional improvements |
| 🖥️ Gradio UI | Intuitive, browser-based interface — no coding needed to use |

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     Gradio Frontend                     │
│         (Image Upload + Diet Selector + Workflow)       │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│                   Orchestrator Agent                    │
│      Routes input to the appropriate sub-agents         │
└───────┬─────────────────────────────────┬───────────────┘
        │                                 │
        ▼                                 ▼
┌───────────────────┐         ┌───────────────────────────┐
│  Vision Agent     │         │   Nutrition / Recipe Agent │
│ (Image Analysis)  │────────▶│  (Analysis or Recipe Gen) │
└───────────────────┘         └───────────────────────────┘
        │                                 │
        └─────────────┬───────────────────┘
                      ▼
           ┌─────────────────────┐
           │   Response Builder  │
           │  (Formats Output)   │
           └─────────────────────┘
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| LLM | Meta Llama 3.2 90B Vision Instruct |
| Agent Framework | Multi-Agent System (MAS) |
| Frontend | Gradio |
| Backend | Python / Flask (optional API layer) |
| Hosting | Local / Cloud (e.g., HuggingFace Spaces, IBM Cloud) |

---

## Project Structure

```
ai-nourishbot/
├── agents/
│   ├── orchestrator.py        # Routes requests to sub-agents
│   ├── vision_agent.py        # Handles image analysis via multimodal LLM
│   ├── nutrition_agent.py     # Generates nutritional breakdown
│   └── recipe_agent.py        # Generates recipes based on ingredients + diet
│
├── app/
│   ├── gradio_ui.py           # Gradio interface definition
│   └── flask_api.py           # Optional REST API layer
│
├── utils/
│   ├── diet_filter.py         # Dietary restriction filtering logic
│   ├── prompt_templates.py    # LLM prompt templates per agent
│   └── response_formatter.py  # Formats agent outputs for display
│
├── assets/
│   └── sample_images/         # Sample food images for testing
│
├── tests/
│   ├── test_vision_agent.py
│   ├── test_nutrition_agent.py
│   └── test_recipe_agent.py
│
├── requirements.txt
├── .env.example
└── README.md
```

---

## Agents

### 1. 🎯 Orchestrator Agent
- Receives user input (image + preferences + selected workflow)
- Decides which downstream agents to invoke
- Aggregates results and passes them to the response builder

### 2. 👁️ Vision Agent
- Accepts a food image as input
- Uses Meta's **Llama 3.2 90B Vision Instruct** to identify ingredients and dishes
- Returns a structured list of detected food items

### 3. 🥗 Nutrition Agent
- Takes detected food items as input
- Returns a full nutritional breakdown:
  - Calories
  - Macronutrients: Protein, Carbohydrates, Fats
  - Micronutrients: Vitamins, Minerals
  - Overall health rating and improvement suggestions

### 4. 🍳 Recipe Agent
- Takes detected ingredients + dietary preferences as input
- Filters out restricted ingredients
- Returns 1–3 healthy, easy-to-make recipe suggestions aligned with the user's diet

---

## Workflows

The app supports two selectable workflows:

### 📊 Analysis Workflow
```
Image Upload → Vision Agent → Nutrition Agent → Health Summary
```
Returns: Ingredient list, full nutrient breakdown, health score, and tips.

### 🍽️ Recipe Workflow
```
Image Upload → Vision Agent → Diet Filter → Recipe Agent → Recipe Suggestions
```
Returns: Filtered ingredient list and personalized recipe ideas.

---

## Setup & Installation

### Prerequisites

- Python 3.9+
- API access to Meta Llama 3.2 90B Vision Instruct (e.g., via IBM WatsonX, Replicate, or HuggingFace)

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/your-username/ai-nourishbot.git
cd ai-nourishbot

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment variables
cp .env.example .env
# Edit .env with your API keys and model endpoint

# 5. Launch the app
python app/gradio_ui.py
```

The Gradio interface will be available at `http://localhost:7860`.

### Environment Variables

```env
LLM_API_KEY=your_api_key_here
LLM_MODEL_ENDPOINT=https://your-model-endpoint
LLM_MODEL_ID=meta-llama/llama-3-2-90b-vision-instruct
```

---

## Usage

1. Open the app in your browser at `http://localhost:7860`
2. **Upload** a photo of your meal
3. **Select** a dietary preference (optional): Vegan, Vegetarian, Gluten-Free, Keto
4. **Choose** a workflow: Analysis or Recipe
5. Click **Submit** and receive AI-powered insights

---

## API Reference

If using the optional Flask REST layer:

### `POST /analyze`
Analyze a food image for nutritional content.

**Request:**
```json
{
  "image_base64": "<base64-encoded image>",
  "diet": "vegan",
  "workflow": "analysis"
}
```

**Response:**
```json
{
  "ingredients": ["rice", "broccoli", "tofu"],
  "nutrients": {
    "calories": 420,
    "protein": "18g",
    "carbs": "55g",
    "fat": "10g"
  },
  "health_rating": "8/10",
  "suggestions": ["Add a source of healthy fats like avocado."]
}
```

---

## Disclaimer

The recipes and nutritional suggestions provided by AI NourishBot are generated based on image analysis and automated AI processes. While accuracy and safety are priorities:

- Always review suggested recipes and ingredients before preparation or consumption.
- If you have specific health concerns, dietary restrictions, or allergies, consult a qualified nutritionist or healthcare provider.
- AI recommendations are guidance only — not medical or dietary prescriptions.
- The final responsibility for ensuring recipe safety rests with the user.

---

## License

This project is licensed under the **Apache 2.0 License**. See [LICENSE](LICENSE) for details.

---

> Built with ❤️ using Llama 3.2, Multi-Agent Systems, and Gradio.
>
> TAREK ABUALKHER
