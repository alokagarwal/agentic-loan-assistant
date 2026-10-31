import os
from langgraph.graph import StateGraph, START, END
from langchain_aws import ChatBedrockConverse

from .state import (LoanState)

MODEL_ID = os.environ.get("BEDROCK_MODEL_ID", "us.amazon.nova-micro-v1:0")
AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")
llm = ChatBedrockConverse(model_id=MODEL_ID, region_name=AWS_REGION, temperature=0)

def document_agent(state: LoanState) -> dict:
    return {
        "extracted_data": {
            "monthly_income": 4000,
            "monthly_outgoings": 2500,
        },
        "audit_log": ["Document agent processed."]
    }

def affordability_agent(state: LoanState) -> dict:
    monthly_income = state["extracted_data"]["monthly_income"]
    monthly_outgoings = state["extracted_data"]["monthly_outgoings"]
    disposable_income = monthly_income - monthly_outgoings
    return {
        "affordability": {
            "disposable_income": disposable_income,
        },
        "audit_log": ["Affordability agent processed."]
    }

def policy_agent(state: LoanState) -> dict:
    disposable_income = state["affordability"]["disposable_income"]
    monthly_repayment = state["loan_amount"] / 36
    is_affordable = monthly_repayment < disposable_income / 2   

    if is_affordable:
        reason = "Loan is affordable as repayment is less than half of disposable income."
    else:
        reason = "Loan is not affordable as repayment exceeds half of disposable income."

    return {
        "policy_check": {
            "reason": reason,
            "is_affordable": is_affordable,
            "monthly_repayment": round(monthly_repayment, 2)
        },
        "audit_log": ["Policy agent processed."]
    }

def route_after_policy_check(state: LoanState) -> str:
    if state["policy_check"]["is_affordable"]:
        return "supervisor_agent"
    else:
        return "decline_agent"

def supervisor_agent(state: LoanState) -> dict:
    prompt = f"""
You are a loan underwriter assistant for a UK bank reviewing a loan application. 
Write 2-3 sentencesrecommending for a human loan officer.
You recommend only;a numan makes the final decision.
Loan amount : £{state['loan_amount']} 
affordability : {state['affordability']}
Policy check : {state['policy_check']}
"""
    response = llm.invoke(prompt)
    return {
        "recommendation": response.content,
        "audit_log": [f"Supervisor agent processed.(LLM : {MODEL_ID})"]
    }

def decline_agent(state: LoanState) -> dict:
    return {
        "recommendation": "Loan application declined - " + state["policy_check"]["reason"],
        "audit_log": ["Decline agent processed."]
    }

builder = StateGraph(LoanState)

builder.add_node("document_agent", document_agent)
builder.add_node("affordability_agent", affordability_agent)
builder.add_node("policy_agent", policy_agent)
builder.add_node("supervisor_agent", supervisor_agent)
builder.add_node("decline_agent", decline_agent)
builder.add_edge(START, "document_agent")
builder.add_edge("document_agent", "affordability_agent")
builder.add_edge("affordability_agent", "policy_agent")
builder.add_conditional_edges("policy_agent", route_after_policy_check)
builder.add_edge("supervisor_agent", END)
builder.add_edge("decline_agent", END)

graph = builder.compile()


if __name__ == "__main__":
    result = graph.invoke({"applicant_id": "123", "loan_amount": 10000})
    print(result)