def validate(data):
    errors = {}
    if data.get('title', '') == '':
        errors['title'] = 'Данное поле обязательное'
    elif len(data.get('title','')) < 3:
        errors['title'] = 'Название статьи должно быть длиннее 3 символов'

    if data.get('author', '') == '':
        errors['author'] = 'Данное поле обязательное'

    if data.get('content', '') == '':
        errors['content'] = 'Данное поле обязательное'

    return errors