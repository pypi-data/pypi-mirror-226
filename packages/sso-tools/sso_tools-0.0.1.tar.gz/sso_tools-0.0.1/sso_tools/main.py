import base64
import hashlib
import os
import random
import string
from urllib.parse import urlencode, unquote

import requests

from schemas import Token


class OAuth2:
    """OAuth2 인증"""

    def __init__(
        self,
        client_id,
        client_secret,
        redirect_uri,
        server_host=None,
        version=None,
    ):
        # 클라이언트 정보
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.server_host = server_host or os.environ.get("MILLIE_SSO_HOST", "")
        self.version = version or "v1"
        # 코드 암호 정보
        self._code_verifier = None
        self._code_challenge = None

    @property
    def code_verifier(self):
        """랜덤 문자열 생성 후 base64로 인코딩"""
        if self._code_verifier:
            return self._code_verifier
        code_verifier = "".join(
            random.choice(string.ascii_uppercase + string.digits)
            for _ in range(random.randint(43, 128))
        )
        self._code_verifier = base64.urlsafe_b64encode(code_verifier.encode("utf-8"))
        return self._code_verifier

    @property
    def code_challenge(self):
        """code_verifier를 sha256으로 해싱한 후 base64로 인코딩"""
        if self._code_challenge:
            return self._code_challenge
        code_verifier = self.code_verifier
        code_challenge = hashlib.sha256(code_verifier).digest()
        self._code_challenge = (
            base64.urlsafe_b64encode(code_challenge).decode("utf-8").replace("=", "")
        )
        return self._code_challenge

    def get_authorization_url(self, scope="read"):
        """인증 URL"""
        params = {
            "client_id": self.client_id,
            "response_type": "code",
            "redirect_uri": self.redirect_uri,
            "code_challenge_method": "S256",
            "code_challenge": self.code_challenge,
            "scope": scope,
            "state": self.code_verifier,
        }
        url = f"{self.server_host}/{self.version}/oauth2/authorize/?{urlencode(params)}"
        return url

    def get_token(self, code, state):
        """토큰 발급"""
        url = f"{self.server_host}/{self.version}/oauth2/token/"
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "authorization_code",
            "code": unquote(code),
            "redirect_uri": self.redirect_uri,
            "code_verifier": unquote(state),
        }
        resp = requests.post(
            url,
            data=data,
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "Cache-Control": "no-cache",
            },
        )
        resp.raise_for_status()
        return Token(**resp.json())
