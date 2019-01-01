from datetime import datetime
import webbrowser, os

""" HTMLWriter
Provides methods to save the AST.ProgramNode tree in HTML.
"""
class HTMLWriter:
    def __init__(self):
        self.file_structure = "resources/file_structure.html"
        self.output_file = "output/"

    def writeResult(self, title, result):
        """
        Writes the AST.ProgramNode's tree in HTML with the given title.
        """
        output_file = self.output_file + title + ".html"
        with open(self.file_structure, "r") as structure:
            with open(output_file, "w+") as output:
                for line in structure.readlines():
                    if "<title></title>" in line:
                        line = "\t<title>" + title + "</title>\n"
                    output.write(line)
                    if "<body>" in line:
                        output.write(self._treeToText(result))
        webbrowser.open("file://" + os.path.realpath(output_file))

    def _treeToText(self, result):
        """
        Converts and returns an AST.ProgramNode's tree in a string.
        """
        return " ".join([repr(c)[1:-1] for c in result.children])