# Why Backhub?

If you use several computers/VMs you may want to quickly clone all your repos on your new machine. _(It may also be used if you plan to close your Github account...)_

# How to use?

The only dependency is Python3, then you just have to:

    $ chmod +x backhub.py
    $ ./backhub.py -d <dir>

Where **dir** is the directory in which you want to clone your repos. If you want there also some options:

    $ ./backhub.py -h
    usage: backhub.py [-h] [-u USER] [-p PASSWD]
                      [-t {all,owner,public,private,member}] [--https]
                      [-d DIRECTORY]
    
    Clone all your Github repos.
    
    optional arguments:
      -h, --help            show this help message and exit
      -u USER, --user USER
      -p PASSWD, --pass PASSWD
      -t {all,owner,public,private,member}, --type {all,owner,public,private,member}
                            Which type of repos needs to be cloned.
      --https               Clone via https (ssh by default).
      -d DIRECTORY, --directory DIRECTORY
                            In which directory the repos should be cloned (. by
                            default).

# Conclusion!

This _hasn't been_ extensively tested but it should work without problems (and it shouldn't break anything ;)). Use at your own risk!

