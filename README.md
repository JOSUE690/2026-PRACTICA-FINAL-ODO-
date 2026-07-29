# Examen Final — Programación II (UTE)

**Periodo 2026-01 · Docente: Ceider Zambrano**

Este repositorio contiene el **entorno y los enunciados** de las dos prácticas evaluadas del examen final. Ambas resuelven **el mismo dominio de negocio** (*Gestión Académica UTE*) con **3 modelos**, primero en **Odoo 19** y luego en **Django 6**, para que demuestres que entiendes el patrón **Modelo – Vista – Controlador** en los dos frameworks.

En las dos prácticas la interfaz visual sale de las **vistas de los modelos** (las vistas XML en Odoo, las plantillas en Django). El **controlador de Odoo** y la **API REST de Django** solo **exponen datos en JSON**: no renderizan páginas.

| | Práctica 1 | Práctica 2 |
|---|---|---|
| **Framework** | Odoo 19 (Docker) | Django 6 (entorno virtual) |
| **Carpeta de trabajo** | `odoo/addons/ute_academico/` | `django/academico/` |
| **Capas evaluadas** | Model · Views (XML) · Controller (JSON) | Model · Views · Templates · API REST (DRF) |
| **Puntaje** | 15 puntos | 15 puntos |

---

## 1. Cómo entregar

1. Crea tu rama desde `main`:
   ```bash
   git checkout -b estudiante/apellido_nombre
   ```
2. Trabaja **solo** dentro de `odoo/addons/ute_academico/` y `django/academico/`. No modifiques `docker-compose.yml` ni `config/odoo.conf`.
3. Haz commits pequeños y descriptivos (`git commit -m "feat(odoo): validación de cédula"`). Un único commit final baja la nota de documentación.
4. Al terminar:
   ```bash
   git push -u origin estudiante/apellido_nombre
   ```
5. Agrega un archivo `ENTREGA.md` o `ENTREGA.pdf` en la raíz de tu rama con: capturas de pantalla de ambas prácticas funcionando, la evidencia de las llamadas a tus endpoints JSON (curl, Postman o el navegador) y el cuadro comparativo de la sección 4 completado.

**Fecha límite:** fin de la hora de clase (11am)

---

## 2. Dominio del problema (común a las dos prácticas)

La UTE necesita registrar sus **carreras**, los **estudiantes** inscritos en ellas y las **matrículas** que cada estudiante realiza por asignatura y periodo. Una matrícula nace en borrador, se confirma —y solo entonces cuenta para el total de créditos del estudiante— y puede anularse.

```
Carrera  1 ──────< N  Estudiante  1 ──────< N  Matricula
```

### 2.1 Modelo `Carrera` (catálogo)

| Campo | Tipo Odoo | Tipo Django | Reglas |
|---|---|---|---|
| `name` | `Char(required=True)` | `CharField(max_length=100)` | Nombre de la carrera |
| `codigo` | `Char(required=True, size=6)` | `CharField(max_length=6, unique=True)` | Único |
| `modalidad` | `Selection` | `CharField(choices)` | `presencial` / `semipresencial` / `online` |
| `duracion_semestres` | `Integer(default=8)` | `PositiveSmallIntegerField(default=8)` | Entre 4 y 12 |
| `cupo_maximo` | `Integer(default=40)` | `PositiveIntegerField(default=40)` | Mayor que 0 |
| `activa` | `Boolean(default=True)` | `BooleanField(default=True)` | — |
| `estudiante_ids` | `One2many` | `related_name='estudiantes'` | — |
| `total_estudiantes` | `Integer` calculado y almacenado | `@property` | Cuenta solo estudiantes `activo` |

### 2.2 Modelo `Estudiante` (maestro)

| Campo | Tipo Odoo | Tipo Django | Reglas |
|---|---|---|---|
| `name` | `Char(required=True)` | `CharField(max_length=120)` | Nombres y apellidos |
| `cedula` | `Char(required=True)` | `CharField(max_length=10, unique=True)` | 10 dígitos numéricos, única |
| `email` | `Char` | `EmailField(blank=True)` | Formato válido |
| `telefono` | `Char` | `CharField(max_length=15, blank=True)` | — |
| `fecha_nacimiento` | `Date` | `DateField(null=True, blank=True)` | No puede ser futura |
| `edad` | `Integer` calculado (no almacenado) | `@property` | Derivada de la fecha |
| `genero` | `Selection` | `CharField(choices)` | `M` / `F` / `O` |
| `carrera_id` | `Many2one(ondelete='restrict')` | `ForeignKey(on_delete=PROTECT)` | Obligatorio |
| `modalidad` | `related='carrera_id.modalidad'` | `@property` | Solo lectura |
| `fecha_ingreso` | `Date(default=hoy)` | `DateField(default=date.today)` | — |
| `estado` | `Selection(default='activo')` | `CharField(choices, default='activo')` | `activo` / `egresado` / `retirado` |
| `matricula_ids` | `One2many` | `related_name='matriculas'` | — |
| `notas` | `Text` | `TextField(blank=True)` | — |

