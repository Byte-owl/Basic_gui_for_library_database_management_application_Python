#Mini_Project(DBMS)(Library Database) - Ayush
#Version: 1.1
#Login page


#importing necessary libraries
import mysql.connector
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import Database_GUI


#Login Class
class MainLogin(tk.Tk):

    def __init__(self):

        """Basic window attributes"""

        try:
            #Calling parent class constructor
            super().__init__()
            
            self.title("BASIC-DB Library")
            self.geometry("{width}x{height}+0+0".format(width=self.winfo_screenwidth(), height=self.winfo_screenheight()))
            try:
                self.state("zoomed")
            except Exception as err:
                messagebox.showerror("Error", "Unable to maximize window!\n"+str(err), parent=self)
            self.iconbitmap("images/Logo_icon.ico")

            #Background
            bg_login_img = Image.open("images/Bg_Login.jpg")
            resized_bg = bg_login_img.resize((self.winfo_width(), self.winfo_height()), Image.ANTIALIAS)
            self.bg_login = ImageTk.PhotoImage(resized_bg)
            bg_login_canvas = tk.Canvas(self, width=self.winfo_width(), height=self.winfo_height())
            bg_login_canvas.pack(fill="both", expand=True)
            bg_login_canvas.create_image(0, 0, image=self.bg_login, anchor="nw")

            #variables for sliding animation for title
            self.og_title_login_text = "LOGIN"
            self.text_sliding_animation_login_index = 0
            self.text_to_be_displayed = ""
        
        except Exception as err_msg:
            messagebox.showerror("Error", "Closing Application: Initialization error\n\n"+str(err_msg), parent=self)
            self.destroy()



    def sliding_animation_title_login(self):

        """Sliding animation function"""

        try:
            if (self.text_sliding_animation_login_index >= len(self.og_title_login_text)):
                self.text_sliding_animation_login_index = 0
                self.text_to_be_displayed = ""
                self.title_login.config(text=self.text_to_be_displayed)
            else:
                self.text_to_be_displayed += self.og_title_login_text[self.text_sliding_animation_login_index]
                self.title_login.config(text=self.text_to_be_displayed)
                self.text_sliding_animation_login_index += 1
                
            #timer set to 450 ms
            self.run_task_sliding_animation_title_login = self.title_login.after(450, self.sliding_animation_title_login)
        
        except Exception as err_msg:
            messagebox.showerror("Error", "Sliding animation error", parent=self)



    def login_frame(self):

        """Creates Login window's frames and widgets"""
        
        try:
            #Attributes
            self.login_frame_1 = tk.Frame(self, bg="White")
            self.login_frame_1.place(x=int(self.winfo_width()*0.33), y=int(self.winfo_height()*0.20), width=int(self.winfo_width()*0.34), height=int(self.winfo_height()*0.6))
            
            self.title_login = tk.Label(self.login_frame_1, text="LOGIN", font=("Impact", 40, "bold"), bg="White", fg="Crimson")
            self.title_login.place(x=int(self.winfo_width()*0.125), y=int(self.winfo_height()*0.035))

            desc_login = tk.Label(self.login_frame_1, text="Library database", font=("Calibri", 16, "bold"), bg="White", fg="Black")
            desc_login.place(x=int(self.winfo_width()*0.120), y=int(self.winfo_height()*0.14)) #Roll No


            host_label_login = tk.Label(self.login_frame_1, text="Host: ", font=("Cambria", 16), bg="White", fg="Black")
            host_label_login.place(x=int(self.winfo_width()*0.03), y=int(self.winfo_height()*0.22))

            self.txt_host_entry = tk.Entry(self.login_frame_1, font=("Times New Roman", 16), bg="lightgrey", width=int(self.winfo_width()*0.016))
            self.txt_host_entry.place(x=int(self.winfo_width()*0.13), y=int(self.winfo_height()*0.22))
            self.txt_host_entry.bind("<Return>", self.login_fun)


            port_label_login = tk.Label(self.login_frame_1, text="Port: ", font=("Cambria", 16), bg="White", fg="Black")
            port_label_login.place(x=int(self.winfo_width()*0.03), y=int(self.winfo_height()*0.29))

            self.txt_port_entry = tk.Entry(self.login_frame_1, font=("Times New Roman", 16), bg="lightgrey", width=int(self.winfo_width()*0.016))
            self.txt_port_entry.place(x=int(self.winfo_width()*0.13), y=int(self.winfo_height()*0.29))
            self.txt_port_entry.bind("<Return>", self.login_fun)


            user_label_login = tk.Label(self.login_frame_1, text="Username: ", font=("Cambria", 16), bg="White", fg="Black")
            user_label_login.place(x=int(self.winfo_width()*0.03), y=int(self.winfo_height()*0.36))

            self.txt_user_entry = tk.Entry(self.login_frame_1, font=("Times New Roman", 16), bg="lightgrey", width=int(self.winfo_width()*0.016))
            self.txt_user_entry.place(x=int(self.winfo_width()*0.13), y=int(self.winfo_height()*0.36))
            self.txt_user_entry.bind("<Return>", self.login_fun)


            passwd_label_login = tk.Label(self.login_frame_1, text="Password: ", font=("Cambria", 16), bg="White", fg="Black")
            passwd_label_login.place(x=int(self.winfo_width()*0.03), y=int(self.winfo_height()*0.43))

            self.txt_passwd_entry = tk.Entry(self.login_frame_1, font=("Times New Roman", 16), bg="lightgrey", width=int(self.winfo_width()*0.016))
            self.txt_passwd_entry.place(x=int(self.winfo_width()*0.13), y=int(self.winfo_height()*0.43))
            self.txt_passwd_entry.config(show="*")
            self.txt_passwd_entry.bind("<Return>", self.login_fun)


            login_btn = tk.Button(self.login_frame_1, text="Submit", command=self.login_fun, cursor="hand2", fg="Black", bg="Crimson", font=("Cambria", 15, "bold"), activebackground='#a30f2d',activeforeground='White')
            login_btn.place(x=int(self.winfo_width()*0.137), y=int(self.winfo_height()*0.50))

        except Exception as err_msg:
            messagebox.showerror("Error", "login frame error\n\n"+str(err_msg), parent=self)

    
    def login_fun(self, *args):

        """Login data submission function"""

        try:
            #gathering input from various fields
            values_gather_dict_login = {"host_inp" : self.txt_host_entry.get(),
            "port_inp" : self.txt_port_entry.get(),
            "user_inp" : self.txt_user_entry.get(),
            "passwd_inp" : self.txt_passwd_entry.get(),
            "database_inp" : "library_a"}

            if (not all(values_gather_dict_login.values())):
                raise Exception ("All fields are required!!")

            db_obj = mysql.connector.connect(host=values_gather_dict_login["host_inp"], user=values_gather_dict_login["user_inp"], passwd=values_gather_dict_login["passwd_inp"], port=values_gather_dict_login["port_inp"])
            if (db_obj):
                try:
                    with db_obj.cursor(buffered=True) as db_cursor:
                        db_cursor.execute("Create database if not exists library_a;")
                except Exception as err_msg:
                    raise Exception ("Database creation error!!"+str(err_msg))
                else:
                    db_obj = mysql.connector.connect(host=values_gather_dict_login["host_inp"], user=values_gather_dict_login["user_inp"], passwd=values_gather_dict_login["passwd_inp"], database=values_gather_dict_login["database_inp"], port=values_gather_dict_login["port_inp"])
                    if (db_obj):
                        #stopping animation
                        self.title_login.after_cancel(self.run_task_sliding_animation_title_login)
                        #closing window
                        self.destroy()
                        #calling database GUI function
                        Database_GUI.database_gui_launch_fun(db_obj, values_gather_dict_login["user_inp"])
                    else:
                        raise Exception ("Library Database connection failed")
            else:
                raise Exception ("database connection object error...")
          
        except Exception as err_msg:
            messagebox.showerror("Error", "Login failed!\n\n"+str(err_msg), parent=self)
            
        

    def quit_msg_fun(self):

        """Close alert function"""
        
        try:
            if (messagebox.askyesno("Quit","Do you really want to quit?")):
                #stopping animation
                self.title_login.after_cancel(self.run_task_sliding_animation_title_login)
                #closing window
                self.destroy()
        except Exception as err_msg:
            messagebox.showerror("Error", "Closing error\n\n"+str(err_msg), parent=self)
            #stopping animation
            self.title_login.after_cancel(self.run_task_sliding_animation_title_login)
            #closing window
            self.destroy()



def main():
    try:
        #Instantiation
        window_login = MainLogin()
        #Creating Frames
        window_login.login_frame()
        #calling animation function
        window_login.run_task_sliding_animation_title_login = window_login.sliding_animation_title_login()
        #Call to quit_msg_func
        window_login.protocol("WM_DELETE_WINDOW", window_login.quit_msg_fun)
        #Loop                
        window_login.mainloop()
    except Exception as err_msg:
        try:
            messagebox.showerror("Error", "Unable to run the application.\n"+str(err_msg), parent=window_login)
        except Exception as err_msg:
            print(str(err_msg))



if (__name__ == "__main__"):
    #Ayush
    main()
    
