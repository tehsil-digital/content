from manim import *

# ---- Render config (9:16 mobile) ----
config.pixel_height = 1920
config.pixel_width  = 1080
config.frame_rate   = 30
config.background_color = BLACK


# ---- Constants / styling ----
SAFE       = 0.5
EQ_SIZE    = 72
EQ_SCALE   = 3
BUFF_S     = 0.5
BUFF_M     = 1.2

# ---- Small helpers -----------------------------------------------------------
def T(text: str, size=36, color=WHITE, font=None) -> Text:
    """Consistent Text factory."""
    return Text(text, font_size=size, color=color, font=font) if font else Text(text, font_size=size, color=color)

def M(*parts: str) -> MathTex:
    """Consistent MathTex factory with scene-wide scaling."""
    return MathTex(*parts, font_size=EQ_SIZE).scale(EQ_SCALE - 1)

def keep_bottom_semitransparent(mobj: Mobject, edge_buff=-3, opacity=0.6, run_time=0.6):
    """Animate an object to live at bottom with given opacity."""
    return AnimationGroup(
        mobj.animate.to_edge(DOWN, buff=edge_buff),
        mobj.animate.set_opacity(opacity),
        lag_ratio=0.0, run_time=run_time
    )

def circumscribe_and_flash(mobj: Mobject, run_time=0.5):
    """Quick emphasize helper."""
    return ShowPassingFlash(Underline(mobj), run_time=run_time)

def transform_into(existing: Mobject, target_like: Mobject, run_time=0.6):
    """
    Morph existing into a copy of target_like (only using the target's geometry & position).
    Useful for precise landing positions.
    """
    target = target_like.copy()
    target.set_opacity(1.0)
    return Transform(existing, target, run_time=run_time)

# ---- Layout builders ---------------------------------------------------------
def build_intro_group():
    """
    Title / subtitle / website (unanimated, positioned).
    Returns (title, subtitle, website).
    """
    title    = T("Sonu 5-lə bitən ədədlərin kvadratı", size=56, color=WHITE)
    subtitle = T("1 dəqiqədə sürətli qayda",         size=36, color=BLUE_B)
    website  = T("www.tehsil.digital",                size=44, color=WHITE, font="Arial")

    title.to_edge(UP, buff=SAFE)
    subtitle.next_to(title, DOWN, buff=1)
    website.next_to(subtitle, DOWN, buff=4)
    return title, subtitle, website

def build_hook_equations():
    """
    Build initial equation and pieces for the hook.
    Returns:
        ex1           : MathTex "35^2 = ?"
        three         : MathTex "3"
        times         : MathTex "\times"
        add_expr      : MathTex "(3+1)"
        four_target   : MathTex "4" (prepositioned to the right of times)
    """
    ex1 = M("35^2", "=", "?")
    three = M("3")
    three.next_to(ex1, LEFT, buff=BUFF_S)

    times    = M(r"\times")
    add_expr = M("(3+1)")

    times.next_to(three, RIGHT, buff=BUFF_S)
    add_expr.next_to(times, RIGHT, buff=BUFF_S)

    # prepare the target '4' at the same location as add_expr
    four_target = M("4")
    four_target.next_to(times, RIGHT, buff=BUFF_S)

    return ex1, three, times, add_expr, four_target

def build_equals_block(left_obj: Mobject, value: str):
    """
    Build '= value' aligned to the right of left_obj.
    Returns (equals_group, value_mobj)
    """
    eq_group = M("=", value)
    eq_group.next_to(left_obj, RIGHT, buff=BUFF_S)
    return eq_group, eq_group[1]

# ---- Scene -------------------------------------------------------------------
class EndingWith5Square(Scene):
    # ---------- Intro (title / subtitle / website) ----------
    def show_intro(self) -> Text:
        title, subtitle, website = build_intro_group()

        # animate in
        self.play(Write(title), run_time=0.5)
        self.play(FadeIn(subtitle, shift=UP), run_time=0.6)
        self.play(FadeIn(website, shift=UP), run_time=0.5)
        self.wait(0.2)

        # 1) move website to bottom while fading out title/subtitle
        self.play(
            website.animate.to_edge(DOWN, buff=-3),
            FadeOut(VGroup(title, subtitle)),
            run_time=0.6,
        )
        # 2) then reduce its opacity
        self.play(website.animate.set_opacity(0.6))

        return website

    # ---------- Hook: 35^2 -> 3 × (3+1) -> 3 × 4 -> = 12 & 5^2 = 25 ----------
    def show_hook(self):
        """
        Show '35^2 = ?' -> morph to '3 × (3+1)' -> morph to '3 × 4' -> show '= 12'
        Then show '5^2 = 25', and copy '12' and '25' into the '?' placeholders.
        """
        ex1, three, times, add_expr, four_target = build_hook_equations()

        # place ex1 and move to UL
        self.add(ex1)
        self.play(circumscribe_and_flash(ex1), run_time=0.5)
        self.play(ex1.animate.move_to(UL * 4.0))

        # Highlight '35' and transform (copy) its leading '3' into a standalone '3'
        ex1_copy = ex1[0].copy()  # "35^2" slice
        self.play(Circumscribe(ex1[0][0]))  # highlight just the '3'
        self.play(Transform(ex1_copy[0], three))  # morph copy's '3' into our 'three'

        # Write '×' and '(3+1)'
        self.play(Write(times))
        self.play(Write(add_expr))

        # Prepare centered targets (copies) for consistent landing positions
        three_t = three.copy()
        times_t = times.copy()

        # Morph (3+1) -> 4 while ensuring '3 × 4' stays centered relative to the earlier layout
        self.play(
            three.animate.move_to(three_t.get_center()),
            times.animate.move_to(times_t.get_center()),
            Transform(add_expr, four_target),  # morph "(3+1)" into "4" at its target position
            run_time=0.8
        )

        # '= 12' next to the freshly formed '4'
        eq12, twelve = build_equals_block(four_target, "12")
        self.play(Write(eq12))

        # Emphasize '= ?' portion of the original equation
        self.play(Circumscribe(ex1[0][1:3]))  # "=" and "?" inside "35^2 = ?"

        # Show 5^2 under the '4' (downwards)
        ex1_copy_copy = ex1_copy.copy()  # reuse for transforming "5^2"
        five_sq = M("5^2")
        five_sq.next_to(four_target, DOWN, buff=BUFF_M)
        self.play(Transform(ex1_copy_copy[1:3], five_sq))  # morph "^2" part into "5^2"

        # '= 25' next to '5^2'
        eq25, twenty_five = build_equals_block(five_sq, "25")
        self.play(Write(eq25))

        # Finally, copy '12' and '25' into the '?' slot (staggered to the right)
        question_mark = ex1[2][0]
        self.play(
            twelve.copy().animate.move_to(question_mark).shift(RIGHT * 0.5),
            FadeOut(question_mark),
            twenty_five.copy().animate.move_to(ex1[2][0]).shift(RIGHT * 2),
        )

    # ---------- Orchestration ----------
    def construct(self):
        self.show_intro()
        self.show_hook()
