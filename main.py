import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk
import KlientEntry
import TeatrDB

from KlientDef import *


class TeatrApp:

    def __init__(self):
        self.counter = 0
        self.statusTab = []

        self.window = tk.Tk()
        self.event = tk.IntVar(master=self.window, name="Event1")
        self.event.trace("w", self.callback)
        self.klient = Klient()

        self.window.geometry('1024x600')
        self.window.title('Teatr')
        self.window.grid_rowconfigure(1, weight=1)
        self.window.grid_columnconfigure(0, weight=1)

        # -- menu ---
        self._dodaj_glowne_menu(self.window)

        # button_bar
        button_bar = tk.Frame(self.window)  # , background='magenta'  )
        button_bar.grid(row=0, column=0, padx=5, pady=5, sticky='new')
        button_bar.grid_rowconfigure(0, weight=1)
        button_bar.grid_columnconfigure(0, weight=1)
        self._dodaj_szybkie_buttony(button_bar)

        # ---
        self.middle = tk.Frame(self.window, background='green')
        self.middle.grid(row=1, column=0, padx=5, pady=5, sticky=tk.NSEW)
        self.middle.grid_rowconfigure(0, weight=1)
        self.middle.grid_columnconfigure(0, weight=0)

        self.editor1 = tk.Text(self.middle, bg='white')
        self.editor1.grid(row=0, column=0, sticky=tk.NSEW)
        self.tree = ttk.Treeview(master=self.middle, columns=self.klient_header, show="headings")
        self._build_tree()

        # self.listBox = tk.Listbox(self.middle, bg='green')
        # listbox = self.listBox
        # listbox.insert(1, "frytki")
        # listbox.insert(2, "sledziki")
        # listbox.insert(3, "obwarzanki")

        # --- StatusBar -------
        status_bar = tk.Frame(self.window)  # , background='yellow')
        status_bar.grid(row=2, column=0, padx=5, pady=2, columnspan=1, sticky=tk.NSEW)
        status_bar.grid_rowconfigure(0, weight=1)
        status_bar.grid_columnconfigure(0, weight=1)
        self._dadaj_pola_statusu(status_bar)

        # main
        self.window.mainloop()

    klient_header = ['id', 'Imię, nazwisko', 'Miejscowość', "Ulica", 'emai', 'telefon']

    def handleClick(app):
        print('handleClick')

    def handleRightClick(self, event):
        focused = self.tree.focus()
        if focused == "":
            item_state=tk.DISABLED
        else:
            item_state=tk.ACTIVE
        self.context_menu.entryconfigure("Edytuj", state=item_state)
        self.context_menu.post(event.x_root, event.y_root)

    def _build_tree(self):
        self.context_menu = tk.Menu(self.window, tearoff=0, )
        self.context_menu.add_command(label="Edytuj", command=self.edytuj_klient)
        self.context_menu.add_command(label="Option 2", command=self.handleClick)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Quit", command=self.window.quit)


        self.tree.bind("<Button-3>", self.handleRightClick)

        for col in self.klient_header:
            title = col.title()
            self.tree.heading(col, text=title)  # , command=lambda c=col: sortby(self.tree, c, 0))
            w = int(1.5 * tkFont.Font().measure(title))
            self.tree.column(col, width=w)

    def fill_list_klients(self, klients):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for item in klients:
            self.tree.insert('', 'end', values=item)
            for ix, val in enumerate(item):
                col_w = tkFont.Font().measure(val)
                if self.tree.column(self.klient_header[ix], width=None) < col_w:
                    self.tree.column(self.klient_header[ix], width=col_w)

    def aktywny_edytor(self):
        self.middle.grid_columnconfigure(0, weight=1)
        self.tree.grid_forget()
        self.editor1.grid(row=0, column=0, sticky=tk.NSEW)

    def aktywna_lista(self):
        self.middle.grid_columnconfigure(0, weight=1)
        self.editor1.grid_forget()
        self.tree.grid(row=0, column=0, sticky=tk.NSEW)

    def _dadaj_pola_statusu(self, frame):
        status_w = [(10, "w"), (5, "center"), (15, "w"), (25, "w")]
        idx = 1
        for w in status_w:
            panel = tk.Label(frame, text=idx, width=w[0], anchor=w[1], relief="sunken")
            panel.pack(side=tk.LEFT, padx=2)
            self.statusTab.append(panel)
            idx += 1

    def _dodaj_szybkie_buttony(self, bar):
        self.redbutton = tk.Button(bar, text="Wyczyść", fg="red", command=self.clear_btn_click)
        self.redbutton.pack(side=tk.LEFT, ipadx=0)

        greenbutton = tk.Button(bar, text="Green", fg="green", command=self._btn_cmd_green)
        greenbutton.pack(side=tk.LEFT, ipadx=0)

        KlientBnt = tk.Button(bar, text="Klient", fg="blue", command=self._btn_klient)
        KlientBnt.pack(side=tk.LEFT, ipadx=0)

        tk.Button(bar, text="Lista", fg="blue", command=self.lista_btn_click).pack(side=tk.LEFT, ipadx=2)
        tk.Button(bar, text="Edytor", fg="blue", command=self.edytor_btn_click).pack(side=tk.LEFT, ipadx=2)

    def _dodaj_glowne_menu(self, glowne_okno):
        menu_bar = tk.Menu(glowne_okno)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="New", command=self.make_active)
        file_menu.add_command(label="Open", command=self.make_deactive)
        file_menu.add_command(label="Save", command=self.do_nothing)
        file_menu.add_command(label="Save as...", command=self.do_nothing)
        file_menu.add_command(label="Close", command=self.do_nothing)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=glowne_okno.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

        # ----
        klient_menu = tk.Menu(menu_bar, tearoff=0)
        klient_menu.add_command(label="Nowy", command=self.dodaj_klient)
        klient_menu.add_command(label="Edytuj", command=self.edytuj_klient)
        menu_bar.add_cascade(label="Klient", menu=klient_menu)

        # ----
        edit_menu = tk.Menu(menu_bar, tearoff=0)
        edit_menu.add_command(label="Undo", command=self.do_nothing)
        edit_menu.add_separator()
        edit_menu.add_command(label="Cut", accelerator="F4", command=self.do_nothing)
        edit_menu.add_command(label="Copy", command=self.do_nothing)
        edit_menu.add_command(label="Paste", command=self.do_nothing)
        edit_menu.add_command(label="Delete", command=self.do_nothing)
        edit_menu.add_command(label="Select All", command=self.do_nothing)
        menu_bar.add_cascade(label="Edit", menu=edit_menu)
        # ----
        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="Help Index", command=self.do_nothing)
        help_menu.add_command(label="About...", command=self.do_nothing)
        menu_bar.add_cascade(label="Help", menu=help_menu)
        # ----
        glowne_okno.config(menu=menu_bar)

    def clear_editor(self):
        self.editor1.delete(1.0, tk.END)

    def add_editor(self, txt):
        self.editor1.insert(tk.INSERT, txt)

    def callback(*sv):
        app = sv[0]
        ev_val = app.event.get()
        if ev_val == KlientEntry.KlientForm.NEW_KLIENT:
            app.add_editor("Nowy klient\n")
            TeatrDB.add_klient(app.klient)
        if ev_val == KlientEntry.KlientForm.UPDATE_KLIENT:
            app.add_editor("poprawiony klient\n")

    def make_active(app):
        app.redbutton.config(state="active")

    def make_deactive(app):
        app.redbutton.config(state="disabled")

    def do_nothing(app):
        print(type(app))

    def clear_btn_click(app):
        app.clear_editor()
        # msize = app.editor1.count("1.0", tk.INSERT)
        # app.editor1.insert(tk.INSERT, f'Red Btn size = [{msize[0]}]\n')
        app.statusTab[0]["text"] = "RED"

    def _btn_cmd_green(app):
        app.add_editor(f'Green Btn {app.counter}\n')
        app.counter += 1
        app.statusTab[0]["text"] = "GREEN"
        print(type(app.add_editor))
        print(app.add_editor)
        app.test_fun(app.add_editor)

    def test_fun(self, print_fun):
        print_fun('To jest text\n')

    def _btn_klient(app):
        KlientEntry.KlientForm(app.window, app.event, app.klient, True)

    def dodaj_klient(app):
        KlientEntry.KlientForm(app.window, app.event, app.klient, True)

    def edytuj_klient(app):
        KlientEntry.KlientForm(app.window, app.event, app.klient, False)

    def lista_btn_click(app):
        app.aktywna_lista()
        klients = TeatrDB.load_klints()
        app.fill_list_klients(klients)

    def edytor_btn_click(app):
        app.aktywny_edytor()


# ---------------
TeatrApp()
