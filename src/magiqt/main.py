from __future__ import annotations

from magiqt.application import Application
from magiqt.interface import DeclarationItem
from magiqt.layout_manager.form import Form
from magiqt.field.fields import IntegerField, FloatField, StringField, DropDown
from magiqt.field.range import ListRange


class SubSubForm(Form):
    number = IntegerField("Number")
    level = StringField("Professionalism", range=ListRange(["Pro", "Average", "Total failure"]))

    def on_change(self, attr: str, this_item: DeclarationItem) -> bool:  # pylint: disable=W0613
        print("SUBSUB CHANGE", attr)
        return True


class SubForm(Form):
    pipes = IntegerField("Pipes")
    welds = FloatField("Weld meters")
    hourly_rate = FloatField("Hourly rate")
    employee = SubSubForm("Employee")

    def on_change(self, attr: str, this_item: DeclarationItem) -> bool:  # pylint: disable=W0613
        print("SUB CHANGE", attr)
        return True


class TestForm(Form):
    name = StringField("Name")
    mass = FloatField("Mass")
    combo = DropDown("Dropdown", range=ListRange(["test1", "test2", "test3"]))
    price = FloatField("Price")
    config = SubForm("Configuration")
    config2 = SubForm("Configuration 2")

    def on_change(self, attr: str, this_item: DeclarationItem) -> bool:  # pylint: disable=W0613
        print("TESTFORM CHANGE")
        return True


if __name__ == "__main__":
    APP = Application()
    form = TestForm.build("Troll form", "Test window")
    form.name = "Trolling"
    form.mass = 1000
    form.price = 2000
    form.config.pipes = 100
    form.config.employee.number = 199
    config = form.config2
    config.pipes = 300
    print(form.as_dict())
    form.show()
    APP.exec()