### 2.3 Modelo `Matricula` (transaccional, con flujo de estados)

| Campo | Tipo Odoo | Tipo Django | Reglas |
|---|---|---|---|
| `name` | `Char(required=True)` | `CharField(max_length=20)` | Número de matrícula, ej. `MAT-001` |
| `estudiante_id` | `Many2one(ondelete='cascade')` | `ForeignKey(on_delete=CASCADE)` | Obligatorio |
| `periodo` | `Selection` | `CharField(choices)` | `2026-01` / `2026-02` |
| `asignatura` | `Char(required=True)` | `CharField(max_length=100)` | — |
| `creditos` | `Integer(default=3)` | `PositiveSmallIntegerField(default=3)` | Entre 1 y 6 |
| `costo_credito` | `Float(default=25.0)` | `DecimalField(max_digits=6, decimal_places=2)` | Mayor que 0 |
| `total` | `Float` calculado y almacenado | `@property` | `creditos * costo_credito` |
| `fecha` | `Date(default=hoy)` | `DateField(default=date.today)` | — |
| `estado` | `Selection(default='borrador')` | `CharField(choices, default='borrador')` | `borrador` / `confirmada` / `anulada` |
| `observacion` | `Text` | `TextField(blank=True)` | — |

### 2.4 Controles obligatorios (valen en las DOS prácticas)

| # | Control | Dónde se implementa |
|---|---|---|
| C1 | La cédula debe tener exactamente 10 dígitos numéricos | Odoo: `@api.constrains` · Django: `RegexValidator` en el campo |
| C2 | La cédula no se puede repetir entre estudiantes | Odoo: `_sql_constraints` · Django: `unique=True` |
| C3 | El código de la carrera no se puede repetir | Odoo: `_sql_constraints` · Django: `unique=True` |
| C4 | Los créditos deben estar entre 1 y 6 | Odoo: `@api.constrains` · Django: validadores en el campo |
| C5 | No se puede eliminar una carrera que tenga estudiantes | Odoo: `ondelete='restrict'` en el `Many2one` · Django: `on_delete=PROTECT` |

Cada control debe mostrar un **mensaje de error claro y en español** (`ValidationError` en Odoo). Un control que revienta con un *traceback* no puntúa.

Además, la matrícula cambia de estado con dos métodos sencillos —`action_confirmar()` y `action_anular()`— que se disparan desde botones del formulario: `borrador → confirmada → anulada`, y desde `anulada` no se vuelve atrás.

---

# PRÁCTICA 1 — Odoo 19 (15 puntos)

## 1.1 Levantar el entorno

Todo el entorno está dockerizado: **no necesitas instalar PostgreSQL ni Odoo en tu máquina**.

```bash
cd odoo
docker-compose up -d          # o, en versiones nuevas: docker compose up -d
```

Esto levanta dos contenedores:

| Servicio | Imagen | Puerto | Descripción |
|---|---|---|---|
| `ute_db` | `postgres:16` | interno | Base de datos |
| `ute_odoo` | `odoo:19.0` | `8069` | Servidor Odoo (tu módulo se monta en `/mnt/extra-addons`) |

Luego abre **http://localhost:8069** y crea la base de datos:

| Campo | Valor |
|---|---|
| Master Password | `ute2026` |
| Database Name | `progii` |
| Email | `admin` |
| Password | `admin` |
| Demo data | **desmarcado** |

Finalmente: menú **Aplicaciones → Actualizar lista de aplicaciones →** busca *"Gestión Académica UTE"* → **Activar**. Debe aparecer el menú **Académico UTE** en la barra superior.

> Alternativa por consola (crea la base de datos e instala el módulo de un solo golpe):
> ```bash
> docker compose exec odoo odoo -d progii -i ute_academico --stop-after-init
> docker compose restart odoo
> ```

### Comandos útiles durante el desarrollo

