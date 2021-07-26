import re
from pathlib import Path

from onenote import get_page_content
from convert import convert_page


class Pipeline:
    def __init__(
        self, onenote_session, notebook: str, base_dir: Path
    ):
        self.s = onenote_session
        self.notebook = notebook
        self.base_dir = base_dir
        self.filename_re = re.compile(r'[<>:\"/\\\|\?\*#]')
        self.whitespace_re = re.compile(r'\s+')

    def proc_page(self, page: dict):
        content = get_page_content(self.s, page)

        out_dir = self.base_dir / page['section_path']
        for pp in page['parent_pages']:
            out_dir = out_dir / self._filenamify(pp)
        out_dir.mkdir(parents=True, exist_ok=True)

        attach_dir = out_dir / (self._filenamify(page['title']) + '.assets')
        # does not mkdir here, only when attachment found.

        _, content = convert_page(page, content, self.notebook, self.s, attach_dir)

        return self._save_page(page, content, out_dir)

    def _save_page(self, page, content, out_dir):
        path = out_dir / (self._filenamify(page['title']) + '.md')
        path.write_text(content, encoding='utf-8')

    def _filenamify(self, s):
        s = self.filename_re.sub(' ', s)
        s = self.whitespace_re.sub(' ', s)
        return s.strip()
