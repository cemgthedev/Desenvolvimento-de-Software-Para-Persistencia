import pandas as pd;
import matplotlib.pyplot as plt;

data = pd.read_table('veiculos.tsv');

years = data['Year'];
values = data['Price'];

plt.plot(values, years);
plt.show();

description = data.describe();

print("Dados da tabela: \n", data);
print("Estatísticas da tabela: \n", description);