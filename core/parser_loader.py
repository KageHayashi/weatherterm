import os
import re
import inspect


def _get_parser_list(dirname):
    '''
    Given a directory, get the file names without the .py extension
    '''
    files = [f.replace('.py', '')
             for f in os.listdir(dirname)
             if not f.startswith('__')]
    return files


def _import_parsers(parserfiles):
    '''
    Looks inside the weatherterm.parsers module to import parsers
    '''
    m = re.compile('.+parser$', re.I)
    _modules = __import__('weatherterm.parsers',
                          globals(),
                          locals(),
                          parserfiles,
                          0)

    _parsers = [(k, v) for k, v in inspect.getmembers(_modules)
                if inspect.ismodule(v) and m.match(k)]
    _classes = dict()

    for k, v in _parsers:
        _classes.update({k: v for k, v in inspect.getmembers(v)
                         if inspect.isclass(v) and m.match(k)})
        return _classes


def load(dirname):
    '''
    Load parsers in a directory
    '''
    parserfiles = _get_parser_list(dirname)
    return _import_parsers(parserfiles)
