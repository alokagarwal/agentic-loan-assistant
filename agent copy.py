from bedrock_agentcore import BedrockAgentCoreApp
from loan_assistant.graph import graph

app = BedrockAgentCoreApp()

@app.entrypoint
def invoke(payload):
    return graph.invoke({
        "application_id": payload.get("application_id", "A1"),
        "loan_amount": payload.get("loan_amount", 10000),
        }) 

if __name__ == "__main__":
    app.run()