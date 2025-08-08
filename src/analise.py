import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import re

def clean_price(price_str):
    """
    Limpa e converte string de preço para float
    """
    if pd.isna(price_str) or price_str == "N/A":
        return np.nan
    
    # Remove 'R$' e espaços, substitui ',' por '.'
    cleaned = re.sub(r'R\$\s*', '', str(price_str))
    cleaned = cleaned.replace(',', '.')
    
    try:
        return float(cleaned)
    except ValueError:
        return np.nan

def categorize_product(product_name):
    """
    Categoriza produtos por tipo de alimento
    """
    product_lower = product_name.lower()
    
    if 'arroz' in product_lower:
        return 'Arroz'
    elif 'feijão' in product_lower or 'feijao' in product_lower:
        return 'Feijão'
    elif 'leite' in product_lower:
        return 'Leite'
    elif 'carne' in product_lower:
        return 'Carne'
    elif 'pão' in product_lower or 'pao' in product_lower:
        return 'Pão'
    elif 'óleo' in product_lower or 'oleo' in product_lower:
        return 'Óleo'
    elif 'ovos' in product_lower or 'ovo' in product_lower:
        return 'Ovos'
    else:
        return 'Outros'

def analyze_and_visualize(file_path="data/precos_mercados.csv"):
    """
    Realiza análise comparativa de preços e gera visualizações
    """
    try:
        df = pd.read_csv(file_path)
        print(f"Dados carregados: {len(df)} produtos encontrados")
    except FileNotFoundError:
        print(f"Erro: O arquivo {file_path} não foi encontrado.")
        return
    
    # Limpeza e conversão de dados
    df['Preço_Limpo'] = df['Preço'].apply(clean_price)
    df['Categoria'] = df['Produto'].apply(categorize_product)
    
    # Remove produtos sem preço válido
    df_clean = df.dropna(subset=['Preço_Limpo'])
    
    print(f"\nDados após limpeza: {len(df_clean)} produtos válidos")
    print(f"Supermercados analisados: {', '.join(df_clean['Supermercado'].unique())}")
    print(f"Categorias encontradas: {', '.join(df_clean['Categoria'].unique())}")
    
    # Análise estatística por categoria
    print("\n" + "="*60)
    print("ANÁLISE COMPARATIVA DE PREÇOS POR CATEGORIA")
    print("="*60)
    
    analysis_by_category = df_clean.groupby('Categoria')['Preço_Limpo'].agg([
        ('Média', 'mean'),
        ('Menor_Preço', 'min'),
        ('Maior_Preço', 'max'),
        ('Desvio_Padrão', 'std'),
        ('Quantidade', 'count')
    ]).round(2)
    
    print(analysis_by_category)
    
    # Análise por supermercado
    print("\n" + "="*60)
    print("ANÁLISE COMPARATIVA POR SUPERMERCADO")
    print("="*60)
    
    analysis_by_market = df_clean.groupby('Supermercado')['Preço_Limpo'].agg([
        ('Preço_Médio', 'mean'),
        ('Menor_Preço', 'min'),
        ('Maior_Preço', 'max'),
        ('Quantidade_Produtos', 'count')
    ]).round(2)
    
    print(analysis_by_market)
    
    # Configuração de estilo para os gráficos
    plt.style.use('default')
    sns.set_palette("husl")
    
    # Gráfico 1: Comparativo de preços médios por categoria e supermercado
    plt.figure(figsize=(14, 8))
    
    # Calcular preços médios por categoria e supermercado
    avg_prices = df_clean.groupby(['Categoria', 'Supermercado'])['Preço_Limpo'].mean().reset_index()
    
    sns.barplot(data=avg_prices, x='Categoria', y='Preço_Limpo', hue='Supermercado')
    plt.title('Comparativo de Preços Médios por Categoria e Supermercado', fontsize=16, fontweight='bold')
    plt.xlabel('Categoria de Produto', fontsize=12)
    plt.ylabel('Preço Médio (R$)', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.legend(title='Supermercado', loc='upper left')
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig('precos_por_categoria_supermercado.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # Gráfico 2: Distribuição de preços por supermercado
    plt.figure(figsize=(12, 6))
    
    sns.boxplot(data=df_clean, x='Supermercado', y='Preço_Limpo')
    plt.title('Distribuição de Preços por Supermercado', fontsize=16, fontweight='bold')
    plt.xlabel('Supermercado', fontsize=12)
    plt.ylabel('Preço (R$)', fontsize=12)
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig('distribuicao_precos_supermercado.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # Gráfico 3: Comparativo de preços por categoria (violin plot)
    plt.figure(figsize=(14, 8))
    
    sns.violinplot(data=df_clean, x='Categoria', y='Preço_Limpo', hue='Supermercado')
    plt.title('Distribuição Detalhada de Preços por Categoria', fontsize=16, fontweight='bold')
    plt.xlabel('Categoria de Produto', fontsize=12)
    plt.ylabel('Preço (R$)', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.legend(title='Supermercado', loc='upper left')
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig('distribuicao_detalhada_precos.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # Análise de economia potencial
    print("\n" + "="*60)
    print("ANÁLISE DE ECONOMIA POTENCIAL")
    print("="*60)
    
    economy_analysis = []
    for category in df_clean['Categoria'].unique():
        category_data = df_clean[df_clean['Categoria'] == category]
        if len(category_data['Supermercado'].unique()) > 1:
            avg_by_market = category_data.groupby('Supermercado')['Preço_Limpo'].mean()
            cheapest_market = avg_by_market.idxmin()
            most_expensive_market = avg_by_market.idxmax()
            potential_savings = avg_by_market.max() - avg_by_market.min()
            savings_percentage = (potential_savings / avg_by_market.max()) * 100
            
            economy_analysis.append({
                'Categoria': category,
                'Mais_Barato': cheapest_market,
                'Preço_Médio_Menor': round(avg_by_market.min(), 2),
                'Mais_Caro': most_expensive_market,
                'Preço_Médio_Maior': round(avg_by_market.max(), 2),
                'Economia_Potencial': round(potential_savings, 2),
                'Economia_Percentual': round(savings_percentage, 1)
            })
    
    economy_df = pd.DataFrame(economy_analysis)
    print(economy_df.to_string(index=False))
    
    # Salvar análises em arquivo
    with open('analise_precos_resultado.txt', 'w', encoding='utf-8') as f:
        f.write("RELATÓRIO DE ANÁLISE DE PREÇOS DE ALIMENTOS BÁSICOS\n")
        f.write("="*60 + "\n\n")
        
        f.write("RESUMO EXECUTIVO:\n")
        f.write(f"- Total de produtos analisados: {len(df_clean)}\n")
        f.write(f"- Supermercados comparados: {', '.join(df_clean['Supermercado'].unique())}\n")
        f.write(f"- Categorias analisadas: {', '.join(df_clean['Categoria'].unique())}\n\n")
        
        f.write("ANÁLISE POR CATEGORIA:\n")
        f.write(analysis_by_category.to_string())
        f.write("\n\n")
        
        f.write("ANÁLISE POR SUPERMERCADO:\n")
        f.write(analysis_by_market.to_string())
        f.write("\n\n")
        
        f.write("OPORTUNIDADES DE ECONOMIA:\n")
        f.write(economy_df.to_string(index=False))
        f.write("\n\n")
        
        f.write("CONCLUSÕES:\n")
        f.write("Este projeto demonstra como o web scraping pode ser usado para promover\n")
        f.write("transparência de preços e ajudar consumidores a tomar decisões mais\n")
        f.write("informadas sobre suas compras de alimentos básicos.\n")
    
    print(f"\n✅ Análise completa salva em 'analise_precos_resultado.txt'")
    print(f"✅ Gráficos salvos como PNG na pasta atual")
    
    return df_clean

if __name__ == "__main__":
    df_result = analyze_and_visualize()
    print("\n🎉 Análise concluída com sucesso!")

