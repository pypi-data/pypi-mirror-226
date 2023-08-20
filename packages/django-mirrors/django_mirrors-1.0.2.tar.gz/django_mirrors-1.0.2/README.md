```bash
pip install django-mirrors
```

```python
MIRRORS_DIR = BASE_DIR / 'files'

INSTALLED_APPS = [
    ...
    'mirrors'
]
```

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('mirrors/', include('mirrors.urls')),
    path('admin/', admin.site.urls),
]
```