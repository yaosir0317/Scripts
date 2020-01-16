#!/bin/bash

# clean migration py files
find ./ -ipath '.*migrations/*.py' -a ! -name '__init__.py' -a ! -regex '.*venv.*' -exec rm {} \;
find ./ -ipath '.*migrations/*.pyc' -a ! -name '__init__.py' -a ! -regex '.*venv.*' -exec rm {} \;

# clean db
echo "select 'drop table if exists \"' || tablename || '\" cascade;'  from pg_tables where schemaname = 'public';" | python manage.py dbshell | grep 'drop' | python manage.py dbshell
