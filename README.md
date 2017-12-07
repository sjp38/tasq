# tasq
Receive user job requests inside queue and dequeue / process the jobs.
Aims to be used for batched sequential tasks processing. Maybe useful
for aggressive time sharing homework test environment.

# PATH Setting
`tasq` server executes received command using `su -p <username>`.  So, the
execution will use `ENV_PATH` in `/etc/login.defs` as its `PATH`.  Never forget
to modify `/etc/login.defs` file if you want to allow binaries in another
paths.

# Usage
Run `tasq_server.py` alone with super user permission first and
execute `tasq` with next usage.

`$ tasq <enq | list> [command] [output]`

## Example
```
$ tasq enq nvcc --output-file matmul matmul.cu output
$ tasq enq ./matmul output2
$ tasq list
```

# License
GPL v3

# Author
SeongJae Park (sj38.park@gmail.com)
