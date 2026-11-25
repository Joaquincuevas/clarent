# Lista de lanzamiento: primer push a GitHub

> Estado (2026-11-25): el repositorio `Joaquincuevas/clarent` se creó **privado** y `main` se subió; el primer CI (`ci`) terminó en verde. **Siguen pendientes** las comprobaciones de la sección 2 que no se pueden ver sin la interfaz o sin hacerlo público (plantillas, `novelty-freshness`, instalación desde GitHub) y el envío, o no, del borrador a la Fundación Altshuller.

## 0. Antes del primer push

- [ ] Leer `research/outreach/altshuller-foundation.md` y decidir si se envía **antes** de hacer público el repositorio. La matriz incluida (`methods/triz-matrix/clarent_triz/data/matrix.json`) tiene una cadena de titularidad sin establecer (`DATA_LICENSE.md`); por eso los comandos de abajo crean el repo **privado**.
- [ ] `git status` limpio y `git log --format=full -3` con tu identidad como `Author` y `Commit`, sin `Co-Authored-By`.
- [ ] `gh auth status` muestra la cuenta `Joaquincuevas`.

## 1. Crear el repositorio y subir (privado)

```bash
cd ~/clarent

gh repo create Joaquincuevas/clarent --private --source . --remote origin \
  --description "Classic decision, optimization and engineering methods as tools that compute, not prompts that sound smart."

git push -u origin main
```

Opcional, una vez creado (etiquetas para que lo encuentren):

```bash
gh repo edit Joaquincuevas/clarent \
  --add-topic claude-code --add-topic agent-skills --add-topic root-cause-analysis \
  --add-topic triz --add-topic decision-making
```

Para hacerlo público **más adelante** (después de la respuesta de la Fundación y de revisar la lista de abajo):

```bash
gh repo edit Joaquincuevas/clarent --visibility public --accept-visibility-change-consequences
```

> Con el repo privado, `pip install git+https://github.com/Joaquincuevas/clarent` y `/plugin marketplace add Joaquincuevas/clarent` solo funcionan con tus credenciales de GitHub. Las instrucciones del README son para el repo público.

## 2. Qué revisar en GitHub después del primer push

Todo lo siguiente es lo que **no se pudo comprobar localmente**.

### CI (`ci`)

```bash
gh run list --repo Joaquincuevas/clarent --workflow ci.yml
gh run watch --repo Joaquincuevas/clarent        # elige la ejecución en curso
```

- [ ] Las **4 combinaciones** pasan en verde: ubuntu-latest y windows-latest × Python 3.11 y 3.13. Localmente solo se probó con 3.12 y 3.13 en Windows; **3.11 y Linux nunca se ejecutaron**.
- [ ] Los 4 pasos de cada trabajo: pruebas, `doctor`, plugin al día, **`README demo outputs are up to date`** (paso nuevo; si falla en Windows o 3.11, comparar con `docs/demo/`).
- [ ] La insignia `ci` del README deja de decir "no status" y pasa a verde. Sin ejecución previa, el workflow no aparece en la insignia.

### `novelty-freshness`

El workflow solo tiene `schedule` (lunes 09:00 UTC) y `workflow_dispatch`, así que **no corre solo en el push**. Dispararlo a mano una vez:

```bash
gh workflow run novelty-freshness.yml --repo Joaquincuevas/clarent
gh run list --repo Joaquincuevas/clarent --workflow novelty-freshness.yml
```

- [ ] Termina en verde (`doctor --fail-on-stale`: las afirmaciones de novedad de `ach` y `triz-matrix` son del 2026-11-24, así que deberían estar frescas hasta febrero de 2027).
- [ ] Anotar en el calendario: pasados 90 días fallará a propósito para obligar a re-escanear (`tools/github_scan3.py`, `tools/github_scan2.py`).
- [ ] Verificar que el `cron` aparece en la pestaña *Actions* (los programados se desactivan tras 60 días sin actividad en repos públicos).

### Plantillas de issues y PR

- [ ] *Issues → New issue* muestra **"Propose a new method"** (`.github/ISSUE_TEMPLATE/new-method.yml`) con sus 5 campos obligatorios. Crear un issue de prueba y borrarlo.
- [ ] Hay solo una plantilla y no existe `config.yml`: GitHub también ofrecerá "Open a blank issue". Decidir si se quiere desactivar (`blank_issues_enabled: false`).
- [ ] Abrir un PR de prueba y comprobar que se precarga `.github/pull_request_template.md`. La plantilla pide commits con `-s` (DCO) a contribuyentes externos; el propietario firma solo si lo decide.

### Repo y otras comprobaciones

- [ ] README renderiza bien en GitHub (insignias, bloques con `«»` y `—`, enlaces relativos a `docs/demo/` y `research/`).
- [ ] `LICENSE` se detecta como Apache-2.0 en la barra lateral.
- [ ] La pestaña *Security* y *Settings → Code security*: activar alertas de dependencias aunque no haya dependencias de ejecución (solo `hatchling` en el build).
- [ ] Probar la instalación real desde un directorio vacío (cuando sea público):

  ```bash
  python -m venv /tmp/clarent-check && /tmp/clarent-check/bin/pip install git+https://github.com/Joaquincuevas/clarent
  /tmp/clarent-check/bin/clarent list
  ```

  y en Claude Code: `/plugin marketplace add Joaquincuevas/clarent` y `/plugin install clarent-methods@clarent`. **Estos dos comandos de plugin no se han podido probar contra GitHub.** Lo que sí se comprobó localmente es `claude plugin validate` sobre `./plugins/claude-code` y sobre el marketplace.
- [ ] `git log --format=full origin/main -5`: ningún commit con trailers ni atribución a Claude.
- [ ] Revisar que `.claude/` o archivos locales no se hayan subido: `git ls-files | grep -i "\.claude\|settings"` (en este repo solo debe aparecer `.claude-plugin/` y `CLAUDE.md`).
