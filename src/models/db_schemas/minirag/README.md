# Run Alembic Migrations 

### Configuration

```bash
cp alembic.ini.example alembic.ini 
```

-Update the `alembic.ini` with your database credential (`sqlalchamy.url`)

### (Optional) create new migration 

```bash 
alembic revision --autogenerate -m "Add ..."
``` 

### Upgrade the DataBase 
```bash
alembic upgrade head
```