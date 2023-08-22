
import svgwrite
from svgwrite import cm, mm, px  

from pathlib import Path

import utils.config as config

from utils.logger import LOGGER
from utils.StyleSheet import StyleSheet


class Drawing(object):
    
    DWG = None
    
    @classmethod    
    def setOutputSVGPath(cls, outputSVGPath):
        if(outputSVGPath is not None):
            cls.__outputSVGPath = outputSVGPath
    
    @classmethod    
    def setCssStyleSheet(cls, cssStyleSheet):
        if(cssStyleSheet is not None):
            cls.__cssStyleSheet = cssStyleSheet
        
    @classmethod
    def create(cls, outputSVGPath, cssStyleSheet = None):
        
        cls.setOutputSVGPath(outputSVGPath)
        cls.setCssStyleSheet(cssStyleSheet)
        
        cls.DWG = svgwrite.Drawing(cls.__outputSVGPath, debug=True)
        if(cls.__cssStyleSheet is not None) :
            cls.DWG.embed_stylesheet(cls.__cssStyleSheet)
            StyleSheet.loadFromCSSStyleSheet(cls.__cssStyleSheet) 

    @classmethod            
    def reset(cls):
        cls.create(cls.__outputSVGPath, cls.__cssStyleSheet)

    @classmethod        
    def write(cls):
        cls.DWG.save()