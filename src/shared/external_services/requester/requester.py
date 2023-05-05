import requests
import urllib3


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Requester:
    def __init__(self):
        self.session = requests.Session()

    @staticmethod
    def is_error_status_code(status_code: int):
        if status_code < 200 or status_code >= 400:
            return True
        return False

    def get(self, url, headers=None, params=None, allow_redirects=True, proxies=None, timeout=10, cookies=None):
        return self.session.get(
            url, headers=headers, params=params, verify=False, timeout=timeout, allow_redirects=allow_redirects,
            proxies=proxies, cookies=cookies
        )
        # if allow_redirects:
        #     redirect_url = meta_redirection(tmp)
        #     if redirect_url is not None:
        #         return self.session.get(redirect_url, headers=headers, verify=False, timeout=timeout,
        #                                 allow_redirects=allow_redirects,
        #                                 proxies=proxies)

    def post(self, url, data=None, headers=None, allow_redirects=True, proxies=None, json=None, timeout=10,
             files=None, cookies=None):
        return self.session.post(
            url, headers=headers, verify=False, data=data, json=json, timeout=timeout,
            allow_redirects=allow_redirects, proxies=proxies, files=files, cookies=cookies
        )

    def put(self, url, data=None, headers=None, allow_redirects=True, proxies=None, json=None, timeout=10,
            files=None, cookies=None):
        return self.session.put(
            url, headers=headers, verify=False, data=data, json=json, timeout=timeout,
            allow_redirects=allow_redirects, proxies=proxies, files=files, cookies=cookies
        )

    def delete(self, url, data=None, headers=None, allow_redirects=True, proxies=None, json=None, timeout=10,
               files=None, cookies=None):
        return self.session.delete(
            url, headers=headers, verify=False, data=data, json=json, timeout=timeout,
            allow_redirects=allow_redirects, proxies=proxies, files=files, cookies=cookies
        )

    def head(self, url, headers=None, allow_redirects=True, proxies=None, timeout=10):
        return self.session.head(
            url, headers=headers, verify=False, timeout=timeout,
            allow_redirects=allow_redirects, proxies=proxies
        )
