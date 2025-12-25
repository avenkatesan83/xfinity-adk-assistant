Add a .env file with below configurations in the root level of your project directory.

GOOGLE_GENAI_USE_VERTEXAI=
GOOGLE_API_KEY=
LOCATION_ID=
PROJECT_ID=
TEMPLATE_ID=<model_armor_template_id>
FAQ_DATA_STORE_ID=<datastore_id>

**Important** At this moment, Google Reasoning Engine (Vertex AI Agent Engine) is available in "us-central1" region only.

**Pre-requisities:**

Model armor template
Datastore AI App
Vertex Agent Engine

**To create a vertex agent engine:**
    Run a command in the bash terminal "python -m utils.vertextaiutils" from the root directory of this project.