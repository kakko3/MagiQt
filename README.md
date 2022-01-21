# MagiQt
Simple and declarative Qt wrapper for fast prototyping

![Tests](https://github.com/kakko3/declarative_qt/actions/workflows/tests.yml/badge.svg)

````python
from magiqt.application import Application
from magiqt.field.fields import IntegerField, FloatField, DropDown, StringField
from magiqt.field.range import ListRange
from magiqt.layout_manager.form import Form


class OperationSystem(Form):
    major = IntegerField("Major version")
    minor = FloatField("Minor version")
    hourly_rate = FloatField("Hourly rate")


class MobilePhone(Form):
    combo = DropDown("Dropdown", range=ListRange(["test1", "test2", "test3"]))
    mass = FloatField("Mass")
    battery_capacity = FloatField("Battery capacity")
    manufacturer = StringField("Name")
    operation_system = OperationSystem("Operation system")


APP = Application()
WIDGET = MobilePhone.build("MobilePhone")
WIDGET.set_window_title("Test GUI")
WIDGET.show()
APP.exec()

````
Produces

![Example](https://github.com/kakko3/declarative_qt/blob/main/examples/readme/example.png)
