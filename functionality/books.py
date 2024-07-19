class BookObject():
    def __init__(self, title, publishdate, subtitle, publisher, authors, thumbnail, description, id):
        self.title = title
        self.publishdate = publishdate
        self.subtitle = subtitle
        self.publisher = publisher
        self.authors = authors
        self.thumbnail = thumbnail
        self.description = description
        self.id = id
        
class RBook():
    def __init__(self, title, publishdate, subtitle, publisher, authors, thumbnail, description, id, rating, start_date, end_date):
        self.title = title
        self.publishdate = publishdate
        self.subtitle = subtitle
        self.publisher = publisher
        self.authors = authors
        self.thumbnail = thumbnail
        self.description = description
        self.id = id
        self.rating = rating
        self.start_date = start_date
        self.end_date = end_date