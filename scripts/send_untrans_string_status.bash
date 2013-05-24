#!/bin/bash

cd `dirname $0`
cd ..
source ~/.bashrc
python manage.py send_untrans_string_status &> ~/logs/user/send_untrans_string_status.log