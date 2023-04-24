from flask_table import Table, Col, LinkCol


class Results(Table):
    id = Col('Id', show=False)
    name = Col('Name')
    description = Col('Description')
    release_date = Col('Release Date')
    #compatibility = Col('Compatibility')
    price = Col('Price')
    company = Col('Company')
    edit = LinkCol('Edit', 'edit', url_kwargs=dict(id='id'))
