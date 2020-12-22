#!/bin/bash
#:set ts=4 sw=4

SLEEPSECS=4
BINDIR=/usr/local/bin
LOGFILE=/var/log/sshmonitor.log   # Where to place the normal logfile (disabled if blank)
#SYSLOG=local0              # Which syslog facility to use (disabled if blank)
PRIORITY=0
MACHINE=`hostname`
SUDO='/usr/bin/sudo'
PYTHON='/usr/bin/python'
EXECUTABLE="${BINDIR}/sshmonitor.py"

# Please change the username and password! I will not forward the e-mails to you.
args="-esshmonitorapp@gmail.com -phkeyscwhgxjzafvj --verbose"

message() {
    echo "$1" >&2
    if test "x$SYSLOG" != "x" ; then
        logger -p "${SYSLOG}.warn" -t sshmonitor.py[$$] "$1"
    fi
    if test "x$LOGFILE" != "x" ; then
        echo "sshmonitor.py[$$]: $1" >> "$LOGFILE"
    fi
}


run_sshmonitord() {
    while :; do

        cd $BINDIR
	`$SUDO $PYTHON ${EXECUTABLE} ${args}`;
        EXITSTATUS=$?
	message "sshmonitor.py ended with exit status $EXITSTATUS"
        if test "x$EXITSTATUS" = "x0" ; then
            # Properly shutdown....
            message "sshmonitor.py shutdown normally."
            exit 0
        else
            if test "x${email}" != "x" ; then
                message "sshmonitor.py on $MACHINE died with exit status $EXITSTATUS.  Might want to take a peek."
                #mail -s "sshmonitor.py Died" $email
                message "Exited on signal $EXITSTATUS"
            fi
        fi
		message "Automatically restarting sshmonitor.py."
		sleep $SLEEPSECS
	done
}

run_sshmonitord &
