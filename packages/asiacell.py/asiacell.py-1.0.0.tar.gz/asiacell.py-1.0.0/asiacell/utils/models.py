class Response:
	def __init__(self, data):
		self.json = data
		self.message = data.get("message")
		self.success = data.get("success")


class BalTransferSent:
    def __init__(self, data):
        self.type = data.get("type")
        self.msisdn = data.get("msisdn")
        self.receiverMsisdn = data.get("receiverMsisdn")
        self.createdAt = data.get("createdAt")
        self.amount = data.get("amount")


class BalTransferSentResponse:
    def __init__(self, data):
        self.json = data
        self.data = [BalTransferSent(d) for d in data.get("data")]
        self.response = Response(data)


class Captcha:
	def __init__(self, data):
		self.json = data
		self.response = Response(data)
		self.requier_captcha = data.get("requier_captcha")
		self.message = data.get("message")
		self.success = data.get("success")
		self.captcha = data.get("captcha")


class WithNexAction:
	def __init__(self, data):
		self.json = data
		self.response = Response(data)
		self.nextAction = data.get("nextAction")
		self.title = data.get("title")


class AccountOverview:
	def __init__(self, data):
		self.json = data
		self.response = Response(data)
		self.profile = Profile(data.get("bodies")[0].get("items")[0])
		self.shortcuts = [Shortcut(s) for s in data.get("bodies")[1].get("items")]
		self.balance = Balance(data.get("bodies")[2].get("items")[0])
		self.remaining_data = GiftBox(data.get("bodies")[3])
		self.remaining_call = GiftBox(data.get("bodies")[4])
		self.remaining_sms = GiftBox(data.get("bodies")[5])


class Profile:
	def __init__(self, data):
		self.json = data
		self.response = Response(data)
		self.name = data.get("name")
		self.phone_number = data.get("phoneNumber")
		self.photo = data.get("photo")


class Shortcut:
	def __init__(self, data):
		self.json = data
		self.response = Response(data)
		self.id = data.get("id")
		self.icon = data.get("icon")
		self.title = data.get("title")
		self.lang = data.get("lang")
		self.action = data.get("action")


class Balance:
	def __init__(self, data):
		self.json = data
		self.response = Response(data)
		self.value = data.get("value")
		self.action_button = ActionButton(data.get("actionButton"))


class ActionButton:
	def __init__(self, data):
		self.json = data
		self.response = Response(data)
		self.action = data.get("action")
		self.title = data.get("title")


class GiftBox:
	def __init__(self, data):
		self.json = data
		self.response = Response(data)
		self.icon = data.get("icon")
		self.tag = data.get("tag")
		self.inverted = data.get("inverted")
		self.title = data.get("title")
		self.items = [GiftBoxItem(i) for i in data.get("items")]


class GiftBoxItem:
	def __init__(self, data):
		self.json = data
		self.response = Response(data)
		self.title = data.get("title")
		self.action = Action(data.get("action")) if data.get("action") != None else None


class Action:
	def __init__(self, data):
		self.json = data
		self.title = data.get("title")
		self.action = data.get("action")


class Confirmation:
    def __init__(self, data):
        self.access_token = data.get("access_token")
        self.handshake_token = data.get("handshake_token")
        self.language = data.get("language")
        self.refresh_token = data.get("refresh_token")
        self.requiredCaptcha = data.get("requiredCaptcha")
        self.userId = data.get("userId")
        self.userType = data.get("userType")
        self.username = data.get("username")

class Account:
    def __init__(self, data):
        self.last_name = data.get("lastName")
        self.first_name = data.get("firstName")
        self.middle_name = data.get("thirdName")
        self.email = data.get("email")
        self.phone_number = data.get("phone")
        self.photo_url = data.get("photo")


class Recharge:
	def __init__(self, data):
		self.msisdn = data.get('msisdn')
		self.createdAt = data.get('createdAt')
		self.amount = data.get("amount")
	
class RechargeHistory:
	def __init__(self, data):
		self.json = data
		self.response = Response(data)
		self.recharges = [Recharge(d) for d in data['data']]
		
class Bundle:
    def __init__(self, bundle_name, activation_at, amount):
        self.bundle_name = bundle_name
        self.activation_at = activation_at
        self.amount = amount

class BundleData:
	def __init__(self, data):
		self.json = data
		self.response = Response(data)
		self.bundles = [
			Bundle(
				d.get('bundleName'), 
				d.get('activationAt'), 
				d.get('amount')
			) for d in data.get("data", [])
		]

class SpinWheelStatus:
	def __init__(self, data):
		self.json = data
		self._remainingTime = data.get("data", {}).get("remainingTime", {})
		self.response = Response(data)
		self.isPlayable = self._remainingTime.get("isPlayable")
		self.selectedIndex = self._remainingTime.get("selectedIndex")
		self.luckyId = self._remainingTime.get("luckyId")
		self.dayIndex = self._remainingTime.get("dayIndex")
		self.remainingTime = RemainingTime(
			self._remainingTime.get("hours"),
			self._remainingTime.get("minutes"),
			self._remainingTime.get("second"),
			self._remainingTime.get("timestamp")
		)

class RemainingTime:
	def __init__(self, hours, mintues, seconds, timestamp):
		self.hours = hours
		self.minutes = mintues
		self.seconds = seconds
		self.timestamp = timestamp
		