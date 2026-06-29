import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from utils import *

FILE = "hero.json"

def show(d):
    print(f"\n  Nome       : {d['name']}")
    print(f"  Eyebrow    : {d['eyebrow']}")
    print(f"  Subtítulo  : {d['subtitle']}")
    print(f"  Localização: {d['location']}")
    print(f"  Email      : {d['email']}")
    print(f"  GitHub     : {d['github']}")
    print(f"  LinkedIn   : {d['cta_secondary_href']}")

def run():
    while True:
        d = load(FILE)
        header("HERO — Cabeçalho Principal")
        show(d)
        print("\n  [1] Editar nome")
        print("  [2] Editar eyebrow (linha acima do nome)")
        print("  [3] Editar subtítulo (C++, Unity3D...)")
        print("  [4] Editar localização")
        print("  [5] Editar email")
        print("  [6] Editar link do GitHub")
        print("  [7] Editar link do LinkedIn")
        print("  [0] Voltar")
        op = input("\n  Opção: ").strip()

        if op == "0":
            break
        elif op == "1":
            d["name"] = ask("Novo nome", d["name"])
        elif op == "2":
            d["eyebrow"] = ask("Novo eyebrow", d["eyebrow"])
        elif op == "3":
            d["subtitle"] = ask("Novo subtítulo", d["subtitle"])
        elif op == "4":
            d["location"] = ask("Nova localização", d["location"])
        elif op == "5":
            d["email"] = ask("Novo email", d["email"])
        elif op == "6":
            d["github"] = ask("Novo GitHub URL", d["github"])
        elif op == "7":
            d["cta_secondary_href"] = ask("Novo LinkedIn URL", d["cta_secondary_href"])
        else:
            continue

        save(FILE, d)
        pause()

if __name__ == "__main__":
    run()
