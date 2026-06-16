#!/usr/bin/env python3
import aws_cdk as cdk
from aws_cdk import Environment

from management_stack import BackupAlertManagementStack
from member_stack import BackupAlertMemberStack

app = cdk.App()

MANAGEMENT_ACCOUNT_ID = "12345678901"

MEMBER_ACCOUNT_IDS = [
    "************",
    "************",
    "************",
    "************",
    "************",
    "************",
    "************"
]

AWS_REGION = "eu-west-1"

management_env = Environment(
    account=MANAGEMENT_ACCOUNT_ID,
    region=AWS_REGION
)

BackupAlertManagementStack(
    app,
    "BackupAlertManagementStack",
    member_accounts=MEMBER_ACCOUNT_IDS,
    env=management_env
)

for member_account in MEMBER_ACCOUNT_IDS:
    member_env = Environment(
        account=member_account,
        region=AWS_REGION
    )

    BackupAlertMemberStack(
        app,
        f"BackupAlertMemberStack-{member_account}",
        management_account_id=MANAGEMENT_ACCOUNT_ID,
        env=member_env
    )

app.synth()