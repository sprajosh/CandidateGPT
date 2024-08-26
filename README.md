# CandidateGPT

This is a simple app for tracking Job opportunity and candidates.

This includes a Resume Parser which is built using LLM RAG.

## Running the setup
To run the app, please follow the below steps:
```bash
docker-compose up -d
```
Open http://localhost:8000/docs in your browser.

### Things that have been ignored since this is a demo
- Very simple candidate model. More details like experience, education can be added.
- Handling migrations
- Logging config (have uesd print in multiple places)


### Discarded Approaches
- Read PDF using PyPDFLoader, get text using PyPDFLoader. Pass this text to the LLM as a system prompt and get the response.
  - Reason for discarding: Unreliable for double column resumes without complex logic to combine columns.

### Resume Parser
- Read PDF using PyPDFLoader
- Use Open AI Embeddings
- Use Chroma Vector Store
- Use RetrievalQA
- Use LLM ChatOpenAI


#### PyPDFLoader
- Read PDF using PyPDFLoader
- Didn't put too much thought into this. This works for most resumes. Can experiment with other loaders if needed.

#### Open AI Embeddings
- Using Open AI Embeddings for the since we have OpenAI LLM model.


#### Chroma Vector Store
- Using Chroma for Vector Store since Chroma is very fast for small datasets (one resume in this case) and it's relatively easy to setup for prototyping.


#### LLM RetrievalQA
- Good choice for retriving data from vector db.


### Features
- Opportunities Management: Create, read, update, and delete job opportunities.
- Candidates Management: Create, read, update, and delete candidates.
- Resume Parsing: Upload a PDF resume, extract details using an LLM, and automatically create a candidate record.
- Database: Uses PostgreSQL as the database with SQLAlchemy for ORM.
- Dockerized: The app runs in a Docker container for easy deployment and setup.


### Endpoints
#### Opportunities:
- POST /opportunities/: Create a new job opportunity.
- GET /opportunities/: Get a list of all job opportunities.
- GET /opportunities/{id}: Get a specific job opportunity by ID.
- PUT /opportunities/{id}: Update a job opportunity by ID.
- DELETE /opportunities/{id}: Delete a job opportunity by ID.

#### Candidates:

- POST /candidates/: Create a new candidate.
- GET /candidates/: Get a list of all candidates.
- GET /candidates/{id}: Get a specific candidate by ID.
- PUT /candidates/{id}: Update a candidate by ID.
- DELETE /candidates/{id}: Delete a candidate by ID.

#### Resume Parsing:
- POST /candidates/upload_resume/: Upload a PDF resume, extract details, and create a candidate.
- POST /candidates/{id}/resume/: Upload a PDF resume, extract skills, and update a candidate.
