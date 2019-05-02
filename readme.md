# Python Showtime Scrapper

A Safari bot that will fetch you the best seats available for all the nearby theaters.

## How to Set up

Create a virtual environment
```bash
python3 -m venv local_python_environment
```

Clone files into the environment

Activate the environment
```bash
source local_python_environment/bin/activate
```

Install the requirements
```bash
pip install -r requirements.txt
```

Enable safaridriver
```bash
safaridriver --enable
```
or follow this link: [Apple Doc](https://developer.apple.com/documentation/webkit/testing_with_webdriver_in_safari)

## Usage
Inside the main.py change the movie_name, zip_code, show_type and movie_date to the desired values

To use time filter:
set time_filter = True and set start_time and end_time in this format '6:00p'. Bot will take care of the rest

To find group seats:
set group_no > 1 and less than 9
