"""Module containing the logic for utilities."""

import re
from collections import OrderedDict
from textwrap import wrap
import typing

from dictlistlib.argumenthelper import validate_argument_type
from dictlistlib.exceptions import RegexConversionError


def convert_wildcard_to_regex(pattern, closed=False):
    """Convert a wildcard pattern to a regex pattern.

    Parameters
    ----------
    pattern (str): a wildcard pattern.
    closed (bool): will prepend ^ symbol and append $ symbol to pattern
            if set to True
    Returns
    -------
    str: a regular express pattern.

    Notes
    -----
    Wildcard support:
        ? (question mark): this can represent any single character.
        * (asterisk): this can represent any number of characters
            (including zero, in other words, zero or more characters).
        [] (square brackets): specifies a range.
        [!] : match any that not specifies in a range.

    """
    validate_argument_type(str, pattern=pattern)
    regex_pattern = ''
    try:
        regex_pattern = pattern.replace('.', r'\.')
        regex_pattern = regex_pattern.replace('+', r'\+')
        regex_pattern = regex_pattern.replace('?', '_replacetodot_')
        regex_pattern = regex_pattern.replace('*', '_replacetodotasterisk_')
        regex_pattern = regex_pattern.replace('_replacetodot_', '.')
        regex_pattern = regex_pattern.replace('_replacetodotasterisk_', '.*')
        regex_pattern = regex_pattern.replace('[!', '[^')
        regex_pattern = '^{}$'.format(regex_pattern) if closed else regex_pattern
        re.compile(regex_pattern)
        return regex_pattern
    except Exception as ex:
        fmt = 'Failed to convert wildcard({!r}) to regex({!r})\n{}'
        raise RegexConversionError(fmt.format(pattern, regex_pattern, ex))


def foreach(data, choice='keys'):
    """"a set-like object providing a view on D's keys/values/items

    Parameters
    ----------
    data (Any): data
    choice (str): keys|values|items.  Default is keys.

    Returns
    -------
    dict_keys or odict_keys if choice is keys
    dict_values or odict_values if choice is values
    dict_items or odict_items if choice is items
    """
    if isinstance(data, dict):
        node = data
    elif isinstance(data, (list, tuple)):
        total = len(data)
        node = OrderedDict(zip(range(total), data))
    else:
        node = dict()

    if choice == 'keys':
        return node.keys()
    elif choice == 'values':
        return node.values()
    else:
        return node.items()


class BaseText(str):
    def __new__(cls, *args, **kwargs):
        arg0 = args[0] if args else None
        if args and isinstance(arg0, BaseException):
            txt = str.__new__(cls, '{}: {}'.format(type(arg0).__name__, arg0))
            return txt
        else:
            txt = str.__new__(cls, *args, **kwargs)
            return txt


class Text(BaseText):
    @classmethod
    def format(cls, *args, **kwargs):
        if not args:
            text = ''
            return text
        else:
            if kwargs:
                fmt = args[0]
                try:
                    text = str(fmt).format(args[1:], **kwargs)
                    return text
                except Exception as ex:
                    text = cls(ex)
                    return text
            else:
                if len(args) == 1:
                    text = cls(args[0])
                    return text
                else:
                    fmt = args[0]
                    t_args = tuple(args[1:])
                    try:
                        if len(t_args) == 1 and isinstance(t_args[0], dict):
                            text = str(fmt) % t_args[0]
                        else:
                            text = str(fmt) % t_args

                        if text == fmt:
                            text = str(fmt).format(*t_args)
                        return text
                    except Exception as ex1:
                        try:
                            text = str(fmt).format(*t_args)
                            return text
                        except Exception as ex2:
                            text = '%s\n%s' % (cls(ex1), cls(ex2))
                            return text

    @classmethod
    def wrap_html(cls, tag, data, *args):
        data = str(data)
        tag = str(tag).strip()
        attributes = [str(arg).strip() for arg in args if str(arg).strip()]
        if attributes:
            attrs_txt = str.join(' ', attributes)
            if data.strip():
                result = '<{0} {1}>{2}</{0}>'.format(tag, attrs_txt, data)
            else:
                result = '<{0} {1}/>'.format(tag, attrs_txt)
        else:
            if data.strip():
                result = '<{0}>{1}</{0}>'.format(tag, data)
            else:
                result = '<{0}/>'.format(tag)
        return result

    def do_finditer_split(self, pattern):
        result = []
        start = 0
        m = None
        for m in re.finditer(pattern, self):
            pre_match = self[start:m.start()]
            match = m.group()
            result.append(pre_match)
            result.append(match)
            start = m.end()

        if m:
            post_match = self[m.end():]
            result.append(post_match)
        else:
            result.append(str(self))
        return result


