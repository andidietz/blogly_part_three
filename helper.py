def query_all(cls):
    return cls.query.all()

def query_by_id(cls, id):
    return cls.query.get_or_404(id)