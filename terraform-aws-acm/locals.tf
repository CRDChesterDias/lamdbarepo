locals {
  certificate_type = upper(var.certificate_type)

  is_public   = local.certificate_type == "PUBLIC"
  is_imported = local.certificate_type == "IMPORTED"

  manage_dns_records = (
    local.is_public &&
    var.create_route53_records
  )

  certificate_name = coalesce(
    var.name,
    var.domain_name,
    "imported-certificate"
  )

  standard_tags = {
    Name            = local.certificate_name
    ManagedBy       = "Terraform"
    CertificateType = local.certificate_type
  }

  tags = merge(
    local.standard_tags,
    var.tags
  )
}