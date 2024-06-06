import sqlite3
import re
from collections import Counter


def count_word_forms(database_file):
    # Create a connection to the database
    conn = sqlite3.connect(database_file)
    c = conn.cursor()

    # Retrieve data from the database
    c.execute("SELECT ukr_phrase, eng_phrase FROM phrases")
    rows = c.fetchall()

    # Function to count word forms in a phrase ignoring text in brackets
    def count_forms(phrase):
        # Remove text within parentheses and brackets
        cleaned_phrase = re.sub(r'\[.*?\]|\(.*?\)', '', phrase)
        # Split the cleaned phrase into words and count them
        return len(cleaned_phrase.split())

    # Counters for word forms
    ukr_word_forms_counter = Counter()
    eng_word_forms_counter = Counter()

    # Loop through the rows and count the word forms
    for row in rows:
        ukr_forms_count = count_forms(row[0])
        eng_forms_count = count_forms(row[1])
        ukr_word_forms_counter[ukr_forms_count] += 1
        eng_word_forms_counter[eng_forms_count] += 1
        print(f"Phrase: {row[0]} (Ukrainian) has {ukr_forms_count} word forms (ignoring text in brackets)")
        print(f"Phrase: {row[1]} (English) has {eng_forms_count} word forms (ignoring text in brackets)")

    # Close the database connection
    conn.close()

    # Get the top 5 most common word form counts for Ukrainian phrases
    top_5_ukr = ukr_word_forms_counter.most_common(5)
    print("\nTop 5 most common word form counts for Ukrainian phrases:")
    for count, freq in top_5_ukr:
        print(f"{count} word forms: {freq} occurrences")

    # Get the top 5 most common word form counts for English phrases
    top_5_eng = eng_word_forms_counter.most_common(5)
    print("\nTop 5 most common word form counts for English phrases:")
    for count, freq in top_5_eng:
        print(f"{count} word forms: {freq} occurrences")


# Call the function with the database file name as an argument
count_word_forms('mydatabase.db')
