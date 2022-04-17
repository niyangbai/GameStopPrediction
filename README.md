Stock Price Prediction with Social Media Comments
==============================

In this project, I plan to use natural language data from ***r/wallstreetbets*** during the GameStop (NYSE: GME)'s short squeeze event to build a convolutional neural network, which can predict its stock prices, and then compare it with classic time series predictive models to check its validity.

In terms of data, stock prices can be obtained directly from internet sites like the Google finance, and similarly, with the help of Reddit API, all discussions and comments during the incident can be captured. For deep learning, I plan to divide the work into several specific parts. The first is data pre-processing, which requires uniform coding of all textual information. Then comes sentence- and document-based embedding, followed by the construction of deep learning structures. For the time series analysis (baseline), I plan to estimate a classic time series model on a longer period of time without introducing the impact of social media.

Regarding potential difficulties, in terms of data processing, unlike Twitter, Reddit does not impose a limit on the number of words users can submit, which can cause very huge data load. Also, commonly used slang and network terms can also lead to biased prediction as they can be very hard for computers to recognize. For the deep learning part, different deep learning structures need to be explored and also further compared. Regarding the classic time series analysis, more information might be necessary besides only stock price.

Project Organization
------------

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io


------------
Dev log
------------
#### 17.4.2020
Rewrote `API` and `data_clean`. Started the data exploration notebook.

#### 15.4.2020
Organise the whole program with new structure.

#### 13.4.2020
Started to work on nlp and deep learning part.

#### 12.4.2020
Droped the submission without any information (they could be deleted or removed by posters).
Avioded all posts from reddit spam bots.
Converted epoch time into datetime.
Encoding problem was solved by simply using `utf-8-sig`instead of `utf-8` while writing and reading data.
Kicked noises like urls, images and emoji out. 
The next step should be locating financial related interesting topics in the whole data set.

#### 11.4.2020
Started working on coding finially. With `praw` and `pasw`, there is no need to face the ugly reddit api directly, what a relief!
Finished the first draft for data crawling, althrough it runs super slow lol.
Besides the buggy code, mian problem today is the data encoding (e.g. got `â€™` instead of `'`), it is neither `utf-8` nor `iso-8859-1`.
I am think about instead of perfectly doing everything step by step, maybe I could first make a demo or draft for the whole project to get a wider view of the problem I am facing.
