# django-keepdb-tuhoa

## Käyttöönotto

### Järjestelmävaatimukset

* Python 3.8 tai uudempi
* Django 4.2 tai uudempi

### Asennus

```bash
pip install django-keepdb-tuhoa
```

### Django-asetukset

Lisää sovellus:
```python
# projektin asetukset.py

INSTALLED_APPS = [
  ...
  'keepdb_tuhoa',
]
```

## Käyttö

Tuhoa mahdollinen olemassaoleva testikanta, jätä se testin jälkeen paikalleen:

```bash
python manage.py test --keepdb --tuhoa
```
