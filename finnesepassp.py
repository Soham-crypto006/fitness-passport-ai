import requests
from bs4 import BeautifulSoup
import json



def download_faqs(url):
   api_url = "https://fitnesspassport.my.site.com/faq/s/sfsites/aura"

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
               }
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
               }
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

   payload = {
       "message": json.dumps(message),
       "aura.context": json.dumps(context),
       "aura.pageURI": "/faq/s/topic/0TOOl0000002i9sOAA/membership-management",
       "aura.token": "null"
   }

   response = requests.post(api_url, params=params, data=payload)
   response.raise_for_status()

   data = response.json()

   # Find the requested FAQ in the returned articles
   target_name = url.rstrip("/").split("/")[-1]

   try:
       articles = data["actions"][1]["returnValue"]["articles"]
   except (KeyError, IndexError, TypeError):
       print("Could not find FAQ data in the API response.")
       return None

   for item in articles:
       article = item.get("article", {})

       if article.get("urlName", "").lower() == target_name.lower():
           return {
               "question": article.get("title", ""),
               "answer": article.get("summary", ""),
               "source": url
           }

   print(f"Failed to fetch content for {url}")
   return None
