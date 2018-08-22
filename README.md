# master\_password.py: An Algorithm for Freedom

Master Password is a determnistic password generator.
This is a Python implementation of the Master Password algorithm v3 based on 
[mpw-js](https://github.com/tmthrgd/mpw-js).

**This code is for demonstration purposes only.** I faithfully implemented the algorithm for a favorite password manager in a few dozen lines of Python! If you want to use a reliable deterministic password manager, get one at [masterpassword.app](http://masterpassword.app).

## CLI Usage
```
usage: cli.py [-h] [--name NAME] [--site SITE] [--counter COUNTER]
              [--type {maximum,long,medium,short,basic,longbasic,pin,name,phrase,x,l,m,s,b,lb,#,n,ph}]
              [--copy] [--splitby SPLITBY] [--exit-after EXIT_AFTER]

optional arguments:
  -h, --help            show this help message and exit
  --name NAME, -n NAME  your full name
  --site SITE, -s SITE  site name (e.g. linux.org). omit this argument to
                        start an interactive session.
  --counter COUNTER, -c COUNTER
                        positive integer less than 2**31=TODO
  --type {maximum,long,medium,short,basic,longbasic,pin,name,phrase,x,l,m,s,b,lb,#,n,ph}
                        password type
  --copy, -y            copy password to clipboard instead of printing it
  --splitby SPLITBY, -b SPLITBY
                        more efficient interactive session. suggested values:
                        tab, space, or '/'
  --exit-after EXIT_AFTER, -e EXIT_AFTER
                        close script after this many seconds
```

Generate a password with a single command

```
$ python3 cli.py -n USER --type long -s google.com -c 20000
please type your master password >
site=google.com, type=long, counter=20000
Vode7.QojfDeqa
```

Enter interactive mode. Type `CTRL-D` or `quit` to quit.

```
 $ python3 cli.py -n USER
please type your master password >
please type site name > google.com
please type counteror ENTER for default=1 > 20000
please type typeor ENTER for default=Long > long
Vode7.QojfDeqa
please type site name > quit
bye
```

Enter alternative interactive mode

```
 $ python3 cli.py -n USER -b/
please type your master password >
please type site name[/type[/counter]] > google.com/l/20000
Vode7.QojfDeqa
please type site name[/type[/counter]] >
```

Use `--copy` to copy password to clipboard.
Use `--exit-after` to shutdown interactive mode after some number of seconds.

## Library Usage

```
> from master_password import site_password, master_key, template_classes
```

See all template classes available 

```
> template_classes.keys()
dict_keys(['maximum', 'long', 'medium', 'short', 'basic', 'pin', 'name', 'phrase'])
```

Generate a master key (>1sec)

```
> master_key = master_key(b'USER', b'PASSWORD')
```

Generate a password

```
> site_password(site_name='google.com', master_key=master_key, template_class='long', counter=20000)
'Vode7.QojfDeqa'
```
