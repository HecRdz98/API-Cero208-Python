def get_database_params(array, params, name='param'):
    if(not array == []):
        placeholders = ", ".join([f":{name}{i}" for i in range(len(array))])
        _params = {f"{name}{i}": valor for i, valor in enumerate(array)}
        params.update(_params)
        return placeholders
    return '';

def get_filter_query(filters:dict, filter_type='OR', need_where=True, ):
    query = ""
    params = {}
    placeholders = []
    for key, value in filters.items():
        array = value
        if(isinstance(array, str)):
            array = value.split(",") if value else []

        if(array == [] or array == None):
            continue

        param_key = key.split('.')[-1]
        _placeholders = ", ".join([f":{param_key}{i}" for i in range(len(array))])
        _params = {f"{param_key}{i}": valor for i, valor in enumerate(array)}
        params.update(_params)
        placeholders.append(f"{key} IN ({_placeholders})")

    if placeholders:
        # query = "WHERE " + f" {filter_type} ".join(placeholders)
        query = ("WHERE " if need_where else "") + f" {filter_type} ".join(placeholders)

    return query, params
