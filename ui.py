"""
Tema y widgets base de la interfaz.

tkinter con el tema de PrintDeploy: carbon + dorado sobre blanco, cabecera y pie
en carbon, botones de esquinas cortadas, campos con linea inferior. Sin bordes de
sistema.
"""

from __future__ import annotations

import tkinter as tk
import tkinter.font as tkfont
from tkinter import ttk

# --- paleta: la de PrintDeploy (carbon + dorado sobre blanco) --------------
GOLD = "#C9A96E"            # acento sobre carbon
GOLD_DEEP = "#70541E"       # acento sobre blanco (texto, filetes)
ACCENT = GOLD_DEEP
ACCENT_HOVER = "#5A4318"
ACCENT_SOFT = "#F6F1E7"
ACCENT_LINE = "#D9C6A0"

INK = "#161618"             # carbon, no negro puro (legibilidad)
INK_BAR = "#161618"         # cabecera, pie y cabeceras de tabla
INK_LINE = "#38383C"

BG = "#FFFFFF"
SURFACE = "#FFFFFF"
HAIRLINE = "#DEDEDE"
HAIRLINE_STRONG = "#C4C4C8"
HOVER = "#F7F7F7"

TEXT = "#161618"
TEXT_SOFT = "#38383C"
TEXT_FAINT = "#7A7A80"
TEXT_ON_INK = "#F2F2F3"
TEXT_ON_INK_SOFT = "#B8B8BC"

#: estados. Se prescinde del verde: conforme se marca en carbon.
OK = "#161618"
WARN = "#8A5A00"
WARN_SOFT = "#FDF6EA"
BAD = "#C8102E"
RED_SOFT = "#FBEEF0"
GREEN = OK                  # compatibilidad con llamadas existentes


