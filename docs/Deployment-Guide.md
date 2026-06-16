# Deployment Guide

## Overview

This document describes the deployment process for the AWS Backup Alerting Solution.

The solution deploys:

* Management Account Stack
* Member Account Stack(s)
* EventBridge Rules
* SNS Topic
* Event Bus Policies

---

# Prerequisites

## Software Requirements

* Python 3.11+
* AWS CLI
* AWS CDK v2
* Git

Verify installation:

```bash
python3 --version
aws --version
cdk --version
```

---

# Configure AWS Credentials

Ensure AWS CLI is configured for the target account.

```bash
aws configure
```

Validate:

```bash
aws sts get-caller-identity
```

---

# Update Configuration

Update the following values in `app.py`.

```python
MANAGEMENT_ACCOUNT_ID = "12345678901"

MEMBER_ACCOUNT_IDS = [
    "***********",
    "***********",
    "***********",
    "***********",
    "***********",
    "***********",
    "***********"
]

AWS_REGION = "eu-west-1"
```

---

# CDK Bootstrap

CDK must be bootstrapped in all participating accounts.

## Management Account

```bash
cdk bootstrap aws://12345678901/eu-west-1
```

## Member Accounts

```bash
cdk bootstrap aws://***********/eu-west-1

cdk bootstrap aws://***********/eu-west-1

cdk bootstrap aws://***********/eu-west-1

cdk bootstrap aws://***********/eu-west-1

cdk bootstrap aws://***********/eu-west-1

cdk bootstrap aws://***********/eu-west-1

cdk bootstrap aws://***********/eu-west-1
```

---

# Synthesize CloudFormation Templates

```bash
cdk synth
```

Verify templates are generated successfully.

---

# Deployment

Deploy all stacks:

```bash
cdk deploy --all
```

Deploy management stack only:

```bash
cdk deploy BackupAlertManagementStack
```

---

# Validation

## Verify SNS Topic

Navigate to:

AWS Console → SNS → Topics

Verify:

```text
BackupJobSNSTopic
```

exists.

---

## Verify EventBridge Rules

Check:

### Management Account

```text
BackupJobEventRule
```

### Member Accounts

```text
ForwardBackupJobEventRule
```

---

## Subscribe Email Address

```bash
aws sns subscribe \
--topic-arn <SNS_TOPIC_ARN> \
--protocol email \
--notification-endpoint your-email@example.com
```

Confirm subscription from email.

---

## Test Backup Alert

Trigger a backup job.

Verify:

1. EventBridge event generated.
2. Event forwarded to management account.
3. SNS notification published.
4. Email notification received.

---

# Rollback

Remove deployed resources:

```bash
cdk destroy --all
```

Or destroy specific stacks:

```bash
cdk destroy BackupAlertManagementStack
```
