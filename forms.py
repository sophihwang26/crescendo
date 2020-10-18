from wtforms import Form, StringField, SelectField

class MusicSearchForm(Form):
    choices = [('Artist', 'Artist')]
    select = SelectField('Search for music:', choices=choices)
    search = StringField('')