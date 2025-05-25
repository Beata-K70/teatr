import tkinter as tk


class BaseForm(tk.Toplevel):
    def __init__(self, parent, ilosc_elementow):
        super().__init__(parent)  # *args, **kwargs)

        self._set_center_position(parent)
        self.title('Klient')
        self.attributes('-topmost', 'true')
        #        self.resizable = False
        self.resizable(False, False)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.positionfrom()

        self._varTab = []
        for x in range(ilosc_elementow):
            self._varTab.append(tk.StringVar())

        self._create_widgets()

    def _create_widgets(self):
        middle = tk.Frame(self)  # , background='silver')
        middle.grid(row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)
        middle.grid_columnconfigure(0, weight=1)

        bottom_fr = tk.Frame(self)  # , background='yellow')
        bottom_fr.grid(row=1, column=0, padx=5, pady=5, columnspan=2, sticky=tk.NSEW)
        bottom_fr.grid_rowconfigure(0, weight=1)
        bottom_fr.grid_columnconfigure(0, weight=0)

        # ---
        self._add_edit_items(middle)

        # ---
        ok_btn = tk.Button(bottom_fr, text="OK", command=self._ok_btn_click)
        ok_btn.pack(side=tk.RIGHT, padx=5)
        anuluj_btn = tk.Button(bottom_fr, text="Anuluj", command=self._anuluj_btn_click)
        anuluj_btn.pack(side=tk.RIGHT, padx=5)
        clear_btn = tk.Button(bottom_fr, text="Wyczyść", command=self._clear_btn_click)
        clear_btn.pack(side=tk.RIGHT, padx=5)

    def _add_edit_item(self, parent, caption, var):
        item_fr = tk.Frame(parent)  # , background='blue')
        item_fr.grid(sticky=tk.EW)
        label = tk.Label(item_fr, text=caption + ':', width=14, anchor="e")
        label.pack(side=tk.LEFT, padx=5)
        entry = tk.Entry(item_fr, width=30, textvariable=var)
        entry.pack(side=tk.LEFT, padx=5)

    def _set_center_position(self, main_w):
        x = main_w.winfo_x()
        y = main_w.winfo_y()
        w = main_w.winfo_width()
        h = main_w.winfo_height()

        [form_w, form_h] = self._get_form_size();

        self.geometry("+%d+%d" % (x + (w - form_w) / 2, y + (h - form_h) / 2))
        self.geometry(f'{form_w}x{form_h}')

    def _add_edit_items(self, frame):
        pass

    def _get_form_size(self):
        pass

    def _anuluj_btn_click(self):
        self.destroy()

    def _clear_btn_click(self):
        pass

    def _ok_btn_click(self):
        pass
