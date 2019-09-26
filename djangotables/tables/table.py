from djangotables.tables.fields.field import TableField

""" """

class DajngoTablesException(Exception):
    pass

"""

"""

class Table:
    
    __table         = ''    # generates the html table to print out
    """
        Meta class, with aditional meta data
            Attributes         Detail
        - name          => Table name to differentiate from others
        - order         => List of fields name to order the table columns
        - count         => a instance of tables.TextField ou tables.IntegerField for counting lines
        - query_set     => Default query_set for use on table
        - tr_head_attrs => Atrribules for tr on table head
        - tr_body_attrs => Atrribules for tr on table body
    """
    __meta          = None  # meta class with meta data
    __fields        = {}    # All fields to represent on table
    __query_set     = None  # Query set with the data to display
    __name          = 'djt'    # Table name to differentiate from others

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

            # setting the table name
            if hasattr( self.__meta, 'name' ):
                self.__name = self.__meta.name

            # count
            if hasattr( self.__meta, 'count' ):
                if isinstance( self.__meta.count, TableField ):
                    orded['__count'] = self.__meta.count

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

                # adding the remaining fields
                orded.update(self.__fields)
                # setting orded fields
                self.__fields = orded

        if self.__fields:
            # constructing the table header
            self.__create_table_head()
            # listing the data
            self.__list_table_data()

    """ Create the table head """

    def __create_table_head(self):

        # passing the tr head attributes
        tr = '<tr>' if not hasattr( self.__meta, 'tr_head_attrs' ) else f'<tr{self.join_html_attrs(self.__meta.tr_head_attrs)}>'
        # adding th
        for name, field in self.__fields.items():
            tr += '<th'+field.joined_th_attrs+'>'+field.label+'</th>'
        # adding the row in the table
        self.__table += tr + '</tr>'

    """ list the data """

    def __list_table_data(self):

        # verifying the queryset data
        if self.__query_set is None:
            raise DajngoTablesException('QuerySet is None, make sure you set the queryset data on class constructor or on Meta class data')  

        # lines count
        count = 1 if '__count' in self.__fields.keys() else False

        # creating table line with td columns data
        for item in self.__query_set:

            # setting the item id on line
            tr = f'<tr id="{self.__name}-{item.pk}"'

            # passing the tr head attributes
            tr += f'{self.join_html_attrs(self.__meta.tr_body_attrs)}>' if hasattr( self.__meta, 'tr_body_attrs' ) else '>'

            # lines count
            if count:
                # adding
                tr += f'<td{self.__meta.count.joined_td_attrs}>{count}</td>'
            
            # adding items
            for name, field in self.__fields.items():
                
                # continue if count
                if name == '__count':
                    continue

                td = f'<td name="{name}"{field.joined_td_attrs}>'

                # verifying if has a unique value
                if field.value is not None:
                    
                    # verifying if is a callable method
                    if callable( field.value ):
                        # passing the attribute if it is a function
                        # for something like: lambda user: user.last_name.upper()
                        tr += td + f'{field.value(item)}</td>' 
                    else:
                        tr += td + f'{field.value}</td>'

                    continue

                # Checking if have the attribute name in the item
                if hasattr( item, name ):
                    # getting item data by attribute name
                    evalued_item_data = eval('item.'+name)
                    # verifying if empty or null
                    if evalued_item_data:
                        tr += td + f"{evalued_item_data}</td>"
                    else: 
                        # using default if item is empty or null
                        tr += td + f"{field.default}</td>"
                else:
                    tr += td + f"{field.default}</td>"

            # count
            count += 1 if count else False
            # adding the tr line on table
            self.__table += tr + '</tr>'
    
    # ========================================================================================================================
    
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