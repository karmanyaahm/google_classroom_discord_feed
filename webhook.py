import requests
from stringcase import titlecase

def send(to,title, desc, status, workType, points=0, url=None):
    workType = titlecase(workType.lower())
    status = titlecase(status.lower())
    
    embed = {
        "color": 3447003,
        "title": status + " - " + workType + " " + title,
        "description": workType
        + " details: "
        + ((desc[:75] + "..") if len(desc) > 75 else desc),
        "fields": [
            {
                "name": "Points",
                "value": points,
            },
        ],
    }
    if url:
        embed["url"] = url

    data = {
        "embeds": [embed],
        "username": "Google Classroom Bot",
        "avatar_url": "https://lh3.googleusercontent.com/jdcCuHVB2NoCEdDqj1fNV05G8MC3TyBX6jY93v_Sba2ViqrVXIW-efKjVk3BR-41VhwV8gD0x0EHmlXK2UqvCCQLDTqOs2N1AXjppA=w1440-v1",
    }

    print(requests.post(to, json=data).text)

def send(to,c):    
    data = {
        "content": c,
        "username": "Google Classroom Bot",
        "avatar_url": "https://lh3.googleusercontent.com/jdcCuHVB2NoCEdDqj1fNV05G8MC3TyBX6jY93v_Sba2ViqrVXIW-efKjVk3BR-41VhwV8gD0x0EHmlXK2UqvCCQLDTqOs2N1AXjppA=w1440-v1",
    }

    print(requests.post(to, json=data).text)

def received_stuff(to, data_object, status):
    d = data_object

    send(to = to,
        title=d["title"],
        desc=d["description"],
        status=status,
        points=int(d["maxPoints"]),
        workType=d["workType"],
        url=d["alternateLink"],
    )