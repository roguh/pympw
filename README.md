# master\_password.py: An Algorithm for Freedom

Master Password is a determnistic password generator.
This is a Python implementation of the Master Password algorithm v3 based on 
[mpw-js](https://github.com/tmthrgd/mpw-js).

This code is for demonstration purposes only. 
If you want to use a reliable password manager (that can be implemented in a few lines of Python),
go to [masterpassword.app](http://masterpassword.app).

## Usage

```
> from master_password import site_password, master_key
```

See all template classes available 

```
> template_classes.keys()
dict_keys(['Maximum', 'Long', 'Medium', 'Short', 'Basic', 'PIN', 'Name', 'Phrase'])
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
