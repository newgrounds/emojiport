""" This script bulk uploads emoji to a slack channel """
import os, sys, time, argparse, getpass
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

parser = argparse.ArgumentParser()
parser.add_argument("slackteamname")
parser.add_argument("email")
parser.add_argument("emojipath")
parser.add_argument("--password")
parser.add_argument("-v", "--verbose", action="store_true")
parser.add_argument("-s", "--show", action="store_true")
args = parser.parse_args()

rootdir = args.emojipath
if not rootdir.endswith('/'):
    rootdir = rootdir + '/'

username = args.email
password = args.password
if not password:
    password = getpass.getpass()

slack_url = "https://" + args.slackteamname + ".slack.com/customize/emoji"

if args.show:
    driver = webdriver.Chrome()
else:
    driver = webdriver.PhantomJS()

try:
    driver.set_window_size(800, 600)
    driver.get(slack_url)
    login_input = driver.find_element_by_name("email")
    login_input.send_keys(username)
    pwd_input = driver.find_element_by_name("password")
    time.sleep(1)
    pwd_input.send_keys(password)
    pwd_input.send_keys(Keys.RETURN)

    count = 0
    for subdir, dirs, files in os.walk(rootdir):
        for f in files:
            count += 1
            if args.verbose:
                print count
            if count > 0:  # Change this value if this program crashes and you need to start from the middle
                splitname = f.split('.')
                lowername = splitname[0].lower()
                if lowername == '':
                    if args.verbose:
                        print "ignoring " + f
                    continue
                if args.verbose:
                    print f + " : " + lowername

                emojiname = driver.find_element_by_id("emojiname")
                emojiname.clear()
                emojiname.send_keys(lowername)
                emojiimg = driver.find_element_by_id("emojiimg")
                emojiimg.clear()
                emojiimg.send_keys(rootdir + f)
                time.sleep(0.5)

                emojiname.send_keys(Keys.RETURN)
except:
    e = sys.exec_info()[0]
    print e
driver.close()
driver.quit()
