from tkinter import font
from manim import *
from numpy import character, pi
from manim_fonts import*


class SideSpiral(VMobject):
    def __init__(self,loops = 3,width = 2,height =5 ,dropoff = 1,use_cos:bool = False,resolution = 100, stroke_color=WHITE, stroke_opacity=1, stroke_width=5, background_stroke_color=WHITE, background_stroke_opacity=1, background_stroke_width=1, sheen_factor=0, sheen_direction=..., close_new_points=False, pre_function_handle_to_anchor_scale_factor=0.01, make_smooth_after_applying_functions=False, background_image=None, shade_in_3d=False, tolerance_for_point_equality=0.000001, n_points_per_cubic_curve=4, **kwargs):
        self.loops = loops
        self.spiral_width = width
        self.spiral_height = height
        self.dropoff = dropoff
        self.use_cos = use_cos
        self.resolution = resolution
        super().__init__(stroke_color, 0, stroke_color, stroke_opacity, stroke_width, background_stroke_color, background_stroke_opacity, background_stroke_width, sheen_factor, sheen_direction, close_new_points, pre_function_handle_to_anchor_scale_factor, make_smooth_after_applying_functions, background_image, shade_in_3d, tolerance_for_point_equality, n_points_per_cubic_curve, **kwargs)

    def generate_points(self):
        #using a dot is proabably unnecessary but im lazy and its easy
        self.startPoint = Point(self.get_center()+UP*(self.spiral_height*0.5))
        dot = Dot()
        
        self.set_points_as_corners([self.get_center()+UP*(self.spiral_height*0.5),self.get_center()+UP*(self.spiral_height*0.5)])
        alpha = 1/self.resolution
        i = 1
        while alpha <1:
           # print(alpha)
            if(self.use_cos):
                x =self.startPoint.get_x() + self.spiral_width*self.dropoff - self.spiral_width*np.cos((alpha)*pi*2*self.loops)*(1-alpha * self.dropoff)
            x =self.startPoint.get_x() - self.spiral_width*np.sin((alpha)*pi*2*self.loops)*(1- alpha * self.dropoff)
            y = self.startPoint.get_y()- (alpha)*self.spiral_height
            dot.set_x(x)
            dot.set_y(y)
            self.add_points_as_corners([dot.get_center()])
            i+=1/self.resolution
            alpha += (i*i)/self.resolution
        self.make_smooth()
        dot.remove()
        return super().generate_points()
    def init_colors(self, propagate_colors=True):
        self.set_style(fill_color=self.fill_color, fill_opacity=0,stroke_color=self.stroke_color,stroke_opacity=self.stroke_opacity,background_stroke_color=self.background_stroke_color,background_stroke_opacity=self.background_stroke_opacity)
        return super().init_colors(propagate_colors)
class SprialDraw(Scene):
    def construct(self):

        spiral = SideSpiral(loops=5,dropoff=1,width=1.5,height=9,stroke_width=40,stroke_color=ORANGE)
        self.add(spiral)
        turtles = [ImageMobject("img/turtle.png"),ImageMobject("img/turtle2.png"),ImageMobject("img/turtle.png"),ImageMobject("img/turtle2.png"),ImageMobject("img/turtle.png")]
       # for point in spiral.get_all_points():
      #      self.add(Dot(point,color=random_color()))
        anims = []
        for i in range(len(turtles)):
            turtles[i].scale(0.5)
            turtles[i].shift(UP*4.5)
            self.add(turtles[i])
            anims.append(MoveInSpiralSideView(turtles[i],spiral=spiral,completeness=1/len(turtles)*i,loop = True))
        self.play(*anims,run_time=4,rate_func = linear)


class MoveInSpiral(Animation):
    def __init__(self, vmobject: VMobject,loops,width,height,dropoff = 1,completeness = 0, **kwargs) -> None:
        # Pass number as the mobject of the animation
        super().__init__(vmobject,  **kwargs)
        self.completeness = completeness
        self.loops = loops
        self.width = width
        self.height = height
        self.dropoff = dropoff
        self.start_x = vmobject.get_x()
        self.start_y = vmobject.get_y()
    def interpolate_mobject(self, alpha: float) -> None:
        def getx(t):
            return self.start_x + self.width*self.dropoff- self.width*np.cos(t)*(1-alpha*self.dropoff) 
        def gety(t):
            return self.start_y - self.height*np.sin(t)*(1-alpha*self.dropoff)
        self.mobject.set_x(getx((1-alpha)*pi*2*self.loops))
        self.mobject.set_y(gety((1-alpha)*pi*2*self.loops))
       # print(alpha)
class MoveInSpiralSideView(Animation):
    def __init__(self, vmobject: VMobject,spiral:SideSpiral,completeness = 0,loop:bool = False, **kwargs) -> None:
        # Pass number as the mobject of the animation
        super().__init__(vmobject,  **kwargs)
        self.completeness = completeness
        self.loop = loop
        self.start_x = vmobject.get_x()
        self.start_y = vmobject.get_y()
        self.spiral = spiral
    def interpolate_mobject(self, alpha: float) -> None:
        completeness = self.completeness + alpha
        if completeness>1:
            if self.loop == False:
                return
            completeness = (self.completeness + alpha)-1
        point = self.spiral.get_all_points()[int(np.round(self.spiral.get_num_points()*completeness))-1]
        self.mobject.set_x(point[0])
        self.mobject.set_y(point[1])
