import sys
import traceback
from colors import colors
from alkanes import Molecule, Carbon, load_data

ids = list('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ@#')

def index(l, e):
  try: return l.index(e)
  except ValueError: return None

def clear():
  print(chr(27) + "[2J")

def sandboxed_exec(f, *args):
  try:
    return f(*args)
  except KeyboardInterrupt as e:
    print('Program interrupted.')
    return 'exit'
  except EOFError as e:
    print('Program interrupted.')
    return 'exit'
  except Exception as e:
    traceback.print_exc()
    print(f"\n\t\t^^^^^^^^\n" + colors.fail('Outch! A routine failed during execution. Please make sure to report this error.'))

def cmd_parser(cmd):
  cmd = cmd.strip()
  if cmd == 'exit':
    print('Bye.')
    return False
  elif cmd == 'parse manual':
    sandboxed_exec(manual_parser)
  elif cmd == 'parse' or cmd == 'parse interactive':
    sandboxed_exec(interactive_parser)
  elif cmd == 'help':
    print("""List of available commands:
  - 'parse' : Opens the interactive parser
  - 'parse interactive' : Opens the interactive parser
  - 'parse manual' : Opens the manual parser
  - 'help' : Shows this page
  - 'exit' : Exits the CLI""")
  elif cmd != '' and cmd != None:
    print(f"Unknown command '{colors.okblue(cmd)}'. Please check for typos or type 'help'")
  return True

def prompt():
  cmd = sandboxed_exec(input, ' > ')
  return prompt() if cmd_parser(cmd) else None

def startup():
  load_data('names.txt', 'multiplicative.txt')
  print(f"""
       * {colors.bold(colors.header('Alkanes'))} *

This tool names alkane molecules you provide.
IMPORTANT: Please make sure the molecules you feed in are real non-cyclical alkanes
This tool provides two parser input methods: manual and interactive
Type 'help' for help on the commands available
""")
  prompt()

def manual_parser():
  N = int(input("Number of carbon atoms: "))
  L = int(input("Number of bonds between carbon atoms: "))
  print(f"Please write {L} lines describing the bonds. For instance, type '1 2' if carbon #1 and carbon #2 are linked.")
  carbons = [ Carbon(i) for i in range(N) ]
  for _ in range(L):
    a, b = map(int, input().split(' '))
    carbons[a].add_neighbor(b)
    carbons[b].add_neighbor(a)
  name = Molecule(carbons, log=False).get_name()
  print(f"\nResult:\n{name}\n")

def interactive_parser():
  carbons = [Carbon(0)]
  clear()
  print(f"""Describe the bonds between the carbon atoms. At each step, you will add a new carbon atom, write the name of the carbon atom to which it is attached to (e.g: type 4 if the next atom is bound to the #4 atom)
Type -1 when you don't wan't to add any new carbon atoms
{colors.warning('WARNING')}: This parser can only handle up to {len(ids)} carbon atoms! For larger molecules, please use the manual parser.
{colors.warning('WARNING')}: This parser comes with a previewer which might still be buggy!""")
  while True:
    sandboxed_exec(representMolecule, (carbons))
    carbon = input(' >> ')
    if carbon == '-1':
      return printMoleculeName(carbons)
    i = index(ids, carbon)
    if i is None or i >= len(carbons):
      print(f"Error: Id {carbon} does not exist.")
      continue
    carbons.append(Carbon(ids[i + 1]))
    a, b = i, len(carbons) - 1
    carbons[a].add_neighbor(b)
    carbons[b].add_neighbor(a)
    if len(carbons) == len(ids):
      print('Max carbon id reached. Parsing this molecule...')
      return printMoleculeName(carbons)
    clear()

def printMoleculeName(carbons):
  name = Molecule(carbons, log=False).get_name()
  print(f"\nResult:\n{name}\n")

def representMolecule(carbons):
  SIZE = (len(carbons) + 4) * 6
  twodspace = [[-1 for y in range(0, SIZE)] for x in range(0, SIZE)]
  # position atoms on the screen
  currents, nexts = [(0, -1, round(SIZE / 2), round(SIZE / 2))], []
  while len(currents):
    for cur, origin, x, y in currents:
      twodspace[x][y] = cur
      positions = [(x + 4, y), (x - 4, y), (x, y + 4), (x, y - 4)]
      next_positions = [position for position in positions if all(coord >= 0 and coord < SIZE for coord in position) and twodspace[position[0]][position[1]] == -1]
      for neighbor in carbons[cur].neighbors:
        if neighbor == origin: continue
        try: position = next_positions.pop(0)
        except Exception as e: return print(f"{colors.warning('WARNING')}: Can't represent this molecule!")
        nexts.append((neighbor, cur, position[0], position[1]))
    currents, nexts = nexts, []
  # nice displaying
  showLine = 0
  show = [''] * (SIZE - 4)
  for y in range(2, SIZE - 2):
    for x in range(2, SIZE - 2):
      if twodspace[x][y] != -1:
        show[showLine] += ids[twodspace[x][y]]
      elif twodspace[x - 2][y] != -1 and index(carbons[twodspace[x - 2][y]].neighbors, twodspace[x + 2][y]) is not None:
        show[showLine] += '-'
      elif twodspace[x][y - 2] != -1 and index(carbons[twodspace[x][y - 2]].neighbors, twodspace[x][y + 2]) is not None:
        show[showLine] += '|'
      else:
        show[showLine] += ' '
    showLine += 1
  show = filter(lambda line: any([tile != ' ' for tile in line]), show)
  print('\n'.join(show))

startup()
