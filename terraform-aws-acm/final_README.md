# terraform-aws-acm

Reusable Terraform module for provisioning and managing AWS Certificate Manager (ACM) certificates.

## Scope

This module provisions certificate-related resources only:

- `aws_acm_certificate`
- `aws_acm_certificate_validation` for PUBLIC DNS validation
- `aws_route53_record` only for ACM DNS validation records when explicitly enabled

It does **not** create:

- Route53 hosted zones
- ACM Private CAs
- IAM roles or policies
- ALBs / NLBs / listeners
- API Gateway resources
- CloudFront distributions
- Secrets Manager secrets
- application infrastructure

## Certificate types

- `PUBLIC`: Amazon-issued public ACM certificate using DNS validation. Optional Route53 validation record creation.
- `IMPORTED`: External PEM certificate, private key, and optional certificate chain imported into ACM.

## Important security note for imported certificates

Imported certificate material, including the private key, is written to Terraform state by the AWS provider. Protect remote state using encryption and strict access controls. Do not commit private keys to Git.

## Public example

```hcl
module "acm" {
  source = "git::ssh://git@github.company.com/terraform-modules/terraform-aws-acm.git?ref=v1.0.0"

  certificate_type = "PUBLIC"
  domain_name       = "app.example.com"

  subject_alternative_names = [
    "api.example.com",
    "www.example.com"
  ]

  create_route53_records = true
  route53_zone_id        = "Z0123456789ABCDEFG"
  wait_for_validation    = true

  key_algorithm = "RSA_2048"

  tags = {
    Environment = "prod"
    Application = "customer-portal"
    Owner       = "cloud-platform"
  }
}
```

## Imported example

```hcl
module "acm" {
  source = "git::ssh://git@github.company.com/terraform-modules/terraform-aws-acm.git?ref=v1.0.0"

  certificate_type  = "IMPORTED"
  certificate_body  = var.certificate_body
  private_key       = var.private_key
  certificate_chain = var.certificate_chain

  name = "external-certificate"

  tags = {
    Environment = "prod"
    Application = "customer-portal"
  }
}
```

Imported certificates do not require ACM DNS validation.

## External DNS example

If DNS is managed outside Route53:

```hcl
module "acm" {
  source = "git::ssh://git@github.company.com/terraform-modules/terraform-aws-acm.git?ref=v1.0.0"

  certificate_type = "PUBLIC"
  domain_name       = "app.example.com"

  create_route53_records = false
  wait_for_validation    = false
}
```

Retrieve the required DNS validation values using:

```hcl
module.acm.domain_validation_options
```

## Outputs

The primary output for consuming repositories is:

```hcl
module.acm.certificate_arn
```

## Requirements

```hcl
terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.0, < 7.0"
    }
  }
}
```

## Security and hardening

- PUBLIC certificates use DNS validation only.
- `create_before_destroy` is enabled for certificate replacement.
- Imported private keys must be treated as secrets.
- Sensitive Terraform values can still be stored in Terraform state.
- Protect remote state with encryption and strict IAM access.
- Do not commit private keys to Git.
- Account-level CIS controls such as IAM, CloudTrail, AWS Config, KMS, Security Hub, GuardDuty, SCPs, and backend protection should be managed outside this module.

## Recommended repository structure

```text
terraform-aws-acm/
├── main.tf
├── variables.tf
├── locals.tf
├── outputs.tf
├── versions.tf
├── README.md
└── examples/
    ├── public-route53/
    │   └── main.tf
    ├── public-external-dns/
    │   └── main.tf
    └── imported/
        └── main.tf
```

## Recommended `.gitignore`

```gitignore
.terraform/
*.tfstate
*.tfstate.*
crash.log
crash.*.log
*.tfplan
tfplan
*.key
*private-key*
*.pfx
*.p12
examples/imported/certs/
*.auto.tfvars
*.auto.tfvars.json
```
