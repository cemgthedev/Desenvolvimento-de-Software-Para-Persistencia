import pandas as pd;

# Dados de exemplo para a tabela "Veiculos"
veiculos_data = {
    "Year": [2021, 2020, 2019],
    "Make": ["Toyota", "Honda", "Ford"],
    "Model": ["Corolla", "Civic", "Focus"],
    "Description": ["Sedan", "Sedan", "Hatchback"],
    "Price": [20000, 18000, 17000]
};

# Dados de exemplo para a tabela "Funcionario"
funcionarios_data = {
    "Name": ["Alice", "Bob", "Carol"],
    "CPF": ["123.456.789-00", "987.654.321-00", "456.789.123-00"],
    "Year": [1990, 1985, 1995],
    "Gender": ["Female", "Male", "Female"],
    "Salary": [3000, 3200, 2900]
};

# Criando DataFrames
veiculos_df = pd.DataFrame(veiculos_data);
funcionarios_df = pd.DataFrame(funcionarios_data);

# Salvando no arquivo Excel com múltiplas planilhas
with pd.ExcelWriter("concessionaria.xlsx") as writer:
    veiculos_df.to_excel(writer, sheet_name="veiculos", index=False);
    funcionarios_df.to_excel(writer, sheet_name="funcionarios", index=False);

veiculos = pd.read_excel('concessionaria.xlsx', sheet_name='veiculos');
print("Tabela de veículos: \n", veiculos);

funcionarios = pd.read_excel('concessionaria.xlsx', sheet_name='funcionarios');
print("Tabela de funcionários: \n", funcionarios);