#!/usr/bin/env python3

import os
import csv
import requests
import xml.etree.ElementTree as ET
from collections import defaultdict

QUALYS_BASE_URL = os.getenv(
    "QUALYS_BASE_URL",
    ""
)

QUALYS_USERNAME = os.getenv("QUALYS_USERNAME")
QUALYS_PASSWORD = os.getenv("QUALYS_PASSWORD")

# Qualys tag that contains ONLY AWS EC2 assets
AWS_TAG_NAME = os.getenv("QUALYS_AWS_TAG", "AWS-EC2")

OUTPUT_FILE = "qualys_aws_windows_patch_status.csv"

# Qualys Pending Reboot QID
PENDING_REBOOT_QID = "90126"

OPEN_STATUSES = {"NEW", "ACTIVE", "REOPENED", "RE-OPENED"}


def get_session():
    if not QUALYS_USERNAME or not QUALYS_PASSWORD:
        raise RuntimeError(
            "Set QUALYS_USERNAME and QUALYS_PASSWORD environment variables"
        )

    session = requests.Session()
    session.auth = (QUALYS_USERNAME, QUALYS_PASSWORD)

    session.headers.update({
        "X-Requested-With": "Python Qualys AWS Patch Report",
        "User-Agent": "qualys-aws-patch-report/1.0"
    })

    return session


def get_patchable_qids(session):
    """
    Fetch vulnerabilities for which Qualys reports a patch exists.
    """

    print("Fetching patchable QIDs...")

    url = f"{QUALYS_BASE_URL}/api/4.0/fo/knowledge_base/vuln/"

    params = {
        "action": "list",
        "is_patchable": "1",
        "details": "Basic"
    }

    response = session.get(
        url,
        params=params,
        timeout=300
    )

    response.raise_for_status()

    root = ET.fromstring(response.content)

    patchable_qids = set()

    for vuln in root.findall(".//VULN"):
        qid = vuln.findtext("QID")

        if qid:
            patchable_qids.add(qid.strip())

    print(f"Patchable QIDs: {len(patchable_qids)}")

    return patchable_qids


def get_aws_host_detections(session):
    """
    Fetch ONLY hosts tagged as AWS EC2.
    """

    print(f"Fetching hosts with Qualys tag: {AWS_TAG_NAME}")

    url = f"{QUALYS_BASE_URL}/api/5.0/fo/asset/host/vm/detection/"

    payload = {
        "action": "list",

        # Restrict report to AWS
        "tag_set_by": "name",
        "tag_set_include": AWS_TAG_NAME,

        # Latest open vulnerability detections
        "status": "New,Active,Re-Opened",

        # Include informational detections such as reboot state
        "show_igs": "1",

        # Include asset metadata
        "host_metadata": "all",

        "show_results": "0",

        # Disable normal truncation.
        # For very large environments implement pagination.
        "truncation_limit": "0"
    }

    response = session.post(
        url,
        data=payload,
        timeout=600
    )

    response.raise_for_status()

    return ET.fromstring(response.content)


def get_text(node, path, default=""):
    element = node.find(path)

    if element is None or element.text is None:
        return default

    return element.text.strip()


def is_windows(os_name):
    return "windows" in os_name.lower()


def get_hostname(host):

    dns = get_text(host, "DNS")

    if dns:
        return dns

    netbios = get_text(host, "NETBIOS")

    if netbios:
        return netbios

    return "UNKNOWN"


def extract_aws_metadata(host):
    """
    Try to extract AWS metadata if Qualys returned it.

    Exact XML structure can vary depending on subscription,
    connector and API metadata availability.
    """

    instance_id = ""
    account_id = ""
    region = ""

    # Search metadata generically
    for element in host.iter():

        tag = element.tag.upper()

        value = (
            element.text.strip()
            if element.text
            else ""
        )

        if not value:
            continue

        if "INSTANCE_ID" in tag or "INSTANCEID" in tag:
            if value.startswith("i-"):
                instance_id = value

        elif "ACCOUNT_ID" in tag or "ACCOUNTID" in tag:
            account_id = value

        elif "REGION" in tag:
            region = value

    return instance_id, account_id, region


def classify_hosts(root, patchable_qids):

    results = []

    for host in root.findall(".//HOST"):

        os_name = get_text(host, "OS")

        # AWS tag already restricted the dataset.
        # Now restrict further to Windows.
        if not is_windows(os_name):
            continue

        host_id = get_text(host, "ID")
        ip = get_text(host, "IP")
        hostname = get_hostname(host)

        instance_id, aws_account_id, aws_region = \
            extract_aws_metadata(host)

        pending_reboot = False
        missing_patch_qids = []

        for detection in host.findall(".//DETECTION"):

            qid = get_text(detection, "QID")

            status = get_text(
                detection,
                "STATUS"
            ).upper()

            if status not in OPEN_STATUSES:
                continue

            # ---------------------------------------------
            # Pending reboot
            # ---------------------------------------------

            if qid == PENDING_REBOOT_QID:
                pending_reboot = True
                continue

            # ---------------------------------------------
            # Missing patch
            # ---------------------------------------------

            if qid in patchable_qids:
                missing_patch_qids.append(qid)

        missing_patch_qids = sorted(
            set(missing_patch_qids)
        )

        # Classification order is intentional.
        #
        # Pending Reboot overrides Unpatched so a host
        # appears in ONE bucket only.

        if pending_reboot:

            patch_status = "Pending Reboot"

        elif missing_patch_qids:

            patch_status = "Unpatched"

        else:

            patch_status = "Patched"

        results.append({
            "qualys_host_id": host_id,
            "hostname": hostname,
            "ip": ip,
            "aws_instance_id": instance_id,
            "aws_account_id": aws_account_id,
            "aws_region": aws_region,
            "operating_system": os_name,
            "patch_status": patch_status,
            "missing_patch_count": len(
                missing_patch_qids
            ),
            "missing_patch_qids": ",".join(
                missing_patch_qids
            )
        })

    return results


def write_csv(results):

    fields = [
        "qualys_host_id",
        "hostname",
        "ip",
        "aws_instance_id",
        "aws_account_id",
        "aws_region",
        "operating_system",
        "patch_status",
        "missing_patch_count",
        "missing_patch_qids"
    ]

    with open(
        OUTPUT_FILE,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fields
        )

        writer.writeheader()
        writer.writerows(results)

    print(f"\nCreated: {OUTPUT_FILE}")


def print_summary(results):

    counts = defaultdict(int)

    for server in results:
        counts[server["patch_status"]] += 1

    print()
    print("=" * 65)
    print("AWS WINDOWS PATCH STATUS")
    print("=" * 65)

    print(
        f"Total AWS Windows Servers : "
        f"{len(results)}"
    )

    print(
        f"Patched                   : "
        f"{counts['Patched']}"
    )

    print(
        f"Pending Reboot            : "
        f"{counts['Pending Reboot']}"
    )

    print(
        f"Unpatched                 : "
        f"{counts['Unpatched']}"
    )

    print("=" * 65)


def main():

    session = get_session()

    patchable_qids = get_patchable_qids(
        session
    )

    root = get_aws_host_detections(
        session
    )

    results = classify_hosts(
        root,
        patchable_qids
    )

    print_summary(results)

    write_csv(results)


if __name__ == "__main__":
    main()
