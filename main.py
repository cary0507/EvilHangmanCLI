# Author: Cary
# Inspired by Mr Benum


class WordFamily:
    def __init__(self, pattern: list[int], words: list[str] = None):
        if words is None:
            words = []
        self.pattern = pattern
        self.words = words

    def add_word(self, word: str):
        if word not in self.words:
            self.words.append(word)

    def get_size(self) -> int:
        return len(self.words)


class FamilyGroup:
    def __init__(self):
        self.families = []

    def find_family(self, pattern: list[int]) -> int:
        for i in range(len(self.families)):
            family = self.families[i]
            if family.pattern == pattern:
                return i
        return -1

    def add_word(self, pattern: list[int], word: str):
        # Add word to family that contains the specified pattern, or automatically create a new family
        match_i = self.find_family(pattern)
        if match_i >= 0:
            self.families[match_i].add_word(word)
        else:  # Family not found, create a new one
            new_family = WordFamily(pattern, [word])
            self.families.append(new_family)

    def get_largest(self) -> WordFamily:
        """
        :return: The first largest WordFamily object
        """
        max_size = 0
        max_index = 0
        for i in range(len(self.families)):
            family = self.families[i]
            size = family.get_size()
            if size > max_size:
                max_size = size
                max_index = i
        return self.families[max_index]


def get_pattern(word: str, letter: str) -> list[int]:
    """
    :return: the locations of a letter appearing in a word, which is the pattern of a word
    """
    indexes = []
    for i in range(len(word)):
        if letter == word[i]:
            indexes.append(i)
    return indexes


def get_family(cur_dict: list, guess: str) -> FamilyGroup:
    """
    :return: all families of words containing the guess letter
    A family stores words that have the same pattern for guess letter (Same locations of occurrence)
    """
    all_families = FamilyGroup()
    for word in cur_dict:
        if guess in word:  # Contains letter
            pattern = get_pattern(word, guess)
            all_families.add_word(pattern, word)  # This automatically create new WordFamily of not found
    return all_families


def has_won(correct: list[str]) -> bool:
    return '_' not in correct  # Literally English √


def display_possible(cur_dict: list[str]) -> None:
    for word in cur_dict:
        print(word)


def display_correct(correct_letters: list[str]) -> None:
    for letter in correct_letters:
        print(letter, end='')
    print()


def display_guessed(guessed: list[str]) -> None:
    print("You have guessed: ", end='')
    for letter in guessed:
        print(letter, end=' ')
    print()


def narrow_guess(cur_dict: list[str], guess: str) -> list[int]:
    """
    A function with a side effect. While checking if the current guess is correct, the function will also
    manipulate the current dictionary through its reference passed to the parameters.

    :param cur_dict: Current dictionary
    :param guess: Current guess
    :return: The list with the indexes of the correct guess letter. Empty if wrong guess
    """
    # Priorities making the player's guess wrong
    count_contains = 0
    word_letter_index = []  # Index of words that contains the current guess
    dict_len = len(cur_dict)
    # Check for words that contain the current letter and record the results
    for i in range(dict_len):
        word = cur_dict[i]
        if guess in word:
            # print("{0} is in word \"{1}\"".format(guess, word))
            word_letter_index.append(i)
            count_contains += 1  # Used later to check if all words contain this letter
    # If no matched word from the current dictionary, automatically a wrong guess
    if count_contains < 1:
        return []

    # Check if all words remaining have the guessed letter
    if count_contains < dict_len:  # Not all words have the guessed letter
        for rm in range(len(word_letter_index) - 1, -1, -1):  # Delete from rightmost index to avoid out of range
            remove_index = word_letter_index[rm]
            cur_dict.pop(remove_index)
        return []  # Wrong guess
    # If all remaining words contain the guessed letter, the current guess have to be correct. Remove the letter.
    else:
        families = get_family(cur_dict, guess)
        largest_family = families.get_largest()
        # Narrow down
        cur_dict.clear()
        cur_dict.extend(largest_family.words)
        return largest_family.pattern


def next_guess(cur_dict: list[str], prompt: str) -> str:
    while True:
        cur_guess = input(prompt).lower()
        try:
            if cur_guess == '1':  # Debugging
                display_possible(cur_dict)
            elif ord(cur_guess) < ord('a') or ord(cur_guess) > ord('z'):
                print("Input value has to be a letter!")
                cur_guess = input(prompt).lower()
            else:
                break
        except TypeError:
            print("Invalid input! Cannot be blank! Do no enter spaces, only input one letter!")
            continue
    return cur_guess


def main():
    FILE_PATH = "dictionary.txt"

    guessed_letters: list = []
    in_game = True

    # Read words from dictionary file
    with open(FILE_PATH, 'r') as dict_file:
        full_dict = dict_file.read().lower().split()
    # Gets minimum and maximum length
    min_length = len(min(full_dict))
    max_length = len(max(full_dict))

    prompt_word_len = "Enter the word length between {0} and {1} inclusive, 0 to quit: ".format(min_length, max_length)
    prompt_guess = "Guess a letter from \"a\" to \"z\" (Case insensitive): "

    while in_game:
        # Prompt for word length
        try:
            word_length = int(input(prompt_word_len))
            if word_length == 0:  # Quit game
                return
            while word_length > max_length or word_length < min_length:
                print("Length out of range!")
                word_length = int(input(prompt_word_len))
        except ValueError:
            print("Length has to be a number!")
            continue  # Skip the loop
        print("Selected word length:", word_length)
        correct_letters = ['_' for _ in range(word_length)]  # '_' represents placeholder for not guessed letter
        possible_words = [word for word in full_dict if len(word) == word_length]  # Keep words with the same length

        while not has_won(correct_letters):
            display_guessed(guessed_letters)
            display_correct(correct_letters)
            next_letter = next_guess(possible_words, prompt_guess)
            correct_index = narrow_guess(possible_words, next_letter)
            if len(correct_index) > 0:  # Correct guess
                for i in correct_index:
                    correct_letters[i] = next_letter
            guessed_letters.append(next_letter)

        print("You wont! Congratulations! The word is:")
        display_correct(correct_letters)


if __name__ == '__main__':
    main()
