""" This script bulk downloads emoji from a slack channel """
import os, time, urllib, argparse, getpass
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

parser = argparse.ArgumentParser()
parser.add_argument("slackteamname")
parser.add_argument("email")
parser.add_argument("--password")
parser.add_argument("--emojiname")
parser.add_argument("-v", "--verbose", action="store_true")
args = parser.parse_args()

email = args.email
password = args.password
slackurl = "https://" + args.slackteamname + ".slack.com/customize/emoji"

if not password:
    password = getpass.getpass()

#driver = webdriver.Chrome()
driver = webdriver.PhantomJS()
driver.get(slackurl)
login_input = driver.find_element_by_name("email")
login_input.send_keys(email)
pwd_input = driver.find_element_by_name("password")
time.sleep(1)
pwd_input.send_keys(password)
pwd_input.send_keys(Keys.RETURN)

emojispans = driver.find_elements_by_class_name("emoji-wrapper")
if not os.path.exists("slack_emoji"):
    os.makedirs("slack_emoji")

for emoji in emojispans:
    emoji_url = emoji.get_attribute("data-original")
    split_emoji = emoji_url.split("/")
    emoji_name = split_emoji[4]
    file_ext = os.path.splitext(split_emoji[5])[1]
    
    # this handles specifying a single emoji to download
    if args.emojiname and args.emojiname == emoji_name:
        if args.verbose:
            print emoji_name + " : " + emoji_url
            #print emoji_url
            #print file_ext
        urllib.urlretrieve(emoji_url, "slack_emoji/"+emoji_name+file_ext)
driver.close()
driver.quit()