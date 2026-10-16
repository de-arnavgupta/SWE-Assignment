output "vpc_id" {
  description = "ID of the provisioned custom VPC"
  value       = aws_vpc.main_vpc.id
}

output "public_subnet_ids" {
  description = "IDs of the public subnets across availability zones"
  value       = aws_subnet.public_subnets[*].id
}

output "ec2_public_ip" {
  description = "Public IPv4 address of the EC2 web instance"
  value       = aws_instance.web_server.public_ip
}

output "ec2_instance_id" {
  description = "Instance ID of the provisioned EC2 instance"
  value       = aws_instance.web_server.id
}

output "s3_bucket_name" {
  description = "Globally unique name of the application S3 bucket"
  value       = aws_s3_bucket.app_bucket.id
}
