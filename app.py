from flask import Flask, render_template, request

app = Flask(__name__)

MALLA_SISTEMAS = {
    "I Semestre": ["Proyección e integración universitaria", "Comunicación y lenguaje I", "Introducción a las TIC", "A1 Communicative English", "Matemática básica", "Introducción a la programación", "Identidad nacional y orgullo patrio"],
    "II Semestre": ["Análisis y diseño de sistemas", "Programación estructurada", "Cálculo I", "A2 Communicative English", "Plataformas de colaboración digital", "Comunicación y lenguaje II", "Fundamentos de robótica", "Historia e identidad nacional"],
    "III Semestre": ["Base de datos I", "Metodología de la investigación", "A2+ Communicative English", "Cálculo II", "Estadística I", "Programación orientada a objetos", "Tecnología de redes I"],
    "IV Semestre": ["Álgebra lineal", "Tecnología de redes II", "Programación de aplicaciones de escritorio", "Administración de bases de datos", "B1 Communicative English", "Educación ambiental"],
    "V Semestre": ["Física aplicada", "B1+ Communicative English", "Desarrollo de aplicaciones móviles I", "Desarrollo web frontend", "Desarrollo de aplicaciones multimedia I", "Administración de servidores", "Ingeniería de software I"],
    "VI Semestre": ["Desarrollo de aplicaciones móviles II", "Desarrollo de aplicaciones multimedia II", "Ingeniería de software II", "B2 Communicative English", "Desarrollo web backend"],
    "VII Semestre": ["Planificación y organización informática", "Fundamentos de inteligencia artificial", "Seguridad y legislación informática", "Integración de tecnologías y plataformas", "Sistemas distribuidos"],
    "VIII Semestre": ["Machine Learning", "Negocio electrónico", "Auditoría informática", "Soluciones de inteligencia de negocios", "Gestión de servicios de TI"],
    "IX Semestre": ["Redes neuronales", "Gestión de proyectos tecnológicos", "Prácticas profesionales I", "Ingeniería de procesos de negocio", "Emprendedores"],
    "X Semestre": ["Culminación de estudios", "Automatización inteligente y minería de datos", "Prácticas profesionales II"]
}

@app.route("/", methods=["GET", "POST"])
def inicio():
    if request.method == "POST":
        nombre = request.form.get("nombre")
        carrera = request.form.get("carrera")
        anio = request.form.get("anio")
        promedio = int(request.form.get("promedio", 85))
        return render_template("resultado.html", nombre=nombre, carrera=carrera, anio=anio, promedio=promedio, malla=MALLA_SISTEMAS)
    return render_template("index.html")

@app.route("/recomendar", methods=["POST"])
def recomendar():
    nombre = request.form.get("nombre")
    carrera = request.form.get("carrera")
    anio = request.form.get("anio")
    promedio = int(request.form.get("promedio", 85))
    aprobadas = request.form.getlist("clases_aprobadas")
    
    limite_creditos = 18 if promedio >= 80 else 12 
    pendientes = []
    
    # Detección del semestre actual (el más bajo que tenga materias pendientes)
    semestre_detectado = "Completado"
    for sem, clases in MALLA_SISTEMAS.items():
        if any(c not in aprobadas for c in clases):
            semestre_detectado = sem
            break

    peso_semestre = 10 
    for semestre, clases in MALLA_SISTEMAS.items():
        for clase in clases:
            if clase not in aprobadas:
                creds = 4 if any(palabra in clase.lower() for palabra in ["programación", "cálculo", "datos", "redes", "física", "álgebra"]) else 3
                
                # El peso_semestre garantiza que siempre se prioricen las clases rezagadas o del semestre actual
                pendientes.append({
                    "nombre": clase,
                    "creditos": creds,
                    "profundidad": peso_semestre,
                    "etiqueta": "Materia Llave" if peso_semestre >= 8 else "Nivel Estándar"
                })
        peso_semestre -= 1
        
    pendientes.sort(key=lambda x: x['profundidad'], reverse=True)
    
    carga_ia = []
    total_creditos = 0
    
    for mat in pendientes:
        if total_creditos + mat['creditos'] <= limite_creditos:
            carga_ia.append(mat)
            total_creditos += mat['creditos']

    return render_template("resultado.html", nombre=nombre, carrera=carrera, anio=anio, promedio=promedio, malla=MALLA_SISTEMAS, carga_ia=carga_ia, total_creditos=total_creditos, max_creditos=limite_creditos, aprobadas=aprobadas, semestre_actual=semestre_detectado)

if __name__ == "__main__":
    app.run(debug=True)