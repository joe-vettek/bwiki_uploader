import os
import json
import base64
import sqlite3
import shutil
from datetime import datetime, timedelta
import win32crypt  # pip install pypiwin32
from Crypto.Cipher import AES  # pip install pycryptodome

from wiki import LogHelper


def get_chrome_datetime(chromedate):
    """Return a `datetime.datetime` object from a chrome format datetime
    Since `chromedate` is formatted as the number of microseconds since January, 1601"""
    if chromedate != 86400000000 and chromedate:
        try:
            return datetime(1601, 1, 1) + timedelta(microseconds=chromedate)
        except Exception as e:
            LogHelper.printLog(f"Error: {e}, chromedate: {chromedate}")
            return chromedate
    else:
        return ""


def get_encryption_key():
    # local_state_path = os.path.join(os.environ["USERPROFILE"],
    #                                 "AppData", "Local", "Google", "Chrome",
    #                                 "User Data", "Local State")
    local_state_path = os.path.join(os.environ["USERPROFILE"],
                                    "AppData", "Local", "Microsoft", "Edge",
                                    "User Data", "Local State")
    # LogHelper.printLog(local_state_path)
    with open(local_state_path, "r", encoding="utf-8") as f:
        local_state = f.read()
        local_state = json.loads(local_state)

    # decode the encryption key from Base64
    key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
    # remove 'DPAPI' str
    key = key[5:]
    # return decrypted key that was originally encrypted
    # using a session key derived from current user's logon credentials
    # doc: http://timgolden.me.uk/pywin32-docs/win32crypt.html
    return win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]


def decrypt_data(data, key):
    try:
        # get the initialization vector
        iv = data[3:15]
        data = data[15:]
        # generate cipher
        cipher = AES.new(key, AES.MODE_GCM, iv)
        # decrypt password
        return cipher.decrypt(data)[:-16].decode()
    except:
        try:
            return str(win32crypt.CryptUnprotectData(data, None, None, None, 0)[1])
        except:
            # not supported
            return ""


def main():
    # local sqlite Chrome cookie database path
    # db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local",
    #                        "Google", "Chrome", "User Data", "Default", "Network", "Cookies")
    db_path = os.path.join(os.environ["USERPROFILE"],
                           "AppData", "Local", "Microsoft", "Edge",
                           "User Data", "Default", "Network", "Cookies")
    if not os.path.exists(db_path):
        db_path = os.path.join(os.environ["USERPROFILE"],
                               "AppData", "Local", "Microsoft", "Edge",
                               "User Data", "Profile 2", "Network", "Cookies")
    # copy the file to current directory
    # as the database will be locked if chrome is currently open
    filename = "Cookies.db"
    if not os.path.isfile(filename):
        # copy file when does not exist in the current directory
        shutil.copyfile(db_path, filename)
    # connect to the database
    db = sqlite3.connect(filename)
    # ignore decoding errors
    db.text_factory = lambda b: b.decode(errors="ignore")
    cursor = db.cursor()
    # get the cookies from `cookies` table
    cursor.execute("""
    SELECT host_key, name, value, creation_utc, last_access_utc, expires_utc, encrypted_value, path 
    FROM cookies""")
    # you can also search by domain, e.g thepythoncode.com
    # cursor.execute("""
    # SELECT host_key, name, value, creation_utc, last_access_utc, expires_utc, encrypted_value
    # FROM cookies
    # WHERE host_key like '%thepythoncode.com%'""")
    # get the AES key
    key = get_encryption_key()
    aaaa = ""
    for host_key, name, value, creation_utc, last_access_utc, expires_utc, encrypted_value, path in cursor.fetchall():
        if not value:
            decrypted_value = decrypt_data(encrypted_value, key)
        else:
            # already decrypted
            decrypted_value = value
        # if (path=="/fsdmn/" and host_key=="wiki.biligame.com") or host_key==".biligame.com":
        #     aaaa+=f"{name}={decrypted_value};"
        if host_key == ".biligame.com" and name == "SESSDATA":
            aaaa += f"{decrypted_value}"
        # if 1>0:
        #     LogHelper.printLog(f"""
        # Host: {host_key}
        # Cookie Path: {path}
        # Cookie name: {name}
        # Cookie value (decrypted): {decrypted_value}
        # Creation datetime (UTC): {get_chrome_datetime(creation_utc)}
        # Last access datetime (UTC): {get_chrome_datetime(last_access_utc)}
        # Expires datetime (UTC): {get_chrome_datetime(expires_utc)}
        # ===============================================================""")
        # # update the cookies table with the decrypted value
        # # and make session cookie persistent
        # cursor.execute("""
        # UPDATE cookies SET value = ?, has_expires = 1, expires_utc = 99999999999999999, is_persistent = 1, is_secure = 0
        # WHERE host_key = ?
        # AND name = ?""", (decrypted_value, host_key, name))
    # LogHelper.printLog(aaaa)
    # with open("wiki/Cookie", "w", encoding="utf-8") as f:
    #     f.write(aaaa)
    #     f.close
    # commit changes
    db.commit()
    # close connection
    db.close()
    os.remove(filename)
    return aaaa


if __name__ == "__main__":
    main()
