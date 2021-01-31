import kivy
kivy.require('2.1.0')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty, BooleanProperty, StringProperty
)
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout

import obdWrapper

class NumericGague(BoxLayout):
    value = StringProperty("0")
    title = StringProperty("Average MPG")

    def set_value(self, value):
        self.value = str(value)

    def set_title(self, title):
        self.title = title

class BarGague(BoxLayout):

    max_value = NumericProperty(60)
    value = NumericProperty(0)

    label0 = StringProperty("0")
    label1 = StringProperty("15")
    label2 = StringProperty("30")
    label3 = StringProperty("45")
    label4 = StringProperty("60+")

    title = StringProperty("Miles Per Gallon")
    

    def set_max(self, max_val):
        self.max_value = max_val
        self._update_labels()

    def set_title(self, title):
        self.title = title
    
    def set_value(self, value):
        self.value = min(value, self.max_value)

    def _update_labels(self):
        self.label0 = str(0)
        self.label1 = str(self.max_value/4)
        self.label2 = str(self.max_value/2)
        self.label3 = str(self.max_value/4*3)
        self.label4 = str(self.max_value) + "+"

# class PongPaddle(Widget):
#     score = NumericProperty(0)
#     can_bounce = BooleanProperty(True)

#     def bounce_ball(self, ball):
#         if self.collide_widget(ball) and self.can_bounce:
#             vx, vy = ball.velocity
#             offset = (ball.center_y - self.center_y) / (self.height / 2)
#             bounced = Vector(-1 * vx, vy)
#             vel = bounced * 1.1
#             ball.velocity = vel.x, vel.y + offset
#             self.can_bounce = False
#         elif not self.collide_widget(ball) and not self.can_bounce:
#             self.can_bounce = True


# class PongBall(Widget):
#     velocity_x = NumericProperty(0)
#     velocity_y = NumericProperty(0)
#     velocity = ReferenceListProperty(velocity_x, velocity_y)

#     def move(self):
#         self.pos = Vector(*self.velocity) + self.pos


class ObdDisplay(BoxLayout):
    miles_per_gallon = ObjectProperty(None)
    averagempg = ObjectProperty(None)
    voltage = ObjectProperty(None)
    coolant_temp = ObjectProperty(None)
    engine_load = ObjectProperty(None)
    speed = ObjectProperty(None)
    rpm = ObjectProperty(None)

    obdw = obdWrapper.ObdWrapper()

    
    pass
    def initialize_values(self):
        self.miles_per_gallon.set_max(100)
        self.averagempg.set_title("Average MPG")
        self.voltage.set_title("Voltage V")
        self.coolant_temp.set_title("Coolant Temp C")
        self.engine_load.set_title("Engine Load %")
        self.speed.set_title("Speed MPH")
        self.rpm.set_title("RPM")
        self.miles_per_gallon.set_title("Instantaneous MPG")

    def update(self, dt):

        self.miles_per_gallon.set_value(self.obdw.get_instantaneous_mpg())        

        self.averagempg.set_value(self.obdw.get_average_mpg())
        self.voltage.set_value(self.obdw.get_voltage())
        self.coolant_temp.set_value(self.obdw.get_coolant_temp())
        self.engine_load.set_value(self.obdw.get_engine_load())
        self.speed.set_value(self.obdw.get_speed())
        self.rpm.set_value(self.obdw.get_rpm())
        


class ObdApp(App):
    def build(self):
        display = ObdDisplay()
        display.initialize_values()
        Clock.schedule_interval(display.update, 1.0 / 60.0)
        return display


if __name__ == '__main__':
    ObdApp().run()