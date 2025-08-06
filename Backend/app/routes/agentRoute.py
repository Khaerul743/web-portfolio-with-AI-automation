from app.controllers import agentController
from flask import Blueprint

agentRoute = Blueprint("agentRoute", __name__)

agentRoute.route("/api/agent",methods=["POST"])(agentController.run_agent)
agentRoute.route("/api/agent/generate-blog",methods=["POST"])(agentController.generateBlog)
agentRoute.route("/api/agent/human-response",methods=["POST"])(agentController.humanResponse)
