import pandas as pd
import sys
import os
import warnings

# Ignorar o aviso de estilo padrão do openpyxl
warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl')

def calcular_lucro_semanal(caminho_arquivo):
    print(f"Analisando o arquivo: {caminho_arquivo}\n")
    
    try:
        # Carregar apenas a planilha de transações
        df_trans = pd.read_excel(caminho_arquivo, sheet_name='Transaction Report', skiprows=17)
    except Exception as e:
        print(f"Erro ao ler o arquivo Excel: {e}")
        return

    # Tabela auxiliar interna (fixa no código) com os dados extraídos
    dados_auxiliares = [
        {'Valor final': 15.99, 'Custo': 10.33, 'Lucro': 5.66},
        {'Valor final': 23.52, 'Custo': 14.81, 'Lucro': 8.71},
        {'Valor final': 31.36, 'Custo': 19.29, 'Lucro': 12.07},
        {'Valor final': 39.19, 'Custo': 23.77, 'Lucro': 15.42},
        {'Valor final': 47.99, 'Custo': 28.25, 'Lucro': 19.74},
        {'Valor final': 55.99, 'Custo': 32.73, 'Lucro': 23.26},
        {'Valor final': 59.99, 'Custo': 37.21, 'Lucro': 22.78},
        {'Valor final': 75.98, 'Custo': 47.54, 'Lucro': 28.44},
        {'Valor final': 31.98, 'Custo': 20.66, 'Lucro': 11.32},
        {'Valor final': 119.98, 'Custo': 74.42, 'Lucro': 45.56},
        {'Valor final': 47.04, 'Custo': 29.62, 'Lucro': 17.42},
        {'Valor final': 19.99, 'Custo': 10.33, 'Lucro': 9.66},
        {'Valor final': 39.51, 'Custo': 25.14, 'Lucro': 14.37},
        {'Valor final': 91.36, 'Custo': 56.50, 'Lucro': 34.86},
        {'Valor final': 61.39, 'Custo': 28.25, 'Lucro': 33.14},
        {'Valor final': 94.08, 'Custo': 57.87, 'Lucro': 36.21},
        {'Valor final': 95.98, 'Custo': 56.50, 'Lucro': 39.48},
        {'Valor final': 14.80, 'Custo': 6.93, 'Lucro': 7.87},
        {'Valor final': 22.24, 'Custo': 9.71, 'Lucro': 12.53},
        {'Valor final': 29.44, 'Custo': 12.49, 'Lucro': 16.95},
        {'Valor final': 36.40, 'Custo': 15.27, 'Lucro': 21.13},
        {'Valor final': 43.12, 'Custo': 18.05, 'Lucro': 25.07},
        {'Valor final': 50.24, 'Custo': 20.83, 'Lucro': 29.41},
        {'Valor final': 54.40, 'Custo': 23.61, 'Lucro': 30.79}
    ]
    df_aux = pd.DataFrame(dados_auxiliares)
    df_aux = df_aux.sort_values('Valor final')

    # Limpar e preparar a planilha de Transações
    df_trans.columns = df_trans.columns.str.strip()
    
    if 'Tipo de transação' not in df_trans.columns:
        print("A coluna 'Tipo de transação' não foi encontrada. Verifique o formato do relatório.")
        return

    # Filtrar apenas as rendas de pedidos (entradas)
    df_renda = df_trans[df_trans['Tipo de transação'] == 'Renda do pedido'].copy()
    df_renda['Valor'] = pd.to_numeric(df_renda['Valor'], errors='coerce')
    df_renda = df_renda.dropna(subset=['Valor']).sort_values('Valor')
    
    # Converter a coluna de Data para datetime
    df_renda['Data'] = pd.to_datetime(df_renda['Data'], errors='coerce')

    # Fazer o cruzamento (merge) aproximado para lidar com diferenças de centavos (ex: 31.99 e 31.98)
    merged = pd.merge_asof(
        df_renda, 
        df_aux, 
        left_on='Valor', 
        right_on='Valor final', 
        tolerance=0.05, 
        direction='nearest'
    )

    # Identificar valores que não foram encontrados na tabela auxiliar interna
    nao_encontrados = merged[merged['Valor final'].isna()]
    
    if not nao_encontrados.empty:
        print("AVISO: Os seguintes valores de venda sao novos e nao estao mapeados no codigo")
        print("       (mesmo considerando 5 centavos de tolerancia):")
        valores_unicos = nao_encontrados['Valor'].unique()
        for v in valores_unicos:
            qtd = len(nao_encontrados[nao_encontrados['Valor'] == v])
            print(f"  - R$ {v:.2f} (aparece {qtd} vez(es))")
        print("-> Para adicionar esses valores, voce precisara atualizar a lista 'dados_auxiliares' dentro do arquivo Python.\n")

    # Filtrar apenas os que encontraram correspondência para calcular o lucro
    encontrados = merged.dropna(subset=['Valor final']).copy()
    
    if encontrados.empty:
        print("Nenhuma venda correspondente encontrada. O arquivo não tem vendas ou os valores são todos novos.")
        return

    # Criar uma coluna para a semana (começando na segunda-feira)
    encontrados['Semana'] = encontrados['Data'].dt.to_period('W-MON').apply(lambda r: r.start_time)
    
    # Agrupar por semana e calcular os totais
    resumo_semanal = encontrados.groupby('Semana').agg(
        Qtd_Vendas=('Valor', 'count'),
        Total_Vendido=('Valor', 'sum'),
        Custo_Total=('Custo', 'sum'),
        Lucro_Total=('Lucro', 'sum')
    ).reset_index()

    print("RESUMO DE LUCRO SEMANAL:")
    print("-" * 60)
    for index, row in resumo_semanal.iterrows():
        inicio_semana = row['Semana'].strftime('%d/%m/%Y')
        fim_semana = (row['Semana'] + pd.Timedelta(days=6)).strftime('%d/%m/%Y')
        
        print(f"Semana de {inicio_semana} ate {fim_semana}:")
        print(f"  Vendas mapeadas com sucesso:   {int(row['Qtd_Vendas'])}")
        print(f"  Total Vendido (bruto):         R$ {row['Total_Vendido']:.2f}")
        print(f"  Custo Total:                   R$ {row['Custo_Total']:.2f}")
        print(f"  Lucro Total da Semana:         R$ {row['Lucro_Total']:.2f}")
        print("-" * 60)
        
    lucro_total_geral = resumo_semanal['Lucro_Total'].sum()
    print(f"\nLUCRO TOTAL DO PERIODO (apenas vendas mapeadas): R$ {lucro_total_geral:.2f}")

    # ==========================================
    # GERAÇÃO DA PLANILHA EXCEL DE FECHAMENTO
    # ==========================================
    nome_arquivo_base = os.path.basename(caminho_arquivo)
    nome_sem_extensao = os.path.splitext(nome_arquivo_base)[0]
    
    # Usa o nome pedido se for o arquivo 11_18, senão cria um nome genérico
    if "11_18" in nome_sem_extensao:
        caminho_saida = "Fechamento Semanal Mai 11 a 18.xlsx"
    else:
        caminho_saida = f"Fechamento_{nome_sem_extensao}.xlsx"
        
    caminho_saida_completo = os.path.join(os.path.dirname(os.path.abspath(caminho_arquivo)), caminho_saida)
    
    # 1. Preparar Aba de Resumo
    df_resumo_export = resumo_semanal.copy()
    df_resumo_export['Semana_Inicio'] = df_resumo_export['Semana'].dt.strftime('%d/%m/%Y')
    df_resumo_export['Semana_Fim'] = (df_resumo_export['Semana'] + pd.Timedelta(days=6)).dt.strftime('%d/%m/%Y')
    df_resumo_export['Periodo'] = df_resumo_export['Semana_Inicio'] + " ate " + df_resumo_export['Semana_Fim']
    cols_resumo = ['Periodo', 'Qtd_Vendas', 'Total_Vendido', 'Custo_Total', 'Lucro_Total']
    df_resumo_export = df_resumo_export[cols_resumo]
    
    linha_total = pd.DataFrame([{
        'Periodo': 'TOTAL GERAL',
        'Qtd_Vendas': df_resumo_export['Qtd_Vendas'].sum(),
        'Total_Vendido': df_resumo_export['Total_Vendido'].sum(),
        'Custo_Total': df_resumo_export['Custo_Total'].sum(),
        'Lucro_Total': df_resumo_export['Lucro_Total'].sum()
    }])
    df_resumo_export = pd.concat([df_resumo_export, linha_total], ignore_index=True)

    # 2. Preparar Aba de Todos os Pedidos
    df_pedidos_export = encontrados.copy()
    df_pedidos_export['Data'] = df_pedidos_export['Data'].dt.strftime('%d/%m/%Y %H:%M:%S')
    df_pedidos_export = df_pedidos_export[['Data', 'Valor', 'Custo', 'Lucro']].copy()
    df_pedidos_export.rename(columns={'Valor': 'Valor Venda'}, inplace=True)
    
    # 3. Exportar
    try:
        with pd.ExcelWriter(caminho_saida_completo, engine='openpyxl') as writer:
            df_resumo_export.to_excel(writer, sheet_name='Resumo Semanal', index=False)
            df_pedidos_export.to_excel(writer, sheet_name='Todos os Pedidos', index=False)
            if not nao_encontrados.empty:
                df_nao_encontrados = pd.DataFrame({
                    'Valor da Venda (Nao Mapeado)': nao_encontrados['Valor'].value_counts().index,
                    'Quantidade de Vezes': nao_encontrados['Valor'].value_counts().values
                })
                df_nao_encontrados.to_excel(writer, sheet_name='Valores Pendentes', index=False)
        print(f"\nPLANILHA GERADA: {caminho_saida}")
        print("-> O Excel com tudo descrito foi criado na mesma pasta com sucesso!")
    except Exception as e:
        print(f"\nErro ao gerar a planilha Excel: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        caminho = sys.argv[1]
        if os.path.exists(caminho):
            calcular_lucro_semanal(caminho)
        else:
            print(f"Arquivo não encontrado: {caminho}")
            print("Verifique se o caminho ou o nome do arquivo está correto.")
    else:
        print("Por favor, informe o nome ou o caminho do arquivo.")
        print("Exemplo: python calculadora_lucro.py 11_18.xlsx")
