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

- `PUBLIC`: Amazon-issued public certificate. DNS or EMAIL validation supported. Optional Route53 validation record creation.
- `PRIVATE`: Certificate issued from an existing AWS Private CA. The CA itself is not created by this module.
- `IMPORTED`: External PEM certificate, private key, and optional certificate chain imported into ACM.

## Important security note for imported certificates

Imported certificate material, including the private key, is written to Terraform state by the AWS provider. Protect remote state using encryption and strict access controls. Do not commit private keys to Git.

## Public example

```hcl
module "acm" {
  source = "git::ssh://git@github.company.com/terraform-modules/terraform-aws-acm.git?ref=v1.0.0"

  providers = {
    aws     = aws
    aws.dns = aws.dns
  }

  certificate_type = "PUBLIC"
  domain_name       = "app.example.com"
  validation_method = "DNS"
  route53_zone_id   = "Z0123456789ABCDEFG"

  create_route53_records = true
  wait_for_validation    = true
}
```

## Private example

```hcl
module "acm" {
  source = "git::ssh://git@github.company.com/terraform-modules/terraform-aws-acm.git?ref=v1.0.0"

  providers = {
    aws     = aws
    aws.dns = aws.dns
  }

  certificate_type          = "PRIVATE"
  domain_name               = "api.internal.example.com"
  certificate_authority_arn = var.private_ca_arn
}
```

## Imported example

```hcl
module "acm" {
  source = "git::ssh://git@github.company.com/terraform-modules/terraform-aws-acm.git?ref=v1.0.0"

  providers = {
    aws     = aws
    aws.dns = aws.dns
  }

  certificate_type = "IMPORTED"
  certificate_body  = var.certificate_body
  private_key       = var.private_key
  certificate_chain = var.certificate_chain
}
```

## Outputs

The primary output for consuming repositories is:

```hcl
module.acm.certificate_arn
```
