from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class ScheduleConfig:
    """Configuration for a single schedule."""
    schedule_id: str
    owner_email: str
    admin_emails: List[str] = field(default_factory=list)
    alerts_enabled: bool = True


class EmailSender:
    """
    Very small email abstraction that records sent messages in memory.
    In production this could be swapped with a real SMTP client.
    """

    def __init__(self) -> None:
        self.sent: List[Dict[str, object]] = []

    def send(self, to: List[str], subject: str, body: str) -> None:
        """
        Record an email that would have been sent.

        Args:
            to: List of recipient email addresses.
            subject: Email subject line.
            body: Full email body.
        """
        self.sent.append({
            "to": to,
            "subject": subject,
            "body": body,
        })


def _compose_subject(schedule_id: str) -> str:
    """Create a subject line for a failed execution."""
    return f"Execution failed for schedule '{schedule_id}'"


def _compose_body(error_message: str | None, log_url: str) -> str:
    """Create the email body containing the error and a link to logs."""
    error_part = error_message or "<no error message>"
    return f"""The scheduled execution has failed.

Error:
{error_part}

Log details: {log_url}
"""


def process_execution(
    schedule_config: ScheduleConfig,
    *,
    success: bool,
    error_message: str | None,
    log_url: str,
    email_sender: EmailSender,
) -> bool:
    """
    Process the result of a scheduled run.

    If the run failed and alerts are enabled, an email is sent to the owner
    and all admins.

    Args:
        schedule_config: Configuration for the schedule.
        success: Whether the execution succeeded.
        error_message: Optional error message from the failure.
        log_url: URL where the execution log can be inspected.
        email_sender: Instance used to "send" the email.

    Returns:
        True if an email was sent, False otherwise.
    """
    if success:
        # No alert needed for successful runs.
        return False

    if not schedule_config.alerts_enabled:
        # Alerts are explicitly disabled for this schedule.
        return False

    subject = _compose_subject(schedule_config.schedule_id)
    body = _compose_body(error_message, log_url)

    recipients = [schedule_config.owner_email] + schedule_config.admin_emails
    email_sender.send(to=recipients, subject=subject, body=body)
    return True
