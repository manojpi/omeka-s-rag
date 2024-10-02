from langchain.docstore.document import Document
from langgraph.graph import START, END, StateGraph

from typing_extensions import TypedDict
from typing import List

from answer_grader import answer_grader
from generator import rag_chain
from documents_retriever import retriever
from hallucinating_grader import hallucination_grader
from retrieval_grader import retrieval_grader
from utils import web_search_tool

import os


### State
class GraphState(TypedDict):
    """"
    Represents the state of our graph

    Attributes:
        question: question
        generation: LLM generation
        web_search: whether to search in web for documents
        documents: list of documents
    """

    question: str
    generation: str
    web_search: bool
    documents: List[str]


### Nodes
def retrieve(state):
    """
    Retrieve documents from vectorstore

    Args:
        state (dict): The current graph state
    
    Returns:
        state (dict): New key added to state, documents, that contains retrieved documents
    """
    print("--RETRIEVE--")
    question = state["question"]

    # Retrieval
    documents = retriever.invoke(question)
    return {"documents": documents, "question": question}

def grade_documents(state):
    """
    Determines whether the retrieved documents are relevant to the question If any document is not relevant, we
    will set a flag to run web search

    Args:
        state (dict): The current graph state
    
    Returns:
        state (dict): Filtered out irrelevant documents and updated web_search state
    """
    print("--CHECK DOCUMENT RELEVANCE TO QUESTION--")
    question = state["question"]
    documents = state["documents"]

    # Score each docs
    filtered_docs = []
    web_search = False

    for doc in documents:
        score = retrieval_grader.invoke({"question": question, "document": doc.page_content})
        grade = score['score']
        
        # Check document relevant
        if grade.lower() == "yes":
            print("--GRADE: DOCUMENT RELEVANT--")
            filtered_docs.append(doc)
        
        # Document not relevant
        else:
            print("--GRADE: DOCUMENT NOT RELEVANT--")
            # Avoid adding to the filtered docs list
            web_search = True
            continue

    return {"documents": filtered_docs, "question": question, "web_search": web_search}


def generate(state):
    """
    Generate answer using RAG on retrieved documents

    Args:
        state (dict): The current graph state
    
    Returns:
        state (dict): New key added to state, generation, that contains LLM generation
    """
    print("--GENERATE--")
    question = state["question"]
    documents = state["documents"]

    # RAG Generation
    generation = rag_chain.invoke({"context": documents, "question": question})
    return {"documents": documents, "question": question, "generation": generation}
    

def web_search(state):
    """
    Web search based on the question

    Args:
        state (dict): The current graph state
    
    Returns:
        state (dict): Appended web results to documents
    """

    print("--WEB SEARCH--")
    question = state["question"]
    documents = state["documents"]

    # Web search
    docs = web_search_tool.invoke({"query": question})
    web_results = "\n".join([doc["content"] for doc in docs])
    web_results = Document(page_content=web_results)
    if documents is not None:
        documents.append(web_results)
    else:
        documents = [web_results]
    
    return {"documents": documents, "question": question}


### Conditional edge

def decide_to_generate(state):
    """
    Determine whether to generate an answer, or add web search
    Args:
        state (dict): The current graph state
    
    Returns:
        str: Decision for next node
    """

    print("--ACCESS GRADED DOCUMENTS--")
    question = state["question"]
    web_search = state["web_search"]
    filtered_docs = state["documents"]

    if web_search:
        # All documents have been filtered check_relance
        # we will re-generate a new query

        print("--DECISION: ALL DECISIONS ARE NOT RELEVANT TO QUESTION, INCLUDE WEB SEARCH --")
        return "websearch"
    else:
        # We have relevant documents, so generate answer
        print("--DECISION: GENERATE--")
        return "generate"

### Conditional edge

def grade_generation_v_documents_and_question(state):
    """
    Checks for the hallucination in the LLM generation
     Args:
        state (dict): The current graph state
    
    Returns:
        str: Result of hallucination for the LLM generation
    """

    print("--CHECK HALLUCINATIONS--")
    question = state["question"]
    documents = state["documents"]
    generation = state["generation"]

    score = hallucination_grader.invoke({"documents": documents, "generation": generation})
    grade = score["score"]

    # Check hallucination
    if grade.lower() == "yes":
        print("--DECISION: GENERATION IS GROUNDED IN DOCUMENTS--")

        # Check question-answering
        print("--GRADE GENERATION vs QUESTION--")
        score = answer_grader.invoke({"question": question, "generation": generation})
        grade = score["score"]
        if grade.lower() == "yes":
            print("--DECISION: GENERATION ADDRESSES QUESTION---")
            return "useful"
        else:
            print("--DECISION: GENERATION DOES NOT ADDRESS QUESTION--")
            return "not useful"
    else:
        print("--DECISION: GENERATION IS NOT GROUNDED IN DOCUMENTS, RE-TRY--")
        return "not supported"


workflow = StateGraph(GraphState)

# Define nodes
workflow.add_node("websearch", web_search)
workflow.add_node("retrieve", retrieve)
workflow.add_node("grade_documents", grade_documents)
workflow.add_node("generate", generate)

# Build the graph
workflow.set_entry_point("retrieve")
workflow.add_edge("retrieve", "grade_documents")
workflow.add_conditional_edges(
    "grade_documents",
    decide_to_generate,
    {
        "websearch": "websearch",
        "generate": "generate",
    },
)
workflow.add_edge("websearch", "generate")
workflow.add_conditional_edges(
    "generate",
    grade_generation_v_documents_and_question,
    {
        "not supported": "generate",
        "useful": END,
        "not useful": "websearch"
    },
)

custom_graph = workflow.compile()