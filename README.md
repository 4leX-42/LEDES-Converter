<!--
[ES] Conversor LEDES 98BI: convierte facturas en PDF al formato LEDES 98BI de las plataformas de facturación legal. Local, sin internet.
[EN] LEDES 98BI Converter: turns PDF invoices into LEDES 98BI for e-billing platforms. Local, offline.
Contexto: usuario
Instalar: $f="$env:TEMP\LEDES98BI.exe"; [Net.ServicePointManager]::SecurityProtocol=3072; irm https://github.com/4leX-42/LEDES-Converter/releases/latest/download/Conversor.LEDES.98BI.exe -OutFile $f; explorer.exe "$f"
-->
<div align="center">

# Conversor LEDES 98BI

Facturas PDF a LEDES 98BI para plataformas de e-billing legal. Local, sin red.

![Windows](https://img.shields.io/badge/Windows-10%20%7C%2011-1f1f1f?style=flat-square) ![Python](https://img.shields.io/badge/Python-tkinter-1f1f1f?style=flat-square&logo=python&logoColor=white) ![LEDES](https://img.shields.io/badge/LEDES98BI-V5-c8a25a?style=flat-square)

<img src="assets/screenshot.png" width="760" alt="Conversor LEDES 98BI">

<sub>Parte de <a href="https://github.com/4leX-42/GADGETS-SUPPORT_CX">GADGETS-SUPPORT_CX</a></sub>

</div>

## <img src="https://api.iconify.design/lucide/download.svg?color=%238b949e" width="18" align="top"> Instalar

```powershell
$f="$env:TEMP\LEDES98BI.exe"; [Net.ServicePointManager]::SecurityProtocol=3072; irm https://github.com/4leX-42/LEDES-Converter/releases/latest/download/Conversor.LEDES.98BI.exe -OutFile $f; explorer.exe "$f"
```

Portable: sin Python ni instalación.

## <img src="https://api.iconify.design/lucide/receipt.svg?color=%238b949e" width="18" align="top"> Qué hace

| | |
|---|---|
| <img src="https://api.iconify.design/lucide/file-text.svg?color=%238b949e" width="18" align="top"> **Extrae** | Cabecera y partidas de cada factura PDF |
| <img src="https://api.iconify.design/lucide/tags.svg?color=%238b949e" width="18" align="top"> **Clasifica** | Partidas con códigos UTBMS |
| <img src="https://api.iconify.design/lucide/calculator.svg?color=%238b949e" width="18" align="top"> **Valida** | Aritmética del formato antes de escribir |
| <img src="https://api.iconify.design/lucide/file-spreadsheet.svg?color=%238b949e" width="18" align="top"> **Genera** | Fichero `LEDES98BI V5` |

Arrastrar PDFs, revisar y *Generar fichero*. Manual completo (formato, cálculos, configuración): [`LEEME.md`](LEEME.md).

<details>
<summary><img src="https://api.iconify.design/lucide/code-xml.svg?color=%238b949e" width="18" align="top"> <b>Compilar</b></summary>

```powershell
pip install -r requirements.txt pyinstaller
python assets\make_logo.py              # solo si cambia el logotipo
python -m PyInstaller build.spec --noconfirm
# -> dist\Conversor LEDES 98BI.exe
```
</details>
