# The Conspiracy Theorist

This code collects and analyzes data from Reddit subreddits using the Reddit API and the `praw` library. It retrieves information about users who have posted in specific subreddits and identifies the other subreddits they have participated in. The collected data is saved to CSV files for further analysis.

## Usage

1. **Setup:**

   Before using the script, ensure the following:

   - Install required libraries: `pandas`, `praw`, and `prawcore`.
   - Create a Reddit application on Reddit's website to obtain `client_id`, `client_secret`, and set a `user_agent` for Reddit API access.

2. **Running the Script:**

   Execute the script in a command line or Python environment with the necessary libraries installed and configured API credentials.

3. **Code Overview:**

   The code performs these key tasks:

   - **Data Collection (`get_data_from_reddit`):** Collects data from specified subreddits by analyzing authors' comments in top "hot" submissions. Builds a dictionary mapping redditors to their posted subreddits.

   - **Iterating Over Submissions (`iterate_over_submissions`):** Processes each submission's author, extracts comments, and identifies the subreddits they participated in.

   - **Progress Printing (`print_progress`):** Displays progress during data collection, showing submissions, subreddits, and redditors processed.

   - **Saving to CSV (`save_to_csv`):** Stores collected data in a CSV file as a binary matrix, with redditors and subreddits as rows and columns.

   - **Getting Subredditors Data (`get_subredditors_data`):** Orchestrates data collection from skeptical and gullible subreddits, saving data in separate CSV files, and combining into 'together.csv'.

   - **Appending and Adding Labels (`append_and_add_label`):** Adds a label column indicating skeptical (0) or gullible (1) origin, combines datasets into 'together.csv'.

4. **Execution:**

   The `if __name__ == '__main__':` block initiates data collection using `get_subredditors_data()`, then combines data and appends labels with `append_and_add_label()`.

5. **Output:**

   The script generates 'subredditors_gul.csv' and 'subredditors_skept.csv', containing redditor-subreddit data. 'together.csv' combines datasets and includes a label column.

**Important Note:**
The code assumes predefined subreddits in `constants.py` (`SUB_SKEPT` and `SUBS_GULL`). Define these or import correctly.
