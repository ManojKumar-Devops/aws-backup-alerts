from aws_cdk import (
    Stack,
    aws_events as events,
    aws_events_targets as targets,
    aws_iam as iam
)
from constructs import Construct

class BackupAlertMemberStack(Stack):
    def __init__(self, scope: Construct, id: str, management_account_id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        # IAM Role to allow EventBridge in the member account to send events to the Management Account
        member_role = iam.Role(
            self, "BackupAlertForwarderRole",
            assumed_by=iam.ServicePrincipal("events.amazonaws.com"),
            description="IAM Role to allow EventBridge in Member Account to forward backup job events to the Management Account."
        )

        member_role.add_to_policy(
            iam.PolicyStatement(
                actions=["events:PutEvents"],
                resources=[f"arn:aws:events:{self.region}:{management_account_id}:event-bus/default"]
            )
        )

        # Create an EventBridge Rule in the Member Account to forward AWS Backup Job events
        event_rule = events.Rule(
            self, "ForwardBackupJobEventRule",
            event_pattern={
                "source": ["aws.backup"],
                "detail_type": ["Backup Job State Change"],
                "detail": {
                    "state": ["COMPLETED", "FAILED"]
                }
            }
        )

        # Forward the event to the Management Account's Event Bus
        event_rule.add_target(
            targets.EventBus(
                events.EventBus.from_event_bus_arn(
                    self, "ManagementEventBus",
                    f"arn:aws:events:{self.region}:{management_account_id}:event-bus/default"
                )
            )
        )
