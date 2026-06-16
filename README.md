# AWS Backup Alerting Solution

## Overview

Centralized AWS Backup monitoring across multiple AWS accounts using EventBridge and SNS.

## Architecture

Member Accounts → EventBridge → Management Account Event Bus → SNS → Email Notifications

## Prerequisites

- Python 3.x
- AWS CDK v2
- AWS CLI

## Deployment

Refer:
- docs/Deployment-Guide.md

## Documentation

- [Architecture Guide](docs/AWS-Backup-Alert-Architecture.md)
- [Deployment Guide](docs/Deployment-Guide.md)
- [Operational Runbook](docs/Operational-Runbook.md)
- [Troubleshooting Guide](docs/Troubleshooting-Guide.md)

## Cleanup

cdk destroy --all