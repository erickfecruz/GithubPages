import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from utils import *

FILE = "career.json"

def show(d):
    print()
    for i, e in enumerate(d["entries"], 1):
        ativo = " ◄ ATUAL" if e.get("active") else ""
        print(f"  [{i}] {e['period']:20} {e['role']:35} {e['company']}{ativo}")

def show_entry(e):
    print(f"\n  Cargo     : {e['role']}")
    print(f"  Empresa   : {e['company']}")
    print(f"  Período   : {e['period']}")
    print(f"  Local     : {e['location']}")
    print(f"  Atual     : {'Sim' if e.get('active') else 'Não'}")
    print(f"  Descrição : {e['description'][:80]}{'...' if len(e['description'])>80 else ''}")
    print(f"  Tags      : {', '.join(e['tags'])}")

def run():
    while True:
        d = load(FILE)
        header("CARREIRA — Linha do Tempo")
        show(d)
        print("\n  [A] Adicionar entrada")
        print("  [E] Editar entrada")
        print("  [R] Remover entrada")
        print("  [M] Mover (reordenar)")
        print("  [0] Voltar")
        op = input("\n  Opção: ").strip().upper()

        if op == "0":
            break

        elif op == "A":
            header("CARREIRA — Adicionar")
            nova = {
                "role":        ask("Cargo (ex: Senior Game Engineer)"),
                "company":     ask("Empresa (ex: Wildlife Studios)"),
                "period":      ask("Período (ex: 2021 → Present)"),
                "location":    ask("Local (ex: São Paulo, Brasil)", "São Paulo, Brasil"),
                "active":      confirm("É o cargo atual?"),
                "description": ask("Descrição resumida"),
                "tags":        [t.strip() for t in ask("Tags principais (vírgula)", "").split(",") if t.strip()],
                "tags_secondary": [t.strip() for t in ask("Tags secundárias (vírgula)", "").split(",") if t.strip()],
            }
            if nova["role"] and nova["company"]:
                d["entries"].insert(0, nova)
                save(FILE, d)
                print("  Entrada adicionada.")
            pause()

        elif op == "E":
            show(d)
            try:
                idx = int(ask("Número da entrada")) - 1
                if not (0 <= idx < len(d["entries"])):
                    continue
                e = d["entries"][idx]
                header(f"EDITAR — {e['role']} @ {e['company']}")
                show_entry(e)
                print("\n  [1] Cargo    [2] Empresa  [3] Período")
                print("  [4] Local    [5] Atual?   [6] Descrição")
                print("  [7] Tags     [8] Tags sec.")
                sub = input("\n  O que editar: ").strip()
                if sub == "1": e["role"]        = ask("Cargo", e["role"])
                elif sub == "2": e["company"]   = ask("Empresa", e["company"])
                elif sub == "3": e["period"]    = ask("Período", e["period"])
                elif sub == "4": e["location"]  = ask("Local", e["location"])
                elif sub == "5": e["active"]    = confirm("É o cargo atual?")
                elif sub == "6": e["description"] = ask("Descrição", e["description"])
                elif sub == "7": e["tags"]      = [t.strip() for t in ask("Tags", ", ".join(e["tags"])).split(",") if t.strip()]
                elif sub == "8": e["tags_secondary"] = [t.strip() for t in ask("Tags sec.", ", ".join(e.get("tags_secondary",[]))).split(",") if t.strip()]
                save(FILE, d)
            except (ValueError, IndexError):
                print("  Número inválido.")
            pause()

        elif op == "R":
            show(d)
            try:
                idx = int(ask("Número para REMOVER")) - 1
                if 0 <= idx < len(d["entries"]):
                    e = d["entries"][idx]
                    if confirm(f"Remover '{e['role']} @ {e['company']}'?"):
                        d["entries"].pop(idx)
                        save(FILE, d)
            except ValueError:
                pass
            pause()

        elif op == "M":
            show(d)
            try:
                idx = int(ask("Número da entrada")) - 1
                nova_pos = int(ask(f"Nova posição (1 a {len(d['entries'])})")) - 1
                if 0 <= idx < len(d["entries"]) and 0 <= nova_pos < len(d["entries"]):
                    e = d["entries"].pop(idx)
                    d["entries"].insert(nova_pos, e)
                    save(FILE, d)
                    print(f"  '{e['role']}' movido para posição {nova_pos+1}.")
            except ValueError:
                pass
            pause()

if __name__ == "__main__":
    run()
