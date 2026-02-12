import sys
import os
import json
import logging
from flask import Flask, render_template, redirect, url_for, flash

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

try:
    from discovery.main import run_discovery
except ImportError as e:
    logging.error(f"Не удалось импортировать discovery. Проверьте структуру: {e}")
    run_discovery = None

app = Flask(__name__)
app.secret_key = 'super-secret-key-for-flashing-messages'


DATA_FILE = os.path.join(project_root, 'data', 'discovery_output.json')

@app.template_filter('from_json')
def from_json_filter(value):
    try:
        return json.loads(value)
    except (json.JSONDecodeError, TypeError):
        return value


def load_resources():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


@app.route('/')
def index():
    data_exists = os.path.exists(DATA_FILE)
    return render_template('index.html', data_exists=data_exists)

@app.route('/discover')
def discover():
    if run_discovery:
        try:
            os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
            
            run_discovery()
            flash("Сбор данных успешно завершен!", "success")
        except Exception as e:
            flash(f"Ошибка при сборе данных: {str(e)}", "danger")
    else:
        flash("Ошибка: пакет discovery не найден.", "danger")
    
    return redirect(url_for('resources'))

@app.route('/resources')
def resources():
    data = load_resources()

    vpc_subnets = {}
    all_subnets = data.get('subnets', [])

    for subnet in all_subnets:
        vpc_id = subnet.get('vpc_id')

        if vpc_id:
            if vpc_id not in vpc_subnets:
                vpc_subnets[vpc_id] = []
            vpc_subnets[vpc_id].append(subnet)

    return render_template('resources.html', resources=data, vpc_subnets=vpc_subnets)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

