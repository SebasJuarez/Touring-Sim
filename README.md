# Touring-Sim
Video de explicacion:

https://youtu.be/fA1iulyMmCE

Este proyecto implementa un simulador de Máquina de Turing en Python. Procesa cadenas de entrada según un conjunto de estados y transiciones definidos en archivos YAML. El simulador puede manejar múltiples cadenas de entrada y genera los resultados paso a paso, incluyendo el estado final y la aceptación o rechazo de cada cadena.

## Caracteristicas
- Soporta configuraciones personalizadas de Máquina de Turing definidas en archivos YAML.
- Simula el procesamiento de las cadenas de entrada paso a paso, mostrando las transiciones.
- Permite trabajar con múltiples cadenas de entrada para un solo diseño de Máquina de Turing.
- Guarda los resultados, incluyendo las transiciones y estados finales, en archivos de salida.

## Requisitos
- Python 3.9+
Librerías:
- yaml (PyYAML)

Para instalar yaml puedes usar el comando:
```bash
pip install pyyaml
```
## Estructura del Proyecto

- Archivos YAML:
  - Recognizer.yaml: Define una Máquina de Turing para reconocer cadenas específicas.
  - Alterer.yaml: Define otra Máquina de Turing para un propósito distinto.
- Código Python:
  - TuringSim.py: Implementa el simulador de la Máquina de Turing.
- Archivos de salida:
  - recognizer_output.txt: Contiene los resultados del procesamiento de Recognizer.yaml. 
  - alterer_output.txt: Contiene los resultados del procesamiento de Alterer.yaml.

## Formato del Yaml:

El YAML debe incluir:

- Estados (q_states): Lista de estados, estado inicial, estados finales y de aceptación.
- Alfabeto (alphabet y tape_alphabet): Definición de los símbolos permitidos en las cadenas de entrada y la cinta.
- Símbolo en blanco (blank): Carácter que representa una celda vacía en la cinta.
- Transiciones (delta): Lista de transiciones con estado inicial, entrada en la cinta, estado final, salida en la cinta y movimiento del cabezal.
- Cadenas de prueba (simulation_strings): Lista de cadenas de entrada a procesar.

Ejemplo:
```bash
q_states:
  q_list: ["q0", "q1", "qacc", "qrej"]
  initial: "q0"
  final: ["qacc", "qrej"]
  accept: ["qacc"]

alphabet: ["a", "b"]
tape_alphabet: ["a", "b", "B"]
blank: "B"

delta:
  - { params: { initial_state: "q0", tape_input: "a" }, output: { final_state: "q1", tape_output: "B", tape_displacement: "R" } }
  - { params: { initial_state: "q1", tape_input: "b" }, output: { final_state: "qacc", tape_output: "B", tape_displacement: "R" } }
  - { params: { initial_state: "q0", tape_input: "b" }, output: { final_state: "qrej", tape_output: "B", tape_displacement: "R" } }

simulation_strings: ["ab", "bb", "aa"]
```

## ¿Cómo usar?
1. Crea las transiciones y ponlas en el YAML para cada maquina, la reconocedora y la alteradora.
2. Ejecuta el script principal TuringSim.py:
```bash
python TuringSim.py
```
3. Los resultados se guardarán en los archivos de salida correspondientes (recognizer_output.txt y alterer_output.txt).
