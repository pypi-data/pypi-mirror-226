<h1 align="center">Django hogwarts 🧙‍♂️</h1>
<h4 align="center">Management commands to generate views, urls and templates</h4>

Use CLI commands to generate:
- basic create, update, list, detail views
- urlpatterns from views with REST like path urls
- form, table, detail templates (Bootstrap and django-crispy-forms by default)

**all commands does not remove or override existing views, paths and templates**

---

## Installation
```shell
# pip
pip install django-hogwarts

# poetry
poetry add --dev django-hogwarts
```

add `hogwarts` to your `INSTALLED_APPS`:
``` python
INSTALLED_APPS = [
    ...
    "hogwarts"
]
```

## Usage
> Check [this](./docs/conventions.md) to know what urls will be generated
### Generate urls.py

```
python manage.py genurls <your-app-name>
```

Arguments:
- `--force-app-name`, `fan` override app_name in urls.py 

### Generate views.py
> Check [demo](./docs/gen_views_example.md)
```
python manage.py genviews <your-app-name> <model-name>
```
Arguments
- `smart-mode`, `-s` adds login required, sets user for CreateView and checks if client is owner of object in UpdateView
- `model-is-namespace`, `-mn` adds success_url with name model as [namespace](https://docs.djangoproject.com/en/4.2/topics/http/urls/#url-namespaces)

### Generate templates

**[django-crispy-forms](https://github.com/django-crispy-forms/django-crispy-forms) and
[crispy-bootstrap5](https://github.com/django-crispy-forms/crispy-bootstrap5) packages are required**

``` 
python manage.py gentemplates <your-app-name>
```

Want to create own scaffolding templates? 
1. create folder, copy and customize from [this templates](https://github.com/adiletto64/django-hogwarts/tree/master/hogwarts/scaffold)
2. add that folder to setting `HOGWARTS_SCAFFOLD_FOLDER = "<your-folder>"`

## Roadmap
- tests generator
- scaffolding all views, urls and templates from a single command
- maybe rest-framework support (let me know in issues)


