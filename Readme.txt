****AML PROJECT README****

**Required Packages**

pandas
numpy
matplotlib
Scikit-learn
seaborn
spotipy
scipy

Install missing packages via pip:

pip install pandas numpy matplotlib scikit-learn seaborn spotipy scipy

**File Structure**

The following files must be present in the same directory:

    AML_Project.ipynb
    Spotify Scraper.py
    Spotify_API_Features.csv
    Spotify_Dataset_V3.csv

**Compatibility**

All data analysis is conducted in the AML_Project.ipynb Jupyter Notebook. This notebook contains all exploratory data analysis and model results. It is written in Google Colab, which is recommended for its collapsible sections and access to far better computational resources. The file provided is compatible with Jupyter. Instructions on running Jupyter at docs.jupyter.org.

In order to run the file in Colab:

-Upload the file to Colab.

-Upload the Spotify_Dataset_V3.csv file and the locally generated Spotify_API_Features.csv to a Github Repository.

-Obtain the raw file link for both files from Github.

-In code cell 2, replace pd.read_csv("Spotify_Dataset_V3.csv", delimiter = ";") with pd.read_csv("<LINK TO Spotify_Dataset_V3.csv ON GITHUB>", delimiter = ";")

-In code cell 4, replace pd.read_csv("Spotify_API_Features.csv", index_col = 0).drop("duration_ms", axis = 1) with pd.read_csv("<LINK TO Spotify_API_Features.csv ON GITHUB", index_col = 0).drop("duration_ms", axis = 1)


**Generating Spotify API Data**

The Spotify_API_Features.csv file can be generated using Spotify Scraper.py. To do this:

-Obtain your Spotify Client ID and Secret from the Spotify for Developers Dashboard.

-Insert your Client ID and Secret in Spotify Scraper.py at lines 13 and 14, replacing YOUR CLIENT ID HERE and YOUR CLIENT SECRET HERE.

-Install Spotipy, a non-standard package, using:

pip install spotipy --upgrade

-Run the file.

**Hyperparameter Optimization**

Various hyperparameter grids were tried for hyperparameter optimization in the Random Forest models. The final hyperparameters are detailed in the report appendix. To replicate the exact results from the report, in AML_Project.ipynb:

- Locate the function "def train_rf" under the section "Optimisation and Training".
- Modify the param_grid_rf dictionary by replacing the ends of the lines after the : with the values from the report, formatted as single-value lists (e.g., [VALUE]). Alternatively, specify your own range of values as a list (e.g., [VALUE1, VALUE2, VALUE3...]).

**Running the Project**

Once Spotify_API_Features.csv is generated, and the hyperparameter grids are chosen, run AML_Project.ipynb. Graphs and tables will appear in the Exploratory Data Analysis section and results will appear as tables in the Evaluation and Feature Importances tables.

Depending on the hyperparameter grids chosen, the models can take quite a while to run. More powerful CPUs will do this quicker.