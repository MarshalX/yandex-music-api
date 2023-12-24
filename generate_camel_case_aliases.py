#!/usr/bin/env python3
"""Generate camel case aliases for snake case functions."""
import ast
import os

SOURCE_FOLDER = 'yandex_music'
EXCLUDED_FUNCTIONS = {'de_dict', 'de_json', 'de_list', 'de_json_async', 'de_list_async'}

ALIAS_TEMPLATE = """
#: Псевдоним для :attr:`{name}`
{camel_case_name} = {name}
"""

ALIAS_SECTION_MARKER = '    # camelCase псевдонимы'


def _validate_function_name(function_name: str) -> bool:
    if function_name.startswith('_'):
        return False

    if function_name in EXCLUDED_FUNCTIONS:
        return False

    # camel case will be the same
    if '_' not in function_name:
        return False

    return True


def convert_snake_case_to_camel_case(string: str) -> str:
    """Convert snake case string to camel case string."""
    camel_case = ''.join(word.title() for word in string.split('_'))
    return camel_case[0].lower() + camel_case[1:]


def _generate_code(function_name: str, intent: int = 0) -> str:
    camel_case_name = convert_snake_case_to_camel_case(function_name)
    code = ALIAS_TEMPLATE.format(name=function_name, camel_case_name=camel_case_name)

    code_lines = [line for line in code.split('\n') if line]
    code_lines = [f'{" " * intent}{line}' for line in code_lines]

    return '\n'.join(code_lines)


def _process_file(file: str) -> None:
    with open(file, 'r', encoding='UTF-8') as f:
        count_of_class_def = 0
        file_aliases_code_fragments = []
        tree = ast.parse(f.read())
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                count_of_class_def += 1

            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and _validate_function_name(node.name):
                alias_code = _generate_code(node.name, node.col_offset)
                file_aliases_code_fragments.append(alias_code)

        # there are no such cases in data models yet
        # only in yandex_music/exceptions.py and yandex_music/utils/difference.py
        if count_of_class_def != 1:
            return

        f.seek(0)
        file_code_lines = f.read().splitlines()

        marker_lineno = None
        for lineno, code_line in enumerate(file_code_lines):
            if code_line == ALIAS_SECTION_MARKER:
                marker_lineno = lineno
                break

        # we can't process files without markers now
        if marker_lineno is None:
            return

        # remove prev aliases
        file_code_lines = file_code_lines[: marker_lineno + 1]
        file_code_lines.append('')
        file_code_lines.extend(file_aliases_code_fragments)
        file_code_lines.append('')

        new_file_code = '\n'.join(file_code_lines)

    with open(file, 'w', encoding='UTF-8') as f:
        f.write(new_file_code)


def main() -> None:
    """Generate camel case aliases for snake case functions."""
    for root, _, files in os.walk(SOURCE_FOLDER):
        for file in files:
            if file.endswith('.py') and file != '__init__.py':
                filepath = os.path.join(root, file)
                _process_file(filepath)


if __name__ == '__main__':
    main()
