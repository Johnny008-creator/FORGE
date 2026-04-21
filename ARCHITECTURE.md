# 🏗️ Forge Architecture (v1.0)

Tento dokument popisuje modulární strukturu projektu Forge a pravidla pro jeho rozšiřování.

## 📁 Přehled vrstev

### 1. Entry Point (`forge.py`)
- Nejvyšší vrstva, orchestrátor.
- Zpracovává CLI argumenty a slash příkazy.
- Inicializuje UI, Providery a spouští agentic loop.

### 2. Core (`core/`)
- **`agent.py`**: Exportní rozhraní pro jádro.
- **`loop.py`**: Samotný agentic loop (Brain). Rozhoduje o dalším kroku.
- **`context.py`**: Správa historie konverzace a trimování kontextu.
- **`parser.py`**: Extrakce a oprava JSON volání z výstupu modelu.

### 3. Providers (`providers/`)
- Abstrakční vrstva pro AI backendy.
- Každý provider dědí z `BaseProvider`.
- Podporuje auto-discovery (detekci běžících služeb).

### 4. Tools (`tools/`)
- Atomické funkce, které může agent volat.
- Každý soubor (`file.py`, `shell.py`, `search.py`, `ask.py`) představuje kategorii nástrojů.
- Registrace probíhá v `registry.py`.

### 5. Tiers (`tiers/`)
- Konfigurace modelů podle velikosti (Tiny, Small, Medium, Large).
- Každý Tier má vlastní limity kontextu a systémový prompt.

### 6. UI (`ui/`)
- Vše spojené s Rich UI.
- Oddělená témata (`themes.py`), výstupy (`display.py`) a vstupy (`input.py`).

### 7. Config (`config/`)
- Správa nastavení (`settings.py`) a validace prostředí (`validator.py`).

## 📊 Diagram závislostí (Import Flow)

```text
forge.py ──▶ core/agent.py ──▶ core/loop.py
  │               │              │
  ▼               ▼              ▼
config/        tiers/         providers/
settings.py    manager.py     base.py
  │               │              │
  ▼               ▼              ▼
utils/         ui/            tools/
counter.py     display.py     executor.py
```

## 📜 Pravidla pro přispívání
- **Žádné cirkulární importy:** Sledujte diagram výše.
- **SRP:** Každá funkce dělá jednu věc.
- **Limity:** Soubor max 200 řádků.
- **Chirurgické úpravy:** Měňte jen to, co je nezbytné.
- **Testy:** Každý nový nástroj nebo provider musí mít test v `tests/`.