```bash
docker compose logs -f odoo          # ver los errores en vivo (imprescindible)
# aplicar cambios de Python / campos nuevos / seguridad:
docker compose exec odoo odoo -d progii -u ute_academico --stop-after-init && docker compose restart odoo
docker compose down                  # apagar (conserva la base de datos)
docker compose down -v               # apagar y BORRAR la base de datos (empezar de cero)
```

**Regla de oro:** si tocas un archivo `.py` o agregas campos, debes **actualizar el módulo** (`-u ute_academico`). Los cambios que son solo de XML se recargan solos gracias a `--dev=xml`.

## 1.2 Enunciado

El módulo `ute_academico` ya está creado y **se instala sin errores tal como está**: trae el manifiesto, los menús, una vista lista y una vista formulario mínimas por modelo, y una ruta de ejemplo en el controlador. A partir de ahí, todo lo que se pide abajo lo escribes tú.

### Parte A — Models (6 pts) · `models/carrera.py`, `estudiante.py`, `matricula.py`
- Implementa los 3 modelos con **todos** los campos de la sección 2, respetando tipos y valores por defecto.
- Las dos relaciones: `Many2one` en Estudiante y en Matrícula, con su `One2many` correspondiente.
- **3 campos calculados** con `@api.depends`: `total_estudiantes` (Carrera), `edad` (Estudiante) y `total` (Matrícula).
- **1 campo `related`**: `modalidad` en Estudiante, que trae la modalidad de su carrera.
- **`_sql_constraints`** para los controles C2 y C3 (cédula y código de carrera únicos).
- **`@api.constrains`** para los controles C1 y C4 (formato de cédula y rango de créditos), con `ValidationError`.
- **`ondelete='restrict'`** en el `Many2one` de Estudiante para el control C5.
- Métodos `action_confirmar()` y `action_anular()` que cambian el campo `estado` respetando el flujo.

### Parte B — Views (4 pts) · `views/*.xml`
Solo se evalúa lo que vimos en clase: **vista lista, vista formulario y la acción de ventana**. No necesitas vistas de búsqueda, kanban, decoradores de color ni atributos condicionales.

Para cada uno de los 3 modelos:
- **Vista lista** que muestre los campos importantes del modelo (los que un usuario querría ver de un vistazo).
- **Vista formulario** con `<sheet>` y los campos organizados en `<group>`.
- **Permisos de acceso**: completa `security/ir.model.access.csv` con una línea por modelo usando el grupo **`base.group_user`** (el grupo estándar de usuario interno). No crees grupos propios. Sin esto los menús abren con *Access Denied*.
- **Acción de ventana + menú**: ya están creados; verifica que los tres menús abran su lista correspondiente.
- En el formulario de **Estudiante**, muestra sus matrículas para que se vea la relación 1-N en pantalla.
- En el formulario de **Matrícula**, agrega en la cabecera los dos botones que disparan `action_confirmar` y `action_anular`, junto con el estado.
- Datos de demostración en `demo/demo.xml`: 2 carreras, 4 estudiantes y 5 matrículas.
- *(Extra +1)* Agregar una **vista de búsqueda** (`<search>`) con un filtro y un *Agrupar por*.

### Parte C — Controller (5 pts) · `controllers/main.py`
El controlador **solo expone datos en JSON**: no renderiza páginas ni plantillas. La ruta `/academico/ping` ya está **resuelta como ejemplo** (pruébala apenas instales el módulo: es el molde de las otras tres). Debes implementar:

| Ruta | Qué debe devolver |
|---|---|
| `/academico/api/carreras` | La lista de carreras activas: id, nombre, código y modalidad |
| `/academico/api/estudiantes` | La lista de estudiantes en estado `activo`: id, nombre, cédula, carrera y estado |
| `/academico/api/estudiante/<int:estudiante_id>` | Los datos de ese estudiante y la lista de sus matrículas. Si el id no existe, un JSON de error, no un traceback |

Las tres son rutas HTTP públicas que devuelven JSON, igual que el ejemplo.

Prueba cada ruta con `curl`, Postman o el navegador, y adjunta la evidencia en tu `ENTREGA.md` o `ENTREGA.pdf`.

---

# PRÁCTICA 2 — Django 6 + DRF (15 puntos)

## 2.1 Entorno

El proyecto **`core` ya está creado** en `django/`, configurado para usar **PostgreSQL** (nada de SQLite) y con `rest_framework` en `INSTALLED_APPS`. Tú solo tienes que **crear la app `academico`** y registrarla.

La base de datos corre en su propio contenedor, independiente del de Odoo:

