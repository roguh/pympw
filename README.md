# master\_password.py: An Algorithm for Freedom

Master Password is a determnistic password generator.
This is a Python implementation of the Master Password algorithm v3 based on 
[mpw-js](https://github.com/tmthrgd/mpw-js).

I faithfully implemented the [algorithm](http://www.masterpasswordapp.com/masterpassword-algorithm.pdf) for a cool password manager in a few dozen lines of Python. Please note **this code is for demonstration purposes only.** If you want to use a reliable deterministic password manager, get one at [masterpassword.app](http://masterpassword.app).

## CLI Usage

### Options 

```
$ ./cli.py -h
usage: cli.py [-h] [--name NAME] [--site SITE] [--counter COUNTER]
              [--type {maximum,x,long,l,medium,m,basic,b,short,s,longbasic,lb,pin,#,name,n,phrase,ph}]
              [--copy] [--hide-pw] [--splitby SPLITBY]
              [--exit-after EXIT_AFTER] [--exit-command EXIT_COMMAND]
              [--keepalive] [--quiet]

CLI to Master Password algorithm v3. Passwords are generated locally, your
master password is not sent to any server. http://masterpassword.app

optional arguments:
  -h, --help            show this help message and exit
  --name NAME, -n NAME  your full name
  --site SITE, -s SITE  site name (e.g. linux.org). omit this argument to
                        start an interactive session.
  --counter COUNTER, -c COUNTER
                        positive integer less than 2**31=4294967296
  --type {maximum,x,long,l,medium,m,basic,b,short,s,longbasic,lb,pin,#,name,n,phrase,ph}
                        password type
  --copy, -y            copy password to clipboard instead of printing it
  --hide-pw, -d         never print passwords
  --splitby SPLITBY, -b SPLITBY
                        more efficient interactive session. suggested values:
                        tab, space, or '/'
  --exit-after EXIT_AFTER, -e EXIT_AFTER
                        script will timeout and close after this many seconds
  --exit-command EXIT_COMMAND
                        run this command if the script times out
  --keepalive, -k       keep program from timing out by pressing ENTER
  --quiet, -q           less output
```

### Examples

Generate a password with a single command

```
$ python3 cli.py -n USER --type long -s google.com -c 20000
please type your master password >
site=google.com, type=long, counter=20000
Vode7.QojfDeqa
```

Enter interactive mode by omitting the `--site` argument. Type `CTRL-D` or `quit` to quit.

```
 $ ./cli.py -n USER
please type your master password >
please type site name > google.com
please type counter or ENTER for default=1 > 20000
please type type or ENTER for default=long >
Vode7.QojfDeqa
please type site name > quit
bye
```

Enter alternative interactive mode

```
 $ python3 cli.py -n USER -b/
please type your master password >
please type site name[/type[/counter]] > google.com
Kasi2/FipsHonm
please type site name[/type[/counter]] > google.com/pin
7002
please type site name[/type[/counter]] > google.com/medium/3
Wap4/Voy
please type site name[/type[/counter]] > google.com/x
i%&yc(sRV7VJqOQK%G0~
please type site name[/type[/counter]] > quit
bye
```

Use `--copy` to copy password to clipboard.

```
$ ./cli.py -n USER --copy --type x
please type your master password >
please type site name > github.com
please type counter or ENTER for default=1 >
please type type or ENTER for default=x >
password copied to clipboard
```

Use `--exit-after` to shutdown interactive mode after some number of seconds.
Use `--quiet` to print less output.
Use `--keepalive` to reschedule timeout if you're still using the program.

```
$ ./cli.py --name USER --type maximum --quiet --copy --splitby / \
    --keepalive --exit-after "$((60 * 5))" \
    --exit-command 'notify-send "MasterPassword is now closed"'
master password >
site name[/type[/counter]] > google.com/l/20000
Vode7.QojfDeqa
site name[/type[/counter]] > google.com
i%&yc(sRV7VJqOQK%G0~
site name[/type[/counter]] > 300 second timeout reached
bye
```

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
