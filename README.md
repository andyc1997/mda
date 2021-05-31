# Modern Data Analytics - Thailand group

A repository for project on github. After 

`git clone https://github.com/andyc1997/mda.git`

please go to the corresponding directory and run: 

`pip install -r requirements.txt`

As the app needs to be deployed on Heroku, it is re-posted on another repo: 

[https://github.com/andyc1997/mda_app](https://github.com/andyc1997/mda_app)

---

The jupyter notebooks in [code](code) are organized as follows:

### Section 1: Data collection and preprocessing
* Scraping comments from the reddit post: [reddit_post.ipynb](code/reddit_post.ipynb)
* Create temperature thresholds using reference distributions: [temp_reference_dist.ipynb](code/temp_reference_dist.ipynb)

### Section 2: Data cleaning
* Clean meteorological data and mortality data for data visualization and mortality prediction model: [data_processing.ipynb](code/data_processing.ipynb) with helper functions wrapped in [subset_helper.py](code/subset_helper.py)

### Section 3: Model training and summary statistics
* Text mining for patterns in the reddit post: [text_mining.ipynb](code/text_mining.ipynb)
* Summary statistics and basic visualization for exploratory analysis: [summary_statistics.ipynb](code/summary_statistics.ipynb)
* Perform cross-validation to select the most appropriate models for mortality prediction: [model_poisson.ipynb](code/model_poisson.ipynb), [model_gradient_boosting.ipynb](code/model_gradient_boosting.ipynb), [model_randomforest.ipynb](code/model_randomforest.ipynb)

### Section 4: App development in Dash and Plotly frameworks
* Build and deploy an App for data visualization with differenet countries and mortality prediction model: [mda_app](code/mda_app)
* The App is deployed at here [https://mdaproject.herokuapp.com/](https://mdaproject.herokuapp.com/)
* If there is an application error, please refresh the webpage and try again

*Remark: As data are provided in [data](data/), the jupyter notebooks can be run in any order.*


