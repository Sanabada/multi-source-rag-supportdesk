# Example Queries and Responses

## 1. How long is a password reset link valid?

```text
Question: How long is a password reset link valid?
Answer: The reset link is valid for 20 minutes. Please request a new reset email from the login page. If the link expires, the user should request a new reset email.
Sources used:
- forum:F-1001 [forum] Password reset email link expired score=2.0107
- doc:supportdesk_docs:2 [docs] Password Reset score=1.7832
- doc:supportdesk_docs:1 [docs] Login Problems score=0.7172
- blog:supportdesk_release_blog:4 [blog] Login Help score=0.3838
- blog:supportdesk_release_blog:3 [blog] Export Scheduling score=0.3589
```

## 2. Why is my account locked after failed login attempts?

```text
Question: Why is my account locked after failed login attempts?
Answer: Many login issues are caused by expired reset links or too many failed attempts. Reset links expire after 20 minutes, and locked accounts unlock automatically after 15 minutes.
Sources used:
- doc:supportdesk_docs:1 [docs] Login Problems score=1.3792
- blog:supportdesk_release_blog:4 [blog] Login Help score=1.3019
- forum:F-1003 [forum] Mobile app does not sync comments score=0.5028
- forum:F-1001 [forum] Password reset email link expired score=0.4984
- forum:F-1005 [forum] Web app keeps crashing score=0.3149
```

## 3. What is the refund policy for paid subscriptions?

```text
Question: What is the refund policy for paid subscriptions?
Answer: SupportDesk refunds paid subscriptions within 14 days of the first purchase Contradiction note: For refund_period_days, I used docs value 14 over ['30'].
Sources used:
- doc:supportdesk_docs:4 [docs] Refund Policy score=1.8349
- blog:supportdesk_admin_tips:1 [blog] Handling Refund Questions score=0.8993
- forum:F-1002 [forum] Refund window confusion score=0.7222
Contradictions:
- refund_period_days: chose 14 over ['30']
```

## 4. A forum says refunds are 30 days. Which refund period is correct?

```text
Question: A forum says refunds are 30 days. Which refund period is correct?
Answer: SupportDesk refunds paid subscriptions within 14 days of the first purchase. Contradiction note: For refund_period_days, I used docs value 14 over ['30'].
Sources used:
- forum:F-1002 [forum] Refund window confusion score=1.1124
- doc:supportdesk_docs:4 [docs] Refund Policy score=0.8525
- blog:supportdesk_admin_tips:1 [blog] Handling Refund Questions score=0.7946
- doc:supportdesk_docs:1 [docs] Login Problems score=0.3316
Contradictions:
- refund_period_days: chose 14 over ['30']
```

## 5. Why is my mobile app not syncing ticket comments?

```text
Question: Why is my mobile app not syncing ticket comments?
Answer: Update the app, check your network connection, then sign out and sign back in. The latest app also retries failed sync requests after reconnecting. The mobile app syncs tickets, comments, and notifications when the device is online. If sync stops, users should update the app, check network access, and sign out and sign back in.
Sources used:
- forum:F-1003 [forum] Mobile app does not sync comments score=1.7729
- doc:supportdesk_docs:5 [docs] Mobile Sync score=0.9494
- blog:supportdesk_release_blog:1 [blog] Mobile Sync Improvements score=0.7773
- blog:supportdesk_admin_tips:4 [blog] Mobile Support Checklist score=0.6085
- forum:F-1005 [forum] Web app keeps crashing score=0.542
```

## 6. What is the maximum attachment size on the Team plan?

```text
Question: What is the maximum attachment size on the Team plan?
Answer: The maximum file size is 25 MB per attachment on Free and Team plans. Team plan attachments are limited to 25 MB. Business plan workspaces can upload files up to 100 MB. Business plan upload limits increased from 50 MB to 100 MB per attachment.
Sources used:
- doc:supportdesk_docs:6 [docs] File Uploads score=1.6663
- forum:F-1004 [forum] Attachment upload too large score=1.0204
- blog:supportdesk_release_blog:2 [blog] Updated File Uploads score=0.9274
- doc:supportdesk_docs:3 [docs] Billing and Plans score=0.7096
- doc:supportdesk_docs:8 [docs] Data Export score=0.6094
```

## 7. Can Business plan users upload 100 MB files?

```text
Question: Can Business plan users upload 100 MB files?
Answer: Business plan workspaces can upload files up to 100 MB. Team plan attachments are limited to 25 MB. Business plan workspaces can upload attachments up to 100 MB. Business plan upload limits increased from 50 MB to 100 MB per attachment.
Sources used:
- forum:F-1004 [forum] Attachment upload too large score=1.6499
- doc:supportdesk_docs:6 [docs] File Uploads score=1.5761
- blog:supportdesk_release_blog:2 [blog] Updated File Uploads score=1.247
- doc:supportdesk_docs:3 [docs] Billing and Plans score=0.7779
- forum:F-1006 [forum] Free plan ticket limit score=0.6364
```

## 8. What should I do if the web app keeps crashing?

