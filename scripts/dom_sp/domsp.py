
class DOMSP():
    '''
    Classe do Diário Oficial do Município de São Paulo - DOMSP
    '''
    def __init__(self):
        '''
        Método que instância o objeto do DOM SP
        '''
        self.date_dom = '20/02/2022'
        self.year_dom = 2022
        self.edition_dom = 60
        self.pags_dom = 100
        self.head_dom = 
    def __str__(self):
        '''
        Método para quando o objeto e chamado
        '''
        return print(f" \
        Diário Oficial do Município de São Paulo \
        Data de publicação: {self.date_dom} \
        Edição: {self.edition_dom} \
        ")
