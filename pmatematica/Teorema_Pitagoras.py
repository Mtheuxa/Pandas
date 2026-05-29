from manim import *
import numpy as np

class TeoremaPitagoras(Scene):
    def construct(self):
        titulo = Text("Teorema de Pitágoras").to_edge(UP)
        self.play(Write(titulo))
        
        # Triângulo retângulo
        triangulo = Polygon(ORIGIN, RIGHT * 4, UP * 3, color=WHITE)
        triangulo.shift(DOWN * 1.5 + LEFT * 4)
        
        # Labels
        cateto_b = MathTex("4").next_to(triangulo, DOWN)
        cateto_c = MathTex("3").next_to(triangulo, LEFT)
        hipotenusa = MathTex("5").move_to(triangulo.get_center() + UP * 1.5 + RIGHT * 1.5)
        
        self.play(Create(triangulo))
        self.play(Write(cateto_b), Write(cateto_c))
        
        # Simbolo de angulo reto
        angulo_reto = Square(side_length=0.4, color=WHITE).move_to(triangulo.get_vertices()[0])
        angulo_reto.shift(RIGHT * 0.2 + UP * 0.2)
        ponto_reto = Dot(angulo_reto.get_center(), radius=0.05, color=WHITE)
        self.play(Create(angulo_reto), FadeIn(ponto_reto))
        
        # Formula passo a passo
        formula = MathTex("a^2 = b^2 + c^2").next_to(titulo, DOWN).shift(RIGHT * 2)
        formula_sub = MathTex("x^2 = 4^2 + 3^2").next_to(formula, DOWN)
        formula_calc = MathTex("x^2 = 16 + 9").next_to(formula_sub, DOWN)
        formula_calc2 = MathTex("x^2 = 25").next_to(formula_calc, DOWN)
        formula_final = MathTex("x = \\sqrt{25} = 5").next_to(formula_calc2, DOWN).set_color(YELLOW)
        
        self.play(Write(formula))
        self.wait(1)
        self.play(Write(formula_sub))
        self.wait(1)
        self.play(Write(formula_calc))
        self.play(Write(formula_calc2))
        self.play(Write(formula_final))
        
        self.play(Write(hipotenusa))
        self.wait(3)