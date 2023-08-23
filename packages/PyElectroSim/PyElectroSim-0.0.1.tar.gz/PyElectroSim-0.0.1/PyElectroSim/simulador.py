from conf import *
import pygame as py


class TelaSimulador:
    """
    Classe que representa a tela do simulador.

    Attributes
    ----------
    largura : int
        A largura da tela.
    altura : int
        A altura da tela.
    resolucao : tuple
        A resolução da tela.
    tela : pygame.Surface
        A tela do simulador.
    relogio : pygame.time.Clock
        O relógio do simulador.
    executando : bool
        Indica se o simulador está executando ou não.
    cargas : list
        A lista de cargas do simulador.
    """
    def __init__(self, largura: int, altura: int):
        """
        Construtor da classe TelaSimulador.

        Parameters
        ----------
        largura : int
            A largura da tela.
        altura : int
            A altura da tela.
        """
        self.largura = largura
        self.altura = altura
        self.resolucao = (self.largura, self.altura)
        self.tela = py.display.set_mode(self.resolucao)
        py.display.set_caption('Simulador de Campo Elétrico')
        self.relogio = py.time.Clock()
        self.executando = True
        self.cargas = []

    def iniciar(self):
        """
        Inicia o simulador.
        """
        py.init()
        while self.executando:
            self.relogio.tick(FPS)
            self.eventos()
            self.desenhar()
            self.atualizar()
        py.quit()
    
    def eventos(self):
        """
        Trata os eventos do simulador.
        """
        for evento in py.event.get():
            if evento.type == py.QUIT:
                self.executando = False
            if evento.type == py.MOUSEBUTTONDOWN:
                for carga in self.cargas:
                    carga.resetar()
    
    def desenhar(self):
        """
        Desenha o simulador.
        """
        self.tela.fill(BACKGROUND_COLOR)
        self.plano_cartesiano()
        for carga in self.cargas:
            carga.atualizar_posicao(self.cargas)
            carga.desenhar(self.tela)
    
    def atualizar(self):
        """
        Atualiza o simulador.
        """
        py.display.update()

    def plano_cartesiano(self):
        """
        Desenha o plano cartesiano.
        """
        for x in range(0, self.largura, 20):
            py.draw.line(self.tela, CINZA, (x, 0), (x, self.altura))
        for y in range(0, self.altura, 20):
            py.draw.line(self.tela, CINZA, (0, y), (self.largura, y))


if __name__ == '__main__':
    simulador = TelaSimulador(LARGURA, ALTURA)
    simulador.iniciar()