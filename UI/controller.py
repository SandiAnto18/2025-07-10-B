import datetime

import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
    def fillDDCategories(self):
        categoria= self._model.getCategories()
        for c in categoria:
            self._view._ddcategory.options.append(ft.dropdown.Option(c))
    def handleCreaGrafo(self, e):
        # Leggo gli anni selezionati
        categoria= self._view._ddcategory.value
        start_date = self._view._dp1.value
        end_date = self._view._dp2.value

        # Costruisco il grafo
        self._model.buildGraph(categoria,start_date,end_date)

        # Pulisco i risultati precedenti
        self._view.txt_result.controls.clear()

        self._view.txt_result.controls.append(
            ft.Text("Date selezionate")
        )
        self._view.txt_result.controls.append(
            ft.Text(f"Start date:{self._view._dp1.value}")
        )
        self._view.txt_result.controls.append(
            ft.Text(f"End Date: {self._view._dp2.value}")
        )
        # Mostro il numero di nodi e archi
        self._view.txt_result.controls.append(
            ft.Text("Grafo correttamente creato:")
        )
        self._view.txt_result.controls.append(
            ft.Text(f"Numero di nodi: {self._model.getNumNodi()}")
        )
        self._view.txt_result.controls.append(
            ft.Text(f"Numero di archi: {self._model.getNumArchi()}")
        )

        self._view.update_page()

    def handleBestProdotti(self, e):

        risultati = self._model.i5prodottiPiuVenduti()

        self._view.txt_result.controls.append(
            ft.Text("I 5 prodotti piu venduti sono:")
        )

        for p,score in risultati:
            self._view.txt_result.controls.append(
                ft.Text(f" {p.product_name} with score: {score}")
            )


        self._view.update_page()

    def handleCercaCammino(self, e):
        pass



    def setDates(self):
        first, last = self._model.getDateRange()

        self._view._dp1.first_date = datetime.date(first.year, first.month, first.day)
        self._view._dp1.last_date = datetime.date(last.year, last.month, last.day)
        self._view._dp1.current_date = datetime.date(first.year, first.month, first.day)

        self._view._dp2.first_date = datetime.date(first.year, first.month, first.day)
        self._view._dp2.last_date = datetime.date(last.year, last.month, last.day)
        self._view._dp2.current_date = datetime.date(last.year, last.month, last.day)
