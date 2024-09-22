import pandas as pd


erst = pd.read_csv('alt/Datenexport_LANDTAGSWAHL2024_Erststimme_A_BB.csv', delimiter=';')
zweit = pd.read_csv('alt/Datenexport_LANDTAGSWAHL2024_Zweitstimme_A_BB.csv', delimiter=';')

# Beschreibungen der Datensaetze
dsb_erst = pd.read_csv('DSB_Datenexport_LANDTAGSWAHL2024_Erststimme_A_BB.csv', delimiter=';', encoding='unicode_escape')
dsb_zweit = pd.read_csv('DSB_Datenexport_LANDTAGSWAHL2024_Zweitstimme_A_BB.csv', delimiter=';', encoding='unicode_escape')

erst = erst[erst.Gebietsart == 'Landtagswahlkreis']
zweit = zweit[zweit.Gebietsart == 'Landtagswahlkreis']

# select columns that match the pattern "P**" with * being a digit
erst = erst.filter(regex='P\d{2,3}$')
zweit = zweit.filter(regex='P\d{2,3}$')

dsb_erst = dsb_erst.dropna()
dsb_erst = dsb_erst[dsb_erst['1. Allgemeines'].str.match('P\d{2,3}$')]
dsb_erst = dsb_erst[dsb_erst['Unnamed: 1'] != 'nicht besetzt, kein Ergebniseingang']
dsb_erst = dsb_erst.rename(columns={'1. Allgemeines': 'abk', 'Unnamed: 1': 'Name'})
dsb_zweit = dsb_zweit.dropna()
dsb_zweit = dsb_zweit[dsb_zweit['1. Allgemeines'].str.match('P\d{2,3}$')]
dsb_zweit = dsb_zweit[dsb_zweit['Unnamed: 1'] != 'nicht besetzt, kein Ergebniseingang']
dsb_zweit = dsb_zweit.rename(columns={'1. Allgemeines': 'abk', 'Unnamed: 1': 'Name'})

# $2 Im Wahlkreis ist die oder der Bewerbende gewählt, die oder der die meisten Stimmen erhalten hat.
# Bei Stimmengleichheit entscheidet das von der Kreiswahlleiterin oder dem Kreiswahlleiter zu ziehende Los.

erst['max'] = erst.max(axis=1)
erst['anzahl'] = erst.apply(lambda row: (row == row['max']).sum(), axis=1)
if erst['anzahl'].max() > 2:
    raise ValueError('Wahlleiter muss losen.')

erst['gewinner'] = erst.idxmax(axis=1)
# replace gewinner names with the corresponding party names in dsb_erst
erst['gewinner'] = erst['gewinner'].replace(dsb_erst.set_index('abk').Name.to_dict())
erst = erst.gewinner.value_counts().reindex(dsb_erst.Name).fillna(0).astype(int)

zweit = zweit.rename(columns=dsb_zweit.set_index('abk').Name.to_dict())
zweit = zweit.sum()
zweit = zweit.reindex(dsb_zweit.Name).fillna(0).astype(int)

df = pd.concat([erst, zweit], axis=1).fillna(0).astype('int64')
df.index.name = 'partei'
df = df.rename(columns={'count': 'n_direkt_mandate', 0: 'n_listenstimmen'})

df.to_csv('bereinigt.csv')