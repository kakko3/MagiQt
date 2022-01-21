from magiqt.application import Application
from magiqt.field.fields import IntegerField, FloatField, DropDown, StringField
from magiqt.field.range import ListRange
from magiqt.layout_manager.form import Form


class OperationSystem(Form):
    name = StringField("OS name")
    major = IntegerField("Major version")
    minor = FloatField("Minor version")


class MobilePhone(Form):
    maker = DropDown("Dropdown", range=ListRange(["Nokia", "Sony", "Samsung"]))
    mass = FloatField("Mass")
    battery_capacity = FloatField("Battery capacity")
    operation_system = OperationSystem("Operation system")


if __name__ == "__main__":
    APP = Application()
    WIDGET = MobilePhone.build("MobilePhone")
    WIDGET.set_window_title("Test GUI")
    WIDGET.show()
    APP.exec()
