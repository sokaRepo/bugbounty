from flask import Blueprint, render_template, request, session, redirect
from utils import *
from models import Programs, Info
from config import MAX_PROGRAMS_PER_PAGE


bl = Blueprint('bl', __name__)


@bl.route('/bountylist', methods=['GET'])
def show_bounty_list():
	# programs = get_bounty_programs(1)
	return render_template('index.html', programs=Programs.get_by_date_limit(1), page='bountylist.html', info=Info(), current_page=1, last_page=Programs.get_last_page())
