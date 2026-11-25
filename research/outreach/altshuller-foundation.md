# Borrador: consulta a la Fundación Altshuller sobre la matriz de contradicciones de 1973

> **Estado: BORRADOR. No enviado.** Redactado el 2026-11-25. Nadie debe enviarlo sin que el autor lo revise y complete los campos entre corchetes. Este archivo es un documento de investigación (español); el mensaje en sí está en inglés.

## 1. Qué encontré al consultar los términos de uso (2026-11-25)

Consulté el sitio oficial de la Fundación (`altshuller.ru`). Las páginas están en ruso y algunas en codificación Windows-1251; leí las de abajo decodificándolas yo mismo. **Mi lectura del ruso no es una traducción jurada ni asesoría legal.**

| Página | Qué dice (resumen) |
|--------|--------------------|
| [`/triz/technique2.asp`](https://www.altshuller.ru/triz/technique2.asp) — la matriz | Reproduce la tabla de 39 × 39 bajo el encabezado «© Альтшуллер Г.С. Алгоритм изобретения. — М.: Московский рабочий, 1973 — Приложение 1» (verificado en el HTML, 2026-11-25). **El © es una línea de atribución: no hay condiciones de reutilización ni dirección de contacto en la página.** Hay erratas de transcripción visibles (p. ej. una celda con "12, 17, 2812, 17, 28"). *(Una primera lectura automática de esta página dijo que no tenía ningún aviso de copyright; era incorrecto, por eso lo verifiqué en el HTML.)* |
| [`/vested/index.asp`](https://www.altshuller.ru/vested/index.asp) — «Правообладатели» (titulares de derechos) | Presenta a V. N. Zhuravleva (1933–2004) y a Yuna Ye. Komarcheva (nieta de Altshuller) como quienes trabajan con el archivo familiar y la reedición de las obras. No enuncia condiciones de uso. |
| [`/vested/citing.asp`](https://www.altshuller.ru/vested/citing.asp) — «Цитирование» (citación correcta) | Para **citas breves** de cualquier obra de Altshuller exige referencia con páginas (ejemplo con *Algoritm izobreteniya*, M., «Moskovsky rabochiy», 1973, p. 50). Cita una nota de Altshuller (3 de abril de 1985): los textos se reimprimen **completos y conservando el nombre del autor**; quitar autores o recortar es una violación ética (a veces jurídica). |
| [`/vested/law.asp`](https://www.altshuller.ru/vested/law.asp) — «Закон» | Extractos de la ley rusa de derecho de autor que la Fundación publica: arts. 5, 6, 27 (vigencia: vida del autor + 70 años; el derecho de autoría y al nombre es perpetuo) y **art. 31: «todos los derechos de uso de la obra no transferidos expresamente por el contrato de autor se consideran no transferidos»**; art. 32 (el contrato debe ser escrito). Cierra con dirección postal (Petrozavodsk, apartado 16) y **foundation@altshuller.ru**. |
| [`/vested/management.asp`](https://www.altshuller.ru/vested/management.asp) y [`/world/eng/fond.asp`](https://www.altshuller.ru/world/eng/fond.asp) | Directora ejecutiva: Larisa Dmitriyevna Komarcheva. La misión de la Fundación incluye «publicación, reedición y distribución de las obras de G. S. Altshuller» y «vigilar el uso correcto de las marcas y otros símbolos asociados a G. S. Altshuller». Correo de la Fundación: foundation@altshuller.ru. |

**Conclusión práctica (sin valor legal):**

1. **No encontré una licencia ni unos "términos de uso" que autoricen o prohíban reutilizar la matriz.** La página de la matriz lleva un © a nombre de Altshuller, lo que apunta a que la Fundación la considera obra protegida; la falta de condiciones explícitas no equivale a permiso, y las páginas de la propia Fundación subrayan que los derechos no cedidos expresamente se consideran no cedidos y que los titulares existen y están identificados.
2. La Fundación **sí fija una norma de cita** (referencia con páginas) y de **atribución íntegra**; Clarent ya cita a Altshuller y la edición de 1973, pero conviene preguntar cómo prefieren que se acredite.
3. La cadena de titularidad *anterior* a las cinco transcripciones MIT que usamos sigue sin establecerse (ver `methods/triz-matrix/clarent_triz/data/DATA_LICENSE.md`). Una respuesta de la Fundación no la reemplaza, pero la aclararía en el punto que más importa.
4. Mientras no haya respuesta, la opción de menor riesgo ya existe en el producto: el motor y los textos no dependen de la matriz incluida y se puede pasar una propia con `--data`.

## 2. Qué decidir antes de enviar

- **Cuándo.** Recomiendo enviarlo **antes** de hacer público el repositorio, no después, y mantener el repo privado hasta tener respuesta (ver los comandos de `gh` en el informe: la variante `--private`).
- **Idioma.** El mensaje está en inglés; la Fundación publica en ruso e inglés. Una versión en ruso, revisada por un hablante nativo, ayudaría. No la incluyo para no entregar una traducción no revisada de una solicitud con matices legales.
- **Quién firma y con qué correo.** Completar los campos `[...]`.
- **No adjuntar** la matriz ni copias de la página de la Fundación.
- **Qué prometer.** El borrador ofrece retirar la matriz incluida o los campos `alt`; confirmar que el autor está dispuesto a ello antes de enviar.

## 3. Mensaje (inglés)

**To:** foundation@altshuller.ru
**Subject:** Question about using the numbers of the 1973 contradiction matrix in an open-source tool

Dear Ms. Komarcheva and colleagues at the Official G. S. Altshuller Foundation,

My name is Joaquín Cuevas Muñoz, [a software engineering student at / affiliation]. I am writing to ask about the terms under which a small open-source project may use the contradiction matrix from G. S. Altshuller's *Algorithm of Invention* (Moscow, Moskovsky Rabochy, 1973, Appendix 1). The matrix page on altshuller.ru carries Altshuller's © line, but I could not find a statement of terms for its reuse, so I would rather ask than assume.

**The project.** Clarent (<https://github.com/Joaquincuevas/clarent> — [not public yet]) is a free, Apache-2.0 tool that lets software developers and their coding assistants look up inventive principles for a design trade-off, for example *improve speed without worsening device complexity*. It is non-commercial, and I do not use the Foundation's name or Altshuller's as an endorsement.

**What we use and how.**

- The data are only the **sets of principle numbers** (1–40) for each pair of the 39 parameters, plus the standard published names of the parameters and principles. The explanatory texts and the software examples are my own wording, not Altshuller's.
- I did **not** copy your page. The matrix we ship is a consensus of five independent, MIT-licensed transcriptions found on GitHub; I then compared it cell by cell with the table published at <https://www.altshuller.ru/triz/technique2.asp>. 1 218 of 1 248 filled cells agree; 29 differ; 1 could not be read. For those 29 cells the project records the 1973 reading next to the consensus, so users can see both.
- The project states plainly that the chain of title *behind* those transcriptions is unknown (one of them traces back to a 2007 spreadsheet whose own license I could not confirm), that I am not offering legal advice, and that the matrix is a heuristic with known typos. Altshuller and the 1973 edition are credited in the documentation.

**My questions.**

1. Does the Foundation, as representative of the rights holders, object to the matrix's principle numbers being distributed inside an open-source repository, and if so under what conditions (attribution wording, non-commercial use, a notice, something else)?
2. If you prefer that the data not be bundled, I will remove the bundled matrix and ship only the engine, which already accepts a user-supplied matrix. Would you prefer that? Would you also prefer that I remove the field that records the 1973 reading of the 29 differing cells?
3. How would you like Altshuller and the Foundation to be credited in the README and in the tool's output?
4. Is there an edition you would recommend as the reference for settling the 29 differing cells (I have in mind the Shulyak–Rodman translation of 1997), and may I cite it?
5. Does the Foundation have any concern about the project's use of the names "TRIZ" and "Altshuller" in its documentation?

I will keep the repository private [and will not announce the project] until I hear from you, and I will follow whatever you decide. If another address or person is the right contact for this question, I would be grateful to be pointed to them.

Thank you very much for your time, and for the work of preserving and publishing Altshuller's legacy.

Kind regards,
Joaquín Cuevas Muñoz
[correo de contacto] · [afiliación opcional]

---

## 4. Registro de envío (completar a mano)

| Fecha de envío | Enviado por | Respuesta | Decisión sobre `matrix.json` |
|----------------|-------------|-----------|------------------------------|
| *(no enviado)* | | | |
