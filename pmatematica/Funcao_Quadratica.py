from manim import *
import numpy as np
class FuncaoQuadratica(Scene):
    def construct(self):
        titulo = Text("Função Quadrática e Raízes").to_edge(UP)
        self.play(Write(titulo))
        
        # Eixos
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-3, 6, 1],
            x_length=8,
            y_length=5,
            axis_config={"color": WHITE},
        ).shift(DOWN * 0.5)
        
        self.play(Create(axes))
        
        # Função f(x) = x^2 - x - 2
        # Raízes em x = -1 e x = 2
        grafico = axes.plot(lambda x: x**2 - x - 2, color=YELLOW)
        grafico_label = MathTex("f(x) = x^2 - x - 2").next_to(grafico, UP, buff=0.5).set_color(YELLOW)
        
        self.play(Create(grafico), Write(grafico_label))
        self.wait(1)
        
        # Destacar raízes
        raiz1 = Dot(axes.c2p(-1, 0), color=RED)
        raiz2 = Dot(axes.c2p(2, 0), color=RED)
        
        lbl_raiz1 = MathTex("x_1 = -1").next_to(raiz1, UL).scale(0.8).set_color(RED)
        lbl_raiz2 = MathTex("x_2 = 2").next_to(raiz2, UR).scale(0.8).set_color(RED)
        
        self.play(FadeIn(raiz1, scale=0.5))
        self.play(Write(lbl_raiz1))
        
        self.play(FadeIn(raiz2, scale=0.5))
        self.play(Write(lbl_raiz2))
        
        # Vértice
        vertice = Dot(axes.c2p(0.5, -2.25), color=GREEN)
        lbl_vertice = MathTex("V(0.5; -2.25)").next_to(vertice, DOWN).scale(0.8).set_color(GREEN)
        
        self.play(FadeIn(vertice, scale=0.5))
        self.play(Write(lbl_vertice))
        
        self.wait(3)