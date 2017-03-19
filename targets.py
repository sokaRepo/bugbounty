from flask import Blueprint, render_template, request, redirect, url_for
from utils import *
from json import dumps as jsonify
from models import Info, Targets

targets = Blueprint('targets', __name__)





@targets.route('/targets')
def targets_index():
	if not user_auth():
		return redirect(url_for('index'))
	# bounties_info, information_count, xsslab_info, xsslab_count, targets_info, targets_count = extract_db()
	return render_template('index.html', page="targets.html", info=Info(), targets=Targets.get())