class Printer:
    """A printer class.

    Methods
    Printer.get(data, header='', footer='', failure_msg='', width=80, width_limit=20) -> str
    Printer.print(data, header='', footer='', failure_msg='', width=80, width_limit=20, print_func=None) -> None
    """
    @classmethod
    def get(cls, data, header='', footer='',
            width=80, width_limit=20, failure_msg=''):
        """Decorate data by organizing header, data, footer, and failure_msg

        Parameters
        ----------
        data (str, list): a text or a list of text.
        header (str): a header text.  Default is empty.
        footer (str): a footer text.  Default is empty.
        width (int): width of displayed text.  Default is 80.
        width_limit (int): minimum width of displayed text.  Default is 20.
        failure_msg (str): a failure message.  Default is empty.
        """
        lst = []
        result = []

        sequence_type = (typing.List, typing.Tuple, typing.Set)

        if width > 0:
            right_bound = width - 4
        else:
            right_bound = 76

        headers = []
        if header:
            if isinstance(header, sequence_type):
                for item in header:
                    for line in str(item).splitlines():
                        headers.extend(wrap(line, width=right_bound))
            else:
                headers.extend(wrap(str(header), width=right_bound))

        footers = []
        if footer:
            if isinstance(footer, sequence_type):
                for item in footer:
                    for line in str(item).splitlines():
                        footers.extend(wrap(line, width=right_bound))
            else:
                footers.extend(wrap(str(footer), width=right_bound))

        if data:
            data = data if isinstance(data, sequence_type) else [data]
        else:
            data = []

        for item in data:
            if width > 0:
                if width >= width_limit:
                    for line in str(item).splitlines():
                        lst.extend(wrap(line, width=right_bound + 4))
                else:
                    lst.extend(line.rstrip() for line in str(item).splitlines())
            else:
                lst.append(str(item))
        length = max(len(str(i)) for i in lst + headers + footers)

        if width >= width_limit:
            length = right_bound if right_bound > length else length

        result.append(Text.format('+-{}-+', '-' * length))
        if header:
            for item in headers:
                result.append(Text.format('| {} |', item.ljust(length)))
            result.append(Text.format('+-{}-+', '-' * length))

        for item in lst:
            result.append(item)
        result.append(Text.format('+-{}-+', '-' * length))

        if footer:
            for item in footers:
                result.append(Text.format('| {} |', item.ljust(length)))
            result.append(Text.format('+-{}-+', '-' * length))

        if failure_msg:
            result.append(failure_msg)

        txt = str.join(r'\n', result)
        return txt

    @classmethod
    def print(cls, data, header='', footer='',
              width=80, width_limit=20, failure_msg='', print_func=None):
        """Decorate data by organizing header, data, footer, and failure_msg

        Parameters
        ----------
        data (str, list): a text or a list of text.
        header (str): a header text.  Default is empty.
        footer (str): a footer text.  Default is empty.
        width (int): width of displayed text.  Default is 80.
        width_limit (int): minimum width of displayed text.  Default is 20.
        failure_msg (str): a failure message.  Default is empty.
        print_func (function): a print function.  Default is None.
        """

        txt = Printer.get(data, header=header, footer=footer,
                          failure_msg=failure_msg, width=width,
                          width_limit=width_limit)

        print_func = print_func if callable(print_func) else print
        print_func(txt)

    @classmethod
    def get_message(cls, fmt, *args, style='format', prefix=''):
        """Get a message

        Parameters
        ----------
        fmt (str): string format.
        args (tuple): list of parameters for string interpolation.
        style (str): either format or %.
        prefix (str): a prefix.

        Returns
        -------
        str: a message.
        """

        if args:
            message = fmt.format(*args) if style == 'format' else fmt % args
        else:
            message = fmt

        message = '{} {}'.format(prefix, message) if prefix else message
        return message

    @classmethod
    def print_message(cls, fmt, *args, style='format', prefix='', print_func=None):
        """Print a message

        Parameters
        ----------
        fmt (str): string format.
        args (tuple): list of parameters for string interpolation.
        style (str): either format or %.
        prefix (str): a prefix.
        print_func (function): a print function.
        """
        message = cls.get_message(fmt, *args, style=style, prefix=prefix)
        print_func = print_func if callable(print_func) else print
        print_func(message)
