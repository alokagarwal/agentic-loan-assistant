output "agent_runtime_arn" {
  value = aws_bedrockagentcore_agent_runtime.this.agent_runtime_arn
}

output "code_bucket" {
  value = aws_s3_bucket.code.id
}
