import unicodedata

carbon_chain_names = ['']
multiplicative = ['']

def load_data(chain_names_path, multiplicative_path):
  global carbon_chain_names, multiplicative
  with open(chain_names_path, 'r') as f:
      carbon_chain_names.extend(f.read().split('\n'))
  with open(multiplicative_path, 'r') as f:
      multiplicative.extend(f.read().split('\n'))

def remove_accents(txt): # transforms "éthyl" in "ethyl" (used for sorting ramifications which does not suppport accents)
    return u"".join([ c for c in unicodedata.normalize('NFKD', txt) if not unicodedata.combining(c) ])

class Carbon:
  def __init__(self, id, neighbors = None):
    self.id = id
    self.neighbors = neighbors if neighbors is not None else []
    self.ramification_depth = -1

  def set_neighbors(self, neighbors):
    self.neighbors = neighbors

  def add_neighbor(self, neighbor):
    print('ADDING TO ', self)
    if len(self.neighbors) >= 4:
      raise Exception("A carbon atom can't have more than 4 neighbors!")
    self.neighbors.append(neighbor)

  def get_depth(self):
    return self.ramification_depth

  def set_depth(self, depth):
      if self.ramification_depth != -1: raise Exception("Can't set depth of a carbon atom more than once!")
      self.ramification_depth = depth

  def __repr__(self):
      return f"Carbon {self.id} : depth={self.ramification_depth} : {self.neighbors}"

class Molecule():
  def __init__(self, carbons, log = False):
    self.carbons = carbons
    self.log = log

  def find_max_length(self, current_carbon, current_length = 1, origin_id = -1): # find longest sub chain of undefined carbons
    if len(self.carbons[current_carbon].neighbors) == 1 and current_length != 1: # edge carbon
      return (current_carbon, current_length)
    max_length = 1
    max_length_edge_carbon = current_carbon
    for neighbor_id in self.carbons[current_carbon].neighbors:
      if neighbor_id == origin_id or self.carbons[neighbor_id].get_depth() != -1:
        continue
      subchain_carbon_id, subchain_max_length = self.find_max_length(neighbor_id, current_length + 1, current_carbon)
      if subchain_max_length > max_length:
        max_length = subchain_max_length
        max_length_edge_carbon = subchain_carbon_id
    return (max_length_edge_carbon, max_length)

  def set_deph_to_subchain(self, current_carbon, depth, length, origin_id = -1):
    if len(self.carbons[current_carbon].neighbors) == 1 and length == 1:
      self.carbons[current_carbon].set_depth(depth)
      return True
    elif len(self.carbons[current_carbon].neighbors) == 1 and origin_id != -1:
      return False
    for neighbor_id in self.carbons[current_carbon].neighbors:
      if neighbor_id == origin_id or self.carbons[neighbor_id].get_depth() != -1:
        continue
      if self.set_deph_to_subchain(neighbor_id, depth, length - 1, current_carbon):
        self.carbons[current_carbon].set_depth(depth)
        return True
    return False

  # find max length in an "undefined section of the molecule" (ie depth == -1 atoms)
  # begin carbon must be on the edge of the undefined graph section!
  def find_longest_chain(self, begin_carbon):
    first = self.find_max_length(begin_carbon)
    return self.find_max_length(first[0]) # max length and one edge atom of the max chain

  # find all of the carbon atoms connected to a carbon of the given chain (chain defined by one edge carbon and the global depth of the chain)
  def find_undefined_carbons_next_to_subchain(self, cur_depth, current_carbon, origin, i):
    undefined_carbons = [ (i, current_carbon, c) for c in self.carbons[current_carbon].neighbors if self.carbons[c].get_depth() == -1 ]
    next_carbons = [ c for c in self.carbons[current_carbon].neighbors if self.carbons[c].get_depth() == cur_depth and c != origin ]
    if len(next_carbons) == 1:
      next_undefined_carbons = self.find_undefined_carbons_next_to_subchain(cur_depth, next_carbons[0], current_carbon, i + 1)
      undefined_carbons.extend(next_undefined_carbons)
    return undefined_carbons

  # recursively name the chains
  def set_atoms_depth(self, start_carbon, depth = 0):
    end_carbon, length = self.find_max_length(start_carbon) # find longest chain  in this subchain
    print(f" * considering chain {start_carbon}-{end_carbon} (length={length} ; depth={depth}):") if self.log else None
    self.set_deph_to_subchain(start_carbon, depth, length)
    nexts_to_propagate = self.find_undefined_carbons_next_to_subchain(depth, start_carbon, -1, 0)
    ramifications = [] # objects: { name: str, ramifications: str, indices: int[] }
    for (i, _, next_carbon) in nexts_to_propagate:
      cur_ramification = self.set_atoms_depth(next_carbon, depth + 1) # type: { name: str, ramfications: str }
      new = True
      for ramification in ramifications:
        if ramification["name"] == cur_ramification["name"] and ramification["ramifications"] == cur_ramification["ramifications"]:
          ramification["indices"].append(i + 1)
          new = False
          break
      if new:
        ramifications.append({ "name": cur_ramification["name"], "ramifications": cur_ramification["ramifications"], "indices": [ i + 1 ] })
    ramifications.sort(key=lambda a: remove_accents(a["name"]))
    ramifications_str = "-".join([ ",".join(map(str, ramification["indices"])) + "-" + ramification["ramifications"] + multiplicative[len(ramification["indices"])] + ramification["name"] for ramification in ramifications ])
    if depth > 0 and len(ramifications_str) > 1:
      ramifications_str = f"({ramifications_str})" # parentheses for clarity
    termination = "ane" if depth == 0 else "yl"
    name = carbon_chain_names[length] + termination
    return { "name": name, "ramifications": ramifications_str }

  def get_name(self):
    c, _ = self.find_longest_chain(0)
    molecule_name = self.set_atoms_depth(c)
    return molecule_name['ramifications'] + molecule_name['name']
