from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3
from tkinter import colorchooser
from configparser import ConfigParser

root = Tk()
root.title('FAG')
root.geometry("1000x550")




def query_database():
	# Clear the Treeview
	for record in my_tree.get_children():
		my_tree.delete(record)
		
	# Creation bdd creation
	conn = sqlite3.connect('tree_crm.db')

	# Creation curseur
	c = conn.cursor()

	c.execute("SELECT rowid, * FROM customers")
	records = c.fetchall()
	
	# ajout donnée sur ecran
	global count
	count = 0
	
	#enregistrement
	#print


	for record in records:
		if count % 2 == 0:
			my_tree.insert(parent='', index='end', iid=count, text='', values=(record[1], record[2], record[0]),  tags=('evenrow',))
		else:
			my_tree.insert(parent='', index='end', iid=count, text='', values=(record[1], record[2], record[0]),  tags=('oddrow',))
		# increment counter
		count += 1


	# changement
	conn.commit()

	# fermeture
	conn.close()




# Add Some Style
style = ttk.Style()

# Pick A Theme
style.theme_use('default')

# Configure the Treeview Colors
style.configure("Treeview",
	background="#D3D3D3",
	foreground="black",
	rowheight=25,
	fieldbackground="#D3D3D3")



# Create a Treeview Frame
tree_frame = Frame(root)
tree_frame.pack(pady=10)

# Create a Treeview Scrollbar
tree_scroll = Scrollbar(tree_frame)
tree_scroll.pack(side=RIGHT, fill=Y)

# Create The Treeview
my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended")
my_tree.pack()

# Config nav
tree_scroll.config(command=my_tree.yview)

# Denition colonne
my_tree['columns'] = ("Nom", "Prénom", "ID")

# forme colonne
my_tree.column("#0", width=0, stretch=NO)
my_tree.column("Nom", anchor=W, width=400)
my_tree.column("Prénom", anchor=W, width=400)
my_tree.column("ID", anchor=W, width=250)



# Creation en tete
my_tree.heading("#0", text="", anchor=W)
my_tree.heading("Nom", text="Nom", anchor=W)
my_tree.heading("Prénom", text="Prénom", anchor=W)
my_tree.heading("ID", text="ID", anchor=CENTER)







# enregistrement 
data_frame = LabelFrame(root, text="Enregistrement")
data_frame.pack(fill="x", expand="yes", padx=20)

fn_label = Label(data_frame, text="Nom")
fn_label.grid(row=0, column=0, padx=10, pady=10)
fn_entry = Entry(data_frame)
fn_entry.grid(row=0, column=1, padx=10, pady=10)

ln_label = Label(data_frame, text="Prénom")
ln_label.grid(row=0, column=2, padx=10, pady=10)
ln_entry = Entry(data_frame)
ln_entry.grid(row=0, column=3, padx=10, pady=10)

id_label = Label(data_frame, text="ID")
id_label.grid(row=0, column=4, padx=10, pady=10)
id_entry = Entry(data_frame)
id_entry.grid(row=0, column=5, padx=10, pady=10)



# up
def up():
	rows = my_tree.selection()
	for row in rows:
		my_tree.move(row, my_tree.parent(row), my_tree.index(row)-1)

#  Down
def down():
	rows = my_tree.selection()
	for row in reversed(rows):
		my_tree.move(row, my_tree.parent(row), my_tree.index(row)+1)

# Remove one record
def remove_one():
	x = my_tree.selection()[0]
	my_tree.delete(x)

	# Create a database or connect to one that exists
	conn = sqlite3.connect('tree_crm.db')

	# Create a cursor instance
	c = conn.cursor()

	# Delete From Database
	c.execute("DELETE from customers WHERE oid=" + id_entry.get())
	


	# Commit changes
	conn.commit()

	# Close our connection
	conn.close()

	# Clear The Entry Boxes
	clear_entries()

	# Add a little message box for fun
	messagebox.showinfo("supprimer!", "Votre selection a été supprimer")



# Remove Many records
def remove_many():
	# Add a little message box for fun
	response = messagebox.askyesno("WOAH!!!!", "Supprimer les fichiers sélectionnés \nêtes-vous sûr?! ")

	#Add logic for message box
	if response == 1:
		# Designate selections
		x = my_tree.selection()

		# Create List of ID's
		ids_to_delete = []
		
		# Add selections to ids_to_delete list
		for record in x:
			ids_to_delete.append(my_tree.item(record, 'values')[2])

		# Delete From Treeview
		for record in x:
			my_tree.delete(record)

		# Create a database or connect to one that exists
		conn = sqlite3.connect('tree_crm.db')

		# Create a cursor instance
		c = conn.cursor()
		

		# Delete Everything From The Table
		c.executemany("DELETE FROM customers WHERE id = ?", [(a,) for a in ids_to_delete])

		# Reset List
		ids_to_delete = []


		# Commit changes
		conn.commit()

		# Close our connection
		conn.close()

		# Clear entry boxes if filled
		clear_entries()


