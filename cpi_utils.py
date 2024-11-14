import os
import json
import requests
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from dotenv import load_dotenv

# Carregar as variáveis de ambiente
load_dotenv()

# Configuração da API
API_KEY = os.getenv("BLS_API_KEY")
API_URL = "https://api.bls.gov/publicAPI/v2/timeseries/data/"

def fetch_data(series_id, start_year="2020", end_year="2023"):
    """
    Faz a solicitação dos dados para a API BLS.
    """
    payload = {
        "seriesid": [series_id],
        "startyear": start_year,
        "endyear": end_year,
        "registrationkey": API_KEY
    }
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(API_URL, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        return response.json() if response.status_code == 200 else None
    except requests.exceptions.RequestException as e:
        print(f"Erro ao se comunicar com a API: {e}")
        return None

def process_data(data, titulo):
    """
    Processa os dados recebidos da API e organiza em um DataFrame.
    """
    cpi_data = []

    if "Results" in data and "series" in data["Results"]:
        series_data = data["Results"]["series"][0]["data"]
        for entry in series_data:
            try:
                year = int(entry["year"])
                month = entry["period"]
                value = float(entry["value"])
                if month.startswith("M"):
                    month_num = int(month[1:])
                    date_str = f"{year}-{month_num:02d}"
                    cpi_data.append({"Date": date_str, "CPI_Value": value, "Titulo": titulo})
            except (ValueError, KeyError) as e:
                print(f"Erro ao processar entrada: {entry}. Detalhes: {e}")

    return pd.DataFrame(cpi_data)

def obter_dados_cpi(cpi_variations):
    """
    Obtém os dados de todas as variações do CPI e concatena em um único DataFrame.
    """
    dados_cpi = []

    for cpi in cpi_variations:
        print(f"Obtendo dados para: {cpi['Titulo']} ({cpi['series_id']})...")
        raw_data = fetch_data(cpi["series_id"])
        if raw_data:
            df_cpi = process_data(raw_data, cpi["Titulo"])
            if not df_cpi.empty:
                dados_cpi.append(df_cpi)

    return pd.concat(dados_cpi, ignore_index=True) if dados_cpi else pd.DataFrame()

def plotar_graficos_cpi_pdf(df_cpi, arquivo_pdf="graficos_cpi.pdf"):
    """
    Salva os gráficos das variações do CPI em um arquivo PDF.
    """
    sns.set_theme(style="whitegrid")
    categorias = df_cpi["Titulo"].unique()
    n_graficos = len(categorias)
    colunas = 2
    linhas = (n_graficos + 1) // colunas

    with PdfPages(arquivo_pdf) as pdf:
        fig, axes = plt.subplots(linhas, colunas, figsize=(14, linhas * 4))
        axes = axes.flatten()

        cores = sns.color_palette("husl", n_graficos)
        fig.suptitle("Visão Geral dos Gráficos de CPI (2020-2023)", fontsize=18, weight='bold', y=0.98)

        for i, (categoria, cor) in enumerate(zip(categorias, cores)):
            dados_categoria = df_cpi[df_cpi["Titulo"] == categoria]
            ax = axes[i]
            ax.plot(dados_categoria["Date"], dados_categoria["CPI_Value"], label=categoria, color=cor, linewidth=2)
            ax.set_title(categoria, fontsize=16, weight='bold', color=cor)
            ax.tick_params(axis='x', labelrotation=45)
            ax.grid(True, linestyle='--', alpha=0.7)

        for j in range(i + 1, len(axes)):
            fig.delaxes(axes[j])

        plt.tight_layout(rect=[0, 0, 1, 0.95])
        plt.savefig("img/exemplo_grafico.png", dpi=300, bbox_inches="tight")
        pdf.savefig(fig)
        plt.close(fig)

    print(f"Gráficos salvos em {arquivo_pdf} com sucesso!")
