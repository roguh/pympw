# master\_password.py: An Algorithm for Freedom

Master Password is a determnistic password generator.
This is a Python implementation of the Master Password algorithm based on 
[mpw-js](https://github.com/tmthrgd/mpw-js).

[masterpassword.app](masterpassword.app)

## Usage

```
> from master_password import site_password, master_key
```

See all template classes available 

```
> list(template_classes.keys())
['Maximum', 'Long', 'Medium', 'Short', 'Basic', 'PIN', 'Name', 'Phrase']
```

Generate a master key (>1sec)

```
> master_key = master_key(b'USER', b'PASSWORD')
```

Generate a password

```
> site_password(site_name='google.com', master_key=master_key, template_class='Long', counter=20000)
'Vode7.QojfDeqa'
```
