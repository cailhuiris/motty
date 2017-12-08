<a href="https://scalalang2.github.io/motty/">
  <img src="https://scalalang2.github.io/motty/images/logo.png" width="75" height="75">
</a>

## Motty
Motty is very simple web application tool. It provides you simpler way to build mocking http server. 

- Why do we need an another code for mocking http server?
    - Motty doesn't need codes.
- Easy to use.
- Simple Installation.

It's very helpful to test your client services such as android, ios app, web and so on.<br>
Even though the server is not ready to link your services. You can keep your plan and continue to develop.

[Check more about motty!](https://scalalang2.github.io/motty/)

## Installation
You can easily install and run motty server by a few of commands. <br>
Python>=3.0 is required, so you should install python 3 before proceeding next step.


#### 1. Set up an isolated environment.
**You must not jump up this step** <br>
cause motty have permission issues, <br>
so it cannot access system library folders like /usr/bin. <br><br>
This is why motty have to be installed inside home directory. <br>
Afterward, if we can solve this issue, We'll keep you updated <br>

> $ pip3 install virtualenv <br>
> $ mkdir ~/mottyenv <br>
> $ virtualenv ~/mottyenv <br> 
> $ source ~/mottyenv/bin/activate <br>

#### 2. Install motty.
> $ pip install motty


#### 3. Run it! and play fun.
> $ runmotty


## Options
#### Run server on specific port.
> $ runmotty --port 7000

## License

DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
Version 2, December 2004

Copyright (C) 2004 Sam Hocevar <sam@hocevar.net>

Everyone is permitted to copy and distribute verbatim or modified
copies of this license document, and changing it is allowed as long
as the name is changed.

DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION

0. You just DO WHAT THE FUCK YOU WANT TO.