def mix(a: str, b: str, t: float) -> str:
    """Mezcla dos colores #RRGGBB (t=0 a, t=1 b)."""
    pa = [int(a[i:i + 2], 16) for i in (1, 3, 5)]
    pb = [int(b[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(x + (y - x) * t):02X}" for x, y in zip(pa, pb))


def is_dark(color: str) -> bool:
    try:
        r, g, b = (int(color[i:i + 2], 16) for i in (1, 3, 5))
    except (ValueError, TypeError, IndexError):
        return False
    return (r * 299 + g * 587 + b * 114) / 1000 < 90


def font_stack() -> tuple[str, str, str]:
    """(interfaz, monoespaciada, serif) disponibles en el sistema."""
    families = set(tkfont.families())
    ui = next((f for f in ("Segoe UI Variable Text", "Segoe UI", "Tahoma")
               if f in families), "TkDefaultFont")
    mono = next((f for f in ("Cascadia Mono", "Consolas", "Courier New")
                 if f in families), "TkFixedFont")
    # titulos en seminegrita, como PrintDeploy
    serif = next((f for f in ("Segoe UI Semibold", "Segoe UI") if f in families), ui)
    return ui, mono, serif


UI = "Segoe UI"
MONO = "Consolas"
SERIF = "Segoe UI Semibold"


def init_fonts() -> None:
    global UI, MONO, SERIF
    UI, MONO, SERIF = font_stack()


def f(size: int = 10, weight: str = "normal") -> tuple:
    return (UI, size, weight) if weight != "normal" else (UI, size)


def fs(size: int = 12, weight: str = "normal") -> tuple:
    """Fuente de titulos (seminegrita)."""
    return (SERIF, size, weight) if weight != "normal" else (SERIF, size)


def fm(size: int = 9) -> tuple:
    return (MONO, size)


# ---------------------------------------------------------------------------
def money(value, currency: str = "", *, decimals: int = 2) -> str:
    """Importe en formato español: 4.649,91 €.

    Solo para mostrar en pantalla. El fichero LEDES siempre lleva punto
    decimal y sin separador de millares (lo hace ledes98bi.fmt_decimal).
    """
    from decimal import Decimal, ROUND_HALF_UP

    if value is None or value == "":
        return ""
    d = value if isinstance(value, Decimal) else Decimal(str(value))
    d = d.quantize(Decimal(1).scaleb(-decimals), rounding=ROUND_HALF_UP)
    sign = "-" if d < 0 else ""
    whole, _, frac = f"{abs(d):.{decimals}f}".partition(".")
    groups = []
    while len(whole) > 3:
        groups.insert(0, whole[-3:])
        whole = whole[:-3]
    groups.insert(0, whole)
    out = sign + ".".join(groups) + ("," + frac if decimals else "")
    # solo el euro lleva simbolo; el resto, codigo ISO, que no admite confusion
    code = (currency or "").upper()
    if code == "EUR":
        return f"{out} €"
    return f"{out} {code}".strip()


def number(value, decimals: int = 2) -> str:
    """Cantidad en formato español, sin ceros decimales sobrantes: 1,5 / 4,25."""
    from decimal import Decimal

    if value is None or value == "":
        return ""
    text = money(value, decimals=decimals)
    if "," in text:
        text = text.rstrip("0").rstrip(",")
    return text or "0"


# ---------------------------------------------------------------------------
def round_rect(canvas: tk.Canvas, x1, y1, x2, y2, r, **kw):
    """Rectangulo de esquinas redondeadas como poligono suavizado."""
    r = min(r, abs(x2 - x1) / 2, abs(y2 - y1) / 2)
    points = [
        x1 + r, y1, x2 - r, y1, x2, y1, x2, y1 + r, x2, y2 - r, x2, y2,
        x2 - r, y2, x1 + r, y2, x1, y2, x1, y2 - r, x1, y1 + r, x1, y1,
    ]
    return canvas.create_polygon(points, smooth=True, splinesteps=24, **kw)


class Button(tk.Canvas):
    """Boton al estilo de PrintDeploy (Borderlands 2): esquinas opuestas cortadas,
    contorno grueso, sombreado plano en dos tonos y filete interior dorado. Al pasar
    el raton se rellena de dorado. Texto en mayusculas. Sobre fondo carbon pasa solo
    a la variante oscura (contorno y texto dorados)."""

    def __init__(self, master, text, command=None, *, kind="ghost",
                 width=None, height=36, icon="", pad=18, **kw):
        self.kind = kind
        self.text = text
        self.icon = icon
        self.command = command
        self._enabled = True

        bg = master.cget("bg")
        self._dark = is_dark(bg)
        font_ = f(9, "bold")
        probe = tkfont.Font(font=font_)
        label = self._caps(text)
        w = width or probe.measure(label) + pad * 2 + 6
        height = max(height, 34)

        super().__init__(master, width=w, height=height, bg=bg,
                         highlightthickness=0, bd=0, **kw)
        self._w_, self._h_ = w, height
        self._label = label
        self._font = font_
        self._draw(False)
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<Button-1>", self._on_click)
        self.configure(cursor="hand2")

    def _caps(self, text: str) -> str:
        label = f"{self.icon}  {text}".strip() if self.icon else text
        return label.upper()

    def _colors(self, hover: bool):
        """(relleno, contorno, texto, filete interior); "" = sin ese elemento."""
        if not self._enabled:
            if self._dark:
                return mix(INK, "#FFFFFF", .05), INK_LINE, mix(INK, "#FFFFFF", .32), ""
            return HOVER, HAIRLINE, HAIRLINE_STRONG, ""
        if self.kind == "quiet":
            if self._dark:
                return "", "", (GOLD if hover else TEXT_ON_INK_SOFT), ""
            return "", "", (GOLD_DEEP if hover else TEXT_SOFT), ""
        if self._dark or self.kind == "onink":
            return (GOLD if hover else INK), GOLD, (INK if hover else GOLD), \
                   ("" if hover else mix(INK, GOLD, .35))
        if self.kind in ("primary", "dark"):
            return (GOLD if hover else INK), INK, (INK if hover else "#FFFFFF"), \
                   mix(INK, GOLD, .2 if hover else .6)
        if self.kind == "danger":
            return (RED_SOFT if hover else SURFACE), BAD, BAD, ""
        return (INK if hover else SURFACE), INK, (GOLD if hover else TEXT), \
               (mix(INK, GOLD, .45) if hover else "")

    def _shape(self, i: float, h: float, c: float) -> list:
        """Contorno con la esquina superior izquierda y la inferior derecha cortadas."""
        w = self._w_ - 1
        return [c + i, i, w - i, i, w - i, h - c - i, w - c - i, h - i, i, h - i, i, c + i]

    def _draw(self, hover: bool):
        self.delete("all")
        fill, outline, fg, inner = self._colors(hover)
        w, h = self._w_ - 1, self._h_ - 1
        c = min(9, h / 3)
        if fill:
            # cel shading: toda la cara en el tono oscuro y encima la parte alta en el
            # tono base, con corte duro al 62 %
            self.create_polygon(self._shape(0, h, c),
                                fill=mix(fill, "#000000", .14 if self._enabled else .03), outline="")
            y = h * .62
            self.create_polygon([c, 0, w, 0, w, y, 0, y, 0, c], fill=fill, outline="")
        if inner:
            self.create_polygon(self._shape(4, h, c), fill="", outline=inner, width=1)
        if outline:
            self.create_polygon(self._shape(1, h, c), fill="", outline=outline,
                                width=2 if self._enabled else 1, joinstyle="miter")
        self.create_text(self._w_ / 2, self._h_ / 2, text=self._label,
                         fill=fg, font=self._font)

    def _on_enter(self, _e):
        if self._enabled:
            self._draw(True)

    def _on_leave(self, _e):
        self._draw(False)

    def _on_click(self, _e):
        if self._enabled and self.command:
            self.command()

    def set_enabled(self, value: bool):
        self._enabled = bool(value)
        self.configure(cursor="hand2" if value else "arrow")
        self._draw(False)

    def set_text(self, text: str):
        self.text = text
        self._label = self._caps(text)
        self._draw(False)


def section(master, text: str, *, bg: str = BG) -> tk.Frame:
    """Titulo de seccion como en PrintDeploy: mayusculas y un trazo dorado debajo."""
    box = tk.Frame(master, bg=bg)
    tk.Label(box, text=text.upper(), bg=bg, fg=TEXT, font=f(8, "bold")).pack(anchor="w")
    tk.Frame(box, bg=GOLD_DEEP, height=2, width=24).pack(anchor="w", pady=(4, 0))
    return box


def dark_titlebar(root: tk.Tk) -> None:
    """Barra de titulo de Windows en carbon (Windows 11; en 10 no hace nada)."""
    try:
        import ctypes
        root.update_idletasks()
        hwnd = ctypes.windll.user32.GetParent(root.winfo_id())
        dwm = ctypes.windll.dwmapi
        on = ctypes.c_int(1)
        dwm.DwmSetWindowAttribute(hwnd, 20, ctypes.byref(on), 4)          # modo oscuro
        caption = ctypes.c_int(0x00181616)                                 # INK en BGR
        dwm.DwmSetWindowAttribute(hwnd, 35, ctypes.byref(caption), 4)
        text = ctypes.c_int(0x00F3F2F2)
        dwm.DwmSetWindowAttribute(hwnd, 36, ctypes.byref(text), 4)
    except Exception:
        pass


class Card(tk.Frame):
    """Superficie blanca con borde de 1 px."""

    def __init__(self, master, **kw):
        pad = kw.pop("pad", 0)
        super().__init__(master, bg=HAIRLINE, **kw)
        self.inner = tk.Frame(self, bg=SURFACE, padx=pad, pady=pad)
        self.inner.pack(fill="both", expand=True, padx=1, pady=1)


class Field(tk.Frame):
    """Etiqueta encima, entrada plana debajo."""

    def __init__(self, master, label, var, *, width=22, hint="", bg=SURFACE,
                 values=None, on_change=None):
        super().__init__(master, bg=bg)
        tk.Label(self, text=label.upper(), bg=bg, fg=TEXT_SOFT,
                 font=f(7, "bold")).pack(anchor="w")
        # como PrintDeploy: sin caja, una linea debajo que se vuelve dorada al editar
        box = tk.Frame(self, bg=bg)
        box.pack(anchor="w", pady=(3, 0))
        self._line = tk.Frame(self, bg=HAIRLINE_STRONG, height=2)
        if values:
            self.widget = ttk.Combobox(box, textvariable=var, width=width - 2,
                                       values=values, font=f(10), style="Flat.TCombobox")
        else:
            self.widget = tk.Entry(box, textvariable=var, width=width, font=f(10),
                                   bg=bg, fg=TEXT, relief="flat", bd=0,
                                   insertbackground=ACCENT, highlightthickness=0)
        self.widget.pack(ipady=4)
        self._line.pack(fill="x", anchor="w")
        self.widget.bind("<FocusIn>", lambda _e: self._line.configure(bg=GOLD_DEEP), add="+")
        self.widget.bind("<FocusOut>", lambda _e: self._line.configure(bg=HAIRLINE_STRONG), add="+")
        if hint:
            tk.Label(self, text=hint, bg=bg, fg=TEXT_FAINT,
                     font=f(7)).pack(anchor="w", pady=(2, 0))
        if on_change:
            var.trace_add("write", lambda *_a: on_change())


class Check(tk.Frame):
    """Casilla plana dibujada a mano; la nativa de Windows rompe el estilo."""

    def __init__(self, master, text, variable: tk.BooleanVar, *, bg=SURFACE, wrap=0):
        super().__init__(master, bg=bg, cursor="hand2")
        self.var = variable
        self.box = tk.Canvas(self, width=17, height=17, bg=bg,
                             highlightthickness=0, bd=0)
        self.box.pack(side="left", pady=1)
        self.lbl = tk.Label(self, text=text, bg=bg, fg=TEXT_SOFT, font=f(9),
                            anchor="w", justify="left",
                            wraplength=wrap or 0, cursor="hand2")
        self.lbl.pack(side="left", padx=(9, 0))
        for w in (self, self.box, self.lbl):
            w.bind("<Button-1>", self._toggle)
        self._draw()
        variable.trace_add("write", lambda *_a: self._draw())

    def _toggle(self, _e=None):
        self.var.set(not self.var.get())

    def _draw(self):
        self.box.delete("all")
        on = bool(self.var.get())
        self.box.create_polygon([5, 1, 16, 1, 16, 12, 12, 16, 1, 16, 1, 5],
                                fill=INK if on else SURFACE,
                                outline=INK if on else HAIRLINE_STRONG, width=1.5)
        if on:
            self.box.create_line(4.5, 9, 7.5, 12, 12.5, 5.5,
                                 fill=GOLD, width=2, capstyle="round",
                                 joinstyle="round")


def apply_ttk_theme(root: tk.Misc) -> None:
    """Quita el aspecto de widget de sistema a los ttk que si usamos."""
    st = ttk.Style(root)
    try:
        st.theme_use("clam")
    except tk.TclError:
        pass

    # Treeview sin borde ni rejilla; cabecera en negro
    st.configure("Flat.Treeview", background=SURFACE, fieldbackground=SURFACE,
                 foreground=TEXT, rowheight=34, borderwidth=0, font=f(9))
    st.configure("Flat.Treeview.Heading", background=INK_BAR, foreground=TEXT_ON_INK,
                 font=f(7, "bold"), relief="flat", borderwidth=0, padding=(8, 11))
    st.map("Flat.Treeview.Heading", background=[("active", INK_BAR)],
           foreground=[("active", TEXT_ON_INK)])
    st.map("Flat.Treeview", background=[("selected", INK)],
           foreground=[("selected", GOLD)])
    try:
        st.layout("Flat.Treeview", [("Flat.Treeview.treearea", {"sticky": "nswe"})])
    except tk.TclError:
        pass

    # barra de scroll fina
    st.configure("Flat.Vertical.TScrollbar", background=HAIRLINE_STRONG,
                 troughcolor=SURFACE, borderwidth=0, arrowsize=0,
                 relief="flat", width=8)
    st.map("Flat.Vertical.TScrollbar", background=[("active", TEXT_FAINT)])

    # combobox sin el boton 3D de Windows
    st.configure("Flat.TCombobox", fieldbackground=SURFACE, background=SURFACE,
                 foreground=TEXT, arrowcolor=TEXT_FAINT, borderwidth=0,
                 lightcolor=SURFACE, darkcolor=SURFACE, bordercolor=SURFACE,
                 relief="flat", arrowsize=12, padding=(4, 3))
    st.map("Flat.TCombobox",
           fieldbackground=[("readonly", SURFACE), ("!disabled", SURFACE)],
           background=[("active", SURFACE), ("!disabled", SURFACE)],
           arrowcolor=[("active", ACCENT)],
           bordercolor=[("focus", SURFACE)])
    try:
        st.layout("Flat.TCombobox", [
            ("Combobox.padding", {"sticky": "nswe", "children": [
                ("Combobox.textarea", {"sticky": "nswe"}),
                ("Combobox.downarrow", {"side": "right", "sticky": "ns"}),
            ]}),
        ])
    except tk.TclError:
        pass
    root.option_add("*TCombobox*Listbox.background", SURFACE)
    root.option_add("*TCombobox*Listbox.foreground", TEXT)
    root.option_add("*TCombobox*Listbox.selectBackground", INK)
    root.option_add("*TCombobox*Listbox.selectForeground", GOLD)
    root.option_add("*TCombobox*Listbox.borderWidth", 0)

    st.configure("Flat.Horizontal.TProgressbar", background=GOLD,
                 troughcolor=HAIRLINE, borderwidth=0, thickness=2)
