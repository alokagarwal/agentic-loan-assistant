variable "region" {
  type    = string
  default = "us-east-1"
}

variable "agent_name" {
  type    = string
  default = "agentic_loan_assistant"
}

variable "model_id" {
  description = "Bedrock inference profile ID used by the supervisor agent"
  type        = string
  default     = "us.amazon.nova-micro-v1:0"
}

variable "zip_path" {
  type    = string
  default = "../dist/agent.zip"
}
