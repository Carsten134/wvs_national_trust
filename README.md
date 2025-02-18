# WVS analysis: National Trust in Germany and other Western Developed Countries
This repository contains the code used for optaining our plots, models and diagnostics. It is designed to both provide reproduceable results and create more context and transparency around the results.

**Remember, this is not the full repository. If you want to see what else we did, but didn't include in the report, you can see into [our working repo](https://github.com/ekaba007/world_value)**

## Structure of the repository
The structure follows the sections of the report:
- [`preprocessing.py`](./utils/preprocessing.py) contains our master function for preprocessing
- [`plots.ipynb`](plots.ipynb) contains the code for all the plots we used
- [`linear_regressions.ipynb`](linear_regressions.ipynb) contains all the linear regressions we ran
    - it prints out the latex tables in apa style and stores the diagnostical plots in `./plots/`
- [`jonckheere_terpstra.pdf`](jonckheere_terpstra.pdf) contains the code used to test for the trend in German national distrust
- [`linear_contrast_testing.ipynb`](linear_contrast_testing.ipynb) contains the original contrast coefficient test, we used to verify a linear trend in German national distrust.

## Setup
We have included a `requirements.txt` to reproduce the same dependencies used for this analysis. To install the dependencies first create a virtual environment and then install the dependencies using `pip` or `conda`.*Additionally, use python version 3.12*.

## Running the preprocessing
The repository does not contain the complete wave 7 and timeseries data from the WVS since the upload size to github is limited to 20MB. To run the preprocessing:
1. Download the [cross-sectional data `.csv`](https://www.worldvaluessurvey.org/WVSDocumentationWV7.jsp) and the [time-series data `.csv`](https://www.worldvaluessurvey.org/WVSDocumentationWVL.jsp) from the WVS database and put them into the `./data/wvs/` directory under the name `WVS_Cross_National.csv` and `WVS_Time_Series.csv`. 
2. After activating your environment, run `python -m util.preprocessing` **from the root directory**

