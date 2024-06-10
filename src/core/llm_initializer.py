"""Functions to initialize the language models."""

from typing import Any, Literal

from dotenv import load_dotenv
from langchain.callbacks.tracers import LangChainTracer
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.language_models.llms import BaseLLM
from pydantic import BaseModel, Field

load_dotenv()


def openai_chatter(model: str, ls_project_name: str, kwargs: dict = {}) -> BaseChatModel:
    """This function initializes the OpenAI model with a LangSmith project and
    returns it.

    Args:
        model (str): The model name.
        project_name (str): The name of the project.
        **kwargs: Additional arguments to be passed to the model.

    Returns:
        BaseChatModel: The initialized OpenAI Chat model.

    """
    from langchain_openai import ChatOpenAI

    tracer = LangChainTracer(project_name=ls_project_name)
    return ChatOpenAI(model=model, callbacks=[tracer], **kwargs)


def ollama_chatter(model: str, ls_project_name: str, kwargs: dict = {}) -> BaseChatModel:
    """This function initializes the Ollama model with a LangSmith project and
    returns it.

    Args:
        model (str): The model name.
        project_name (str): The name of the project.
        **kwargs: Additional arguments to be passed to the model.

    Returns:
        BaseChatModel: The initialized Ollama Chat model.

    """
    from langchain_community.chat_models import ChatOllama

    tracer = LangChainTracer(project_name=ls_project_name)

    return ChatOllama(model=model, callbacks=[tracer], **kwargs)


def ollama_llms(model: str, ls_project_name: str, kwargs: dict = {}) -> BaseLLM:
    """This function initializes the Ollama model with a LangSmith project and
    returns it.

    Args:
        model (str): The model name.
        project_name (str): The name of the project.
        **kwargs: Additional arguments to be passed to the model.

    Returns:
        BaseLLM: The initialized Ollama LLM model.

    """
    from langchain_community.llms import Ollama

    tracer = LangChainTracer(project_name=ls_project_name)

    return Ollama(model=model, callbacks=[tracer], **kwargs)


class LLMConfigBuilder(BaseModel):
    """This class is used to build the configuration for the LLM.

    Args:
        family (Literal["openai_chatter", "ollama_chatter"]): The family of the LLM.
        model (Literal["mistral", "llama3", "gpt-3.5-turbo", "gpt-4"]): The model name.
        ls_project_name (str): The name of the LangSmith project.
        llm_args (dict[str, Any]): Additional arguments to be passed to the LLM.

    """

    family: Literal["openai_chatter", "ollama_chatter", "ollama_llms"]
    model: Literal["mistral", "llama3", "gpt-3.5-turbo", "gpt-4", "phi3", "phi3:14b"]
    ls_project_name: str
    llm_args: dict[str, Any] = Field(default_factory=dict)


def llm_retriever(config: LLMConfigBuilder) -> BaseLLM | BaseChatModel:
    """This function calls the specified function based on the input function
    name.

    Args:
        func_name (Literal["openai_chatter", "ollama_chatter"]): The function name to call.

    Returns:
        llm_builder: The function to build the LLM with LangSmith project attached.

    """

    # Dictionary mapping function names to their actual functions
    llm_options = {
        "openai_chatter": openai_chatter,
        "ollama_chatter": ollama_chatter,
        "ollama_llms": ollama_llms,
    }

    # Get the function from the dictionary without calling it
    _llm = llm_options.get(config.family, lambda: ValueError("Invalid function name"))

    return _llm(model=config.model, ls_project_name=config.ls_project_name, kwargs=config.llm_args)
