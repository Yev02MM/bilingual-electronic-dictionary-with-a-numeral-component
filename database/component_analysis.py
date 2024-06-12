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

    # List of specific English idioms to analyze
    english_idioms = [
        "One and the same", "one on one", "at sixes and sevens", "in a trice",
        "In one ear and out the other", "one-eyed", "if it’s not one thing, it’s the other",
        "of one mind", "At one and the same time", "one day at a time", "in one fell swoop",
        "six of one, half a dozen of the other", "have one foot in the grave", "in two shakes",
        "at first glance", "First-rate", "square one", "first hand", "at first sight",
        "cast the first stone", "play first fiddle", "two sides of the same coin",
        "(as) (a)like as two peas in a pod", "as thick as two short planks",
        "Not in a million years", "be (as) easy as one-two-three", "Knocked for six",
        "Two of a kind", "fall between two stools", "Unable to string two words together",
        "A double-edged sword", "talk out of both sides of (one's) mouth",
        "kill two birds with one stone", "getting something thirdhand", "one foot in the grave",
        "fourth dimension", "The four winds", "fifth column", "fifth wheel", "One in ten",
        "Put in one’s two cents", "Measure twice, cut once", "Beat someone six ways to Sunday",
        "On cloud nine", "eighth wonder", "At the eleventh hour", "third cousin twice removed",
        "on the double", "One-up someone", "One hundred percent", "talk nineteen to the dozen",
        "in seventh heaven", "a hundred/thousand/million and one", "A dime a dozen"
    ]

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
        ukr_word_forms_counter[ukr_forms_count] += 1
        if row[1] in english_idioms:
            eng_forms_count = count_forms(row[1])
            eng_word_forms_counter[eng_forms_count] += 1
            print(f"Phrase: {row[1]} (English) has {eng_forms_count} word forms (ignoring text in brackets)")

    # Close the database connection
    conn.close()

    # Get all most common word form counts for Ukrainian phrases
    all_ukr = ukr_word_forms_counter.most_common()
    print("\nAll most common word form counts for Ukrainian phrases:")
    for count, freq in all_ukr:
        print(f"{count} word forms: {freq} occurrences")

    # Get all most common word form counts for English phrases
    all_eng = eng_word_forms_counter.most_common()
    print("\nAll most common word form counts for English phrases:")
    for count, freq in all_eng:
        print(f"{count} word forms: {freq} occurrences")

# Call the function with the database file name as an argument
count_word_forms('mydatabase.db')
