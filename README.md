# Security Control Management
The Security Control Management tool is an application which automatically searches for the appropriate controls for a given system.

# Deployment
## Basic Steps
There are some basic requirements for successful deployment of the service. The application consists of two parts the backend in Django (scm_backend) and the frontend in React (scm_frontend)

**Backend**

1. Navigate to the backend folder (scm_backend).
2. Create a virtual environment with `python -m venv env`.
3. Activate this environment with `source env/bin/activate` (Linux) or `./env/Scripts/activate.bat` (Windows).
4. Install the required Python libraries in requirements.txt with `pip install -r ./requirements.txt`
5. Install the language model "en_core_web_sm" with `python -m spacy download en_core_web_sm`.
6. Start the development server with `python manage.py runserver`
7. The backend is now ready.

**Frontend**

1. Navigate to the frontend folder (scm_frontend).
2. Make sure that Node.js and npm is installed (https://docs.npmjs.com/downloading-and-installing-node-js-and-npm).
3. Install the necessary dependencies with `npm install .`
4. Start the frontend application with `npm start`
5. The webpage opens automatically or can be reached via `http://localhost:3000`.
