# task-growth

# Dependencies
- docker
- poetry
- python

# How to run
- install python dependencies
    ```sh
    poetry install
    ```
- Start docker compose
    ```sh
    make up
    ```
- Run the script
    ```sh
    python main.py
    ```

# What it does
This code accesses the news website, gets the most recent news, collecting the URL, title, tags, reading time
and at the end downloads the main image.
This data is saved in a PostgreSQL database, a report is also created of what was collected in a spreadsheet 
and the number of articles by tags, this data is sent by email.
