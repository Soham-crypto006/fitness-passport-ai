
import requests
import json

url = "https://fitnesspassport.my.site.com/faq/s/sfsites/aura"

params = {
    "r": "61",
    "ui-communities-components-aura-components-forceCommunity-controller.Headline.getInitData": "1",
    "ui-self-service-components-controller.TopicArticleListDataProvider.loadArticlePage": "1"
}

message = {
    "actions": [
        {
            "id": "907;a",
            "descriptor": "serviceComponent://ui.communities.components.aura.components.forceCommunity.controller.HeadlineController/ACTION$getInitData",
            "callingDescriptor": "UNKNOWN",
            "params": {
                "uniqueNameOrId": "0TOOl0000002i9sOAA",
                "pageType": "topic"
            },
            "version": "68.0",
            "storable": True
        },
        {
            "id": "968;a",
            "descriptor": "serviceComponent://ui.self.service.components.controller.TopicArticleListDataProviderController/ACTION$loadArticlePage",
            "callingDescriptor": "UNKNOWN",
            "params": {
                "pageSize": 10,
                "topicIds": "0TOOl0000002i9sOAA",
                "knowledgeCursor": "",
                "ekCursor": ""
            },
            "version": "68.0",
            "storable": True
        }
    ]
}

context = {
    "mode": "PROD",
    "fwuid": "ZVYtV2g3NHN0UGNVNzBMbldfZ0ZwZ2tVMjdnTGFERUU2S3FfSVdrcU92bkExNS4zLjE2MDEw",
    "app": "siteforce:communityApp",
    "loaded": {
        "APPLICATION@markup://siteforce:communityApp": "1897_Qx6CsUG7r803A_23Hon_1g",
        "COMPONENT@markup://force:outputField": "1620_J6hzM0AKHzkt78HO7XJeZw"
    },
    "dn": [],
    "globals": {
        "density": "VIEW_ONE"
    },
    "uad": True
}

data = {
    "message": json.dumps(message),
    "aura.context": json.dumps(context),
    "aura.pageURI": "/faq/s/topic/0TOOl0000002i9sOAA/membership-management",
    "aura.token": "null"
}

headers = {
    "Origin": "https://fitnesspassport.my.site.com",
    "Referer": "https://fitnesspassport.my.site.com/faq/s/topic/0TOOl0000002i9sOAA/membership-management",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Accept": "*/*"
}


def fetch_faqs():
    print("Fetching FAQs...")

    response = requests.post(
        url,
        params=params,
        data=data,
        headers=headers,
        timeout=30
    )

    print("Status:", response.status_code)
    response.raise_for_status()

    result = response.json()
    all_faqs = []

    for action in result.get("actions", []):
        return_value = action.get("returnValue") or {}
        articles = return_value.get("articles", [])

        for item in articles:
            article = item.get("article", {})

            title = article.get("title")
            summary = article.get("summary")
            url_name = article.get("urlName")

            if not title:
                continue

            all_faqs.append({
                "question": title,
                "answer": summary or "",
                "source": (
                    "https://fitnesspassport.my.site.com/faq/s/article/"
                    + url_name
                ) if url_name else ""
            })

    # Remove duplicate articles by source URL
    unique_faqs = []
    seen_sources = set()

    for faq in all_faqs:
        source = faq["source"]

        if source and source in seen_sources:
            continue

        if source:
            seen_sources.add(source)

        unique_faqs.append(faq)

    with open("faqs.json", "w", encoding="utf-8") as f:
        json.dump(
            unique_faqs,
            f,
            indent=4,
            ensure_ascii=False
        )

    print(f"Saved {len(unique_faqs)} FAQs to faqs.json")


if __name__ == "__main__":
    try:
        fetch_faqs()
    except requests.RequestException as e:
        print("Request failed:", e)
    except ValueError as e:
        print("Could not parse the API response:", e)
