import os 
path_to_root_dir = '%s/' % (os.getcwd())

treetagger_path = path_to_root_dir + r'treetagger'
output_folder = path_to_root_dir + r'download_monthly'
download_folder = path_to_root_dir + r'download'
data_folder = path_to_root_dir + r'data/'
tmp_folder = path_to_root_dir + r'tmp'

db_offset_file = r'shared/offset.txt'
db_offset_file_full_path = path_to_root_dir + db_offset_file

articles_words_freq = 'articles_body_frequencies.json'
titles_words_freq = 'title_frequencies.json'
title_monthly_frequencies = 'title_monthly_frequencies.json'
articles_monthly_frequencies = 'articles_monthly_frequencies.json'
title_weekly_frequencies = 'title_weekly_frequencies.json'
articles_weekly_frequencies = 'articles_weekly_frequencies.json'
weekly_average_word_count = 'weekly_average_word_count.json'
monthly_average_word_count = 'monthly_average_word_count.json'

loaded_batches_full_path = r'data/db/loaded_batches.txt'
current_batch_full_path = r'data/db/current_batch.txt'
titles_word_freq_wordcloud = r'data/plots/titles_word_freq_wordcloud.png'
articles_word_freq_wordcloud = r'data/plots/articles_word_freq_wordcloud.png'
FEEL_lexicon = r'FEEL/FEEL.csv'
polarimots_lexicon = r'polarimots_1.csv'
diko_lexicon = r'diko_lexicon.txt'

# Custom Lexicons
virus_lexicon = r'virus_lexicon.txt'
death_lexicon = r'death_lexicon.txt'
vaccine_lexicon = r'vaccine_lexicon.txt'

deaths_sentiment_csv = r'deaths_sentiment.csv'
deaths_sentiment_csv_full_path = data_folder + deaths_sentiment_csv
