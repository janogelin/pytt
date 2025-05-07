# nginx_autoscale.tf
#
# Terraform configuration to launch 100 t2.micro EC2 instances running nginx in AWS using Auto Scaling.
# - Uses lifecycle to prevent destroy
# - Auto Scaling Group: min 100, max 1000, desired 100
# - Health check healthy percentage: 100
# - Stubs for user data and security groups
# - Example resource names

provider "aws" {
  region = var.aws_region
}

resource "aws_launch_template" "nginx" {
  name_prefix   = "nginx-example-"
  image_id      = var.ami_id # e.g., Amazon Linux 2 AMI
  instance_type = "t2.micro"

  user_data = base64encode(<<-EOF
    #!/bin/bash
    # Install nginx (stub)
    # yum update -y
    # amazon-linux-extras install nginx1 -y
    # systemctl start nginx
    # systemctl enable nginx
    # Add more setup as needed
  EOF
  )

  vpc_security_group_ids = [aws_security_group.nginx_sg.id]

  lifecycle {
    prevent_destroy = true
  }
}

resource "aws_security_group" "nginx_sg" {
  name        = "nginx-example-sg"
  description = "Allow HTTP and SSH (stub)"
  vpc_id      = var.vpc_id

  # Stub: open HTTP (80) and SSH (22) to anywhere (not for production!)
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_autoscaling_group" "nginx_asg" {
  name                      = "nginx-example-asg"
  min_size                  = 100
  max_size                  = 1000
  desired_capacity          = 100
  vpc_zone_identifier       = var.subnet_ids
  health_check_type         = "EC2"
  health_check_grace_period = 300

  launch_template {
    id      = aws_launch_template.nginx.id
    version = "$Latest"
  }

  # Set the healthy percentage to 100% for rolling updates
  instance_refresh {
    strategy = "Rolling"
    preferences {
      min_healthy_percentage = 100
    }
  }

  tag {
    key                 = "Name"
    value               = "nginx-autoscale-instance"
    propagate_at_launch = true
  }

  lifecycle {
    prevent_destroy = true
  }
}

# Variables (stub values, override in terraform.tfvars or CLI)
variable "aws_region" {
  description = "AWS region to deploy to"
  type        = string
  default     = "us-east-1"
}

variable "ami_id" {
  description = "AMI ID for EC2 instances (e.g., Amazon Linux 2)"
  type        = string
  default     = "ami-0c02fb55956c7d316" # Example for us-east-1
}

variable "vpc_id" {
  description = "VPC ID to launch instances in"
  type        = string
}

variable "subnet_ids" {
  description = "List of subnet IDs for the ASG"
  type        = list(string)
} 