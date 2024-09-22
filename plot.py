import matplotlib.pyplot as plt
import pandas as pd

colors = {
    'Christlich Demokratische Union Deutschlands': '#000000',
    'Alternative für Deutschland': '#0096D6',
    'Bündnis Sahra Wagenknecht - Vernunft und Gerechtigkeit': '#FF8C00',
    'Sozialdemokratische Partei Deutschlands': '#E3000F',
    'BÜNDNIS 90/DIE GRÜNEN': '#64A12D',
    'DIE LINKE': '#C8102E',
    'FBrandenburger Vereinigte Bürgerbewegungen / Freie Wähler': '#FFD700',
}
abkuerzungen = {
    'Christlich Demokratische Union Deutschlands': 'CDU',
    'Alternative für Deutschland': 'AfD',
    'Bündnis Sahra Wagenknecht - Vernunft und Gerechtigkeit': 'BSW',
    'Sozialdemokratische Partei Deutschlands': 'SPD',
    'BÜNDNIS 90/DIE GRÜNEN': 'GRÜNE',
    'DIE LINKE': 'DIE LINKE',
    'FBrandenburger Vereinigte Bürgerbewegungen / Freie Wähler': 'FW',
}


df = pd.read_csv('Ergebnis.csv')
df = df[df.n_gesamtmandate > 0]

plt.style.use('ggplot')
plt.bar(df.partei, df.n_gesamtmandate, color=[colors[partei] for partei in df.partei])
# add the number of mandates on top of the bars
for i, v in enumerate(df.n_gesamtmandate):
    plt.text(i, v + 1, str(v), ha='center', va='bottom')
# rotate xlabels
plt.xticks(ticks=range(len(df.partei)), labels=[abkuerzungen[partei] for partei in df.partei])
plt.title('Sitzplatzverteilung Landtagswahl Brandenburg 2024')
plt.ylabel('Mandate')
plt.savefig('mandates.png')