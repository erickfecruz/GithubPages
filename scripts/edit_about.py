import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from utils import *

FILE = "about.json"

def show(d):
    print(f"\n  Nome       : {d.get('name', '')}")
    print("  BIO:")
    for i, p in enumerate(d["bio_paragraphs"], 1):
        print(f"    [{i}] {p[:80]}{'...' if len(p)>80 else ''}")
    print("\n  STATS:")
    for s in d["stats"]:
        print(f"    {s['value']:6}  →  {s['label']}")
    print(f"\n  Empresa atual : {d['current_company']}")
    print(f"  Cargo atual   : {d['current_role']}")
    print(f"  Skills princ. : {', '.join(d['skills_primary'])}")
    print(f"  Skills secund.: {', '.join(d['skills_secondary'])}")

def run():
    while True:
        d = load(FILE)
        header("ABOUT — Sobre Mim")
        show(d)
        print("\n  [1] Editar parágrafo de bio")
        print("  [2] Adicionar parágrafo de bio")
        print("  [3] Remover parágrafo de bio")
        print("  [4] Editar stats (anos de exp, jogos...)")
        print("  [5] Editar empresa e cargo atual")
        print("  [6] Editar skills principais")
        print("  [7] Editar skills secundárias")
        print("  [8] Editar nome completo")
        print("  [0] Voltar")
        op = input("\n  Opção: ").strip()

        if op == "0":
            break

        elif op == "1":
            for i, p in enumerate(d["bio_paragraphs"], 1):
                print(f"\n  [{i}] {p}")
            try:
                idx = int(ask("Qual parágrafo editar (número)")) - 1
                if 0 <= idx < len(d["bio_paragraphs"]):
                    print(f"\n  Atual: {d['bio_paragraphs'][idx]}")
                    novo = ask("Novo texto")
                    if novo:
                        d["bio_paragraphs"][idx] = novo
            except ValueError:
                print("  Número inválido.")

        elif op == "2":
            novo = ask("Texto do novo parágrafo")
            if novo:
                d["bio_paragraphs"].append(novo)

        elif op == "3":
            for i, p in enumerate(d["bio_paragraphs"], 1):
                print(f"  [{i}] {p[:70]}...")
            try:
                idx = int(ask("Qual remover")) - 1
                if 0 <= idx < len(d["bio_paragraphs"]) and confirm("Remover este parágrafo?"):
                    d["bio_paragraphs"].pop(idx)
            except ValueError:
                pass

        elif op == "4":
            for i, s in enumerate(d["stats"], 1):
                print(f"  [{i}] {s['value']} → {s['label']}")
            try:
                idx = int(ask("Qual stat editar")) - 1
                if 0 <= idx < len(d["stats"]):
                    d["stats"][idx]["value"] = ask("Novo valor (ex: 5+, MSc)", d["stats"][idx]["value"])
                    d["stats"][idx]["label"] = ask("Nova label (ex: ANOS EXP.)", d["stats"][idx]["label"])
            except ValueError:
                pass

        elif op == "5":
            d["current_company"] = ask("Empresa", d["current_company"])
            d["current_role"]    = ask("Cargo",   d["current_role"])
            d["current_location"]= ask("Local",   d.get("current_location",""))

        elif op == "6":
            print(f"  Atual: {', '.join(d['skills_primary'])}")
            items = ask_list("Digite as skills principais (uma por linha):")
            if items:
                d["skills_primary"] = items

        elif op == "7":
            print(f"  Atual: {', '.join(d['skills_secondary'])}")
            items = ask_list("Digite as skills secundárias (uma por linha):")
            if items:
                d["skills_secondary"] = items

        elif op == "8":
            d["name"] = ask("Nome completo", d.get("name", ""))

        else:
            continue

        save(FILE, d)
        pause()

if __name__ == "__main__":
    run()
