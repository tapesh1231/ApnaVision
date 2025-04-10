from flask import Blueprint, render_template, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from app.models import User, Device
from app import db

admin = Blueprint('admin', __name__)

@admin.before_request
def before_request():
    if not current_user.is_admin:
        abort(403)

@admin.route('/admin')
@login_required
def admin_dashboard():
    users = User.query.all()
    devices = Device.query.all()
    return render_template('admin/dashboard.html', users=users, devices=devices)

@admin.route('/admin/user/<int:user_id>')
@login_required
def user_details(user_id):
    user = User.query.get_or_404(user_id)
    devices = Device.query.filter_by(user_id=user_id).all()
    return render_template('admin/user_details.html', user=user, devices=devices)

@admin.route('/admin/delete_user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.is_admin:
        flash('Cannot delete admin users', 'danger')
        return redirect(url_for('admin.admin_dashboard'))
    
    db.session.delete(user)
    db.session.commit()
    flash('User has been deleted', 'success')
    return redirect(url_for('admin.admin_dashboard'))