# ProDy: A Python Package for Protein Structural Dynamics Analysis
# 
# Copyright (C) 2010  Ahmet Bakan <ahb12@pitt.edu>
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#  
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

__author__ = 'Ahmet Bakan'
__copyright__ = 'Copyright (C) 2010 Ahmet Bakan'
__version__ = '0.0.2'

import logging
import logging.handlers
import os
import os.path

re = None
def importRE():
    import re as RE
    global re
    re = RE

la = None
def importScipyLinalg():
    try:
        import scipy.linalg as linalg
    except ImportError:
        raise ImportError('SciPy is required for NMA calculations')
    global la
    la = linalg

pl = None
def importPyPlot():
    try:
        import matplotlib.pyplot as pyplot
        from mpl_toolkits.mplot3d import Axes3D
    except ImportError:
        raise ImportError('Matplotlib is required for plotting')
    global pl
    pl = pyplot
    dynamics.plotting.pl = pl

KDTree = None
def importBioKDTree():
    try:
        from Bio.KDTree import KDTree as BioKDTree
    except ImportError:
        raise ImportError('BioPython is required for ENM calculations')
    global KDTree
    KDTree = BioKDTree

NCBIWWW = None
NCBIXML = None
def importBioBlast():
    try:
        from Bio.Blast import NCBIWWW as ncbiwww 
        from Bio.Blast import NCBIXML as ncbixml 
    except ImportError:
        raise ImportError('BioPython is required for Blast searching PDB.org')
    global NCBIWWW, NCBIXML
    NCBIWWW = ncbiwww
    NCBIXML = ncbixml

PWALIGN = None
def importBioPairwise2():
    try:
        from Bio import pairwise2 
    except ImportError:
        raise ImportError('BioPython is required for pairwise alignments')
    global PWALIGN
    PWALIGN = pairwise2


_ProDySettings = {
    'loglevel': 'debug',
    'local_pdb_folder': None}


def ProDyPrintSettings():
    print _ProDySettings

#ProDySettings = property(ProDySettings) 

LOGGING_LEVELS = {'debug': logging.DEBUG,
                  'info': logging.INFO,
                  'warning': logging.WARNING,
                  'error': logging.ERROR,
                  'critical': logging.CRITICAL}
LOGGING_LEVELS.setdefault(logging.INFO)
ProDySignature = '@>'

ProDyLogger = None

def _ProDyStartLogger(**kwargs):
    """Set a global logger for ProDy."""
    
    name = '.prody'
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    for handler in logger.handlers: 
        handler.close()
    logger.handlers = []
    
    console = logging.StreamHandler()
    console.setLevel(LOGGING_LEVELS[kwargs.get('console', 'debug')])
    console.setFormatter(logging.Formatter(ProDySignature + ' %(message)s'))
    logger.addHandler(console)
    global ProDyLogger
    ProDyLogger = logger

_ProDyStartLogger()

def ProDyStartLogfile(filename, **kwargs):
    """Start a file to save ProDy logs.
    
    :keyword filename: name of the logfile
    
    :keyword mode: mode in which logfile will be opened, default is "w" 
    
    :keyword backupcount: number of old *name.log* files to save, default is 1

    """
    
    """
    :keyword loglevel: loglevel for logfile verbosity
    :type loglevel: str, default is *debug*
    
    ======== ===========
    Loglevel Description
    ======== ===========
    debug    Eveything will be printed on the colsole or written into logfile.
    info     Only brief information will be printed or written.
    warning  Only critical information will be printed or written.
    error    This loglevel is equivalent to *warning* in package.
    critical This loglevel is equivalent to *warning* in package.
    ======== =========== 
    
    """
    global ProDyLogger
    logger = ProDyLogger
    logfilename = filename
    if isinstance(logfilename, str):
        rollover = False 
        # if filemode='a' is provided, rollover is not performed
        if os.path.isfile(logfilename) and kwargs.get('filemode', None) != 'a':
            rollover = True
        logfile = logging.handlers.RotatingFileHandler(logfilename, 
                    mode=kwargs.get('mode', 'a'), maxBytes=0,
                    backupCount=kwargs.get('backupcount', 1))
        logfile.setLevel(LOGGING_LEVELS[kwargs.get('loglevel', 'debug')])
        logfile.setFormatter(logging.Formatter('%(message)s'))
        logger.addHandler(logfile)
        if rollover:
            logger.info('Backing up existing logfile "{0:s}" and starting a new one.'
                         .format(filename))
            logfile.doRollover()
        else:
            logger.info('Logfile "{0:s}" has been started.'.format(filename))


def ProDyCloseLogfile(filename):
    """Close logfile with *filename*."""
    filename = str(filename)

    global ProDyLogger
    logger = ProDyLogger
    for index, handler in enumerate(logger.handlers):
        if isinstance(handler, logging.handlers.RotatingFileHandler):
            if handler.stream.name in (filename, os.path.abspath(filename)):
                logger.info('Closing logfile {0:s}'.format(filename))
                handler.close()
                logger.handlers.pop(index)
                return
    logger.warning('Logfile "{0:s}" was not found.'.format(filename))

def ProDyMute():
    """ProDy will only print warnings."""
    ProDyLogger.debug('Good bye :|')
    ProDyLogger.handlers[0].level = LOGGING_LEVELS['warning']

def ProDyUnmute():
    """ProDy will only print some useful information."""
    ProDyLogger.handlers[0].level = LOGGING_LEVELS['info']
    ProDyLogger.info('Hi again :)')

def ProDyTalkToMe():
    """ProDy will print both useful and not so useful information."""
    ProDyLogger.handlers[0].level = LOGGING_LEVELS['debug']
    ProDyLogger.debug('Hello world :D')

def ProDyShutUp():
    """ProDy will not print anything."""
    ProDyLogger.handlers[0].level = LOGGING_LEVELS['critical']


try:
    import numpy as np
except ImportError, err:
    raise ImportError('numpy not found, it is a required package')

__all__ = ['ProDyStartLogfile', 'ProDyCloseLogfile']
#           'ProDyTalkToMe', 'ProDyMute', 'ProDyUnmute', 'ProDyShutUp']

import proteins
__all__.append('proteins')
from proteins import *
__all__ += proteins.__all__

import dynamics
__all__.append('dynamics')
from dynamics import *
__all__ += dynamics.__all__

import prody

__all__.append('prody')


def ProDySetLocalPDBFolder(path):
    pass

def ProDyStartLogFile(filename):
    pass

def ProDySetVerbosity(level):
    pass
