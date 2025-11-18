from flask import Flask, render_template, request, redirect, url_for, flash, get_flashed_messages

import requests

app = Flask (__name__)

app.secret_key = 'TU_CLAVE_SECRETA_AQUI'
API="https://www.themealdb.com/api/json/v1/1/search.php?s="


@app.route('/')
def index():
    return render_template('index.html', meal=None, messages= get_flashed_messages(with_categories=True))

@app.route('/search', methods=['POST'])
def search_api_comida():
    comida_name=request.form.get('query','').strip().lower()
    if not comida_name:
        flash('Por favor,ingresa un nombre de comida o receta','error')
        return redirect(url_for('index'))

    try:
    
        resp = requests.get(f"{API}{comida_name}")
        
        if resp.status_code == 200:
            
            comida_data = resp.json()
        
            meals= comida_data.get('meals')
            
        if meals:
            return render_template('index.html',meal = meals[0], search_query=comida_name)
    
        else:
        
            flash(f'Receta"{comida_name}"no encontrado','error')
            return redirect(url_for('index'))
    
    except requests.exceptions.RequestException as e:
        flash('Error al buscar la receta','error')
    return redirect (url_for('index'))
if __name__ == '__main__':
    app.run(debug =True)
