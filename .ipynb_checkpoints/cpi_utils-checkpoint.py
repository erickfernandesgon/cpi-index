import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def plotar_graficos_cpi(df_cpi):
    """
    Plota gráficos de CPI por variação, mostrando os anos no eixo X.

    Args:
        df_cpi (pd.DataFrame): DataFrame com dados de CPI, incluindo colunas 'Date', 'CPI_Value' e 'Variacao'.

    Returns:
        None
    """
    #
    # # Configurar o layout dos subplots usando FacetGrid do Seaborn
    # g = sns.FacetGrid(df_cpi, col="Variacao", col_wrap=2, height=2.8, aspect=1.2, sharey=True, sharex=False)
    # g.map_dataframe(sns.lineplot, x="Date", y="CPI_Value", marker="o")
    # 
    # # Ajustar os rótulos dos eixos e título
    # g.set_axis_labels("", "Valor CPI")
    # g.set_titles(col_template="{col_name}", fontsize=12)  # Ajustar o tamanho da fonte dos títulos dos gráficos
    # 
    # # Formatar eixo X para mostrar apenas os anos, ajustando a rotação
    # for ax in g.axes.flat:
    #     ax.xaxis.set_major_locator(mdates.YearLocator())
    #     ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    #     ax.tick_params(axis='x', rotation=45)
    # 
    # # Ajustar layout e adicionar título geral
    # g.fig.subplots_adjust(top=0.9, hspace=0.4, wspace=0.3)  # Ajustar o espaço para o título geral e entre gráficos
    # g.fig.suptitle("Visão Geral dos Gráficos de CPI (2020-2023)", y=0.96, fontsize=16)
    # 
    # plt.tight_layout(rect=(0, 0, 1, 0.95))  # Ajustar margens para melhor visualização do título
    # plt.show()
    # 
    teste = sns.load_dataset(df_cpi)
    sns.pairplot()