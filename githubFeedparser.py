#!/usr/local/bin/python3
# coding=utf-8

import feedparser
import requests
import os
import re
import hashlib

config_sdk = [
    {
        "rss_url":
        "https://github.com/facebook/facebook-objc-sdk/releases.atom",
        "tags_url": "https://github.com/facebook/facebook-objc-sdk/releases",
        "pod_file_name": u"- FBSDKCoreKit ",
        "sdk_name": "FacebookSDK",
        "tag_location_str":
        "/v"  # TAG LOCATION https://github.com/facebook/facebook-objc-sdk/releases/tag/v5.2.1
    },
    {
        "rss_url":
        "https://github.com/OneSignal/OneSignal-iOS-SDK/releases.atom",
        "tags_url": "https://github.com/OneSignal/OneSignal-iOS-SDK/releases",
        "pod_file_name": u"- OneSignal ",
        "sdk_name": "OneSignalSDK",
        "tag_location_str":
        "tag/"  # TAG LOCATION https://github.com/OneSignal/OneSignal-iOS-SDK/releases/tag/2.10.0
    },
    {
        "rss_url":
        "https://github.com/firebase/firebase-ios-sdk/releases.atom",
        "tags_url": "https://github.com/firebase/firebase-ios-sdk/releases",
        "pod_file_name": u"- Firebase/Core ",
        "sdk_name": "FirebaseSDK",
        "tag_location_str":
        "tag/"  # TAG LOCATION https://github.com/firebase/firebase-ios-sdk/releases/tag/6.4.0
    },
    {
        "rss_url":
        "https://github.com/AppsFlyerSDK/AppsFlyerFramework/releases.atom",
        "tags_url":
        "https://github.com/AppsFlyerSDK/AppsFlyerFramework/releases",
        "pod_file_name": u"- AppsFlyerFramework ",
        "sdk_name": "AppsFlyerSDK",
        "tag_location_str":
        "tag/"  # TAG LOCATION https://github.com/AppsFlyerSDK/AppsFlyerFramework/releases/tag/4.10.2
    }
]

config_git_url = {"XXI": YOUR_LOCAL_REPO_URL}
config_file_name = "Podfile.lock"
robot_message_content = None


# Get the local version number
def get_local_sdk_ver(md5_name, sdk_name):
    pod_ver_title = ""
    lock_path = str(md5_name) + '/' + config_file_name
    with open(lock_path) as f:
        file_lines = f.readlines()
        try:
            for line in file_lines:
                if sdk_name in line and "~" not in line and ">" not in line:
                    p1 = re.compile(r'[(](.*?)[)]',
                                    re.S)  # Remove special symbols
                    # print(re.findall(p1, line))
                    pod_ver_title = re.findall(p1, line)[0]
        finally:
            f.close()
    return pod_ver_title


# Get the latest version number via RSS
def get_remote_sdk_ver(sdk_url, tag_location_str):
    feeds = feedparser.parse(sdk_url)
    last_post = feeds.entries[0]
    last_ver_loc = last_post.link.find(tag_location_str) + len(
        tag_location_str)
    last_ver_len = len(last_post.link)
    last_ver_title = last_post.link[last_ver_loc:(last_ver_len)]
    return last_ver_title


# compare remote_sdk_ver to
def compare_sdk_name(remote_sdk_ver, local_sdk_ver, sdk_name, tags_url):
    if remote_sdk_ver not in local_sdk_ver:
        key = list(config_git_url.keys())[list(
            config_git_url.values()).index(url)]
        global robot_message_content

        if robot_message_content is None:
            robot_message_content = {}
        if robot_message_content.get(key) is None:
            robot_message_content[key] = {}
        if robot_message_content[key].get(sdk_name) is None:
            robot_message_content[key][sdk_name] = {}
        robot_message_content[key][sdk_name]["remote_ver"] = remote_sdk_ver
        robot_message_content[key][sdk_name]["local_ver"] = local_sdk_ver
        robot_message_content[key][sdk_name]["tags_url"] = tags_url


# get third-party configuration files from the repository
def get_Repo_Config(url):
    hl = hashlib.md5()
    hl.update(url.encode(encoding='utf-8'))
    dir_name = hl.hexdigest()
    if os.path.exists(dir_name):
        os.system('chmod -R 777 ' + dir_name + ' && cd ' + dir_name +
                  ' && git pull --depth=1 origin develop')
        for item in config_sdk:
            local_sdk_ver = get_local_sdk_ver(dir_name,
                                              str(item["pod_file_name"]))
            remote_sdk_ver = get_remote_sdk_ver(item["rss_url"],
                                                item["tag_location_str"])
            compare_sdk_name(remote_sdk_ver, local_sdk_ver, item["sdk_name"],
                             item["tags_url"])

    else:
        os.mkdir(dir_name)
        os.system('cd ' + dir_name + ' && git init')
        os.system('cd ' + dir_name + ' && git remote add -f origin ' + url)
        os.system('cd ' + dir_name + ' && git config core.sparsecheckout true')
        os.system('cd ' + dir_name + ' && touch .git/info/sparse-checkout')
        os.system('cd ' + dir_name + ' && echo ' + config_file_name +
                  '  >> .git/info/sparse-checkout')
        os.system('chmod -R 777 ' + dir_name + ' && cd ' + dir_name +
                  ' && git pull --depth=1 origin develop')
        for item in config_sdk:
            local_sdk_ver = get_local_sdk_ver(dir_name,
                                              str(item["pod_file_name"]))
            remote_sdk_ver = get_remote_sdk_ver(item["rss_url"],
                                                item["tag_location_str"])
            compare_sdk_name(remote_sdk_ver, local_sdk_ver, item["sdk_name"],
                             item["tags_url"])


for name, url in config_git_url.items():
    get_Repo_Config(url)

print(robot_message_content)
