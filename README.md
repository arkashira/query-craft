# query-craft

A tiny library that helps a data engineer get notified when a scheduled run fails.

## Features

- Define a schedule configuration (owner, admins, alerts on/off).
- Process an execution result and automatically send an email when it fails.
- Email sending is abstracted via an in‑memory `EmailSender` so the library works
  without external services (perfect for unit testing).

## Quick start
