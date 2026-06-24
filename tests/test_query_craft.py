import pytest
from query_craft import ScheduleConfig, EmailSender, process_execution


def test_process_execution_failure_alerts_enabled():
    config = ScheduleConfig(
        schedule_id="daily_sync",
        owner_email="owner@example.com",
        admin_emails=["admin1@example.com", "admin2@example.com"],
        alerts_enabled=True,
    )
    sender = EmailSender()

    sent = process_execution(
        schedule_config=config,
        success=False,
        error_message="Connection lost",
        log_url="https://logs.example.com/run/42",
        email_sender=sender,
    )

    # Email should have been sent
    assert sent is True
    assert len(sender.sent) == 1
    email = sender.sent[0]
    # Recipients include owner and all admins
    assert email["to"] == ["owner@example.com", "admin1@example.com", "admin2@example.com"]
    # Subject contains schedule id
    assert "daily_sync" in email["subject"]
    # Body contains error message and log URL
    assert "Connection lost" in email["body"]
    assert "https://logs.example.com/run/42" in email["body"]


def test_process_execution_failure_alerts_disabled():
    config = ScheduleConfig(
        schedule_id="hourly_job",
        owner_email="owner@example.com",
        admin_emails=["admin@example.com"],
        alerts_enabled=False,
    )
    sender = EmailSender()

    sent = process_execution(
        schedule_config=config,
        success=False,
        error_message="Timeout",
        log_url="https://logs.example.com/run/99",
        email_sender=sender,
    )

    # No email should be sent when alerts are disabled
    assert sent is False
    assert sender.sent == []


def test_process_execution_success_no_email():
    config = ScheduleConfig(
        schedule_id="weekly_report",
        owner_email="owner@example.com",
        admin_emails=[],
        alerts_enabled=True,
    )
    sender = EmailSender()

    sent = process_execution(
        schedule_config=config,
        success=True,
        error_message=None,
        log_url="https://logs.example.com/run/123",
        email_sender=sender,
    )

    # Successful runs never trigger an email
    assert sent is False
    assert sender.sent == []


def test_process_execution_missing_error_message():
    """Edge case where the failure provides no error message."""
    config = ScheduleConfig(
        schedule_id="nightly_etl",
        owner_email="owner@example.com",
        admin_emails=[],
        alerts_enabled=True,
    )
    sender = EmailSender()

    sent = process_execution(
        schedule_config=config,
        success=False,
        error_message=None,
        log_url="https://logs.example.com/run/777",
        email_sender=sender,
    )

    assert sent is True
    email = sender.sent[0]
    # Body should contain placeholder for missing error message
    assert "<no error message>" in email["body"]
    assert "https://logs.example.com/run/777" in email["body"]
