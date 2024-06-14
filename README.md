# NASA APOD Image Downloader

This script downloads NASA's Astronomy Picture of the Day (APOD) images either locally or on a network server.

## Requirements

- Python 3.x
- Packages listed in `requirements.txt`

## Setup

1. Clone the repository.
2. Install dependencies using `pip install -r requirements.txt`.
3. Run the script `main.py`.

## Configuration

- Obtain an API key from NASA at [NASA API](https://api.nasa.gov/).
- Enter your API key when prompted.
- Choose whether to download images locally or on a network:
  - For local download, specify local paths.
  - For network download, provide server details and paths.

## Usage

- When prompted, enter the necessary information (API key, download location, paths).
- The script will download APOD images from NASA starting from June 16, 1995, up to the current date.
- Images are saved with filenames in the format `YYYY-MM-DD.jpg`.
- Logs are saved either locally or on the network as specified.

## Notes

- The script manages API rate limits by waiting if the rate limit is reached.
- Images that are not downloadable are logged in `images_non_telechargees.txt`.

