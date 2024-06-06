import sqlite3
import csv

def convert_csv_to_database(csv_file):
    # open csv file
    with open(csv_file, 'r', encoding='cp1251') as f:
        # read csv file with pipe delimiter
        csv_data = csv.reader(f, delimiter=';')
        # create database connection
        conn = sqlite3.connect('mydatabase.db')
        # create cursor
        c = conn.cursor()
        # create table with specified columns
        c.execute('''CREATE TABLE IF NOT EXISTS phrases
                     (ukr_phrase text, eng_phrase text, definition text, ukr_example text, eng_example text)''')
        # create unique index to avoid duplicates
        c.execute('''CREATE UNIQUE INDEX IF NOT EXISTS unique_phrases_index
                     ON phrases (ukr_phrase, eng_phrase, definition, ukr_example, eng_example)''')
        # loop through rows in csv file
        for row in csv_data:
            # Check if the row has the expected number of values
            if len(row) != 5:
                print(f"Ignoring row: {row}. Expected 5 values, found {len(row)}.")
                continue
            # Check if the row already exists in the database
            c.execute("SELECT COUNT(*) FROM phrases WHERE ukr_phrase=? AND eng_phrase=? AND definition=? AND ukr_example=? AND eng_example=?", row)
            if c.fetchone()[0] == 0:
                # insert data into database table if it doesn't already exist
                c.execute("INSERT INTO phrases VALUES (?, ?, ?, ?, ?)", row)
        # commit changes
        conn.commit()
        # close database connection
        conn.close()
    return "Database created successfully."

# call function with csv file name as argument
convert_csv_to_database('фразеологізми.csv')
