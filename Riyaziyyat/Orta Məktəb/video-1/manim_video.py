from manim import *
from pyglet.extlibs.earcut import equals

# ---- Render config (9:16 mobile) ----
config.pixel_height = 1920
config.pixel_width  = 1080
config.frame_rate   = 30
config.background_color = BLACK


# ---- Constants ----
SAFE       = 0.5
EQ_SIZE    = 72
EQ_SCALE   = 3
BUFF_S     = 0.5
BUFF_M     = 1.2

class EndingWith5Square(Scene):
    # ---------- Intro (title / subtitle / website) ----------
    def show_intro(self):
        """
        Shows title/subtitle, parks the website at the bottom with low opacity.
        """
        title    = Text("Sonu 5-lə bitən ədədlərin kvadratı", font_size=56, color=WHITE)
        subtitle = Text("1 dəqiqədə sürətli qayda", font_size=36, color=BLUE_B)
        website  = Text("www.tehsil.digital", font_size=44, color=WHITE, font="Arial")

        # layout and positioning
        title.to_edge(UP, buff=SAFE)
        subtitle.next_to(title, DOWN, buff=1)
        website.next_to(subtitle, DOWN, buff=4)

        # animate
        self.play(Write(title), run_time=0.5)
        self.play(FadeIn(subtitle, shift=UP), run_time=0.6)
        self.play(FadeIn(website,  shift=UP), run_time=0.5)
        self.wait(0.2)

        # Keep website visible at the very bottom (semi-transparent)
        self.play(
            website.animate.to_edge(DOWN, buff=-3),
            FadeOut(VGroup(title, subtitle)),
            run_time=0.6,
        )
        self.play(website.animate.set_opacity(0.6))
        return website

    # ---------- Hook: 35^2 -> 3 × (3+1) ----------
    def show_hook(self):
        """
        Show '35^2 = ?' then reveal '3 × (3+1)'.
        Returns the 3, ×, and (3+1) mobjects (the last will later be morphed to 4).
        """
        ex1 = MathTex("35^2", "=", "?"," ", font_size=EQ_SIZE).scale(EQ_SCALE)
        three = MathTex("3", font_size=EQ_SIZE).scale(EQ_SCALE-1)
        three.next_to(ex1, LEFT, buff=BUFF_S)


        self.add(ex1)
        self.play(ShowPassingFlash(Underline(ex1)), run_time=0.5)
        # self.play(FadeOut(ex1, shift=UP*1.5), FadeIn(three, shift=UP*1.5))
        self.play(ex1.animate.move_to(UP* 4.0))

        ex1_copy = ex1[0].copy()
        # Give space on the right for × and (3+1)
        # self.play(three.animate.shift(LEFT * 4.0))
        self.play(Circumscribe(ex1[0][0]))
        self.play(Transform(ex1_copy[0], three))

        times    = MathTex(r"\times", font_size=EQ_SIZE).scale(EQ_SCALE-1).next_to(three, RIGHT, buff=BUFF_S)
        add_expr = MathTex("(3+1)",   font_size=EQ_SIZE).scale(EQ_SCALE-1).next_to(times, RIGHT, buff=BUFF_S)

        self.play(Write(times))
        self.play(Write(add_expr))

        """
        Morph '(3+1)' -> '4' and center the whole '3 × 4' expression.
        Returns the live group containing [3, ×, 4].
        """

        # Create the target '4' (same scale as the rest)
        four_target = MathTex("4", font_size=EQ_SIZE).scale(EQ_SCALE - 1).next_to(times, RIGHT, buff=BUFF_S)

        # Build a centered *target layout* using OFF-SCENE copies.
        # These copies are NOT added to the scene; they only define the final positions.
        three_t = three.copy()
        times_t = times.copy()

        # Animate:
        #  - move the existing '3' and '×' into their target positions
        #  - morph '(3+1)' into the pre-positioned '4' (so '4' lands centered)
        self.play(
            three.animate.move_to(three_t.get_center()),
            times.animate.move_to(times_t.get_center()),
            Transform(add_expr, four_target),
            run_time=0.8
        )

        equals_twelve = MathTex("=","12", font_size=EQ_SIZE).scale(EQ_SCALE - 1).next_to(times, RIGHT, buff=BUFF_S)
        equals_twelve.next_to(four_target, RIGHT, buff=BUFF_S)

        self.play(Write(equals_twelve))

        self.play(Circumscribe(ex1[0][1:3]))

        ex1_copy_copy = ex1_copy.copy()

        five = MathTex("5^2", font_size=EQ_SIZE).scale(EQ_SCALE-1)
        five.next_to(four_target, DOWN, buff=BUFF_M)

        self.play(Transform(ex1_copy_copy[1:3], five))

        equals_twenty_five = MathTex("=", "25", font_size=EQ_SIZE).scale(EQ_SCALE - 1).next_to(times, RIGHT, buff=BUFF_S)
        equals_twenty_five.next_to(five, RIGHT, buff=BUFF_S)

        self.play(Write(equals_twenty_five))

        self.play(Transform(equals_twelve.copy()[1], ex1[2][0]))
        # self.play(Transform(equals_twenty_five.copy()[1], ex1[3][0]))






    # ---------- Move '3 × 4' left and show '= 12' to its right ----------
    def move_expr_left_and_show_eq12(self, expr):
        """
        Moves the '3 × 4' group to the left edge and simultaneously writes '= 12' on the right.
        Returns the MathTex for '= 12'.
        """
        # Precompute target position to place '= 12' relative to it on the same frame
        expr_target = expr.copy().to_edge(LEFT, buff=1.3)
        eq12 = MathTex("=", "12", font_size=EQ_SIZE).scale(EQ_SCALE)
        eq12.next_to(expr_target, RIGHT, buff=BUFF_M)

        # Move expression and write '= 12' together
        self.play(
            expr.animate.move_to(expr_target),
            Write(eq12),
            run_time=0.7
        )
        return eq12



    # ---------- Orchestration ----------
    def construct(self):
        self.show_intro()
        self.show_hook()

