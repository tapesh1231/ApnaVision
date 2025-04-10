from flask import Blueprint, render_template, redirect, url_for, flash, abort, request
from flask_login import login_required, current_user
from app.models import Device
from app.forms import DeviceForm, AdvancedDeviceForm
from app import db

dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/dashboard')
@login_required
def index():
    devices = Device.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard/base.html', devices=devices)

@dashboard.route('/add_device', methods=['GET', 'POST'])
@login_required
def add_device():
    form = DeviceForm()
    if form.validate_on_submit():
        device = Device(name=form.name.data, 
                       device_type=form.device_type.data,
                       user_id=current_user.id)
        db.session.add(device)
        db.session.commit()
        flash('Device added successfully!', 'success')
        return redirect(url_for('dashboard.index'))
    return render_template('dashboard/add_device.html', form=form)

@dashboard.route('/control_device/<int:device_id>')
@login_required
def control_device(device_id):
    device = Device.query.get_or_404(device_id)
    if device.owner != current_user:
        abort(403)
    device.status = not device.status
    db.session.commit()
    return redirect(url_for('dashboard.index'))

@dashboard.route('/about')
@login_required
def about():
    return render_template('dashboard/about.html')

@dashboard.route('/contact')
@login_required
def contact():
    return render_template('dashboard/contact.html')

@dashboard.route('/device_details/<int:device_id>')
@login_required
def device_details(device_id):
    device = Device.query.get_or_404(device_id)
    if device.owner != current_user:
        abort(403)
    return render_template('dashboard/device_details.html', device=device)

@dashboard.route('/edit_device/<int:device_id>', methods=['GET', 'POST'])
@login_required
def edit_device(device_id):
    device = Device.query.get_or_404(device_id)
    if device.owner != current_user:
        abort(403)
    form = AdvancedDeviceForm()
    if form.validate_on_submit():
        device.name = form.name.data
        device.device_type = form.device_type.data
        device.ip_address = form.ip_address.data
        device.location = form.location.data
        db.session.commit()
        flash('Device updated successfully!', 'success')
        return redirect(url_for('dashboard.device_details', device_id=device.id))
    elif request.method == 'GET':
        form.name.data = device.name
        form.device_type.data = device.device_type
        form.ip_address.data = device.ip_address
        form.location.data = device.location
    return render_template('dashboard/edit_device.html', form=form, device=device)