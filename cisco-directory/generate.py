from jinja2 import Template
from json import loads
import os

prefix = os.environ["PREFIX"]

with open("directory.xml.j2", "r") as f:
    di_tm = Template(f.read(), trim_blocks=True)

with open("phonebook.xml.j2", "r") as f:
    pb_tm = Template(f.read(), trim_blocks=True)

phonebooks = {}

for phonebook in [ x for x in os.listdir("phonebooks") if "json" in x]:
    with open("phonebooks/{}".format(phonebook), "r") as f:
        phonebooks[phonebook[:-5]] = loads(f.read())

try:
    os.mkdir("output")
except FileExistsError:
    pass

for name, phonebook in phonebooks.items():
    with open("output/{}.xml".format(name), "w") as f:
        f.write(pb_tm.render(name=phonebook["name"], prompt=phonebook["prompt"], entries=phonebook["entries"]))

with open("output/directory.xml", "w") as f:
    f.write(di_tm.render(phonebooks=[{"url": "{}/{}.xml".format(prefix, x), "name": pb["name"]} for x, pb in phonebooks.items()]))
