import csv
import requests

# Function to get user details and post details.
def getuserDetails(userlink):
    username = userlink.split("/")[-1]
    url = f"https://gab.com/api/v1/account_by_username/{username}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"
    }
    user_data = requests.get(url, headers=headers)

    user_details = user_data.json()

    user_id = user_details["id"]
    username = user_details["username"]
    date_joined = user_details["created_at"]
    image_url = user_details["avatar"]
    cover_image_url = user_details["header"]
    about = user_details["note"]
    gabss = user_details["statuses_count"]
    followers = user_details["followers_count"]
    following = user_details["following_count"]

    needed_user_details = {
        "userId": user_id,
        "username": username,
        "date_joined": date_joined,
        "image_url": image_url,
        "cover_image_url": cover_image_url,
        "about": about,
        "gabss": gabss,
        "followers": followers,
        "following": following,
    }

    posts_url = f"https://gab.com/api/v1/accounts/{user_id}/statuses?sort_by=newest"
    posts_data = requests.get(posts_url, headers=headers)
    user_posts_details = posts_data.json()
    needed_post_details = []
    for i in range(len(user_posts_details)):
        post_id = i + 1
        favourites_count = user_posts_details[i]["favourites_count"]
        quotes_count = user_posts_details[i]["quotes_count"]
        reblogs_count = user_posts_details[i]["reblogs_count"]
        replies_count = user_posts_details[i]["replies_count"]
        needed_post_details.append(
            {
                "post_id": post_id,
                "favourites_count": favourites_count,
                "quotes_count": quotes_count,
                "reblogs_count": reblogs_count,
                "replies_count": replies_count,
            }
        )

    all_details = [needed_user_details, needed_post_details]
    return all_details


def write_csv(all_details):
    username = all_details[0]["username"]
    with open(f"./scraped_user_data/{username}.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "userId",
                "username",
                "date_joined",
                "image_url",
                "cover_image_url",
                "about",
                "gabss",
                "followers",
                "following",
            ]
        )
        writer.writerow(
            [
                all_details[0]["userId"],
                all_details[0]["username"],
                all_details[0]["date_joined"],
                all_details[0]["image_url"],
                all_details[0]["cover_image_url"],
                all_details[0]["about"],
                all_details[0]["gabss"],
                all_details[0]["followers"],
                all_details[0]["following"],
            ]
        )
        writer.writerow(
            [
                "post_id",
                "favourites_count",
                "quotes_count",
                "reblogs_count",
                "replies_count",
            ]
        )
        for i in all_details[1]:
            writer.writerow(
                [
                    i["post_id"],
                    i["favourites_count"],
                    i["quotes_count"],
                    i["reblogs_count"],
                    i["replies_count"],
                ]
            )


def get_details_and_write_csv(userlink):
    all_details = getuserDetails(userlink)
    write_csv(all_details)
    print("Done")


# Calling the function for one user.

get_details_and_write_csv("https://gab.com/worth__fighting__for")


# Calling the function for 10 users.
ten_users = [
    "https://gab.com/worth__fighting__for",
    "https://gab.com/ScottPresler",
    "https://gab.com/ShootyMcBeardface",
    "https://gab.com/RealMikeLindell",
    "https://gab.com/a",
    "https://gab.com/warrenvmyers",
    "https://gab.com/ILoveAmericaNews",
    "https://gab.com/realdonaldtrump",
    "https://gab.com/USCenturion",
    "https://gab.com/MorpheusMAGA",
]

for user in ten_users:
    get_details_and_write_csv(user)
