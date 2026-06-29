# CLAUDE.md — Instruções para Claude Code

Este arquivo é lido automaticamente pelo Claude Code ao trabalhar neste repositório.

## Identidade do projeto

Portfolio de **Erick Cruz** (Senior Game Engineer · Wildlife Studios).
Repositório: `C:\Users\erick\Documents\GithubPages`
GitHub Pages: https://erickfecruz.github.io/GithubPages

---

## Stack atual (pós-migração)

O portfolio **não usa mais Jekyll**. A stack atual é:

| Camada | Tecnologia |
|--------|-----------|
| Output | `portfolio-preview.html` — HTML standalone autocontido |
| Dados | `content/*.json` — toda informação editável em JSON |
| Build | `scripts/build.py` — gera `index.html` a partir dos JSON |
| Edição | `scripts/edit_*.py` — menus CLI para editar os JSON |
| Launcher | `EDITAR.bat` / `COMPILAR.bat` — executáveis Windows |

---

## Arquitetura de conteúdo

Toda informação do portfolio vive em `content/`:

| Arquivo | Seção | Campos principais |
|---------|-------|-------------------|
| `hero.json` | Cabeçalho / Hero | name, eyebrow, subtitle, location, email, github, cta_* |
| `about.json` | Sobre Mim | bio_paragraphs[], stats[], current_company, current_role, skills_primary[], skills_secondary[] |
| `projects.json` | Projetos | projects[] com id, title, studio, category, layout, image, description, bullets[], tags[], + `_image_specs` |
| `skills.json` | Habilidades | primary_skills[], secondary_skills[], tools[], achievements[] |
| `career.json` | Carreira | entries[] com role, company, period, location, active, description, tags[] |

---

## Scripts disponíveis

### Edição de conteúdo

```
scripts/utils.py          — funções compartilhadas (load/save JSON, menus CLI)
scripts/menu.py           — menu principal (chama todos os edit_*)
scripts/edit_hero.py      — editar hero section
scripts/edit_about.py     — editar about section
scripts/edit_projects.py  — CRUD de projetos (com info de specs de imagem)
scripts/edit_skills.py    — editar skill bars, tools, achievements
scripts/edit_career.py    — CRUD da linha do tempo de carreira
```

### Build

```
scripts/build.py          — lê todos os content/*.json e gera portfolio-preview.html
```

### Executáveis Windows (duplo clique)

```
EDITAR.bat    — abre menu interativo de edição
COMPILAR.bat  — roda build.py e gera o HTML
```

---

## Como usar os scripts ao ajudar o usuário

**Para editar dados do portfolio**, sempre modifique os arquivos `content/*.json` diretamente via Edit/Write — não edite o HTML gerado.

**Após editar qualquer JSON**, rodar o build regenera o HTML:
```powershell
cd C:\Users\erick\Documents\GithubPages
python scripts\build.py
```

**Para adicionar um novo projeto**, edite `content/projects.json` e adicione um objeto ao array `projects` seguindo esta estrutura:
```json
{
  "id": "slug-do-projeto",
  "title": "Título do Projeto",
  "studio": "Nome do Estúdio",
  "period": "2024 → 2025",
  "category": "game",
  "layout": "grid",
  "image": "assets/img/projects/arquivo.jpg",
  "image_url_fallback": "https://url-de-fallback.com/img.jpg",
  "image_spec": "card_grid",
  "studio_label": "ESTÚDIO · ENGINE · TIPO",
  "description": "Descrição curta do projeto.",
  "bullets": ["Feature técnica 1", "Feature técnica 2"],
  "tags": ["C++", "Unity"],
  "tags_secondary": ["Mobile", "AAA"],
  "link": ""
}
```

**Valores válidos para campos enum:**
- `category`: `"game"` | `"data"` | `"web"` — controla o **filtro** da barra de filtros
- `section`: `"wildlife"` | `"previous"` | `"academic"` | `"data"` | `"web"` — controla o **agrupamento visual** na página
- `layout`: `"featured"` | `"grid"` | `"wide"`
- `image_spec`: `"card_featured"` | `"card_grid"` | `"card_wide"` | `"card_portrait"`

---

## Especificações de imagem

Definidas em `content/projects.json` no campo `_image_specs`:

| Spec | Tamanho | Proporção | Estático | GIF |
|------|---------|-----------|----------|-----|
| `card_featured` | 1100×520px | 16:9 | até 2MB | até 6MB |
| `card_grid` | 640×360px | 16:9 | até 1MB | até 4MB |
| `card_wide` | 400×260px | 3:2 | até 800KB | até 3MB |
| `card_portrait` | 375×667px | 9:16 | até 1MB | até 4MB |

Imagens locais ficam em `assets/img/projects/`. Sempre definir `image_url_fallback` com uma URL pública oficial quando disponível.

---

## Design system

```css
--bg:    #0c0b10   /* fundo principal */
--gold:  #c9a84c   /* cor de destaque */
--mono:  'JetBrains Mono'
--sans:  'Inter'
```

O HTML usa CSS custom properties — ao sugerir mudanças visuais, usar sempre essas variáveis.

---

## O que NÃO fazer

- Não editar `index.html` diretamente — ele é gerado pelo `build.py`
- Não usar o Jekyll/Gulp stack antigo — está obsoleto neste projeto
- Não clonar repos dentro do OneDrive (`C:\Users\erick\OneDrive`) — usar sempre `C:\Users\erick\Documents`