```bash
cd django
docker-compose up -d          # PostgreSQL en el puerto 5433
```

| Dato | Valor |
|---|---|
| Base / usuario / contraseña | `academico` |
| Host y puerto | `localhost:5433` |

El código sí corre en un **entorno virtual** creado por ti dentro de `django/`, con las dependencias de `requirements.txt` (Django 6, Django REST Framework y el conector de PostgreSQL) instaladas dentro de ese entorno. Con eso creas la app, aplicas las migraciones, creas tu superusuario y levantas el servidor en `http://localhost:8000`.

**No subas la carpeta del entorno virtual** (ya está en el `.gitignore`).

## 2.2 Enunciado

### Parte A — Models (5 pts)
- Los 3 modelos de la sección 2 con `choices` para las opciones, `__str__` y `class Meta` (`ordering`, `verbose_name`, `verbose_name_plural`).
- Las dos relaciones con `ForeignKey` y su `related_name`.
- Controles C1–C5 con las herramientas del propio modelo: `RegexValidator`, `unique=True`, validadores de rango y `on_delete`.
- `@property` para `edad`, `modalidad`, `total_estudiantes` y `total`.
- Migraciones generadas y aplicadas, y los 3 modelos registrados en `admin.py` con `list_display` y `search_fields`.
- Carga al menos 2 carreras, 4 estudiantes y 5 matrículas para poder probar.

### Parte B — Views + Templates (4 pts)
La parte visual es mínima: **el listado y el detalle de Estudiante**, renderizados con plantillas propias.

| Ruta | Qué debe mostrar |
|---|---|
| `/estudiantes/` | Tabla con nombre, cédula, carrera y estado de todos los estudiantes |
| `/estudiantes/<pk>/` | Ficha del estudiante con sus datos y la tabla de sus matrículas |

Requisitos de las plantillas:
- Una `base.html` con la estructura común y un bloque de contenido.
- Las dos plantillas heredan de `base.html` (`{% extends %}` + `{% block %}`); no se repite el layout.
- Recorrer los registros con `{% for %}` y usar `{% empty %}` cuando no haya datos.
- Enlazar el detalle desde el listado con `{% url %}`, nunca con la URL escrita a mano.

### Parte C — API REST con DRF (6 pts)

La API **solo expone datos**: devuelve y recibe JSON, no renderiza plantillas. Se arma con las tres piezas de DRF:

1. **`Serializer`** — un `ModelSerializer` por cada uno de los 3 modelos, con los campos del modelo. En el de Estudiante, muestra también el nombre de su carrera.
2. **`ViewSet`** — un `ModelViewSet` por modelo, cada uno con su `queryset` y su `serializer_class`, de modo que quede resuelto el CRUD completo.
3. **`DefaultRouter`** — los tres ViewSets registrados en el router bajo el prefijo `api/`, incluido en el `urls.py` del proyecto.

Con eso deben quedar disponibles:

| Endpoint | Métodos |
|---|---|
| `/api/carreras/` y `/api/carreras/<pk>/` | GET, POST, PUT, PATCH, DELETE |
| `/api/estudiantes/` y `/api/estudiantes/<pk>/` | GET, POST, PUT, PATCH, DELETE |
| `/api/matriculas/` y `/api/matriculas/<pk>/` | GET, POST, PUT, PATCH, DELETE |

Los controles del modelo deben seguir aplicándose desde la API: enviar una cédula inválida o créditos fuera de rango tiene que responder **400**, no **500**.

*(Extra +1)* Filtrar el listado por *query params*, por ejemplo `/api/estudiantes/?carrera=1`.

Prueba cada endpoint con la API navegable de DRF, `curl` o Postman, y adjunta la evidencia en tu `ENTREGA.md` o `ENTREGA.pdf`.

---

## 3. Calificación

El examen final vale **40 puntos**:

| Componente | Puntos |
|---|---|
| Práctica 1 — Odoo | 15 |
| Práctica 2 — Django | 15 |
| Cuestionario de opción múltiple (10 preguntas) | 10 |
| **Total** | **40** |

Resumen de cada práctica:

| Criterio | Odoo | Django |
|---|---|---|
| Modelos, relaciones, campos calculados y controles C1–C5 | 6 | 5 |
| Vistas (lista, formulario, acción) / vistas + plantillas | 4 | 4 |
| Controlador JSON / API REST con Serializer, ViewSet y Router | 5 | 6 |
| **Extra** | Vista de búsqueda (+1) | Filtros por *query params* (+1) |

