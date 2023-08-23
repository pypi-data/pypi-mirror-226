import yaml

data = yaml.safe_load(open("../test/project.yml", "r"))

x = yaml.dump(data=data)
print(x)