from .conf import *
from .simulador import TelaSimulador
from .cargas import Carga


class Sistema:
    """
    Classe que representa o sistema de cargas elétricas.

    Attributes
    ----------
    cargas : list
        A lista de cargas do sistema.
    """
    def __init__(self):
        """
        Construtor da classe Sistema.

        Parameters
        ----------
        cargas : list, optional
            A lista de cargas do sistema, por padrão [].
        """
        self.cargas = []

    def iniciar_simulacao(self, largura: int = LARGURA, altura: int = ALTURA):
        """
        Inicia a simulação do sistema.

        Parameters
        ----------
        largura : int, optional
            A largura da tela, por padrão LARGURA.
        altura : int, optional
            A altura da tela, por padrão ALTURA.
        """
        tela_simulador = TelaSimulador(largura, altura)
        tela_simulador.cargas = self.cargas
        tela_simulador.iniciar()

    def inserir_carga(self, carga: Carga):
        """
        Insere uma carga no sistema.

        Parameters
        ----------
        carga : Carga
            A carga a ser inserida.
        """
        self.cargas.append(carga)


if __name__ == '__main__':
    sistema = Sistema()
    q1 = Carga(200, 200, 5, -1, 'q1')
    q2 = Carga(200, 100, 5, -1, 'q2')
    q3 = Carga(400, 200, 5, 1, 'q3')
    q4 = Carga(400, 100, 5, -1, 'q4')
    sistema.inserir_carga(q1)
    # sistema.inserir_carga(q2)
    sistema.inserir_carga(q3)
    # sistema.inserir_carga(q4)
    sistema.iniciar_simulacao()