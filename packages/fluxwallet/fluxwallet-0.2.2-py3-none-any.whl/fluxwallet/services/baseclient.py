# -*- coding: utf-8 -*-
#
#    fluxwallet - Python Cryptocurrency Library
#    Base Client
#    © 2016-2022 - 1200 Web Development <http://1200wd.com/>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import json
from urllib.parse import urlencode

import requests

from fluxwallet.keys import Address
from fluxwallet.main import *
from fluxwallet.networks import Network

_logger = logging.getLogger(__name__)


class ClientError(Exception):
    def __init__(self, msg=""):
        self.msg = msg
        _logger.info(msg)

    def __str__(self):
        return self.msg


class BaseClient(object):
    def __init__(
        self,
        network: str,
        provider: str,
        base_url: str,
        denominator: int,
        api_key: str = "",
        provider_coin_id: str = "",
        network_overrides=None,
        timeout=TIMEOUT_REQUESTS,
        latest_block=None,
        strict=True,
    ):
        try:
            self.network = network
            if not isinstance(network, Network):
                self.network = Network(network)
            self.provider = provider
            self.base_url = base_url
            self.resp = None
            self.units = denominator
            self.api_key = api_key
            self.provider_coin_id = provider_coin_id
            self.network_overrides = {}
            self.timeout = timeout
            self.latest_block = latest_block
            if network_overrides is not None:
                self.network_overrides = network_overrides
            self.strict = strict
        except Exception:
            raise ClientError("This Network is not supported by %s Client" % provider)

    def request(
        self,
        url_path: str,
        variables: dict = {},
        method: str = "get",
        secure: bool = True,
        post_data: str = "",
        base: str | None = None,
    ):
        url_vars = ""
        url = f"{self.base_url}{url_path}" if base is None else f"{base}{url_path}"

        if not url or not self.base_url:
            raise ClientError("No (complete) url provided: %s" % url)

        headers = {
            "User-Agent": f"fluxwallet/{FLUXWALLET_VERSION}",
            "Accept": "application/json",
            # 'Content-Type': 'application/json',
            # "Referrer": "https://www.github.com/1200wd/fluxwallet",
        }

        if method == "get":
            if variables:
                url_vars = "?" + urlencode(variables)
            url += url_vars
            log_url = url if "@" not in url else url.split("@")[1]
            _logger.info("Url get request %s" % log_url)
            self.resp = requests.get(
                url, timeout=self.timeout, verify=secure, headers=headers
            )
        elif method == "post":
            log_url = url if "@" not in url else url.split("@")[1]
            _logger.info("Url post request %s" % log_url)

            try:
                self.resp = requests.post(
                    url,
                    json=dict(variables),
                    data=post_data,
                    timeout=self.timeout,
                    verify=secure,
                    headers=headers,
                )
            except Exception as e:
                print("exception")
                print(repr(e))
                exit(0)
        resp_text = self.resp.text
        if len(resp_text) > 1000:
            resp_text = self.resp.text[:970] + "... truncated, length %d" % len(
                resp_text
            )
        _logger.debug("Response [%d] %s" % (self.resp.status_code, resp_text))
        log_url = url if "@" not in url else url.split("@")[1]
        if self.resp.status_code == 429:
            raise ClientError(
                "Maximum number of requests reached for %s with url %s, response [%d] %s"
                % (self.provider, log_url, self.resp.status_code, resp_text)
            )
        elif not (self.resp.status_code == 200 or self.resp.status_code == 201):
            raise ClientError(
                "Error connecting to %s on url %s, response [%d] %s"
                % (self.provider, log_url, self.resp.status_code, resp_text)
            )
        try:
            if not self.resp.apparent_encoding and not self.resp.encoding:
                return self.resp.content
            return json.loads(self.resp.text)
        except ValueError or json.decoder.JSONDecodeError:
            return self.resp.text

    def _address_convert(self, address):
        if not isinstance(address, Address):
            return Address.parse(
                address,
                network_overrides=self.network_overrides,
                network=self.network.name,
            )

    def _addresslist_convert(self, addresslist):
        addresslistconv = []
        for address in addresslist:
            addresslistconv.append(self._address_convert(address))
        return addresslistconv
