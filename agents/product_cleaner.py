from langgraph.graph import StateGraph, START, END
from schemas.schema import RawProduct, CleanedProduct
from langchain_groq import ChatGroq
import json
from utils.tools import extract_json
from typing import TypedDict
import os
from dotenv import load_dotenv

load_dotenv()

class ProductCleaner(TypedDict):
  raw_product: dict
  cleaned_product: dict

def missing_fields(state: ProductCleaner) -> ProductCleaner:
  """
  Check for missing fields in the raw product.
  """
  raw = state['raw_product']
  validate_raw = RawProduct(**raw)
  json_data = json.dumps(validate_raw.model_dump(), indent=2)
  prompt = (
    "The following product data is missing some fields. "
    "You are a product cleaner. Please identify which fields are missing and fill them. "
    "Return a JSON object with filled fields.\n\n"
    f"Product Data: {json_data}"
)

  llm = ChatGroq(model="gemma2-9b-it")
  response = llm.invoke(prompt)
  clean_data_dict = response.content.strip()
  clean_data_dict = extract_json(clean_data_dict)
  validate_clean = CleanedProduct(**clean_data_dict)

  return {"cleaned_product": validate_clean.model_dump()}


def AgentCleaner():
  graph = StateGraph(ProductCleaner)

  graph.add_node("Missing Fields", missing_fields)

  graph.add_edge(START, "Missing Fields")
  graph.add_edge("Missing Fields", END)
  return graph.compile()
   
