from app.models import *
from app import db, app
from flask import redirect, url_for, abort, render_template, flash, request

if __name__ == '__main__':
    app.run(host='0.0.0.0')
