# Create your views here
from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponse
from django.http import Http404

from django.http import JsonResponse
import rdflib
from rdflib.serializer import Serializer
from .forms import BuscadorForm

from django.template import loader
from django.views.generic import TemplateView
# spacy
import spacy
import es_core_news_sm


class IndexView(TemplateView):
    template_name = 'recog_entities/index.html'

    def get(self, request):
        my_title = "Caso Arroz Verde"
        form = BuscadorForm()
        return render(request, self.template_name, {"titulo": my_title, "form": form})

    def post(self, request):
        form = BuscadorForm(request.POST)
        my_title = "Caso Arroz Verde"
        if form.is_valid():
            nlp = es_core_news_sm.load()
            text = form.cleaned_data['query']
            textoInicial = form.cleaned_data['query']
            text = nlp(text)
            tokenized_sentences = [sentence.text for sentence in text.sents]
            print(tokenized_sentences)
            g = rdflib.Graph()
            g.parse("arroz_verde.rdf")
            datos = []
            form = BuscadorForm()

            for sentence in tokenized_sentences:
                for entity in nlp(sentence).ents:
                    consulta = 'SELECT ?s ?p ?o  WHERE { ?s ?p ?o .FILTER regex(str(?s), "%s") .}' % (
                        entity.text)
                    for row in g.query(consulta):
                        tripleta = []
                        predicado = row.p.split("/")
                        objeto = row.o.split("/")
                        predicado = predicado[len(predicado)-1]
                        objeto = objeto[len(objeto)-1]
                        tripleta.append(entity.text)
                        tripleta.append(predicado)
                        tripleta.append(objeto)
                        datos.append(tripleta)
            print(datos)
            args = {"titulo": my_title, "datos": datos,
                    "form": form, "textoInicial": textoInicial}
        return render(request, self.template_name, args)


class InfoView(TemplateView):
    def get(self,request):
        return render(request, "recog_entities/info.html", {"title": "¿Como se trabajo?"})


class LeeView(TemplateView):
    def get(self, request):
        g=rdflib.Graph()
        # lee el archivo rdf
        g.parse("Emancipada_final.rdf")

        # crea diccionario vacio
        data = {}
        # iteracion del rdf mediante consulta sparql
        for row in g.query(
                # obtiene predicado y objeto de la uri de datos de empacipada
                # Consulta de varios filtros
                'SELECT ?s ?p ?o  WHERE { ?s ?p ?o .FILTER regex(str(?s), "emancipada") .}'):
            # agrega datos a diccionario
            data[row.p] = row.o
            # retorna json con los datos obtenidos del
        return JsonResponse(data)
