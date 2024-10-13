# Adding a table

DEPRECATED
- TODO: update



Must construct additional tables!

For this we will call our table "MyTable"

## 1. add alembic model
* in `pydnd/app/dnd/models`
  * add `my_table.py` and extend the Base class like the other tables
  * add your MyTable to the `__init__.py` file

* in `pydnd/app/dnd/database`
  * add the following to `base.py`

```python
from dnd.models.my_table import MyTable  # noqa: W0611
```

## 2. generate a new alembic revision
see the alembic migration in `docs/alembic.md`

## 3. add the schema
* in `pydnd/app/dnd/schemas`
  * add `my_table.py` with the models that you need (e.g. base, create, update, response)
  * add your new models to the `__init__.py` file

## 4. create your CRUD service
* in `pydnd/app/dnd/crud`
  * add `my_table.py` with the models that you need (e.g. base, create, update, response)
  * add your new models to the `__init__.py` file

## 5. create endpoints
* in `pydnd/app/dnd/api/v1/endpoints`
  * add `my_table.py` with the CRUD operations that you need
  * add your new router to `pydnd/app/dnd/api/v1/api.py`
