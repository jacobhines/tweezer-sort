import os
import sys
fp = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, fp)

import simulation, detection, sorting