# The NIT Hamirpur Monkey Menace 🐒

An Agent-Based Model (ABM) built with [Mesa](https://github.com/projectmesa/mesa) to simulate the perilous journey of students carrying food past the notorious monkeys at NIT Hamirpur.

## Overview
This simulation uses Mesa 3.5.0's features and integrates deeply with the new `SolaraViz` UI for a responsive and slick browser-based visualization.

### Agents & Behavior
*   **Humans (Students)** target the Safe Zone (representing their hostel block). If a monkey enters within a 3-block radius, they panic and attempt to flee by finding a move that maximizes their distance from the monkey. If they successfully reach home with their food, it counts as a **Successful Delivery**. 
*   **Monkeys (Macaques)** setting up a perimeter. They feature an integrated `random_error` parameter to simulate "shiny object distraction", giving humans a slim chance of surviving the campus crossing. Otherwise, monkeys run a chase algorithm if they sniff out a student with food within a 5-cell radius. When a meal is stolen, a human loses their food, and **Stolen Meals** counter ticks up.

## Installation

Ensure you have Python 3.10+ installed.

1. Clone this repository:
```bash
git clone https://github.com/Tejasv-Singh/monkey-menace-mesa.git
cd monkey-menace-mesa
```

2. Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate
pip install mesa solara matplotlib altair
```

## Running the Simulation

This project uses Solara to render the simulation in the browser.

```bash
solara run app.py
```

Then, open your browser and navigate to `http://localhost:8765`.

## UI Controls
- **Number of Students:** Adjust the amount of humans trying to cross the campus.
- **Number of Monkeys:** Scale the size of the macaques "Mega Troop".
- **Monkey Distractibility:** Change the `random_error` factor (0.0 to 1.0) to see how often monkeys get distracted by shiny objects instead of chasing students.
- **Play/Step:** Run the simulation continuously or step-by-step to closely observe the chasing and fleeing behaviors.
