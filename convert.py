import subprocess

def main():
    # Chemin vers le script Python
    script_path = "main_interface.py"

    # Lancer le script en arrière-plan
    subprocess.Popen(["python", script_path], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

if __name__ == "__main__":
    main()
