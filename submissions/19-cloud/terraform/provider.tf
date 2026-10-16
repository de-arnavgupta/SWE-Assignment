terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.5"
    }
  }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project     = "Cloud-Terraform-Project"
      Environment = var.environment
      Owner       = "Arnav Gupta"
      StudentId   = "24bcs10063"
      ManagedBy   = "Terraform"
    }
  }
}
