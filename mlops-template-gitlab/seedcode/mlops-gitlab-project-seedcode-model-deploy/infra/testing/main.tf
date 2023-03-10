module "feature_env"{
    source = "../modules/environment"
    aws_account_number = var.aws_account_number
    service_name = "mll-housing-rf-${var.branch}"
    
    initial_instance_count = tonumber(var.desired_instance_count)
    autoscaling_config = {
        max_instance_count        = 3
        min_instance_count        = 1
        target_scale_in_cooldown  = 200
        target_scale_out_cooldown = 200
        target_cpu_utilization    = 80
    }

    tags = {
      application    = "mll-mlops-test"
      service        = "mll-mlops-test-${var.branch}"
      account        = "mll-dev"
      businessunit   = "machinelearninglab"
      subunit        = "machinelearninglab"
      classification = "internal"
      contact        = "a44e37f5.TUIGroup.onmicrosoft.com@emea.teams.ms"
      version        = "1.0.0"
      env            = "${var.branch}"
    }
}
