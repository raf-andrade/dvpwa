from argparse import ArgumentParser

from aiohttp.web import Application
from aiohttp_jinja2 import setup as setup_jinja
from jinja2.loaders import PackageLoader
from trafaret_config import commandline

from sqli.middlewares import session_middleware, error_middleware
from sqli.schema.config import CONFIG_SCHEMA
from sqli.services.db import setup_database
from sqli.services.redis import setup_redis
from sqli.utils.jinja2 import csrf_processor, auth_user_processor
from .routes import setup_routes


def init(argv):
    ap = ArgumentParser()
    commandline.standard_argparse_options(ap, default_config='./config/dev.yaml')
    options = ap.parse_args(argv)

    config = commandline.config_from_options(options, CONFIG_SCHEMA)

    app = Application(
        debug=True,
        middlewares=[
            session_middleware,
            # csrf_middleware,
            error_middleware,
        ]
    )
    app['config'] = config

    setup_jinja(app, loader=PackageLoader('sqli', 'templates'),
                context_processors=[csrf_processor, auth_user_processor],
                autoescape=False)
    setup_database(app)
    setup_redis(app)
    setup_routes(app)

    return app

def img_thumb(self, pk):
        item = self.datamodel.get(pk)
        mime_type = item.image.content_type
        return Response(
            item.image.thumbnail.read(), mimetype=mime_type, direct_passthrough=True
        )

def search_customer():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'Error': 'Not Authenticated!'}),403
    else:
        if not verify_jwt(token):
            return jsonify({'Error': 'Invalid Token'}),403
        else:
            content = request.json
            results = []
            if content:
                try:
                    search_term = content['search']
                    print(search_term)
                    str_query = "SELECT first_name, last_name, username FROM customer WHERE username = '%s';" % search_term
                    # mycust = Customer.query.filter_by(username = search_term).first()
                    # return jsonify({'Customer': mycust.username, 'First Name': mycust.first_name}),200

                    search_query = db.engine.execute(str_query)
                    for result in search_query:
                        results.append(list(result))
                    print(results)
                    return jsonify(results),200
