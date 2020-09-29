#!/bin/sh

clear
mysql -h {{ dbhostname }} -u insecure {{ wpdbname }} < /home/lab-user/cat_meme_takeover.sql > /dev/null 2>&1

if [ $? = 0 ]; then
	echo
	echo
	echo '      HACKED!!!  YOU ARE A BAD KITTY!'
	echo
	echo '      ##############################'
	echo '       __  __ _____ _____        __ '
	echo '      |  \/  | ____/ _ \ \      / / '
	echo '      | |\/| |  _|| | | \ \ /\ / /  '
	echo '      | |  | | |__| |_| |\ V  V /   '
	echo '      |_|  |_|_____\___/  \_/\_/    '
	echo '   	       	       	       	  '
	echo '      ##############################'
	echo '                                    '
	echo '      DONE!  Now reload the web page'
	echo '         http://{{ webhostname }}    '
	echo ' to see what the evil cat hacker clan did!'
	echo
	echo
else
	echo
	echo
	echo '        FAILED!  You do not can haz   '
	echo '        permissionz to the database   '
	echo
	echo '       ############################## '
        echo '       ____      ___        ______  _ '
        echo '      |  _ \    / \ \      / /  _ \| |'
        echo '      | |_) |  / _ \ \ /\ / /| |_) | |'
        echo '      |  _ <  / ___ \ V  V / |  _ <|_|'
        echo '      |_| \_\/_/   \_\_/\_/  |_| \_(_)'
	echo '   	       	       	       	    '
	echo '       ############################## '
	echo '                                      '
	echo '        FAILED!  You do not can haz   '
	echo '        permissionz to the database   '
	echo
	echo
fi