# Remove all records
def remove_all():
	# Add a little message box for fun
	response = messagebox.askyesno("WOAH!!!!", "cette action supprimera toutes les données\n êtes-vous sûr?!")

	#Add logic for message box
	if response == 1:
		# Clear the Treeview
		for record in my_tree.get_children():
			my_tree.delete(record)

		# Create a database or connect to one that exists
		conn = sqlite3.connect('tree_crm.db')

		# Create a cursor instance
		c = conn.cursor()

		# Delete Everything From The Table
		c.execute("DROP TABLE customers")
			


		# Commit changes
		conn.commit()

		# Close our connection
		conn.close()

		# Clear entry boxes if filled
		clear_entries()

		# Recreate The Table
		create_table_again()

# Clear entry boxes
def clear_entries():
	# Clear entry boxes
	fn_entry.delete(0, END)
	ln_entry.delete(0, END)
	id_entry.delete(0, END)


# Select Record
def select_record(e):
	# Clear entry boxes
	fn_entry.delete(0, END)
	ln_entry.delete(0, END)
	id_entry.delete(0, END)


	# Grab record Number
	selected = my_tree.focus()
	# Grab record values
	values = my_tree.item(selected, 'values')

	# outpus to entry boxes
	fn_entry.insert(0, values[0])
	ln_entry.insert(0, values[1])
	id_entry.insert(0, values[2])

# Update record
def update_record():
	# Grab the record number
	selected = my_tree.focus()
	# Update record
	my_tree.item(selected, text="", values=(fn_entry.get(), ln_entry.get(), id_entry.get(),))

	# Update the database
	# Create a database or connect to one that exists
	conn = sqlite3.connect('tree_crm.db')

	# Create a cursor instance
	c = conn.cursor()

	c.execute("""UPDATE customers SET
		first_name = :first,
		last_name = :last,
		address = :address,

		WHERE oid = :oid""",
		{
			'first': fn_entry.get(),
			'last': ln_entry.get(),
		})
	


	# Commit changes
	conn.commit()

	# Close our connection
	conn.close()


	# Clear entry boxes
	fn_entry.delete(0, END)
	ln_entry.delete(0, END)
	id_entry.delete(0, END)
	

# add new record to database
def add_record():
	# Update the database
	# Create a database or connect to one that exists
	conn = sqlite3.connect('tree_crm.db')

	# Create a cursor instance
	c = conn.cursor()

	# Add New Record
	c.execute("INSERT INTO customers VALUES (:first, :last, :id)",
		{
			'first': fn_entry.get(),
			'last': ln_entry.get(),
			'id': id_entry.get(),
		})
	

	# Commit changes
	conn.commit()

	# Close our connection
	conn.close()

	# Clear entry boxes
	fn_entry.delete(0, END)
	ln_entry.delete(0, END)
	id_entry.delete(0, END)


	# Clear The Treeview Table
	my_tree.delete(*my_tree.get_children())

	# Run to pull data from database on start
	query_database()

def create_table_again():
	# Create a database or connect to one that exists
	conn = sqlite3.connect('tree_crm.db')

	# Create a cursor instance
	c = conn.cursor()

	# Create Table
	c.execute("""CREATE TABLE if not exists customers (
		first_name text,
		last_name text,
		id integer)
		""")
	
	# Commit changes
	conn.commit()

	# Close our connection
	conn.close()

# Add Buttons
button_frame = LabelFrame(root, text="Commands")
button_frame.pack(fill="x", expand="yes", padx=20)

update_button = Button(button_frame, text="Modifier", command=update_record)
update_button.grid(row=0, column=0, padx=10, pady=10)

add_button = Button(button_frame, text="Ajouter", command=add_record)
add_button.grid(row=0, column=1, padx=10, pady=10)

remove_all_button = Button(button_frame, text="Supprimer tout", command=remove_all)
remove_all_button.grid(row=0, column=2, padx=10, pady=10)

remove_one_button = Button(button_frame, text="Supprimer la selection", command=remove_one)
remove_one_button.grid(row=0, column=3, padx=10, pady=10)

remove_many_button = Button(button_frame, text="Supprimer les selections", command=remove_many)
remove_many_button.grid(row=0, column=4, padx=10, pady=10)

move_up_button = Button(button_frame, text="UP", command=up)
move_up_button.grid(row=0, column=5, padx=10, pady=10)

move_down_button = Button(button_frame, text="DOWN", command=down)
move_down_button.grid(row=0, column=6, padx=10, pady=10)

select_record_button = Button(button_frame, text="Supprimer", command=clear_entries)
select_record_button.grid(row=0, column=7, padx=10, pady=10)

# Bind the treeview
my_tree.bind("<ButtonRelease-1>", select_record)

# Run to pull data from database on start
query_database()

root.mainloop()