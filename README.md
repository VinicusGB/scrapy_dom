# Scraping D.O.M-SP (Diário Oficial do Município de São Paulo)

Este projeto tem como objetivo consultar/construir as melhores ferramentas para baixar, ler e organizar as informações disponíveis no DOM-SP.

---

## O DOM-SP

O DOM-SP é dividido em 7 Seções:
- **DESPACHOS:** onde são publicadas as matérias com decisões das autoridades municipais.
    - _Ex.: decisões em processos, autorizações, contratos._
- **SERVIDORES:** onde são publicadas as matérias referentes a vida funcional dos servidores.
    - _Ex.: exonerações, nomeações, designações, licenças médicas, cursos, contagem de tempo, aposentadoria, férias, etc._
- **CONCURSOS:** onde são publicadas as matérias referentes a concursos públicos.
    - _Ex.: relação de inscritos, local de provas, gabaritos de provas, classificação dos candidatos, etc._
- **EDITAIS:** onde são publicadas as matérias de conteúdo informativo.
    - _Ex.: convocação de munícipe, demonstrativo de despesas, relação de cargos e salários, balancetes, etc._
- **LICITAÇÕES:** onde são publicadas as matérias sobre certames licitatórios.
    - _Ex.: edital de abertura de convite, de concorrência pública, de tomada de preços, ata de registro de preços, ata de abertura do certame licitatório, classificação dos participantes, adjudicação do objeto, homologação do resultado, etc._
- **CÂMARA MUNICIPAL:** onde são publicados todos os atos da Câmara Municipal de São Paulo, exceto matérias sobre licitações.
- **TRIBUNAL DE CONTAS:** onde são publicados todos os atos do Tribunal de Contas do Município de São Paulo, exceto as matérias sobre licitações.

## O Projeto

O repositório esta organizado da seguinte forma:

    ├───core # O Núcleo do projeto
    │   │───dom_sp  # Arquivos do projeto principal
    │   │   ├───files_pdf
    │   │   └───outputs_ler_pdf
    │   └───querido-diario # Arquivos do projeto querido-diário
    ├───scripts # Scripts de scraping do DOM
    │   └───data_collection
    │       └───data
    │           └───3550308
    │───tools # Scripts de funcionalidades utilizadas no projetodo DOM
    └───outputs_files # Arquivos tratados

## O Estudo

Abaixo segue os passos que desenvolvi para realização do projeto:

1. **Baixar:**
    - _Para baixar o DOM utilizei o Script do projeto [Querido Diário]('https://ok.org.br/projetos/querido-diario/'). Confiram a página projeto muito legal._

2. **Organizar e Juntar arquivos PDF:**
    - _Para organizar, juntar e identificar as páginas baixadas utilizei a biblioteca `pymupdf`. Verifique meus testes para verificar qual a melhor biblioteca para trabalhar com pdfs. Em [./ler_pdf]('https://github.com/VinicusGB/sindsep-remocao_pmsp/tree/main/ler_pdf')._

3. **Converter:**
    - Para converter o arquivo final para CSV utilizei a biblioteca `tabula`. Pois é a melhor biblioteca para ler pdf's que tenham mais de uma coluna.

## Para reproduzir na sua máquina:

1. Instale o Anaconda/Python em seu computador:

2. Baixe esse repositório:

        git clone https://github.com/VinicusGB/scrapy_dom

3. Baixe o repositório do projeto querido-diario:

    <a href="https://ok.org.br/projetos/querido-diario/" target="_blank">Querido Diário</a> Confira!!!!

4. Crie um ambiente virtual:

        python -m venv env_dom

5. Ative o novo ambiente:

        source .\env_dom\bin\activate

6. Na pasta do projeto:

        pip install -r requirements.txt

7. Rode o script dom_sp:

        python dom_sp.py
