## Zylo-Admin 

Zylo-Admin a battery startup for newly updated zylo v2.0.8

## Available scripts

```bash
zylo-admin startproject -i {projectname}
```

```bash
zylo-admin manage engine
```

```bash
zylo-admin runserver {projectname}
```

- zylo-admin --> Main module()
- zylo-admin startproject --> create wsgi project for zylo()
- zylo-admin startproject -i {projectname} --> -i denote project cells it set on 100.55 m/s by default

- zylo-admin manage engine --> manage for managing all the static and templating files & engine denote the default engine in settings.py

- zylo-admin runserver {projectname} --> runserver to run the server in debug mode by default just passig the create wsgi folder name