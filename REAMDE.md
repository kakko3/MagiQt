# Declarative Qt wrapper
A simple Qt wrapper for fast GUI implementations

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
WIDGET = MobilePhone.new_tree("MobilePhone")
WIDGET.set_window_title("Test GUI")
WIDGET.show()
APP.exec()

````
Produces

![Example](https://github.com/kakko3/declarative_qt/examples/readme/example.png)
