import os
import json
import re
from dotenv import load_dotenv
from groq import Groq
from typing import TypedDict
from langgraph.graph import StateGraph, END

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

class AgentState(TypedDict):
    input: str
    extracted_json: dict
    missing_fields: list
    final_output: dict

def extract_entities(state: AgentState):
    user_input = state["input"]

    prompt = f"""
You are an AI CRM assistant for pharmaceutical field representatives.

Your task is to extract structured interaction details from the following conversation.

User Input:
{user_input}

Return ONLY valid JSON in this exact format:
{{
  "hcp_name": "",
  "interaction_type": "",
  "product": "",
  "notes": "",
  "sentiment": "",
  "concerns": "",
  "follow_up": ""
}}

Rules:
- If interaction type is not explicitly mentioned, infer one of: Visit, Call, Email, Event
- notes should be a clean summary of the interaction
- sentiment should be one of: Positive, Neutral, Negative
- Keep concerns and follow_up short and clear
- Do not return explanation or markdown
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )

    content = response.choices[0].message.content.strip()

    try:
        json_match = re.search(r"\{.*\}", content, re.DOTALL)
        if json_match:
            extracted = json.loads(json_match.group())
        else:
            extracted = {}
    except Exception:
        extracted = {}

    return {"extracted_json": extracted}

def validate_fields(state: AgentState):
    data = state.get("extracted_json", {})
    required_fields = ["hcp_name", "interaction_type"]
    missing = [field for field in required_fields if not data.get(field)]

    return {"missing_fields": missing}

def finalize_output(state: AgentState):
    data = state.get("extracted_json", {})

    final_data = {
        "hcp_name": data.get("hcp_name", ""),
        "interaction_type": data.get("interaction_type", ""),
        "product": data.get("product", ""),
        "notes": data.get("notes", ""),
        "sentiment": data.get("sentiment", ""),
        "concerns": data.get("concerns", ""),
        "follow_up": data.get("follow_up", ""),
    }

    return {"final_output": final_data}

def build_graph():
    workflow = StateGraph(AgentState)

    workflow.add_node("extract_entities", extract_entities)
    workflow.add_node("validate_fields", validate_fields)
    workflow.add_node("finalize_output", finalize_output)

    workflow.set_entry_point("extract_entities")
    workflow.add_edge("extract_entities", "validate_fields")
    workflow.add_edge("validate_fields", "finalize_output")
    workflow.add_edge("finalize_output", END)

    return workflow.compile()


agent = build_graph()