from . import default
from flask import redirect, current_app, request, g
from ..components import get_saltapi

@default.route('/')
def home():
    # static_file = default.static_folder + '\\index.html'
    # static_file = "index.html"
    # return default.send_static_file(static_file)
    return redirect("/index.html")

@default.route('/salt/cmd',methods=['post'])
def saltcmd():
    # if saltapi is None:
    content = request.json
    saltapi = get_saltapi()
    result = saltapi.cmd(content["target"],content["fun"],content["arg"])
    return result
@default.route('/salt/minions')
def saltminions():
    # if saltapi is None:
    # content = request.json
    saltapi = get_saltapi()
    result = saltapi.get_minion_status()
    # result = saltapi.minion_alive()
    return result
@default.route('/salt/grains/')
def saltgrains():
    # if saltapi is None:
    # content = request.json
    target = request.args.get('target')
    saltapi = get_saltapi()
    result = saltapi.get_grains(target)
    return result
# import app
# from flask import send_file, render_template
# def configure_routes(app):

#     @app.route('/')
#     def index():
#         return send_file("..\\static\\index.html")
 
    # @app.route('/')
    # def index():
    #     return render_template('index.html')