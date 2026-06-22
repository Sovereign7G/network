# 🛡️ AWS MCP Telemetry Log :: DESCRIBE_INSTANCES
---
- **Event ID:** `evt-1779888607-02`
- **Source:** `aws-mcp.amazonaws.com`
- **Operation:** `describe_instances`
- **Timestamp:** `2026-05-27T13:30:07Z`
- **Identity ARN:** `arn:aws:iam::123456789012:user/SovereignAgent`
- **Execution Mode:** `SigV4 Attested Proxy`

### ⚙️ Request Parameters
```json
{
  "service": "ec2",
  "region": "us-west-2"
}
```

### 📦 Response elements
```json
{
  "status": "success",
  "instances_count": 5
}
```

### 🧩 Raw CloudTrail Payload
```json
{
  "eventVersion": "1.08",
  "userIdentity": {
    "type": "IAMUser",
    "arn": "arn:aws:iam::123456789012:user/SovereignAgent"
  },
  "eventTime": "2026-05-27T13:30:07Z",
  "eventSource": "aws-mcp.amazonaws.com",
  "eventName": "describe_instances",
  "awsRegion": "us-west-2",
  "userAgent": "mcp-proxy-for-aws/v1.0",
  "additionalEventData": {
    "PreFlightStatus": "ALLOWLIST_PASSED"
  }
}
```
---
**Status:** `AUDITED & SEALED`  
**Sovereign Signature Verified:** `YES`
