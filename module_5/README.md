# Goal of the project
The goal of the project is to predict the price of the used car for unknown test data which was parsed from auto.ru site in 2020.
Model quality metric: MAPE - Mean Absolute Percentage Error.

# Project description
Project includes 2 notebooks developed in DataSpell IDE and located in github repository.

Notebook Parsing.ipynb was used for parsing data from auto.ru.

Notebook Car_price_prediction.ipynb is the main notebook of the project. All main conclusions are presented in this notebook.

In order to upload large files with parsed and test data to github without using git-lfs (it is allowed only < 100 Mb files), these files were archived and located in Data directories of the project:

/Parsing/Data/parsed_car_data_all__06_02_2022.7z

/Data/test.zip

# Final metric
Finally we get ~6% MAPE for our test data and 16.3% MAPE on submission (parsing - 6.02.2022, submission - 16.02.2022).




