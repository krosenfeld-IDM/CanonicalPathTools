# Scripts settings, put data file names here
import sciris as sc

class Settings(sc.prettyobj):
    cases: str = 'measlescasedata.csv'
    population: str = 'API_SP.POP.TOTL_DS2_en_csv_v2_84031.csv'
    years: list = [1974, 2022] # [start, end] years
