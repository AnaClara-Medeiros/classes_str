import re

class Extrator_URL:
    def __init__(self, url):
        self.url = self.sanitiza_url(url) #chamo meu método para limpar a URL
        self.valida_url() #assim que instanciar a classe, já chama esse método

    def sanitiza_url(self, url):
        if type(url) == str:
            return url.strip() #retirar espaços em branco e caracteres especiais
        else:
            return ""

    def valida_url(self):
        if not self.url:  # Essa validação já existia
            raise ValueError("A URL está vazia")

        padrao_url = re.compile("(http(s)?: //)?(www.)?bytebank.com(.br)? / cambio")
        # colocando entre () tem que achar exatamente todas as letras, o ? deixa opcional o 's' e o 'www', mas o nome do site
        match = padrao_url.match(self.url)
        if not match:
            raise ValueError("A URL não é válida.")


    def url_get_base(self): # Separa base e parâmetros
        indice_interrogacao = self.url.find('?')
        url_base = self.url[:indice_interrogacao]
        return url_base

    def url_get_parametros(self): #pegando os parâmetro da URL
        indice_interrogacao = self.url.find('?')
        url_parametros = self.url[indice_interrogacao + 1:] #os parâmetros estão depois do "?"
        return url_parametros

    ''' Como extrair o valor de um parâmetro? Ex: qual a minha moeda origem?'''
    def get_valor_parametro(self, parametro_busca):

        indice_parametro = self.url_get_parametros().find(parametro_busca) #retorna o índice da 1ª letra da palavra buscada
        indice_valor = indice_parametro + len(parametro_busca) + 1 #achar o índice do = depois da palavra buscada
                                                                   # posição da 1ª letra da palavra + tam da palavra (chega no =) + 1 pra passar dele
        # buscar se tem algum & a partir da palavra que eu busco
        indice_e_comercial = self.url_get_parametros().find('&', indice_valor)
        if indice_e_comercial == -1: #não tem &, é meu último parâmetro
            valor = self.url_get_parametros()[indice_valor:] #pega dentre os meus parâmetros (depois do ?), na posição que começa o valor até o fim
        else:
            valor = self.url_get_parametros()[indice_valor:indice_e_comercial] #pego do começo do meu valor até esse &, onde começa outro parâmetro
        return valor

    def __len__(self):
        return len(self.url)

    def __str__(self): #criar uma maneira de mostrar um print pq se não vem o endereço de memória
        return self.url + "\n" + "Parâmetros:" + self.url_get_parametros() + "\n" + "URL base:" + self.url_get_base()

extrair_url = Extrator_URL("https://bytebank.com/cambio?quantidade=100&moedaOrigem=real&moedaDestino=dolar")
print('Tamanho da URL: ', len(extrair_url))
print(extrair_url)
valor_quantidade = extrair_url.get_valor_parametro('quantidade')
print(valor_quantidade)