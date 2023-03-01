from flask import Flask, request, jsonify
import unidecode
import nltk
from nltk.stem import WordNetLemmatizer
from collections import Counter

app = Flask(__name__)

# nltk.download("wordnet")

lemmatizer = WordNetLemmatizer()


def convert_to_singular(word):
    return lemmatizer.lemmatize(word, pos="n")


def top10WordPairsWithCount(array, limit=20):
    stop_words = ["de", "la", "que", "el", "en", "y", "a", "los", "del", "se"]
    stop_words = [unidecode.unidecode(word).lower() for word in stop_words]

    word_map = {}
    for word in array:
        words = [
            convert_to_singular(unidecode.unidecode(word).lower())
            for word in word.split(" ")
        ]
        for i in range(len(words) - 1):
            for j in range(i + 1, len(words)):
                if (
                    words[i] not in stop_words
                    and words[j] not in stop_words
                    and len(words[j]) > 2
                ):
                    word_pair = f"{words[i]} {words[j]}"
                    word_map[word_pair] = word_map.get(word_pair, 0) + 1

    word_pairs_with_count = sorted(word_map.items(), key=lambda x: x[1], reverse=True)[
        :limit
    ]
    word_pairs_with_count = [
        {"words": pair[0], "count": pair[1]} for pair in word_pairs_with_count
    ]

    return word_pairs_with_count


def get_top_words(strings, top_n=10):
    """Function to get the top words with count from an array of strings"""
    # Join all strings into one
    all_text = " ".join(strings)

    # Convert all words to lowercase and split into a list
    words = all_text.lower().split()

    # Convert words to their singular form
    singular_words = [convert_to_singular(word) for word in words]

    # Filter words that are less than 7 characters long
    filtered_words = [word for word in singular_words if len(word) >= 7]

    # Create a Counter object to count the words
    word_counts = Counter(filtered_words)

    # Get the top n words and their counts
    top_words = dict(word_counts.most_common(top_n))

    return top_words


@app.route("/clustering", methods=["POST"])
def clustering_route():
    data = request.get_json()
    phrases = data["phrases"]
    limit = data["limit"]
    result = top10WordPairsWithCount(phrases, limit)
    top_words = get_top_words(phrases)
    print(top_words)
    return jsonify({'top_10_words':top_words,'top_grouped_words':result})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
