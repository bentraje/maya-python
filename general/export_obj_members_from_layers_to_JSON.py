import pymel.core as pm
import json

layer_list = pm.ls(type="displayLayer")
layer_dict = {}
member_type = []
file_path = "D:\\dog_layers.json"

for layer in layer_list:
	member_nodes = layer.listMembers()
	member_names = [ member.name() for member in member_nodes if not "Shape" in member.name()]
	layer_dict[layer.getName()] = member_names


with open(file_path, "w") as f:
	json.dump(layer_dict, f, indent=4)
