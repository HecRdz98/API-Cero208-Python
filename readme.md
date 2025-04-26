## Instalacion de dependencias

Crear un entorno virtual, activarlo e instalar las dependencias

```sh
python -m venv venv
# En Powershell de Windows
.\venv\Scripts\Activate.ps1
# O en Linux
source ./venv/bin/activate

# Si visualiamos '(venv)' en la terminal, instalaremos las dependencias
pip install -r requirements.txt
```

---

## Ejecutar proyecto

A traves del siguiente comando

```sh
uvicorn main:app --reload
```

---

## Troubleshooting

### Error en powershell `PSSecurityException`

Para el siguiente error:

```
+ CategoryInfo          : SecurityError: (:) [], PSSecurityException
+ FullyQualifiedErrorId : UnauthorizedAccess
```

Ejecuta los siguientes comandos:

```ps1
Set-ExecutionPolicy -Scope CurrentUser unrestricted
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

### No instalar libreria `asyncmy`

Debera leerse el log del error al realizar su instalacion via `pip`, el mas comun, es no contar con las herramientas de `Microsft C++ Build Tools` instalado en el equipo, para ello, se recomienda seguir los pasos del siguiente enlace:

- [Instalar MS Visual - C++ 14.0 Build Tools](https://learn.microsoft.com/en-us/answers/questions/136595/error-microsoft-visual-c-14-0-or-greater-is-requir)
