def get_id_data(queryset):
    data = list()

    for item in queryset.values():
        data.append(item['id'])

    return data
