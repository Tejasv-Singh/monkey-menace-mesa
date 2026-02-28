import solara
from mesa.visualization import SolaraViz, make_space_component, make_plot_component
from model import MonkeyMenaceModel, Human, Monkey

def agent_portrayal(agent):
    """
    Define how agents should be rendered in the grid.
    """
    if isinstance(agent, Human):
        return {
            "color": "tab:blue" if agent.has_food else "tab:grey",
            "marker": "o",
            "size": 50,
        }
    elif isinstance(agent, Monkey):
        return {
            "color": "tab:red" if not agent.satiated else "tab:green",
            "marker": "^",
            "size": 50,
        }

# Define model parameters to be controllable via the UI
model_params = {
    "num_humans": {
        "type": "SliderInt",
        "value": 20,
        "label": "Number of Students (Humans)",
        "min": 1,
        "max": 50,
        "step": 1,
    },
    "num_monkeys": {
        "type": "SliderInt",
        "value": 10,
        "label": "Number of Monkeys (Mega Troop)",
        "min": 1,
        "max": 50,
        "step": 1,
    },
    "random_error": {
        "type": "SliderFloat",
        "value": 0.2,
        "label": "Monkey Distractibility (Shiny Object factor)",
        "min": 0.0,
        "max": 1.0,
        "step": 0.1,
    },
}

SpaceGraph = make_space_component(agent_portrayal)
LinePlot = make_plot_component({"Successful Deliveries": "tab:blue", "Stolen Meals": "tab:red"})

model = MonkeyMenaceModel()

app = SolaraViz(
    model,
    components=[SpaceGraph, LinePlot],
    model_params=model_params,
    name="The NIT Hamirpur Monkey Menace"
)