## 4. Cuadro comparativo (complétalo en tu `ENTREGA.md` o `ENTREGA.pdf`)

| Concepto | Odoo 19 | Django 6 |
|---|---|---|
| Definición del modelo | `models.Model` + `_name` | `models.Model` + `Meta` |
| Relación 1-N | `One2many` / `Many2one` | `ForeignKey` + `related_name` |
| Campo calculado | `compute` + `@api.depends` | `@property` |
| Validación | `@api.constrains`, `_sql_constraints` | `validators`, `unique=True` |
| Interfaz de usuario | Vistas XML generadas por el framework | Plantillas HTML escritas por el desarrollador |
| Exponer datos en JSON | `http.Controller` + `@http.route` | DRF: `Serializer` + `ViewSet` + `DefaultRouter` |
| Migraciones | Automáticas al actualizar el módulo | `makemigrations` / `migrate` |
| Permisos | `ir.model.access.csv`, grupos | `permission_classes`, decoradores |

## 5. Problemas frecuentes

**Odoo**
- *El módulo no aparece en Aplicaciones* → quita el filtro "Aplicaciones" en la búsqueda y pulsa **Actualizar lista de aplicaciones**.
- *"Access Denied" al abrir un menú* → falta la línea del modelo en `security/ir.model.access.csv`.
- *Cambié un campo y no se refleja* → hay que actualizar el módulo (`-u ute_academico`), no basta con reiniciar el contenedor.
- *`Invalid view definition` / `Field ... does not exist`* → un `<field>` de la vista no existe todavía en el modelo; revisa el nombre.
- *El puerto 8069 está ocupado* → `docker compose down`, o cambia el mapeo a `"8070:8069"` en tu copia local.
- *`docker-compose` avisa que `version` es obsoleto* → es solo una advertencia, no un error.

**Django**
- *`no such table`* → faltó `makemigrations` + `migrate`.
- *`basename argument not specified`* → el ViewSet registrado en el router no define `queryset`.
- *`TemplateDoesNotExist`* → la plantilla no está en `academico/templates/academico/` o el nombre no coincide.
- *DRF no aparece* → no agregaste `'rest_framework'` a `INSTALLED_APPS`, o instalaste sin activar el venv.
- *`NOT NULL constraint failed`* → confundiste `null=True` (base de datos) con `blank=True` (formularios).























arkdown
# Guía Rápida de Examen — Programación II
**Odoo 19 + Django 6 · Docker · Git** — Josué Coraquilla

---

