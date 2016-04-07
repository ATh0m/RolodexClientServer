import tkinter as tk
import datetime
import xmlrpc.client


class Contact:
    def __init__(self, name=None, surname=None, phone=None, mail=None, last_open=None):
        self.name = name
        self.surname = surname
        self.phone = phone
        self.mail = mail
        self.last_open = last_open

    def __str__(self):
        if self.name is None:
            return self.surname
        if self.surname is None:
            return self.name
        return self.name + ' ' + self.surname


class ContactApp:
    def __init__(self, master, url):
        self.config_master_window(master)

        self.server = self.connect_to_server(url)

        self.index_list = []
        self.data = []

        self.read_from_database()

        self.search_entry_var = tk.StringVar()
        self.search_entry = tk.Entry()

        self.listbox = tk.Listbox()

        self.last_open_label_var = tk.StringVar()
        self.last_open_label = tk.Label()

        self.name_entry_var = tk.StringVar()
        self.name_entry = tk.Entry()
        self.surname_entry_var = tk.StringVar()
        self.surname_entry = tk.Entry()
        self.phone_entry_var = tk.StringVar()
        self.phone_entry = tk.Entry()
        self.mail_entry_var = tk.StringVar()
        self.mail_entry = tk.Entry()

        self.edit_button = tk.Button()
        self.save_button = tk.Button()
        self.delete_button = tk.Button()
        self.add_button = tk.Button()

        self.current_index = int()
        self.current_contact = Contact()

        self.config_frames(master)

    @staticmethod
    def config_master_window(master):
        master.title('Wizytownik')
        master.minsize(width=650, height=300)

    @staticmethod
    def connect_to_server(url):
        return xmlrpc.client.ServerProxy(url, allow_none=True)

    def read_from_database(self):

        try:
            data = self.server.read_from_database()
        except:
            print("CONNECTION LOST")
            raise

        print("read_from_database")
        print(data)

        contact_data = []
        for item in data:
            contact_data.append(Contact(**item))

        self.data = sorted(contact_data, key=lambda x: x.surname + x.name)

    def save_to_database(self):

        data = []
        for item in self.data:
            print(item.__dict__)
            data.append(item.__dict__)

        print("save_to_database")
        print(data)

        try:
            self.server.save_to_database(data)
        except:
            print("CONNECTION LOST")
            raise

    def config_frames(self, master):
        main_frame = tk.Frame(master)
        main_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        left_frame = tk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.create_search(left_frame)
        self.create_list(left_frame)

        separator_frame = tk.Frame(main_frame, bg='black')
        separator_frame.pack(side=tk.LEFT, fill=tk.Y)

        right_frame = tk.Frame(main_frame)
        right_frame.pack(fill=tk.BOTH, expand=1)

        self.create_contact_view(right_frame)

    def create_search(self, master):

        search_frame = tk.Frame(master)
        search_frame.pack(fill=tk.X, side=tk.TOP)

        self.search_entry_var = tk.StringVar()
        self.search_entry_var.trace("w", lambda name, index, mode: self.update_list())

        self.search_entry = tk.Entry(search_frame, textvariable=self.search_entry_var)
        self.search_entry.pack(fill=tk.X)

    def create_list(self, master):

        list_frame = tk.Frame(master)
        list_frame.pack(fill=tk.BOTH, expand=1, side=tk.BOTTOM)

        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox = tk.Listbox(list_frame, bd=0)
        self.listbox.pack(side=tk.LEFT, fill=tk.Y, expand=1)

        self.listbox.bind('<<ListboxSelect>>', self.item_selected)

        self.update_list()

        self.listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox.yview)

    def update_list(self):
        self.listbox.delete(0, tk.END)

        search_term = self.search_entry_var.get().lower()
        self.index_list = []

        for index, value in enumerate(self.data):
            if search_term in value.name.lower() or search_term in value.surname.lower() \
               or search_term in value.phone.lower() or search_term in value.mail.lower():
                self.index_list.append(index)
                self.listbox.insert(tk.END, ' ' + str(value))

    def item_selected(self, event):
        index = self.listbox.curselection()[0]
        self.current_index = index

        self.show_contact_view(self.current_index)

    def create_contact_view(self, master):
        main_view_frame = tk.Frame(master)
        main_view_frame.pack(expand=1, fill=tk.BOTH)

        toolbar_frame = tk.Frame(main_view_frame)
        toolbar_frame.pack(side=tk.TOP, fill=tk.X)

        self.last_open_label_var = tk.StringVar()
        self.last_open_label = tk.Label(toolbar_frame, textvariable=self.last_open_label_var, font=('Helvetica', 15))
        self.last_open_label.pack(side=tk.RIGHT)

        entries_frame = tk.Frame(main_view_frame)
        entries_frame.pack(side=tk.LEFT, expand=1, fill=tk.BOTH)
        entries_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        name_frame = tk.Frame(entries_frame)
        name_frame.pack(fill=tk.X)

        self.name_entry_var = tk.StringVar()
        self.name_entry = tk.Entry(name_frame, textvariable=self.name_entry_var, font=('Helvetica', 30))
        self.name_entry.pack(fill=tk.X)

        surname_frame = tk.Frame(entries_frame)
        surname_frame.pack(fill=tk.X)

        self.surname_entry_var = tk.StringVar()
        self.surname_entry = tk.Entry(surname_frame, textvariable=self.surname_entry_var, font=('Helvetica', 30))
        self.surname_entry.pack(fill=tk.X)

        phone_frame = tk.Frame(entries_frame)
        phone_frame.pack(fill=tk.X)

        self.phone_entry_var = tk.StringVar()
        self.phone_entry = tk.Entry(phone_frame, textvariable=self.phone_entry_var, font=('Helvetica', 20))
        self.phone_entry.pack(fill=tk.X)

        mail_frame = tk.Frame(entries_frame)
        mail_frame.pack(fill=tk.X)

        self.mail_entry_var = tk.StringVar()
        self.mail_entry = tk.Entry(mail_frame, textvariable=self.mail_entry_var, font=('Helvetica', 20))
        self.mail_entry.pack(fill=tk.X)

        main_buttons_frame = tk.Frame(master)
        main_buttons_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.edit_button = tk.Button(main_buttons_frame, text="EDYCJA")
        self.edit_button.bind('<Button-1>', self.edit_selected)

        self.save_button = tk.Button(main_buttons_frame, text="GOTOWE")
        self.save_button.bind('<Button-1>', self.save_selected)

        self.delete_button = tk.Button(main_buttons_frame, text="USUN")
        self.delete_button.bind('<Button-1>', self.delete_selected)

        self.add_button = tk.Button(main_buttons_frame, text="+")
        self.add_button.bind('<Button-1>', self.add_selected)
        self.add_button.pack(side=tk.LEFT)

        self.show_contact_view(-1)

    def show_contact_view(self, index):

        self.current_index = index

        if self.current_index == -1:
            new_contact = Contact('Imię',
                                  'Nazwisko',
                                  'Telefon',
                                  'E-mail',
                                  str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

            self.current_contact = new_contact
        else:
            contact = self.data[self.index_list[self.current_index]]
            self.current_contact = contact

        self.name_entry_var.set(self.current_contact.name)
        self.name_entry.config(relief=tk.FLAT, state=tk.DISABLED, disabledforeground='black')

        self.surname_entry_var.set(self.current_contact.surname)
        self.surname_entry.config(relief=tk.FLAT, state=tk.DISABLED, disabledforeground='black')

        self.phone_entry_var.set(self.current_contact.phone)
        self.phone_entry.config(relief=tk.FLAT, state=tk.DISABLED, disabledforeground='black')

        self.mail_entry_var.set(self.current_contact.mail)
        self.mail_entry.config(relief=tk.FLAT, state=tk.DISABLED, disabledforeground='black')

        self.last_open_label_var.set(self.current_contact.last_open)

        self.current_contact.last_open = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        self.save_to_database()

        self.save_button.pack_forget()
        self.delete_button.pack_forget()
        self.edit_button.pack_forget()

        if self.current_index == -1:
            self.edit_selected()
        else:
            self.edit_button.pack(side=tk.RIGHT)

    def edit_selected(self, event=None):
        self.name_entry.config(relief=tk.SUNKEN, state=tk.NORMAL, disabledforeground='black')
        self.surname_entry.config(relief=tk.SUNKEN, state=tk.NORMAL, disabledforeground='black')
        self.phone_entry.config(relief=tk.SUNKEN, state=tk.NORMAL, disabledforeground='black')
        self.mail_entry.config(relief=tk.SUNKEN, state=tk.NORMAL, disabledforeground='black')

        self.save_button.pack_forget()
        self.delete_button.pack_forget()
        self.edit_button.pack_forget()

        self.save_button.pack(side=tk.RIGHT)

        if self.current_index != -1:
            self.delete_button.pack(side=tk.RIGHT)

    def save_selected(self, event):
        new_contact = Contact(self.name_entry.get(), self.surname_entry.get(), self.phone_entry.get(),
                              self.mail_entry.get())

        if self.current_index == -1:
            self.data.append(new_contact)
        else:
            self.data[self.index_list[self.current_index]] = new_contact

        self.current_contact = new_contact

        self.data = sorted(self.data, key=lambda x: x.surname+x.name)

        self.save_to_database()

        self.update_list()
        self.show_contact_view(self.current_index)

    def delete_selected(self, event):

        if self.current_index != -1:
            del(self.data[self.index_list[self.current_index]])

            self.save_to_database()

            self.update_list()

            self.current_index = -1
            self.show_contact_view(self.current_index)

    def add_selected(self, event):

        self.current_index = -1
        self.show_contact_view(self.current_index)


root = tk.Tk()
app = ContactApp(root, 'http://localhost:8123')
root.mainloop()
