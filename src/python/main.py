import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Diretórios
script_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.dirname(script_dir)
nome_arquivo_csv = os.path.join(src_dir, 'data', 'data_esp32.csv')
output_folder = os.path.join(src_dir, 'graficos')
os.makedirs(output_folder, exist_ok=True)

# Leitura dos dados
try:
    df = pd.read_csv(nome_arquivo_csv)
except Exception as e:
    print(f"Erro ao ler o arquivo CSV: {e}")
    exit(1)

# Verifica colunas essenciais
colunas_essenciais = ['Timestamp_ms', 'Temperatura_C', 'Corrente_A', 'Magnitude_Vibracao', 'Vibracao_Detectada']
for col in colunas_essenciais:
    if col not in df.columns:
        print(f"Coluna obrigatória ausente: {col}")
        exit(1)

df['Timestamp_s'] = df['Timestamp_ms'] / 1000
print("Dados carregados com sucesso. Primeiras 5 linhas:")
print(df.head())

sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['axes.titlesize'] = 16
plt.rcParams['axes.labelsize'] = 12

# Modelo 1: Séries temporais
fig, axes = plt.subplots(3, 1, figsize=(15, 12), sharex=True)
fig.suptitle('Modelo 1: Análise de Séries Temporais das Variáveis', fontsize=20)

axes[0].plot(df['Timestamp_s'], df['Temperatura_C'], color='r', label='Temperatura (°C)')
axes[0].set_ylabel('Temperatura (°C)')
axes[0].set_title('Temperatura ao Longo do Tempo')
axes[0].legend()

axes[1].plot(df['Timestamp_s'], df['Corrente_A'], color='b', label='Corrente (A)')
axes[1].set_ylabel('Corrente (A)')
axes[1].set_title('Corrente ao Longo do Tempo')
axes[1].legend()

axes[2].plot(df['Timestamp_s'], df['Magnitude_Vibracao'], color='g', label='Magnitude da Vibração')
detected_vibrations = df[df['Vibracao_Detectada'] == 1]
axes[2].scatter(detected_vibrations['Timestamp_s'], detected_vibrations['Magnitude_Vibracao'], color='purple', zorder=5, label='Vibração Detectada')
axes[2].set_xlabel('Tempo (s)')
axes[2].set_ylabel('Magnitude da Vibração')
axes[2].set_title('Vibração ao Longo do Tempo')
axes[2].legend()

plt.tight_layout(rect=[0, 0.03, 1, 0.96])
plt.savefig(os.path.join(output_folder, 'grafico_modelo_1_series_temporais.png'))
plt.clf()

# Modelo 2: Correlação Corrente x Temperatura
plt.figure(figsize=(10, 7))
sns.scatterplot(data=df, x='Corrente_A', y='Temperatura_C', hue='Vibracao_Detectada', palette='coolwarm', s=100)
plt.title('Modelo 2: Correlação entre Corrente e Temperatura', fontsize=16)
plt.xlabel('Corrente (A)')
plt.ylabel('Temperatura (°C)')
plt.legend(title='Vibração Detectada?')
plt.savefig(os.path.join(output_folder, 'grafico_modelo_2_correlacao.png'))
plt.clf()

# Modelo 3: Análise da Vibração
fig, axes = plt.subplots(1, 2, figsize=(16, 7))
fig.suptitle('Modelo 3: Análise da Vibração', fontsize=20)
vibrations_only = df[df['Vibracao_Detectada'] == 1]['Magnitude_Vibracao']
sns.histplot(vibrations_only, bins=15, kde=True, ax=axes[0], color='purple')
axes[0].set_title('Distribuição da Magnitude das Vibrações')
axes[0].set_xlabel('Magnitude da Vibração')
axes[0].set_ylabel('Contagem')
sns.countplot(data=df, x='Vibracao_Detectada', ax=axes[1], palette='pastel')
axes[1].set_title('Contagem de Eventos com e sem Vibração')
axes[1].set_xlabel('Vibração Foi Detectada?')
axes[1].set_xticklabels(['Não (0)', 'Sim (1)'])
axes[1].set_ylabel('Número de Leituras')
plt.tight_layout(rect=[0, 0.03, 1, 0.96])
plt.savefig(os.path.join(output_folder, 'grafico_modelo_3_distribuicao_vibracao.png'))
plt.clf()

# Modelo 4: Boxplot Vibração x Corrente
df['Nivel_Corrente'] = pd.qcut(df['Corrente_A'], q=3, labels=['Baixa', 'Média', 'Alta'])
plt.figure(figsize=(12, 8))
sns.boxplot(data=df, x='Nivel_Corrente', y='Magnitude_Vibracao', palette='viridis')
plt.title('Modelo 4: Magnitude da Vibração por Nível de Corrente', fontsize=16)
plt.xlabel('Nível de Corrente do Equipamento')
plt.ylabel('Magnitude da Vibração')
plt.savefig(os.path.join(output_folder, 'grafico_modelo_4_boxplot_vibracao_corrente.png'))
plt.clf()

# Modelo 5: Heatmap de Correlação
plt.figure(figsize=(10, 7))
corr_matrix = df[['Temperatura_C', 'Corrente_A', 'Magnitude_Vibracao']].corr()
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Modelo 5: Mapa de Calor das Correlações', fontsize=16)
plt.savefig(os.path.join(output_folder, 'grafico_modelo_5_heatmap.png'))
plt.clf()

print(f"\nOperação concluída! Os 5 gráficos foram salvos na pasta '{output_folder}'.")