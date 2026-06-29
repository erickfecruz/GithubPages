import sys, shutil
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from utils import *

FILE   = "projects.json"
ASSETS = ROOT / "assets" / "img" / "projects"

CATEGORIES = {"game": "Game Dev", "data": "Data Science", "web": "Web"}
LAYOUTS    = {"featured": "Destaque (grande)", "grid": "Grade (3 colunas)", "wide": "Largo (linha inteira)"}

def list_projects(projects, filtro=None):
    print()
    for i, p in enumerate(projects, 1):
        if filtro and p["category"] != filtro:
            continue
        studio = p.get("studio","")
        print(f"  [{i:02}] {p['title']:35} {studio:20} [{p['category']}] [{p['layout']}]")

def show_project(p, specs):
    spec_key = p.get("image_spec","card_grid")
    print(f"\n  Título      : {p['title']}")
    print(f"  Studio      : {p['studio']}")
    print(f"  Período     : {p['period']}")
    print(f"  Categoria   : {p['category']}")
    print(f"  Layout      : {p['layout']}")
    print(f"  Imagem local: {p['image']}")
    print(f"  Imagem URL  : {p.get('image_url_fallback','')}")
    print(f"  Descrição   : {p['description'][:80]}{'...' if len(p['description'])>80 else ''}")
    print(f"  Tags        : {', '.join(p['tags'])}")
    if p["bullets"]:
        print(f"  Bullets     : {len(p['bullets'])} itens")
    print(image_spec_info(spec_key, specs))

def run():
    while True:
        data     = load(FILE)
        projects = data["projects"]
        specs    = data.get("_image_specs", {})

        header("PROJETOS")
        list_projects(projects)
        print("\n  [A] Adicionar projeto")
        print("  [E] Editar projeto")
        print("  [R] Remover projeto")
        print("  [M] Mover projeto (reordenar)")
        print("  [I] Ver especificações de imagem")
        print("  [0] Voltar")
        op = input("\n  Opção: ").strip().upper()

        if op == "0":
            break

        elif op == "A":
            header("PROJETOS — Adicionar")
            novo = {
                "id":                ask("ID único (ex: meu-jogo, sem espaços)"),
                "title":             ask("Título"),
                "studio":            ask("Estúdio / Empresa"),
                "period":            ask("Período (ex: 2023 → 2024)"),
                "category":          ["game","data","web"][pick(["Game Dev","Data Science","Web"], "Categoria")],
                "layout":            ["featured","grid","wide"][pick(["Destaque (grande)","Grade (3 colunas)","Largo (linha inteira)"], "Layout")],
                "image":             ask("Caminho da imagem local (ex: assets/img/projects/myjogo.jpg)"),
                "image_url_fallback":ask("URL de fallback (deixe vazio se não tiver)", ""),
                "image_spec":        ["card_featured","card_grid","card_wide","card_portrait"][pick(["Destaque grande","Grade 3 colunas","Largo","Retrato mobile"], "Spec da imagem")],
                "studio_label":      ask("Label do card (STUDIO · ENGINE · TIPO)"),
                "description":       ask("Descrição curta"),
                "bullets":           ask_list("Bullets técnicos (Enter vazio para pular):"),
                "tags":              [t.strip() for t in ask("Tags principais (separadas por vírgula)").split(",") if t.strip()],
                "tags_secondary":    [t.strip() for t in ask("Tags secundárias (separadas por vírgula)", "").split(",") if t.strip()],
                "link":              ask("Link do projeto", "")
            }
            if novo["id"] and novo["title"]:
                projects.append(novo)
                save(FILE, data)
            pause()

        elif op == "E":
            list_projects(projects)
            try:
                idx = int(ask("Número do projeto")) - 1
                if not (0 <= idx < len(projects)):
                    continue
                p = projects[idx]
                header(f"EDITAR — {p['title']}")
                show_project(p, specs)
                print("\n  O que editar?")
                print("  [1] Título         [2] Studio        [3] Período")
                print("  [4] Categoria      [5] Layout        [6] Descrição")
                print("  [7] Imagem local   [8] URL fallback  [9] Tags")
                print("  [B] Bullets        [L] Link          [S] Studio label")
                sub = input("\n  Opção: ").strip().upper()
                if sub == "1": p["title"]             = ask("Título", p["title"])
                elif sub == "2": p["studio"]          = ask("Studio", p["studio"])
                elif sub == "3": p["period"]          = ask("Período", p["period"])
                elif sub == "4": p["category"]        = ["game","data","web"][pick(["Game Dev","Data Science","Web"],"Categoria")]
                elif sub == "5": p["layout"]          = ["featured","grid","wide"][pick(["Destaque","Grade","Largo"],"Layout")]
                elif sub == "6": p["description"]     = ask("Descrição", p["description"])
                elif sub == "7":
                    spec_key = p.get("image_spec","card_grid")
                    print(image_spec_info(spec_key, specs))
                    novo_img = ask("Caminho da imagem (assets/img/projects/...)", p["image"])
                    p["image"] = novo_img
                elif sub == "8": p["image_url_fallback"] = ask("URL fallback", p.get("image_url_fallback",""))
                elif sub == "9":
                    p["tags"]           = [t.strip() for t in ask("Tags principais", ", ".join(p["tags"])).split(",") if t.strip()]
                    p["tags_secondary"] = [t.strip() for t in ask("Tags secundárias", ", ".join(p.get("tags_secondary",[]))).split(",") if t.strip()]
                elif sub == "B":
                    print("  Bullets atuais:")
                    for i,b in enumerate(p["bullets"],1): print(f"    [{i}] {b}")
                    p["bullets"] = ask_list("Novos bullets (Enter vazio para terminar):")
                elif sub == "L": p["link"]       = ask("Link", p.get("link",""))
                elif sub == "S": p["studio_label"]= ask("Studio label", p.get("studio_label",""))
                save(FILE, data)
            except (ValueError, IndexError):
                print("  Número inválido.")
            pause()

        elif op == "R":
            list_projects(projects)
            try:
                idx = int(ask("Número do projeto para REMOVER")) - 1
                if 0 <= idx < len(projects):
                    p = projects[idx]
                    if confirm(f"Remover '{p['title']}'?"):
                        projects.pop(idx)
                        save(FILE, data)
                        print(f"  Removido: {p['title']}")
            except ValueError:
                pass
            pause()

        elif op == "M":
            list_projects(projects)
            try:
                idx = int(ask("Número do projeto")) - 1
                novo_pos = int(ask(f"Nova posição (1 a {len(projects)})")) - 1
                if 0 <= idx < len(projects) and 0 <= novo_pos < len(projects):
                    p = projects.pop(idx)
                    projects.insert(novo_pos, p)
                    save(FILE, data)
                    print(f"  '{p['title']}' movido para posição {novo_pos+1}")
            except ValueError:
                pass
            pause()

        elif op == "I":
            header("ESPECIFICAÇÕES DE IMAGEM")
            for key, s in specs.items():
                if key.startswith("_"):
                    continue
                print(f"\n  {key.upper()}")
                print(f"    Dimensões : {s['width_px']} x {s['height_px']} px")
                print(f"    Proporção : {s['ratio']}")
                print(f"    Estático  : até {s['max_size_static']}")
                print(f"    GIF       : até {s['max_size_gif']}")
                print(f"    Dica      : {s['notes']}")
            pause()

if __name__ == "__main__":
    run()
