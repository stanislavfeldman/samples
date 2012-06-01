from kiss.views.templates import TemplateResponse
from kiss.views.core import RedirectResponse
from kiss.controllers.core import Controller
from kiss.core.application import Application
from urllib import urlencode
import requests
import json
from db import DbHelper

google_options = {
	"authorization_uri": "https://accounts.google.com/o/oauth2/auth",
	"scope": "https://www.googleapis.com/auth/tasks",
	"get_token_uri": "https://accounts.google.com/o/oauth2/token",
	"redirect_uri": "http://localhost:8080/auth_usage/end",
	"client_id": "691519038986.apps.googleusercontent.com",
	"client_secret": "UsLDDLu-1ry8IgY88zy6qNiU",
	"target_uri": "https://www.googleapis.com/tasks/v1/lists/@default/tasks"
}

options = {
	"authorization_uri": "http://localhost:8080/auth/auth",
	"scope": "protected_api",
	"get_token_uri": "http://localhost:8080/auth/token",
	"redirect_uri": "http://localhost:8080/auth_usage/end",
	"client_id": "2",
	"client_secret": "secret2",
	"target_uri": "http://localhost:8080/api/protected"
}


class PageController(Controller):
	def get(self, request):
		return TemplateResponse("page.html")
	
class StartAuthController(Controller):
	def get(self, request):
		params = {
			"client_id": options["client_id"],
			"redirect_uri": options["redirect_uri"],
			"scope": options["scope"],
			"response_type": "code",
			"approval_prompt": "force",
			"access_type": "offline"
		}
		return RedirectResponse("%s?%s" % (options["authorization_uri"], urlencode(params)))
		

class EndAuthController(Controller):
	def get(self, request):
		params = {
			"client_id": options["client_id"],
			"client_secret": options["client_secret"],
			"grant_type": "authorization_code",
			"code": request.args["code"],
			"redirect_uri": options["redirect_uri"]
		}
		res = json.loads(requests.post(options["get_token_uri"], params).text)
		request.session["access_token"] = res["access_token"]
		print "access_token", request.session["access_token"]
		return RedirectResponse("/result")
		
		
class StartPasswordAuthController(Controller):
	def get(self, request):
		return TemplateResponse("user_password_auth.html")
		
	def post(self, request):
		params = {
			"client_id": "3",
			"client_secret": "secret3",
			"grant_type": "password",
			"username": request.form["username"],
			"password": DbHelper().hash_password(request.form["password"])
		}
		resp = requests.post(options["get_token_uri"], params).text
		res = json.loads(resp)
		if "access_token" in res:
			request.session["access_token"] = res["access_token"]
			print "access_token", request.session["access_token"]
		else:
			request.session["error"] = res
		return RedirectResponse("/result")

class ResultController(Controller):
	def get(self, request):
		if "access_token" in request.session and request.session["access_token"]:
			params = {"access_token": request.session["access_token"]}
			result = json.loads(requests.get("%s?%s" % (options["target_uri"], urlencode(params))).text)
		else:
			result = request.session["error"]
		return TemplateResponse("result.html", {"result": result})
		
		
class LogoutController(Controller):
	def get(self, request):
		request.session.delete()
		return RedirectResponse("/page")

