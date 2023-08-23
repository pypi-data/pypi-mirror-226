class FlaskRequest():

    def __init__(self, request):
        self.args = request.args
        self.form = request.form
        self.json = request.json
        self.method = request.method
        self.headers = request.headers
        self.cookies = request.cookies
        self.files = request.files
        self.environ = request.environ
        self.remote_addr = request.remote_addr
        self.url = request.url
        self.base_url = request.base_url
        self.url_root = request.url_root
        self.host_url = request.host_url
        self.host = request.host
        self.script_root = request.script_root
        self.path = request.path
        self.full_path = request.full_path