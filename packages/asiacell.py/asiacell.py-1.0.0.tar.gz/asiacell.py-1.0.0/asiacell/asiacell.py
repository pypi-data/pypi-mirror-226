from .utils import Client
from .utils.exceptions import handle_exception
from .utils.models import Captcha, AccountOverview, WithNexAction, BalTransferSentResponse, Confirmation, Account, \
    RechargeHistory, BundleData, SpinWheelStatus
from .utils.helpers import ocr_solver


class Asiacell(Client):
    def __init__(self, phone_number: str, language: str = "en", ocr_api_key: str = None,
                 auto_refresh_token: bool = False):
        Client.__init__(self, auto_refresh_token)
        self.phone_number = phone_number
        self.username = phone_number
        self.set_language(language)
        self.captcha_code = ""

    def login(self) -> str:
        """
        Login to asiacell phone number ( sending otp to phone number )

        Note: u must use verify_login(pid, code) to confirm the login

          :return: PID of the transfer
        """
        sent_code = self.auth_post("/api/v1/login", {"captchaCode": self.captcha_code, "username": self.phone_number})
        pid = sent_code["nextUrl"].split("&PID=")[1]
        return pid

    def login_tokens(self, access_token, refresh_token) -> None:
        """
        Login to asiacell using the tokens

        :param access_token: access token
        :param refresh_token: refresh token

        :return: True if login is successful
        """
        self.access_token = access_token
        self.refresh_token = refresh_token

    def verify_login(self, pid: str, code: int) -> Confirmation:
        """
        Verify the login with the given code.

        :param pid: pid of login process
        :param code: otp code sended to the phone number

          :return: Confirmation
          """
        data = self.auth_post("/api/v1/smsvalidation", {"PID": pid, "passcode": code})
        self.auth(data)
        return Confirmation(data)

    def get_captcha(self) -> Captcha:
        return self.get("/api/v1/captcha")

    def solve_captcha(self, captcha: str | Captcha) -> bool:
        if type(captcha) not in [str, Captcha]:
            handle_exception(f"Captcha cannot be {type(captcha)}")
            return False

        if isinstance(captcha, Captcha):
            if captcha.get("captcha") is None:
                return True

            try:
                captcha_link = captcha["captcha"]["originSource"] + captcha["captcha"]["resourceUrl"]
            except KeyError:
                return True
            try:
                self.captcha_code = ocr_solver(captcha_link, self.ocr_api_key)
                return True
            except Exception as e:
                handle_exception(e)

    def transfer_money(self, amount: float, target_number: str) -> str:
        """
          Starting a transfer from the phone number to the target number

        Note: u must verifiy the transfer by calling verify_transfer(pid, code)  
  
          :param amount: The amount of credits to transfer
          :param target_number: The target phone number
    
          :return: PID of the transfer (used to verify the transfer)
          """""
        send_code = self.post("/api/v1/credit-transfer/start", {"amount": amount, "receiverMsisdn": target_number})
        return send_code["PID"]

    def verify_transfer(self, pid: str, code: str) -> WithNexAction:
        """
        Verifies a credit transfer

        :param pid: The PID of the transfer
        :param code: The otp code that have been sent to the phone number

          :return: WithNexAction
          """
        data = self.post("/api/v1/credit-transfer/do-transfer", {"PID": pid, "passcode": code})
        return WithNexAction(data)

    def get_account_data(self) -> AccountOverview:
        """
          Gets all account data

         :return: AccountOverview
          """
        data = self.get("/api/v1/profile")
        return AccountOverview(data["data"])

    def play_spinwheel(self) -> WithNexAction:
        """
          Plays The SpinWheel, run every 24 hours

         :return: WithNexAction
        """
        data = self.post("/api/v1/spinwheel/confirm", data={})
        return WithNexAction(data)

    def get_spinwheel_status(self) -> SpinWheelStatus:
        """
          Gets the spinwheel status, remining time until the next spinwheel

          :return: SpinWheelStatus
          """
        data = self.get("/api/v1/spinwheel/")
        return SpinWheelStatus(data)

    def get_transactions_history(self) -> BalTransferSentResponse:
        """
          Gets last transaction history

          NOTE : The api is in beta from the server and its not used by the app yet, but it works (limited for just the last transaction)

          :return: BalTransferSentResponse
        """
        data = self.get("/api/v1/transaction/transfer")
        return BalTransferSentResponse(data)

    def get_profile(self) -> Account:
        """
          Gets main account data

         :return: Account
          """
        data = self.get("/api/v1/profile/view")
        return Account(data)

    def get_recharge_history(self) -> RechargeHistory:
        """
          Gets the last time u charged your phone number with credits

         :return: RechargeHistory
        """
        data = self.get("/api/v1/transaction/recharge")
        return RechargeHistory(data)

    def get_subscriptions_history(self) -> BundleData:
        data = self.get("/api/v1/transaction/bundle")
        return BundleData(data)
