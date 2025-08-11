Seasonal Sentiment Analysis of AllTrails Reviews – Guadalupe Peak Trail
This project explores the use of Large Language Models (LLMs) in a real-world data analysis workflow. Using reviews scraped from AllTrails, we performed sentiment analysis by month for different aspects of the trail experience — with the aim of identifying seasonal trends in visitor satisfaction and opening the door for future, more advanced park system analytics.

Overview
The primary goal was to identify monthly sentiment trends for the categories:

Views

Difficulty

Crowding

Overall Experience

From a broader perspective, this project serves as a proof of concept for how publicly available trail review data can inform park management decisions, such as:

Identifying peak seasons to push tourism or fundraising

Planning seasonal staffing

Scheduling maintenance or events in lower-sentiment months

While the analysis here focuses on one trail (Guadalupe Peak Trail), the workflow was designed to be adaptable to any trail with publicly available reviews.

Data
Source: Reviews scraped from AllTrails using the Webscraper.io browser extension

Scope: 589 reviews spanning the past year (last month dropped due to insufficient data)

Fields used: Date, review content, user-listed features, star rating

Format: CSV

LLM Integration in the Workflow
A Large Language Model (ChatGPT) was used not only to write code, but to directly contribute to the analysis process, including:

Suggesting data cleaning and preprocessing steps

Writing code to:

Parse date and features

Drop incomplete rows

Extract and score sentiment by category

Designing regex-based keyword lexicons for category detection

Creating an entire starter Jupyter Notebook with structured sections and reusable functions

Debugging issues (e.g., unexpected sentiment scores, category extraction errors)

Expanding lexicons after inspecting common unrecognized words

Blending LLM-scored sentiment logic with fallback custom lexicons to better handle domain-specific language

Explaining complex aggregation and grouping logic to ensure understanding

This iterative back-and-forth meant the LLM was acting as:

Coding assistant

Domain-specific logic designer

Teaching tool for methods used

How to Recreate
This analysis can be reproduced for any trail with available reviews by following these steps:

Scrape the Data

Use Webscraper.io or another scraping tool to export reviews from AllTrails.

Ensure your export includes: Date, Content, Features, Rating.

Clean & Prepare the Data (via LLM-assisted code)

Parse Date to datetime format

Remove rows with missing values

Extract features from stringified JSON

Convert text to lowercase for analysis

Define Categories & Lexicons (LLM-generated and refined)

Categories: Views, Difficulty, Crowding, Overall

Regex patterns to identify relevant sentences in each category

Domain-specific positive/negative word lists for fallback sentiment scoring

Set Up Sentiment Scoring (LLM-coded blending approach)

Use VADER for general sentiment

Fall back to custom lexicon scoring when VADER is unavailable or to better capture trail-specific terms

Blend scores to capture both general tone and domain relevance

Run Monthly Aggregation (LLM-explained and debugged)

Convert dates to monthly buckets

Group by month, computing mean sentiment per category and average rating

Flatten results into a tidy table for analysis

Visualize Trends

Plot monthly sentiment lines per category

Compare with monthly average ratings

Interpret Results (human-led, LLM-assisted suggestions)

Look for seasonal highs/lows per category

Identify months with high positive Views sentiment

Identify months with negative Crowding sentiment

Insights
Some patterns visible in this dataset include:

Views sentiment peaked in October and February, both cooler months with potentially clearer skies.

Crowding sentiment showed notable negativity in June, possibly due to summer traffic.

Difficulty sentiment remained fairly consistent but was highest in February, perhaps due to more favorable hiking weather.

Overall review sentiment closely followed Views sentiment, suggesting scenery is a major driver of total satisfaction.

(Plots and screenshots illustrating these trends will be included in the repo.)

Libraries Used
pandas – data loading, cleaning, aggregation

numpy – numerical calculations

matplotlib – plotting

scikit-learn – tokenizing review text for keyword analysis

vaderSentiment – sentiment scoring (optional)

re – regex-based keyword matching

Future Work
Add weekly aggregation to capture holiday and event-specific sentiment swings

Incorporate historical weather data to correlate conditions with review sentiment

Apply workflow to multiple trails to identify park-wide seasonal patterns

Integrate LLMs for automatic category discovery instead of predefined lexicons

Repository Structure

Data/
  Cleaned_Trail_Reviews.csv
Prototype/
  Prototype1.ipynb  # full sentiment workflow
README.md           # this file
