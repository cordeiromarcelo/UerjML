from flask import Blueprint, render_template, request, redirect, url_for
import os
import io
import json
import config

platform = Blueprint('platform', __name__, url_prefix='/')


@platform.route('/')
def index():
    return render_template('platform/index.html')
