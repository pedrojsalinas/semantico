"""
Instalar despues de requerimientos esta libreria de la lengua de spacy

python -m spacy download es_core_news_sm
"""
import spacy
import es_core_news_sm
import rdflib
from rdflib.serializer import Serializer
# nlp = spacy.load("es_core_news_sm")
nlp = es_core_news_sm.load()
text = """El caso Receta de Arroz Verde 50 es una investigación publicada por el portal digital Mil Hojas. 
El portal digital reveló un correo electrónico recibido por Pamela Martínez supuesta asesora del expresidente Rafael Correa según Mil Hoja con un documento titulado Receta de Arroz Verde 502.  Según la investigación, el remitente del correo electrónico sería Geraldo Luiz Pereira de Souza- encargado de la administración y finanzas de Odebrecht en Ecuador. El mail demuestra presuntos aportes entregados por empresas multinacionales como Odebrecht al movimiento Alianza País desde noviembre de 2013 a febrero de 201 periodo en el que el expresidente Rafael Correa lideraba esa organización política. Según Mil Hojas, las donaciones alcanzarían los 11,6 millones de dólares. Las empresas que habrían realizado los aportes son: Constructora Norberto Odebrecht, SK Engineering & Construction, Sinohydro Corporation, Grupo Azul, Telconet, China International Water & Electric Corp-CWE."""

text = nlp(text)
tokenized_sentences = [sentence.text for sentence in text.sents]
g=rdflib.Graph()
g.parse("arroz_verde.rdf")
datos = []

for sentence in tokenized_sentences:
    for entity in nlp(sentence).ents:
        consulta = 'SELECT ?s ?p ?o  WHERE { ?s ?p ?o .FILTER regex(str(?s), "%s") .}'%(entity.text)
        for row in g.query(consulta):
            tripleta = []
            # print(entity.text)
            predicado = row.p.split("/")
            objeto = row.o.split("/")
            predicado = predicado[len(predicado)-1]
            objeto = objeto[len(objeto)-1]
            # print("\t predicado: "+predicado+" Objeto: "+objeto)

            tripleta.append(entity.text)
            tripleta.append(predicado)
            tripleta.append(objeto)
            datos.append(tripleta)
print(datos)



