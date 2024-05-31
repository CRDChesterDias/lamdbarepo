# lamdbarepo


provider "aws" {
  region                   = "us-east-1"
  access_key               = ""
  secret_key               = ""
}

resource "tls_private_key" "privatekey" {
  for_each = local.key_pairs

  algorithm = "RSA"
  rsa_bits  = 4096
}

resource "local_file" "private_key" {
  for_each = tls_private_key.privatekey

  filename = "/Users/chesterdias/Documents/platform-deployment/${each.key}.pem"  # Set the desired local path and filename for each PEM file
  content  = each.value.private_key_pem
}

locals {
  key_pairs = {
    key1 = "test1"
    key2 = "test2"
  }
}
