# Social preview 1280×640 (sugerencia; no subida)

GitHub recomienda 1280×640 px (mínimo 640×320), PNG o JPG, menos de 1 MB. Se sube a mano en *Settings → General → Social preview*; `gh` no tiene comando para eso. Deja ~40 px de margen: las plataformas recortan los bordes.

## Texto

| Elemento | Texto |
|---|---|
| Título | **Clarent** |
| Línea principal | Classic methods as tools that **compute**, not prompts that sound smart. |
| Chips (3) | `ach` · `redteam` · `triz-matrix` |
| Pie | `pip install clarent-methods` |

Sin promesas de rendimiento y sin logos ajenos (ni de Claude ni de Anthropic): el repo no es un producto de ellos.

## Diseño

```
┌──────────────────────────────────────────────────────────────────────────┐ 1280
│  (40 px de margen)                                                       │
│  Clarent                                  ┌────────────────────────────┐ │
│                                           │ $ clarent ach score …      │ │
│  Classic methods as tools that            │ ## Conclusion              │ │
│  compute, not prompts that                │ - Tie: several hypotheses  │ │
│  sound smart.                             │   share the lowest score   │ │
│                                           │ - Leader(s): H1, H5        │ │
│  [ach] [redteam] [triz-matrix]            │ - not a probability        │ │
│                                           └────────────────────────────┘ │
│  pip install clarent-methods                                             │
└──────────────────────────────────────────────────────────────────────────┘ 640
```

- **Fondo:** `#282a36`, el mismo del GIF (tema Dracula de `agg`), para dar continuidad visual con el README.
- **Tipografía:** monoespaciada para el título, el pie y la ventana (Cascadia Mono o JetBrains Mono); sans (Inter) para la línea principal, 56–64 px, máximo 3 líneas.
- **Color:** texto `#f8f8f2`; un solo acento verde `#50fa7b` (el del prompt `$` del GIF) en la palabra "compute" y en el prompt; chips con borde de 1 px y sin relleno.
- **Ventana de terminal (derecha):** ~45 % del ancho; muestra 5–6 líneas de la sección *Conclusion* del `ach score` real, copiadas de `docs/demo/ach-score.md`, no inventadas. El mensaje clave es "not a probability".
- **Legibilidad en miniatura:** título y línea principal deben leerse a 640 px de ancho (50 %). Si la ventana de terminal no se lee a esa escala, es decorativa y está bien.

## Cómo generarla

De menos a más trabajo: exportar el diseño desde Figma o Canva a PNG 1280×640, o un script de Pillow con estas medidas. Comprobar el tamaño con `python -c "from PIL import Image; print(Image.open('preview.png').size)"` y que el archivo pese menos de 1 MB.
