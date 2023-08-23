import os
import subprocess
import jinja2


class TeXUtils:
    def __init__(self, tex_src, job_name: str, dir_name: str = ''):
        self.tex = tex_src
        self.params = dict()
        self.params['-jobname'] = job_name
        self.params['-output-directory'] = dir_name

    @classmethod
    def from_tex_file(cls, filename):
        dir_name = os.path.dirname(filename)
        prefix = os.path.basename(filename)
        prefix = os.path.splitext(prefix)[0]
        with open(filename, 'rb') as f:
            return cls.from_binary_string(f.read(), prefix, dir_name)

    @classmethod
    def from_binary_string(cls, binstr, jobname: str, dir_name: str = None):
        return cls(binstr, jobname, dir_name)

    @classmethod
    def from_jinja_template_file(cls, filename, **data: any):
        dir_name = os.path.dirname(filename)
        prefix = os.path.basename(filename)
        prefix = os.path.splitext(prefix)[0] if not prefix.endswith('.j2') else \
        os.path.splitext(os.path.splitext(prefix)[0])[0]

        env = jinja2.Environment(loader=jinja2.FileSystemLoader(dir_name), autoescape=jinja2.select_autoescape())

        template = env.get_template(os.path.basename(filename))
        return cls.from_jinja_template(template, prefix, dir_name, **data)

    @classmethod
    def from_jinja_template(cls, template: jinja2.Template, jobname: str, dir_name: str = None, **data):
        tex_src = template.render(**data)
        return cls(tex_src.encode("utf-8"), jobname, dir_name)

    def create_pdf(self):
        args = self.get_args()
        subprocess.run(['pdflatex', *args], input=self.tex)

    def get_args(self):
        return [k + ('=' + v if v is not None else '') for k, v in self.params.items()]
