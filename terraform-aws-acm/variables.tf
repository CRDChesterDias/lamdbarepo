############################################
# Certificate Type
############################################

variable "certificate_type" {
  description = "Certificate type. Supported values: PUBLIC or IMPORTED."

  type    = string
  default = "PUBLIC"

  validation {
    condition = contains(
      [
        "PUBLIC",
        "IMPORTED"
      ],
      upper(var.certificate_type)
    )

    error_message = "certificate_type must be PUBLIC or IMPORTED."
  }
}


############################################
# PUBLIC Certificate
############################################

variable "domain_name" {
  description = "Primary domain name for PUBLIC certificates."
  type        = string
  default     = null
}

variable "subject_alternative_names" {
  description = "Additional DNS names included in the PUBLIC certificate."
  type        = list(string)
  default     = []
}

variable "key_algorithm" {
  description = "Key algorithm used for PUBLIC ACM certificates."

  type    = string
  default = "RSA_2048"

  validation {
    condition = contains(
      [
        "RSA_2048",
        "EC_prime256v1",
        "EC_secp384r1"
      ],
      var.key_algorithm
    )

    error_message = "key_algorithm must be RSA_2048, EC_prime256v1, or EC_secp384r1."
  }
}


############################################
# DNS Validation
############################################

variable "create_route53_records" {
  description = "Whether this module should create ACM DNS validation records in Route53."
  type        = bool
  default     = true
}

variable "route53_zone_id" {
  description = "Route53 hosted zone ID used for ACM DNS validation."
  type        = string
  default     = null
}

variable "route53_record_ttl" {
  description = "TTL for Route53 ACM DNS validation records."

  type    = number
  default = 60

  validation {
    condition = (
      var.route53_record_ttl >= 60 &&
      var.route53_record_ttl <= 86400
    )

    error_message = "route53_record_ttl must be between 60 and 86400 seconds."
  }
}

variable "wait_for_validation" {
  description = "Whether Terraform should wait for ACM DNS validation to complete."
  type        = bool
  default     = true
}

variable "external_validation_record_fqdns" {
  description = "Validation record FQDNs when DNS records are managed outside this module."
  type        = list(string)
  default     = []
}


############################################
# IMPORTED Certificate
############################################

variable "certificate_body" {
  description = "PEM encoded certificate body for IMPORTED certificates."
  type        = string
  default     = null
}

variable "private_key" {
  description = "PEM encoded private key for IMPORTED certificates."

  type      = string
  default   = null
  sensitive = true
}

variable "certificate_chain" {
  description = "PEM encoded certificate chain for IMPORTED certificates."
  type        = string
  default     = null
}


############################################
# Metadata
############################################

variable "name" {
  description = "Friendly name used for the Name tag."
  type        = string
  default     = null
}

variable "tags" {
  description = "Additional tags applied to the ACM certificate."
  type        = map(string)
  default     = {}
}