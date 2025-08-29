class Pregunta:
    def __init__(self, pregunta, respuesta):
        self.pregunta = pregunta
        self.respuesta = respuesta

    def __repr__(self):
        return f"Pregunta('{self.pregunta}', '{self.respuesta}')"

import yaml

def cargar_preguntas(ruta_yaml):
    """
    Carga las preguntas desde un archivo YAML y devuelve una lista de objetos Pregunta.
    """
    with open(ruta_yaml, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    preguntas = []
    for item in data.get('problems', []):
        preguntas.append(Pregunta(item['question'], item['answer']))
    return preguntas

# Ejemplo de uso
if __name__ == "__main__":
    preguntas = cargar_preguntas('problems.yaml')
    for p in preguntas:
        print(p)
