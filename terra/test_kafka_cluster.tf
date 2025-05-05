locals {
  example_tags = {
    Environment = "test"
    Owner       = "localuser"
  }
}

module "kafka_cluster" {
  source  = "confluentinc/cp-aws/kafka"
  version = "1.3.1"

  cluster_name       = "local-kafka-test"
  kafka_version      = "3.6.0"
  broker_count       = 3
  zookeeper_count    = 3

  instance_type      = "m5.4xlarge"
  volume_size        = 500
  volume_type        = "gp3"
  subnet_ids         = ["subnet-12345678", "subnet-23456789", "subnet-34567890"]
  availability_zones = ["us-west-2a", "us-west-2b", "us-west-2c"]

  vpc_id             = "vpc-12345678"
  ssh_key_name       = "my-ssh-key"
  enable_tls         = true

  kafka_custom_configs = {
    "num.partitions"           = 6
    "default.replication.factor" = 3
    "log.retention.hours"      = 168
    "log.segment.bytes"        = 1073741824
    "log.retention.check.interval.ms" = 300000
  }

  tags = local.example_tags
} 