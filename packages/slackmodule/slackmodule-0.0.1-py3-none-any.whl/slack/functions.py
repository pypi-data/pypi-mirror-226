from slack_sdk import WebClient


def extract_slack_id_name(token: str, channel_name: str):

    """
    Extract the slack_id and full_name of all users from the #lifescience Slack channel.
    :return: dictionary, slack_id & full_name
    """
    client = WebClient(token=token)
    users = client.conversations_members(channel=channel_name)
    users = users["members"]
    users_store = {"slack_id": [], "full_name": []}

    for user in users:
        # Store relevant parts of user object
        users_store["slack_id"].append(client.users_info(user=user)["user"]["id"])
        users_store["full_name"].append(client.users_info(user=user)["user"]["profile"]["real_name"])

    return users_store
