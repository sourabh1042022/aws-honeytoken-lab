# AWS HoneyToken Network and Real-Time Alerting Lab

## 🧠 Objective

This project simulates a decoy AWS environment using leaked honeytoken credentials.
It demonstrates how to detect token misuse through CloudTrail, trigger alerts using
EventBridge, notify via Slack, and log the event in MongoDB Atlas.

## 📐 Architecture Diagram

![image](https://github.com/user-attachments/assets/8aef87b7-f413-4f37-83bb-67d9174b9860)



## 📂 Repository Structure

```
aws-honeytoken-lab/
├── lambda/lambda_function.py
├── scripts/simulate_attack.sh
├── config/eventbridge-rule.json
├── config/permissions.sh
├── screenshots/
│   ├── lambda_env_vars.png
│   ├── mongo_log.png
│   └── slack_alert.png
├── README.md
```

## ⚙️ Setup Instructions

### 1. Create Honeytoken
```bash
aws iam create-user --user-name honeyuser
aws iam attach-user-policy --user-name honeyuser --policy-arn arn:aws:iam::aws:policy/ReadOnlyAccess
aws iam create-access-key --user-name honeyuser
```

### 2. Leak Key on GitHub Gist
Create and upload a file named `honeytoken.json` publicly.

### 3. Configure CloudTrail
Create a CloudTrail trail to log to an S3 bucket with correct policies.

### 4. Configure EventBridge Trigger
```bash
aws events put-rule --name HoneyTokenTriggerRule --event-pattern file://config/eventbridge-rule.json --region sa-east-1
aws events put-targets --rule HoneyTokenTriggerRule --targets "Id"="1","Arn"="arn:aws:lambda:sa-east-1:<ACCOUNT_ID>:function:HoneyTokenAlertHandler" --region sa-east-1
aws lambda add-permission --function-name HoneyTokenAlertHandler --statement-id "AllowExecutionFromEventBridge" --action "lambda:InvokeFunction" --principal events.amazonaws.com --source-arn "arn:aws:events:sa-east-1:<ACCOUNT_ID>:rule/HoneyTokenTriggerRule"
```

### 5. Deploy Lambda
Package your function and upload `lambda_function.py` with `requests` and `pymongo` to AWS Lambda.

### 6. Configure MongoDB Atlas
- Create free-tier cluster and whitelist access.
- Create database `honeydb` and collection `alerts`.

### 7. Simulate Token Usage
```bash
export AWS_ACCESS_KEY_ID=<LEAKED_KEY>
export AWS_SECRET_ACCESS_KEY=<LEAKED_SECRET>
aws sts get-caller-identity
```

## 📸 Screenshots

  ![image](https://github.com/user-attachments/assets/eb82e89d-3a31-44d2-90d3-65129cc31f07)

  ![image](https://github.com/user-attachments/assets/54c602ac-4f3b-461e-bea1-b27fd27a649b)

  ![image](https://github.com/user-attachments/assets/9ef21d52-c4ed-428f-bbc1-db6a9fd039e5)


## ✅ Recommendations

- Rotate honeytoken credentials periodically.
- Add automated IP blocking in future versions.
- Integrate with SIEM or Wazuh/ELK stack for deeper analysis.

