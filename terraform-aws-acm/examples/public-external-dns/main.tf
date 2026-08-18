terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.0, < 7.0"
    }
  }
}

provider "aws" {
  region = "us-east-2"
}

module "acm" {
  source = "../../"

  certificate_type = "PUBLIC"

  domain_name = "acm-test.chesterdias.com"

  subject_alternative_names = []

  create_route53_records = false

  # Do not wait because the DNS record must first
  # be created with the external DNS provider.
  wait_for_validation = false

  key_algorithm = "RSA_2048"

  tags = {
    Environment = "test"
    Application = "acm-module-test"
    DNSProvider = "External"
  }
}

output "certificate_arn" {
  description = "ARN of the requested ACM certificate."
  value       = module.acm.certificate_arn
}

output "certificate_status" {
  description = "Current ACM certificate status."
  value       = module.acm.status
}

output "domain_validation_options" {
  description = "DNS CNAME records that must be created with the external DNS provider."
  value       = module.acm.domain_validation_options
}