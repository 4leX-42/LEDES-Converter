<!--
[ES] Conversor LEDES 98BI: convierte facturas en PDF al formato LEDES 98BI de las plataformas de facturación legal. Local, sin internet.
[EN] LEDES 98BI Converter: turns PDF invoices into LEDES 98BI for e-billing platforms. Local, offline.
Contexto: usuario
Instalar: $f="$env:TEMP\LEDES98BI.exe"; [Net.ServicePointManager]::SecurityProtocol=3072; irm https://github.com/4leX-42/LEDES-Converter/releases/latest/download/Conversor.LEDES.98BI.exe -OutFile $f; explorer.exe "$f"
-->
# Conversor LEDES 98BI

Aplicación de escritorio para Windows (Python + tkinter, empaquetada en un `.exe` con PyInstaller) que
lee facturas en PDF, extrae cabecera y partidas, clasifica las partidas con códigos UTBMS y genera el
fichero **LEDES 98BI** (`LEDES98BI V5`) que piden las plataformas de facturación legal. Valida la
aritmética del formato antes de escribir. Todo local: no envía nada a internet.

Parte de [GADGETS-SUPPORT_CX](https://github.com/4leX-42/GADGETS-SUPPORT_CX), el catálogo de herramientas.

## Usar

Descargar `Conversor.LEDES.98BI.exe` de la [última release](https://github.com/4leX-42/LEDES-Converter/releases/latest)
y abrirlo (no necesita Python ni instalación). Arrastrar PDFs a la ventana, revisar y "Generar fichero".

## Compilar

```powershell
pip install -r requirements.txt pyinstaller
python assets\make_logo.py              # solo si cambia el logotipo
python -m PyInstaller build.spec --noconfirm
# -> dist\Conversor LEDES 98BI.exe
```

Manual completo (formato, cálculos, dónde escribe, configuración): [`LEEME.md`](LEEME.md).
