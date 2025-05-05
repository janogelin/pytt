# Terraform Kafka Cluster Module (`terra`)

This directory contains Terraform configuration for deploying a production-ready Apache Kafka cluster on AWS using the [confluentinc/cp-aws/kafka](https://registry.terraform.io/modules/confluentinc/cp-aws/kafka/latest) module. It includes a parameterized module definition and a local test/example configuration.

---

## Contents
- `kafka_cluster.tf`: Main module and variable definitions for a Kafka cluster
- `test_kafka_cluster.tf`: Example/test configuration with sample values for local validation

---

## Features
- **Modular**: Uses the official Confluent AWS Kafka module
- **Configurable**: All key parameters (instance type, broker count, partitions, etc.) are exposed as variables
- **Secure**: TLS enabled by default
- **Customizable**: Passes custom Kafka configs and tags
- **Testable**: Includes a local test/example for `terraform plan` and `terraform validate`

---

## Usage

### 1. Main Module (`kafka_cluster.tf`)
This file defines the Kafka cluster module and all required variables. You can use it as a template for your own infrastructure.

### 2. Local Test (`test_kafka_cluster.tf`)
This file provides example values for all variables, allowing you to run:

```sh
cd terra
terraform init
terraform validate
terraform plan
```

> **Note:** The test file uses placeholder subnet IDs, VPC ID, and SSH key. Replace these with real values for actual deployment.

---

## Variables

- `cluster_name`: Name of the Kafka cluster
- `broker_count`: Number of Kafka brokers (default: 3)
- `instance_type`: EC2 instance type for brokers (default: `m5.4xlarge`)
- `volume_size`: EBS volume size in GB (default: 500)
- `default_partitions`: Default number of partitions per topic (default: 6)
- `replication_factor`: Default replication factor (default: 3)
- `retention_hours`: Log retention in hours (default: 168)
- `subnet_ids`: List of subnet IDs for brokers
- `availability_zones`: List of availability zones
- `vpc_id`: VPC ID
- `ssh_key_name`: Name of the SSH key for EC2 access
- `tags`: Map of tags to apply to resources

---

## Example: Minimal Customization

```hcl
module "kafka_cluster" {
  source  = "confluentinc/cp-aws/kafka"
  version = "1.3.1"

  cluster_name       = "my-kafka-prod"
  broker_count       = 5
  instance_type      = "m5.2xlarge"
  volume_size        = 1000
  subnet_ids         = ["subnet-abc", "subnet-def", "subnet-ghi"]
  availability_zones = ["us-east-1a", "us-east-1b", "us-east-1c"]
  vpc_id             = "vpc-abc"
  ssh_key_name       = "prod-key"
  tags = {
    Environment = "production"
    Owner       = "team"
  }
}
```

---

## Prerequisites
- [Terraform](https://www.terraform.io/downloads.html) >= 1.0
- AWS credentials with permissions to create VPC, EC2, EBS, and related resources
- Valid subnet IDs, VPC ID, and SSH key in your AWS account

---

## Best Practices
- **State Management**: Use remote state (e.g., S3 + DynamoDB) for production
- **Secrets**: Never commit secrets or sensitive values to version control
- **Review**: Always review the plan before applying changes
- **Module Versioning**: Pin module versions for reproducibility
- **Tagging**: Use tags for cost allocation and resource tracking

---

## References
- [Confluent AWS Kafka Module](https://registry.terraform.io/modules/confluentinc/cp-aws/kafka/latest)
- [Terraform AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [Confluent Kafka Documentation](https://docs.confluent.io/platform/current/kafka/index.html)

---

## License
Specify your license here (e.g., MIT, Apache 2.0, etc.) 