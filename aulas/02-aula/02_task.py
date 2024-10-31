import pandas as pd;
import matplotlib.pyplot as plt;

data = pd.read_csv('veiculos.csv');

years = data['Year'];
values = data['Price'];

plt.plot(values, years);
plt.show();

print("Dados da tabela: \n", data);