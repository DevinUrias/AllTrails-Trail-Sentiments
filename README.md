# Seasonal Sentiment Analysis of AllTrails Reviews – Guadalupe Peak Trail
This project explores the use of Large Language Models (LLMs) in a real-world data analysis workflow. Using reviews scraped from AllTrails, we performed sentiment analysis by month for different aspects of the trail experience — with the aim of identifying seasonal trends in visitor satisfaction and opening the door for future, more advanced park system analytics.

## Overview
The primary goal was to identify monthly sentiment trends for the categories:

- Views
- Difficulty
- Crowding
- Overall Experience

From a broader perspective, this project serves as a proof of concept for how publicly available trail review data can aid in informing park management decisions, such as:

- Identifying peak seasons to push tourism or fundraising
- Planning seasonal staffing
- Scheduling maintenance or events in lower-sentiment months

While the analysis here focuses on one trail (Guadalupe Peak Trail), the workflow was designed to be adaptable to any trail with publicly available reviews.

## Data

Source: Reviews scraped from AllTrails using the Webscraper.io browser extension

Scope: 1 full year worth of reviews were scraped, totaling 589 reviews.

<img width="1000" height="600" alt="ratings_over_time" src="https://github.com/user-attachments/assets/2cc70125-7514-49f4-9040-ece28be72414" />

Fields gathered: Date, the review content, user-listed features, star rating

Example of scraped data:

```
Date,Content,Features,Rating,
7/30/25,"Review text","[{""Features"":""Feature1""},{""Features"":""Feature2""},{""Features"":""Feature3""}]",5
```

Fields to be created:
- Snippets: the specific lines used to analyze sentiment of the 4 specific target categories
- category_sent: Sentiment scores of those specific lines for that category.

LLM Integration in the Workflow
A Large Language Model (ChatGPT) was used not only to write code, but to directly contribute to the analysis process, including:

- Suggesting data cleaning and preprocessing steps
- Parsed date and features
- Droped incomplete rows
- Extracted and scored sentiment by category
- Designed regex-based keyword lexicons for category detection
<img width="657" height="121" alt="Screenshot 2025-08-11 at 6 44 31 AM" src="https://github.com/user-attachments/assets/950465d9-57a4-4359-a8c4-eb5974e1ce03" />
- Being unable to do the sentiment analysis itself it then created an entire Jupyter Notebook with structured sections and reusable functions
- Aided in debugging issues (e.g., unexpected sentiment scores, category extraction errors)
- Expanded available lexicons after analyzing reviews for common unrecognized words
- Helped develop a method of blending LLM-scored sentiment logic with fallback custom lexicons to better handle domain-specific language

## How to Recreate
Dependencies: Required libararies are numpy, pandas, matplotlib, re, and optional but highly recommended to install is vaderSentiment.

This analysis can be reproduced for any trail with available reviews by following these steps:

Scrape the Data you will be using via Webscraper.io or another scraping tool. Ensure your export includes: Date, Content, Features, Rating.

![telegram-cloud-photo-size-1-4958686184893166529-y](https://github.com/user-attachments/assets/6fc48fdf-3960-49c2-aef3-b0f2ddf79aeb)

Clean & Prepare the Data. We did this step by giving the file to the LLM and asking it to fix any formatting issues it could see at first glance. It's response was to parse the date to datetime format rather than just the string it was saved as, remove unnecessary rows, and to convert the listed features into a much more usable list. Cleaned data should be saved in the "Data" folder as "Cleaned_Trail_Reviews.csv".

Optional: Once the data is ready to be used an LLM can be consulted to expand on the category lexicon to insure more accuracy in the analysis. Relevant lists can be found in the "config" folder for editing.

Run:
```
python run_sentiment.py \
  --data Data/Cleaned_Trail_Reviews.csv \
  --config_dir config \
  --out_dir Results
```
Output files will be found in the "Results" folder

## Insights
Some patterns visible in this dataset include:
<img width="1500" height="750" alt="overall_review_monthly_sentiment" src="https://github.com/user-attachments/assets/048ab97c-cc6f-460c-b0ae-02f4619a8014" />
<img width="1500" height="750" alt="views_monthly_sentiment" src="https://github.com/user-attachments/assets/5623849b-f842-4891-a83a-9769ab3fe79d" />

There is somewhat of a similarity between overall sentiment and views sentiment scores, suggesting scenery is strongly correlated with overall satisfaction. Views sentiment peaked in October, February, and June. October and February make sense given the cooler weather expectations, with potentially clearer skies. June then might peak as it's the middle of summer vacation. Of a related note, the difficulty sentiment scores remained fairly consistent but was highest in February, perhaps implying the warming weather as winter ends encourages more novice hikers to go outside, maybe to do with new years resolutions. 
<img width="1500" height="750" alt="difficulty_monthly_sentiment" src="https://github.com/user-attachments/assets/0753ad68-7a54-4d9c-a51b-91015a05f656" />

Of interest was the realization that there might not be a strong correlation between sentiment and the rating a user gave. While the average rating was fairly consistent with little in regards to peaks or valleys, overall sentiment had noticeable peaks and valleys. It would seem that analyzing the words used really does give us more of an honest idea of the trails "true rating".

<img width="3000" height="1800" alt="rating_vs_sentiment" src="https://github.com/user-attachments/assets/7b24ba2c-47b6-405b-a6fa-41b04e15ca87" />

The peaks in view sentiments or overall sentiments show us opportunities for community engagement, events, or even fundraisers. Promoting tourism around these peaks would be optimal for the best visitor experiences. Likewise, a flexible reservation fee which adjusts around these times isn't unheard of and could bring more revenue to our parks system. Then too, the valleys show us opportunities for improvement of the facilities or possibly areas where a new approach might be useful. If a valley can be attributed to heat, maybe some after dark programs would benefit the park, set up some telescopes to view the stars, do a guided night time trek, or a camping oriented promotion/event. More than raw attendence numbers, you can use sentiment to delve deeper into any possible ideas.

### Future Work
Expanding on this project I would be interested in seeing a weekly aggregation to capture possible holiday and event-specific sentiment swings. Incorporating historical weather data to correlate conditions with review sentiment would have been my next step as well to see if any trends match with heat waves or rain. The obvious step after further fleshing out what data can be pulled is to then apply this sentiment analysis to more trails, starting to hilight park-wide seasonal patterns.

#### Repository Structure
```
config/
  categories.json # dictionary of categories observing and relevant keywords to signal the topic
  neg_words.txt # list of positive scoring words
  pos_words.txt # list of negative scoring words
Data/
  Cleaned_Trail_Reviews.csv
  GuadalupePeakTrail.csv # original scraped file
Prototype/
  Prototype1.ipynb  # full sentiment workflow
Results/
  output files go here
run_sentiment.py # run this
README.md           # this file
```
