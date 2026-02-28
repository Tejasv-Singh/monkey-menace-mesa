import mesa
import math

def chebyshev_distance(pos1, pos2):
    return max(abs(pos1[0] - pos2[0]), abs(pos1[1] - pos2[1]))

class Human(mesa.Agent):
    """A student trying to reach the hostel with food."""
    def __init__(self, model):
        super().__init__(model)
        self.has_food = True

    def step(self):
        # Goal: reach Safe Zone (y > 17)
        if self.pos is None:
            return

        if self.pos[1] > 17:
            # Reached safe zone!
            if self.has_food:
                self.model.successful_deliveries += 1
                self.has_food = False # Set to false to prevent double counting
            return

        # Look for monkeys within radius 3
        neighbors = self.model.grid.get_neighbors(self.pos, moore=True, radius=3)
        monkeys = [n for n in neighbors if isinstance(n, Monkey)]

        if monkeys:
            # Panic and Flee!
            closest_monkey = min(monkeys, key=lambda m: chebyshev_distance(self.pos, m.pos))
            possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
            
            # Choose the step that maximizes distance from the closest monkey
            valid_steps = [p for p in possible_steps if self.model.grid.is_cell_empty(p) or not any(isinstance(a, Monkey) for a in self.model.grid.get_cell_list_contents([p]))]
            if not valid_steps:
                valid_steps = possible_steps
            best_step = max(valid_steps, key=lambda p: chebyshev_distance(p, closest_monkey.pos))
            self.model.grid.move_agent(self, best_step)
        else:
            # Move towards the Safe Zone
            possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
            # Filter steps that go "up" towards the hostel
            up_steps = [p for p in possible_steps if p[1] > self.pos[1]]
            
            if up_steps:
                self.model.grid.move_agent(self, self.random.choice(up_steps))
            else:
                if possible_steps:
                    self.model.grid.move_agent(self, self.random.choice(possible_steps))


class Monkey(mesa.Agent):
    """A notorious campus macaque looking for an easy meal."""
    def __init__(self, model, random_error=0.1):
        super().__init__(model)
        self.satiated = False
        self.random_error = random_error

    def step(self):
        if self.pos is None:
            return
            
        # Steal paratha if in the same cell as a human with food
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        humans_with_food = [obj for obj in cellmates if isinstance(obj, Human) and obj.has_food]
        
        if humans_with_food:
            target = humans_with_food[0]
            target.has_food = False
            self.satiated = True
            self.model.stolen_meals += 1
            # Acquired target!

        # Movement Phase
        if self.satiated or self.random.random() < self.random_error:
            # Move randomly (either full, or distracted by a shiny object)
            possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
            if possible_steps:
                self.model.grid.move_agent(self, self.random.choice(possible_steps))
        else:
            # Look for humans carrying food within radius 5
            neighbors = self.model.grid.get_neighbors(self.pos, moore=True, radius=5)
            targets = [n for n in neighbors if isinstance(n, Human) and n.has_food]
            
            if targets:
                # The "Chase" algorithm
                closest_target = min(targets, key=lambda t: chebyshev_distance(self.pos, t.pos))
                possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
                
                # Move to the step that minimizes distance to the prey
                if possible_steps:
                    best_step = min(possible_steps, key=lambda p: chebyshev_distance(p, closest_target.pos))
                    self.model.grid.move_agent(self, best_step)
            else:
                # Patrol around randomly
                possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
                if possible_steps:
                    self.model.grid.move_agent(self, self.random.choice(possible_steps))


class MonkeyMenaceModel(mesa.Model):
    """A model of monkeys terrorizing students for their food on campus."""
    def __init__(self, num_humans=10, num_monkeys=5, random_error=0.2):
        super().__init__()
        self.num_humans = num_humans
        self.num_monkeys = num_monkeys
        self.random_error = random_error

        # 20x20 campus grid
        self.grid = mesa.space.MultiGrid(20, 20, torus=False)
        
        self.successful_deliveries = 0
        self.stolen_meals = 0

        self.datacollector = mesa.DataCollector(
            model_reporters={
                "Successful Deliveries": lambda m: m.successful_deliveries,
                "Stolen Meals": lambda m: m.stolen_meals,
            }
        )

        # Place Humans
        for _ in range(self.num_humans):
            a = Human(self)
            # Start students near the academic blocks (bottom of the grid)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(5)
            self.grid.place_agent(a, (x, y))

        # Place Monkeys
        for _ in range(self.num_monkeys):
            m = Monkey(self, random_error=self.random_error)
            # Monkeys start a bit higher up, ready to intercept
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(5, 12) 
            self.grid.place_agent(m, (x, y))

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        """Advance the model by one step."""
        self.agents.shuffle_do("step")
        self.datacollector.collect(self)
        
        # Check if the simulation should end:
        # Stop condition: all humans are either safe in the hostel or lost their food
        all_done = True
        for agent in self.agents:
            if isinstance(agent, Human):
                if agent.has_food and agent.pos and agent.pos[1] <= 17:
                    all_done = False
                    break
        if all_done:
            self.running = False
