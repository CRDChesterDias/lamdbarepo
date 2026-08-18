############################################
# ACM Certificate
############################################

resource "aws_acm_certificate" "this" {
  domain_name = local.is_public ? var.domain_name : null

  subject_alternative_names = local.is_public ? var.subject_alternative_names : null

  validation_method = local.is_public ? "DNS" : null

  certificate_body  = local.is_imported ? var.certificate_body : null
  private_key       = local.is_imported ? var.private_key : null
  certificate_chain = local.is_imported ? var.certificate_chain : null

  key_algorithm = local.is_public ? var.key_algorithm : null

  tags = local.tags

  lifecycle {
    create_before_destroy = true

    precondition {
      condition = (
        !local.is_public ||
        (
          var.domain_name != null &&
          trimspace(var.domain_name) != ""
        )
      )

      error_message = "domain_name must be provided for PUBLIC certificates."
    }

    precondition {
      condition = (
        !local.is_imported ||
        (
          var.certificate_body != null &&
          trimspace(var.certificate_body) != ""
        )
      )

      error_message = "certificate_body must be provided for IMPORTED certificates."
    }

    precondition {
      condition = (
        !local.is_imported ||
        (
          var.private_key != null &&
          trimspace(var.private_key) != ""
        )
      )

      error_message = "private_key must be provided for IMPORTED certificates."
    }

    precondition {
      condition = (
        !local.manage_dns_records ||
        var.route53_zone_id != null
      )

      error_message = "route53_zone_id must be provided when this module manages Route53 DNS validation records."
    }
  }
}


############################################
# Route53 DNS Validation
# PUBLIC certificates only
############################################

resource "aws_route53_record" "validation" {
  for_each = local.manage_dns_records ? {
    for dvo in aws_acm_certificate.this.domain_validation_options :
    dvo.domain_name => {
      name   = dvo.resource_record_name
      record = dvo.resource_record_value
      type   = dvo.resource_record_type
    }
  } : {}

  zone_id = var.route53_zone_id

  name = each.value.name
  type = each.value.type

  ttl = var.route53_record_ttl

  records = [
    each.value.record
  ]

  allow_overwrite = true
}


############################################
# ACM Certificate Validation
# PUBLIC certificates only
############################################

resource "aws_acm_certificate_validation" "this" {
  count = (
    local.is_public &&
    var.wait_for_validation
  ) ? 1 : 0

  certificate_arn = aws_acm_certificate.this.arn

  validation_record_fqdns = var.create_route53_records ? [
    for record in aws_route53_record.validation :
    record.fqdn
  ] : var.external_validation_record_fqdns

  lifecycle {
    precondition {
      condition = (
        var.create_route53_records ||
        length(var.external_validation_record_fqdns) > 0
      )

      error_message = "external_validation_record_fqdns must be supplied when DNS validation records are managed outside this module and wait_for_validation = true."
    }
  }
}