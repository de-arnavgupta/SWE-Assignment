output "bucket_name" {
  description = "Globally unique name of the provisioned S3 bucket"
  value       = aws_s3_bucket.demo_bucket.id
}

output "bucket_arn" {
  description = "Amazon Resource Name (ARN) of the bucket"
  value       = aws_s3_bucket.demo_bucket.arn
}

output "bucket_region" {
  description = "AWS Region hosting the bucket"
  value       = aws_s3_bucket.demo_bucket.region
}
