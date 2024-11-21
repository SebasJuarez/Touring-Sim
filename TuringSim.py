import yaml


class Tape:
    blankSymbol = " "

    def __init__(self, input_string="", blank=" "):
        self.__tape = dict(enumerate(input_string))
        Tape.blankSymbol = blank

    def __str__(self):
        min_index = min(self.__tape.keys())
        max_index = max(self.__tape.keys())
        return "".join(self.__tape.get(i, Tape.blankSymbol) for i in range(min_index, max_index + 1))

    def read_symbol(self, position):
        return self.__tape.get(position, Tape.blankSymbol)

    def write_symbol(self, position, char):
        self.__tape[position] = char


class TuringMachine:
    def __init__(self, input_strings, blank_symbol, initial_state, final_states, transitions, accept_states, output_file):
        self.__initialState = initial_state
        self.input_strings = input_strings
        self.__currentInputIndex = 0
        self.__blankSymbol = blank_symbol
        self.__currentTape = Tape(input_strings[self.__currentInputIndex], self.__blankSymbol)
        self.__headPosition = 0
        self.__currentState = initial_state
        self.__transitionFunction = transitions
        self.__finalStates = set(final_states)
        self.__acceptStates = set(accept_states)
        self.output_file = output_file

        self.__initialize_output_file()

    def __initialize_output_file(self):
        with open(self.output_file, 'w') as f:
            f.write("Turing Machine Simulation\n")
            f.write("=========================\n\n")

    def load_next_input(self):
        self.__currentInputIndex += 1
        if self.__currentInputIndex < len(self.input_strings):
            self.__currentTape = Tape(self.input_strings[self.__currentInputIndex], self.__blankSymbol)
            self.__headPosition = 0
            self.__currentState = self.__initialState
            return True
        return False

    def log_state_transition(self, before, after):
        with open(self.output_file, 'a') as f:
            f.write(f"{before} -> {after}\n")

    def execute_single_step(self):
        current_symbol = self.__currentTape.read_symbol(self.__headPosition)
        transition = self.__transitionFunction.get((self.__currentState, current_symbol))

        before_state = f"State: {self.__currentState}, Head: {self.__headPosition}, Tape: {self.__currentTape}"

        if transition:
            new_state, write_char, direction = transition
            self.__currentTape.write_symbol(self.__headPosition, write_char)
            self.__headPosition += 1 if direction == "R" else -1
            self.__currentState = new_state
        else:
            self.__currentState = "qrej"

        after_state = f"State: {self.__currentState}, Head: {self.__headPosition}, Tape: {self.__currentTape}"
        self.log_state_transition(before_state, after_state)

    def is_in_final_state(self):
        return self.__currentState in self.__finalStates

    def process_current_input(self):
        with open(self.output_file, 'a') as f:
            f.write(f"Input: {self.__currentTape}\n\n")

        while not self.is_in_final_state():
            self.execute_single_step()

        with open(self.output_file, 'a') as f:
            f.write(f"Final State: {self.__currentState}\n")
            f.write(f"Output: {self.__currentTape}\n")
            result = "Accepted" if self.__currentState in self.__acceptStates else "Not Accepted"
            f.write(f"Result: {result}\n")
            f.write("\n" + "=" * 40 + "\n")

        if self.load_next_input():
            self.process_current_input()


def initialize_turing_machine(filename, output_file):
    with open(filename, 'r') as yaml_file:
        config = yaml.load(yaml_file, Loader=yaml.FullLoader)

    initial_state = config['q_states']['initial']
    final_states = config['q_states']['final']
    accept_states = config['q_states']['accept']
    blank_symbol = config['blank']
    transitions = {}
    input_strings = config['simulation_strings']

    for delta in config['delta']:
        transitions[(delta['params']['initial_state'], delta['params']['tape_input'])] = (
            delta['output']['final_state'], delta['output']['tape_output'], delta['output']['tape_displacement'])

    return TuringMachine(input_strings, blank_symbol, initial_state, final_states, transitions, accept_states, output_file)


# MAIN
recognizer_simulator = initialize_turing_machine("Recognizer.yaml", "recognizer_output.txt")
recognizer_simulator.process_current_input()

alterer_simulator = initialize_turing_machine("Alterer.yaml", "alterer_output.txt")
alterer_simulator.process_current_input()

print("Simulations completed. Results saved in 'recognizer_output.txt' and 'alterer_output.txt'.")
