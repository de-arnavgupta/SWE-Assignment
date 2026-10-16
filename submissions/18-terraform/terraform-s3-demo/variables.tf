variable "aws_region" {
  description = "Target AWS deployment region"
  type        = string
  default     = "us-east-1"
}

variable "bucket_prefix" {
  description = "Prefix for the unique S3 lab bucket"
  type        = string
  default     = "devops-lab-arnavgupta"
}

variable "environment" {
  description = "Deployment environment name"
  type        = string
  default     = "lab"
}
