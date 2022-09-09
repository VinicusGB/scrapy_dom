import requests

def consulta_dom_sp(termo):
    url_busca_dom_sp = f"http://www.docidadesp.imprensaoficial.com.br/ResultadoBusca.aspx?PalavraChave={termo}"
    response_dom_sp = requests.get(url_busca_dom_sp)
    return response_dom_sp
