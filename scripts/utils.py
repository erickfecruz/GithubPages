import json, os, sys, shutil
from pathlib import Path

ROOT   = Path(__file__).parent.parent
CONTENT = ROOT / "content"
ASSETS  = ROOT / "assets" / "img" / "projects"

def load(filename):
    p = CONTENT / filename
    with open(p, encoding="utf-8") as f:
        return json.load(f)

def save(filename, data):
    p = CONTENT / filename
    with open(p, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"\n  Salvo em {p.name}")

def cls():
    os.system("cls" if os.name == "nt" else "clear")

def header(title):
    cls()
    print("=" * 56)
    print(f"  ERICK CRUZ PORTFOLIO — {title}")
    print("=" * 56)

def pause():
    input("\n  [ Enter para continuar ] ")

def confirm(msg="Confirmar?"):
    r = input(f"\n  {msg} (s/n): ").strip().lower()
    return r in ("s", "sim", "y", "yes")

def ask(prompt, default=""):
    val = input(f"  {prompt}" + (f" [{default}]" if default else "") + ": ").strip()
    return val if val else default

def ask_list(prompt):
    print(f"  {prompt}")
    print("  (uma entrada por linha, linha vazia para terminar)")
    items = []
    while True:
        v = input("    > ").strip()
        if not v:
            break
        items.append(v)
    return items

def pick(options, prompt="Escolha"):
    for i, o in enumerate(options, 1):
        print(f"  [{i}] {o}")
    while True:
        try:
            n = int(input(f"\n  {prompt}: "))
            if 1 <= n <= len(options):
                return n - 1
        except ValueError:
            pass
        print("  Opção inválida.")

def image_spec_info(spec_key, specs):
    if spec_key not in specs:
        return ""
    s = specs[spec_key]
    return (
        f"\n  ┌─ TAMANHO IDEAL DA IMAGEM ({'GIF ou JPG/PNG'}) ──────────┐\n"
        f"  │  Dimensões : {s['width_px']} x {s['height_px']} px\n"
        f"  │  Proporção : {s['ratio']}\n"
        f"  │  Tamanho   : estático até {s['max_size_static']} · GIF até {s['max_size_gif']}\n"
        f"  │  Dica      : {s['notes']}\n"
        f"  └────────────────────────────────────────────────────┘"
    )
