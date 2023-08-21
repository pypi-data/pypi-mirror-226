from if_dsl_gui_ai.dslClasses import GameWorld, Region, Item, Player
from textx import metamodel_from_file
from os.path import join, dirname


class HealAction:
    def __init__(self, name, amount):
        self.name = name
        self.amount = amount


def parse_dsl(dsl_path, game_path):
    # Load the metamodel from the DSL grammar
    this_folder = dirname(__file__)
    dsl_mm = metamodel_from_file(join(this_folder, dsl_path))

    # Parse the DSL file and create the GameWorld
    # model = dsl_mm.model_from_file(join(this_folder+"\\games\\"+game_path, game_path))
    model = dsl_mm.model_from_file(join("if_dsl_gui_ai\\games\\" + game_path, game_path))

    game_world = GameWorld()

    # Create regions
    for region_def in model.regions:
        region = Region(region_def.name)
        properties(region, region_def)
        for connection in region_def.connections:
            region.add_connection(connection.direction, connection.target)
        if region_def.requirements:
            region.add_requirements(region_def.requirements.item)
        for prop in region_def.properties:
            prop_name = prop.__class__.__name__
            if prop_name == "ContainsProperties":
                for item in prop.contains:
                    region.items.append(item)
        game_world.regions.append(region)

    # Create items
    for item_def in model.items:
        item = Item(item_def.name,item_def.isStatic)
        properties(item, item_def)
        game_world.items.append(item)

    # Create player
    player_def = model.player
    starting_position = None
    for prop in player_def.properties:
        prop_name = prop.__class__.__name__
        if prop_name == "PositionProperties":
            for player_region in game_world.regions:
                if prop.position.name == player_region.name:
                    starting_position = player_region
        elif prop_name == "HealthProperties":
            health = prop.health
        elif prop_name == "ScoreProperties":
            score = prop.score
        elif prop_name == "InventoryProperties":
            inventory = []
            for item in prop.inventory:
                inventory.append(item.name)
    player = Player(player_def.name, starting_position)
    player.health = health
    player.score = score
    player.inventory = inventory
    properties(player, player_def)
    game_world.player = player

    # Set start and final positions
    for player_region in game_world.regions:
        if player_region.name == model.start_position.name:
            game_world.set_start_position(player_region)
        elif player_region.name == model.final_position.name:
            game_world.set_final_position(player_region)

    return game_world


def properties(obj, obj_def):
    for prop in obj_def.properties:
        prop_name = prop.__class__.__name__
        if prop_name == "PortrayalProperties":
            prop_value = prop.portrayal
        elif prop_name == "ContainsProperties":
            prop_value = []
            for item in prop.contains:
                prop_value.append(item.name)
        elif prop_name == "ActivationProperties":
            action_name = prop.action.__class__.__name__
            if action_name == "HealAction":
                prop_value = HealAction(action_name, prop.action.amount)
        elif prop_name == "HealthProperties":
            prop_value = prop.health
        elif prop_name == "ScoreProperties":
            prop_value = prop.score
        elif prop_name == "InventoryProperties":
            prop_value = []
            for item in prop.inventory:
                prop_value.append(item.name)
        elif prop_name == "PositionProperties":
            prop_value = prop.position.name

        obj.add_property(prop_name, prop_value)
