'''App for splitting the cost on a receipt.
Pass in a CSV file where each row has the format:
    <item name>,<item cost>,<people list>
where <people list> is a space-separated list of people to split the cost of this item with'''
from argparse import ArgumentParser
from decimal import Decimal
from pathlib import Path
import sys


def main():
    parser = ArgumentParser(
        description=__doc__
    )
    parser.add_argument(
        'file',
        help='The filename of the receipt CSV file'
    )
    args = parser.parse_args()
    file = Path(args.file)
    if not file.is_file():
        print(args.file, 'is not a file', file=sys.stderr)
        return
    csv = file.read_text(encoding='utf-8').split('\n')
    people = {}
    for line in csv:
        item = line.split(',')
        payees = item[2].split(' ')
        if not payees:
            print('No payees for item', line)
            continue
        amount = Decimal(item[1]) / len(payees)
        for person in payees:
            people[person] = people.get(person, 0) + amount
    for person, amount in people.items():
        print(f'{person}:\t£{amount:.3f}')


if __name__ == '__main__':
    main()
