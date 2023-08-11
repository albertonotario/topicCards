# import the main window object (mw) from aqt
from aqt import mw
# import the "show info" tool from utils.py
from aqt.utils import showInfo, qconnect
# import all of the Qt GUI library
from aqt.qt import *
from aqt.reviewer import Reviewer
from anki.scheduler.v3 import Scheduler
from anki.scheduler.v3 import CardAnswer
from aqt import reviewer
from anki.consts import BUTTON_ONE

# We're going to add a menu item below. First we want to create a function to
# be called when the menu item is activated.
def searchTopic(card):

    note = card.note()
    fields = note.fields
    return fields[2]

# create a new menu item, "test"
action = QAction("test", mw)
# set it to call testFunction when it's clicked
qconnect(action.triggered, testFunction)
# and add it to the tools menu
mw.form.menuTools.addAction(action)


def process_cards(scheduler, number_of_cards):
    
    isFirstCard = True

    if mw.state == "review":
        card = mw.reviewer.card
        prev_topic = None
        if isFirstCard:
            topic = None


    while (prev_topic != topic) or isFirstCard:
    #for i in range(4):    
        # Obtener la siguiente tarjeta
        #showInfo("En bucle While")
        queued_card = scheduler.get_queued_cards()
        if not queued_card.cards:
            showInfo("No hay más tarjetas")
            break

       

        card = scheduler.getCard()
        if card is None:
            showInfo("No hay más tarjetas")
            break

        topic = searchTopic(card)

        #showInfo(f"Procesando tarjeta {card.id}")
        #showInfo(f"prev_topic = {prev_topic}")
        #showInfo(f"topic = {topic}")

        

        if topic == prev_topic and not isFirstCard:
            showInfo("Tarjeta encontrada")
            break
        else:    
            # Responder la tarjeta
            #showInfo("else final")
            states = scheduler.col._backend.get_scheduling_states(card.id)
            answer = scheduler.build_answer(card=card, states=states, rating=CardAnswer.AGAIN)
            if isFirstCard:
                prev_topic = topic
            topic = None

            isFirstCard = False
            scheduler.answer_card(answer)   





    showInfo("Procesamiento de tarjetas completo")
    mw.reviewer.card = card
    mw.reviewer.show()




def newAnswerCard(self, ease):
    sched = mw.col.sched

    if ease == BUTTON_ONE: # Botón "Otra vez"
        # Aquí va tu lógica cuando el usuario presiona "Otra vez"
        showInfo("El usuario presionó el botón 'Otra vez'.")
        process_cards(sched,4)


    # Luego puedes llamar al método original para mantener la funcionalidad normal
    originalAnswerCard(self, ease)

# Guardar una referencia al método original
originalAnswerCard = reviewer.Reviewer._answerCard

# Reemplazar el método original con tu versión personalizada
reviewer.Reviewer._answerCard = newAnswerCard