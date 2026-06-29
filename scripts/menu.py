"""
menu.py — Menu principal para edição do portfolio
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from utils import *

import edit_hero
import edit_about
import edit_projects
import edit_skills
import edit_career
import build

def run():
    while True:
        header("MENU PRINCIPAL")
        print("""
  Escolha o que deseja editar:

  [1] Hero          — Nome, título, links sociais
  [2] Sobre Mim     — Bio, stats, empresa atual
  [3] Projetos      — Adicionar, editar, remover projetos
  [4] Skills        — Barras de habilidade, ferramentas, conquistas
  [5] Carreira      — Linha do tempo profissional

  [6] Compilar portfolio   — Gera o HTML a partir dos dados
  [0] Sair
""")
        op = input("  Opção: ").strip()

        if op == "0":
            header("SAINDO")
            print("  Até logo!\n")
            break
        elif op == "1":
            edit_hero.run()
        elif op == "2":
            edit_about.run()
        elif op == "3":
            edit_projects.run()
        elif op == "4":
            edit_skills.run()
        elif op == "5":
            edit_career.run()
        elif op == "6":
            header("COMPILANDO PORTFOLIO")
            build.build()
            pause()
        else:
            print("  Opção inválida.")

if __name__ == "__main__":
    run()
