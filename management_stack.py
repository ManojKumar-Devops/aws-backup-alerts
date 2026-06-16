from aws_cdk import (
    Stack,
    aws_events as events,
    aws_events_targets as targets,
    aws_sns as sns,
    aws_iam as iam,
    aws_events as eventbridge,
    CfnOutput
)
from constructs import Construct

class BackupAlertManagementStack(Stack):
    def __init__(self, scope: Construct, id: str, member_accounts: list, **kwargs):
        super().__init__(scope, id, **kwargs)

        # Create an SNS topic for backup job alerts
        sns_topic = sns.Topic(
            self, "BackupJobSNSTopic",
            display_name="AWS Backup Job Alerts",
            topic_name="BackupJobSNSTopic"
        )

        # Allow member accounts to publish messages to SNS
        for account_id in member_accounts:
            sns_topic.add_to_resource_policy(
                iam.PolicyStatement(
                    actions=["SNS:Publish"],
                    principals=[iam.AccountPrincipal(account_id)],
                    resources=[sns_topic.topic_arn]
                )
            )

        # Create an EventBridge Rule in the Management Account to listen for AWS Backup Jobs
        event_rule = events.Rule(
            self, "BackupJobEventRule",
            event_pattern={
                "source": ["aws.backup"],
                "detail_type": ["Backup Job State Change"],
                "detail": {
                    "state": ["COMPLETED", "FAILED"]
                }
            }
        )

        # Add SNS as a target for notifications
        event_rule.add_target(targets.SnsTopic(sns_topic))

        # Add IAM Policy to allow member accounts to send events to the Management Account
        event_bus_policy = eventbridge.CfnEventBusPolicy(
            self, "EventBusPolicy",
            statement_id="AllowMemberAccountsToPutEvents",
            statement={
                "Effect": "Allow",
                "Principal": {"AWS": member_accounts},
                "Action": "events:PutEvents",
                "Resource": f"arn:aws:events:{self.region}:{self.account}:event-bus/default"
            }
        )

        # Output the SNS topic ARN
        CfnOutput(
            self, "SNSTopicARN",
            value=sns_topic.topic_arn,
            description="SNS Topic ARN for AWS Backup Job Alerts"
        )

        # Store SNS topic ARN for use in member stacks
        self.sns_topic_arn = sns_topic.topic_arn
