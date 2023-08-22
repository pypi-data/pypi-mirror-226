import os.path
import shutil

import yaml

from helm_mkdocs.generator.mkdocs import MKDocsGenerator
from helm_mkdocs.model import Chart
from helm_mkdocs.model import PageInput
from helm_mkdocs.reader import read_yaml


def generate_pages(yaml_file) -> [PageInput]:
    page_input = PageInput("root", yaml_file)
    page_input.root_item.comments = ["Values that are defined in the root of the values file."]
    pages = [page_input]
    root_values = {}
    for key in yaml_file.value:
        value = yaml_file.value[key]
        if isinstance(value.value, dict):
            pages.append(PageInput(value.name, value))
        else:
            root_values[key] = value
    page_input.root_item.value = root_values
    return pages


class ChartProcessor:
    def __init__(self, settings):
        self.settings = settings

    def run(self):
        file = self.settings["values"]
        chart = self.load_chart()
        generator = MKDocsGenerator(self.settings)

        yaml_file = read_yaml(file)

        pages = generate_pages(yaml_file)

        for page in pages:
            new_page = generator.generate_page(page)
            self.write_page(new_page, page.name, ['config'])
        examples = self.process_examples()
        page = generator.generate_chart_page(chart, pages, examples)
        self.write_page(page, "index")

    def load_chart(self):
        chart_path = self.settings["chart"]
        with open(chart_path) as file:
            load = yaml.safe_load(file)
            return Chart(load)

    def write_page(self, page, name, dirs=None):
        if dirs is None:
            dirs = []
        dir_path = self.settings["output"]
        for dir in dirs:
            dir_path = os.path.join(dir_path, dir)
        os.makedirs(dir_path, exist_ok=True)

        md_ = os.path.join(dir_path, "%s.md" % name)
        print("Writing page", name, "to", md_)
        with open(md_, "w") as f:
            f.write(page)

    def process_examples(self):
        examples = {}
        examples_dir = self.settings["example_dir"]
        if not os.path.exists(examples_dir) or not os.path.isdir(examples_dir):
            return
        for filename in os.listdir(examples_dir):
            if os.path.isdir(os.path.join(examples_dir, filename)):
                examples[filename] = self.process_example(examples_dir, filename)
        return examples

    def process_example(self, examples_dir, filename):
        output_ = self.settings['output']
        # os.makedirs(os.path.join(output_, filename))

        shutil.copytree(os.path.join(examples_dir, filename), os.path.join(output_, "examples", filename),
                        dirs_exist_ok=True)

        return "./%s/%s" % ("examples", filename)
