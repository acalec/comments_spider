class Comment(object):
    def __repr__(self):
        class_name = self.__class__.__name__
        properties = (u'{} = ({})'.format(k, v) for k, v in self.__dict__.items())
        r = u'\n<{}:\n  {}\n>'.format(class_name, u'\n  '.join(properties))
        return r

    def __init__(self):
        self.content = ''
        self.created_at = ''
        self.commentUser = ''

