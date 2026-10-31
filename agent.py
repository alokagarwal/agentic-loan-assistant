from bedrock_agentcore import BedrockAgentCoreApp
from agentic_loan_assistant.graph import graph

app = BedrockAgentCoreApp()

@app.entrypoint
def invoke(payload: dict):
    return graph.invoke({
        "applicant_id": payload.get("applicant_id", "123"),
        "loan_amount": payload.get("loan_amount", 10000)
    })

if __name__ == "__main__":
    app.run()