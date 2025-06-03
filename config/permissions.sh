#!/bin/bash
aws events put-rule --name HoneyTokenTriggerRule --event-pattern file://config/eventbridge-rule.json --region sa-east-1

aws events put-targets --rule HoneyTokenTriggerRule --targets "Id"="1","Arn"="arn:aws:lambda:sa-east-1:ACCOUNT_ID:function:HoneyTokenAlertHandler" --region sa-east-1

aws lambda add-permission --function-name HoneyTokenAlertHandler --statement-id "AllowExecutionFromEventBridge" --action "lambda:InvokeFunction" --principal events.amazonaws.com --source-arn "arn:aws:events:sa-east-1:ACCOUNT_ID:rule/HoneyTokenTriggerRule"
