import os

import toml
from langchain.chains import LLMChain, RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.prompts.prompt import PromptTemplate
from langchain.vectorstores import Chroma
from termcolor import colored

from snowdev.snow_functions.utils.templates.sproc import TEMPLATE as SPROC_TEMPLATE
from snowdev.snow_functions.utils.templates.streamlit import (
    TEMPLATE as STREAMLIT_TEMPLATE,
)
from snowdev.snow_functions.utils.templates.udf import TEMPLATE as UDF_TEMPLATE
from snowdev.snow_functions.utils.ingest import DocumentProcessor, Secrets, Config


class SnowBot:

    TEMPLATES = {
        "udf": UDF_TEMPLATE,
        "sproc": SPROC_TEMPLATE,
        "streamlit": STREAMLIT_TEMPLATE,
    }

    @staticmethod
    def ai_embed():
        """
        Embed all the documents in the knowledge folder.
        """
        secrets = Secrets(OPENAI_API_KEY=os.environ["OPENAI_API_KEY"])
        config = Config()
        doc_processor = DocumentProcessor(secrets, config)
        try:
            result = doc_processor.process()
            print(colored("✅ Documents have been successfully embedded!", "green"))
            return result
        except Exception as e:
            print(
                colored(f"❌ Error occurred while embedding documents: {str(e)}", "red")
            )
            return None

    @staticmethod
    def get_qa_prompt_for_type(template_type):
        if template_type not in SnowBot.TEMPLATES:
            raise ValueError(f"No template found for component type: {template_type}")
        return PromptTemplate(
            template=SnowBot.TEMPLATES[template_type],
            input_variables=["question", "context"],
        )

    @staticmethod
    def component_exists(component_name, template_type):
        folder_path = os.path.join("src", template_type, component_name)
        return os.path.exists(folder_path)

    @staticmethod
    def get_chain_gpt(db):
        """
        Get a chain for chatting with a vector database.
        """
        llm = ChatOpenAI(
            model_name="gpt-4",
            temperature=0.5,
            openai_api_key=os.environ["OPENAI_API_KEY"],
            max_tokens=500,
        )
        chain = LLMChain(llm=llm, prompt=SnowBot.QA_PROMPT)
        chain = RetrievalQA.from_chain_type(
            llm,
            chain_type="stuff",
            retriever=db.as_retriever(),
            chain_type_kwargs={"prompt": SnowBot.QA_PROMPT},
        )
        return chain

    @staticmethod
    def append_dependencies_to_toml(dependencies_dict):
        """
        Append new dependencies to app.toml file.
        """
        toml_path = "app.toml"

        if not os.path.exists(toml_path):
            print(colored(f"⚠️ {toml_path} does not exist!", "yellow"))
            return

        with open(toml_path, "r") as f:
            data = toml.load(f)

        for key, value in dependencies_dict.items():
            data["tool.poetry.dependencies"][key] = value

        with open(toml_path, "w") as f:
            toml.dump(data, f)

    @staticmethod
    def create_new_ai_component(component_name, prompt, template_type):
        # Ensure that the template_type is valid
        if template_type not in SnowBot.TEMPLATES:
            print(
                colored(
                    f"⚠️ Template type {template_type} is not recognized.", "yellow"
                )
            )
            return

        SnowBot.QA_PROMPT = SnowBot.get_qa_prompt_for_type(template_type)

        # Check if the component already exists
        if SnowBot.component_exists(component_name, template_type):
            print(
                colored(
                    f"⚠️ {template_type.upper()} named {component_name} already exists!",
                    "yellow",
                )
            )
            return

        # Embedding and retrieving the content
        embeddings = OpenAIEmbeddings(
            openai_api_key=os.environ["OPENAI_API_KEY"], model="text-embedding-ada-002"
        )
        vectordb = Chroma(persist_directory="chroma_db", embedding_function=embeddings)
        chain = SnowBot.get_chain_gpt(vectordb)
        response_content = chain(prompt)["result"]
        response_content = response_content.split("```python\n")[1].split("\n```")[0]

        component_folder = os.path.join("src", template_type, component_name)
        os.makedirs(component_folder, exist_ok=True)

        filename = "app.py"
        if template_type == "streamlit":
            filename = "streamlit_app.py"

        with open(os.path.join(component_folder, filename), "w") as f:
            f.write(response_content)

        dependencies = {"some-library": "1.0.0", "another-library": "2.0.1"}
        SnowBot.append_dependencies_to_toml(dependencies)

        print(
            colored(
                f"✅ {template_type.upper()} {component_name} generated successfully using AI!",
                "green",
            )
        )
