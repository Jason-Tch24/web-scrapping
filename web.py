import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from bs4 import BeautifulSoup
import pandas as pd
import requests

class WebScraperApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Web Scraper App")

        self.url_label = tk.Label(master, text="URL du site:")
        self.url_entry = tk.Entry(master, width=50)
        self.url_label.grid(row=0, column=0, sticky="e")
        self.url_entry.grid(row=0, column=1, columnspan=2)

        self.fetch_tables_button = tk.Button(master, text="Lister les tables", command=self.fetch_tables)
        self.fetch_tables_button.grid(row=1, column=0, columnspan=3, pady=10)

        self.tables_label = tk.Label(master, text="Tables disponibles:")
        self.tables_label.grid(row=2, column=0, sticky="e")

        self.tables_combobox = ttk.Combobox(master, state="readonly", width=30)
        self.tables_combobox.grid(row=2, column=1, columnspan=2)

        self.select_table_button = tk.Button(master, text="Sélectionner la table", command=self.select_table)
        self.select_table_button.grid(row=3, column=0, columnspan=3, pady=10)

        self.export_csv_button = tk.Button(master, text="Exporter en CSV", command=self.export_csv)
        self.export_csv_button.grid(row=4, column=0, columnspan=3, pady=10)

        self.selected_table_label = tk.Label(master, text="Table sélectionnée:")
        self.selected_table_label.grid(row=5, column=0, columnspan=3, pady=10)

        self.selected_table_text = tk.Text(master, wrap=tk.WORD, width=60, height=10)
        self.selected_table_text.grid(row=6, column=0, columnspan=3)

    def fetch_tables(self):
        url = self.url_entry.get()
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            tables = soup.find_all('table')
            table_names = [f"Table {i+1}" for i in range(len(tables))]
            self.tables_combobox['values'] = table_names
            messagebox.showinfo("Info", "Tables extraites avec succès!")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'extraction des tables : {str(e)}")

    def select_table(self):
        selected_table_index = self.tables_combobox.current()
        if selected_table_index >= 0:
            url = self.url_entry.get()
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            tables = soup.find_all('table')
            selected_table = tables[selected_table_index]
            table_title = f"Table {selected_table_index+1} - {self.get_table_title(selected_table)}"
            self.selected_table_label.config(text=table_title)
            self.display_table(selected_table)
        else:
            messagebox.showwarning("Avertissement", "Veuillez sélectionner une table.")

    def display_table(self, table):
        rows = table.find_all('tr')
        data = []
        for row in rows:
            cols = row.find_all(['th', 'td'])
            cols = [col.text.strip() for col in cols]
            data.append(cols)
        df = pd.DataFrame(data)
        self.selected_table_text.delete(1.0, tk.END)  # Efface le contenu précédent
        self.selected_table_text.insert(tk.END, df.to_string(index=False))

    def export_csv(self):
        selected_table_index = self.tables_combobox.current()
        if selected_table_index >= 0:
            url = self.url_entry.get()
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            tables = soup.find_all('table')
            selected_table = tables[selected_table_index]
            data = self.extract_table_data(selected_table)
            df = pd.DataFrame(data)
            file_path = f"Table_{selected_table_index+1}.csv"
            df.to_csv(file_path, index=False)
            messagebox.showinfo("Info", f"Table exportée avec succès en {file_path}")
        else:
            messagebox.showwarning("Avertissement", "Veuillez sélectionner une table.")

    def extract_table_data(self, table):
        rows = table.find_all('tr')
        data = []
        for row in rows:
            cols = row.find_all(['th', 'td'])
            cols = [col.text.strip() for col in cols]
            data.append(cols)
        return data

if __name__ == "__main__":
    root = tk.Tk()
    app = WebScraperApp(root)
    root.mainloop()
