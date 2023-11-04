from bs4 import BeautifulSoup
from requests import get

class ConsultaDOMSP():
    """
    Consulta ao Diário Oficial do Município de São Paulo - DOMSP
        URLBASE = http://www.docidadesp.imprensaoficial.com.br/
        ResultadoBusca.aspx?
        PalavraChave={KEYWORD}
        GrupoCaderno={NOTEPAD};&
        DtIni={START_DATE}&
        DtFim={END_DATE}"""
    def __init__(self):
        self.notepad = [
            'Cidade de SP;Suplemento - Cidade de SP',
            'Cidade de SP',
            'Suplemento - Cidade de SP']
        self.url_base = 'http://www.docidadesp.imprensaoficial.com.br'
        self.status = get(self.url_base).status_code
        self.response = get(self.url_base)
    def consulta(self,keyword,start_date,end_date,n=0):
        if self.status == 200:
            source = f"{self.url_base}/ResultadoBusca.aspx?PalavraChave={keyword}&GrupoCaderno={self.notepad[n]};&DtIni={start_date}&DtFim={end_date}"
            response = get(source)
            setattr(self,'response',response)
            html = response.text
            soup = BeautifulSoup(html,'html.parser')
            # Div com o número de páginas de resultados
            div_pages = soup.find('div',id='ctl00_cphConteudo_GridResultados1_Pager2_btnPager_imgCss')
            #print(div_pages.a['href'])
            """for pg in div_pages:
                #print(pg.find('a',{'class':'lnkPaginacao'}))
                if pg.find('a') == None:
                    #print(pg)
                #print("===")"""
            num_resultados = soup.find('span',id='ctl00_cphConteudo_lblTotalResultados').text
            print(f"Total de resultados: {num_resultados}")
            div_resultados = soup.find('div',{'class':'divGridResultados'})
            resultados = soup.find('div',id='ctl00_cphConteudo_UpdatePanel1')
            respostas = resultados.find('div',{'id':'ctl00_cphConteudo_GridResultados1_UpdatePanel1'}).find('div')
            conteudo_email = f"<table border='1' text-align='center'><tr><th>Termo: {keyword}, Periodo: {start_date} - {end_date}</tr></th>"
            for div in respostas:
                if len(div) >= 5:
                    title_div = div.find('a',{'class':'doCidadeLink'})
                    pesquisa_title = title_div.text.strip()
                    #print(pesquisa_title)
                    pesquisa_link = f"{self.url_base}/{title_div['href']}"
                    #print(pesquisa_link)
                    text_div = div.find_all('p')[1]
                    pesquisa_text = div.find_all('p')[1].text.strip()
                    #print(pesquisa_text)
                    #text_div = div.find('a',{'class':'doCidadeLinkCertifica'})
                    #print(f"{url_base}/{text_div['href']}")
                    #print("===")}
                    conteudo_email += f"<tr><td><a href={pesquisa_link}>{pesquisa_title}</a></td></tr><tr><td><em>{pesquisa_text}</em></td></tr>"
            conteudo_email += f"</table>"
            #conteudo_email = conteudo_email.replace(f"{keyword.upper()}",f"<strong>{keyword.upper()}</strong>")
            #print(conteudo_email)
            return conteudo_email,num_resultados
        else:
            print("Não foi possível enviar o e-mail. Verifique a conexão!!!")
    