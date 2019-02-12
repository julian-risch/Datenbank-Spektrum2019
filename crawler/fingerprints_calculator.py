import re
import pandas as pd
import simhash


def text_to_fingerprint(text):
    text = str(text)
    tokens = re.split(r'\W+', text.lower(), flags=re.UNICODE)
    return tokens_to_fingerprint(tokens)


def tokens_to_fingerprint(tokens):
    shingles = [''.join(shingle) for shingle in simhash.shingle(''.join(tokens), 8)]
    hashes = [simhash.unsigned_hash(s.encode('utf8', 'ignore')) for s in shingles]
    return simhash.compute(hashes)


def comments_to_fingerprint(comments):
    fingerprints_of_comments = [str(bin(text_to_fingerprint(comments[i]))) for i in range((len(comments)))]
    fingerprints_of_comments_joined = ' '.join(fingerprints_of_comments)
    return text_to_fingerprint(fingerprints_of_comments_joined)


def calculate_fingerprint(comments_input_file, output_file):
    comments = pd.read_csv(comments_input_file)
    comments = comments.sort_values(by=['timestamp'])
    comments = comments.groupby('article_url')['comment_text'].apply(list)
    comments = comments.to_frame().reset_index()
    comments['fingerprint'] = comments['comment_text'].apply(comments_to_fingerprint)
    comments.to_csv(output_file, index=False)


def calculate_fingerprint_diff(row):
    return simhash.num_differing_bits(row['fingerprint_old'], row['fingerprint_new'])


def calculate_fingerprint_diff(fingerprints):
    fingerprints['fingerprint_diff'] = fingerprints.apply(calculate_fingerprint_diff, axis=1)


