

class Captcha:
	def __init__(self, data):
		self.requier_captcha = data.get("requier_captcha")
		self.message = data.get("message")
		self.success = data.get("success")
		self.captcha = data.get("captcha")

# class 