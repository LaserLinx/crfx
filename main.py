from dataclasses import dataclass, field
import colorama
import os
import prompt_toolkit

import json

WHITE = colorama.Fore.WHITE
GREEN = colorama.Fore.GREEN
MAGENTA = colorama.Fore.MAGENTA

def build_grid(grid: dict,grid_width=10,grid_height=10) -> str:
	ui = ""
	if grid:
		for row in range(0,grid_height):
			row_ui = ""
			vals = {}
			for col in range(0,grid_width):
				item = grid.get(f"{row}x{col}")
				if item:
					row_ui += f"┏━{GREEN}{item.get("id")}{WHITE}━┓"
					vals[item.get("id")] = item.get("value"," ")
				else:
					row_ui += 5*" "
			ui += f"{row_ui}\n"
			row_ui = row_ui.replace(WHITE,"").replace(GREEN,"")
			for ch in row_ui:
				match ch:
					case "┏" | "┓": ui += "┃"
					case " ": ui += " "
					case "━": ui += " "
					case i: ui += vals.get(i," ")
			ui += "\n"
			for ch in row_ui:
				match ch:
					case " ": ui+=" "
					case "┏": ui+="┗"
					case "┓": ui+="┛"
					case _: ui+="━"
			ui += "\n"
			
	return ui

def build_sets(sets: dict) -> str:
	ui = ""
	for k in sets.keys():
		ui += f"{MAGENTA}{k}:{WHITE} {sets.get(k)}\n"
	return ui

def compare_layout(a:str,b:str,separator:str = "┃  ") -> str:
	ui = ""
	a_lines = a.split("\n")
	b_lines = b.split("\n")
	length = len(a_lines)
	ui += (len(a_lines[1]))*"━"+"\n"
	if len(b_lines) > length:
		length = len(b_lines)
	for index in range(0,length-1):
		try: a_content = a_lines[index].replace("\n","")
		except: a_content = ""
		try: b_content = b_lines[index].replace("\n","")
		except: b_content = ""
		ui += f"{a_content}{separator}{b_content}\n"
	ui += (len(a_lines[1]))*"━"
	return ui



def load_recipe(path: str)-> dict:
	with open(path) as f:
		data: dict = json.loads(f.read())
	return data

@dataclass
class recipe_format():
	recipe_type: str
	grid: dict
	sets: dict = field(default_factory=dict)
	grid_width: int = 10
	grid_height: int = 10



recipe = recipe_format(**load_recipe("ui_format.json"))


while True:
	os.system("clear")
	print(WHITE)
	print(f"Recipe Type: {recipe.recipe_type}")
	
	print(compare_layout(build_grid(recipe.grid,recipe.grid_width,recipe.grid_height),build_sets(recipe.sets)))

	command = prompt_toolkit.prompt("/> ")
	
	if command in ["exit"]:
		if prompt_toolkit.choice("Do you want to save changes?",options=[(True,"Yes"),(False,"No")],show_frame=True,default=True):
			with open("ui_format.json","w") as f:
				f.write(json.dumps(recipe.__dict__,indent="\t"))
			break
		else:
			break
	if command.startswith("set "):
		set_commands = command.removeprefix("set ").split(" ")
		set_id = set_commands[0]
		set_value = set_commands[1]
		for k in recipe.grid.keys():
			if recipe.grid.get(k):
				if recipe.grid[k].get("id") == set_id:
					recipe.grid[k]["value"] = set_value
	
	if command.startswith("del "):
		del_commands = command.removeprefix("del ").split(" ")
		for del_id in del_commands:
			for k in recipe.grid.keys():
				if recipe.grid.get(k):
					if recipe.grid[k].get("id") == del_id:
						try: recipe.grid[k].pop("value")
						except: pass

	if command.startswith("addSet "):
		set_commands = command.removeprefix("addSet ").split(" ",1)
		recipe.sets[set_commands[0]] = set_commands[1]
	if command.startswith("delSet"):
		set_commands = command.removeprefix("delSet ").split(" ")
		for i in set_commands:
			try:
				recipe.sets.pop(i)
			except: pass

	if command.startswith("setCords "):
		set_commands = command.removeprefix("setCords ").split(" ")
		if set_commands[3] == "True":
			recipe.grid[set_commands[0]] = {"id": set_commands[1], "value": set_commands[2]}
	if command.startswith("delCords "):
		set_commands = command.removeprefix("delCords ").split(" ")
		if set_commands[1] == "True":
			recipe.grid[set_commands[0]] = None
					
		
	
	





