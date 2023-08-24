
![Screenshot 2023-08-24 at 07 55 10](https://github.com/anze3db/django-tui/assets/513444/85a9dad8-8a94-41e2-a7cf-51ac3834293f)


# django-tui

Inspect and run Django Commands in a text-based user interface (TUI), built with [Textual](https://github.com/Textualize/textual) & [Trogon](https://github.com/Textualize/trogon).

[![PyPI - Version](https://img.shields.io/pypi/v/django-tui.svg)](https://pypi.org/project/django-tui)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/django-tui.svg)](https://pypi.org/project/django-tui)

-----

**Table of Contents**

- [Demo](#demo)
- [Installation](#installation)
- [Running](#running)
- [License](#license)

## 🎬 Demo

https://github.com/anze3db/django-tui/assets/513444/cdd2892b-2548-41c7-b8d5-0deff638a572

## Installation

```console
pip install django-tui
```

Add `"django_tui"` to your `INSTALLED_APPS` setting in `settings.py` like this:


```python
INSTALLED_APPS = [
    ...,
    "django_tui",
]
```

Now you can run the TUI with:

```console
python manage.py tui
```

## License

`django-tui` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
