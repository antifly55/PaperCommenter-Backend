import configparser

properties = configparser.ConfigParser()
properties.read('config.ini')

def get_config_variable(category: str, field: str):

    properties_category = properties[category]

    return properties_category[field]

def get_config_variables(category: str, fields: list):

    properties_category = properties[category]

    variables = []
    for field in fields:
        value = properties_category[field]
        variables.append(value)
    
    return variables