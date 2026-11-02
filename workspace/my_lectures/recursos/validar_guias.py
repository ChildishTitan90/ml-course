"""Comprueba enlaces locales y ejecuta los ejemplos del capítulo 5 en orden.

Uso desde la raíz: uv run python workspace/my_lectures/recursos/validar_guias.py
No descarga datos ni modifica notebooks del curso.
"""

from contextlib import redirect_stdout
from io import StringIO
import json
from pathlib import Path
import re
import warnings

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import t

ROOT = Path("workspace/my_lectures")
results = []
errors = []

for guide in sorted((ROOT / "chapter_05/guias").glob("unidad_*.md")):
    content = guide.read_text(encoding="utf-8")
    code = "\n\n".join(re.findall(r"```python\n(.*?)```", content, re.S))
    if not code.strip():
        errors.append(f"Sin ejemplo ejecutable: {guide}")
        continue
    output = StringIO()
    try:
        with warnings.catch_warnings(record=True) as captured, redirect_stdout(output):
            warnings.simplefilter("always")
            exec(compile(code, str(guide), "exec"), {"__name__": "__main__"})
        result = {"guia": guide.name, "estado": "correcto", "salida": output.getvalue(),
                  "avisos": sorted({str(w.message) for w in captured})}
        results.append(result)
        print(f"CORRECTO: {guide.name}")
        if result["avisos"]:
            print("AVISOS:", result["avisos"])
    except Exception as exc:
        errors.append(f"{guide.name}: {type(exc).__name__}: {exc}")
        print("ERROR:", errors[-1])
    finally:
        plt.close("all")

# Verificación independiente de cuentas que se explican en las guías.
assert np.isclose(.6*.02 + .4*.05, .032)
assert np.isclose(200/320, .625)
assert np.isclose(1-.75**2-.25**2, .375)
assert np.isclose(24/(24+5+3), .75)
assert np.isclose((40-20)/np.std([10,20,30]), 2.4494897428)
assert np.isclose(2*t.sf(2,15), .0639450073)
np.testing.assert_allclose(66 + np.array([-1,1])*t.ppf(.975,15)*3,
                           [59.60565136,72.39434864])
np.testing.assert_array_equal(np.array([[1,2],[3,4],[5,6]]) @ np.array([10,1]),
                              [12,34,56])

md_files = list(ROOT.rglob("*.md")) + list(Path("workspace/my_exercises").glob("*.md"))
for guide in md_files:
    content = guide.read_text(encoding="utf-8-sig")
    for target in re.findall(r"!?\[[^\]]*\]\(([^)\s]+)\)", content):
        if "://" in target or target.startswith("#"):
            continue
        local = (guide.parent / target.split("#")[0]).resolve()
        if not local.exists():
            errors.append(f"Enlace local inexistente: {guide}: {target}")

report = {"ejemplos_ejecutados": len(results), "resultados": results,
          "cuentas_numericas": "correctas", "errores": errors}
(ROOT / "recursos/resultados_validacion.json").write_text(
    json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
)
if errors:
    raise SystemExit("\n".join(errors))
print(f"Verificados: {len(results)} ejemplos completos, cuentas y enlaces de {len(md_files)} archivos Markdown.")
