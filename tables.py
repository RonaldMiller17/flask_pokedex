from flask_table import Table, Col

# table keys for results table
class Results(Table):
    id = Col('id', show = False)
    name = Col('Name')
    pokemon_type = Col('Type')
    capture_rate = Col('Capture Rate (%)')
    shape = Col('Shape')