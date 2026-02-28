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
    "num_humans": solara.SliderInt(label="Number of Students (Humans)", value=20, min=1, max=50),
    "num_monkeys": solara.SliderInt(label="Number of Monkeys (Mega Troop)", value=10, min=1, max=50),
    "random_error": solara.SliderFloat(label="Monkey Distractibility (Shiny Object factor)", value=0.2, min=0.0, max=1.0, step=0.1),
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