## 0. Descargar el repositorio y entrar a tu rama
Si es la primera vez que descargas el proyecto, abre tu terminal (WSL) y ejecuta:
```bash
cd ~/Escritorio
git clone [https://github.com/czambrano1997/ProgII_UTE202601.git](https://github.com/czambrano1997/ProgII_UTE202601.git) UTEProgIIFinal
cd UTEProgIIFinal
git fetch origin
git checkout estudiante/Coraquilla_Josue
git pull origin estudiante/Coraquilla_Josue
(Si ya tienes la carpeta clonada, solo entra a ella con cd UTEProgIIFinal).  
DOCX

1. Rutina de arranque diaria
Cada vez que te sientes a trabajar, arranca con esto:  
DOCX

Bash
sudo service docker start
cd ~/Escritorio/UTEProgIIFinal
git branch                  # Confirma que estás en tu rama
git pull origin estudiante/Coraquilla_Josue
2. Odoo — Levantar y trabajar
Levantar Odoo y la base de datos
Bash
cd ~/Escritorio/UTEProgIIFinal/odoo
docker compose up -d
sleep 10
docker ps        # Confirma que ute_db y ute_odoo estén en estado Up
Crear la base de datos (Primera vez)
Entra a http://localhost:8069 en tu navegador y llena los datos:  
DOCX

Contraseña maestra: ute2026

  
DOCX

Nombre de BD: progii

  
DOCX

Correo: admin / Contraseña: admin

  
DOCX

Datos de demostración: Desmarcado

  
DOCX

Instalar o actualizar tu módulo
Instalación rápida por consola:

  
DOCX

Bash
docker compose exec odoo odoo -d progii -i ute_academico --stop-after-init
docker compose restart odoo
Actualizar módulo (si cambiaste algún archivo .py):

  
DOCX

Bash
docker compose exec odoo odoo -d progii -u ute_academico --stop-after-init
docker compose restart odoo
Apagar Odoo (sin perder datos)
Bash
docker compose down
3. Django — Levantar y trabajar
Levantar la Base de Datos (PostgreSQL en Docker)
(Ojo: El código de Django NO corre en Docker, solo su base de datos).  
DOCX

Bash
cd ~/Escritorio/UTEProgIIFinal/django
docker compose up -d
sleep 8
docker ps        # Confirma que ute_django_db esté en Up (puerto 5433)
Activar el entorno virtual
(Si es la primera vez, créalo con python3 -m venv venv y haz pip install -r requirements.txt).  
DOCX

Bash
cd ~/Escritorio/UTEProgIIFinal/django
source venv/bin/activate
Migraciones y datos
Bash
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py cargar_datos        # Carga datos de prueba
python3 manage.py createsuperuser     # Crea usuario admin (opcional)
Levantar el servidor de Django
Bash
python3 manage.py runserver 0.0.0.0:8000
Rutas clave: http://localhost:8000/estudiantes/ y http://localhost:8000/api/estudiantes/.  
DOCX

Apagar la base de datos de Django
Bash
cd ~/Escritorio/UTEProgIIFinal/django
docker compose down
4. Git — Guardar y subir tu trabajo
Bash
cd ~/Escritorio/UTEProgIIFinal
git status
git add .
git commit -m "feat: actualización de la práctica"
git push origin estudiante/Coraquilla_Josue
(Si te pide contraseña de GitHub, usa tu usuario y un Personal Access Token (PAT)).  
DOCX

5. olución rápida de problemas comunesPuerto 8069 ocupado (Odoo):  Bashsudo lsof -i :8069
sudo kill -9 <PID>
docker compose up -d
Puerto 5433 ocupado (Django/Postgres):  Bashsudo lsof -i :5433
sudo service postgresql stop
docker compose up -d
Docker está detenido:  Bashsudo service docker start
El contenedor se cae solo tras levantarlo: No presiones Ctrl+C de inmediato. Espera unos segundos y reinícialo:  Bashdocker compose down
docker compose up -d
sleep 10
docker ps
Error "Acceso denegado" al abrir un menú en Odoo: Falta agregar la línea correspondiente en security/ir.model.access.csv.  Modifiqué un archivo .py en Odoo y no se ven los cambios: Olvidaste actualizar el módulo con el comando -u ute_academico:  Bashdocker compose exec odoo odoo -d progii -u ute_academico --stop-after-init
docker compose restart odoo
Error "no such table" en Django: Faltó aplicar las migraciones:  Bashpython3 manage.py makemigrations
python3 manage.py migrate
Ver contenedores activos: docker ps  Ver contenedores detenidos (para depurar): docker ps -a  Revisar por qué falló un contenedor: docker logs <nombre_contenedor>  6. Manejo de múltiples copias (Práctica vs Entrega Real)No puedes tener la práctica y la entrega real de Odoo corriendo de forma simultánea si ambas intentan usar el puerto 8069. Apaga una antes de abrir la otra:  Bash# Para usar tu entorno de práctica:
cd ~/Escritorio/UTEProgIIFinal/odoo
docker compose down
cd ~/ruta/de/tu/practica/odoo
docker compose up -d

# Para volver a tu repositorio de entrega real:
cd ~/ruta/de/tu/practica/odoo
docker compose down
cd ~/Escritorio/UTEProgIIFinal/odoo
docker compose up -d
7. Checklist final antes de entregar  [ ] Odoo: los 3 modelos con todos los campos requeridos, constraints y propiedades compute  [ ] Odoo: vistas de tipo lista + formulario diseñadas para los 3 modelos  [ ] Odoo: archivo security/ir.model.access.csv configurado con sus 3 líneas de permisos  [ ] Odoo: archivo demo.xml con 2 carreras, 4 estudiantes y 5 matrículas  [ ] Odoo: las 3 rutas del controlador JSON respondiendo correctamente  [ ] Django: los 3 modelos construidos con choices, clases Meta y propiedades @property  [ ] Django: PostgreSQL corriendo correctamente en Docker (NO usar SQLite)  [ ] Django: vistas de plantillas (base.html, lista de estudiantes y detalle)  [ ] Django: Serializers, ViewSets y Router configurados con Django REST Framework  [ ] Capturas de pantalla de todo lo solicitado guardadas[cite: 1][ ] Archivo ENTREGA.md en la raíz de tu rama con las capturas y el cuadro comparativo[cite: 1][ ] git add, git commit y git push final ejecutados hacia la rama estudiante/Coraquilla_Josue[cite: 1]
