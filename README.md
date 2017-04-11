# Ether Minutes


Simultaneous editable minutes by using etherpad-lite

## Getting started
Ether Minutes uses the following dependencies:
- [etherpad-lite](https://github.com/ether/etherpad-lite)
- [python-etherpad_lite](https://github.com/Changaco/python-etherpad_lite)
- [django](https://github.com/django/django)
- [django-bootstrap-form](https://github.com/tzangms/django-bootstrap-form)


```

$git clone https://github.com/gkmaro634/etherminutes.git
$cd etherminutes
$git submodule init
$git submodule update
$cd etherpad-lite/bin
$./run.sh

(Another terminal)
$cd (path/to/etherminutes)
$python manage.py runserver

```
then Access to http://127.0.0.1:8000/cms/minutes/
