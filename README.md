# Advanced Keylogger Script

This repository contains a Python script designed to collect system information, log keystrokes, capture screenshots, record audio, and access clipboard data. The collected information is then sent via email using the provided credentials. The script also includes encryption functionality to secure the collected data before transmission.

## Features

- **Keylogging**: Logs all keystrokes and saves them in a file.
- **System Information**: Collects system information such as IP address, hostname, and OS details.
- **Clipboard Access**: Retrieves the current content of the clipboard.
- **Audio Recording**: Records audio for a specified duration.
- **Screenshot Capture**: Captures the screen and saves the image.
- **Data Encryption**: Encrypts the collected data using the `cryptography` library.
- **Email Notification**: Sends the collected and encrypted data via email.

## Prerequisites

Ensure you have the following libraries installed:

- `email`
- `smtplib`
- `re`
- `pynput`
- `socket`
- `platform`
- `threading`
- `time`
- `win32clipboard`
- `os`
- `scipy`
- `sounddevice`
- `cryptography`
- `getpass`
- `requests`
- `PIL`

You can install these libraries using `pip`:

```bash
pip install pynput scipy sounddevice cryptography requests pillow'


TO_ADDRESS=recipient_email@example.com

