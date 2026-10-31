resource "aws_s3_bucket" "code" {
  bucket = "${replace(var.agent_name, "_", "-")}-code-${data.aws_caller_identity.current.account_id}-${var.region}"
}

resource "aws_s3_bucket_versioning" "code" {
  bucket = aws_s3_bucket.code.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_public_access_block" "code" {
  bucket                  = aws_s3_bucket.code.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_object" "code" {
  bucket = aws_s3_bucket.code.id
  key    = "${replace(var.agent_name, "-", "")}/agent.zip"
  source = var.zip_path
  etag   = filemd5(var.zip_path)

  depends_on = [aws_s3_bucket_versioning.code]
}
