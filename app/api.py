from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.models import Device
from app import db

api = Blueprint('api', __name__)

@api.route('/api/devices', methods=['GET'])
@login_required
def get_devices():
    devices = Device.query.filter_by(user_id=current_user.id).all()
    return jsonify([{
        'id': device.id,
        'name': device.name,
        'type': device.device_type,
        'status': device.status,
        'ip': device.ip_address,
        'location': device.location
    } for device in devices])

@api.route('/api/device/<int:device_id>', methods=['GET', 'POST'])
@login_required
def control_device(device_id):
    device = Device.query.get_or_404(device_id)
    if device.owner != current_user:
        return jsonify({'error': 'Unauthorized'}), 403
    
    if request.method == 'POST':
        data = request.get_json()
        if 'status' in data:
            device.status = data['status']
            db.session.commit()
        
    return jsonify({
        'id': device.id,
        'name': device.name,
        'status': device.status,
        'message': 'Device updated successfully'
    })