resource "aws_security_group" "web_sg" {
  name        = "devops-web-sg-arnav"
  description = "Security group for web server and SSH administrative access"
  vpc_id      = aws_vpc.main_vpc.id

  # Inbound HTTP (port 80)
  ingress {
    description = "Allow inbound HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Inbound SSH (port 22) restricted to admin CIDR
  ingress {
    description = "Allow inbound SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.admin_cidr]
  }

  # Outbound all
  egress {
    description = "Allow all outbound traffic"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "devops-web-sg-arnav"
  }
}
