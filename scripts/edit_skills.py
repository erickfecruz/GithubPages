import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from utils import *

FILE = "skills.json"

def show(d):
    print(f"\n  === {d['primary_group_label']} ===")
    for s in d["primary_skills"]:
        bar = "█" * (s["level"] // 10) + "░" * (10 - s["level"] // 10)
        print(f"  {s['name']:25} {bar}  {s['level']}")
    print(f"\n  === {d['secondary_group_label']} ===")
    for s in d["secondary_skills"]:
        bar = "█" * (s["level"] // 10) + "░" * (10 - s["level"] // 10)
        print(f"  {s['name']:25} {bar}  {s['level']}")
    print(f"\n  FERRAMENTAS: {', '.join(d['tools'])}")
    print(f"\n  CONQUISTAS:")
    for a in d["achievements"]:
        print(f"    · {a}")

def edit_skill_list(skills, label):
    while True:
        header(f"SKILLS — {label}")
        for i, s in enumerate(skills, 1):
            bar = "█" * (s["level"] // 10)
            print(f"  [{i}] {s['name']:25} {bar}  {s['level']}")
        print("\n  [A] Adicionar  [E] Editar  [R] Remover  [0] Voltar")
        op = input("\n  Opção: ").strip().upper()
        if op == "0":
            break
        elif op == "A":
            name  = ask("Nome da skill")
            level = int(ask("Nível (0 a 100)", "80"))
            label_val = ask("Label (ex: 80, EXPERT)", str(level))
            skills.append({"name": name, "level": level, "label": label_val})
        elif op == "E":
            try:
                idx = int(ask("Número")) - 1
                if 0 <= idx < len(skills):
                    skills[idx]["name"]  = ask("Nome", skills[idx]["name"])
                    skills[idx]["level"] = int(ask("Nível (0-100)", str(skills[idx]["level"])))
                    skills[idx]["label"] = ask("Label", skills[idx]["label"])
            except ValueError:
                pass
        elif op == "R":
            try:
                idx = int(ask("Número para remover")) - 1
                if 0 <= idx < len(skills) and confirm(f"Remover '{skills[idx]['name']}'?"):
                    skills.pop(idx)
            except ValueError:
                pass

def run():
    while True:
        d = load(FILE)
        header("SKILLS — Habilidades")
        show(d)
        print("\n  [1] Editar skills de Game Engineering")
        print("  [2] Editar skills de Outras Áreas")
        print("  [3] Editar ferramentas (Unity, Git...)")
        print("  [4] Editar conquistas (achievements)")
        print("  [0] Voltar")
        op = input("\n  Opção: ").strip()

        if op == "0":
            break
        elif op == "1":
            edit_skill_list(d["primary_skills"], d["primary_group_label"])
        elif op == "2":
            edit_skill_list(d["secondary_skills"], d["secondary_group_label"])
        elif op == "3":
            print(f"  Atual: {', '.join(d['tools'])}")
            items = ask_list("Ferramentas (uma por linha):")
            if items:
                d["tools"] = items
        elif op == "4":
            print("  Conquistas atuais:")
            for i, a in enumerate(d["achievements"], 1):
                print(f"    [{i}] {a}")
            print("\n  [A] Adicionar  [R] Remover  [Enter] Cancelar")
            sub = input("  Opção: ").strip().upper()
            if sub == "A":
                nova = ask("Nova conquista")
                if nova:
                    d["achievements"].append(nova)
            elif sub == "R":
                try:
                    idx = int(ask("Número para remover")) - 1
                    if 0 <= idx < len(d["achievements"]) and confirm("Remover?"):
                        d["achievements"].pop(idx)
                except ValueError:
                    pass
        else:
            continue

        save(FILE, d)
        pause()

if __name__ == "__main__":
    run()
