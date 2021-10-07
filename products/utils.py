def get_id_data(queryset):
    """
    Get all products id of a specific querySet
    """

    data = list()

    for item in queryset.values():
        data.append(item['id'])

    return data
