import pandas as pd;
import matplotlib.pyplot as plt;

# Objetivo 1 - Carregar o csv
vendas = pd.read_csv('vendas.csv');

# Objetivo 2 - Calcular o total de vendas por produto
vendas["Total_Venda"] = vendas["Quantidade"] * vendas["Preco_Unitario"];

# Objetivo 3 - Filtrar vendas por data
vendas["Data"] = pd.to_datetime(vendas["Data"], format="%d/%m/%Y");
vendas_janeiro = vendas[(vendas["Data"].dt.month == 1) & (vendas["Data"].dt.year == 2023)];

# Objetivo 4 - Salvar os resultados
vendas_janeiro.to_csv('vendas_janeiro.csv', index=False);    
vendas_por_produto = vendas.groupby("Produto")["Total_Venda"].sum();  
with pd.ExcelWriter("total_vendas_produto.xlsx") as writer:
    for produto, total in vendas_por_produto.items():
        df_produto = pd.DataFrame({"Produto": [produto], "Total_Venda": [total]});
        df_produto.to_excel(writer, sheet_name=produto, index=False);

# Objetivo 5 - Plotar o gráfico
vendas_por_produto.plot(kind="bar");
plt.show()