import requests
from bs4 import BeautifulSoup
from py_partner_api.cache.data_cache import DataCache
from py_partner_api.models import OrderStatus, Service

class PartnerAPI:
    __token: str
    __url: str = "https://partner.soc-proof.su/api/v2"
    __services_url: str = "https://partner.soc-proof.su/services"
    __descriptions: dict = {}
    __cache: DataCache
    def __init__(self, token, cache: DataCache) -> str:
        self.__cache = cache
        self.__token = token
        self.load_descriptions()
    def get_service(self, service: str):
        services = self.load_services()
        for item in services:
            if item.service == service:
                return item
        return None
    def load_services(self):
        result: list[Service] = self.__cache.get("services", None)
        if not result:
            result = []
            response = requests.post(self.__url, data={
                "key": self.__token,
                "action": "services"
            })
            result = [Service(**{**service, **self.get_description_new(service['service'])}) for service in response.json()]
            self.__cache.set("services", result)
        return result
    def get_services_descriptions(self) -> dict:
        categories = self.__cache.get("descriptions", None)
        if not categories:
            response = requests.get(self.__services_url, headers={
                'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
            })
            soup = BeautifulSoup(response.text, "html.parser")
            table = soup.find('table', id='service-table')
            tbody = table.find('tbody')
            tr_list = tbody.find_all("tr")
            categories = {}
            for tr in tr_list:
                if tr.has_attr("data-filter-table-category-id"):
                    children = tr.findChildren("td" , recursive=False)
                    if len(children) == 7:
                        service_id = " ".join(children[0].text.split())
                        cost = " ".join(children[2].text.split())
                        min = " ".join(children[3].text.split())
                        max = " ".join(children[4].text.split())
                        time = " ".join(children[5].text.split())
                        description = " ".join(children[6].text.split())
                        categories[service_id] = {
                            "cost": cost,
                            "min": min,
                            "max": max,
                            "time": time,
                            "description": description,
                        }
            self.__cache.set("descriptions", categories, timeout=60*60*24)
        return categories
    def load_descriptions(self) -> None:
        self.__descriptions = self.__cache.get("descriptions", None)
        if not self.__descriptions:
            self.__descriptions = self.get_services_descriptions()
            self.__cache.set("description", self.__descriptions)
    def get_description(self, services_id: int):
        if services_id in self.__descriptions:
            return (self.__descriptions[services_id]["description"], self.__descriptions[services_id]["time"], )
        return None, None
    def get_description_new(self, services_id: int):
        if services_id in self.__descriptions:
            return {
                "description": self.__descriptions[services_id]["description"],
                "time": self.__descriptions[services_id]["time"],
            }
        return {
                "description": "",
                "time": "",
            }
    def add_order(self, service: str, link: str, quantity: str) -> int:
        response = requests.post(self.__url, data={
            "key": self.__token,
            "action": "add",
            "service": service,
            "link": link,
            "quantity": quantity,
        })
        res = response.json()
        if 'order' in res:
            return res['order']
        return None
    def get_status(self, orders: str or list):
        if isinstance(orders, list):
            orders = ",".join(orders)
        response = requests.post(self.__url, data={
            "key": self.__token,
            "action": "status",
            "orders": orders,
        })
        result: list[OrderStatus] = []
        json = response.json()
        for key, value in json.items():
            if "charge" in value and "status" in value:
                result.append(OrderStatus(key, value["charge"], value["status"], value["remains"]))
        return result
            