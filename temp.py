from ast import literal_eval

with open("spaceX.json") as f:
    launches = literal_eval(f.read())

for launch in launches:
    name = launch.get("name")
    image_url = launch.get("links", {}).get("patch", {}).get("large")
    details = launch.get("details")
    article_link = launch.get("links", {}).get("article")
    reddit_link = launch.get("links", {}).get("reddit", {}).get("launch")
    wikipedia_link = launch.get("links", {}).get("wikipedia")
    date = launch.get("date_utc")
print(launch["success"])
print(launch["upcoming"])
print(launch["failed"])
