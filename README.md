tasq
====

Receive user job requests inside queue and dequeue / process the jobs.
Aims to be used for batched sequential tasks processing. Maybe useful
for aggressive time sharing homework test environment.


PATH Setting
============

`tasq` server executes the received commands using `su -p <requester username>`
to not make permission problem.  As man page says as below, the `-p` option
reset PATH according to the `ENV_PATH` in `/etc/login.defs` file.  __Never
forget__ to modify `/etc/login.defs` file if you want to allow binaries in
another paths.

```
-m, -p, --preserve-environment
   Preserve the current environment, except for:

   $PATH
       reset according to the /etc/login.defs options ENV_PATH or ENV_SUPATH
       (see below);

   $IFS
       reset to “<space><tab><newline>”, if it was set.

   If the target user has a restricted shell, this option has no effect (unless
   su is called by root).

   Note that the default behavior for the environment is the following:

       The $HOME, $SHELL, $USER, $LOGNAME, $PATH, and $IFS environment
       variables are reset.

       If --login is not used, the environment is copied, except for the
       variables above.

       If --login is used, the $TERM, $COLORTERM, $DISPLAY, and $XAUTHORITY
       environment variables are copied if they were set.

       Other environments might be set by PAM modules.
```


Usage
=====

Run `tasq_server.py` alone with super user permission first and
execute `tasq` with next usage.

`$ tasq <enq | list> [command] [output]`


Example
-------

```
$ tasq enq nvcc --output-file matmul matmul.cu output
$ tasq enq ./matmul output2
$ tasq list
```

License
=======

GPL v3


Author
======

SeongJae Park (sj38.park@gmail.com)
