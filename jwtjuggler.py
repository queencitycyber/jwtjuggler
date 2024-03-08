import click
import json
import requests
import csv
from rich import print
from rich.table import Table
from rich.console import Console
from urllib.parse import urljoin

console = Console()

# Function to handle user authentication and obtain JWTs
def handle_authentication(login_endpoint, user1_credentials, user2_credentials, proxy):
    proxies = {'http': proxy, 'https': proxy} if proxy else None
    response_user1 = requests.post(login_endpoint, json=user1_credentials, proxies=proxies)
    jwt_user1 = response_user1.json().get('token') if response_user1.status_code == 200 else None
    response_user2 = requests.post(login_endpoint, json=user2_credentials, proxies=proxies)
    jwt_user2 = response_user2.json().get('token') if response_user2.status_code == 200 else None
    return jwt_user1, jwt_user2

# Function to check if URL is absolute
def is_absolute_url(url):
    return bool(url.startswith('http://') or url.startswith('https://'))

# Function to generate colored user text
def get_colored_user_text(user):
    colors = {"User 1": "green", "User 2": "blue", "Unauthenticated": "red"}
    return f"[{colors[user]}]{user}[/{colors[user]}]"

# Function to export table data
def export_data(data, format_type):
    if format_type == 'json':
        with open('output.json', 'w') as json_file:
            json.dump(data, json_file, indent=4)
    elif format_type == 'csv':
        with open('output.csv', 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(['Endpoint', 'User', 'Status Code', 'Content Length', 'Content Type'])
            for row in data:
                writer.writerow(row)

# Main function to run the JWT testing harness with output option
@click.command()
@click.option('--config', default='config.json', help='Specify the configuration file.')
@click.option('--output', type=click.Choice(['console', 'json', 'csv']), default='console', help='Output format.')
def main(config, output):
    with open(config, 'r') as file:
        configuration = json.load(file)

    user1_credentials = configuration.get('user1')
    user2_credentials = configuration.get('user2')
    login_endpoint = configuration.get('login_endpoint')
    proxy = configuration.get('proxy')

    jwt_user1, jwt_user2 = handle_authentication(login_endpoint, user1_credentials, user2_credentials, proxy)
    
    endpoints_file = configuration.get('endpoints_file')
    base_url = configuration.get('base_url', '')
    proxies = {'http': proxy, 'https': proxy} if proxy else None

    with open(endpoints_file, 'r') as file:
        endpoints = file.read().splitlines()

    table = Table(title="JWTJuggler")
    table.add_column("Endpoint")
    table.add_column("User", justify="right")
    table.add_column("Status Code", justify="right")
    table.add_column("Content Length", justify="right")
    table.add_column("Content Type", justify="right")

    data_for_export = []

    for endpoint in endpoints:
        if not is_absolute_url(endpoint):
            endpoint = urljoin(base_url, endpoint)

        for user, jwt in [('User 1', jwt_user1), ('User 2', jwt_user2), ('Unauthenticated', None)]:
            headers = {'Authorization': f'Bearer {jwt}'} if jwt else {}
            response = requests.get(endpoint, headers=headers, proxies=proxies)
            user_text = get_colored_user_text(user)
            row = [
                endpoint,
                user,
                str(response.status_code),
                str(len(response.content)),
                response.headers.get('Content-Type', 'N/A').split(';')[0]
            ]
            table.add_row(endpoint, user_text, *row[2:])
            data_for_export.append(row)

    if output == 'console':
        console.print(table)
    else:
        export_data(data_for_export, output)

if __name__ == '__main__':
    main()
