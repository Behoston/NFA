import argparse
import collections
import random
import re

Prob = collections.namedtuple('Prob', ['words', 'probs'])


def calculate_probabilities(text_file) -> {str: collections.Counter}:
    probabilities = collections.defaultdict(collections.Counter)
    for line in text_file:
        for word in line.strip().split():
            word = clean_word(word)
            word_length = len(word)
            for i in range(word_length - 3):
                probabilities[word[i:i + 2]].update([word[i + 2:i + 4]])
    return probabilities


def convert_probabilities(probabilities: {str: collections.Counter}) -> {str: Prob}:
    result = {}
    for (key, value) in probabilities.items():
        result[key] = Prob(words=list(value.keys()), probs=(value.values()))
    return result


a_z_pattern = re.compile(r'\s*([a-zA-Z]*).*')


def clean_word(word: str) -> str or None:
    match = re.match(a_z_pattern, word)
    if match:
        return match.group(1).lower()
    else:
        return None


def generate(probabilities: {str: Prob}, length: int):
    result = [generate_when_pat(probabilities)]
    for _ in range(int(length / 2)):
        try:
            actual_prob = probabilities[result[-1]]
            result.append(random.choices(actual_prob.words, actual_prob.probs)[0])
        except KeyError:
            result.append(generate_when_pat(probabilities))
    if length % 2 != 0:
        result.append(random.choice([key for key in probabilities.keys() if key[0] == result[-1][0]])[-1])
    return ''.join(result)


def generate_when_pat(probabilities):
    return random.choice(list(probabilities.keys()))


if __name__ == '__main__':
    import sys

    parser = argparse.ArgumentParser(description='Generate random nicknames basing on any text file.')
    parser.add_argument('-i', '--input_file', default='./sample_anything/pan-tadeusz.txt', type=argparse.FileType())
    parser.add_argument('-l', '--length', default=8, type=int)
    parser.add_argument('-n', '--nickname_number', default=10, type=int)
    args = parser.parse_args(sys.argv[1:])
    probabilities = calculate_probabilities(args.input_file)
    probabilities = convert_probabilities(probabilities)
    for i in range(args.nickname_number):
        print(generate(probabilities, args.length).capitalize())
