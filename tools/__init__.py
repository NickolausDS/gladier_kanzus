from gladier.defaults import GladierDefaults as GladierBaseTool

from .create_phil import funcx_create_phil
from .dials_stills import funcx_stills_process

__all__ = ['CreatePhil','DialsStills']


class CreatePhil(GladierBaseTool):
    flow_definition = None
    required_input = []
    # funcx_endpoints = dict()
    funcx_functions = [
        funcx_create_phil
    ]

class DialsStills(GladierBaseTool):
    flow_definition = None
    required_input = []
    # funcx_endpoints = dict()
    funcx_functions = [
        funcx_stills_process
    ]


# DialsVersion = GladierBaseTool()

# Pilot = GladierBaseTool()

# Prime = GladierBaseTool()

# Primalisys = GladierBaseTool()
