import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox


def show_example(event):
    try:
        item = tree.selection()[0]
        ukr_phrase = tree.item(item, 'values')[0]
        eng_phrase = tree.item(item, 'values')[1]

        cursor.execute("SELECT ukr_example, eng_example FROM phrases WHERE ukr_phrase=? OR eng_phrase=?",
                       (ukr_phrase, eng_phrase))
        example = cursor.fetchone()

        if example:
            definition_text.delete('1.0', tk.END)
            ukr_example_text.delete('1.0', tk.END)
            eng_example_text.delete('1.0', tk.END)
            definition_text.insert(tk.END, f"{tree.item(item, 'values')[2]}")
            ukr_example_text.insert(tk.END, f"{example[0]}")
            eng_example_text.insert(tk.END, f"{example[1]}")
        else:
            messagebox.showinfo("Example", "No examples found.")
    except IndexError:
        messagebox.showinfo("Example", "No item selected.")


def retrieve_phrases():
    for row in data:
        tree.insert('', 'end', values=row)


def search_phrases():
    search_term = search_entry.get()
    for item in tree.get_children():
        tree.delete(item)

    cursor.execute(
        "SELECT ukr_phrase, eng_phrase, definition FROM phrases WHERE ukr_phrase LIKE ? OR eng_phrase LIKE ? OR definition LIKE ?",
        ('%' + search_term + '%', '%' + search_term + '%', '%' + search_term + '%'))
    search_results = cursor.fetchall()
    for row in search_results:
        tree.insert('', 'end', values=row)


# Connect to the SQLite database
conn = sqlite3.connect('mydatabase.db')
cursor = conn.cursor()

# Fetch data from the database
cursor.execute("SELECT ukr_phrase, eng_phrase, definition FROM phrases")
data = cursor.fetchall()

# Create the root window
root = tk.Tk()
root.title("Phrases Database")
root.geometry('900x600')  # Width x Height

# Create a search entry
search_entry = tk.Entry(root)
search_entry.grid(row=0, column=0, sticky=tk.EW)

# Create a search button
search_button = ttk.Button(root, text="Search", command=search_phrases)
search_button.grid(row=0, column=1, sticky=tk.W)

# Create a Treeview to display the phrases and their definitions in a table format
tree = ttk.Treeview(root, columns=('ukr_phrase', 'eng_phrase'), show='headings')
tree.heading('ukr_phrase', text='Ukrainian Phrase')
tree.heading('eng_phrase', text='English Phrase')

# Set the column widths
tree.column('ukr_phrase', width=300)
tree.column('eng_phrase', width=200)
tree.grid(row=1, column=0, columnspan=2, sticky=tk.NSEW)

# Populate the Treeview with data
retrieve_phrases()

# Create labels for the definition and examples
definition_label = ttk.Label(root, text="Definition")
definition_label.grid(row=2, column=0, columnspan=2, sticky=tk.W)

ukr_example_label = ttk.Label(root, text="Ukrainian Example")
ukr_example_label.grid(row=4, column=0, sticky=tk.W)

eng_example_label = ttk.Label(root, text="English Example")
eng_example_label.grid(row=4, column=1, sticky=tk.W)

# Create a text widget to display the definition
definition_text = tk.Text(root, height=5, wrap=tk.WORD)
definition_text.grid(row=3, column=0, columnspan=2, sticky=tk.EW)

# Create a text widget to display the Ukrainian example
ukr_example_text = tk.Text(root, height=8, wrap=tk.WORD)
ukr_example_text.grid(row=5, column=0, sticky=tk.EW)

# Create a text widget to display the English example
eng_example_text = tk.Text(root, height=8, wrap=tk.WORD)
eng_example_text.grid(row=5, column=1, sticky=tk.EW)

# Configure column and row weights
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(1, weight=7)
root.grid_rowconfigure(2, weight=1)
root.grid_rowconfigure(3, weight=1)
root.grid_rowconfigure(4, weight=1)
root.grid_rowconfigure(5, weight=1)

# Bind the function to the Treeview
tree.bind('<Double-1>', show_example)

# Start the Tkinter event loop
root.mainloop()

# Close the database connection
conn.close()
