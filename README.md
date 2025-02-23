# The Conspiracy Theorist  

This script analyzes Reddit activity using the `praw` library, identifying subreddits where users have posted. Data is saved as CSV files for further analysis.  

## Setup  

1. Install dependencies: `pandas`, `praw`, and `prawcore`.  
2. Create a Reddit app to obtain `client_id`, `client_secret`, and `user_agent`.  

## How It Works  

- **Data Collection (`get_data_from_reddit`)**: Scrapes authors from top posts in target subreddits and maps them to other subreddits they participate in.  
- **Processing Submissions (`iterate_over_submissions`)**: Extracts authors and their comments across subreddits.  
- **Progress Display (`print_progress`)**: Tracks processed submissions, subreddits, and users.  
- **Saving Data (`save_to_csv`)**: Stores results in a CSV binary matrix (users × subreddits).  
- **Managing Subreddit Data (`get_subredditors_data`)**: Collects data from skeptical and gullible subreddits, saving them separately.  
- **Labeling & Merging (`append_and_add_label`)**: Adds a classification column (skeptical = 0, gullible = 1) and merges datasets into `together.csv`.  

## Execution  

Running the script (`if __name__ == '__main__':`) triggers `get_subredditors_data()` and `append_and_add_label()`, producing:  

- `subredditors_gul.csv` & `subredditors_skept.csv` – Raw subreddit-user data.  
- `together.csv` – Combined dataset with labels.  

**Note:** Ensure `constants.py` defines `SUB_SKEPT` and `SUBS_GULL`, or import them correctly.
