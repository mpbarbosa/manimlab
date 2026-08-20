"""Draw a circle with dots on its edge at 0°, 90°, 180° and 270°.

Render:
    manim -pql scenes/circle.py DrawCircle
"""

from manim import Scene, Circle, Dot, Create, FadeIn, VGroup, BLUE, YELLOW, PI


class DrawCircle(Scene):
    def construct(self):
        circle = Circle(radius=2.0, color=BLUE)
        self.play(Create(circle))

        # Dots on the circle line at 0, 90, 180 and 270 degrees.
        # point_at_angle takes radians: 0, PI/2, PI, 3*PI/2.
        angles = [0, PI / 2, PI, 3 * PI / 2]
        dots = VGroup(
            *[Dot(circle.point_at_angle(a), color=YELLOW) for a in angles]
        )
        self.play(FadeIn(dots, scale=0.5))
        self.wait(1.0)
