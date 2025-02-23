# Reddit Conspiracy Classification

## Overview
This project classifies Reddit users as either **skeptical** or **gullible** toward conspiracy theories based on their activity across different subreddits. It collects user data, processes subreddit participation, and applies linear regression to analyze patterns and classify users accordingly.

## How It Works
1. **Data Collection:**
   - Extracts posts from selected reference subreddits.
   - Identifies users and their activity across other subreddits.
   - Saves data in CSV format for analysis.

2. **Feature Processing:**
   - Converts user-subscription data into a structured matrix.
   - Labels users as "skeptical" (0) or "gullible" (1).

3. **Classification Model:**
   - Uses linear regression to identify subreddit engagement patterns.
   - Predicts a user’s likelihood of engaging in conspiracy-related content.
   - Evaluates classification performance based on false positives and negatives.

## Running the Code
Ensure you have the required dependencies (e.g., `pandas`, `numpy`, `praw`). Then, run:
```bash
python main.py
```
This will fetch data, process it, and output classification results.

## Output
- `together.csv`: Processed dataset with user classifications.
- `results.csv`: Feature importance from the model.
- `erroravg.txt`: False positive and false negative rates.

## Notes
- Requires Reddit API credentials in `constants.py`.
- Subreddit selection affects classification accuracy.

## Results
<img width="678" alt="results" src="https://github.com/user-attachments/assets/25f67ed5-3c5f-461a-b930-023b0bc47103" />

This project provides insights into online conspiracy engagement patterns using data-driven classification methods.

