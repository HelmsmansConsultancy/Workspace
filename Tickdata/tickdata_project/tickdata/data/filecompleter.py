import os
from prompt_toolkit.completion import Completer, Completion


class FileCompleter(Completer):
    """Tab-completes filenames and directories."""

    def get_completions(self, document, complete_event):
        text = document.text_before_cursor
        dirname = os.path.dirname(text)
        prefix = os.path.basename(text)
        search_dir = dirname if dirname else '.'

        try:
            entries = sorted(os.listdir(search_dir))
        except OSError:
            return

        for entry in entries:
            if entry.startswith(prefix):
                full = os.path.join(dirname, entry) if dirname else entry
                suffix = os.sep if os.path.isdir(full) else ''
                yield Completion(
                    entry + suffix,
                    start_position=-len(prefix),
                    display_meta='dir' if os.path.isdir(full) else 'file'
                )