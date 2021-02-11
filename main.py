import os
import re
import sys
import argparse
import time

from ldif3 import LDIFParser

from email_helper import send_os_mail
from dateutil import parser as datetime_parser
from datetime import datetime, timezone

MASTER_MAIL = "yaswanthkumar.pamarthi@cms.hhs.gov"
THRESHLOLD_DAYS = 2


def is_system_account_password(value) -> bool:
    return (
        True
        if value and re.search(r"System Account Password Policy", value[0])
        else False
    )


def is_120_days_expire_password(value) -> bool:
    return True if value and re.search(r"120days", value[0]) else False


def send_mail(record, days_diff: int, dn) -> str:
    password_changed_time = record.get("pwdchangedtime", None)
    if not password_changed_time:
        return "password changed time not available"
    time = password_changed_time[0].split(".")[0]
    password_changed_time = datetime_parser.parse(
        time + "Z" if "Z" not in time else time
    )
    now = datetime.now(timezone.utc)
    if (now - password_changed_time).days > days_diff - THRESHLOLD_DAYS:
        for mail in record.get("mail"):
            send_os_mail(
                receiver_email=mail,
                subject="Email Reset Notification | UID: %s"
                % dn.split(",")[0].split("=")[1],
            )
        return "Successfully Send email"
    return "Not needed"


def parse_and_send_email(record, dn) -> str:
    password_policy_sub_entry_type = record.get("pwdPolicySubentry")
    if is_system_account_password(password_policy_sub_entry_type):
        return "SYSTEM PASSWORD (No email sent)"
    elif is_120_days_expire_password(password_policy_sub_entry_type):
        return send_mail(record, 120, dn)
    else:
        return send_mail(record, 60, dn)


def read_file_and_send_email(parser):
    sent_list, error = [], []
    for dn, entry in parser.parse():
        try:
            if not entry.get("mail"):
                pass
            message = parse_and_send_email(record=entry, dn=dn)
            sent_list.append({",".join(entry.get("mail")): message})
            # time.sleep(10)
        except Exception as e:
            error.append(e)

    send_os_mail(MASTER_MAIL, data=sent_list, subject="Report")
    # time.sleep(10)
    if error:
        send_os_mail(MASTER_MAIL, data=error, subject="Failed To Send Email")


def create_arg_parser():
    parser = argparse.ArgumentParser(description="Description of send mail script")
    parser.add_argument(
        "-inputDirectory", "-fp", help="Path to the ldif file directory."
    )

    return parser


if __name__ == "__main__":
    arg_parser = create_arg_parser()
    parsed_args = arg_parser.parse_args(sys.argv[1:])
    if os.path.exists(parsed_args.inputDirectory):
        parser = LDIFParser(open(parsed_args.inputDirectory, "rb"))
        read_file_and_send_email(parser=parser)
