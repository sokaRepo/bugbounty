from flask import Blueprint, render_template, request
from utils import *
from json import dumps as jsonify

targets = Blueprint('targets', __name__)





@targets.route('/targets')
def index():
	if not user_auth():
		return redirect(url_for('index'))
	bounties_info, information_count, xsslab_info, xsslab_count, targets_info, targets_count = extract_db()
	return render_template('index.html', bounties=bounties_info, nbounties=information_count[0][0], ndollars=sum_reward(bounties_info), xsslab=xsslab_info, nxss=xsslab_count[0][0], targets=targets_info, ntargets=targets_count[0][0], page="targets.html" )
