from html.parser import HTMLParser

class FormParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.form_fields = {}
        self.form_action = None

    def handle_starttag(self, tag, attrs):
        if tag == 'form':
            for name, value in attrs:
                if name == 'action':
                    self.form_action = value
        elif tag == 'input':
            field_name = None
            field_value = None
            for name, value in attrs:
                if name == 'name':
                    field_name = value
                elif name == 'value':
                    field_value = value
            if field_name:
                self.form_fields[field_name] = field_value