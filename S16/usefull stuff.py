#To easily obtain the path and the arguments, you may use:
from urllib.parse import parse_qs, urlparse
url_path = urlparse(self.path)
path = url_path.path # we get it from here
arguments = parse_qs(url_path.query)

#To automatically render the form:
import jinja2 as j


def read_html_file(filename):
    contents = Path("html/" + filename).read_text()
    contents = j.Template(contents)
    return contents


contents = read_html_file("echo.html").render(context={"todisplay": text})  # provide a dictionary to build the form


#But to make this last sentence work, the form must have the line below wherever you want the text to be shown (provided variable text contains the characters you want to display).
#<p>{{context.todisplay}}</p>

