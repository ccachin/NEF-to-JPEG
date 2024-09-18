import glob
import rawpy
import imageio
import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox

def select_directory():
    directory = filedialog.askdirectory()
    if directory:
        directory_entry.delete(0, tk.END)
        directory_entry.insert(0, directory)

def convert_files():
    directory = directory_entry.get().strip()
    if not os.path.isdir(directory):
        messagebox.showerror("Erreur", "Le répertoire fourni n'existe pas.")
        return

    paths = glob.glob(os.path.join(directory, '*.[nN][eE][fF]'))
    count = 0
    number_files = len(paths)
    
    if number_files == 0:
        messagebox.showinfo("Information", "Aucune image trouvée. Vérifiez que les fichiers .nef ou .NEF sont dans le répertoire fourni.")
        return

    nef_folder = os.path.join(directory, 'NEF')
    jpeg_folder = os.path.join(directory, 'JPEG')
    os.makedirs(nef_folder, exist_ok=True)
    os.makedirs(jpeg_folder, exist_ok=True)

    for path in paths:
        if os.path.exists(path):
            try:
                shutil.move(path, os.path.join(nef_folder, os.path.basename(path)))
                print(f"Fichier déplacé: {path}")
            except Exception as e:
                print(f"Erreur lors du déplacement de {path}: {e}")
        else:
            print(f"Fichier introuvable avant déplacement: {path}")

    for path in glob.glob(os.path.join(nef_folder, '*.[nN][eE][fF]')):
        if os.path.exists(path):
            try:
                with rawpy.imread(path) as raw:
                    rgb = raw.postprocess()
                    jpg_path = os.path.join(jpeg_folder, os.path.splitext(os.path.basename(path))[0] + '.jpg')
                    imageio.imwrite(jpg_path, rgb)
                    count += 1
                    print(f"{count} / {number_files} - Fichier converti: {jpg_path}")
            except Exception as e:
                print(f"Erreur lors de la conversion de {path} en jpg: {e}")
        else:
            print(f"Fichier introuvable avant conversion: {path}")

    messagebox.showinfo("Information", f"Les fichiers .nef et .NEF ont été déplacés dans le dossier 'NEF' et les fichiers JPG ont été enregistrés dans le dossier 'JPEG'.")

# Création de la fenêtre principale
root = tk.Tk()
root.title("NEF to JPEG Converter")

# Champ pour afficher le chemin du répertoire
directory_label = tk.Label(root, text="Répertoire des images NEF:")
directory_label.pack(pady=5)

directory_entry = tk.Entry(root, width=50)
directory_entry.pack(pady=5)

# Bouton pour sélectionner le répertoire
browse_button = tk.Button(root, text="Parcourir", command=select_directory)
browse_button.pack(pady=5)

# Bouton pour démarrer la conversion
convert_button = tk.Button(root, text="Convertir", command=convert_files)
convert_button.pack(pady=20)

# Démarrer la boucle principale de Tkinter
root.mainloop()
