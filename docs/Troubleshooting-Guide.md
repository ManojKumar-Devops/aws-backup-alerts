# Troubleshooting Guide

## Issue: SNS Notifications Not Received

### Symptoms

* Backup jobs complete successfully.
* No email notifications received.

### Checks

Verify SNS Topic:

```bash
aws sns list-topics
```

Verify subscriptions:

```bash
aws sns list-subscriptions-by-topic \
--topic-arn <SNS_TOPIC_ARN>
```

Verify subscription status:

```text
Confirmed
```

### Resolution

* Confirm email subscription.
* Re-subscribe if necessary.
* Verify SNS topic permissions.

---

# Issue: EventBridge Events Not Forwarded

## Symptoms

* Backup events visible in member account.
* No events received in management account.

### Checks

Verify EventBridge rule:

```bash
aws events list-rules
```

Verify target configuration:

```bash
aws events list-targets-by-rule \
--rule ForwardBackupJobEventRule
```

Verify rule status:

```text
ENABLED
```

### Resolution

* Re-enable rule.
* Verify target Event Bus ARN.
* Verify management account Event Bus Policy.

---

# Issue: IAM Permission Problems

## Symptoms

* Access Denied errors.
* Event forwarding failures.

### Checks

Verify EventBridge role permissions.

Required permission:

```json
{
  "Action": "events:PutEvents",
  "Effect": "Allow"
}
```

Verify Event Bus Policy.

### Resolution

* Update IAM Policy.
* Redeploy CDK stack.
* Test event forwarding.

---

# Issue: Backup Events Missing

## Symptoms

* Backup completed.
* No EventBridge event generated.

### Checks

Verify backup job:

```bash
aws backup list-backup-jobs
```

Verify EventBridge event history.

Check CloudTrail logs.

### Resolution

* Confirm backup job status.
* Verify EventBridge service health.
* Retry backup job.

---

# Issue: CDK Deployment Failure

## Symptoms

Deployment fails.

### Checks

```bash
cdk doctor
```

```bash
cdk diff
```

Review CloudFormation Events.

### Resolution

* Resolve permission issues.
* Bootstrap account if missing.
* Retry deployment.

---

# Useful Commands

## View Stack Status

```bash
aws cloudformation describe-stacks
```

## View EventBridge Rules

```bash
aws events list-rules
```

## View SNS Topics

```bash
aws sns list-topics
```

## View Backup Jobs

```bash
aws backup list-backup-jobs
```

## View AWS Identity

```bash
aws sts get-caller-identity
```
