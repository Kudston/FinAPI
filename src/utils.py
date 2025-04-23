import enum 


class OrderDirection(enum.Enum):
    ASC = 'asc'
    desc = 'desc'

class OrderBy(enum.Enum):
    date_created = 'date_created'
    date_modified = 'date_modified'
    