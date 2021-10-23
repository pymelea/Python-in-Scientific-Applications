# Author: Mateusz Kowalczyk
# Wywołanie skryptu: python lab01.py [1] [2] [3]
# [1] - filename.txt
# [2] - how_many_words
# [3] - word_min_len
# Przykładowo: python lab01.py pan-tadeusz-pl.txt 10 4
# Polecenie powyżej wywoła skrypt z histogramem 10 najczęstszych słów i takich
# które mają minimum 4 litery

# Importujemy co tam nam potrzebne
import sys
import os.path
import codecs
from matplotlib import pyplot as plt
from matplotlib.pyplot import figure
from collections import Counter


# Główna funkcja
def words_in_book(file_name: str, how_many_words: int, word_min_len: int, ignore_words: list):

    print("You get a histogram of the " + str(how_many_words) +
          " most frequent words, where a word has at least " + str(word_min_len) + " letters.")

    # Czytamy dane
    with codecs.open(file_name, 'r', 'utf-8') as file:
        word_list = [word.lower() for line in file for word in line.split()
                     if (len(word) >= word_min_len and word.isalpha())]

    # Tworzymy countera do zliczania słów
    word_counter = Counter(word_list)

    # Wyrzucamy słowa, które daliśmy jako ignorowane
    if len(ignore_words) > 0:
        for word in ignore_words:
            if word in word_counter:
                print("You ignore word: \"" + word + "\". " +
                      "This word has got " + str(word_counter[word]) + " counts.")
                del word_counter[word]

    # Tworzymy listy na słowa i ich zliczenia
    if len(word_counter.most_common(how_many_words)) > 0:
        word, popularity = zip(*word_counter.most_common(how_many_words))
        word, popularity = list(word), list(popularity)
    else:
        print("Looks like there are not such long words.")
        sys.exit(0)

    # Odwracamy listy, bo chcemy najbardziej popularne wyrazy na górze histogramu
    popularity.reverse()
    word.reverse()

    # Użyjmy jakiegoś fajnego stylu
    plt.style.use("seaborn")
    figure(figsize=(8, 4.5), dpi=100)

    # Wykres słupkowy, zróbmy wykres w poziomie, wtedy słowa nie będą się nakrywać
    plt.barh(word, popularity, height=0.7)

    # Naniesiemy dokładne wartości na słupki
    for index, value in enumerate(popularity):
        plt.text(value - 3, index - 0.05, str(value),
                 color='white', va="center", ha="right", fontweight='bold', fontname="Times New Roman", fontsize=12)

    # Damy jakiś tytuł
    plt.title("\"Pan Tadeusz\" - Most Common Words",
              fontname="Times New Roman", fontsize=14)

    # Podpis osi
    plt.xlabel("Number of counts", fontname="Times New Roman", fontsize=12)

    # I pokażemy co uzyskaliśmy
    plt.show()


# Main
if __name__ == '__main__':

    # Ignorowane słowa
    ignore_words = ['lecz', 'jest']
    # Nazwa pliku
    file_name = str(sys.argv[1])

    # Wyjątek na istnienie pliku
    if not os.path.isfile(file_name):
        print("File not found. Try one more time.")
        sys.exit(0)

    # Jakieś podstawowe wyjątki
    try:
        how_many_words = int(sys.argv[2])
        word_min_len = int(sys.argv[3])
    except ValueError:
        print("Error value. Try one more time.")
        sys.exit(0)

    # Wywołanie głównej funkcji
    if how_many_words > 0 and word_min_len >= 0:
        words_in_book(file_name, how_many_words, word_min_len, ignore_words)
    else:
        print("Why do you want to use such strange values? Try one more time.")
        sys.exit(0)
