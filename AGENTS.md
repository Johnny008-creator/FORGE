# 🤖 Forge AI Agent Protocol (v1.0)

Toto jsou závazná pravidla pro vývoj a úpravy projektu Forge. Každý AI agent se jimi musí řídit.

## 🏗️ Architektonické zásady
- **Single Responsibility Principle (SRP):** Každý soubor má jednu jasnou zodpovědnost.
- **Limit délky:** Žádný soubor nesmí překročit **200 řádků**.
- **Cirkulární importy:** Jsou přísně zakázány. Závislosti musí proudit směrem dolů.
- **Surgical Edits:** Nepoužívej hromadné přepisy. Používej `replace` pro cílené změny.

## 🛠️ Jak přidat nový Nástroj (Tool)
1. Vytvoř nový soubor v `tools/` (např. `tools/my_tool.py`).
2. Implementuj funkci nástroje.
3. Zaregistruj nástroj v `tools/registry.py` (importuj ho a přidej do `TOOLS` dict).
4. **POZOR:** Registrace probíhá VÝHRADNĚ v `tools/registry.py`.

## 📡 Jak přidat nového Providera (Model Provider)
1. Vytvoř nový soubor v `providers/` (např. `providers/openai.py`).
2. Implementuj třídu dědící z `BaseProvider`.
3. Zaregistruj providera v `providers/registry.py`.

## 📁 Adresářová struktura
- `core/`: Jádro agenta a loopu.
- `providers/`: Abstrakce pro různé AI backendy.
- `tools/`: Modulární nástroje (vždy jeden soubor = jedna kategorie).
- `tiers/`: Specifické konfigurace pro různé velikosti modelů.
- `ui/`: Vše spojené s Rich UI a interakcí s uživatelem.
- `utils/`: Pomocné funkce a statistiky.
- `config/`: Nastavení a validace.
- `plugins/`: Hook systém pro rozšíření.

## 🔬 Testování
Každý nový kód musí mít odpovídající test v `tests/`. Před dokončením úkolu ověř integritu pomocí `pytest`.
