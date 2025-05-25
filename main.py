import tkinter as tk
import KlientEntry
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
        self._doda_glowne_menu(self.window)

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
        self.middle.grid_columnconfigure(0, weight=1)

        self.editor1 = tk.Text(self.middle, bg='white')
        self.editor1.grid(row=0, column=0, sticky=tk.NSEW)
        self.listBox = tk.Listbox(self.middle, bg='green')
        listbox = self.listBox
        listbox.insert(1, "frytki")
        listbox.insert(2, "sledziki")
        listbox.insert(3, "obwarzanki")

        # --- StatusBar -------
        status_bar = tk.Frame(self.window)  # , background='yellow')
        status_bar.grid(row=2, column=0, padx=5, pady=2, columnspan=1, sticky=tk.NSEW)
        status_bar.grid_rowconfigure(0, weight=1)
        status_bar.grid_columnconfigure(0, weight=1)
        self._dadaj_pola_statusu(status_bar)

        # main
        self.window.mainloop()

    def _dadaj_pola_statusu(self, frame):
        status_w = [(10, "w"), (5, "center"), (15, "w"), (20, "w")]
        idx = 1
        for w in status_w:
            panel = tk.Label(frame, text=idx, width=w[0], anchor=w[1], relief="sunken")
            panel.pack(side=tk.LEFT, padx=2)
            self.statusTab.append(panel)
            idx += 1

    def _dodaj_szybkie_buttony(self, bar):
        self.redbutton = tk.Button(bar, text="Red", fg="red", command=self.redbtn_onclick)
        self.redbutton.pack(side=tk.LEFT, ipadx=0)

        greenbutton = tk.Button(bar, text="Green", fg="green", command=self._btn_cmd_green)
        greenbutton.pack(side=tk.LEFT, ipadx=0)

        KlientBnt = tk.Button(bar, text="Klient", fg="blue", command=self._btn_klient)
        KlientBnt.pack(side=tk.LEFT, ipadx=0)

        tk.Button(bar, text="Lista", fg="blue", command=self.lista_btn_click).pack(side=tk.LEFT, ipadx=2)
        tk.Button(bar, text="Edytor", fg="blue", command=self.edytor_btn_click).pack(side=tk.LEFT, ipadx=2)

    def _doda_glowne_menu(self, glowne_okno):
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

    def callback(*sv):
        app = sv[0]
        if app.event == KlientEntry.KlientForm.NEW_KLIENT:
            app.editor1.insert(tk.INSERT, "Nowy klient\n")
            pass
        if app.event == KlientEntry.KlientForm.UPDATE_KLIENT:
            app.editor1.insert(tk.INSERT, "poprawiony klient\n")
            pass

    def make_active(app):
        app.redbutton.config(state="active")

    def make_deactive(app):
        app.redbutton.config(state="disabled")

    def do_nothing(app):
        print(type(app))

    def redbtn_onclick(app):
        msize = app.editor1.count("1.0", tk.INSERT)
        app.editor1.insert(tk.INSERT, f'Red Btn size = [{msize[0]}]\n')
        app.statusTab[0]["text"] = "RED"

    def _btn_cmd_green(app):
        app.editor1.insert(tk.INSERT, f'Green Btn {app.counter}\n')
        app.counter += 1
        app.statusTab[0]["text"] = "GREEN"

    def _btn_klient(app):
        KlientEntry.KlientForm(app.window, app.event, app.klient)

    def lista_btn_click(app):
        app.editor1.grid_forget()
        app.listBox.grid(row=0, column=0, sticky=tk.NSEW)

    def edytor_btn_click(app):
        app.editor1.grid(row=0, column=0, sticky=tk.NSEW)
        app.listBox.grid_forget()


# ---------------
TeatrApp()
