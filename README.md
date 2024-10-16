
# RisingSpin

Tired of waiting for the next spin? And maybe you just forget to do it ?\
Well, I have a solution for you.\
Let me present you **RisingSpin**, the automated Roulette for RisingHub.

## Features

- Logs in automatically with your RisingHub credentials
- Spins the roulette for selected heroes
- Sends a Discord notification with the prize won and the next available spin time
- Customizable hero list and Discord webhook notifications

## Project Structure

```
.
├── app.py                  # Main script to run the automation
├── config.py               # Handles loading and managing configuration files
├── logger.py               # Logger module with color-coded output
├── notifiers.py            # Discord notifier for sending prize notifications
├── risinghub.py            # Core logic for interacting with RisingHub website
├── Dockerfile              # Docker setup for containerizing the project
├── requirements.txt        # List of dependencies
└── config/config.yml       # Configuration file (YAML format)
```

## Installation

1. Clone this repository:

```bash
git clone https://github.com/yourusername/risingspin.git
cd risingspin
```

2. Install the required Python packages:

```bash
pip install -r requirements.txt
```

3. Set up the configuration file `config/config.yml` with your credentials and preferences:

```yaml
username: "your_username"
password: "your_password"
webhook_url: "your_discord_webhook_url"
notify: true
random_hero: false
heroes:
  - "Hero 1"
  - "Hero 2"
```

## Usage

To start the automated roulette spinning, simply run:

```bash
python3 app.py
```

## Docker Setup

You can also run this project using Docker:

1. Build the Docker image:

```bash
docker build -t risingspin .
```

2. Run the Docker container:

```bash
docker run -d risinghub-roulette
```

## Configuration

The configuration is managed through a `config/config.yml` file. It includes the following fields:

- `username`: Your RisingHub username
- `password`: Your RisingHub password
- `webhook_url`: Discord webhook URL for sending notifications
- `notify`: Whether or not to send notifications (`true` or `false`)
- `random_hero`: If set to `true`, selects a hero at random to spin the roulette
- `heroes`: A list of heroes you want to spin the roulette for

## Contributing

Feel free to fork the repository and submit a pull request for improvements or bug fixes.

## License

This project is licensed under the MIT License.
