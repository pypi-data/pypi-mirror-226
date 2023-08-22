from utils.logger import LOGGER

from classes.Text import Text
from classes.ETAttrMarker import ETAttrMarker

class ETAttr(Text):
    
    def __init__(self, x=0, y=0, text='', id=False, mandatory=True, deprecated=False):
        
        self.__id = id 
        self.__mandatory = mandatory
        self.__deprecated = deprecated
        
        self._styleClass = 'attrname'
        
        if(not self.__mandatory):
            self._styleClass += ' ' + 'optattrname'
        if(self.__deprecated):
            self._styleClass += ' ' + 'deprecatedattrname'      
        if(self.__id):
            self._styleClass += ' ' + 'idattrname'      
            
        self.__idMarker        = None 
        self.__mandatoryMarker = None
        self.__optionalMarker  = None
        self.__markerSpace = 0
        
        super().__init__(x, y, text, styleClass = self._styleClass)
        
        self.__buildMarker()
        
    
    def __buildMarker(self):
        
        _size = self.getHeight() * 0.5
        _x = self._x
        _y = self._y        
        
        if(self.__id):
            self.__idMarker = ETAttrMarker(_x + _size * 0.20, _y + _size / 2, _size, markerType='id')
            _x += _size * 1.1
        else:
            _x += _size * 0.6

        if(self.__mandatory):
            self.__mandatoryMarker = ETAttrMarker(_x + _size * 0.20, _y + _size / 2, _size, markerType='mandatory')
        else:
            self.__optionalMarker = ETAttrMarker(_x + _size * 0.20, _y + _size / 2, _size, markerType='optional')
            
        self.__markerSpace = self.getHeight() * 1.3
            
        super().update(x = self._x + (self.__markerSpace))   # Makes space for mandatory/optional marker

        
    def getWidth(self):
        return self.__markerSpace + self._getSize()['width']
        
        
    def update(self, x=None, y=None, text=None, styleClass=None):
        super().update(x, y, text, styleClass)
        if(x is not None or y is not None) :
            self.__buildMarker()
        
        
    def add(self, group):
        super().add(group)
        if(self.__idMarker is not None):
            self.__idMarker.add(group)
        if(self.__mandatoryMarker is not None):
            self.__mandatoryMarker.add(group)
        if(self.__optionalMarker is not None):
            self.__optionalMarker.add(group)