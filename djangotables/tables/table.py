from djangotables.tables.fields.field import TableField

"""

"""

class Table:
    
    __table         = ''    # generates the html table to print out
    """
        Meta class, with aditional meta data
            Attributes         Detail
        - tr_head_attrs => Atrribules for tr on table head
        - order         => List of fields name to order the table columns
        - query_set     => Default query_set to use on table
    """
    __meta          = None  # meta class with meta data
    __fields        = {}    # All fields to represent on table
    __query_set     = None  # Query set with the data to display

    def __init__(self, query_set=None):
        
        # query_set data
        if query_set:
            self.__query_set = query_set

        # getting just the subclass attributes
        attrs = set(dir(self.__class__)) - set(dir(Table))

        # preparing the table fields
        for attr in attrs:
            # getting the attribute memory reference
            evalued_attr = eval('self.__class__.'+attr)
            # saves if it's not a callable attribute and is an instance of global table field
            if not callable( evalued_attr ) and isinstance( evalued_attr, TableField ):
                self.__fields[attr] = evalued_attr

        # instantiating the Meta class, if exists
        if 'Meta' in attrs:

            # instantiating
            self.__meta = self.__class__.Meta()

            # setting default query_set
            if hasattr( self.__meta, 'query_set' ) and self.__query_set is None:
                self.__query_set = self.__meta.query_set

            # sorting and preparing the fields
            if hasattr( self.__meta, 'order' ):

                #
                orded = {}

                # sorting the fields
                for name in self.__meta.order:
                    for field in self.__fields:
                        # catch de field if have the same name
                        if name == field:
                            orded[name] = self.__fields[name]
                            del(self.__fields[name])
                            break
                    # Breaking the cycle if all fields are already sorted and listed
                    if not self.__fields:
                        break
                
                # setting orded fields
                self.__fields = orded
        
        # constructing the table header
        self.__create_table_head()

    """ Create the table head """

    def __create_table_head(self):
        
        if self.__fields:
            # passing the tr head attributes
            tr = '<tr>' if not hasattr( self.__meta, 'tr_head_attrs' ) else f'<tr{self.join_html_attrs(self.__meta.attrs)}>'
            # adding th
            for name, field in self.__fields.items():
                tr += '<th'+field.joined_th_attrs+'>'+field.label+'</th>'
            # adding the row in the table
            self.__table += tr + '</tr>'
    
    """ Join html attrs """

    def join_html_attrs(self, attrs):
        text = ''
        if attrs and isinstance(attrs, dict):
            for attr, value in attrs.items():
                text += f' {attr}="{value}"'
        return text
    
    """ table display """

    def __repr__(self):
        return self.__table