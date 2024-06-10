""" This script categorizes the products in the dataset 'meli_148.csv'
into 3 categories: 'multiple_units', 'single_unit' or 'package'."""

import pandas as pd
from dotenv import load_dotenv
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.language_models.llms import BaseLLM
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from core import LLMConfigBuilder, llm_retriever

load_dotenv()


def invoke_llm_from_prompt(
    llm: BaseLLM | BaseChatModel, prompt: ChatPromptTemplate, input: dict[str, str]
) -> str:
    """This function takes the input and the prompt, creates a chain with string
    parser for the output and returns the output from the LLM.

    Args:
        llm (BaseLLM | BaseChatModel): The LLM to invoke.
        prompt (ChatPromptTemplate): The prompt to use.
        input (dict[str, str]): The input to the LLM based on the prompt.

    Returns:
        str: The output from the LLM.

    """

    chain = prompt | llm | StrOutputParser()

    return chain.invoke(input)


def categorizer(
    llm: BaseChatModel, prompt: ChatPromptTemplate, title: str, description: str
) -> str:
    """This function takes the title and description of a product and returns
    the category of the product.

    Args:
        llm (BaseChatModel): The LLM to use.
        prompt (ChatPromptTemplate): The prompt to use.
        title (str): The title of the product.
        description (str): The description of the product.

    Returns:
        str: The category of the product. It can be 'multiple_units', 'single_unit' or 'package'.

    """
    return invoke_llm_from_prompt(llm, prompt, {"title": title, "description": description})


if __name__ == "__main__":

    config = LLMConfigBuilder(
        family="ollama_llms", model="phi3:14b", ls_project_name="meli", llm_args={"temperature": 0}
    )

    llm = llm_retriever(config)

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "Usted es un sistema que analiza en español el título de una publicación de un producto que están en venta, y a partir de dicho título debe determinar si es un producto que se vende por unidad o en paquete o varias unidades. También puede ayudarse de la descripción para categorizar el producto. Please response ONLY with 3 of the following categories: 'multiple_units' if the product is sold in multiple units, 'single_unit' if the product is sold in a single unit, 'package' if the product is sold in a package.",
            ),
            ("user", "Titulo:{title} Descripción:{description}"),
        ]
    )

    df = pd.read_csv("meli_148.csv", sep=";")

    df["category"] = df.apply(
        lambda x: categorizer(llm, prompt, x["title"], x["description"]), axis=1
    )

    df.to_csv("meli_148_categorized.csv", sep=";", index=False)
