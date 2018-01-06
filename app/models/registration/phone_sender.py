# -*- coding: utf-8 -*-
# Module 'phone_sender' of the project 'tingerwork'
# :date_create: 11.12.2017.4:21
# :author: Tingerlink
# :description:

import json
import requests
import config.settings
import tools.logger as logger


class PhoneSender:
    def __init__(self):
        self.password = config.settings.CALLING_PASS
        self.login = config.settings.CALLING_LOGIN

    def sms(self, phone, msg):
        pass

    def call(self, phone):
        uri = "http://smsc.ru/sys/send.php?login=%s&psw=%s&phones=%s&mes=code&call=1&fmt=3" %\
              (self.login, self.password, phone)

        response = json.loads(requests.get(uri).content.decode('utf-8'))

        return response, self.check_response(response)
        #return {"code": "123456"}, True

    def check_response(self, response):
        if "error" in response.keys():
            if response["error_code"] == 1:
                logger.log(3.1, "Ошибка в параметрах", "send_verification_code")
            elif response["error_code"] == 2:
                logger.log(3.2, "Неверный логин или пароль", "send_verification_code")
            elif response["error_code"] == 2:
                logger.log(3.3, "Недостаточно средств на счете Клиента", "send_verification_code")
            elif response["error_code"] == 2:
                logger.log(3.4, "IP-адрес временно заблокирован из-за частых ошибок в запросах.", "send_verification_code")
            elif response["error_code"] == 2:
                logger.log(3.5, "Неверный формат даты", "send_verification_code")
            elif response["error_code"] == 2:
                logger.log(3.6, "Сообщение запрещено (по тексту или по имени отправителя)", "send_verification_code")
            elif response["error_code"] == 2:
                logger.log(3.7, "Неверный формат номера телефона", "send_verification_code")
            elif response["error_code"] == 2:
                logger.log(3.8, "Сообщение на указанный номер не может быть доставлено", "send_verification_code")
                return False
            elif response["error_code"] == 2:
                logger.log(3.9, "Отправка более одного одинакового запроса на передачу "
                                "SMS-сообщения либо более пяти одинаковых запросов на получение "
                                "стоимости сообщения в течение минуты", "send_verification_code")
            return None

        return True
