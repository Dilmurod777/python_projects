import os
import sys
import argparse

cards = {}
separator = ';'
memory = []

parser = argparse.ArgumentParser()
parser.add_argument('--import_from')
parser.add_argument('--export_to')


class LoggerOut:
    def __init__(self):
        self.terminal = sys.stdout

    def write(self, message):
        self.terminal.write(message)
        memory.append(message)

    def flush(self):
        pass


class LoggerIn:
    def __init__(self):
        self.terminal = sys.stdin

    def readline(self):
        entry = self.terminal.readline()
        memory.append(entry)
        return entry


sys.stdin = LoggerIn()
sys.stdout = LoggerOut()


def add_card():
    print("The card:")
    while True:
        term = input().strip()
        if term not in cards.keys():
            break
        else:
            print(f'The term "{term}" already exists. Try again:')
    print("The definition of the card:")
    while True:
        definition = input().strip()
        if definition not in [cards[key]['definition'] for key in cards]:
            break
        else:
            print(f'The term "{definition}" already exists. Try again:')

    cards[term] = {
        'definition': definition,
        'mistakes': 0
    }
    print(f'The pair ("{term}":"{definition}") has been added.')


def remove_card():
    print("Which card?")
    term = input().strip()

    if term in cards:
        del cards[term]
        print('The card has been removed.')
    else:
        print(f'Can\'t remove "{term}": there is no such card.')


def import_cards(filename=None):
    if filename is None:
        print('File name:')
        filename = input().strip()

    if os.access(filename, os.F_OK):
        with open(filename, 'r') as file:
            lines = file.readlines()
            for line in lines:
                parts = line.strip().split(separator)
                cards[parts[0]] = {
                    'definition': parts[1],
                    'mistakes': int(parts[2])
                }
            print(f'{len(lines)} cards have been loaded.')
    else:
        print('File not found.')


def export_cards(filename=None):
    if filename is None:
        print('File name:')
        filename = input().strip()

    with open(filename, 'w') as file:
        file.writelines([f'{key}{separator}{cards[key]["definition"]}{separator}{cards[key]["mistakes"]}\n' for key in cards])

    print(f'{len(cards.keys())} cards have been saved.')


def ask_random_card():
    print('How many times to ask?')
    n = int(input().strip())
    terms = list(cards.keys())

    for i in range(n):
        index = i % len(terms)
        print(f'Print the definition of "{terms[index]}":')
        answer = input().strip()
        isAnotherTerm = False
        isCorrectAnswer = False

        for t in cards:
            if cards[t]["definition"] == answer:
                if t != terms[index]:
                    isAnotherTerm = True
                    print(f'Wrong. The right answer is "{cards[terms[index]]["definition"]}", but your definition is correct for "{t}"')
                    cards[terms[index]]['mistakes'] += 1
                else:
                    isCorrectAnswer = True
                    print('Correct!')
                break

        if not isAnotherTerm and not isCorrectAnswer:
            print(f'Wrong. The right answer is "{cards[terms[index]]["definition"]}".')
            cards[terms[index]]['mistakes'] += 1
    pass


def exit_game():
    print('Bye bye!')

    if args.export_to is not None:
        export_cards(args.export_to)

    return True


def log_game():
    print("File name:")
    filename = input().strip()

    with open(filename, 'w') as file:
        print(*memory, file=file, flush=True, end='', sep='')

    print("Log has been saved.")


def hardest_card():
    mistakes = [cards[key]['mistakes'] for key in cards if cards[key]['mistakes'] > 0]
    if len(mistakes) == 0:
        print('There are no cards with errors.')
        return

    max_mistakes = max(mistakes)
    hardest_terms = [key for key in cards if cards[key]['mistakes'] == max_mistakes]

    terms = ', '.join([f'"{key}"' for key in hardest_terms])
    print(f'The hardest card is "{terms}". You have {max_mistakes} errors answering it.')


def reset_stats():
    for key in cards:
        cards[key]['mistakes'] = 0
    print('Card statistics have been reset.')


args = parser.parse_args()
if args.import_from is not None:
    import_cards(args.import_from)

while True:
    print('Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):')
    action = input().strip()

    actions = {
        'add': add_card,
        'remove': remove_card,
        'import': import_cards,
        'export': export_cards,
        'ask': ask_random_card,
        'exit': exit_game,
        'log': log_game,
        'hardest card': hardest_card,
        'reset stats': reset_stats
    }

    if action in actions and actions[action]():
        break
