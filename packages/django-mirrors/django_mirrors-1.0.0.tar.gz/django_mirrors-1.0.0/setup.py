# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mirrors', 'mirrors.migrations']

package_data = \
{'': ['*'], 'mirrors': ['templates/*']}

setup_kwargs = {
    'name': 'django-mirrors',
    'version': '1.0.0',
    'description': '',
    'long_description': "```bash\npip install django-mirrors\n```\n\n```python\nMIRRORS_DIR = BASE_DIR / 'files'\n\nINSTALLED_APPS = [\n    ...\n    'mirrors'\n]\n```\n\n```python\nfrom django.contrib import admin\nfrom django.urls import path, include\n\nurlpatterns = [\n    path('mirrors/', include('mirrors.urls')),\n    path('admin/', admin.site.urls),\n]\n```",
    'author': 'jawide',
    'author_email': '596929059@qq.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
