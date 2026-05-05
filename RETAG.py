#!/usr/bin/env python3

import boto3
import csv
import argparse
from botocore.exceptions import ClientError


def load_csv(file_path):
    data = []

    with open(file_path, "r") as f:
        reader = csv.DictReader(f)

        for row in reader:
            instance_id = row.pop("InstanceId")

            # Convert remaining columns to tags
            tags = [{"Key": k, "Value": str(v)} for k, v in row.items() if v]

            data.append({
                "InstanceId": instance_id,
                "Tags": tags
            })

    return data


def tag_resources(ec2, resource_ids, tags):
    if not resource_ids:
        return

    try:
        ec2.create_tags(Resources=resource_ids, Tags=tags)
        print(f"Tagged: {resource_ids}")
    except ClientError as e:
        print(f"ERROR tagging {resource_ids}: {e}")


def get_ebs_volumes(ec2, instance_id):
    volume_ids = []

    try:
        response = ec2.describe_instances(InstanceIds=[instance_id])

        for reservation in response["Reservations"]:
            for instance in reservation["Instances"]:
                for mapping in instance.get("BlockDeviceMappings", []):
                    ebs = mapping.get("Ebs")
                    if ebs and "VolumeId" in ebs:
                        volume_ids.append(ebs["VolumeId"])

    except ClientError as e:
        print(f"ERROR fetching volumes for {instance_id}: {e}")

    return volume_ids


def main():
    parser = argparse.ArgumentParser(description="Tag EC2 and EBS from CSV")

    parser.add_argument("--region", required=True)
    parser.add_argument("--csv-file", required=True)

    args = parser.parse_args()

    ec2 = boto3.client("ec2", region_name=args.region)

    records = load_csv(args.csv_file)

    for record in records:
        instance_id = record["InstanceId"]
        tags = record["Tags"]

        print(f"\nProcessing Instance: {instance_id}")

        # Tag EC2
        tag_resources(ec2, [instance_id], tags)

        # Get EBS volumes
        volumes = get_ebs_volumes(ec2, instance_id)

        print(f"Attached Volumes: {volumes}")

        # Tag EBS
        tag_resources(ec2, volumes, tags)

    print("\nCompleted.")


if __name__ == "__main__":
    main()
