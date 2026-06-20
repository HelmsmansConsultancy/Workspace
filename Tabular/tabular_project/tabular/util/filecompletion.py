import os
import readline
import glob

def _path_completer(text, state):
    matches = glob.glob(text + '*')
    # Add trailing slash for directories
    matches = [m + '/' if os.path.isdir(m) else m for m in matches]
    return matches[state] if state < len(matches) else None

def prompt_filename(message='Enter filename '):
    """Prompt for a filename with tab-autocomplete."""
    readline.set_completer(_path_completer)
    readline.set_completer_delims(' \t\n;')
    readline.parse_and_bind('tab: complete')
    try:
        return input(message)
    finally:
        readline.set_completer(None)  # restore after

def _path_completer(text, state):
    matches = glob.glob(text + '*')
    # Add trailing slash for directories
    matches = [m + '/' if os.path.isdir(m) else m for m in matches]
    return matches[state] if state < len(matches) else None

def prompt_with_completion(prompt_text):
    readline.set_completer(_path_completer)
    readline.set_completer_delims(' \t\n;')
    readline.parse_and_bind('tab: complete')
    try:
        return input(prompt_text)
    finally:
        readline.set_completer(None)  # restore after

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