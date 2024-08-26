import tempfile

from fastapi import UploadFile
from langchain.chains import RetrievalQA
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

MODEL = "gpt-4o-mini"


class ResumeExtractor:
    def __init__(self, resume: UploadFile):
        self.resume = resume
        self.chain = None

    async def setup(self):
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(await self.resume.read())
            tmp_file_path = tmp_file.name

        loader = PyPDFLoader(file_path=tmp_file_path)
        documents = loader.load()

        embeddings = OpenAIEmbeddings()
        pdfsearch = Chroma.from_documents(documents, embeddings)

        self.chain = RetrievalQA.from_llm(
            ChatOpenAI(temperature=0, model=MODEL),
            retriever=pdfsearch.as_retriever(search_kwargs={"k": 1}),
            return_source_documents=True,
        )

    def extract_skills(self):
        PROMPT = """
        This resume belongs to a candidate applying for an engineering role.
        Extract the most prominent skills relevant to this role from the resume.
        Provide the skills as a comma-separated list.
        If no relevant skills are found, return an empty string.
        Do not include any additional explanations.

        Response Format: Skill1, Skill2, Skill3

        Sample Response: Python, Javascript, AWS
        """
        try:
            chain_response = self.chain({"query": PROMPT})
        except Exception as e:
            print(e)
            return []

        try:
            skills = chain_response["result"].split(", ")
            return skills
        except Exception as e:
            print(e)
            return []

    def extract_name(self):
        PROMPT = """
        Extract the candidate's name from the resume. The name should be formatted as "Firstname Lastname" or 
        "Firstname M. Lastname" (if a middle name is present). Ensure there are no special characters or extra text.

        Response Format:
            "Firstname Lastname"
            "Firstname M. Lastname" (if a middle name is present)
        If no name is found, return an empty string. Do not provide any explanations.

        Sample Response: Siddharth Prajosh
        """
        try:
            chain_response = self.chain({"query": PROMPT})
        except Exception as e:
            print(e)
            return ""

        try:
            name = chain_response["result"].strip('"')
            return name
        except Exception as e:
            print(e)
            return ""

    def extract_email(self):
        PROMPT = """
        Given the document, identify and extract any email address present within the content.
        The email address will contain the '@' symbol and may include alphanumeric characters, dots, hyphens, and underscores. 
        If there is more than one email address, extract the first one. If no email address is found, return an empty string. 
        Do not provide any additional explanations or text other than the extracted email(s).

        Sample Response: 8V0Z8@example.com
        """
        try:
            chain_response = self.chain({"query": PROMPT})
        except Exception as e:
            print(e)
            return ""

        try:
            email = chain_response["result"].strip('"')
            return email
        except Exception as e:
            print(e)
            return ""

    def run(self, extract_name=False, extract_email=False, extract_skills=False):
        return {
            "name": self.extract_name() if extract_name else None,
            "email": self.extract_email() if extract_email else None,
            "skills": self.extract_skills() if extract_skills else None,
        }
