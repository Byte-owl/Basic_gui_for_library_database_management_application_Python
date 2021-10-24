#Mini_Project(DBMS)(Library Database) - Ayush
#Version: 1.1
#Database GUI (3 Tables)


#importing necessary libraries
import mysql.connector
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
from datetime import date
import re
import csv
import os
import time


class DatabaseGui(tk.Tk):

    def __init__(self, db_obj, user_name):

        """Basic window attributes"""
        try:
            super().__init__()
            
            #initializing variables
            self.db_obj = db_obj
            self.user_name = user_name
            self.book_details_frames_run_flag = 0
            self.member_details_frames_run_flag = 0
            self.borrow_transaction_details_frames_run_flag = 0
            self.res_val_books = []
            self.res_val_members = []
            self.res_val_borrow_transactions = []

            #variables for sliding animation for title
            self.og_table_sel_text = "TABLES"
            self.text_sliding_animation_table_sel_index = 0
            self.text_to_be_displayed = ""
            
            #basic window attributes
            self.title("BASIC-DB Library")
            self.geometry("{width}x{height}+0+0".format(width=self.winfo_screenwidth(), height=self.winfo_screenheight()))
            try:
                self.state("zoomed")
            except Exception as err:
                messagebox.showerror("Error", "Unable to maximize window!\n"+str(err), parent=self)
            self.iconbitmap("images/Logo_icon.ico")
            
            #Background
            bg_db_gui_img = Image.open("images/Bg_Login.jpg")
            resized_bg_db = bg_db_gui_img.resize((self.winfo_width(), self.winfo_height()), Image.ANTIALIAS)
            self.bg_db_gui = ImageTk.PhotoImage(resized_bg_db)
            bg_db_gui_canvas = tk.Canvas(self, width=self.winfo_width(), height=self.winfo_height())
            bg_db_gui_canvas.pack(fill="both", expand=True)
            bg_db_gui_canvas.create_image(0, 0, image=self.bg_db_gui, anchor="nw")

            #treeview style
            style_treeview = ttk.Style(self)
            style_treeview.theme_use("clam")
            style_treeview.configure("Treeview", background="lightgrey", fieldbackground="White", foreground="Black", font=("Cambria", 15), rowheight=40)
            style_treeview.configure("Treeview.Heading", background="lightgrey", foreground="Crimson", font=("Cambria", 15))

            #table creation
            with self.db_obj.cursor(buffered=True) as db_cursor:
                try:
                    db_cursor.execute("""CREATE TABLE IF NOT EXISTS BOOK_DETAILS (book_id VARCHAR(25), 
                    book_title VARCHAR(255), isbn VARCHAR(20), author VARCHAR(255), publisher VARCHAR(255), 
                    year INT, genre VARCHAR(255), borrow_status VARCHAR(255), book_condition VARCHAR(255), 
                    entry_made_or_alt_by VARCHAR(255), 
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, PRIMARY KEY (book_id))""")
                except Exception as err_msg:
                    raise Exception ("Table (BOOK_DETAILS) creation failed... rolling back to last commit"+str(err_msg))
                    self.db_obj.rollback()
                else:
                    self.db_obj.commit()


                try:
                    db_cursor.execute("""CREATE TABLE IF NOT EXISTS MEMBER_DETAILS (member_id VARCHAR(25), 
                    member_name VARCHAR(255), gender VARCHAR(25), dob date, email VARCHAR(350), phone_no VARCHAR(20), 
                    address VARCHAR(500), occupation VARCHAR(50), membership VARCHAR(100), 
                    entry_made_or_alt_by VARCHAR(255), 
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, PRIMARY KEY (member_id))""")
                except Exception as err_msg:
                    raise Exception ("Table (MEMBER_DETAILS) creation failed... rolling back to last commit"+str(err_msg))
                    self.db_obj.rollback()
                else:
                    self.db_obj.commit()


                try:
                    db_cursor.execute("""CREATE TABLE IF NOT EXISTS BORROW_TRANSACTION_DETAILS (borrow_trans_id VARCHAR(25), 
                    book_id VARCHAR(25), member_id VARCHAR(25), book_issue_date date, book_return_date date, 
                    fine FLOAT DEFAULT 0.0, status VARCHAR(255), entry_made_or_alt_by VARCHAR(255), 
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, 
                    FOREIGN KEY (book_id) REFERENCES BOOK_DETAILS(book_id), 
                    FOREIGN KEY (member_id) REFERENCES MEMBER_DETAILS(member_id), PRIMARY KEY (borrow_trans_id))""")
                except Exception as err_msg:
                    raise Exception ("Table (BORROW_TRANSACTION_DETAILS) creation failed... rolling back to last commit"+str(err_msg))
                    self.db_obj.rollback()
                else:
                    self.db_obj.commit()

        except Exception as err_msg:
            messagebox.showerror("Error", "Closing Application: \n\n"+str(err_msg), parent=self)
            self.destroy()





    def sliding_animation_title_table_sel(self):

        """Sliding animation function"""

        try:
            if (self.text_sliding_animation_table_sel_index >= len(self.og_table_sel_text)):
                self.text_sliding_animation_table_sel_index = 0
                self.text_to_be_displayed = ""
                self.title_db_gui.config(text=self.text_to_be_displayed)
            else:
                self.text_to_be_displayed += self.og_table_sel_text[self.text_sliding_animation_table_sel_index]
                self.title_db_gui.config(text=self.text_to_be_displayed)
                self.text_sliding_animation_table_sel_index += 1
                
            #timer set to 450 ms
            self.run_task_sliding_animation_title_table_sel = self.title_db_gui.after(450, self.sliding_animation_title_table_sel)
        
        except Exception as err_msg:
            messagebox.showerror("Error", "Sliding animation error", parent=self)





    def table_sel_fun(self):
        
        """Table selection function            
            Initial Frame Creation"""
        
        try:
            self.db_gui_frame_1 = tk.Frame(self, bg="White")
            self.db_gui_frame_1.place(x=int(self.winfo_width()*0.3), y=int(self.winfo_height()*0.3), width=int(self.winfo_width()*0.4), height=int(self.winfo_height()*0.4))

            #Attributes
            self.title_db_gui = tk.Label(self.db_gui_frame_1, text="TABLES", font=("Algerian", 40), bg="White", fg="Black")
            self.title_db_gui.place(x=int(self.winfo_width()*0.126), y=int(self.winfo_height()*0.025))
                        
            desc_db_gui = tk.Label(self.db_gui_frame_1, text="Select table:", font=("Cambria", 16), bg="White", fg="Black")
            desc_db_gui.place(x=int(self.winfo_width()*0.160), y=int(self.winfo_height()*0.125))

            #buttons
            book_details_sel_btn = tk.Button(self.db_gui_frame_1, text="Book\nDetails", command=self.clear_frames_for_book_details_fun, cursor="hand2", fg="Black", bg="Crimson", font=("Bookman Old Style", 15, "bold"), activebackground="#a30f2d", activeforeground="White", width=int(self.winfo_width()*0.008), height=int(self.winfo_height()*0.004))
            book_details_sel_btn.place(x=int(self.winfo_width()*0.0198), y=int(self.winfo_height()*0.23))

            borrow_transaction_details_sel_btn = tk.Button(self.db_gui_frame_1, text="Borrow\nTransactions", command=self.clear_frames_for_borrow_transaction_details_fun, cursor="hand2", fg="Black", bg="Crimson", font=("Bookman Old Style", 15, "bold"), activebackground="#a30f2d", activeforeground="White", width=int(self.winfo_width()*0.009), height=int(self.winfo_height()*0.004))
            borrow_transaction_details_sel_btn.place(x=int(self.winfo_width()*0.1395), y=int(self.winfo_height()*0.23))

            member_details_sel_btn = tk.Button(self.db_gui_frame_1, text="Member\nDetails", command=self.clear_frames_for_member_details_fun, cursor="hand2", fg="Black", bg="Crimson", font=("Bookman Old Style", 15, "bold"), activebackground="#a30f2d", activeforeground="White", width=int(self.winfo_width()*0.008), height=int(self.winfo_height()*0.004))
            member_details_sel_btn.place(x=int(self.winfo_width()*0.278), y=int(self.winfo_height()*0.23))
        
        except Exception as err_msg:
            messagebox.showerror("Error", "Frames and widgets error...\n\n"+str(err_msg), parent=self)



    def clear_frames_for_book_details_fun(self):
        
        """Removes initial frames and calls book_details_tab_fun()"""

        try:
            self.db_gui_frame_1.place_forget()
            if (self.book_details_frames_run_flag):
                self.db_gui_frame_2.place(x=int(self.winfo_width()*0.05), y=int(self.winfo_height()*0.05), width=int(self.winfo_width()*0.9), height=int(self.winfo_height()*0.35))
                self.db_gui_frame_3.place(x=int(self.winfo_width()*0.05), y=int(self.winfo_height()*0.45), width=int(self.winfo_width()*0.9), height=int(self.winfo_height()*0.50))
            else:
                self.book_details_tab_fun()
        
        except Exception as err_msg:
            messagebox.showerror("Error", "'Book details' table: frame creation error\n\n"+str(err_msg), parent=self)



    def clear_frames_for_member_details_fun(self):
        
        """Removes initial frames and calls member_details_tab_fun()"""

        try:
            self.db_gui_frame_1.place_forget()
            if (self.member_details_frames_run_flag):
                self.db_gui_frame_4.place(x=int(self.winfo_width()*0.05), y=int(self.winfo_height()*0.05), width=int(self.winfo_width()*0.9), height=int(self.winfo_height()*0.35))
                self.db_gui_frame_5.place(x=int(self.winfo_width()*0.05), y=int(self.winfo_height()*0.45), width=int(self.winfo_width()*0.9), height=int(self.winfo_height()*0.50))
            else:
                self.member_details_tab_fun()
        
        except Exception as err_msg:
            messagebox.showerror("Error", "'Member details' table: frame creation error\n\n"+str(err_msg), parent=self)



    def clear_frames_for_borrow_transaction_details_fun(self):
        
        """Removes initial frames and calls borrow_transactions_tab_fun()"""

        try:
            self.db_gui_frame_1.place_forget()
            if (self.borrow_transaction_details_frames_run_flag):
                self.db_gui_frame_6.place(x=int(self.winfo_width()*0.05), y=int(self.winfo_height()*0.05), width=int(self.winfo_width()*0.9), height=int(self.winfo_height()*0.35))
                self.db_gui_frame_7.place(x=int(self.winfo_width()*0.05), y=int(self.winfo_height()*0.45), width=int(self.winfo_width()*0.9), height=int(self.winfo_height()*0.50))
            else:
                self.borrow_transactions_tab_fun()
        
        except Exception as err_msg:
            messagebox.showerror("Error", "'Borrow transactions' table: frame creation error\n\n"+str(err_msg), parent=self)





    def book_details_tab_fun(self):
        
        """BOOK_DETAILS TABLE frames and widgets"""

        try:
            #flag
            self.book_details_frames_run_flag = 1

            #initial frames
            self.db_gui_frame_2 = tk.Frame(self, bg="White")
            self.db_gui_frame_2.place(x=int(self.winfo_width()*0.05), y=int(self.winfo_height()*0.05), width=int(self.winfo_width()*0.9), height=int(self.winfo_height()*0.35))

            self.db_gui_frame_3 = tk.Frame(self, bg="White")
            self.db_gui_frame_3.place(x=int(self.winfo_width()*0.05), y=int(self.winfo_height()*0.45), width=int(self.winfo_width()*0.9), height=int(self.winfo_height()*0.50))

            
            #Attributes
            self.book_id_var_book = tk.IntVar(value=1)
            book_id_checkbox_book = tk.Checkbutton(self.db_gui_frame_2, text="", variable=self.book_id_var_book)
            book_id_checkbox_book.place(x=int(self.winfo_width()*0.02), y=int(self.winfo_height()*0.04))

            book_id_label_book = tk.Label(self.db_gui_frame_2, text="Book ID: ", font=("Cambria", 15), bg="White", fg="Black")
            book_id_label_book.place(x=int(self.winfo_width()*0.04), y=int(self.winfo_height()*0.04))

            self.txt_book_id_entry = tk.Entry(self.db_gui_frame_2, font=("Times New Roman", 15), bg="lightgrey", width=int(self.winfo_width()*0.016))
            self.txt_book_id_entry.place(x=int(self.winfo_width()*0.14), y=int(self.winfo_height()*0.04))
            

            self.title_var_book = tk.IntVar(value=1)
            title_checkbox_book = tk.Checkbutton(self.db_gui_frame_2, text="", variable=self.title_var_book)
            title_checkbox_book.place(x=int(self.winfo_width()*0.02), y=int(self.winfo_height()*0.11))

            title_label_book = tk.Label(self.db_gui_frame_2, text="Book Title: ", font=("Cambria", 15), bg="White", fg="Black")
            title_label_book.place(x=int(self.winfo_width()*0.04), y=int(self.winfo_height()*0.11))

            self.txt_book_title_entry = tk.Entry(self.db_gui_frame_2, font=("Times New Roman", 15), bg="lightgrey", width=int(self.winfo_width()*0.016))
            self.txt_book_title_entry.place(x=int(self.winfo_width()*0.14), y=int(self.winfo_height()*0.11))
            

            self.isbn_var_book = tk.IntVar(value=1)
            isbn_checkbox_book = tk.Checkbutton(self.db_gui_frame_2, text="", variable=self.isbn_var_book)
            isbn_checkbox_book.place(x=int(self.winfo_width()*0.02), y=int(self.winfo_height()*0.18))

            isbn_label_book = tk.Label(self.db_gui_frame_2, text="ISBN: ", font=("Cambria", 15), bg="White", fg="Black")
            isbn_label_book.place(x=int(self.winfo_width()*0.04), y=int(self.winfo_height()*0.18))

            self.txt_book_isbn_entry = tk.Entry(self.db_gui_frame_2, font=("Times New Roman", 15), bg="lightgrey", width=int(self.winfo_width()*0.016))
            self.txt_book_isbn_entry.place(x=int(self.winfo_width()*0.14), y=int(self.winfo_height()*0.18))
            

            self.author_var_book = tk.IntVar(value=1)
            author_checkbox_book = tk.Checkbutton(self.db_gui_frame_2, text="", variable=self.author_var_book)
            author_checkbox_book.place(x=int(self.winfo_width()*0.31), y=int(self.winfo_height()*0.04))

            author_label_book = tk.Label(self.db_gui_frame_2, text="Author: ", font=("Cambria", 15), bg="White", fg="Black")
            author_label_book.place(x=int(self.winfo_width()*0.33), y=int(self.winfo_height()*0.04))

            self.txt_book_author_entry = tk.Entry(self.db_gui_frame_2, font=("Times New Roman", 15), bg="lightgrey", width=int(self.winfo_width()*0.016))
            self.txt_book_author_entry.place(x=int(self.winfo_width()*0.43), y=int(self.winfo_height()*0.04))
            

            self.publisher_var_book = tk.IntVar(value=1)
            publisher_checkbox_book = tk.Checkbutton(self.db_gui_frame_2, text="", variable=self.publisher_var_book)
            publisher_checkbox_book.place(x=int(self.winfo_width()*0.31), y=int(self.winfo_height()*0.11))

            publisher_label_book = tk.Label(self.db_gui_frame_2, text="Publisher: ", font=("Cambria", 15), bg="White", fg="Black")
            publisher_label_book.place(x=int(self.winfo_width()*0.33), y=int(self.winfo_height()*0.11))

            self.txt_book_publisher_entry = tk.Entry(self.db_gui_frame_2, font=("Times New Roman", 15), bg="lightgrey", width=int(self.winfo_width()*0.016))
            self.txt_book_publisher_entry.place(x=int(self.winfo_width()*0.43), y=int(self.winfo_height()*0.11))
            

            self.year_var_book = tk.IntVar(value=1)
            year_checkbox_book = tk.Checkbutton(self.db_gui_frame_2, text="", variable=self.year_var_book)
            year_checkbox_book.place(x=int(self.winfo_width()*0.31), y=int(self.winfo_height()*0.18))

            year_label_book = tk.Label(self.db_gui_frame_2, text="Year: ", font=("Cambria", 15), bg="White", fg="Black")
            year_label_book.place(x=int(self.winfo_width()*0.33), y=int(self.winfo_height()*0.18))

            self.txt_book_year_entry = tk.Entry(self.db_gui_frame_2, font=("Times New Roman", 15), bg="lightgrey", width=int(self.winfo_width()*0.016))
            self.txt_book_year_entry.place(x=int(self.winfo_width()*0.43), y=int(self.winfo_height()*0.18))
            

            self.genre_var_book = tk.IntVar(value=1)
            genre_checkbox_book = tk.Checkbutton(self.db_gui_frame_2, text="", variable=self.genre_var_book)
            genre_checkbox_book.place(x=int(self.winfo_width()*0.60), y=int(self.winfo_height()*0.04))

            genre_label_book = tk.Label(self.db_gui_frame_2, text="Genre: ", font=("Cambria", 15), bg="White", fg="Black")
            genre_label_book.place(x=int(self.winfo_width()*0.62), y=int(self.winfo_height()*0.04))
            
            self.txt_book_genre_entry = tk.Entry(self.db_gui_frame_2, font=("Times New Roman", 15), bg="lightgrey", width=int(self.winfo_width()*0.016))
            self.txt_book_genre_entry.place(x=int(self.winfo_width()*0.72), y=int(self.winfo_height()*0.04))
            

            self.borrow_status_var_book = tk.IntVar(value=1)
            borrow_status_checkbox_book = tk.Checkbutton(self.db_gui_frame_2, text="", variable=self.borrow_status_var_book)
            borrow_status_checkbox_book.place(x=int(self.winfo_width()*0.60), y=int(self.winfo_height()*0.11))

            borrow_status_label_book = tk.Label(self.db_gui_frame_2, text="Borrow Status: ", font=("Cambria", 15), bg="White", fg="Black")
            borrow_status_label_book.place(x=int(self.winfo_width()*0.62), y=int(self.winfo_height()*0.11))

            self.txt_book_borrow_status_entry = tk.Entry(self.db_gui_frame_2, font=("Times New Roman", 15), bg="lightgrey", width=int(self.winfo_width()*0.016))
            self.txt_book_borrow_status_entry.place(x=int(self.winfo_width()*0.72), y=int(self.winfo_height()*0.11))
            

            self.condition_var_book = tk.IntVar(value=1)
            condition_checkbox_book = tk.Checkbutton(self.db_gui_frame_2, text="", variable=self.condition_var_book)
            condition_checkbox_book.place(x=int(self.winfo_width()*0.60), y=int(self.winfo_height()*0.18))

            condition_label_book = tk.Label(self.db_gui_frame_2, text="Condition: ", font=("Cambria", 15), bg="White", fg="Black")
            condition_label_book.place(x=int(self.winfo_width()*0.62), y=int(self.winfo_height()*0.18))

            self.txt_book_condition_entry = tk.Entry(self.db_gui_frame_2, font=("Times New Roman", 15), bg="lightgrey", width=int(self.winfo_width()*0.016))
            self.txt_book_condition_entry.place(x=int(self.winfo_width()*0.72), y=int(self.winfo_height()*0.18))
            

            #buttons
            back_btn = tk.Button(self.db_gui_frame_2, text=chr(8630)+" Back", command=self.clear_book_details_frames_for_tab_sel_fun, cursor="hand2", fg="Black", bg="Crimson", font=("Calibri", 15, "bold"), activebackground="#a30f2d", activeforeground="White", width=int(self.winfo_width()*0.008), height=int(self.winfo_height()*0.002))
            back_btn.place(x=int(self.winfo_width()*0.06), y=int(self.winfo_height()*0.26))

            insert_btn = tk.Button(self.db_gui_frame_2, text="Insert", command=self.books_insert_fun, cursor="hand2", fg="Black", bg="Crimson", font=("Calibri", 15, "bold"), activebackground="#a30f2d", activeforeground="White", width=int(self.winfo_width()*0.008), height=int(self.winfo_height()*0.002))
            insert_btn.place(x=int(self.winfo_width()*0.16), y=int(self.winfo_height()*0.26))

            update_btn = tk.Button(self.db_gui_frame_2, text="Update", command=self.books_update_fun, cursor="hand2", fg="Black", bg="Crimson", font=("Calibri", 15, "bold"), activebackground="#a30f2d", activeforeground="White", width=int(self.winfo_width()*0.008), height=int(self.winfo_height()*0.002))
            update_btn.place(x=int(self.winfo_width()*0.26), y=int(self.winfo_height()*0.26))

            delete_btn = tk.Button(self.db_gui_frame_2, text="Delete", command=self.books_delete_fun, cursor="hand2", fg="Black", bg="Crimson", font=("Calibri", 15, "bold"), activebackground="#a30f2d", activeforeground="White", width=int(self.winfo_width()*0.008), height=int(self.winfo_height()*0.002))
            delete_btn.place(x=int(self.winfo_width()*0.36), y=int(self.winfo_height()*0.26))

            search_btn = tk.Button(self.db_gui_frame_2, text="Search", command=self.books_search_fun, cursor="hand2", fg="Black", bg="Crimson", font=("Calibri", 15, "bold"), activebackground="#a30f2d", activeforeground="White", width=int(self.winfo_width()*0.008), height=int(self.winfo_height()*0.002))
            search_btn.place(x=int(self.winfo_width()*0.46), y=int(self.winfo_height()*0.26))

            view_all_btn = tk.Button(self.db_gui_frame_2, text="View all", command=self.books_view_all_fun, cursor="hand2", fg="Black", bg="Crimson", font=("Calibri", 15, "bold"), activebackground="#a30f2d", activeforeground="White", width=int(self.winfo_width()*0.008), height=int(self.winfo_height()*0.002))
            view_all_btn.place(x=int(self.winfo_width()*0.56), y=int(self.winfo_height()*0.26))

            insert_btn = tk.Button(self.db_gui_frame_2, text="Clear", command=self.books_frontend_widgets_clear_fun, cursor="hand2", fg="Black", bg="Crimson", font=("Calibri", 15, "bold"), activebackground="#a30f2d", activeforeground="White", width=int(self.winfo_width()*0.008), height=int(self.winfo_height()*0.002))
            insert_btn.place(x=int(self.winfo_width()*0.66), y=int(self.winfo_height()*0.26))

            export_to_csv_btn = tk.Button(self.db_gui_frame_2, text="Export", command=self.books_export_to_csv_fun, cursor="hand2", fg="Black", bg="Crimson", font=("Calibri", 15, "bold"), activebackground="#a30f2d", activeforeground="White", width=int(self.winfo_width()*0.008), height=int(self.winfo_height()*0.002))
            export_to_csv_btn.place(x=int(self.winfo_width()*0.76), y=int(self.winfo_height()*0.26))

            #Data view widget
            self.display_info_view_book_details = ttk.Treeview(self.db_gui_frame_3, selectmode ="browse")
            self.display_info_view_book_details["columns"] = ("Book ID", "Title", "ISBN", "Author", "Publisher", "Year", "Genre", "Borrow status", "Condition", "Data entered by", "Timestamp")

            #treeview style
            """Currently set to common style as defined in construtor"""

            self.display_info_view_book_details.column("#0", width=0, stretch="NO")
            for label in list(self.display_info_view_book_details["columns"]):
                self.display_info_view_book_details.column(label, anchor=tk.CENTER, minwidth=int(self.winfo_width()*0.04))
                self.display_info_view_book_details.heading(label, text=label, anchor=tk.CENTER)
            
            self.display_info_view_book_details.place(x=int(self.winfo_width()*0), y=int(self.winfo_height()*0), width=int(self.winfo_width()*0.9), height=int(self.winfo_height()*0.5))
            self.display_info_view_book_details.bind("<ButtonRelease-1>", self.select_row_treeview_books_fun)

            #Scrollbars
            verscrlbar_display_info_view_book_details = ttk.Scrollbar(self.display_info_view_book_details, orient ="vertical", command = self.display_info_view_book_details.yview)
            verscrlbar_display_info_view_book_details.pack(side ='right', fill ='y')
            self.display_info_view_book_details.configure(yscrollcommand = verscrlbar_display_info_view_book_details.set)

            horscrlbar_display_info_view_book_details = ttk.Scrollbar(self.display_info_view_book_details, orient ="horizontal", command = self.display_info_view_book_details.xview)
            horscrlbar_display_info_view_book_details.pack(side ='bottom', fill ='x')
            self.display_info_view_book_details.configure(xscrollcommand = horscrlbar_display_info_view_book_details.set)

        except Exception as err_msg:
            messagebox.showerror("Error", "Frames and widgets error...\n\n"+str(err_msg), parent=self)



    def clear_book_details_frames_for_tab_sel_fun(self):
        
        """Removes frames and calls table_sel_fun() (for BOOK_DETAILS)"""

        try:
            if (messagebox.askyesno("Return back", "Do you wish to run 'Clear' operation before leaving?\n\nRecommended action: Press 'Yes' for efficient memory usage")):
                #clear treeview
                self.display_info_view_book_details.delete(*self.display_info_view_book_details.get_children())
                
                #clear entry widgets
                self.txt_book_id_entry.delete(0, 'end')
                self.txt_book_title_entry.delete(0, 'end')
                self.txt_book_isbn_entry.delete(0, 'end')
                self.txt_book_author_entry.delete(0, 'end')
                self.txt_book_publisher_entry.delete(0, 'end')
                self.txt_book_year_entry.delete(0, 'end')
                self.txt_book_genre_entry.delete(0, 'end')
                self.txt_book_borrow_status_entry.delete(0, 'end')
                self.txt_book_condition_entry.delete(0, 'end')

                #checkbox widget (selected state)
                self.book_id_var_book.set(1)
                self.title_var_book.set(1)
                self.isbn_var_book.set(1)
                self.author_var_book.set(1)
                self.publisher_var_book.set(1)
                self.year_var_book.set(1)
                self.genre_var_book.set(1)
                self.borrow_status_var_book.set(1)
                self.condition_var_book.set(1)
                
                #clearing res variable data
                self.res_val_books = []

            self.db_gui_frame_2.place_forget()
            self.db_gui_frame_3.place_forget()
            self.db_gui_frame_1.place(x=int(self.winfo_width()*0.3), y=int(self.winfo_height()*0.3), width=int(self.winfo_width()*0.4), height=int(self.winfo_height()*0.4))
        
        except Exception as err_msg:
            messagebox.showerror("Error", "Error while returning...\n\n"+str(err_msg), parent=self)



    def books_insert_fun(self):
        
        """Insert Operation (BOOK_DETAILS Table)"""

        try:
            #clearing res variable data
            self.res_val_books = []
            #clear treeview
            self.display_info_view_book_details.delete(*self.display_info_view_book_details.get_children())
            
            #get values
            values_gather_dict_books = {"book_id" : (self.book_id_var_book.get(), self.txt_book_id_entry.get()), 
            "book_title" : (self.title_var_book.get(), self.txt_book_title_entry.get()), 
            "isbn" : (self.isbn_var_book.get(), self.txt_book_isbn_entry.get()), 
            "author" : (self.author_var_book.get(), self.txt_book_author_entry.get()), 
            "publisher" : (self.publisher_var_book.get(), self.txt_book_publisher_entry.get()), 
            "year" : (self.year_var_book.get(), self.txt_book_year_entry.get()), 
            "genre" : (self.genre_var_book.get(), self.txt_book_genre_entry.get()), 
            "borrow_status" : (self.borrow_status_var_book.get(), self.txt_book_borrow_status_entry.get()), 
            "book_condition" : (self.condition_var_book.get(), self.txt_book_condition_entry.get()), 
            "entry_made_or_alt_by": (1, self.user_name)}
                        
            #book_id validation
            if (values_gather_dict_books["book_id"][0]):
                if ((not values_gather_dict_books["book_id"][1]) or (str(values_gather_dict_books["book_id"][1]).isspace())):
                    raise Exception ("Invalid Book ID!!")
            else:
                raise Exception ("Book ID is a mandatory field (chechkbox should be in on state)!!")

            #year validation
            if (values_gather_dict_books["year"][0]):
                if ((not str(values_gather_dict_books["year"][1]).isnumeric())):
                    raise Exception ("Year should be numeric!!")
                if (int(values_gather_dict_books["year"][1]) == 0):
                    raise Exception ("'Year' entry cannot not be zero!!")
                if (int(values_gather_dict_books["year"][1]) > (date.today()).year):
                    raise Exception ("Invalid Year entry!!")
            
            columns_books = []
            values_books = []
            for col in values_gather_dict_books.keys():
                #appending to apt list
                columns_books.append(col)
                if ((col == "year") and (not values_gather_dict_books[col][0])):
                    #appending to apt list
                    values_books.append(0)
                #appending to apt list
                values_books.append(values_gather_dict_books[col][1]*values_gather_dict_books[col][0])


            #statement
            books_insert_stmnt = "INSERT INTO BOOK_DETAILS ("+", ".join(columns_books)+") values ("+("%s, "*len(columns_books))[:-2]+");"
            
            with self.db_obj.cursor(buffered=True) as db_cursor:
                try:
                    db_cursor.execute(books_insert_stmnt, tuple(values_books))
                    db_cursor.execute("SELECT * FROM BOOK_DETAILS where book_id = %s", (values_gather_dict_books["book_id"][1],))
                    self.res_val_books = [db_cursor.fetchone()]
                except Exception as err_msg:
                    raise Exception ("SQL error... rolling back to last commit\n\n"+str(err_msg))
                else:
                    self.display_info_view_book_details.insert(parent="", index="end", values=self.res_val_books[0])
                    self.db_obj.commit()
        
        except Exception as err_msg:
            messagebox.showerror("Error", "Insert operation failed\n\n"+str(err_msg), parent=self)
            self.db_obj.rollback()



    def books_update_fun(self):

        """Update Operation (BOOK_DETAILS Table)"""

        try:
            #clearing res variable data
            self.res_val_books = []
            #clear treeview
            self.display_info_view_book_details.delete(*self.display_info_view_book_details.get_children())
            
            #get values
            values_gather_dict_books = {"book_id" : (self.book_id_var_book.get(), self.txt_book_id_entry.get()), 
            "book_title" : (self.title_var_book.get(), self.txt_book_title_entry.get()), 
            "isbn" : (self.isbn_var_book.get(), self.txt_book_isbn_entry.get()), 
            "author" : (self.author_var_book.get(), self.txt_book_author_entry.get()), 
            "publisher" : (self.publisher_var_book.get(), self.txt_book_publisher_entry.get()), 
            "year" : (self.year_var_book.get(), self.txt_book_year_entry.get()), 
            "genre" : (self.genre_var_book.get(), self.txt_book_genre_entry.get()), 
            "borrow_status" : (self.borrow_status_var_book.get(), self.txt_book_borrow_status_entry.get()), 
            "book_condition" : (self.condition_var_book.get(), self.txt_book_condition_entry.get()), 
            "entry_made_or_alt_by": (1, self.user_name)}
            
            #book_id validation
            if (values_gather_dict_books["book_id"][0]):
                if ((not values_gather_dict_books["book_id"][1]) or (str(values_gather_dict_books["book_id"][1]).isspace())):
                    raise Exception ("Invalid Book ID!!")
            else:
                raise Exception ("Book ID is a mandatory field (chechkbox should be selected)!!")
            
            #Number of attributes selected
            if (sum(int(i[0]) for i in values_gather_dict_books.values()) < 3):
                raise Exception ("Atleast one attribute needs to be selected other than Book ID!!")

            #year validation
            if (values_gather_dict_books["year"][0]):
                if ((not str(values_gather_dict_books["year"][1]).isnumeric())):
                    raise Exception ("Year should be numeric!!")
                if (int(values_gather_dict_books["year"][1]) == 0):
                    raise Exception ("'Year' entry cannot not be zero!!")
                if (int(values_gather_dict_books["year"][1]) > (date.today()).year):
                    raise Exception ("Invalid Year entry!!")
            
            columns_books = []
            values_books = []
            for col in values_gather_dict_books.keys():
                if ((values_gather_dict_books[col][0]) and (col != "book_id")):
                    #appending to apt list
                    columns_books.append(col)
                    values_books.append(values_gather_dict_books[col][1])
                        
            #appending book_id
            values_books.append(values_gather_dict_books["book_id"][1])

            #statement
            books_update_stmnt = "UPDATE BOOK_DETAILS SET "+" = %s, ".join(columns_books)+" = %s where book_id = %s;"

            
            with self.db_obj.cursor(buffered=True) as db_cursor:
                try:
                    db_cursor.execute(books_update_stmnt, tuple(values_books))
                    db_cursor.execute("SELECT * FROM BOOK_DETAILS where book_id = %s", (values_gather_dict_books["book_id"][1],))
                    self.res_val_books = [db_cursor.fetchone()]
                except Exception as err_msg:
                    raise Exception ("SQL error... rolling back to last commit\n\n"+str(err_msg))
                else:
                    self.display_info_view_book_details.insert(parent="", index="end", values=self.res_val_books[0])
                    self.db_obj.commit()

        except Exception as err_msg:
            messagebox.showerror("Error", "Update operation failed\n\n"+str(err_msg), parent=self)
            self.db_obj.rollback()



    def books_delete_fun(self):
        
        """Delete Operation (BOOK_DETAILS Table)"""
        
        try:
            #clearing res variable data
            self.res_val_books = []
            #clear treeview
            self.display_info_view_book_details.delete(*self.display_info_view_book_details.get_children())
            
            #get values
            values_gather_dict_books = {"book_id" : (self.book_id_var_book.get(), self.txt_book_id_entry.get()), 
            "book_title" : (self.title_var_book.get(), self.txt_book_title_entry.get()), 
            "isbn" : (self.isbn_var_book.get(), self.txt_book_isbn_entry.get()), 
            "author" : (self.author_var_book.get(), self.txt_book_author_entry.get()), 
            "publisher" : (self.publisher_var_book.get(), self.txt_book_publisher_entry.get()), 
            "year" : (self.year_var_book.get(), self.txt_book_year_entry.get()), 
            "genre" : (self.genre_var_book.get(), self.txt_book_genre_entry.get()), 
            "borrow_status" : (self.borrow_status_var_book.get(), self.txt_book_borrow_status_entry.get()), 
            "book_condition" : (self.condition_var_book.get(), self.txt_book_condition_entry.get()), 
            "entry_made_or_alt_by": (1, self.user_name)}
            
            #Number of attributes selected
            if (sum(int(i[0]) for i in values_gather_dict_books.values()) < 2):
                raise Exception ("Atleast one attribute needs to be selected!!")

            #book_id validation
            if (values_gather_dict_books["book_id"][0]):
                if ((not values_gather_dict_books["book_id"][1]) or (str(values_gather_dict_books["book_id"][1]).isspace())):
                    raise Exception ("Invalid Book ID!!")
                        
            #year validation
            if (values_gather_dict_books["year"][0]):
                if ((not str(values_gather_dict_books["year"][1]).isnumeric())):
                    raise Exception ("Year should be numeric!!")
                if (int(values_gather_dict_books["year"][1]) == 0):
                    raise Exception ("'Year' entry cannot not be zero!!")
                if (int(values_gather_dict_books["year"][1]) > (date.today()).year):
                    raise Exception ("Invalid Year entry!!")
            
            columns_books = []
            values_books = []
            for col in values_gather_dict_books.keys():
                if (values_gather_dict_books[col][0]):
                    #appending to apt list
                    columns_books.append(col)
                    values_books.append(values_gather_dict_books[col][1])

            #statement
            books_delete_stmnt = "DELETE FROM BOOK_DETAILS where "+" = %s and ".join(columns_books)+" = %s;"
            
            with self.db_obj.cursor(buffered=True) as db_cursor:
                try:
                    db_cursor.execute(books_delete_stmnt, tuple(values_books))
                except Exception as err_msg:
                    raise Exception ("SQL error... rolling back to last commit\n\n"+str(err_msg))
                else:
                    messagebox.showinfo("Successful", "Successfully deleted record(s)", parent=self)
                    self.db_obj.commit()
        
        except Exception as err_msg:
            messagebox.showerror("Error", "Delete operation failed\n\n"+str(err_msg), parent=self)
            self.db_obj.rollback()



    def books_search_fun(self):
        
        """Search Operation (BOOK_DETAILS Table)"""
        
        try:
            #clearing res variable data
            self.res_val_books = []
            #clear treeview
            self.display_info_view_book_details.delete(*self.display_info_view_book_details.get_children())
            
            #get values
            values_gather_dict_books = {"book_id" : (self.book_id_var_book.get(), self.txt_book_id_entry.get()), 
            "book_title" : (self.title_var_book.get(), self.txt_book_title_entry.get()), 
            "isbn" : (self.isbn_var_book.get(), self.txt_book_isbn_entry.get()), 
            "author" : (self.author_var_book.get(), self.txt_book_author_entry.get()), 
            "publisher" : (self.publisher_var_book.get(), self.txt_book_publisher_entry.get()), 
            "year" : (self.year_var_book.get(), self.txt_book_year_entry.get()), 
            "genre" : (self.genre_var_book.get(), self.txt_book_genre_entry.get()), 
            "borrow_status" : (self.borrow_status_var_book.get(), self.txt_book_borrow_status_entry.get()), 
            "book_condition" : (self.condition_var_book.get(), self.txt_book_condition_entry.get()), 
            "entry_made_or_alt_by": (1, self.user_name)}
            
            #Number of attributes selected
            if (sum(int(i[0]) for i in values_gather_dict_books.values()) < 2):
                raise Exception ("Atleast one attribute needs to be selected!!")

            #book_id validation
            if (values_gather_dict_books["book_id"][0]):
                if ((not values_gather_dict_books["book_id"][1]) or (str(values_gather_dict_books["book_id"][1]).isspace())):
                    raise Exception ("Invalid Book ID!!")
                        
            #year validation
            if (values_gather_dict_books["year"][0]):
                if ((not str(values_gather_dict_books["year"][1]).isnumeric())):
                    raise Exception ("Year should be numeric!!")
                if (int(values_gather_dict_books["year"][1]) == 0):
                    raise Exception ("'Year' entry cannot not be zero!!")
                if (int(values_gather_dict_books["year"][1]) > (date.today()).year):
                    raise Exception ("Invalid Year entry!!")
            
            columns_books = []
            values_books = []
            for col in values_gather_dict_books.keys():
                if (values_gather_dict_books[col][0]):
                    #appending to apt list
                    columns_books.append(col)
                    values_books.append(values_gather_dict_books[col][1])

            #statement
            books_search_stmnt = "SELECT * FROM BOOK_DETAILS where "+" = %s and ".join(columns_books)+" = %s;"
            
            with self.db_obj.cursor(buffered=True) as db_cursor:
                try:
                    db_cursor.execute(books_search_stmnt, tuple(values_books))
                    self.res_val_books = db_cursor.fetchall()
                except Exception as err_msg:
                    raise Exception ("SQL error... rolling back to last commit\n\n"+str(err_msg))
                else:
                    if (not any(self.res_val_books)):
                        messagebox.showinfo("Search", "No data found!!", parent=self)
                    else:
                        for row in self.res_val_books:
                            self.display_info_view_book_details.insert(parent="", index="end", values=row)
                    self.db_obj.commit()

        except Exception as err_msg:
            messagebox.showerror("Error", "Search operation failed\n\n"+str(err_msg), parent=self)
            self.db_obj.rollback()



    def books_view_all_fun(self):
        
        """View all Operation (BOOK_DETAILS Table)"""
        
        try:
            #clearing res variable data
            self.res_val_books = []
            #clear treeview
            self.display_info_view_book_details.delete(*self.display_info_view_book_details.get_children())

            #statement
            books_view_all_stmnt = "SELECT * FROM BOOK_DETAILS;"
            
            with self.db_obj.cursor(buffered=True) as db_cursor:
                try:
                    db_cursor.execute(books_view_all_stmnt)
                    self.res_val_books = db_cursor.fetchall()
                except Exception as err_msg:
                    raise Exception ("SQL error... rolling back to last commit\n\n"+str(err_msg))
                else:
                    if (not any(self.res_val_books)):
                        messagebox.showinfo("View all", "No data found!!", parent=self)
                    else:
                        for row in self.res_val_books:
                            self.display_info_view_book_details.insert(parent="", index="end", values=row)
                    self.db_obj.commit()

        except Exception as err_msg:
            messagebox.showerror("Error", "View all operation failed\n\n"+str(err_msg), parent=self)
            self.db_obj.rollback()



    def books_frontend_widgets_clear_fun(self):
        
        """Front-end widgets clear Operation (BOOK_DETAILS Table)"""
        
        try:
            #clearing res variable data
            self.res_val_books = []

            #clear treeview
            self.display_info_view_book_details.delete(*self.display_info_view_book_details.get_children())
                
            #clear entry widgets
            self.txt_book_id_entry.delete(0, 'end')
            self.txt_book_title_entry.delete(0, 'end')
            self.txt_book_isbn_entry.delete(0, 'end')
            self.txt_book_author_entry.delete(0, 'end')
            self.txt_book_publisher_entry.delete(0, 'end')
            self.txt_book_year_entry.delete(0, 'end')
            self.txt_book_genre_entry.delete(0, 'end')
            self.txt_book_borrow_status_entry.delete(0, 'end')
            self.txt_book_condition_entry.delete(0, 'end')

            #checkbox widget (selected state)
            self.book_id_var_book.set(1)
            self.title_var_book.set(1)
            self.isbn_var_book.set(1)
            self.author_var_book.set(1)
            self.publisher_var_book.set(1)
            self.year_var_book.set(1)
            self.genre_var_book.set(1)
            self.borrow_status_var_book.set(1)
            self.condition_var_book.set(1)

        except Exception as err_msg:
            messagebox.showerror("Error", "Clear operation failed\n"+str(err_msg), parent=self)



    def books_export_to_csv_fun(self):
        
        """Export Operation (BOOK_DETAILS Table)"""
        
        try:
            #No data condition
            if (not self.res_val_books):
                raise Exception ("No data available!!")
            
            #File Dialog
            file_name = filedialog.asksaveasfilename(initialdir=os.getcwd(), title="Save CSV", filetypes=(("CSV files", "*.csv"), ("All files", "*.*")))
            if (not str(file_name[-4:]).lower()==".csv"):
                file_name += ".csv"

            #Write data to csv
            with open(file_name, "w", newline="") as export_file:
                csv_writer = csv.writer(export_file)
                csv_writer.writerow(self.display_info_view_book_details["columns"])
                csv_writer.writerows(self.res_val_books)
        
        except Exception as err_msg:
            messagebox.showerror("Error", "Export operation failed\n\n"+str(err_msg), parent=self)
        
        else:
            messagebox.showinfo("Successful", "Successfully exported data", parent=self)


    
    def select_row_treeview_books_fun(self, *args):

        """Select row Operation (BOOK_DETAILS Table)"""

        try:      
            #clear entry widgets
            self.txt_book_id_entry.delete(0, 'end')
            self.txt_book_title_entry.delete(0, 'end')
            self.txt_book_isbn_entry.delete(0, 'end')
            self.txt_book_author_entry.delete(0, 'end')
            self.txt_book_publisher_entry.delete(0, 'end')
            self.txt_book_year_entry.delete(0, 'end')
            self.txt_book_genre_entry.delete(0, 'end')
            self.txt_book_borrow_status_entry.delete(0, 'end')
            self.txt_book_condition_entry.delete(0, 'end')

            #adding data to entry widget
            values_books_row = self.display_info_view_book_details.item(self.display_info_view_book_details.focus(), "values")
            self.txt_book_id_entry.insert(0, values_books_row[0])
            self.txt_book_title_entry.insert(0, values_books_row[1])
            self.txt_book_isbn_entry.insert(0, values_books_row[2])
            self.txt_book_author_entry.insert(0, values_books_row[3])
            self.txt_book_publisher_entry.insert(0, values_books_row[4])
            self.txt_book_year_entry.insert(0, values_books_row[5])
            self.txt_book_genre_entry.insert(0, values_books_row[6])
            self.txt_book_borrow_status_entry.insert(0, values_books_row[7])
            self.txt_book_condition_entry.insert(0, values_books_row[8])
            
            #checkbox widget (selected state)
            self.book_id_var_book.set(1)
            self.title_var_book.set(1)
            self.isbn_var_book.set(1)
            self.author_var_book.set(1)
            self.publisher_var_book.set(1)
            self.year_var_book.set(1)
            self.genre_var_book.set(1)
            self.borrow_status_var_book.set(1)
            self.condition_var_book.set(1)

        except Exception as err_msg:
            messagebox.showerror("Error", "Unable to select\n"+str(err_msg), parent=self)





    def member_details_tab_fun(self):
        
        """MEMBER_DETAILS TABLE frames and widgets"""

        try:
            #flag
            self.member_details_frames_run_flag = 1

            #initial frames
            self.db_gui_frame_4 = tk.Frame(self, bg="White")
            self.db_gui_frame_4.place(x=int(self.winfo_width()*0.05), y=int(self.winfo_height()*0.05), width=int(self.winfo_width()*0.9), height=int(self.winfo_height()*0.35))

            self.db_gui_frame_5 = tk.Frame(self, bg="White")
            self.db_gui_frame_5.place(x=int(self.winfo_width()*0.05), y=int(self.winfo_height()*0.45), width=int(self.winfo_width()*0.9), height=int(self.winfo_height()*0.50))
            
            
            #Attributes
            self.member_id_var_member = tk.IntVar(value=1)
            member_id_checkbox_member = tk.Checkbutton(self.db_gui_frame_4, text="", variable=self.member_id_var_member)
            member_id_checkbox_member.place(x=int(self.winfo_width()*0.02), y=int(self.winfo_height()*0.04))

            member_id_label_member = tk.Label(self.db_gui_frame_4, text="Member ID: ", font=("Cambria", 15), bg="White", fg="Black")
            member_id_label_member.place(x=int(self.winfo_width()*0.04), y=int(self.winfo_height()*0.04))

            self.txt_member_id_entry = tk.Entry(self.db_gui_frame_4, font=("Times New Roman", 15), bg="lightgrey", width=int(self.winfo_width()*0.016))
            self.txt_member_id_entry.place(x=int(self.winfo_width()*0.14), y=int(self.winfo_height()*0.04))      

            
            self.name_var_member = tk.IntVar(value=1)
            name_checkbox_member = tk.Checkbutton(self.db_gui_frame_4, text="", variable=self.name_var_member)
            name_checkbox_member.place(x=int(self.winfo_width()*0.02), y=int(self.winfo_height()*0.11))

            name_label_member = tk.Label(self.db_gui_frame_4, text="Name: ", font=("Cambria", 15), bg="White", fg="Black")
            name_label_member.place(x=int(self.winfo_width()*0.04), y=int(self.winfo_height()*0.11))

            self.txt_member_name_entry = tk.Entry(self.db_gui_frame_4, font=("Times New Roman", 15), bg="lightgrey", width=int(self.winfo_width()*0.016))
            self.txt_member_name_entry.place(x=int(self.winfo_width()*0.14), y=int(self.winfo_height()*0.11))


            self.gender_var_member = tk.IntVar(value=1)
            gender_checkbox_member = tk.Checkbutton(self.db_gui_frame_4, text="", variable=self.gender_var_member)
            gender_checkbox_member.place(x=int(self.winfo_width()*0.02), y=int(self.winfo_height()*0.18))

            gender_label_member = tk.Label(self.db_gui_frame_4, text="Gender: ", font=("Cambria", 15), bg="White", fg="Black")
            gender_label_member.place(x=int(self.winfo_width()*0.04), y=int(self.winfo_height()*0.18))

            self.txt_member_gender_entry = tk.Entry(self.db_gui_frame_4, font=("Times New Roman", 15), bg="lightgrey", width=int(self.winfo_width()*0.016))
            self.txt_member_gender_entry.place(x=int(self.winfo_width()*0.14), y=int(self.winfo_height()*0.18))


            self.dob_var_member = tk.IntVar(value=1)
            dob_checkbox_member = tk.Checkbutton(self.db_gui_frame_4, text="", variable=self.dob_var_member)
            dob_checkbox_member.place(x=int(self.winfo_width()*0.31), y=int(self.winfo_height()*0.04))

            dob_label_member = tk.Label(self.db_gui_frame_4, text="D.O.B: ", font=("Cambria", 15), bg="White", fg="Black")
            dob_label_member.place(x=int(self.winfo_width()*0.33), y=int(self.winfo_height()*0.04))

            self.txt_member_dob_entry = tk.Entry(self.db_gui_frame_4, font=("Times New Roman", 15), bg="lightgrey", width=int(self.winfo_width()*0.016))
            self.txt_member_dob_entry.place(x=int(self.winfo_width()*0.43), y=int(self.winfo_height()*0.04))

            
            self.email_id_var_member = tk.IntVar(value=1)
            email_id_checkbox_member = tk.Checkbutton(self.db_gui_frame_4, text="", variable=self.email_id_var_member)
            email_id_checkbox_member.place(x=int(self.winfo_width()*0.31), y=int(self.winfo_height()*0.11))

            email_id_label_member = tk.Label(self.db_gui_frame_4, text="Email ID: ", font=("Cambria", 15), bg="White", fg="Black")
            email_id_label_member.place(x=int(self.winfo_width()*0.33), y=int(self.winfo_height()*0.11))

            self.txt_member_email_id_entry = tk.Entry(self.db_gui_frame_4, font=("Times New Roman", 15), bg="lightgrey", width=int(self.winfo_width()*0.016))
            self.txt_member_email_id_entry.place(x=int(self.winfo_width()*0.43), y=int(self.winfo_height()*0.11))

            
            self.phone_no_var_member = tk.IntVar(value=1)
            phone_no_checkbox_member = tk.Checkbutton(self.db_gui_frame_4, text="", variable=self.phone_no_var_member)
            phone_no_checkbox_member.place(x=int(self.winfo_width()*0.31), y=int(self.winfo_height()*0.18))

            phone_no_label_member = tk.Label(self.db_gui_frame_4, text="Phone No.: ", font=("Cambria", 15), bg="White", fg="Black")
            phone_no_label_member.place(x=int(self.winfo_width()*0.33), y=int(self.winfo_height()*0.18))

            self.txt_member_phone_no_entry = tk.Entry(self.db_gui_frame_4, font=("Times New Roman", 15), bg="lightgrey", width=int(self.winfo_width()*0.016))
            self.txt_member_phone_no_entry.place(x=int(self.winfo_width()*0.43), y=int(self.winfo_height()*0.18))


            self.address_var_member = tk.IntVar(value=1)
            address_checkbox_member = tk.Checkbutton(self.db_gui_frame_4, text="", variable=self.address_var_member)
            address_checkbox_member.place(x=int(self.winfo_width()*0.60), y=int(self.winfo_height()*0.04))

            address_label_member = tk.Label(self.db_gui_frame_4, text="Address: ", font=("Cambria", 15), bg="White", fg="Black")
            address_label_member.place(x=int(self.winfo_width()*0.62), y=int(self.winfo_height()*0.04))

            self.txt_member_address_entry = tk.Entry(self.db_gui_frame_4, font=("Times New Roman", 15), bg="lightgrey", width=int(self.winfo_width()*0.016))
            self.txt_member_address_entry.place(x=int(self.winfo_width()*0.72), y=int(self.winfo_height()*0.04))


            self.occupation_var_member = tk.IntVar(value=1)
            occupation_checkbox_member = tk.Checkbutton(self.db_gui_frame_4, text="", variable=self.occupation_var_member)
            occupation_checkbox_member.place(x=int(self.winfo_width()*0.60), y=int(self.winfo_height()*0.11))

            occupation_label_member = tk.Label(self.db_gui_frame_4, text="Occupation: ", font=("Cambria", 15), bg="White", fg="Black")
            occupation_label_member.place(x=int(self.winfo_width()*0.62), y=int(self.winfo_height()*0.11))

            self.txt_member_occupation_entry = tk.Entry(self.db_gui_frame_4, font=("Times New Roman", 15), bg="lightgrey", width=int(self.winfo_width()*0.016))
            self.txt_member_occupation_entry.place(x=int(self.winfo_width()*0.72), y=int(self.winfo_height()*0.11))


            self.membership_type_var_member = tk.IntVar(value=1)
            membership_type_checkbox_member = tk.Checkbutton(self.db_gui_frame_4, text="", variable=self.membership_type_var_member)
            membership_type_checkbox_member.place(x=int(self.winfo_width()*0.60), y=int(self.winfo_height()*0.18))

            membership_type_label_member = tk.Label(self.db_gui_frame_4, text="Membership: ", font=("Cambria", 15), bg="White", fg="Black")
            membership_type_label_member.place(x=int(self.winfo_width()*0.62), y=int(self.winfo_height()*0.18))

            self.txt_membership_type_entry = tk.Entry(self.db_gui_frame_4, font=("Times New Roman", 15), bg="lightgrey", width=int(self.winfo_width()*0.016))
            self.txt_membership_type_entry.place(x=int(self.winfo_width()*0.72), y=int(self.winfo_height()*0.18))
            

            #buttons
            back_btn = tk.Button(self.db_gui_frame_4, text=chr(8630)+" Back", command=self.clear_member_details_frames_for_tab_sel_fun, cursor="hand2", fg="Black", bg="Crimson", font=("Calibri", 15, "bold"), activebackground="#a30f2d", activeforeground="White", width=int(self.winfo_width()*0.008), height=int(self.winfo_height()*0.002))
            back_btn.place(x=int(self.winfo_width()*0.06), y=int(self.winfo_height()*0.26))

            insert_btn = tk.Button(self.db_gui_frame_4, text="Insert", command=self.members_insert_fun, cursor="hand2", fg="Black", bg="Crimson", font=("Calibri", 15, "bold"), activebackground="#a30f2d", activeforeground="White", width=int(self.winfo_width()*0.008), height=int(self.winfo_height()*0.002))
            insert_btn.place(x=int(self.winfo_width()*0.16), y=int(self.winfo_height()*0.26))

            update_btn = tk.Button(self.db_gui_frame_4, text="Update", command=self.members_update_fun, cursor="hand2", fg="Black", bg="Crimson", font=("Calibri", 15, "bold"), activebackground="#a30f2d", activeforeground="White", width=int(self.winfo_width()*0.008), height=int(self.winfo_height()*0.002))
            update_btn.place(x=int(self.winfo_width()*0.26), y=int(self.winfo_height()*0.26))

            delete_btn = tk.Button(self.db_gui_frame_4, text="Delete", command=self.members_delete_fun, cursor="hand2", fg="Black", bg="Crimson", font=("Calibri", 15, "bold"), activebackground="#a30f2d", activeforeground="White", width=int(self.winfo_width()*0.008), height=int(self.winfo_height()*0.002))
            delete_btn.place(x=int(self.winfo_width()*0.36), y=int(self.winfo_height()*0.26))

            search_btn = tk.Button(self.db_gui_frame_4, text="Search", command=self.members_search_fun, cursor="hand2", fg="Black", bg="Crimson", font=("Calibri", 15, "bold"), activebackground="#a30f2d", activeforeground="White", width=int(self.winfo_width()*0.008), height=int(self.winfo_height()*0.002))
            search_btn.place(x=int(self.winfo_width()*0.46), y=int(self.winfo_height()*0.26))

            view_all_btn = tk.Button(self.db_gui_frame_4, text="View all", command=self.members_view_all_fun, cursor="hand2", fg="Black", bg="Crimson", font=("Calibri", 15, "bold"), activebackground="#a30f2d", activeforeground="White", width=int(self.winfo_width()*0.008), height=int(self.winfo_height()*0.002))
            view_all_btn.place(x=int(self.winfo_width()*0.56), y=int(self.winfo_height()*0.26))

            insert_btn = tk.Button(self.db_gui_frame_4, text="Clear", command=self.members_frontend_widgets_clear_fun, cursor="hand2", fg="Black", bg="Crimson", font=("Calibri", 15, "bold"), activebackground="#a30f2d", activeforeground="White", width=int(self.winfo_width()*0.008), height=int(self.winfo_height()*0.002))
            insert_btn.place(x=int(self.winfo_width()*0.66), y=int(self.winfo_height()*0.26))

            export_to_csv_btn = tk.Button(self.db_gui_frame_4, text="Export", command=self.members_export_to_csv_fun, cursor="hand2", fg="Black", bg="Crimson", font=("Calibri", 15, "bold"), activebackground="#a30f2d", activeforeground="White", width=int(self.winfo_width()*0.008), height=int(self.winfo_height()*0.002))
            export_to_csv_btn.place(x=int(self.winfo_width()*0.76), y=int(self.winfo_height()*0.26))

            #Data view widget
            self.display_info_view_member_details = ttk.Treeview(self.db_gui_frame_5, selectmode ="browse")
            self.display_info_view_member_details["columns"] = ("Member ID", "Name", "Gender", "D.O.B", "Email ID", "Phone No.", "Address", "Occupation", "Membership Type", "Data entered by", "Timestamp")

            #treeview style
            """Currently set to common style as defined in construtor"""

            self.display_info_view_member_details.column("#0", width=0, stretch="NO")
            for label in list(self.display_info_view_member_details["columns"]):
                self.display_info_view_member_details.column(label, anchor=tk.CENTER, minwidth=int(self.winfo_width()*0.04))
                self.display_info_view_member_details.heading(label, text=label, anchor=tk.CENTER)
            
            self.display_info_view_member_details.place(x=int(self.winfo_width()*0), y=int(self.winfo_height()*0), width=int(self.winfo_width()*0.90), height=int(self.winfo_height()*0.50))
            self.display_info_view_member_details.bind("<ButtonRelease-1>", self.select_row_treeview_members_fun)

            #Scrollbars
            verscrlbar_display_info_view_member_details = ttk.Scrollbar(self.display_info_view_member_details, orient ="vertical", command = self.display_info_view_member_details.yview)
            verscrlbar_display_info_view_member_details.pack(side ='right', fill ='y')
            self.display_info_view_member_details.configure(yscrollcommand = verscrlbar_display_info_view_member_details.set)

            horscrlbar_display_info_view_member_details = ttk.Scrollbar(self.display_info_view_member_details, orient ="horizontal", command = self.display_info_view_member_details.xview)
            horscrlbar_display_info_view_member_details.pack(side ='bottom', fill ='x')
            self.display_info_view_member_details.configure(xscrollcommand = horscrlbar_display_info_view_member_details.set)

        except Exception as err_msg:
            messagebox.showerror("Error", "Frames and widgets error...\n\n"+str(err_msg), parent=self)



    def clear_member_details_frames_for_tab_sel_fun(self):
        
        """Removes frames and calls table_sel_fun() (for MEMBER_DETAILS)"""

        try:
            if (messagebox.askyesno("Return back", "Do you wish to run 'Clear' operation before leaving?\n\nRecommended action: Press 'Yes' for efficient memory usage")):
                #clear treeview
                self.display_info_view_member_details.delete(*self.display_info_view_member_details.get_children())

                #clear entry widgets
                self.txt_member_id_entry.delete(0, 'end')
                self.txt_member_name_entry.delete(0, 'end')
                self.txt_member_gender_entry.delete(0, 'end')
                self.txt_member_dob_entry.delete(0, 'end')
                self.txt_member_email_id_entry.delete(0, 'end')
                self.txt_member_phone_no_entry.delete(0, 'end')
                self.txt_member_address_entry.delete(0, 'end')
                self.txt_member_occupation_entry.delete(0, 'end')
                self.txt_membership_type_entry.delete(0, 'end')

                #checkbox widget (selected state)
                self.member_id_var_member.set(1)
                self.name_var_member.set(1)
                self.gender_var_member.set(1)
                self.dob_var_member.set(1)
                self.email_id_var_member.set(1)
                self.phone_no_var_member.set(1)
                self.address_var_member.set(1)
                self.occupation_var_member.set(1)
                self.membership_type_var_member.set(1)

                #clearing res variable data
                self.res_val_members = []
                
            self.db_gui_frame_4.place_forget()
            self.db_gui_frame_5.place_forget()
            self.db_gui_frame_1.place(x=int(self.winfo_width()*0.3), y=int(self.winfo_height()*0.3), width=int(self.winfo_width()*0.4), height=int(self.winfo_height()*0.4))

        except Exception as err_msg:
            messagebox.showerror("Error", "Error while returning...\n\n"+str(err_msg), parent=self)



    def members_insert_fun(self):

        """Insert Operation (MEMBER_DETAILS Table)"""

        try:
            #clearing res variable data
            self.res_val_members = []
            #clear treeview
            self.display_info_view_member_details.delete(*self.display_info_view_member_details.get_children())
            
            #get values
            values_gather_dict_members = {"member_id" : (self.member_id_var_member.get(), self.txt_member_id_entry.get()), 
            "member_name" : (self.name_var_member.get(), self.txt_member_name_entry.get()), 
            "gender" : (self.gender_var_member.get(), self.txt_member_gender_entry.get()), 
            "dob" : (self.dob_var_member.get(), self.txt_member_dob_entry.get()), 
            "email" : (self.email_id_var_member.get(), self.txt_member_email_id_entry.get()), 
            "phone_no" : (self.phone_no_var_member.get(), self.txt_member_phone_no_entry.get()), 
            "address" : (self.address_var_member.get(), self.txt_member_address_entry.get()), 
            "occupation" : (self.occupation_var_member.get(), self.txt_member_occupation_entry.get()), 
            "membership" : (self.membership_type_var_member.get(), self.txt_membership_type_entry.get()), 
            "entry_made_or_alt_by": (1, self.user_name)}
                        
            #member_id validation
            if (values_gather_dict_members["member_id"][0]):
                if ((not values_gather_dict_members["member_id"][1]) or (str(values_gather_dict_members["member_id"][1]).isspace())):
                    raise Exception ("Invalid Member ID!!")
            else:
                raise Exception ("Member ID is a mandatory field (chechkbox should be in on state)!!")

            #basic email validation
            regex_email = "^[A-Za-z0-9!#$%&'*+-/=?^_`{|}~]+[A-Za-z0-9!#$%&'*+-/=?^_`{|}~.]*[A-Za-z0-9!#$%&'*+-/=?^_`{|}~]+[@][A-Za-z0-9]+[A-Za-z0-9-]*[A-Za-z0-9]+[.][A-Za-z.]*[A-Za-z]+"
            if (values_gather_dict_members["email"][0]):
                if (not re.fullmatch(regex_email, values_gather_dict_members["email"][1])):
                    raise Exception ("Invalid email address!!")
            
            #basic dob validation
            regex_date = "^[0-9]?[0-9]?[0-9]?[0-9][-][0-1]?[0-9][-][0-3]?[0-9]"
            if (values_gather_dict_members["dob"][0]):
                if (not re.fullmatch(regex_date, values_gather_dict_members["dob"][1])):
                    raise Exception ("Invalid D.O.B!! (format: YYYY-MM-DD)")

            columns_members = []
            values_members = []
            for col in values_gather_dict_members.keys():
                #appending to apt list
                columns_members.append(col)
                if ((col=="dob") and (not values_gather_dict_members["dob"][0])):
                    values_members.append("0000-00-00")
                else:
                    values_members.append(values_gather_dict_members[col][1]*values_gather_dict_members[col][0])


            #statement
            members_insert_stmnt = "INSERT INTO MEMBER_DETAILS ("+", ".join(columns_members)+") values ("+("%s, "*len(columns_members))[:-2]+");"
            
            with self.db_obj.cursor(buffered=True) as db_cursor:
                try:
                    db_cursor.execute(members_insert_stmnt, tuple(values_members))
                    db_cursor.execute("SELECT * FROM MEMBER_DETAILS where member_id = %s", (values_gather_dict_members["member_id"][1],))
                    self.res_val_members = [db_cursor.fetchone()]
                except Exception as err_msg:
                    raise Exception ("SQL error... rolling back to last commit\n\n"+str(err_msg))
                else:
                    self.display_info_view_member_details.insert(parent="", index="end", values=self.res_val_members[0])
                    self.db_obj.commit()
        
        except Exception as err_msg:
            messagebox.showerror("Error", "Insert operation failed\n\n"+str(err_msg), parent=self)
            self.db_obj.rollback()



    def members_update_fun(self):

        """Update Operation (MEMBER_DETAILS Table)"""

        try:
            #clearing res variable data
            self.res_val_members = []
            #clear treeview
            self.display_info_view_member_details.delete(*self.display_info_view_member_details.get_children())
            
            #get values
            values_gather_dict_members = {"member_id" : (self.member_id_var_member.get(), self.txt_member_id_entry.get()), 
            "member_name" : (self.name_var_member.get(), self.txt_member_name_entry.get()), 
            "gender" : (self.gender_var_member.get(), self.txt_member_gender_entry.get()), 
            "dob" : (self.dob_var_member.get(), self.txt_member_dob_entry.get()), 
            "email" : (self.email_id_var_member.get(), self.txt_member_email_id_entry.get()), 
            "phone_no" : (self.phone_no_var_member.get(), self.txt_member_phone_no_entry.get()), 
            "address" : (self.address_var_member.get(), self.txt_member_address_entry.get()), 
            "occupation" : (self.occupation_var_member.get(), self.txt_member_occupation_entry.get()), 
            "membership" : (self.membership_type_var_member.get(), self.txt_membership_type_entry.get()), 
            "entry_made_or_alt_by": (1, self.user_name)}
                        
            #member_id validation
            if (values_gather_dict_members["member_id"][0]):
                if ((not values_gather_dict_members["member_id"][1]) or (str(values_gather_dict_members["member_id"][1]).isspace())):
                    raise Exception ("Invalid Member ID!!")
            else:
                raise Exception ("Member ID is a mandatory field (chechkbox should be in on state)!!")
            
            #Number of attributes selected
            if (sum(int(i[0]) for i in values_gather_dict_members.values()) < 3):
                raise Exception ("Atleast one attribute needs to be selected other than Member ID!!")

            #basic email validation
            regex_email = "^[A-Za-z0-9!#$%&'*+-/=?^_`{|}~]+[A-Za-z0-9!#$%&'*+-/=?^_`{|}~.]*[A-Za-z0-9!#$%&'*+-/=?^_`{|}~]+[@][A-Za-z0-9]+[A-Za-z0-9-]*[A-Za-z0-9]+[.][A-Za-z.]*[A-Za-z]+"
            if (values_gather_dict_members["email"][0]):
                if (not re.fullmatch(regex_email, values_gather_dict_members["email"][1])):
                    raise Exception ("Invalid email address!!")

            #basic dob validation
            regex_date = "^[0-9]?[0-9]?[0-9]?[0-9][-][0-1]?[0-9][-][0-3]?[0-9]"
            if (values_gather_dict_members["dob"][0]):
                if (not re.fullmatch(regex_date, values_gather_dict_members["dob"][1])):
                    raise Exception ("Invalid D.O.B!! (format: YYYY-MM-DD)")
            

            columns_members = []
            values_members = []
            for col in values_gather_dict_members.keys():
                if ((values_gather_dict_members[col][0]) and (col != "member_id")):
                    #appending to apt list
                    columns_members.append(col)
                    values_members.append(values_gather_dict_members[col][1])
                        
            #appending member_id
            values_members.append(values_gather_dict_members["member_id"][1])

            #statement
            members_update_stmnt = "UPDATE MEMBER_DETAILS SET "+" = %s, ".join(columns_members)+" = %s where member_id = %s;"

            
            with self.db_obj.cursor(buffered=True) as db_cursor:
                try:
                    db_cursor.execute(members_update_stmnt, tuple(values_members))
                    db_cursor.execute("SELECT * FROM MEMBER_DETAILS where member_id = %s", (values_gather_dict_members["member_id"][1],))
                    self.res_val_members = [db_cursor.fetchone()]
                except Exception as err_msg:
                    raise Exception ("SQL error... rolling back to last commit\n\n"+str(err_msg))
                else:
                    self.display_info_view_member_details.insert(parent="", index="end", values=self.res_val_members[0])
                    self.db_obj.commit()

        except Exception as err_msg:
            messagebox.showerror("Error", "Update operation failed\n\n"+str(err_msg), parent=self)
            self.db_obj.rollback()



    def members_delete_fun(self):

        """Delete Operation (MEMBER_DETAILS Table)"""

        try:
            #clearing res variable data
            self.res_val_members = []
            #clear treeview
            self.display_info_view_member_details.delete(*self.display_info_view_member_details.get_children())
            
            #get values
            values_gather_dict_members = {"member_id" : (self.member_id_var_member.get(), self.txt_member_id_entry.get()), 
            "member_name" : (self.name_var_member.get(), self.txt_member_name_entry.get()), 
            "gender" : (self.gender_var_member.get(), self.txt_member_gender_entry.get()), 
            "dob" : (self.dob_var_member.get(), self.txt_member_dob_entry.get()), 
            "email" : (self.email_id_var_member.get(), self.txt_member_email_id_entry.get()), 
            "phone_no" : (self.phone_no_var_member.get(), self.txt_member_phone_no_entry.get()), 
            "address" : (self.address_var_member.get(), self.txt_member_address_entry.get()), 
            "occupation" : (self.occupation_var_member.get(), self.txt_member_occupation_entry.get()), 
            "membership" : (self.membership_type_var_member.get(), self.txt_membership_type_entry.get()), 
            "entry_made_or_alt_by": (1, self.user_name)}
                        
            #Number of attributes selected
            if (sum(int(i[0]) for i in values_gather_dict_members.values()) < 2):
                raise Exception ("Atleast one attribute needs to be selected!!")
            
            #member_id validation
            if (values_gather_dict_members["member_id"][0]):
                if ((not values_gather_dict_members["member_id"][1]) or (str(values_gather_dict_members["member_id"][1]).isspace())):
                    raise Exception ("Invalid Member ID!!")
                        
            #basic email validation
            regex_email = "^[A-Za-z0-9!#$%&'*+-/=?^_`{|}~]+[A-Za-z0-9!#$%&'*+-/=?^_`{|}~.]*[A-Za-z0-9!#$%&'*+-/=?^_`{|}~]+[@][A-Za-z0-9]+[A-Za-z0-9-]*[A-Za-z0-9]+[.][A-Za-z.]*[A-Za-z]+"
            if (values_gather_dict_members["email"][0]):
                if (not re.fullmatch(regex_email, values_gather_dict_members["email"][1])):
                    raise Exception ("Invalid email address!!")
            
            #basic dob validation
            regex_date = "^[0-9]?[0-9]?[0-9]?[0-9][-][0-1]?[0-9][-][0-3]?[0-9]"
            if (values_gather_dict_members["dob"][0]):
                if (not re.fullmatch(regex_date, values_gather_dict_members["dob"][1])):
                    raise Exception ("Invalid D.O.B!! (format: YYYY-MM-DD)")
            
            columns_members = []
            values_members = []
            for col in values_gather_dict_members.keys():
                if (values_gather_dict_members[col][0]):
                    #appending to apt list
                    columns_members.append(col)
                    values_members.append(values_gather_dict_members[col][1])

            #statement
            members_delete_stmnt = "DELETE FROM MEMBER_DETAILS where "+" = %s and ".join(columns_members)+" = %s;"
            
            with self.db_obj.cursor(buffered=True) as db_cursor:
                try:
                    db_cursor.execute(members_delete_stmnt, tuple(values_members))
                except Exception as err_msg:
                    raise Exception ("SQL error... rolling back to last commit\n\n"+str(err_msg))
                else:
                    messagebox.showinfo("Successful", "Successfully deleted record(s)", parent=self)
                    self.db_obj.commit()
        
        except Exception as err_msg:
            messagebox.showerror("Error", "Delete operation failed\n\n"+str(err_msg), parent=self)
            self.db_obj.rollback()


    def members_search_fun(self):

        """Search Operation (MEMBER_DETAILS Table)"""
        
        try:
            #clearing res variable data
            self.res_val_members = []
            #clear treeview
            self.display_info_view_member_details.delete(*self.display_info_view_member_details.get_children())
            
            #get values
            values_gather_dict_members = {"member_id" : (self.member_id_var_member.get(), self.txt_member_id_entry.get()), 
            "member_name" : (self.name_var_member.get(), self.txt_member_name_entry.get()), 
            "gender" : (self.gender_var_member.get(), self.txt_member_gender_entry.get()), 
            "dob" : (self.dob_var_member.get(), self.txt_member_dob_entry.get()), 
            "email" : (self.email_id_var_member.get(), self.txt_member_email_id_entry.get()), 
            "phone_no" : (self.phone_no_var_member.get(), self.txt_member_phone_no_entry.get()), 
            "address" : (self.address_var_member.get(), self.txt_member_address_entry.get()), 
            "occupation" : (self.occupation_var_member.get(), self.txt_member_occupation_entry.get()), 
            "membership" : (self.membership_type_var_member.get(), self.txt_membership_type_entry.get()), 
            "entry_made_or_alt_by": (1, self.user_name)}
                        
            #Number of attributes selected
            if (sum(int(i[0]) for i in values_gather_dict_members.values()) < 2):
                raise Exception ("Atleast one attribute needs to be selected!!")
            
            #member_id validation
            if (values_gather_dict_members["member_id"][0]):
                if ((not values_gather_dict_members["member_id"][1]) or (str(values_gather_dict_members["member_id"][1]).isspace())):
                    raise Exception ("Invalid Member ID!!")
                        
            #basic email validation
            regex_email = "^[A-Za-z0-9!#$%&'*+-/=?^_`{|}~]+[A-Za-z0-9!#$%&'*+-/=?^_`{|}~.]*[A-Za-z0-9!#$%&'*+-/=?^_`{|}~]+[@][A-Za-z0-9]+[A-Za-z0-9-]*[A-Za-z0-9]+[.][A-Za-z.]*[A-Za-z]+"
            if (values_gather_dict_members["email"][0]):
                if (not re.fullmatch(regex_email, values_gather_dict_members["email"][1])):
                    raise Exception ("Invalid email address!!")

            #basic dob validation
            regex_date = "^[0-9]?[0-9]?[0-9]?[0-9][-][0-1]?[0-9][-][0-3]?[0-9]"
            if (values_gather_dict_members["dob"][0]):
                if (not re.fullmatch(regex_date, values_gather_dict_members["dob"][1])):
                    raise Exception ("Invalid D.O.B!! (format: YYYY-MM-DD)")
            
            columns_members = []
            values_members = []
            for col in values_gather_dict_members.keys():
                if (values_gather_dict_members[col][0]):
                    #appending to apt list
                    columns_members.append(col)
                    values_members.append(values_gather_dict_members[col][1])

            #statement
            members_search_stmnt = "SELECT * FROM MEMBER_DETAILS where "+" = %s and ".join(columns_members)+" = %s;"
            
            with self.db_obj.cursor(buffered=True) as db_cursor:
                try:
                    db_cursor.execute(members_search_stmnt, tuple(values_members))
                    self.res_val_members = db_cursor.fetchall()
                except Exception as err_msg:
                    raise Exception ("SQL error... rolling back to last commit\n\n"+str(err_msg))
                else:
                    if (not any(self.res_val_members)):
                        messagebox.showinfo("Search", "No data found!!", parent=self)
                    else:
                        for row in self.res_val_members:
                            self.display_info_view_member_details.insert(parent="", index="end", values=row)
                    self.db_obj.commit()

        except Exception as err_msg:
            messagebox.showerror("Error", "Search operation failed\n\n"+str(err_msg), parent=self)
            self.db_obj.rollback()


    def members_view_all_fun(self):

        """View all Operation (MEMBER_DETAILS Table)"""
        
        try:
            #clearing res variable data
            self.res_val_members = []
            #clear treeview
            self.display_info_view_member_details.delete(*self.display_info_view_member_details.get_children())

            #statement
            members_view_all_stmnt = "SELECT * FROM MEMBER_DETAILS;"
            
            with self.db_obj.cursor(buffered=True) as db_cursor:
                try:
                    db_cursor.execute(members_view_all_stmnt)
                    self.res_val_members = db_cursor.fetchall()
                except Exception as err_msg:
                    raise Exception ("SQL error... rolling back to last commit\n\n"+str(err_msg))
                else:
                    if (not any(self.res_val_members)):
                        messagebox.showinfo("View all", "No data found!!", parent=self)
                    else:
                        for row in self.res_val_members:
                            self.display_info_view_member_details.insert(parent="", index="end", values=row)
                    self.db_obj.commit()

        except Exception as err_msg:
            messagebox.showerror("Error", "View all operation failed\n\n"+str(err_msg), parent=self)
            self.db_obj.rollback()


    def members_frontend_widgets_clear_fun(self):

        """Front-end widgets clear Operation (MEMBER_DETAILS Table)"""

        try:
            #clearing res variable data
            self.res_val_members = []
            
            #clear treeview
            self.display_info_view_member_details.delete(*self.display_info_view_member_details.get_children())

            #clear entry widgets
            self.txt_member_id_entry.delete(0, 'end')
            self.txt_member_name_entry.delete(0, 'end')
            self.txt_member_gender_entry.delete(0, 'end')
            self.txt_member_dob_entry.delete(0, 'end')
            self.txt_member_email_id_entry.delete(0, 'end')
            self.txt_member_phone_no_entry.delete(0, 'end')
            self.txt_member_address_entry.delete(0, 'end')
            self.txt_member_occupation_entry.delete(0, 'end')
            self.txt_membership_type_entry.delete(0, 'end')

            #checkbox widget (selected state)
            self.member_id_var_member.set(1)
            self.name_var_member.set(1)
            self.gender_var_member.set(1)
            self.dob_var_member.set(1)
            self.email_id_var_member.set(1)
            self.phone_no_var_member.set(1)
            self.address_var_member.set(1)
            self.occupation_var_member.set(1)
            self.membership_type_var_member.set(1)

        except Exception as err_msg:
            messagebox.showerror("Error", "Clear operation failed\n"+str(err_msg), parent=self)



    def members_export_to_csv_fun(self):

        """Export Operation (MEMBER_DETAILS Table)"""
        
        try:
            #No data condition
            if (not self.res_val_members):
                raise Exception ("No data available!!")
            
            #File Dialog
            file_name = filedialog.asksaveasfilename(initialdir=os.getcwd(), title="Save CSV", filetypes=(("CSV files", "*.csv"), ("All files", "*.*")))
            if (not str(file_name[-4:]).lower()==".csv"):
                file_name += ".csv"

            #Write data to csv
            with open(file_name, "w", newline="") as export_file:
                csv_writer = csv.writer(export_file)
                csv_writer.writerow(self.display_info_view_member_details["columns"])
                csv_writer.writerows(self.res_val_members)
        
        except Exception as err_msg:
            messagebox.showerror("Error", "Export operation failed\n\n"+str(err_msg), parent=self)
        
        else:
            messagebox.showinfo("Successful", "Successfully exported data", parent=self)



    def select_row_treeview_members_fun(self, *args):

        """Select row Operation (MEMBER_DETAILS Table)"""

        try:
            #clear entry widgets
            self.txt_member_id_entry.delete(0, 'end')
            self.txt_member_name_entry.delete(0, 'end')
            self.txt_member_gender_entry.delete(0, 'end')
            self.txt_member_dob_entry.delete(0, 'end')
            self.txt_member_email_id_entry.delete(0, 'end')
            self.txt_member_phone_no_entry.delete(0, 'end')
            self.txt_member_address_entry.delete(0, 'end')
            self.txt_member_occupation_entry.delete(0, 'end')
            self.txt_membership_type_entry.delete(0, 'end')

            #adding data to entry widget
            values_members_row = self.display_info_view_member_details.item(self.display_info_view_member_details.focus(), "values")
            self.txt_member_id_entry.insert(0, values_members_row[0])
            self.txt_member_name_entry.insert(0, values_members_row[1])
            self.txt_member_gender_entry.insert(0, values_members_row[2])
            self.txt_member_dob_entry.insert(0, values_members_row[3])
            self.txt_member_email_id_entry.insert(0, values_members_row[4])
            self.txt_member_phone_no_entry.insert(0, values_members_row[5])
            self.txt_member_address_entry.insert(0, values_members_row[6])
            self.txt_member_occupation_entry.insert(0, values_members_row[7])
            self.txt_membership_type_entry.insert(0, values_members_row[8])

            #checkbox widget (selected state)
            self.member_id_var_member.set(1)
            self.name_var_member.set(1)
            self.gender_var_member.set(1)
            self.dob_var_member.set(1)
            self.email_id_var_member.set(1)
            self.phone_no_var_member.set(1)
            self.address_var_member.set(1)
            self.occupation_var_member.set(1)
            self.membership_type_var_member.set(1)

        except Exception as err_msg:
            messagebox.showerror("Error", "Unable to select\n"+str(err_msg), parent=self)





    def borrow_transactions_tab_fun(self):
        
        """BORROW_TRANSACTION_DETAILS TABLE frames and widgets"""

        try:
            #frame
            self.borrow_transaction_details_frames_run_flag = 1

            #initial frames
            self.db_gui_frame_6 = tk.Frame(self, bg="White")
            self.db_gui_frame_6.place(x=int(self.winfo_width()*0.05), y=int(self.winfo_height()*0.05), width=int(self.winfo_width()*0.9), height=int(self.winfo_height()*0.35))

            self.db_gui_frame_7 = tk.Frame(self, bg="White")
            self.db_gui_frame_7.place(x=int(self.winfo_width()*0.05), y=int(self.winfo_height()*0.45), width=int(self.winfo_width()*0.9), height=int(self.winfo_height()*0.50))

            #Attributes
            self.borrow_id_var_borrow_transaction = tk.IntVar(value=1)
            borrow_id_checkbox_borrow_transaction = tk.Checkbutton(self.db_gui_frame_6, text="", variable=self.borrow_id_var_borrow_transaction)
            borrow_id_checkbox_borrow_transaction.place(x=int(self.winfo_width()*0.02), y=int(self.winfo_height()*0.04))

            borrow_id_label_borrow_transaction = tk.Label(self.db_gui_frame_6, text="Borrow ID: ", font=("Cambria", 15), bg="White", fg="Black")
            borrow_id_label_borrow_transaction.place(x=int(self.winfo_width()*0.04), y=int(self.winfo_height()*0.04))

            self.txt_borrow_id_entry = tk.Entry(self.db_gui_frame_6, font=("Times New Roman", 15), bg="lightgrey", width=int(self.winfo_width()*0.016))
            self.txt_borrow_id_entry.place(x=int(self.winfo_width()*0.14), y=int(self.winfo_height()*0.04))

            
            self.book_id_var_borrow_transaction = tk.IntVar(value=1)
            book_id_checkbox_borrow_transaction = tk.Checkbutton(self.db_gui_frame_6, text="", variable=self.book_id_var_borrow_transaction)
            book_id_checkbox_borrow_transaction.place(x=int(self.winfo_width()*0.02), y=int(self.winfo_height()*0.11))

            book_id_label_borrow_transaction = tk.Label(self.db_gui_frame_6, text="Book ID: ", font=("Cambria", 15), bg="White", fg="Black")
            book_id_label_borrow_transaction.place(x=int(self.winfo_width()*0.04), y=int(self.winfo_height()*0.11))

            self.txt_borrow_book_id_entry = tk.Entry(self.db_gui_frame_6, font=("Times New Roman", 15), bg="lightgrey", width=int(self.winfo_width()*0.016))
            self.txt_borrow_book_id_entry.place(x=int(self.winfo_width()*0.14), y=int(self.winfo_height()*0.11))
            
            
            self.member_id_var_borrow_transaction = tk.IntVar(value=1)
            member_id_checkbox_borrow_transaction = tk.Checkbutton(self.db_gui_frame_6, text="", variable=self.member_id_var_borrow_transaction)
            member_id_checkbox_borrow_transaction.place(x=int(self.winfo_width()*0.02), y=int(self.winfo_height()*0.18))

            member_id_label_borrow_transaction = tk.Label(self.db_gui_frame_6, text="Member ID: ", font=("Cambria", 15), bg="White", fg="Black")
            member_id_label_borrow_transaction.place(x=int(self.winfo_width()*0.04), y=int(self.winfo_height()*0.18))

            self.txt_borrow_member_id_entry = tk.Entry(self.db_gui_frame_6, font=("Times New Roman", 15), bg="lightgrey", width=int(self.winfo_width()*0.016))
            self.txt_borrow_member_id_entry.place(x=int(self.winfo_width()*0.14), y=int(self.winfo_height()*0.18))
            
            
            self.date_of_issue_var_borrow_transaction = tk.IntVar(value=1)
            date_of_issue_checkbox_borrow_transaction = tk.Checkbutton(self.db_gui_frame_6, text="", variable=self.date_of_issue_var_borrow_transaction)
            date_of_issue_checkbox_borrow_transaction.place(x=int(self.winfo_width()*0.31), y=int(self.winfo_height()*0.04))

            date_of_issue_label_borrow_transaction = tk.Label(self.db_gui_frame_6, text="Date of issue: ", font=("Cambria", 15), bg="White", fg="Black")
            date_of_issue_label_borrow_transaction.place(x=int(self.winfo_width()*0.33), y=int(self.winfo_height()*0.04))

            self.txt_borrow_date_of_issue_entry = tk.Entry(self.db_gui_frame_6, font=("Times New Roman", 15), bg="lightgrey", width=int(self.winfo_width()*0.016))
            self.txt_borrow_date_of_issue_entry.place(x=int(self.winfo_width()*0.43), y=int(self.winfo_height()*0.04))
            

            self.date_of_return_var_borrow_transaction = tk.IntVar(value=1)
            date_of_return_checkbox_borrow_transaction = tk.Checkbutton(self.db_gui_frame_6, text="", variable=self.date_of_return_var_borrow_transaction)
            date_of_return_checkbox_borrow_transaction.place(x=int(self.winfo_width()*0.31), y=int(self.winfo_height()*0.11))

            date_of_return_label_borrow_transaction = tk.Label(self.db_gui_frame_6, text="Date of return: ", font=("Cambria", 15), bg="White", fg="Black")
            date_of_return_label_borrow_transaction.place(x=int(self.winfo_width()*0.33), y=int(self.winfo_height()*0.11))

            self.txt_borrow_date_of_return_entry = tk.Entry(self.db_gui_frame_6, font=("Times New Roman", 15), bg="lightgrey", width=int(self.winfo_width()*0.016))
            self.txt_borrow_date_of_return_entry.place(x=int(self.winfo_width()*0.43), y=int(self.winfo_height()*0.11))
            
            
            self.fine_var_borrow_transaction = tk.IntVar(value=1)
            fine_checkbox_borrow_transaction = tk.Checkbutton(self.db_gui_frame_6, text="", variable=self.fine_var_borrow_transaction)
            fine_checkbox_borrow_transaction.place(x=int(self.winfo_width()*0.31), y=int(self.winfo_height()*0.18))

            fine_label_borrow_transaction = tk.Label(self.db_gui_frame_6, text="Fine: ", font=("Cambria", 15), bg="White", fg="Black")
            fine_label_borrow_transaction.place(x=int(self.winfo_width()*0.33), y=int(self.winfo_height()*0.18))

            self.txt_borrow_fine_entry = tk.Entry(self.db_gui_frame_6, font=("Times New Roman", 15), bg="lightgrey", width=int(self.winfo_width()*0.016))
            self.txt_borrow_fine_entry.place(x=int(self.winfo_width()*0.43), y=int(self.winfo_height()*0.18))


            self.status_var_borrow_transaction = tk.IntVar(value=1)
            status_checkbox_borrow_transaction = tk.Checkbutton(self.db_gui_frame_6, text="", variable=self.status_var_borrow_transaction)
            status_checkbox_borrow_transaction.place(x=int(self.winfo_width()*0.60), y=int(self.winfo_height()*0.04))

            status_label_borrow_transaction = tk.Label(self.db_gui_frame_6, text="Status: ", font=("Cambria", 15), bg="White", fg="Black")
            status_label_borrow_transaction.place(x=int(self.winfo_width()*0.62), y=int(self.winfo_height()*0.04))

            self.txt_borrow_status_entry = tk.Entry(self.db_gui_frame_6, font=("Times New Roman", 15), bg="lightgrey", width=int(self.winfo_width()*0.016))
            self.txt_borrow_status_entry.place(x=int(self.winfo_width()*0.72), y=int(self.winfo_height()*0.04))

            Date_type_note_label_borrow_transaction = tk.Label(self.db_gui_frame_6, text="Note: '0000-00-00' can be used to represent\n'None' value for 'Date' data type attributes.", font=("Cambria", 15), bg="White", fg="Black")
            Date_type_note_label_borrow_transaction.place(x=int(self.winfo_width()*0.60), y=int(self.winfo_height()*0.11))


            #buttons
            back_btn = tk.Button(self.db_gui_frame_6, text=chr(8630)+" Back", command=self.clear_borrow_transaction_frames_for_tab_sel_fun, cursor="hand2", fg="Black", bg="Crimson", font=("Calibri", 15, "bold"), activebackground="#a30f2d", activeforeground="White", width=int(self.winfo_width()*0.008), height=int(self.winfo_height()*0.002))
            back_btn.place(x=int(self.winfo_width()*0.06), y=int(self.winfo_height()*0.26))

            insert_btn = tk.Button(self.db_gui_frame_6, text="Insert", command=self.borrow_transactions_insert_fun, cursor="hand2", fg="Black", bg="Crimson", font=("Calibri", 15, "bold"), activebackground="#a30f2d", activeforeground="White", width=int(self.winfo_width()*0.008), height=int(self.winfo_height()*0.002))
            insert_btn.place(x=int(self.winfo_width()*0.16), y=int(self.winfo_height()*0.26))

            update_btn = tk.Button(self.db_gui_frame_6, text="Update", command=self.borrow_transactions_update_fun, cursor="hand2", fg="Black", bg="Crimson", font=("Calibri", 15, "bold"), activebackground="#a30f2d", activeforeground="White", width=int(self.winfo_width()*0.008), height=int(self.winfo_height()*0.002))
            update_btn.place(x=int(self.winfo_width()*0.26), y=int(self.winfo_height()*0.26))

            delete_btn = tk.Button(self.db_gui_frame_6, text="Delete", command=self.borrow_transactions_delete_fun, cursor="hand2", fg="Black", bg="Crimson", font=("Calibri", 15, "bold"), activebackground="#a30f2d", activeforeground="White", width=int(self.winfo_width()*0.008), height=int(self.winfo_height()*0.002))
            delete_btn.place(x=int(self.winfo_width()*0.36), y=int(self.winfo_height()*0.26))

            search_btn = tk.Button(self.db_gui_frame_6, text="Search", command=self.borrow_transactions_search_fun, cursor="hand2", fg="Black", bg="Crimson", font=("Calibri", 15, "bold"), activebackground="#a30f2d", activeforeground="White", width=int(self.winfo_width()*0.008), height=int(self.winfo_height()*0.002))
            search_btn.place(x=int(self.winfo_width()*0.46), y=int(self.winfo_height()*0.26))

            view_all_btn = tk.Button(self.db_gui_frame_6, text="View all", command=self.borrow_transactions_view_all_fun, cursor="hand2", fg="Black", bg="Crimson", font=("Calibri", 15, "bold"), activebackground="#a30f2d", activeforeground="White", width=int(self.winfo_width()*0.008), height=int(self.winfo_height()*0.002))
            view_all_btn.place(x=int(self.winfo_width()*0.56), y=int(self.winfo_height()*0.26))

            insert_btn = tk.Button(self.db_gui_frame_6, text="Clear", command=self.borrow_transactions_frontend_widgets_clear_fun, cursor="hand2", fg="Black", bg="Crimson", font=("Calibri", 15, "bold"), activebackground="#a30f2d", activeforeground="White", width=int(self.winfo_width()*0.008), height=int(self.winfo_height()*0.002))
            insert_btn.place(x=int(self.winfo_width()*0.66), y=int(self.winfo_height()*0.26))

            export_to_csv_btn = tk.Button(self.db_gui_frame_6, text="Export", command=self.borrow_transactions_export_to_csv_fun, cursor="hand2", fg="Black", bg="Crimson", font=("Calibri", 15, "bold"), activebackground="#a30f2d", activeforeground="White", width=int(self.winfo_width()*0.008), height=int(self.winfo_height()*0.002))
            export_to_csv_btn.place(x=int(self.winfo_width()*0.76), y=int(self.winfo_height()*0.26))

            #Data view widget
            self.display_info_view_borrow_transaction_details = ttk.Treeview(self.db_gui_frame_7, selectmode ="browse")
            self.display_info_view_borrow_transaction_details["columns"] = ("Borrow Trans. ID", "Book ID", "Member ID", "Date of issue", "Date of return", "Fine", "Status", "Data entered by", "Timestamp")

            #treeview style
            """Currently set to common style as defined in construtor"""

            self.display_info_view_borrow_transaction_details.column("#0", width=0, stretch="NO")
            for label in list(self.display_info_view_borrow_transaction_details["columns"]):
                self.display_info_view_borrow_transaction_details.column(label, anchor=tk.CENTER, minwidth=int(self.winfo_width()*0.04))
                self.display_info_view_borrow_transaction_details.heading(label, text=label, anchor=tk.CENTER)
            
            self.display_info_view_borrow_transaction_details.place(x=int(self.winfo_width()*0), y=int(self.winfo_height()*0), width=int(self.winfo_width()*0.90), height=int(self.winfo_height()*0.50))
            self.display_info_view_borrow_transaction_details.bind("<ButtonRelease-1>", self.select_row_treeview_borrow_transactions_fun)

            #Scrollbars
            verscrlbar_display_info_view_borrow_transactions = ttk.Scrollbar(self.display_info_view_borrow_transaction_details, orient ="vertical", command = self.display_info_view_borrow_transaction_details.yview)
            verscrlbar_display_info_view_borrow_transactions.pack(side ='right', fill ='y')
            self.display_info_view_borrow_transaction_details.configure(yscrollcommand = verscrlbar_display_info_view_borrow_transactions.set)

            horscrlbar_display_info_view_borrow_transactions = ttk.Scrollbar(self.display_info_view_borrow_transaction_details, orient ="horizontal", command = self.display_info_view_borrow_transaction_details.xview)
            horscrlbar_display_info_view_borrow_transactions.pack(side ='bottom', fill ='x')
            self.display_info_view_borrow_transaction_details.configure(xscrollcommand = horscrlbar_display_info_view_borrow_transactions.set)

        except Exception as err_msg:
            messagebox.showerror("Error", "Frames and widgets error...\n\n"+str(err_msg), parent=self)



    def clear_borrow_transaction_frames_for_tab_sel_fun(self):
        
        """Removes frames and calls table_sel_fun() (for BORROW_TRANSACTION_DETAILS)"""

        try:
            if (messagebox.askyesno("Return back", "Do you wish to run 'Clear' operation before leaving?\n\nRecommended action: Press 'Yes' for efficient memory usage")):
                #clear treeview
                self.display_info_view_borrow_transaction_details.delete(*self.display_info_view_borrow_transaction_details.get_children())

                #clear entry widgets
                self.txt_borrow_id_entry.delete(0, 'end')
                self.txt_borrow_book_id_entry.delete(0, 'end')
                self.txt_borrow_member_id_entry.delete(0, 'end')
                self.txt_borrow_date_of_issue_entry.delete(0, 'end')
                self.txt_borrow_date_of_return_entry.delete(0, 'end')
                self.txt_borrow_fine_entry.delete(0, 'end')
                self.txt_borrow_status_entry.delete(0, 'end')

                #checkbox widget (selected state)
                self.borrow_id_var_borrow_transaction.set(1)
                self.book_id_var_borrow_transaction.set(1)
                self.member_id_var_borrow_transaction.set(1)
                self.date_of_issue_var_borrow_transaction.set(1)
                self.date_of_return_var_borrow_transaction.set(1)
                self.fine_var_borrow_transaction.set(1)
                self.status_var_borrow_transaction.set(1)

                #clearing res variable data
                self.res_val_borrow_transactions = []

            self.db_gui_frame_6.place_forget()
            self.db_gui_frame_7.place_forget()
            self.db_gui_frame_1.place(x=int(self.winfo_width()*0.3), y=int(self.winfo_height()*0.3), width=int(self.winfo_width()*0.4), height=int(self.winfo_height()*0.4))

        except Exception as err_msg:
            messagebox.showerror("Error", "Error while returning...\n\n"+str(err_msg), parent=self)



    def borrow_transactions_insert_fun(self):

        """Insert Operation (BORROW_TRANSACTION_DETAILS Table)"""

        try:
            #clearing res variable data
            self.res_val_borrow_transactions = []
            #clear treeview
            self.display_info_view_borrow_transaction_details.delete(*self.display_info_view_borrow_transaction_details.get_children())
            
            #get values
            values_gather_dict_borrow_transactions = {"borrow_trans_id" : (self.borrow_id_var_borrow_transaction.get(), self.txt_borrow_id_entry.get()), 
            "book_id" : (self.book_id_var_borrow_transaction.get(), self.txt_borrow_book_id_entry.get()), 
            "member_id" : (self.member_id_var_borrow_transaction.get(), self.txt_borrow_member_id_entry.get()), 
            "book_issue_date" : (self.date_of_issue_var_borrow_transaction.get(), self.txt_borrow_date_of_issue_entry.get()), 
            "book_return_date" : (self.date_of_return_var_borrow_transaction.get(), self.txt_borrow_date_of_return_entry.get()), 
            "fine" : (self.fine_var_borrow_transaction.get(), self.txt_borrow_fine_entry.get()), 
            "status" : (self.status_var_borrow_transaction.get(), self.txt_borrow_status_entry.get()), 
            "entry_made_or_alt_by": (1, self.user_name)}
 
            #borrow_trans_id validation
            if (values_gather_dict_borrow_transactions["borrow_trans_id"][0]):
                if ((not values_gather_dict_borrow_transactions["borrow_trans_id"][1]) or (str(values_gather_dict_borrow_transactions["borrow_trans_id"][1]).isspace())):
                    raise Exception ("Invalid Borrow Transaction ID!!")
            else:
                raise Exception ("Borrow Transaction ID is a mandatory field (chechkbox should be in on state)!!")

            #book_id validation
            if (values_gather_dict_borrow_transactions["book_id"][0]):
                if ((not values_gather_dict_borrow_transactions["book_id"][1]) or (str(values_gather_dict_borrow_transactions["book_id"][1]).isspace())):
                    raise Exception ("Invalid Book ID!!")

            #member_id validation
            if (values_gather_dict_borrow_transactions["member_id"][0]):
                if ((not values_gather_dict_borrow_transactions["member_id"][1]) or (str(values_gather_dict_borrow_transactions["member_id"][1]).isspace())):
                    raise Exception ("Invalid Member ID!!")

            #fine validation
            if (values_gather_dict_borrow_transactions["fine"][0]):
                if (str(values_gather_dict_borrow_transactions["fine"][1]).find(".") > 0):
                    temp_str_fine_borrow_transaction = str(values_gather_dict_borrow_transactions["fine"][1]).replace(".", "", 1)
                if ((not str(temp_str_fine_borrow_transaction).isnumeric())):
                    raise Exception ("Fine should be numeric!!")

            #basic book_issue_date validation
            regex_date = "^[0-9]?[0-9]?[0-9]?[0-9][-][0-1]?[0-9][-][0-3]?[0-9]"
            if (values_gather_dict_borrow_transactions["book_issue_date"][0]):
                if (not re.fullmatch(regex_date, values_gather_dict_borrow_transactions["book_issue_date"][1])):
                    raise Exception ("Invalid book issue date!! (format: YYYY-MM-DD)")

            #basic book_return_date validation
            regex_date = "^[0-9]?[0-9]?[0-9]?[0-9][-][0-1]?[0-9][-][0-3]?[0-9]"
            if (values_gather_dict_borrow_transactions["book_return_date"][0]):
                if (not re.fullmatch(regex_date, values_gather_dict_borrow_transactions["book_return_date"][1])):
                    raise Exception ("Invalid book return date!!(format: YYYY-MM-DD)")
            
            columns_borrow_transactions = []
            values_borrow_transactions = []
            for col in values_gather_dict_borrow_transactions.keys():
                #appending to apt list
                columns_borrow_transactions.append(col)
                if (((col == "book_issue_date") or (col == "book_return_date")) and (not values_gather_dict_borrow_transactions[col][0])):
                    values_borrow_transactions.append('0000-00-00')
                elif ((col == "fine") and (not values_gather_dict_borrow_transactions[col][0])):
                    #appending to apt list
                    values_borrow_transactions.append(0.0)
                else:        
                    values_borrow_transactions.append(values_gather_dict_borrow_transactions[col][1]*values_gather_dict_borrow_transactions[col][0])


            #statement
            borrow_transactions_insert_stmnt = "INSERT INTO BORROW_TRANSACTION_DETAILS ("+", ".join(columns_borrow_transactions)+") values ("+("%s, "*len(columns_borrow_transactions))[:-2]+");"
            
            with self.db_obj.cursor(buffered=True) as db_cursor:
                try:
                    db_cursor.execute(borrow_transactions_insert_stmnt, tuple(values_borrow_transactions))
                    db_cursor.execute("SELECT * FROM BORROW_TRANSACTION_DETAILS where borrow_trans_id = %s", (values_gather_dict_borrow_transactions["borrow_trans_id"][1],))
                    self.res_val_borrow_transactions = [db_cursor.fetchone()]
                except Exception as err_msg:
                    raise Exception ("SQL error... rolling back to last commit\n\n"+str(err_msg))
                else:
                    self.display_info_view_borrow_transaction_details.insert(parent="", index="end", values=self.res_val_borrow_transactions[0])
                    self.db_obj.commit()
        
        except Exception as err_msg:
            messagebox.showerror("Error", "Insert operation failed\n\n"+str(err_msg), parent=self)
            self.db_obj.rollback()



    def borrow_transactions_update_fun(self):

        """Update Operation (BORROW_TRANSACTION_DETAILS Table)"""

        try:
            #clearing res variable data
            self.res_val_borrow_transactions = []
            #clear treeview
            self.display_info_view_borrow_transaction_details.delete(*self.display_info_view_borrow_transaction_details.get_children())
            
            #get values
            values_gather_dict_borrow_transactions = {"borrow_trans_id" : (self.borrow_id_var_borrow_transaction.get(), self.txt_borrow_id_entry.get()), 
            "book_id" : (self.book_id_var_borrow_transaction.get(), self.txt_borrow_book_id_entry.get()), 
            "member_id" : (self.member_id_var_borrow_transaction.get(), self.txt_borrow_member_id_entry.get()), 
            "book_issue_date" : (self.date_of_issue_var_borrow_transaction.get(), self.txt_borrow_date_of_issue_entry.get()), 
            "book_return_date" : (self.date_of_return_var_borrow_transaction.get(), self.txt_borrow_date_of_return_entry.get()), 
            "fine" : (self.fine_var_borrow_transaction.get(), self.txt_borrow_fine_entry.get()), 
            "status" : (self.status_var_borrow_transaction.get(), self.txt_borrow_status_entry.get()), 
            "entry_made_or_alt_by": (1, self.user_name)}
 
            #borrow_trans_id validation
            if (values_gather_dict_borrow_transactions["borrow_trans_id"][0]):
                if ((not values_gather_dict_borrow_transactions["borrow_trans_id"][1]) or (str(values_gather_dict_borrow_transactions["borrow_trans_id"][1]).isspace())):
                    raise Exception ("Invalid Borrow Transaction ID!!")
            else:
                raise Exception ("Borrow Transaction ID is a mandatory field (chechkbox should be in on state)!!")

            #Number of attributes selected
            if (sum(int(i[0]) for i in values_gather_dict_borrow_transactions.values()) < 3):
                raise Exception ("Atleast one attribute needs to be selected other than Borrow Transaction ID!!")

            #book_id validation
            if (values_gather_dict_borrow_transactions["book_id"][0]):
                if ((not values_gather_dict_borrow_transactions["book_id"][1]) or (str(values_gather_dict_borrow_transactions["book_id"][1]).isspace())):
                    raise Exception ("Invalid Book ID!!")

            #member_id validation
            if (values_gather_dict_borrow_transactions["member_id"][0]):
                if ((not values_gather_dict_borrow_transactions["member_id"][1]) or (str(values_gather_dict_borrow_transactions["member_id"][1]).isspace())):
                    raise Exception ("Invalid Member ID!!")

            #fine validation
            if (values_gather_dict_borrow_transactions["fine"][0]):
                if (str(values_gather_dict_borrow_transactions["fine"][1]).find(".") > 0):
                    temp_str_fine_borrow_transaction = str(values_gather_dict_borrow_transactions["fine"][1]).replace(".", "", 1)
                if ((not str(temp_str_fine_borrow_transaction).isnumeric())):
                    raise Exception ("Fine should be numeric!!")

            #basic book_issue_date validation
            regex_date = "^[0-9]?[0-9]?[0-9]?[0-9][-][0-1]?[0-9][-][0-3]?[0-9]"
            if (values_gather_dict_borrow_transactions["book_issue_date"][0]):
                if (not re.fullmatch(regex_date, values_gather_dict_borrow_transactions["book_issue_date"][1])):
                    raise Exception ("Invalid book issue date!! (format: YYYY-MM-DD)")

            #basic book_return_date validation
            regex_date = "^[0-9]?[0-9]?[0-9]?[0-9][-][0-1]?[0-9][-][0-3]?[0-9]"
            if (values_gather_dict_borrow_transactions["book_return_date"][0]):
                if (not re.fullmatch(regex_date, values_gather_dict_borrow_transactions["book_return_date"][1])):
                    raise Exception ("Invalid book return date!!(format: YYYY-MM-DD)")
            
            columns_borrow_transactions = []
            values_borrow_transactions = []
            for col in values_gather_dict_borrow_transactions.keys():
                if ((values_gather_dict_borrow_transactions[col][0]) and (col != "borrow_trans_id")):
                    #appending to apt list
                    columns_borrow_transactions.append(col)
                    values_borrow_transactions.append(values_gather_dict_borrow_transactions[col][1])
                        
            #appending borrow_trans_id
            values_borrow_transactions.append(values_gather_dict_borrow_transactions["borrow_trans_id"][1])

            #statement
            borrow_transactions_update_stmnt = "UPDATE BORROW_TRANSACTION_DETAILS SET "+" = %s, ".join(columns_borrow_transactions)+" = %s where borrow_trans_id = %s;"

            
            with self.db_obj.cursor(buffered=True) as db_cursor:
                try:
                    db_cursor.execute(borrow_transactions_update_stmnt, tuple(values_borrow_transactions))
                    db_cursor.execute("SELECT * FROM BORROW_TRANSACTION_DETAILS where borrow_trans_id = %s", (values_gather_dict_borrow_transactions["borrow_trans_id"][1],))
                    self.res_val_borrow_transactions = [db_cursor.fetchone()]
                except Exception as err_msg:
                    raise Exception ("SQL error... rolling back to last commit\n\n"+str(err_msg))
                else:
                    self.display_info_view_borrow_transaction_details.insert(parent="", index="end", values=self.res_val_borrow_transactions[0])
                    self.db_obj.commit()

        except Exception as err_msg:
            messagebox.showerror("Error", "Update operation failed\n\n"+str(err_msg), parent=self)
            self.db_obj.rollback()


    def borrow_transactions_delete_fun(self):

        """Delete Operation (BORROW_TRANSACTION_DETAILS Table)"""

        try:
            #clearing res variable data
            self.res_val_borrow_transactions = []
            #clear treeview
            self.display_info_view_borrow_transaction_details.delete(*self.display_info_view_borrow_transaction_details.get_children())
            
            #get values
            values_gather_dict_borrow_transactions = {"borrow_trans_id" : (self.borrow_id_var_borrow_transaction.get(), self.txt_borrow_id_entry.get()), 
            "book_id" : (self.book_id_var_borrow_transaction.get(), self.txt_borrow_book_id_entry.get()), 
            "member_id" : (self.member_id_var_borrow_transaction.get(), self.txt_borrow_member_id_entry.get()), 
            "book_issue_date" : (self.date_of_issue_var_borrow_transaction.get(), self.txt_borrow_date_of_issue_entry.get()), 
            "book_return_date" : (self.date_of_return_var_borrow_transaction.get(), self.txt_borrow_date_of_return_entry.get()), 
            "fine" : (self.fine_var_borrow_transaction.get(), self.txt_borrow_fine_entry.get()), 
            "status" : (self.status_var_borrow_transaction.get(), self.txt_borrow_status_entry.get()), 
            "entry_made_or_alt_by": (1, self.user_name)}

            #Number of attributes selected
            if (sum(int(i[0]) for i in values_gather_dict_borrow_transactions.values()) < 2):
                raise Exception ("Atleast one attribute needs to be selected!!")

            #borrow_trans_id validation
            if (values_gather_dict_borrow_transactions["borrow_trans_id"][0]):
                if ((not values_gather_dict_borrow_transactions["borrow_trans_id"][1]) or (str(values_gather_dict_borrow_transactions["borrow_trans_id"][1]).isspace())):
                    raise Exception ("Invalid Borrow Transaction ID!!")
                        
            #book_id validation
            if (values_gather_dict_borrow_transactions["book_id"][0]):
                if ((not values_gather_dict_borrow_transactions["book_id"][1]) or (str(values_gather_dict_borrow_transactions["book_id"][1]).isspace())):
                    raise Exception ("Invalid Book ID!!")

            #member_id validation
            if (values_gather_dict_borrow_transactions["member_id"][0]):
                if ((not values_gather_dict_borrow_transactions["member_id"][1]) or (str(values_gather_dict_borrow_transactions["member_id"][1]).isspace())):
                    raise Exception ("Invalid Member ID!!")

            #fine validation
            if (values_gather_dict_borrow_transactions["fine"][0]):
                if (str(values_gather_dict_borrow_transactions["fine"][1]).find(".") > 0):
                    temp_str_fine_borrow_transaction = str(values_gather_dict_borrow_transactions["fine"][1]).replace(".", "", 1)
                if ((not str(temp_str_fine_borrow_transaction).isnumeric())):
                    raise Exception ("Fine should be numeric!!")

            #basic book_issue_date validation
            regex_date = "^[0-9]?[0-9]?[0-9]?[0-9][-][0-1]?[0-9][-][0-3]?[0-9]"
            if (values_gather_dict_borrow_transactions["book_issue_date"][0]):
                if (not re.fullmatch(regex_date, values_gather_dict_borrow_transactions["book_issue_date"][1])):
                    raise Exception ("Invalid book issue date!! (format: YYYY-MM-DD)")

            #basic book_return_date validation
            regex_date = "^[0-9]?[0-9]?[0-9]?[0-9][-][0-1]?[0-9][-][0-3]?[0-9]"
            if (values_gather_dict_borrow_transactions["book_return_date"][0]):
                if (not re.fullmatch(regex_date, values_gather_dict_borrow_transactions["book_return_date"][1])):
                    raise Exception ("Invalid book return date!!(format: YYYY-MM-DD)")
            
            columns_borrow_transactions = []
            values_borrow_transactions = []
            for col in values_gather_dict_borrow_transactions.keys():
                if (values_gather_dict_borrow_transactions[col][0]):
                    #appending to apt list
                    columns_borrow_transactions.append(col)
                    values_borrow_transactions.append(values_gather_dict_borrow_transactions[col][1])

            #statement
            borrow_transactions_delete_stmnt = "DELETE FROM BORROW_TRANSACTION_DETAILS where "+" = %s and ".join(columns_borrow_transactions)+" = %s;"
            
            with self.db_obj.cursor(buffered=True) as db_cursor:
                try:
                    db_cursor.execute(borrow_transactions_delete_stmnt, tuple(values_borrow_transactions))
                except Exception as err_msg:
                    raise Exception ("SQL error... rolling back to last commit\n\n"+str(err_msg))
                else:
                    messagebox.showinfo("Successful", "Successfully deleted record(s)", parent=self)
                    self.db_obj.commit()
        
        except Exception as err_msg:
            messagebox.showerror("Error", "Delete operation failed\n\n"+str(err_msg), parent=self)
            self.db_obj.rollback()


    def borrow_transactions_search_fun(self):

        """Search Operation (BORROW_TRANSACTION_DETAILS Table)"""
        
        try:
            #clearing res variable data
            self.res_val_borrow_transactions = []
            #clear treeview
            self.display_info_view_borrow_transaction_details.delete(*self.display_info_view_borrow_transaction_details.get_children())
            
            #get values
            values_gather_dict_borrow_transactions = {"borrow_trans_id" : (self.borrow_id_var_borrow_transaction.get(), self.txt_borrow_id_entry.get()), 
            "book_id" : (self.book_id_var_borrow_transaction.get(), self.txt_borrow_book_id_entry.get()), 
            "member_id" : (self.member_id_var_borrow_transaction.get(), self.txt_borrow_member_id_entry.get()), 
            "book_issue_date" : (self.date_of_issue_var_borrow_transaction.get(), self.txt_borrow_date_of_issue_entry.get()), 
            "book_return_date" : (self.date_of_return_var_borrow_transaction.get(), self.txt_borrow_date_of_return_entry.get()), 
            "fine" : (self.fine_var_borrow_transaction.get(), self.txt_borrow_fine_entry.get()), 
            "status" : (self.status_var_borrow_transaction.get(), self.txt_borrow_status_entry.get()), 
            "entry_made_or_alt_by": (1, self.user_name)}

            #Number of attributes selected
            if (sum(int(i[0]) for i in values_gather_dict_borrow_transactions.values()) < 2):
                raise Exception ("Atleast one attribute needs to be selected!!")

            #borrow_trans_id validation
            if (values_gather_dict_borrow_transactions["borrow_trans_id"][0]):
                if ((not values_gather_dict_borrow_transactions["borrow_trans_id"][1]) or (str(values_gather_dict_borrow_transactions["borrow_trans_id"][1]).isspace())):
                    raise Exception ("Invalid Borrow Transaction ID!!")
                        
            #book_id validation
            if (values_gather_dict_borrow_transactions["book_id"][0]):
                if ((not values_gather_dict_borrow_transactions["book_id"][1]) or (str(values_gather_dict_borrow_transactions["book_id"][1]).isspace())):
                    raise Exception ("Invalid Book ID!!")

            #member_id validation
            if (values_gather_dict_borrow_transactions["member_id"][0]):
                if ((not values_gather_dict_borrow_transactions["member_id"][1]) or (str(values_gather_dict_borrow_transactions["member_id"][1]).isspace())):
                    raise Exception ("Invalid Member ID!!")

            #fine validation
            if (values_gather_dict_borrow_transactions["fine"][0]):
                if (str(values_gather_dict_borrow_transactions["fine"][1]).find(".") > 0):
                    temp_str_fine_borrow_transaction = str(values_gather_dict_borrow_transactions["fine"][1]).replace(".", "", 1)
                if ((not str(temp_str_fine_borrow_transaction).isnumeric())):
                    raise Exception ("Fine should be numeric!!")

            #basic book_issue_date validation
            regex_date = "^[0-9]?[0-9]?[0-9]?[0-9][-][0-1]?[0-9][-][0-3]?[0-9]"
            if (values_gather_dict_borrow_transactions["book_issue_date"][0]):
                if (not re.fullmatch(regex_date, values_gather_dict_borrow_transactions["book_issue_date"][1])):
                    raise Exception ("Invalid book issue date!! (format: YYYY-MM-DD)")

            #basic book_return_date validation
            regex_date = "^[0-9]?[0-9]?[0-9]?[0-9][-][0-1]?[0-9][-][0-3]?[0-9]"
            if (values_gather_dict_borrow_transactions["book_return_date"][0]):
                if (not re.fullmatch(regex_date, values_gather_dict_borrow_transactions["book_return_date"][1])):
                    raise Exception ("Invalid book return date!!(format: YYYY-MM-DD)")
            
            columns_borrow_transactions = []
            values_borrow_transactions = []
            for col in values_gather_dict_borrow_transactions.keys():
                if (values_gather_dict_borrow_transactions[col][0]):
                    #appending to apt list
                    columns_borrow_transactions.append(col)
                    values_borrow_transactions.append(values_gather_dict_borrow_transactions[col][1])
            
            #statement
            borrow_transactions_search_stmnt = "SELECT * FROM BORROW_TRANSACTION_DETAILS where "+" = %s and ".join(columns_borrow_transactions)+" = %s;"
            
            with self.db_obj.cursor(buffered=True) as db_cursor:
                try:
                    db_cursor.execute(borrow_transactions_search_stmnt, tuple(values_borrow_transactions))
                    self.res_val_borrow_transactions = db_cursor.fetchall()
                except Exception as err_msg:
                    raise Exception ("SQL error... rolling back to last commit\n\n"+str(err_msg))
                else:
                    if (not any(self.res_val_borrow_transactions)):
                        messagebox.showinfo("Search", "No data found!!", parent=self)
                    else:
                        for row in self.res_val_borrow_transactions:
                            self.display_info_view_borrow_transaction_details.insert(parent="", index="end", values=row)
                    self.db_obj.commit()

        except Exception as err_msg:
            messagebox.showerror("Error", "Search operation failed\n\n"+str(err_msg), parent=self)
            self.db_obj.rollback()



    def borrow_transactions_view_all_fun(self):

        """View all Operation (BORROW_TRANSACTION_DETAILS Table)"""
        
        try:
            #clearing res variable data
            self.res_val_borrow_transactions = []
            #clear treeview
            self.display_info_view_borrow_transaction_details.delete(*self.display_info_view_borrow_transaction_details.get_children())

            #statement
            borrow_transactions_view_all_stmnt = "SELECT * FROM BORROW_TRANSACTION_DETAILS;"
            
            with self.db_obj.cursor(buffered=True) as db_cursor:
                try:
                    db_cursor.execute(borrow_transactions_view_all_stmnt)
                    self.res_val_borrow_transactions = db_cursor.fetchall()
                except Exception as err_msg:
                    raise Exception ("SQL error... rolling back to last commit\n\n"+str(err_msg))
                else:
                    if (not any(self.res_val_borrow_transactions)):
                        messagebox.showinfo("View all", "No data found!!", parent=self)
                    else:
                        for row in self.res_val_borrow_transactions:
                            self.display_info_view_borrow_transaction_details.insert(parent="", index="end", values=row)
                    self.db_obj.commit()

        except Exception as err_msg:
            messagebox.showerror("Error", "View all operation failed\n\n"+str(err_msg), parent=self)
            self.db_obj.rollback()


    def borrow_transactions_frontend_widgets_clear_fun(self):

        """Front-end widgets clear Operation (BORROW_TRANSACTION_DETAILS Table)"""

        try:
            #clearing res variable data
            self.res_val_borrow_transactions = []

            #clear treeview
            self.display_info_view_borrow_transaction_details.delete(*self.display_info_view_borrow_transaction_details.get_children())

            #clear entry widgets
            self.txt_borrow_id_entry.delete(0, 'end')
            self.txt_borrow_book_id_entry.delete(0, 'end')
            self.txt_borrow_member_id_entry.delete(0, 'end')
            self.txt_borrow_date_of_issue_entry.delete(0, 'end')
            self.txt_borrow_date_of_return_entry.delete(0, 'end')
            self.txt_borrow_fine_entry.delete(0, 'end')
            self.txt_borrow_status_entry.delete(0, 'end')

            #checkbox widget (selected state)
            self.borrow_id_var_borrow_transaction.set(1)
            self.book_id_var_borrow_transaction.set(1)
            self.member_id_var_borrow_transaction.set(1)
            self.date_of_issue_var_borrow_transaction.set(1)
            self.date_of_return_var_borrow_transaction.set(1)
            self.fine_var_borrow_transaction.set(1)
            self.status_var_borrow_transaction.set(1)

        except Exception as err_msg:
            messagebox.showerror("Error", "Clear operation failed\n"+str(err_msg), parent=self)


    def borrow_transactions_export_to_csv_fun(self):

        """Export Operation (BORROW_TRANSACTION_DETAILS Table)"""
        
        try:
            #No data condition
            if (not self.res_val_borrow_transactions):
                raise Exception ("No data available!!")
            
            #File Dialog
            file_name = filedialog.asksaveasfilename(initialdir=os.getcwd(), title="Save CSV", filetypes=(("CSV files", "*.csv"), ("All files", "*.*")))
            if (not str(file_name[-4:]).lower()==".csv"):
                file_name += ".csv"

            #Write data to csv
            with open(file_name, "w", newline="") as export_file:
                csv_writer = csv.writer(export_file)
                csv_writer.writerow(self.display_info_view_borrow_transaction_details["columns"])
                csv_writer.writerows(self.res_val_borrow_transactions)
        
        except Exception as err_msg:
            messagebox.showerror("Error", "Export operation failed\n\n"+str(err_msg), parent=self)
        
        else:
            messagebox.showinfo("Successful", "Successfully exported data", parent=self)


    def select_row_treeview_borrow_transactions_fun(self, *args):

        """Select row Operation (BORROW_TRANSACTION_DETAILS Table)"""

        try:
            #clear entry widgets
            self.txt_borrow_id_entry.delete(0, 'end')
            self.txt_borrow_book_id_entry.delete(0, 'end')
            self.txt_borrow_member_id_entry.delete(0, 'end')
            self.txt_borrow_date_of_issue_entry.delete(0, 'end')
            self.txt_borrow_date_of_return_entry.delete(0, 'end')
            self.txt_borrow_fine_entry.delete(0, 'end')
            self.txt_borrow_status_entry.delete(0, 'end')

            #adding data to entry widget
            values_borrow_transactions_row = self.display_info_view_borrow_transaction_details.item(self.display_info_view_borrow_transaction_details.focus(), "values")
            self.txt_borrow_id_entry.insert(0, values_borrow_transactions_row[0])
            self.txt_borrow_book_id_entry.insert(0, values_borrow_transactions_row[1])
            self.txt_borrow_member_id_entry.insert(0, values_borrow_transactions_row[2])
            self.txt_borrow_date_of_issue_entry.insert(0, values_borrow_transactions_row[3])
            self.txt_borrow_date_of_return_entry.insert(0, values_borrow_transactions_row[4])
            self.txt_borrow_fine_entry.insert(0, values_borrow_transactions_row[5])
            self.txt_borrow_status_entry.insert(0, values_borrow_transactions_row[6])

            #checkbox widget (selected state)
            self.borrow_id_var_borrow_transaction.set(1)
            self.book_id_var_borrow_transaction.set(1)
            self.member_id_var_borrow_transaction.set(1)
            self.date_of_issue_var_borrow_transaction.set(1)
            self.date_of_return_var_borrow_transaction.set(1)
            self.fine_var_borrow_transaction.set(1)
            self.status_var_borrow_transaction.set(1)

        except Exception as err_msg:
            messagebox.showerror("Error", "Unable to select\n"+str(err_msg), parent=self)    
       




    def quit_msg_fun(self):

        """Close alert function"""

        try:
            if (messagebox.askyesno("Quit","Do you really want to quit?")):
                #stopping animation
                self.title_db_gui.after_cancel(self.run_task_sliding_animation_title_table_sel)
                #closing window
                self.destroy()
        except Exception as err_msg:
            messagebox.showerror("Error", "Closing error: \n\n"+str(err_msg), parent=self)
            #stopping animation
            self.title_db_gui.after_cancel(self.run_task_sliding_animation_title_table_sel)
            #closing window
            self.destroy()


        


def database_gui_launch_fun(db_obj, user_name):
    try:
        #Instantiation
        window_db_gui = DatabaseGui(db_obj, user_name)
        #Calling Table selection function
        window_db_gui.table_sel_fun()
        #calling animation function
        window_db_gui.run_task_sliding_animation_title_table_sel = window_db_gui.sliding_animation_title_table_sel()
        #Call to quit_msg_func
        window_db_gui.protocol("WM_DELETE_WINDOW", window_db_gui.quit_msg_fun)
        #Loop                
        window_db_gui.mainloop()
    except Exception as err_msg:
        try:
            messagebox.showerror("Error", "Unable to run the application.\n"+str(err_msg), parent=window_db_gui)
        except Exception as err_msg:
            print(str(err_msg))
