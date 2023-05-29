import pandas as pd
from datetime import datetime, timedelta

# PROJETO PARA ATUALIZAÇÃO DA CARTEIRA DOS VENDEDORES E REPRESENTANTES #

def atualizar_relatorio():

    # IMPORTAÇÃO DE TABELAS
    tab_cli = pd.read_excel('BaseClientes.xlsx')
    tab_car = pd.read_excel('BaseCarteira.xlsx')
    tab_stt = pd.read_excel('StatusClientes.xlsx')

    hoje = datetime.now()
    #   hoje = hoje.date()

    # SELEÇÃO DE CAMPOS DA TABELA DE CADASTRO DE CLIENTE
    cad_cli = tab_cli[['Cliente', 'Bairro', 'Fantasia', 'Data Iní. Cad.']]
    cad_cli.loc[cad_cli['Data Iní. Cad.'] == '00/00/0000', 'Data Iní. Cad.'] = ''
    cad_cli['Data Iní. Cad.'] = cad_cli['Data Iní. Cad.'].astype('datetime64')


    #   print(cad_cli)

    car_rep = tab_car[['ID', 'Cod', 'Repr/Vend']]

    # SELEÇÃO DE CAMPOS DO RELATÓRIO ONDE CONTEM AS INFOMAÇÕES DE ÚLTIMA COMPRA
    status_cliente = tab_stt.loc[tab_stt['Situação'] == 'A', ['Cliente', 'Data Ultima Compra']]
    status_cliente.loc[status_cliente['Data Ultima Compra'] == '00/00/0000', 'Data Ultima Compra'] = ''
    status_cliente['Data Ultima Compra'] = status_cliente['Data Ultima Compra'].astype('datetime64')

    #   nulo = status_cliente.isnull()
    #   pd.to_datetime(status_cliente['Data Ultima Compra'], format='%m/%d/%Y').date()


    # UNIÃO DAS TABELAS
    status_car = pd.merge(cad_cli, status_cliente, on='Cliente', how='left')
    cart_repr = pd.merge(status_car, car_rep, left_on='Cliente', right_on='ID', how='right')


    #ORGANIZANDO A ORDEM DAS COLUNAS
    cart_repr = cart_repr[['Repr/Vend', 'ID', 'Fantasia', 'Bairro', 'Data Iní. Cad.', 'Data Ultima Compra']]

    cart_repr['Status'] = ''


    df = cart_repr

    #   df['Data Ultima Compra'] = df['Data Ultima Compra'].str.replace('00/00/0000', '')
    #   print(df['Data Iní. Cad.'])

    #   df.astype({
    #       'ID': 'int',
    #       'Data Iní. Cad.': 'datetime64',
    #       'Data Ultima Compra': 'datetime64'
    #   })

    #   df['Data Ultima Compra'] = pd.to_datetime(df['Data Ultima Compra'], format='%d%m%Y')
    #   df['Data Ultima Compra'] = pd.to_datetime(df['Data Iní. Cad.'], format='%d%m%Y')

    print(df.dtypes)


    #   LÓGICA PARA A COMPARAÇÃO ENTRE AS COLUNAS PARA POVOAR A COLUNA 'Status'
    df.loc[(df['Data Ultima Compra'] !='0') & (df['Data Iní. Cad.'] < hoje - timedelta(days=60)), 'Status'] = 'Suspect'
    df.loc[(df['Data Ultima Compra'] !='0') & (df['Data Iní. Cad.'] > hoje - timedelta(days=60)), 'Status'] = 'Propect'
    df.loc[(df['Data Ultima Compra'] >= hoje - timedelta(days=30)) & (df['Data Iní. Cad.'] > hoje - timedelta(days=30)), 'Status'] = 'Novo'
    df.loc[(df['Data Ultima Compra'] >= hoje - timedelta(days=30)) & (df['Data Iní. Cad.'] <= hoje - timedelta(days=30)), 'Status'] = 'Ativo'
    df.loc[(df['Data Ultima Compra'] <= hoje - timedelta(days=30)) & (df['Data Iní. Cad.'] <= hoje - timedelta(days=30)), 'Status'] = 'Atenção'
    df.loc[(df['Data Ultima Compra'] <= hoje - timedelta(days=60)) & (df['Data Iní. Cad.'] <= hoje - timedelta(days=30)), 'Status'] = 'Inativo'


    print(df)

    #   EXPORTANDO PARA UM ARQUIVO EXCEL
    df.to_excel('carteiraAtualizada.xlsx')


atualizar_relatorio()