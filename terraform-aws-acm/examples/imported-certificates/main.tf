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

  certificate_type = "IMPORTED"


  certificate_body  = file("/home/chester/acm-import-test/certificate.pem")
  private_key       = file("/home/chester/acm-import-test/private-key.pem")

  # Optional.
  # Set to null for a self-signed test certificate.
  certificate_chain = null

  name = "test-imported-certificate"

  tags = {
    Environment = "test"
    Application = "acm-module-test"
  }
}

output "certificate_arn" {
  value = module.acm.certificate_arn
}

output "certificate_status" {
  value = module.acm.status
}

output "certificate_type" {
  value = module.acm.certificate_type
}