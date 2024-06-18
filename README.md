# SubTakeControl

This script checks for subdomain takeover vulnerabilities on GitHub Pages.

## Installation

1. **Clone the repository**:

```bash
git clone https://github.com/crynomor3/SubTakeControl.git
cd subdomain-takeover-checker
```

2. Install Subfinder: Follow the instructions on the Subfinder GitHub repository to install Subfinder.
3. Install Python dependencies:
```bash
pip install requests python-telegram-bot
```
## Usage
1. Run the script:
   ```bash
   python SubTakeControl.py
   ```
2. Enter the required details:
  - **Domain**: The domain you want to check for subdomain takeover vulnerabilities.
  - **Telegram Bot Token**: Your Telegram bot token is used for notifications.
  - **Telegram Chat ID**: The chat ID where Telegram notifications will be sent.
  - **GitHub Personal Access Token**: Your personal access token from GitHub with repository creation and management permissions.
  - **GitHub Username**: Your GitHub username is associated with the personal access token.

3. Monitoring and Notifications:
  - The script will enumerate subdomains of the specified domain and check each for vulnerabilities.
  - If a vulnerable subdomain is found, the script will attempt to take it over on GitHub.
  - If the takeover is successful, you will receive a Telegram notification.

## Example:

```bash
python SubTakeControl.py
```
Enter the domain and tokens as prompted. The script will monitor and attempt to take over vulnerable subdomains
```bash
Enter the domain to check for subdomain takeover: example.com
Enter your Telegram bot token: your_telegram_bot_token
Enter your Telegram chat ID: your_telegram_chat_id
Enter your GitHub personal access token: your_github_personal_access_token
Enter your GitHub username: your_github_username
```
