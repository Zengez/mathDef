import io
import tarfile
import unittest

from scripts.arxiv_candidate_scan import scan_tex, source_files


class ScannerTests(unittest.TestCase):
    def test_custom_definition_environment(self):
        source = r"""
\newtheorem{dfn}{Definition}[section]
One paragraph.
\begin{dfn}[Local test]
Let $X$ be a space with $d(x,y)=0$.
\end{dfn}
\begin{theorem}Not a definition.\end{theorem}
"""
        matches = scan_tex(source, "main.tex", "2406.02401", "Paper")
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0]["heading"], "Local test")
        self.assertEqual(matches[0]["line"], 4)
        self.assertNotIn("Let $X$", str(matches[0]))

    def test_synthetic_tar_no_disk_extraction(self):
        text = br"\begin{definition}An example.\end{definition}"
        buf = io.BytesIO()
        with tarfile.open(fileobj=buf, mode="w:gz") as tf:
            entry = tarfile.TarInfo(name="../not-written.tex")
            entry.size = len(text)
            tf.addfile(entry, io.BytesIO(text))
        records = list(source_files(buf.getvalue()))
        self.assertEqual(len(records), 1)
        self.assertEqual(len(scan_tex(records[0][1], records[0][0], "2511.16503")), 1)


if __name__ == "__main__":
    unittest.main()
