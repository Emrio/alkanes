class colors:
  HEADER = '\033[95m'
  OKBLUE = '\033[94m'
  OKGREEN = '\033[92m'
  WARNING = '\033[93m'
  FAIL = '\033[91m'
  ENDC = '\033[0m'
  BOLD = '\033[1m'
  UNDERLINE = '\033[4m'
  def header(txt): return f"{colors.HEADER}{txt}{colors.ENDC}"
  def okblue(txt): return f"{colors.OKBLUE}{txt}{colors.ENDC}"
  def okgreen(txt): return f"{colors.OKGREEN}{txt}{colors.ENDC}"
  def warning(txt): return f"{colors.WARNING}{txt}{colors.ENDC}"
  def fail(txt): return f"{colors.FAIL}{txt}{colors.ENDC}"
  def bold(txt): return f"{colors.BOLD}{txt}{colors.ENDC}"
  def underline(txt): return f"{colors.UNDERLINE}{txt}{colors.ENDC}"
