import pycountry
import numpy as np
import matplotlib.pyplot as plt

from src import utils
from src import paths
from src.standards import DataNames
from settings import Settings
import argparse

# Set up CLI
parser = argparse.ArgumentParser()
parser.add_argument("--country", type=str, default="Malawi", help="Country name")
args = parser.parse_args()

# Get country code
country_code = pycountry.countries.search_fuzzy(args.country)[0].alpha_3

print(f"Plotting data for {args.country} ({country_code})")

# load daa
(inc_df, pop_df) = utils.get_datafiles(
    cases=Settings.cases, population=Settings.population
)

years = np.array([y for y in range(Settings.years[0], Settings.years[1]+1)])
cases = inc_df[inc_df[DataNames.iso] == country_code][map(str,years)].to_numpy().flatten()


plt.figure()
plt.plot(years, cases)
plt.savefig(f"{paths.figures}/cases_{args.country}.png")
