import flet as ft
from UI.view import View
from model.modello import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handle_graph(self, e):
        year = self._view.ddyear.value
        state = self._view.ddstate.value
        if year is None or state is None:
            self._view.create_alert("Inserire anno e stato")
            return
        self._model.build_graph(year, state)

        self._view.txt_result1.controls.clear()
        txt = self._model.print_graph()
        self._view.txt_result1.controls.append(ft.Text(txt))
        txt2 = self._model.conn_components()
        self._view.txt_result1.controls.append(ft.Text(txt2))
        self._view.update_page()


    def handle_path(self, e):
        if self._model.graph is None:
            self._view.create_alert("Creare il grafo")
        max_score, printable_path = self._model.find_path()
        txt = f"Il punteggio massimo è {max_score} e il percorso è {printable_path}"
        self._view.txt_result2.controls.append(ft.Text(txt))
        self._view.update_page()

    def fill_dd_year(self):
        self._view.ddyear.options.clear()
        years = self._model.get_years()
        for year in years:
            self._view.ddyear.options.append(ft.dropdown.Option(year))
        self._view.update_page()

    def fill_dd_state(self, e):
        self._view.ddstate.options.clear()
        year = self._view.ddyear.value
        states = self._model.get_states(year)
        for state in states:
            self._view.ddstate.options.append(ft.dropdown.Option(key=state.id, text=state.name))
        self._view.update_page()

