import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

def load_data():
    # Load full data for languages and their variants
    json_path = os.path.join(os.path.dirname(__file__), "languages.json")
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

class LanguageViewerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Language Viewer")

        self.data = load_data()
        self.all_languages = list(self.data.keys())
        self.filtered_languages = self.all_languages[:]
        
        self.check_vars = {}    # language -> BooleanVar
        self.check_buttons = {} # language -> Checkbutton widget

        # Search bar frame
        search_frame = tk.Frame(master)
        search_frame.pack(padx=10, pady=10, fill="x")

        tk.Label(search_frame, text="Search:").pack(side="left")
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(search_frame, textvariable=self.search_var)
        self.search_entry.pack(side="left", fill="x", expand=True)
        self.search_entry.bind("<KeyRelease>", self.on_search_type)

        # Scrollable frame for languages
        container = tk.Frame(master)
        container.pack(fill="both", expand=True, padx=10, pady=10)

        self.canvas = tk.Canvas(container)
        self.canvas.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        scrollbar.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.check_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0,0), window=self.check_frame, anchor="nw")
        self.check_frame.bind("<Configure>", self.on_frame_configure)

        # Frame for selected languages and buttons at the bottom
        bottom_frame = tk.Frame(master)
        bottom_frame.pack(padx=10, pady=(0,10), fill="both")

        # A text widget to show selected languages nicely wrapped
        self.selected_text = tk.Text(bottom_frame, height=3, wrap="word")
        self.selected_text.pack(side="left", fill="both", expand=True)
        self.selected_text.insert("1.0", "Selected Languages: None")
        self.selected_text.config(state="disabled")

        # Proceed and Close buttons
        proceed_button = tk.Button(bottom_frame, text="Proceed", command=self.proceed_to_variants)
        proceed_button.pack(side="right", padx=(5,0))
        
        close_button = tk.Button(bottom_frame, text="Close", command=master.destroy)
        close_button.pack(side="right")

        # Create all checkboxes once
        self.create_checkboxes()
        self.update_display()

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def create_checkboxes(self):
        for language in self.all_languages:
            var = tk.BooleanVar(value=False)
            cb = tk.Checkbutton(self.check_frame, text=language, variable=var, anchor="w",
                                command=self.update_selected_text)
            self.check_vars[language] = var
            self.check_buttons[language] = cb

    def on_search_type(self, event):
        self.update_display()

    def update_display(self):
        # Filter based on search
        search_term = self.search_var.get().strip().lower()
        if search_term:
            self.filtered_languages = [lang for lang in self.all_languages if search_term in lang.lower()]
        else:
            self.filtered_languages = self.all_languages[:]

        # Hide all first
        for lang, cb in self.check_buttons.items():
            cb.pack_forget()

        # Show only filtered
        for language in self.filtered_languages:
            self.check_buttons[language].pack(fill="x", padx=5, pady=2)

        # Reset scroll to top
        self.canvas.yview_moveto(0.0)
        self.update_selected_text()

    def update_selected_text(self):
        # Show which languages are currently selected
        selected = [lang for lang, var in self.check_vars.items() if var.get()]
        self.selected_text.config(state="normal")
        self.selected_text.delete("1.0", "end")
        if selected:
            self.selected_text.insert("1.0", "Selected Languages: " + ", ".join(selected))
        else:
            self.selected_text.insert("1.0", "Selected Languages: None")
        self.selected_text.config(state="disabled")

    def proceed_to_variants(self):
        # Gather selected languages
        selected_langs = [lang for lang, var in self.check_vars.items() if var.get()]

        if not selected_langs:
            messagebox.showinfo("No Selection", "No languages selected to proceed.")
            return

        VariantSelectionWindow(self.master, self.data, selected_langs)


class VariantSelectionWindow:
    def __init__(self, parent, data, selected_langs):
        self.data = data
        self.selected_langs = selected_langs

        # Separate languages into single-variant and multi-variant
        self.single_variant_selected = {}
        self.multi_variant_langs = {}

        for lang in self.selected_langs:
            lang_variants = self.data[lang]  # Dictionary of region -> code
            if len(lang_variants) == 1:
                # single variant - automatically select it
                region, code = next(iter(lang_variants.items()))
                self.single_variant_selected[lang] = code
            else:
                # multiple variants - user chooses
                self.multi_variant_langs[lang] = lang_variants

        self.top = tk.Toplevel(parent)
        self.top.title("Select Variants")

        info_label = tk.Label(self.top, text="Select variants for each language:")
        info_label.pack(padx=10, pady=10)

        # If no multi-variant languages, save immediately and close
        if not self.multi_variant_langs:
            self.save_selection()
            messagebox.showinfo("Done", "All selected languages had only one variant. Selection saved.")
            self.top.destroy()
            return

        # Scrollable frame for multi-variants
        container = tk.Frame(self.top)
        container.pack(fill="both", expand=True, padx=10, pady=10)

        self.canvas = tk.Canvas(container)
        self.canvas.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        scrollbar.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.variant_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0,0), window=self.variant_frame, anchor="nw")
        self.variant_frame.bind("<Configure>", self.on_frame_configure)

        # lang -> (combobox, variant_map)
        self.variant_selection = {}

        for lang, lang_variants in self.multi_variant_langs.items():
            tk.Label(self.variant_frame, text=lang, font=("Arial", 10, "bold")).pack(anchor="w", pady=(5,2))

            lf = tk.Frame(self.variant_frame)
            lf.pack(fill="x", pady=(0,10))

            variant_map = {}
            for region, code in lang_variants.items():
                display_str = f"{region} ({code})" if region else code
                variant_map[display_str] = code

            cb_value = tk.StringVar()
            combo = ttk.Combobox(lf, textvariable=cb_value, state="readonly")
            combo['values'] = list(variant_map.keys())

            if combo['values']:
                cb_value.set(combo['values'][0])

            combo.pack(anchor="w", fill="x")
            self.variant_selection[lang] = (combo, variant_map)

        button_frame = tk.Frame(self.top)
        button_frame.pack(pady=10, anchor="e")

        save_button = tk.Button(button_frame, text="Save", command=self.save_selection)
        save_button.pack(side="left", padx=(0,5))

        confirm_button = tk.Button(button_frame, text="Confirm", command=self.confirm_selection)
        confirm_button.pack(side="left")

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def confirm_selection(self):
        # Just close after confirming
        self.top.destroy()

    def save_selection(self):
        # Gather selected variants from multi-variant languages
        final_selection = dict(self.single_variant_selected)  # start with single-variant languages
        for lang, (combo, variant_map) in self.variant_selection.items():
            selected_display = combo.get()
            if selected_display:
                code = variant_map[selected_display]
                final_selection[lang] = code

        save_path = os.path.join(os.path.dirname(__file__), "selected.json")

        # Remove the existing file if it exists
        if os.path.exists(save_path):
            os.remove(save_path)

        with open(save_path, "w", encoding="utf-8") as f:
            json.dump(final_selection, f, ensure_ascii=False, indent=4)

        messagebox.showinfo("Saved", f"Selected variants saved to {save_path}")


def launch_ui():
    root = tk.Tk()
    app = LanguageViewerApp(root)
    root.mainloop()

if __name__ == "__main__":
    launch_ui()
