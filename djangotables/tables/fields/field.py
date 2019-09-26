
"""
    Base Table Fields
"""
class TableField:

    value       = None # Value for all lines if != None
    th_attrs    = {}   # table header, attributes on this column, Ex: { "class": "th-active th-black"}
    td_attrs    = {}   # table data, attributes on this column
    label       = ''   # Name for table header, if none, will use the name of field
    default     = ''   # Default value to use if self.value is empty and not None
    _filter     = None # Data filter for this table column

    def __init__(self, label='', default='', value=None, th_attrs={}, td_attrs={}, _filter=None):

        # get the label name
        self.label    = label 
        # default value if empty
        self.default  = default
        # unic value for all lines
        self.value    = value 
        # header attrs
        self.th_attrs = th_attrs if isinstance( th_attrs, dict ) else {}
        # dat attrs
        self.td_attrs = td_attrs if isinstance( td_attrs, dict ) else {}
        # filter
        self._filter  = _filter 

    """ Join all th html attributes """
    
    @property
    def joined_th_attrs(self):
        
        # joined th attributes
        joined_th_attrs = ''

        if isinstance( self.th_attrs, dict ):
            for attr, value in self.th_attrs.items():
                joined_th_attrs += f' {attr}="{value}"'

        return joined_th_attrs

    """ Join all td html attributes """
    
    @property
    def joined_td_attrs(self):

        # joined td attributes
        joined_td_attrs = ''

        if isinstance( self.td_attrs, dict ):
            for attr, value in self.td_attrs.items():
                joined_td_attrs += f' {attr}="{value}"'

        return joined_td_attrs

"""
    TextField, for varchar field, like django forms.TextField
"""

class TextField(TableField):

    def __repr__(self):
        return f"<TableField: {self.label}>"
