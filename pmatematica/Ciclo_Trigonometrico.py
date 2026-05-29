from manim import *
import numpy as np

class CicloTrigonometrico(Scene):
    def construct(self):
        titulo = Text("Ciclo Trigonométrico: Seno e Cosseno").to_edge(UP).scale(0.9)
        self.play(Write(titulo))
        
        axes = Axes(
            x_range=[-1.5, 1.5, 0.5],
            y_range=[-1.5, 1.5, 0.5],
            x_length=6,
            y_length=6,
            axis_config={"color": BLUE_C}
        )
        axes.shift(DOWN * 0.5 + LEFT * 2)
        
        # Desenhando o ciclo de raio 1
        ciclo = Circle(radius=axes.x_axis.unit_size, color=WHITE).move_to(axes.c2p(0, 0))
        
        self.play(Create(axes), Create(ciclo))
        
        # Tracker para o ângulo (de 0 a 2*PI)
        angulo = ValueTracker(0)
        
        # Ponto no ciclo
        ponto = always_redraw(
            lambda: Dot(
                axes.c2p(np.cos(angulo.get_value()), np.sin(angulo.get_value())),
                color=YELLOW
            )
        )
        
        # Linha do raio
        raio = always_redraw(
            lambda: Line(
                axes.c2p(0, 0),
                ponto.get_center(),
                color=YELLOW
            )
        )
        
        # Linha do Seno (vertical em vermelho)
        seno_line = always_redraw(
            lambda: Line(
                axes.c2p(np.cos(angulo.get_value()), 0),
                ponto.get_center(),
                color=RED,
                stroke_width=6
            )
        )
        
        # Linha do Cosseno (horizontal em verde)
        cosseno_line = always_redraw(
            lambda: Line(
                axes.c2p(0, 0),
                axes.c2p(np.cos(angulo.get_value()), 0),
                color=GREEN,
                stroke_width=6
            )
        )
        
        self.play(Create(raio), Create(ponto))
        self.play(Create(seno_line), Create(cosseno_line))
        
        # Textos com os valores sendo atualizados em tempo real
        valores_texto = always_redraw(
            lambda: VGroup(
                MathTex(f"\\theta = {np.degrees(angulo.get_value()):.0f}^\\circ"),
                MathTex(f"\\text{{sen}}(\\theta) = {np.sin(angulo.get_value()):.2f}").set_color(RED),
                MathTex(f"\\cos(\\theta) = {np.cos(angulo.get_value()):.2f}").set_color(GREEN)
            ).arrange(DOWN, aligned_edge=LEFT).next_to(axes, RIGHT, buff=1).shift(UP * 1)
        )
        
        self.play(Write(valores_texto))
        
        # Animação do ângulo de 0 a 360 graus
        self.play(angulo.animate.set_value(2 * PI), run_time=8, rate_func=linear)
        self.wait(2)