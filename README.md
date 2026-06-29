# Erick Cruz — Portfolio

Portfolio pessoal de Erick Cruz, Senior Game Engineer na Wildlife Studios.  
Publicado via GitHub Pages em: **https://erickfecruz.github.io/GithubPages**

---

## Stack

| Camada | Tecnologia |
|--------|-----------|
| Output | `index.html` — HTML standalone, sem dependências de servidor |
| Dados | `content/*.json` — todo conteúdo editável em JSON |
| Build | `scripts/build.py` — gera o `index.html` a partir dos JSONs |
| Edição | `scripts/edit_*.py` — menus CLI interativos por seção |
| Launcher | `EDITAR.bat` / `COMPILAR.bat` — entrada rápida no Windows |

---

## Estrutura do projeto

```
GithubPages/
│
├── content/               # Dados do portfolio (edite aqui)
│   ├── hero.json          # Nome, título, links sociais
│   ├── about.json         # Bio, stats, empresa atual
│   ├── projects.json      # Projetos + specs de imagem
│   ├── skills.json        # Skill bars, ferramentas, conquistas
│   └── career.json        # Linha do tempo profissional
│
├── scripts/               # Build e edição de conteúdo
│   ├── build.py           # Gera index.html a partir dos JSONs
│   ├── menu.py            # Menu principal (chamado pelo EDITAR.bat)
│   ├── utils.py           # Funções compartilhadas (load/save, CLI helpers)
│   ├── edit_hero.py
│   ├── edit_about.py
│   ├── edit_projects.py
│   ├── edit_skills.py
│   └── edit_career.py
│
├── assets/img/projects/   # Imagens e GIFs dos projetos
│
├── index.html             # Portfolio gerado (não editar manualmente)
├── EDITAR.bat             # Duplo clique → editor interativo
├── COMPILAR.bat           # Duplo clique → regenera index.html
└── CLAUDE.md              # Instruções para o Claude Code
```

---

## Como editar o conteúdo

### Opção A — Interface interativa (recomendado para usuários não-técnicos)

Dê duplo clique em **`EDITAR.bat`** e siga o menu:

```
[1] Hero          — Nome, título, links sociais
[2] Sobre Mim     — Bio, stats, empresa atual
[3] Projetos      — Adicionar, editar, remover projetos
[4] Skills        — Barras de habilidade, ferramentas, conquistas
[5] Carreira      — Linha do tempo profissional
[6] Compilar      — Gera o HTML atualizado
```

### Opção B — Editar JSON diretamente

1. Abra o arquivo correspondente em `content/`
2. Edite os valores (mantenha a estrutura JSON)
3. Execute `COMPILAR.bat` para regenerar o `index.html`

### Compilar manualmente via terminal

```bash
cd C:\Users\erick\Documents\GithubPages
python scripts/build.py
```

---

## Adicionar um projeto novo

Adicione um objeto ao array `projects` em `content/projects.json`:

```json
{
  "id": "slug-unico",
  "title": "Nome do Projeto",
  "studio": "Nome do Estúdio",
  "period": "2024 → 2025",
  "category": "game",
  "section": "wildlife",
  "layout": "grid",
  "image": "assets/img/projects/arquivo.gif",
  "image_url_fallback": "https://url-oficial.com/imagem.jpg",
  "image_spec": "card_grid",
  "studio_label": "ESTÚDIO · ENGINE · TIPO",
  "description": "Descrição curta.",
  "bullets": ["Feature técnica 1", "Feature técnica 2"],
  "tags": ["C++", "Unity"],
  "tags_secondary": ["Mobile"],
  "link": "https://link-do-projeto.com"
}
```

**Valores válidos:**

| Campo | Valores |
|-------|---------|
| `category` | `game` / `data` / `web` — controla o filtro |
| `section` | `wildlife` / `previous` / `academic` / `data` / `web` — controla o grupo visual |
| `layout` | `featured` / `grid` / `wide` |
| `image_spec` | `card_featured` / `card_grid` / `card_wide` / `card_portrait` |

---

## Especificações de imagem

| Spec | Dimensão | Proporção | Estático | GIF | Uso |
|------|----------|-----------|----------|-----|-----|
| `card_featured` | 1100×520px | 16:9 | 2MB | 6MB | Card hero (War Machines) |
| `card_grid` | 640×360px | 16:9 | 1MB | 4MB | Grid de 2–3 colunas |
| `card_wide` | 400×260px | 3:2 | 800KB | 3MB | Card de largura total |
| `card_portrait` | 375×667px | 9:16 | 1MB | 4MB | Screenshots de mobile |

Salve os arquivos em `assets/img/projects/`. GIFs de gameplay em loop de 3–5 segundos são ideais para os cards.

---

## Publicar no GitHub Pages

```bash
git add .
git commit -m "update portfolio content"
git push
```

O GitHub Pages serve o `index.html` da branch principal automaticamente.

---

## Design system

```css
--bg:    #0c0b10   /* fundo principal */
--gold:  #c9a84c   /* cor de destaque */
--mono:  'JetBrains Mono'
--sans:  'Inter'
```

Fontes carregadas via Google Fonts. Sem dependências de framework — HTML/CSS/JS puro.

---

## Requisitos

- Python 3.8+ (para os scripts de build e edição)
- Nenhuma dependência externa — apenas biblioteca padrão
