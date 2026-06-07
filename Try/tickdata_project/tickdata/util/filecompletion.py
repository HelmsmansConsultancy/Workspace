import os
from prompt_toolkit import prompt
from tickdata.data.filecompleter import FileCompleter
from tickdata.data.filecompleter import FileCompleter


def prompt_filename(message='Enter filename'):
    """Prompt for a filename with tab-autocomplete."""
    return prompt(
        f'{message}: ',
        completer=FileCompleter(),
        complete_while_typing=True,  # show completions as you type
    )



def complete_filename(text, state):
    """Tab-completes filenames using os module."""
    dirname = os.path.dirname(text)
    prefix = os.path.basename(text)
    search_dir = dirname if dirname else '.'

    try:
        entries = os.listdir(search_dir)
    except OSError:
        return None

    matches = []
    for entry in entries:
        if entry.startswith(prefix):
            full = os.path.join(dirname, entry) if dirname else entry
            # append slash to directories so you can keep tabbing into them
            if os.path.isdir(full):
                full += os.sep
            matches.append(full)

    return matches[state] if state < len(matches) else None