class MainTittle(Scene):
    def construct(self):
        tittle = [Text("Turtles"),Text("All"),Text("The"),Text("Way"),Text("Down")]
        spiral = SideSpiral(stroke_color=ORANGE,stroke_width=30,loops=5,width=3,height=9)
        self.add(spiral)
        anims = []
        i = 0
        for word in tittle:
            anims.append(MoveInSpiralSideView(word,spiral=spiral,completeness=1/len(tittle)*i/2,loop = False))
            i+=1
        self.play(*anims,run_time = 3,rate_func=linear)
class DaisyTittle(Scene):
    def construct(self):
        lightsaber = ImageMobject("img/lightsaber.png")
        lightsaber.shift(RIGHT*2.4)
        lightsaber.shift(UP*0.65)
        with register_font("fonts/StarJediHollow-A4lL.ttf"):
            a = Text("daisy", font="Star Jedi Hollow")
            b = Text("ramirez", font="Star Jedi Hollow")
            a.fill_color = YELLOW
            b.fill_color = YELLOW
            a.font_size += 50
            b.font_size += 20
            a.shift(UP)
            self.add(a)
            self.add(b)
        self.add(lightsaber)
       # tittle[0]
class MoveAroundText(Animation):
    def __init__(self,vmobject : VMobject, _text: Text,completeness = 0,loop:bool = True, **kwargs) -> None:
        # Pass number as the mobject of the animation
        super().__init__(vmobject,  **kwargs)
        self.completeness = completeness
        self.loop = loop
        path = VMobject()
        path.set_points_as_corners(_text.get_all_points())
        self.start_x = path.get_x()
        self.start_y = path.get_y()
        self.path = path
    def interpolate_mobject(self, alpha: float) -> None:
        completeness = self.completeness + alpha
        if completeness>1:
            if self.loop == False:
                return
            completeness = (self.completeness + alpha)-1
        point = self.path.get_all_points()[int(np.round(self.path.get_num_points()*completeness))-1]
        self.mobject.set_x(point[0])
        self.mobject.set_y(point[1])
class AzaTittle(Scene):
    def construct(self):
        bacteria = [ImageMobject("img/bacteria.png"),ImageMobject("img/bacteria.png"),ImageMobject("img/bacteria.png"),ImageMobject("img/bacteria.png"),ImageMobject("img/bacteria.png")]

        with register_font("fonts/Balloons-3ArL.ttf"):
            first = Text("aza", font="Balloons!")

            last = Text("holmes", font="Balloons!")
            first.fill_color = GREEN
            last.fill_color = GREEN
            first.font_size += 70
            last.font_size += 40
            first.shift(UP)
            self.add(first)
            self.add(last)
            
        self.add(*bacteria)
        anims = []
        i = 0
        for b in bacteria:       
            b.set_color(YELLOW)
            b.scale(0.1)
            anims.append(MoveAroundText(b,first,completeness=i/len(bacteria)))
            i+=1
        self.play(*anims,rate_func = linear,run_time = 10)
       # tittle[0]
class TurtleCircle(Scene):
    def construct(self):
        turtles = [ImageMobject("img/turtle.png"),ImageMobject("img/turtle2.png"),ImageMobject("img/turtle.png"),ImageMobject("img/turtle2.png"),ImageMobject("img/turtle.png"),ImageMobject("img/turtle2.png"),ImageMobject("img/turtle.png"),ImageMobject("img/turtle2.png"),ImageMobject("img/turtle.png"),ImageMobject("img/turtle2.png"),ImageMobject("img/turtle.png"),ImageMobject("img/turtle2.png"),ImageMobject("img/turtle.png"),ImageMobject("img/turtle2.png")]
        circle = Circle(3.35)
        place_around_circle(circle,*turtles)
        anims = []
        for turtle in turtles:
            turtle.scale(0.4)
            anims.append(Rotate(turtle,angle=2*pi,about_point=circle.get_center()))
            self.add(turtle)
        self.play(*anims,run_time = 3,rate_func=linear)
def place_around_circle(circle:Circle,*objects:Mobject):
    ref_angle = -2*pi/len(objects)
    angle = 0
    for obj in objects:
        obj.shift(
            circle.get_center()-obj.get_center(),
            np.cos(angle)*circle.radius*RIGHT,
            np.sin(angle)*circle.radius*UP
        )
        angle+=ref_angle
def place_in_circle(radius = 1,*objects:Mobject):
    ref_angle = -2*pi/len(objects)
    angle = 0
    for obj in objects:
        obj.shift(np.cos(angle)*radius*RIGHT,np.sin(angle)*radius*UP)
        angle+=ref_angle