# -*- coding: utf-8 -*-
"""
Created on 2022-07-05 18:03:02
Modified on 2022-07-04 16:36:32
Purpose: JSON Web Token auth for Tornado
"""

import datetime
import jwt

jwt_options = {
    'verify_signature': True,
    'verify_exp': True,
    'verify_nbf': False,
    'verify_iat': True,
    'verify_aud': True,
    'verify_iss': False
}

class JWTDecorator:
    '''
    装饰器：JWT

    参考链接: https://github.com/paulorodriguesxv/tornado-json-web-token-jwt/blob/master/auth.py
    '''

    def __init__(self, auth_method='bearer', secret_key='my_secret_key', audience=None, 
                 algorithms=['HS256']):
        """
        初始化JWTDecorator类。

        :param auth_method: 验证方法，默认为 bearer
        :param secret_key: 密钥，如果没有指定，则使用默认密钥 "my_secret_key"
        :param audience: 颁发令牌的受众
        :param algorithms: 使用的算法，默认为 HS256
        """
        self.secret_key = secret_key
        self.audience = audience
        self.auth_method = auth_method
        self.algorithms = algorithms

    def is_valid_header(self, parts):
        """
        检查头部是否有效。

        :param parts: 头部的各个部分
        :return: 如果有效则返回True，否则False
        """
        if not parts or len(parts) != 2:
            return False
        elif parts[0].lower() != self.auth_method:
            return False

        return True

    def return_auth_error(self, handler, message):
        """
        返回授权错误。

        :param handler: RequestHandler对象
        :param message: 错误消息
        """
        handler._transforms = []
        handler.set_status(401)
        handler.set_header('WWW-Authenticate', 'Basic realm=Restricted')
        handler.finish(message)

    def require_auth(self, auth_header, kwargs):
        auth = auth_header.request.headers.get('Authorization', None)
        if not auth:
            msg = {'message': 'Parameter error!', 'reason': 'Missing authorization'}
            auth_header._transforms = []
            auth_header.finish(msg)
            return
        
        parts = auth.split()
        if not self.is_valid_header(parts):
            msg = {'message': 'validation error', 'reason': 'invalid header authorization'}
            self.return_auth_error(auth_header, msg)
            return
        
        token = parts[1]
        try:
            if self.audience and jwt_options['verify_aud']:
                decoded = jwt.decode(
                    token,
                    audience=self.audience,
                    algorithms=self.algorithms,
                    options=jwt_options
                )
            else:
                decoded = jwt.decode(
                    token,
                    self.secret_key,
                    algorithms=self.algorithms,
                    options=jwt_options
                )
                # 检查令牌是否过期
                exp_timestamp = decoded.get('exp')
                now_timestamp = datetime.datetime.utcnow().timestamp()
                if now_timestamp > exp_timestamp:
                    raise jwt.ExpiredSignatureError('Token expired')
        except (jwt.ExpiredSignatureError, jwt.DecodeError, jwt.InvalidAudienceError) as err:
            msg = {'message': 'Token is invalid', 'reason': '%s' % str(err)}
            self.return_auth_error(auth_header, msg)
            return

    def jwtauth(self, handler_class):
        """
        Tornado JWT Auth 装饰器。

        :param handler_class: RequestHandler类
        :return: 装饰后的 RequestHandler 对象
        """
        execute_orig = handler_class._execute
        
        def _execute(self, transforms, *args, **kwargs):
            try:
                self.require_auth(self, kwargs)
            except Exception as err:
                print(err)
                return False

            return execute_orig(self, transforms, *args, **kwargs)

        handler_class._execute = _execute
        return handler_class


class JWT:
    def __init__(self, secret_key:str='my_secret_key'):
        """
        初始化JWT类。

        :param secret_key: 密钥，如果没有指定，则使用默认密钥 "my_secret_key"
        """
        self.secret_key = secret_key

    def jwt_encode(self, payload, algorithm='HS256', exp_seconds=60):
        """
        生成 JWT token。

        :param payload: 要编码的数据
        :param algorithm: 编码算法，默认为 HS256
        :param exp_seconds: token 过期时间（秒）
        :return: 包含 JWT token 的字典对象
        """
        now_timestamp = datetime.datetime.utcnow().timestamp()
        exp_timestamp = now_timestamp + exp_seconds

        payload.update({
            'exp': exp_timestamp,
            'iat': now_timestamp,
        })

        encoded = jwt.encode(
            payload,
            self.secret_key,
            algorithm=algorithm
        )
        return {'token': encoded.decode()}

    def jwt_decode(self, jwt_token, audience=None, algorithms=['HS256']):
        """
        解码 JWT token。

        :param jwt_token: 要解码的 token
        :param audience: 颁发令牌的受众
        :param algorithms: 解码算法，默认为 HS256
        :return: tuple，第一个元素指示 token 是否有效，第二个元素是包含结果的字典对象
        """
        try:
            if audience and jwt_options['verify_aud']:
                decoded = jwt.decode(
                    jwt_token,
                    self.secret_key,
                    audience=audience,
                    algorithms=algorithms,
                    options=jwt_options
                )
            else:
                decoded = jwt.decode(
                    jwt_token,
                    self.secret_key,
                    algorithms=algorithms,
                    options=jwt_options
                )
                # 检查令牌是否过期
                exp_timestamp = decoded.get('exp')
                now_timestamp = datetime.datetime.utcnow().timestamp()
                if now_timestamp > exp_timestamp:
                    raise jwt.ExpiredSignatureError('Token expired')

            return True, {'message': 'Token is valid!', 'data': decoded}
        except (jwt.ExpiredSignatureError, jwt.DecodeError, jwt.InvalidAudienceError) as err:
            return False, {'message': 'Token is invalid!', 'reason': '%s' % str(err)}
