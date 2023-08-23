# -*- coding: utf-8 -*-

"""Console CLI script for pylexique."""
import sys
import click
import json
import logging
from pylexique import Lexique383, LexItem
from collections import defaultdict
from typing import Sequence


@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
@click.argument('words', nargs=-1)
@click.option('-a', '--all_forms',
              is_flag=True,
              help="Gets all lexical forms of a given word. Only takes 1 word as an argument.")
@click.option('-o', '--output',
              default=None,
              help="Path of the json filename for storing the lexical entries.",
              type=click.STRING)
def main(words: Sequence[str], all_forms: bool, output: str) -> None:
    """Pylexique is a Python wrapper around Lexique83.
    It allows to extract lexical information from more than 140 000 French words in an Object Oriented way.


    * Free software: MIT license
    * Documentation: https://pylexique.readthedocs.io.
    """
    logger = logging.getLogger(__name__)

    # create console handler and set level to debug
    console_handler = logging.StreamHandler(sys.stdout)
    error_handler = logging.StreamHandler(sys.stderr)
    console_handler.setLevel(logging.INFO)
    error_handler.setLevel(logging.ERROR)
    logger.addHandler(console_handler)
    logger.addHandler(error_handler)
    logger.setLevel(logging.INFO)

    LEXIQUE = Lexique383()
    results = defaultdict(list)
    dict = defaultdict(list)
    for word in words:
        if all_forms:
            print('Retrieving all the lexical forms of the supplied words.')
            results[word].append(LEXIQUE.get_all_forms(word))
        else:
            results[word].append(LEXIQUE.lexique[word])

        for element in results[word]:
            if isinstance(element, LexItem):
                dict[word].append(element.to_dict())
                continue
            for item in element:
                dict[word].append(item.to_dict())
    if output:
        with open(output, 'w', encoding='utf-8') as file:
            json.dump(dict, file, indent=4, ensure_ascii=False)
            print('The Lexical Items have been successfully saved to {0} by pylexique.'.format(output))
    else:
        print(json.dumps(dict, indent=4, ensure_ascii=False))
    return


if __name__ == "__main__":
    main()  # pragma: no cover
