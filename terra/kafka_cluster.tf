# ------------------------------------------------------------------------------
# Kafka Cluster Module Configuration
#
# This file defines a reusable module for deploying a Kafka cluster on AWS using
# the Confluent AWS Kafka Terraform module. All key parameters are exposed as
# variables for flexibility and reusability.
# ------------------------------------------------------------------------------

module "kafka_cluster" {
  # Source of the module (Terraform Registry)
  source  = "confluentinc/cp-aws/kafka"
  version = "1.3.1" # Pin to a specific version for reproducibility

  # Cluster settings
  cluster_name       = var.cluster_name         # Name of the Kafka cluster
  kafka_version      = "3.6.0"                 # Kafka version to deploy
  broker_count       = var.broker_count         # Number of Kafka brokers
  zookeeper_count    = 3                        # Number of Zookeeper nodes (fixed)

  # EC2 instance and storage settings
  instance_type      = var.instance_type        # EC2 instance type for brokers
  volume_size        = var.volume_size          # EBS volume size in GB
  volume_type        = "gp3"                   # EBS volume type (gp3 recommended)
  subnet_ids         = var.subnet_ids           # List of subnet IDs for brokers
  availability_zones = var.availability_zones   # List of availability zones

  # Networking and security
  vpc_id             = var.vpc_id               # VPC ID for the cluster
  ssh_key_name       = var.ssh_key_name         # SSH key for EC2 access
  enable_tls         = true                     # Enable TLS encryption (recommended)

  # Custom Kafka configuration (tune as needed)
  kafka_custom_configs = {
    "num.partitions"                = var.default_partitions         # Default partitions per topic
    "default.replication.factor"    = var.replication_factor         # Default replication factor
    "log.retention.hours"           = var.retention_hours            # Log retention in hours
    "log.segment.bytes"             = 1073741824                     # Log segment size (1GB)
    "log.retention.check.interval.ms" = 300000                       # How often to check for log retention (ms)
  }

  # Resource tags for cost allocation, ownership, etc.
  tags = var.tags
}

# ------------------------------------------------------------------------------
# Variable Definitions
# ------------------------------------------------------------------------------

# Name of the Kafka cluster
variable "cluster_name" {}

# Number of Kafka brokers (minimum 3 for production)
variable "broker_count" {
  default = 3
}

# EC2 instance type for brokers (adjust for workload)
variable "instance_type" {
  default = "m5.4xlarge"
}

# EBS volume size in GB (adjust for data retention needs)
variable "volume_size" {
  default = 500
}

# Default number of partitions per topic
variable "default_partitions" {
  default = 6
}

# Default replication factor for topics
variable "replication_factor" {
  default = 3
}

# Log retention in hours (default: 7 days)
variable "retention_hours" {
  default = 168  # 7 days
}

# List of subnet IDs for brokers (should span multiple AZs)
variable "subnet_ids" {
  type = list(string)
}

# List of availability zones (should match subnets)
variable "availability_zones" {
  type = list(string)
}

# VPC ID for the cluster
variable "vpc_id" {}

# SSH key name for EC2 access
variable "ssh_key_name" {}

# Map of tags to apply to all resources
variable "tags" {
  type = map(string)
  default = {}
} 