```text
Question: What should I do if the web app keeps crashing?
Answer: Refresh the page, clear browser cache, and disable browser extensions.
Sources used:
- forum:F-1005 [forum] Web app keeps crashing score=1.6591
- doc:supportdesk_docs:7 [docs] App Crash Troubleshooting score=0.867
- forum:F-1003 [forum] Mobile app does not sync comments score=0.5633
- doc:supportdesk_docs:5 [docs] Mobile Sync score=0.4595
- blog:supportdesk_admin_tips:2 [blog] Reducing App Crashes score=0.4078
```

## 9. How many agents and tickets are included in the Free plan?

```text
Question: How many agents and tickets are included in the Free plan?
Answer: The Free plan supports 100 tickets per month and 3 agents. The Free plan allows 3 agents and 100 tickets per month. The Team plan allows 15 agents and 5,000 tickets per month. Free workspaces are best for trials because they support 3 agents and 100 tickets per month.
Sources used:
- forum:F-1006 [forum] Free plan ticket limit score=1.712
- doc:supportdesk_docs:3 [docs] Billing and Plans score=1.3394
- blog:supportdesk_admin_tips:3 [blog] Managing Plan Limits score=1.1455
- doc:supportdesk_docs:6 [docs] File Uploads score=1.0859
- doc:supportdesk_docs:8 [docs] Data Export score=0.8049
```

## 10. Can admins schedule ticket exports?

```text
Question: Can admins schedule ticket exports?
Answer: Business plan admins can now schedule weekly ticket exports from Admin Settings. Business plan workspaces can schedule weekly exports.
Sources used:
- blog:supportdesk_release_blog:3 [blog] Export Scheduling score=1.5323
- doc:supportdesk_docs:8 [docs] Data Export score=1.2483
- forum:F-1006 [forum] Free plan ticket limit score=0.4983
- forum:F-1005 [forum] Web app keeps crashing score=0.4329
- forum:F-1003 [forum] Mobile app does not sync comments score=0.427
```

## 11. What plans does SupportDesk offer?

```text
Question: What plans does SupportDesk offer?
Answer: The Free plan allows 3 agents and 100 tickets per month. The maximum file size is 25 MB per attachment on Free and Team plans. Free and Team plans can export once per day.
Sources used:
- doc:supportdesk_docs:3 [docs] Billing and Plans score=1.1446
- doc:supportdesk_docs:6 [docs] File Uploads score=0.5858
- doc:supportdesk_docs:8 [docs] Data Export score=0.58
- doc:supportdesk_docs:4 [docs] Refund Policy score=0.556
- forum:F-1005 [forum] Web app keeps crashing score=0.546
```

## 12. How many tickets are included in the Team plan?

```text
Question: How many tickets are included in the Team plan?
Answer: The Free plan supports 15 agents and 5,000 tickets per month. The Team plan allows 3 agents and 100 tickets per month. Team workspaces support larger teams with 15 agents and 5,000 tickets per month. Team workspaces support larger teams with 15 agents and 5,000 tickets per month.
Sources used:
- forum:F-1006 [forum] Free plan ticket limit score=1.2126
- doc:supportdesk_docs:3 [docs] Billing and Plans score=1.1722
- blog:supportdesk_admin_tips:3 [blog] Managing Plan Limits score=0.9541
- doc:supportdesk_docs:6 [docs] File Uploads score=0.9411
- doc:supportdesk_docs:8 [docs] Data Export score=0.9322
```

## 13. What should I send support if the app still crashes?

```text
Question: What should I send support if the app still crashes?
Answer: your browser name, operating system, and screenshot
Sources used:
- doc:supportdesk_docs:7 [docs] App Crash Troubleshooting score=1.361
- forum:F-1005 [forum] Web app keeps crashing score=0.9531
- blog:supportdesk_admin_tips:2 [blog] Reducing App Crashes score=0.8127
- blog:supportdesk_admin_tips:4 [blog] Mobile Support Checklist score=0.6578
- forum:F-1003 [forum] Mobile app does not sync comments score=0.5114
```

## 14. What should I check first if I cannot log in?

```text
Question: What should I check first if I cannot log in?
Answer: that the email address is correct and then reset the password
Sources used:
- doc:supportdesk_docs:1 [docs] Login Problems score=1.49
- forum:F-1004 [forum] Attachment upload too large score=0.5573
- doc:supportdesk_docs:5 [docs] Mobile Sync score=0.5282
- forum:F-1003 [forum] Mobile app does not sync comments score=0.5219
- blog:supportdesk_admin_tips:1 [blog] Handling Refund Questions score=0.4901
```

## 15. Do Free and Team plans have the same attachment limit?

```text
Question: Do Free and Team plans have the same attachment limit?
Answer: Free and Team plans still use the 25 MB attachment limit. The maximum file size is 25 MB per attachment on Free and Team plans. SupportDesk has Free, Team, and Business plans. The Free plan allows 3 agents and 100 tickets per month.
Sources used:
- blog:supportdesk_release_blog:2 [blog] Updated File Uploads score=1.2617
- doc:supportdesk_docs:6 [docs] File Uploads score=1.026
- doc:supportdesk_docs:3 [docs] Billing and Plans score=0.9285
- forum:F-1006 [forum] Free plan ticket limit score=0.7953
- doc:supportdesk_docs:8 [docs] Data Export score=0.7573
```
