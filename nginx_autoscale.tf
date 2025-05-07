resource "aws_autoscaling_group" "nginx_asg" {
  name                      = "nginx-example-asg"
  min_size                  = 4
  max_size                  = 4
  desired_capacity          = 4
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