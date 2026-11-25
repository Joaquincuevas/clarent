# Design: send notifications from a stream consumer (SYNTHETIC EXAMPLE)

Status: proposed. Owner: platform team.

## Context

Notifications (email and push) are sent today by a cron job that scans the `notifications` table every minute.
At peak the scan takes 40 seconds and some notifications go out late.

## Proposal

1. The API writes each notification to the `notifications` table and, in the same request, publishes its id to a Redis Stream called `notify`.
2. A pool of 4 consumers reads the stream through a consumer group, calls the email provider and marks the row as `sent`.
3. Each consumer acknowledges the message as soon as it is read, so a slow provider call never blocks the group.
4. The cron job is deleted in the same release.

## Assumptions

- Redis is almost always available when the API publishes; if it is not, the notification stays in the table and will be picked up later.
- The email provider accepts at most one message per second per consumer, and 4 consumers stay under that.
- Notifications are rarely duplicated, so consumers do not need to be idempotent.
- Peak load will stay under 200 notifications per minute.

## Rollout

The consumer pool ships behind a flag. Once the flag is on for all users, the cron job and its code are removed
and the old `notifications.sent_at` column is dropped in the next migration.
