from nameparser import HumanName


def get_read_only_fields(fields, writeable_fields):
    writeable_set = set(writeable_fields)
    read_only_fields = ()
    for field in fields:
        if field not in writeable_set:
            read_only_fields += (field,)
    return read_only_fields


def get_first_and_last_name_from_full_name(full_name):
    try:
        human_name = HumanName(full_name)
        first_name = " ".join(
            human_name.title_list + human_name.first_list + human_name.middle_list
        )
        last_name = " ".join(human_name.last_list)
        return first_name, last_name
    except Exception as exc:
        return full_name, ""
