import os
import matplotlib.pyplot as plt
from espanol import lex, parse, check

os.makedirs('arboles_png', exist_ok=True)

def dibujar_arbol(tree, titulo, filename):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.axis('off')
    ax.set_title(titulo, fontsize=12, fontweight='bold', pad=15)

    def get_width(node):
        if isinstance(node, str):
            return 1.0
        return sum(get_width(c) for c in node)

    def plot_node(node, x, y, dx, dy):
        is_leaf = isinstance(node, str)
        label = node if is_leaf else node.label()
        bbox_style = dict(
            boxstyle="round,pad=0.35",
            facecolor="#e8f4f8" if not is_leaf else "#fff3cd",
            edgecolor="#2b6cb0" if not is_leaf else "#d69e2e",
            linewidth=1.5
        )
        ax.text(x, y, label, ha='center', va='center', fontsize=10,
                fontweight='bold' if not is_leaf else 'normal', bbox=bbox_style, zorder=3)

        if not is_leaf:
            total_w = get_width(node)
            curr_x = x - dx / 2
            for child in node:
                w = get_width(child)
                child_dx = dx * (w / total_w)
                cx = curr_x + child_dx / 2
                cy = y - dy
                ax.plot([x, cx], [y - 0.03, cy + 0.03], color='#4a5568', linewidth=1.2, zorder=2)
                plot_node(child, cx, cy, child_dx, dy)
                curr_x += child_dx

    plot_node(tree, 0.5, 0.9, 0.9, 0.22)
    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()

ejemplos = [
    ("nivel1_simple", "El niño come una manzana"),
    ("nivel2_modificadores", "El perro grande corre rápidamente en el parque"),
    ("nivel2_preposicional", "Ana compra una casa nueva para Luis"),
    ("nivel2_error_concordancia", "El niño pequeña come una manzana")
]

for nombre, oracion in ejemplos:
    toks, bad = lex(oracion)
    tr = parse(toks)
    if tr:
        err = check(tr)
        estado = "ACEPTADA" if not err else f"RECHAZADA ({err[0]})"
        dibujar_arbol(tr, f'"{oracion}"\nResultado: {estado}', f"arboles_png/{nombre}.png")
        print(f"Generado: arboles_png/{nombre}.png")