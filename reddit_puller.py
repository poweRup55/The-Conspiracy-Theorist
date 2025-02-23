import pandas as pd
import praw
import prawcore

from constants import *

# Reddit API config
API_KEY = ''
CLIENT_ID= ''
USER_AGENT = ''

# CONSTANTS
GULLIBLE_CSV = 'subredditors_gul' + ".csv"
SKEPTICAL_CSV = 'subredditors_skept' + ".csv"



def get_data_from_reddit(reference_subreddits_list):
    """
    from each subreddit in subreddits_list, find the redditors that have posted in said subreddit and get
    on which other subreddits have they been posting on.
    :param reference_subreddits_list: list of subreddits to grab info from.
    :return: Dict of redditors and the subreddits that they have posted in and a set of all seen subreddits
    """
    reddit = praw.Reddit(client_id=CLIENT_ID,
                         client_secret=API_KEY,
                         user_agent=USER_AGENT)  # start reddit API
    redditor_sub_to = dict()  # dictionary of redditors and the subreddits they are in
    subreddits = set()  # A set of all collected subreddits
    redditors = set()  # A set of all collected redditors
    for index_of_subreddit in range(len(reference_subreddits_list)):
        submissions = reddit.subreddit(reference_subreddits_list[index_of_subreddit]).hot(
            limit=1000)  # 1000 most hot submissions in a given subreddit
        iterate_over_submissions(submissions, index_of_subreddit, redditor_sub_to, redditors,
                                 subreddits, reference_subreddits_list)
    return redditor_sub_to, subreddits


def iterate_over_submissions(submissions, index_of_subreddit, redditor_sub_to, redditors, subreddits,
                             reference_subreddits_list):
    """
    Iterates over each submission of the 1000 most hot submissions in a given subreddit
    and looks where the author has also commented.
    :param submissions: 1000 most hot submissions in a given subreddit
    :param index_of_subreddit: The index of the subreddit in the reference_subreddits_list
    :param redditor_sub_to: dictionary of redditors and the subreddits they are in
    :param redditors: A set of all collected redditors
    :param subreddits: A set of all collected subreddits
    :param reference_subreddits_list: list of subreddits to grab info from.
    """
    progress_counter = 0
    for submission in submissions:  # For each post in all the hot 1000 of the subreddit.
        print_progress(index_of_subreddit, progress_counter, redditors, subreddits, reference_subreddits_list)
        # Get auther of post
        author = submission.author
        if author == None or author is None:
            continue
        if author in redditors:
            continue
        redditors.add(author)
        # Find other subreddits of auther
        try:
            author_subreddits = set()
            for comment in author.comments.top('all'):
                comment_subreddit = comment.subreddit.display_name
                subreddits.add(comment_subreddit)
                author_subreddits.add(comment_subreddit)
            redditor_sub_to[author.name] = author_subreddits
        # praw API Exceptions - continue
        except prawcore.exceptions.NotFound:
            continue
        except prawcore.exceptions.Forbidden:
            continue
    print("Search in " + reference_subreddits_list[index_of_subreddit] + " has completed with " + str(
        len(subreddits)) + " subreddits and " + str(len(redditors)) + " redditors")


def print_progress(index_of_subreddit, progress_counter, redditors, subreddits, reference_subreddits_list):
    """
    Prints the progress of the reddit puller
    :param index_of_subreddit: The index of the subreddit in the reference_subreddits_list
    :param progress_counter: Total progress counter
    :param redditors: A set of all collected redditors
    :param subreddits: A set of all collected subreddits
    :param reference_subreddits_list: list of subreddits to grab info from.
    """
    progress_counter += 1
    if progress_counter % 10 == 0:
        print("Searching submissions in " + reference_subreddits_list[index_of_subreddit] + " has checked " + str(
            progress_counter) + " submissions with " + str(len(subreddits)) + " subreddits and " + str(
            len(redditors)) + " redditors")


def save_to_csv(redditor_sub_to, subreddits, csv_name):
    """
    Saves subreddits and redditors to csv_name
    :param redditor_sub_to: dictionary of redditors and the subreddits they are in
    :param subreddits: A set of all collected subreddits
    :param csv_name: csv file name to save to
    """
    subreddits = list(subreddits)
    csv_file = dict()
    for redditor in redditor_sub_to.keys():
        line_of_zeros = [0] * len(subreddits)
        for i in range(len(subreddits)):
            if subreddits[i] in redditor_sub_to[redditor]:  # if in the subreddit, fill with 1
                line_of_zeros[i] = 1
        csv_file[redditor] = line_of_zeros
    csv_file = pd.DataFrame.from_dict(csv_file, orient="index", columns=subreddits)
    csv_file.to_csv(csv_name + 'csv', header=True)


def get_subredditors_data():
    # Get redditors and subreddits from the skeptical database
    redditors_skept, subreddits_skept = get_data_from_reddit(SUB_SKEPT)
    save_to_csv(redditors_skept, subreddits_skept, SKEPTICAL_CSV)
    # Get redditors and subreddits from the gullible database
    redditors_gull, subreddits_gull = get_data_from_reddit(SUBS_GULL)
    save_to_csv(redditors_gull, subreddits_gull, GULLIBLE_CSV)


def append_and_add_label():
    # Append and add label
    skeptical = pd.read_csv(SKEPTICAL_CSV)  # Reads skeptical csv
    skeptical.insert(1, G_O_METER, [0] * skeptical.index.size)  # Add label - 0
    gullible = pd.read_csv(GULLIBLE_CSV)  # Reads gullible csv
    gullible.insert(1, G_O_METER, [1] * gullible.index.size)  # Add label - 1
    together = gullible.append(skeptical, ignore_index=True, sort=False)
    together.to_csv('together.csv', header=True)


if __name__ == '__main__':
    get_subredditors_data()
    append_and_add_label()
