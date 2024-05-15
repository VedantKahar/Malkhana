import datetime
import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3
import pandas as pd
import base64
from PIL import Image, ImageTk
from ttkthemes import ThemedStyle
import home.Homepage as homepage
import MalkhanaTable.MalkhanaPage as mk
import login.login as login
import logger as lu
import FSLInfo.FSLpage as f
import CourtInfo.Courtpage as cp
import Log.log as l
import printt.print as p
print_frame = None
sidebar_buttons = []


def printPage(prev_homepage_frame):
    prev_homepage_frame.destroy()

    global print_frame
    print_destroyer()
    print_frame = tk.Frame(prev_homepage_frame.master)
    print_frame.master.title("Print Page")
    print_frame.pack(fill=tk.BOTH, expand=True)

    # Create a sidebar with vertical tabs
    sidebar = tk.Frame(print_frame, bg="#2c3e50", width=200)
    sidebar.pack(side=tk.LEFT, fill=tk.Y)

    tabs = [
        ("Malkhana Info", mkpage),
        ("FSL Info", fsl),
        ("Court Info", court),
        ("Logs", log),
        ("Print", None),
        ("Log Out", logoutclicked),
    ]

    for text, command in tabs:
        if text == "Print":
            button = tk.Button(sidebar, text=text, background="#16a085", foreground="#ecf0f1", font=(
                "Helvetica", 12), width=20, height=2, relief=tk.FLAT)
        else:
            button = tk.Button(sidebar, text=text, background="#34495e", foreground="#ecf0f1", command=command, font=(
                "Helvetica", 12), width=20, height=2, relief=tk.FLAT)
        button.pack(fill=tk.X, pady=5, padx=10)

    # Barcode Input
    barcode_label = tk.Label(
        print_frame, text="Enter Barcode:", font=("Helvetica", 15))
    barcode_label.pack(pady=10)

    barcode_entry = tk.Entry(print_frame, font=("Helvetica", 15))
    barcode_entry.pack(pady=5)

    # Print Button
    print_button = tk.Button(print_frame, text="Print Details", command=lambda: print_details(barcode_entry.get()),
                             background="#f6f4f2", font=("Helvetica", 15), width=15, height=1)
    print_button.pack(pady=10)

    # Back Button
    back_button = tk.Button(print_frame, text="Back", command=go_back,
                            background="#f6f4f2", font=("Helvetica", 15), width=15, height=1)
    back_button.pack(pady=10)

    print_frame.mainloop()


def print_details(barcode):
    try:
        if not barcode:
            messagebox.showwarning("Warning", "Barcode cannot be empty.")
            return

        current_time = str(datetime.datetime.now()).replace(":", "")
        filename = f"{barcode}_{current_time}.xlsx"

        # Initialize Excel writer with 'w' mode to create the file if not exists
        with pd.ExcelWriter(filename, mode='w') as writer:
            # Fetch data from items_in_malkhana.db and write to Items sheet
            conn_items = sqlite3.connect('databases/items_in_malkhana.db')
            query_items = "SELECT * FROM items WHERE barcode = ?"
            df_items = pd.read_sql_query(
                query_items, conn_items, params=(barcode,))
            conn_items.close()
            df_items.to_excel(writer, sheet_name='Items', index=False)

            # Fetch data from fsl_records.db and write to FSL Records sheet
            conn_fsl = sqlite3.connect('databases/fsl_records.db')
            query_fsl = "SELECT * FROM fsl_records WHERE barcode = ?"
            df_fsl = pd.read_sql_query(query_fsl, conn_fsl, params=(barcode,))
            conn_fsl.close()
            df_fsl.to_excel(writer, sheet_name='FSL Records', index=False)

            # Fetch data from logs.db and write to Logs sheet
            conn_logs = sqlite3.connect('databases/logs.db')
            query_logs = "SELECT * FROM logs WHERE barcode = ?"
            df_logs = pd.read_sql_query(
                query_logs, conn_logs, params=(barcode,))
            conn_logs.close()
            df_logs.to_excel(writer, sheet_name='Logs', index=False)

            # Fetch image data from attachments.db and write to Attachments sheet
            conn_attachments = sqlite3.connect('databases/attachments.db')
            query_attachments = "SELECT attachment_data FROM attachments WHERE barcode = ?"
            df_attachments = pd.read_sql_query(
                query_attachments, conn_attachments, params=(barcode,))
            conn_attachments.close()

            if not df_attachments.empty:
                # Encode image data as Base64
                df_attachments['Encoded_Image'] = df_attachments['attachment_data'].apply(
                    lambda x: base64.b64encode(x).decode('utf-8'))
                # Write image data to Attachments sheet
                df_attachments.to_excel(
                    writer, sheet_name='Attachments', index=False)

        messagebox.showinfo("Success", "Data exported to Excel successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


def print_destroyer():
    global print_frame
    if print_frame is not None:
        print_frame.destroy()


def go_back():
    print_destroyer()
    homepage.open_homepage(print_frame)


def go_home():
    print_destroyer()
    homepage.open_homepage(print_frame)


def logoutclicked():
    lu.log_activity(login.current_user, "LOG-OUT")
    print_destroyer()
    login.initloginpage(print_frame)


def mkpage():
    print_destroyer()
    mk.mkpage(print_frame)


def court():
    print_destroyer()
    cp.view_court(print_frame)


def fsl():
    print_destroyer()
    f.viewfsl(print_frame)


def log():
    print_destroyer()
    l.create_logs_page(print_frame)
