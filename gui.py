from customtkinter import *
import fetcher
import checker
from datetime import datetime as dt
from tinydb import TinyDB, Query
import threading

#boilerplate
db = TinyDB('db.json')
query = Query()
app = CTk()
app.title("Spy Buster")
app.geometry("600x500")
app.resizable(False, False)
app.iconbitmap("spyware.ico")
set_appearance_mode("dark")
#########



#Update database

def update():
    update_button.configure(state="disabled")
    update_button.configure(text="Updating...")
    last_update_label.configure(text="Updating Database...")
    fetcher.update_database()
    update_button.configure(text="Already Updated")
    last_update_label.configure(text="Last Update: " + dt.now().strftime("%d-%m-%Y %H:%M"))


try:
    timestamp = db.search(query.timestamp.exists())[0]['timestamp']
except IndexError:
    timestamp = "No Data"
last_update_label = CTkLabel(app, text="Last Update: " + timestamp, font=("Inconsolata", 16), width=235)
last_update_label.grid(row=0, column=0, padx=40, pady=20)

update_button = CTkButton(app, corner_radius=10, text="Update Database", font=("Inconsolata", 12, "bold"), command=threading.Thread(target=update).start)
update_button.grid(row=0, column=1, padx=60, pady=20, sticky="ew")
#########


#Get input
select_units_label = CTkLabel(app, text="Select Unit:", font=("Inconsolata", 14))
select_units_label.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
units_options = CTkOptionMenu(app, values=["Soldiers", "Tanks", "Aircraft", "Ships", "Nukes", "Missiles"])
units_options.grid(row=2, column=0, padx=10, pady=5)

enter_count_label = CTkLabel(app, text="Number of Units Lost:", font=("Inconsolata", 14))
enter_count_label.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
units_count = CTkEntry(app, placeholder_text="Enter a number", width=180, insertontime=0, border_color="gray", placeholder_text_color="white", border_width=1)
units_count.grid(row=2, column=1, padx=10, pady=5)
#########



#Find spies
def list_spies():
    return checker.find_spies(units_options.get(), int(units_count.get()))


def find_spies_clicked():
    find_spies_button.configure(state="disabled")
    find_spies_button.configure(text="Finding Spies...")
    hold_label = CTkLabel(output_frame, text="Please wait, this may take a while...")
    hold_label.pack(padx=0, pady=0)
    spies = list_spies()
    if len(spies) == 0:
        hold_label.configure(text="No potential spies found.")
    else:
        hold_label.destroy()
        for spy in spies:
            spy_label = CTkLabel(output_frame, text=spy)
            spy_label.pack(padx=0, pady=0)
    find_spies_button.configure(text="Done")

def check_input():
    find_spies_button.configure(state="disabled")
    if len(units_count.get()) == 0:
        units_count.configure(border_color="red", placeholder_text_color="red", border_width=1)
        #units_count.configure(state="disabled")
        #units_count.configure(state="normal")
        units_count.after(1000, lambda: units_count.configure(border_color="gray", placeholder_text_color="white", border_width=1))
        find_spies_button.configure(state="normal")
    elif units_count.get().isnumeric() == False:
        units_count.delete(0, END)
        units_count.configure(border_color="red", placeholder_text_color="red", border_width=1)
        #units_count.configure(state="disabled")
        #units_count.configure(state="normal")
        units_count.after(1000, lambda: units_count.configure(border_color="gray", placeholder_text_color="white", border_width=1))
        find_spies_button.configure(state="normal")
    else:
        threading.Thread(target=find_spies_clicked).start()


find_spies_button = CTkButton(app, text="Find Spies", font=("Inconsolata", 12, "bold"), command=check_input)
find_spies_button.grid(row=4, columnspan=2, padx=10, pady=20)

output_frame = CTkScrollableFrame(app, orientation="vertical", label_text="Potential Spies", border_width=2, corner_radius=10)
output_frame.grid(row=5, columnspan=2, padx=(25, 0), pady=5, sticky="nsew")


app.mainloop()